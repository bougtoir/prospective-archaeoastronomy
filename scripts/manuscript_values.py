#!/usr/bin/env python3
"""Extract every number the manuscript quotes into manuscript/values.json.

No number may be hand-written into the manuscript: build_manuscript.py
interpolates only from this file.
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
OUT = ROOT / "manuscript" / "values.json"


def rnd(dfval, nd=4):
    return None if pd.isna(dfval) else round(float(dfval), nd)


def main():
    v = {}

    e1c = pd.read_csv(RES / "summary_e1c.csv")

    def cell(arch, t):
        r = e1c[(e1c.arch == arch) & (e1c.t == float(t))]
        return r.iloc[0] if len(r) else None

    for arch, key in [("M3_stars_50", "stars50"),
                      ("M5_quasars_50", "quasars50"),
                      ("M7_hybrid_all", "hybrid")]:
        for t in ["1e+04", "1e+05", "1e+06", "1e+07", "1e+08"]:
            r = cell(arch, t)
            if r is not None:
                v[f"{key}_p1_t{t}"] = rnd(r["p_err<1.0deg"])
                v[f"{key}_med_t{t}"] = rnd(r["median_err_deg"], 5)

    e1 = pd.read_csv(RES / "summary_e1.csv")
    r = e1[e1.arch == "M1_single_star"]
    v["single_star_p_invalid_mean"] = rnd(r["p_invalid"].mean())
    r = e1[(e1.arch == "M5_quasars_50") & (e1.t == 1e8)]
    v["quasars50_p1_t1e8_e1"] = rnd(r["p_err<1.0deg"].iloc[0])

    e2 = pd.read_csv(RES / "summary_e2.csv")
    for est in ["ls", "huber", "ransac"]:
        for pm in [0.0, 0.2, 0.5]:
            r = e2[(e2.arch == "M7_hybrid_all") & (e2.estimator == est)
                   & (e2.p_mismatch == pm)]
            if len(r):
                v[f"hybrid_{est}_pm{pm}"] = rnd(r["p_err<1.0deg"].iloc[0])

    e8 = pd.read_csv(RES / "summary_e8.csv")
    for _, r in e8.iterrows():
        key = "nc1" if "NC1" in r["scenario"] else "nc2"
        v[f"{key}_p1"] = rnd(r["p_err<1.0deg"])

    e9 = pd.read_csv(RES / "summary_e9.csv")
    for _, r in e9.iterrows():
        key = "chir_on" if bool(r["chirality"]) else "chir_off"
        v[f"{key}_p1"] = rnd(r["p_err<1.0deg"])
        v[f"{key}_pmirror_wrong"] = rnd(r["p_mirror_wrong"])

    e3 = pd.read_csv(RES / "summary_e3.csv")
    r = e3[(e3.severity == "baseline") & (e3.p_mismatch == 0.0)]
    v["hybrid_p1_t1e7_nomismatch"] = rnd(r["p_err<1.0deg"].iloc[0])
    r = e3[(e3.severity == "pessimistic") & (e3.p_mismatch == 0.5)]
    v["hybrid_p1_t1e7_worst"] = rnd(r["p_err<1.0deg"].iloc[0])

    e10 = pd.read_csv(RES / "summary_e10.csv")
    for cls in ["star", "quasar"]:
        for n in [1, 10, 50, 100]:
            r = e10[(e10.cls == cls) & (e10.n == n)]
            if len(r):
                v[f"{cls}_{n}_p1_t1e4"] = rnd(r["p_err<1.0deg"].iloc[0])

    e7 = pd.read_csv(RES / "summary_e7.csv")
    for t in [1e6, 1e7, 1e8]:
        d = e7[e7.t == t]
        i = d["p_err<1.0deg"].idxmax()
        r = d.loc[i]
        v[f"best_alloc_t{t:g}"] = (
            f"star {int(r.n_star)} + pulsar {int(r.n_pulsar)} + "
            f"quasar {int(r.n_quasar)} + galaxy {int(r.n_galaxy)}")
        v[f"best_alloc_p1_t{t:g}"] = rnd(r["p_err<1.0deg"])

    e6b = pd.read_csv(RES / "summary_e6b.csv")
    e6b = e6b[e6b.arch == "M5_quasars_50"]
    for mm in ["permutation", "substitution", "injection"]:
        for enc, tag in [("b_chir", "bchir"), ("knn_chir", "knnchir")]:
            r = e6b[(e6b.mismatch_model == mm) & (e6b.encoding == enc)]
            if len(r):
                v[f"edge_{tag}_{mm}_p1"] = rnd(r["p_err<1.0deg"].iloc[0])

    e6c = pd.read_csv(RES / "summary_e6c.csv")
    e6c = e6c[e6c.arch == "M5_quasars_50"]
    for enc, tag in [("b_chir", "bchir"), ("knn_chir", "knnchir")]:
        for bits in [8, 32]:
            r = e6c[(e6c.encoding == enc) & (e6c.prec_bits == bits)]
            if len(r):
                v[f"prec_{tag}_{bits}b_median_err"] = rnd(
                    r["median_err_deg"].iloc[0], 5)
                v[f"prec_{tag}_{bits}b_p01"] = rnd(r["p_err<0.1deg"].iloc[0])

    e11 = pd.read_csv(RES / "summary_e11.csv")
    for t in ["1e+03", "1e+04", "1e+05", "1e+06", "1e+07", "1e+08"]:
        r = e11[(e11.variant == "M1b") & (e11.t == float(t))]
        if len(r):
            v[f"m1b_p1_t{t}"] = rnd(r["p_err<1.0deg"].iloc[0])
            v[f"m1b_p_invalid_t{t}"] = rnd(r["p_invalid"].iloc[0])
            v[f"m1b_med_t{t}"] = rnd(r["median_err_deg"].iloc[0], 5)
    for t in ["1e+04", "1e+05", "1e+06"]:
        r = e11[(e11.variant == "M1b_subst0.5") & (e11.t == float(t))]
        if len(r):
            v[f"m1b_subst_p1_t{t}"] = rnd(r["p_err<1.0deg"].iloc[0])
            v[f"m1b_subst_med_t{t}"] = rnd(r["median_err_deg"].iloc[0], 5)

    # ---- Layer-2 calibration values (SMPT revision) -------------------------
    CAL = RES / "calibration"
    if (CAL / "calibrated_summary.csv").exists():
        import numpy as np
        proc = ROOT / "data" / "processed"
        gaia = pd.read_csv(proc / "gaia_dr3_bright.csv")
        atnf = pd.read_csv(proc / "atnf_pulsars.csv")
        icrf = pd.read_csv(proc / "icrf3_quasars.csv")
        v["cal_n_gaia"] = int(len(gaia))
        v["cal_n_atnf"] = int(len(atnf))
        v["cal_n_icrf3"] = int(len(icrf))
        v["cal_n_icrf3_defining"] = int(icrf.defining_flag.sum())
        v["cal_n_atnf_pm_meas"] = int(atnf.pm_tot_masyr.notna().sum())
        v["cal_atnf_pm_missing_frac"] = rnd(atnf.pm_tot_masyr.isna().mean(), 3)
        v["cal_star_med_pm"] = rnd(np.hypot(gaia.pmra_masyr,
                                          gaia.pmdec_masyr).median(), 2)
        v["cal_star_p90_pm"] = rnd(np.hypot(gaia.pmra_masyr,
                                          gaia.pmdec_masyr).quantile(0.9), 2)
        pm = atnf.pm_tot_masyr.dropna()
        v["cal_psr_med_pm"] = rnd(pm.median(), 1)
        v["cal_psr_p90_pm"] = rnd(pm.quantile(0.9), 0)
        v["cal_psr_median_age"] = float(atnf.age_yr.dropna().median())
        miss = pd.read_csv(CAL / "missingness_report.csv")
        for _, r in miss.iterrows():
            k = (f"miss_{r.catalogue}_{r.column}"
                 .replace("gaia_dr3_bright", "gaia")
                 .replace("atnf_pulsars", "atnf")
                 .replace("icrf3_quasars", "icrf3"))
            v[k] = rnd(r.frac_missing, 3)
        pc = pd.read_csv(CAL / "propagation_comparison.csv")
        for _, r in pc.iterrows():
            tag = f"{r.t_years:.0e}"
            v[f"prop_lin_deg_t{tag}"] = rnd(r.median_deg_angular_linear, 3)
            v[f"prop_3d_deg_t{tag}"] = rnd(r.median_deg_3d, 3)
            v[f"prop_diff_deg_t{tag}"] = rnd(r.median_abs_diff_deg, 4)
        cs = pd.read_csv(CAL / "calibrated_summary.csv")

        def c1(sc, t, col="p_err_lt1"):
            r = cs[(cs.scenario == sc) & (cs.t_years == float(t))]
            return rnd(r[col].iloc[0]) if len(r) else None

        for sc in ["C_star10", "C_star50", "C_star100", "C_pulsar10",
                   "C_pulsar50", "C_quasar10", "C_quasar50", "C_quasar100",
                   "C_hybrid_spq", "C_hybrid50",
                   "C_star50_opt", "C_pulsar50_opt", "C_quasar50_opt",
                   "S_star50", "S_pulsar50", "S_quasar50", "S_hybrid_all",
                   "S_hybrid_spq"]:
            key = sc.lower()
            for t in ["1e+03", "1e+04", "1e+05", "1e+06", "1e+07", "1e+08"]:
                val = c1(sc, float(t))
                if val is not None:
                    v[f"{key}_p1_t{t}"] = val
                    m = c1(sc, float(t), "median_err_deg")
                    if m is not None:
                        v[f"{key}_med_t{t}"] = m
        for est in ("ls", "huber", "ransac"):
            for pm_ in (0.0, 0.2, 0.5):
                val = c1(f"Cest_hybrid_{est}_pm{pm_}", 1e6)
                if val is not None:
                    v[f"cest_{est}_pm{pm_}_t1e+06"] = val
        for b in (8, 32):
            val = c1(f"Cprec_quasar50_{b}b", 1e4)
            if val is not None:
                v[f"cprec_q50_{b}b_t1e+04"] = val
            m = c1(f"Cprec_quasar50_{b}b", 1e4, "median_err_deg")
            if m is not None:
                v[f"cprec_q50_{b}b_med_t1e+04"] = m
        sens_path = CAL / "sensitivity_summary.csv"
        if sens_path.exists():
            ss = pd.read_csv(sens_path)
            for _, r in ss.iterrows():
                k = (r.scenario.lower().replace(".", "p")
                     .replace("s1_", "sens1_").replace("s2_", "sens2_")
                     .replace("s3_", "sens3_").replace("s4_", "sens4_")
                     .replace("s5_", "sens5_").replace("s6_", "sens6_"))
                v[f"{k}_p1_t{r.t_years:.0e}"] = rnd(r.p_err_lt1)
        tvc_path = CAL / "theory_vs_calibrated_findings.csv"
        if tvc_path.exists():
            tvc = pd.read_csv(tvc_path)
            for _, r in tvc.iterrows():
                v[f"tvc_{str(r.finding_id).lower()}"] = r.classification

    OUT.write_text(json.dumps(v, indent=2, sort_keys=True))
    print(f"{len(v)} values -> {OUT}")


if __name__ == "__main__":
    main()
