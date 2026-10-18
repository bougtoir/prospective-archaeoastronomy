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

    OUT.write_text(json.dumps(v, indent=2, sort_keys=True))
    print(f"{len(v)} values -> {OUT}")


if __name__ == "__main__":
    main()
