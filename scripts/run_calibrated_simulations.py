#!/usr/bin/env python3
"""Observation-calibrated validation experiments (SMPT revision, Layer 2).

Primary calibrated analysis: horizons 1e3..1e6 yr.
Extrapolative stress tests: 1e7, 1e8 yr (never reported as calibrated
forecasts — flagged in scenario names and summary columns).

Reads persisted processed catalogues only (data/processed/). No live API.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from proarch import calibration, simulation  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CAL = ROOT / "results" / "calibration"
MAS = calibration.MAS_YR_TO_RAD_YR

PRIMARY_T = [1e3, 1e4, 1e5, 1e6]
STRESS_T = [1e7, 1e8]


def base_kw(cfg):
    return dict(sigma_obs=cfg["sigma_obs_rad"],
                p_mismatch=cfg["p_mismatch_baseline"],
                mismatch_model=cfg["mismatch_model"],
                estimator=cfg["estimator_default"],
                chirality=cfg["chirality_default"],
                mirror_ambiguity=cfg["mirror_ambiguity"],
                bits=cfg["bits_default"])


N_OPT_ENSEMBLE = 25


def run_cal(name, counts, pools, t, n_mc, rng, kw, atnf_df, optimize=False):
    rows = []
    # D-optimal selection is a deterministic geometry operation on the pool;
    # rebuild it only N_OPT_ENSEMBLE times (an ensemble of selections) and
    # cycle reps through the ensemble. Per-source quasar drift draws are still
    # re-sampled every replication; measured star/pulsar drift is fixed.
    opt_pops = None
    if optimize:
        cls, n = next(iter(counts.items()))
        opt_pops = [calibration.build_calibrated_population(
            pools[cls], n, rng, optimize=True, cls=cls)
            for _ in range(N_OPT_ENSEMBLE)]
    for rep in range(n_mc):
        if opt_pops is not None:
            base = opt_pops[rep % N_OPT_ENSEMBLE]
            cal_pop = {k: (v.copy() if isinstance(v, np.ndarray) else v)
                       for k, v in base.items()}
            qmask = cal_pop["labels"] == "quasar"
            if qmask.any():
                cal_pop["drift_rad_per_yr"][qmask] = (
                    calibration.quasar_motion(np.zeros(int(qmask.sum())), rng))
        elif len(counts) == 1:
            cls, n = next(iter(counts.items()))
            cal_pop = calibration.build_calibrated_population(
                pools[cls], n, rng, optimize=optimize, cls=cls)
        else:
            cal_pop = calibration.build_calibrated_hybrid(pools, counts, rng)
        r = simulation.run_replication(
            {}, t, rng, cal_pop=cal_pop,
            p_use_fn=lambda lab, tt: calibration.usability_vector(
                lab, tt, atnf_df), **kw)
        r["scenario"] = name
        r["t_years"] = t
        r["rep"] = rep
        rows.append(r)
    return pd.DataFrame(rows)


def run_synth(name, spec, t, n_mc, rng, kw):
    rows = []
    for rep in range(n_mc):
        r = simulation.run_replication(spec, t, rng, **kw)
        r["scenario"] = name
        r["t_years"] = t
        r["rep"] = rep
        rows.append(r)
    return pd.DataFrame(rows)


def summarize(df):
    def p_lt(x, thr):
        x = np.asarray(x, dtype=float)
        return float(np.nanmean(x < thr)) if np.isfinite(x).any() else np.nan
    g = df.groupby(["scenario", "t_years"], as_index=False).agg(
        n=("err_deg", "size"),
        p_err_lt1=("err_deg", lambda s: p_lt(s, 1.0)),
        p_err_lt0p1=("err_deg", lambda s: p_lt(s, 0.1)),
        median_err_deg=("err_deg", "median"),
        mean_usable=("n_usable", "mean"),
        p_invalid=("success", lambda s: float((~s.astype(bool)).mean())))
    g["regime"] = np.select(
        [g.t_years <= 1e5, g.t_years == 1e6],
        ["observation_anchored", "extended_projection"],
        default="extrapolative_stress")
    return g


def propagation_comparison(gaia, out):
    """Angular-linear vs 3D Cartesian constant-velocity propagation on the
    RV-measured subset of the Gaia sample."""
    sub = gaia.dropna(subset=["radial_velocity_kms", "parallax_mas"])
    sub = sub[sub["parallax_mas"] > 0]
    ra = np.deg2rad(sub["ra_deg"].to_numpy())
    dec = np.deg2rad(sub["dec_deg"].to_numpy())
    q = calibration.radec_to_unit(sub["ra_deg"], sub["dec_deg"])
    pm_tot = np.hypot(sub["pmra_masyr"], sub["pmdec_masyr"]).to_numpy()
    d_pc = 1000.0 / sub["parallax_mas"].to_numpy()
    d_kpc = d_pc / 1000.0
    pmra = sub["pmra_masyr"].to_numpy()
    pmdec = sub["pmdec_masyr"].to_numpy()
    vr = sub["radial_velocity_kms"].to_numpy()
    era = np.stack([-np.sin(ra), np.cos(ra), np.zeros_like(ra)], axis=1)
    edec = np.stack([-np.sin(dec) * np.cos(ra),
                     -np.sin(dec) * np.sin(ra), np.cos(dec)], axis=1)
    udir = q
    # Cartesian constant-velocity model: v_t = 4.74047 * pm(mas/yr) * d(kpc)
    v = (4.74047 * pmra[:, None] * d_kpc[:, None] * era
         + 4.74047 * pmdec[:, None] * d_kpc[:, None] * edec
         + vr[:, None] * udir)  # km/s
    KM_S_TO_PC_YR = 1.022712165e-6
    r0 = q * d_pc[:, None]
    rows = []
    for t in [1e3, 1e4, 1e5, 1e6]:
        # angular-linear: displacement angle = pm_tot(mas/yr)*t -> rad
        d_ang = pm_tot * t * MAS
        # 3D constant velocity
        r1 = r0 + v * KM_S_TO_PC_YR * t
        q1 = r1 / np.linalg.norm(r1, axis=1, keepdims=True)
        cosd = np.clip(np.sum(q1 * q, axis=1), -1, 1)
        d_3d = np.arccos(cosd)
        rows.append(dict(t_years=t, n_stars=len(sub),
                         median_deg_angular_linear=float(
                             np.median(np.degrees(d_ang))),
                         p90_deg_angular_linear=float(
                             np.quantile(np.degrees(d_ang), 0.9)),
                         median_deg_3d=float(np.median(np.degrees(d_3d))),
                         p90_deg_3d=float(
                             np.quantile(np.degrees(d_3d), 0.9)),
                         median_abs_diff_deg=float(np.median(np.abs(
                             np.degrees(d_3d - d_ang))))))
    df = pd.DataFrame(rows)
    df.to_csv(out, index=False)
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(ROOT / "configs/default.yaml"))
    ap.add_argument("--n-mc", type=int, default=None)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--sensitivity", action="store_true",
                    help="run the sensitivity branch instead of the primary grid")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config))
    kw = base_kw(cfg)
    n_mc = args.n_mc or (500 if args.quick else cfg["n_mc"])
    seed = cfg["master_seed"] + 5555
    CAL.mkdir(parents=True, exist_ok=True)

    gaia = calibration.load_catalogue("gaia_dr3_bright")
    atnf = calibration.load_catalogue("atnf_pulsars")
    icrf3 = calibration.load_catalogue("icrf3_quasars")
    atnf_meas, atnf_miss = calibration.pulsar_motion(atnf)

    # --- missingness report -------------------------------------------------
    miss_rows = []
    for name, df, cols in [
            ("gaia_dr3_bright", gaia,
             ["pmra_masyr", "pmdec_masyr", "parallax_mas",
              "radial_velocity_kms", "ruwe"]),
            ("atnf_pulsars", atnf,
             ["p0_s", "p1_ss", "pm_tot_masyr", "age_yr",
              "dist_kpc", "dist1_kpc"]),
            ("icrf3_quasars", icrf3,
             ["dec_unc_arcsec", "ra_unc_s", "n_sessions"])]:
        for c in cols:
            if c in df.columns:
                miss_rows.append(dict(catalogue=name, column=c,
                                      n_total=len(df),
                                      n_missing=int(df[c].isna().sum()),
                                      frac_missing=float(df[c].isna().mean())))
    pd.DataFrame(miss_rows).to_csv(CAL / "missingness_report.csv", index=False)

    # --- source-motion calibration summary ----------------------------------
    rows = [calibration.motion_summary(
                "star", calibration.star_motion(gaia),
                "Gaia DR3 bright sample (measured)"),
            calibration.motion_summary(
                "pulsar", atnf_meas["pm_tot_masyr"].to_numpy(),
                f"ATNF PMTOT measured subset "
                f"(n_missing={len(atnf_miss)} excluded)"),
            calibration.motion_summary(
                "quasar_prior_masyr",
                10 ** np.linspace(-3, -1, 1000),
                "log-uniform literature prior 1e-3..1e-1 mas/yr")]
    pd.DataFrame(rows).to_csv(CAL / "source_motion_calibration.csv",
                              index=False)
    calibration.write_registry()
    calibration.write_classification()

    # --- angular-linear vs 3D propagation comparison ------------------------
    propagation_comparison(gaia, CAL / "propagation_comparison.csv")

    pools = {"star": gaia, "pulsar": atnf_meas, "quasar": icrf3}

    if args.sensitivity:
        sens = []
        rng = np.random.default_rng(seed + 900)
        # S1: pulsars including PM-missing resampled from measured PMTOT CDF
        pm_cdf = np.sort(atnf_meas["pm_tot_masyr"].to_numpy())
        for t in PRIMARY_T + STRESS_T:
            for rep in range(min(n_mc, 1000)):
                sub = atnf.sample(50, random_state=rng.integers(2**31))
                pm = sub["pm_tot_masyr"].to_numpy()
                fill = rng.uniform(0, 1, len(sub))
                pm = np.where(np.isnan(pm), np.quantile(pm_cdf, fill), pm)
                cal_pop = {"Q": calibration.radec_to_unit(
                               sub["ra_deg"], sub["dec_deg"]),
                           "labels": np.array(["pulsar"] * len(sub)),
                           "drift_rad_per_yr": pm * MAS}
                r = simulation.run_replication(
                    {}, t, rng, cal_pop=cal_pop,
                    p_use_fn=lambda lab, tt: calibration.usability_vector(
                        lab, tt, atnf), **kw)
                r["scenario"] = "S1_pulsar50_missingPM_resampled"
                r["t_years"] = t
                sens.append(r)
        # S2: star existence tau low/high
        for tau in calibration.STAR_EXIST_TAU_RANGE_YR:
            for t in PRIMARY_T + STRESS_T:
                for rep in range(min(n_mc, 500)):
                    cal_pop = calibration.build_calibrated_population(
                        pools["star"], 50, rng, cls="star")
                    r = simulation.run_replication(
                        {}, t, rng, cal_pop=cal_pop,
                        p_use_fn=lambda lab, tt: np.full(
                            len(lab), calibration.star_exists(tt, tau)), **kw)
                    r["scenario"] = f"S2_star50_tau{tau:.0e}"
                    r["t_years"] = t
                    sens.append(r)
        # S3: pulsar existence k low/high
        for k_ in calibration.PSR_EXIST_K_RANGE:
            for t in PRIMARY_T + STRESS_T:
                for rep in range(min(n_mc, 500)):
                    cal_pop = calibration.build_calibrated_population(
                        pools["pulsar"], 50, rng, cls="pulsar")
                    r = simulation.run_replication(
                        {}, t, rng, cal_pop=cal_pop,
                        p_use_fn=lambda lab, tt: np.full(
                            len(lab), calibration.pulsar_exists(
                                tt, atnf, k_)), **kw)
                    r["scenario"] = f"S3_pulsar50_k{k_}"
                    r["t_years"] = t
                    sens.append(r)
        # S5: Gaia quality-cut sensitivity -- stricter astrometric subset
        gaia_hq = gaia[(gaia["ruwe"] <= 1.1)
                       & (gaia["visibility_periods_used"] >= 10)]
        for t in PRIMARY_T:
            for rep in range(min(n_mc, 500)):
                cal_pop = calibration.build_calibrated_population(
                    gaia_hq, 50, rng, cls="star")
                r = simulation.run_replication(
                    {}, t, rng, cal_pop=cal_pop,
                    p_use_fn=lambda lab, tt: calibration.usability_vector(
                        lab, tt, atnf), **kw)
                r["scenario"] = "S5_star50_strict"
                r["t_years"] = t
                sens.append(r)
        # S6: ICRF3 defining-source subset vs full catalogue
        icrf_def = icrf3[icrf3["defining_flag"] == True]  # noqa: E712
        for t in PRIMARY_T + STRESS_T:
            for rep in range(min(n_mc, 500)):
                cal_pop = calibration.build_calibrated_population(
                    icrf_def, 50, rng, cls="quasar")
                cal_pop["drift_rad_per_yr"] = calibration.quasar_motion(
                    np.zeros(50), rng)
                r = simulation.run_replication(
                    {}, t, rng, cal_pop=cal_pop,
                    p_use_fn=lambda lab, tt: np.ones(len(lab)), **kw)
                r["scenario"] = "S6_quasar50_defining"
                r["t_years"] = t
                sens.append(r)
        # S4: quasar drift prior x0.1 / x10
        for scale in (0.1, 10.0):
            for t in STRESS_T:
                for rep in range(min(n_mc, 500)):
                    cal_pop = calibration.build_calibrated_population(
                        pools["quasar"], 50, rng, cls="quasar")
                    cal_pop["drift_rad_per_yr"] = (
                        cal_pop["drift_rad_per_yr"] * scale)
                    r = simulation.run_replication(
                        {}, t, rng, cal_pop=cal_pop,
                        p_use_fn=lambda lab, tt: np.ones(len(lab)), **kw)
                    r["scenario"] = f"S4_quasar50_driftx{scale}"
                    r["t_years"] = t
                    sens.append(r)
        df = pd.DataFrame(sens)
        df.to_csv(CAL / "sensitivity_reps.csv", index=False)
        summarize(df).to_csv(CAL / "sensitivity_summary.csv", index=False)
        print("sensitivity done:", len(df))
        return

    # --- primary calibrated grid -------------------------------------------
    nets = []
    for n in (10, 50, 100):
        nets.append((f"C_star{n}", {"star": n}, True))
    for n in (10, 50):
        nets.append((f"C_pulsar{n}", {"pulsar": n}, True))
    for n in (10, 50, 100):
        nets.append((f"C_quasar{n}", {"quasar": n}, True))
    nets.append(("C_hybrid_spq", {"star": 10, "pulsar": 10, "quasar": 10},
                 False))
    # equal-count heterogeneous comparison for C_quasar50 (finding F)
    nets.append(("C_hybrid50", {"star": 20, "pulsar": 10, "quasar": 20},
                 False))

    frames = []
    rng = np.random.default_rng(seed)
    for name, counts, optimizable in nets:
        for opt in ([False, True] if optimizable else [False]):
            for t in PRIMARY_T + STRESS_T:
                tag = name + ("_opt" if opt else "")
                frames.append(run_cal(tag, counts, pools, t, n_mc, rng,
                                      kw, atnf, optimize=opt))
        print("done", name)

    # --- calibrated estimator and precision comparisons ---------------------
    # Finding D (robust estimators under misidentification) and finding E
    # (finite precision) assessed on observed populations.
    for est in ("ls", "huber", "ransac"):
        for pm in (0.0, 0.2, 0.5):
            kwx = dict(kw, estimator=est, p_mismatch=pm)
            for t in PRIMARY_T:
                frames.append(run_cal(
                    f"Cest_hybrid_{est}_pm{pm}",
                    {"star": 10, "pulsar": 10, "quasar": 10},
                    pools, t, n_mc, rng, kwx, atnf))
        print("done estimator", est)
    for bits in (8, 32):
        kwx = dict(kw, bits=bits)
        for t in (1e4,):
            frames.append(run_cal(f"Cprec_quasar50_{bits}b",
                                  {"quasar": 50}, pools, t, n_mc, rng,
                                  kwx, atnf))
    print("done precision")

    # --- equal-count synthetic matched comparisons --------------------------
    matched = {"S_star50": {"star": 50}, "S_pulsar50": {"pulsar": 50},
               "S_quasar50": {"quasar": 50},
               "S_hybrid_all": {"star": 5, "pulsar": 5, "quasar": 10,
                                "galaxy": 10},
               "S_hybrid_spq": {"star": 10, "pulsar": 10, "quasar": 10}}
    for name, spec in matched.items():
        for t in PRIMARY_T + STRESS_T:
            frames.append(run_synth(name, spec, t, n_mc, rng, kw))
        print("done", name)

    reps = pd.concat(frames, ignore_index=True)
    reps.to_csv(CAL / "calibrated_reps.csv", index=False)
    summarize(reps).to_csv(CAL / "calibrated_summary.csv", index=False)
    print("total reps:", len(reps))


if __name__ == "__main__":
    main()
