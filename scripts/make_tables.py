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
    write(piv.reset_index(), "table3_performance")

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
    write(pd.DataFrame(rows), "table4_sensitivity")
    print("tables written")


if __name__ == "__main__":
    main()
