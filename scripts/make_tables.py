#!/usr/bin/env python3
"""Generate Tables 1-4 (CSV + LaTeX) from results and architecture defs."""
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from proarch import architectures  # noqa

ROOT = Path(__file__).resolve().parents[1]
RES, TAB = ROOT / "results", ROOT / "tables"
TAB.mkdir(exist_ok=True)


def write(df, name):
    df.to_csv(TAB / f"{name}.csv", index=False)
    try:
        df.to_latex(TAB / f"{name}.tex", index=False, escape=False)
    except Exception:
        pass


def main():
    # Table 1: architecture definitions
    desc = {
        "M1_single_star": "single stellar landmark",
        "M2_star_triangle": "stellar triangle",
        "M3_stars_10": "stellar network, n=10",
        "M3_stars_20": "stellar network, n=20",
        "M3_stars_50": "stellar network, n=50",
        "M3_stars_100": "stellar network, n=100",
        "M4_pulsars_10": "pulsar network, n=10",
        "M4_pulsars_20": "pulsar network, n=20",
        "M4_pulsars_50": "pulsar network, n=50",
        "M5_quasars_10": "quasar (ICRF-like) network, n=10",
        "M5_quasars_20": "quasar (ICRF-like) network, n=20",
        "M5_quasars_50": "quasar (ICRF-like) network, n=50",
        "M5_quasars_100": "quasar (ICRF-like) network, n=100",
        "M6_galaxies_10": "galaxy/cluster network, n=10",
        "M6_galaxies_20": "galaxy/cluster network, n=20",
        "M6_galaxies_50": "galaxy/cluster network, n=50",
        "M7_hybrid_pq": "hybrid: 10 pulsars + 10 quasars",
        "M7_hybrid_spq": "hybrid: 10 stars + 10 pulsars + 10 quasars",
        "M7_hybrid_all": "hybrid: 5 stars + 5 pulsars + 10 quasars + 10 galaxies",
    }
    rows = []
    for name, spec in architectures.ARCHITECTURES.items():
        r = {"architecture": name, "description": desc.get(name, "")}
        for c in ("star", "pulsar", "quasar", "galaxy"):
            r[f"n_{c}"] = spec.get(c, 0)
        r["n_total"] = sum(spec.values())
        rows.append(r)
    rows.append({"architecture": "M1b_direct_axis_landmark",
                 "description": "direct-axis landmark control (direction "
                                "defines axis; benchmark only)",
                 "n_star": 1, "n_pulsar": 0, "n_quasar": 0, "n_galaxy": 0,
                 "n_total": 1})
    write(pd.DataFrame(rows), "table1_architectures")

    # Table 2: scenario parameters
    cfg = yaml.safe_load(open(ROOT / "configs/default.yaml"))
    rows = [
        ("time grid (yr)", "1e3, 1e4, 1e5, 1e6, 1e7, 1e8"),
        ("N_MC default", cfg["n_mc"]),
        ("N_MC core scenarios", cfg["n_mc_core"]),
        ("sigma_obs baseline (rad)", cfg["sigma_obs_rad"]),
        ("p_mismatch baseline", cfg["p_mismatch_baseline"]),
        ("mismatch model", cfg["mismatch_model"]),
        ("severity levels", "pessimistic / baseline / optimistic"),
        ("estimators", "LS, Huber (IRLS), RANSAC"),
        ("primary outcome", "P(eps_theta < 1 deg), Wilson 95% CI"),
        ("master seed", cfg["master_seed"]),
        ("star drift (rad/yr)", "5e-7 (scenario assumption)"),
        ("pulsar drift (rad/yr)", "1e-7"),
        ("quasar drift (rad/yr)", "1e-9"),
        ("galaxy/cluster drift (rad/yr)", "2e-9"),
        ("usability tau star (yr)", "3e5"),
        ("usability tau pulsar (yr)", "3e6"),
        ("usability tau quasar (yr)", "3e8"),
        ("usability tau galaxy (yr)", "1e8"),
    ]
    write(pd.DataFrame(rows, columns=["parameter", "value"]),
          "table2_parameters")

    # Table 3: main performance p<1deg (core scenarios, n_mc_core)
    s = pd.read_csv(RES / "summary_e1c.csv")
    piv = s.pivot(index="arch", columns="t", values="p_err<1.0deg")
    piv.columns = [f"{t:.0e}" for t in piv.columns]
    write(piv.reset_index(), "table5_performance")

    # Table 4: sensitivity/falsification summary
    e2 = pd.read_csv(RES / "summary_e2.csv")
    e8 = pd.read_csv(RES / "summary_e8.csv")
    e9 = pd.read_csv(RES / "summary_e9.csv")
    rows = []
    for _, r in e2.iterrows():
        rows.append({"experiment": "estimator",
                     "condition": f"{r.arch}/{r.estimator}/pm={r.p_mismatch}",
                     "p_err_lt_1deg": r["p_err<1.0deg"],
                     "median_err_deg": r["median_err_deg"]})
    for _, r in e8.iterrows():
        rows.append({"experiment": "negative_control",
                     "condition": r["scenario"],
                     "p_err_lt_1deg": r["p_err<1.0deg"],
                     "median_err_deg": r["median_err_deg"]})
    for _, r in e9.iterrows():
        rows.append({"experiment": "chirality",
                     "condition": f"chirality={r.chirality}",
                     "p_err_lt_1deg": r["p_err<1.0deg"],
                     "median_err_deg": r["median_err_deg"]})
    write(pd.DataFrame(rows), "table6_sensitivity")

    # ---- Layer-2 calibration tables (SMPT revision) ------------------------
    CAL = RES / "calibration"
    if (CAL / "calibrated_summary.csv").exists():

        # Table 5: data sources and calibration variables
        ledger = pd.read_csv(ROOT / "data" / "acquisition_ledger.csv")
        cat_rows = []
        proc = {
            "gaia_slices": ("Gaia DR3 (gaiadr3.gaia_source)",
                            "sky-tiling source_id slices, TOP 100 brightest "
                            "per slice; G<12, parallax>0.1 mas, ruwe<1.4, "
                            "visibility_periods>8",
                            "positions, proper motions, parallax, RV, G mag, "
                            "ruwe, astrometric_excess_noise"),
            "icrf3k": ("ICRF3-K (IERS)",
                       "full K-band catalogue",
                       "positions, defining-source flag, formal "
                       "uncertainties, RA-Dec correlation, observing span"),
            "atnf_psrcat_short": ("ATNF Pulsar Catalogue v1.71",
                                  "psrcat proc_form short export",
                                  "positions, P, Pdot, PMRA/PMDec/PMTot, "
                                  "characteristic age, distances"),
        }
        for _, r in ledger.iterrows():
            key = next((k for k in proc if k in str(r["local_path"])), None)
            if key:
                name, q, cols = proc[key]
                cat_rows.append({
                    "catalogue": name, "query_or_snapshot": q,
                    "fields_used": cols,
                    "acquired_utc": r["fetched_utc"],
                    "sha256": r["sha256"][:12]})
        write(pd.DataFrame(cat_rows), "table3_data_sources")

        # Table 6: parameter classification (from generated CSV)
        write(pd.read_csv(CAL / "calibration_parameter_classification.csv"),
              "table4_parameter_classification")

        # Table 7: synthetic vs calibrated assumptions
        srows = [
            ("star drift", "5e-7 rad/yr fixed",
             "measured Gaia |PM| per source (observed)"),
            ("pulsar drift", "1e-7 rad/yr fixed",
             "measured ATNF PMTOT; missing reported, resampled only in "
             "sensitivity S1 (observed)"),
            ("quasar drift", "1e-9 rad/yr fixed",
             "log-uniform 1e-3..1e-1 mas/yr prior; ICRF3 uncertainties + "
             "literature (literature-constrained)"),
            ("star usability", "Weibull tau=3e5 yr",
             "exists exp(-t/5e9 yr) literature tau, sensitivity 5e8..2e10"),
            ("pulsar usability", "Weibull tau=3e6 yr",
             "exists exp(-t/(k*median AGE)), ATNF-derived scale, k in "
             "0.3..3 (derived)"),
            ("quasar usability", "Weibull tau=3e8 yr",
             "exists = 1 (conditional persistence assumption)"),
            ("galaxy/cluster", "2e-9 rad/yr, tau=1e8 yr",
             "not credibly calibratable: removed from primary "
             "(sensitivity-only)"),
            ("sky geometry", "isotropic on sphere",
             "actual catalogue sky positions (observed, anisotropic for "
             "ICRF3)"),
        ]
        write(pd.DataFrame(
            srows, columns=["parameter", "synthetic_assumption",
                            "calibrated_treatment"]),
              "table7_synth_vs_cal")

        # Table 8: primary calibrated results
        cs = pd.read_csv(CAL / "calibrated_summary.csv")
        prim = cs[(cs.regime.isin(["observation_anchored", "extended_projection"]))
                  & cs.scenario.str.startswith("C_")]
        piv = prim.pivot_table(index="scenario", columns="t_years",
                               values="p_err_lt1")
        piv.columns = [f"{t:.0e}" for t in piv.columns]
        write(piv.reset_index(), "table8_calibrated_primary")

        # Table 9: theory vs calibrated findings
        write(pd.read_csv(CAL / "theory_vs_calibrated_findings.csv"),
              "table9_theory_vs_calibrated")
    print("tables written")


if __name__ == "__main__":
    main()
