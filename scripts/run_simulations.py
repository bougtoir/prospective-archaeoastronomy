#!/usr/bin/env python3
"""Run the full Monte Carlo experiment grid -> results/*.csv (per-replication)."""
import argparse
import itertools
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from proarch import architectures, simulation  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"


def scenario_name(*parts):
    return "|".join(str(p) for p in parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(ROOT / "configs/default.yaml"))
    ap.add_argument("--n-mc", type=int, default=None)
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config))
    n_mc = args.n_mc or (500 if args.quick else cfg["n_mc"])
    n_mc_core = 500 if args.quick else cfg["n_mc_core"]
    T = cfg["time_grid_years"]
    base = dict(severity=cfg["severity_baseline"],
                sigma_obs=cfg["sigma_obs_rad"],
                p_mismatch=cfg["p_mismatch_baseline"],
                mismatch_model=cfg["mismatch_model"],
                estimator=cfg["estimator_default"],
                chirality=cfg["chirality_default"],
                mirror_ambiguity=cfg["mirror_ambiguity"],
                bits=cfg["bits_default"])
    A = architectures.ARCHITECTURES
    RES.mkdir(exist_ok=True)
    seed = cfg["master_seed"]

    # ---------- E1: architecture x time grid (main result) ----------
    sc = []
    for arch, t in itertools.product(A, T):
        sc.append(dict(name=scenario_name("E1", arch, t), spec=A[arch],
                       t_years=t, **base))
    df = simulation.run_grid(sc, n_mc, seed); seed += 100000
    df.to_csv(RES / "e1_architecture_time.csv", index=False)
    print(f"E1 done: {len(df)} reps")

    # ---------- E1c: core headline scenarios at n_mc_core ----------
    core = ["M3_stars_50", "M5_quasars_50", "M7_hybrid_all"]
    sc = [dict(name=scenario_name("E1c", a, t), spec=A[a], t_years=t, **base)
          for a, t in itertools.product(core, T)]
    df = simulation.run_grid(sc, n_mc_core, seed); seed += 100000
    df.to_csv(RES / "e1c_core.csv", index=False)
    print(f"E1c done: {len(df)} reps")

    # ---------- E2: estimator comparison ----------
    est_arch = ["M3_stars_50", "M5_quasars_50", "M7_hybrid_all"]
    sc = []
    for a, est, pm in itertools.product(est_arch,
                                        ["ls", "huber", "ransac"],
                                        [0.0, 0.05, 0.2, 0.5]):
        kw = dict(base, estimator=est, p_mismatch=pm)
        sc.append(dict(name=scenario_name("E2", a, est, pm),
                       spec=A[a], t_years=1e6, **kw))
    df = simulation.run_grid(sc, n_mc, seed); seed += 100000
    df.to_csv(RES / "e2_estimators.csv", index=False)
    print(f"E2 done: {len(df)} reps")

    # ---------- E3: mismatch x severity heatmap ----------
    sc = []
    for sev, pm in itertools.product(
            ["pessimistic", "baseline", "optimistic"],
            [0.0, 0.01, 0.05, 0.10, 0.20, 0.30, 0.50]):
        kw = dict(base, severity=sev, p_mismatch=pm)
        sc.append(dict(name=scenario_name("E3", sev, pm),
                       spec=A["M7_hybrid_all"], t_years=1e7, **kw))
    df = simulation.run_grid(sc, n_mc, seed); seed += 100000
    df.to_csv(RES / "e3_heatmap.csv", index=False)
    print(f"E3 done: {len(df)} reps")

    # ---------- E4: observational-noise sweep ----------
    sc = []
    for s_obs in [0.0, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2]:
        kw = dict(base, sigma_obs=s_obs, p_mismatch=0.0)
        sc.append(dict(name=scenario_name("E4", s_obs),
                       spec=A["M7_hybrid_all"], t_years=1e6, **kw))
    df = simulation.run_grid(sc, n_mc, seed); seed += 100000
    df.to_csv(RES / "e4_noise.csv", index=False)
    print(f"E4 done: {len(df)} reps")

    # ---------- E5: source geometry ----------
    sc = []
    for g, a in itertools.product(
            ["isotropic", "clustered", "banded", "optimized"],
            ["M3_stars_50", "M5_quasars_50"]):
        kw = dict(base, geometry_kind=("isotropic" if g == "optimized" else g),
                  optimize=(g == "optimized"))
        sc.append(dict(name=scenario_name("E5", g, a), spec=A[a],
                       t_years=1e5, **kw))
    df = simulation.run_grid(sc, n_mc, seed); seed += 100000
    df.to_csv(RES / "e5_geometry.csv", index=False)
    print(f"E5 done: {len(df)} reps")

    # ---------- E6: information cost ----------
    sc = []
    for enc, bits in itertools.product(
            ["b_only", "knn", "b_chir", "knn_chir"], [8, 16, 32, 64]):
        for a in ["M3_stars_20", "M5_quasars_50", "M7_hybrid_all"]:
            kw = dict(base,
                      chirality=("chir" in enc),
                      encoding_edges=("knn" if "knn" in enc else "none"),
                      bits=bits)
            sc.append(dict(name=scenario_name("E6", enc, bits, a),
                           spec=A[a], t_years=1e7, **kw))
    df = simulation.run_grid(sc, n_mc, seed); seed += 100000
    df.to_csv(RES / "e6_infocost.csv", index=False)
    print(f"E6 done: {len(df)} reps")

    # ---------- E6b: stored edges under each mismatch model ----------
    # Edges detect wrong-source substitutions/injections but cannot detect
    # b-correspondence permutations; run all three models to separate that.
    # chirality=True in BOTH conditions (inherited from base): this isolates
    # the edges effect; labels are b_chir/knn_chir to match the encodings.
    sc = []
    for enc, mm in itertools.product(
            ["b_chir", "knn_chir"],
            ["permutation", "substitution", "injection"]):
        for a in ["M3_stars_20", "M5_quasars_50", "M7_hybrid_all"]:
            kw = dict(base, chirality=True,
                      encoding_edges=("knn" if "knn" in enc else "none"),
                      mismatch_model=mm, p_mismatch=0.5, bits=32)
            sc.append(dict(name=scenario_name("E6b", enc, mm, a),
                           spec=A[a], t_years=1e7, **kw))
    df = simulation.run_grid(sc, n_mc, seed); seed += 100000
    df.to_csv(RES / "e6b_edgebenefit.csv", index=False)
    print(f"E6b done: {len(df)} reps")

    # ---------- E6c: storage-precision floor at a precision-limited horizon --
    # At t=1e7 drift dominates and the bits axis is flat; at t=1e4 the noise
    # floor is low enough that coarse quantization measurably degrades decode.
    sc = []
    for enc, bits, a in itertools.product(
            ["b_chir", "knn_chir"], [8, 32],
            ["M5_quasars_50", "M7_hybrid_all"]):
        kw = dict(base, chirality=True,
                  encoding_edges=("knn" if "knn" in enc else "none"),
                  bits=bits)
        sc.append(dict(name=scenario_name("E6c", enc, bits, a),
                       spec=A[a], t_years=1e4, **kw))
    df = simulation.run_grid(sc, n_mc, seed); seed += 100000
    df.to_csv(RES / "e6c_precision.csv", index=False)
    print(f"E6c done: {len(df)} reps")

    # ---------- E7: heterogeneous composition optimization ----------
    sc = []
    alloc = []
    for n_tot in [20, 30, 50]:
        step = 10
        grid = range(0, n_tot + 1, step)
        for s_, p_, q_ in itertools.product(grid, grid, grid):
            g_ = n_tot - s_ - p_ - q_
            if g_ < 0:
                continue
            alloc.append((n_tot, {"star": s_, "pulsar": p_,
                                  "quasar": q_, "galaxy": g_}))
    for (n_tot, spec), t in itertools.product(alloc, [1e6, 1e7, 1e8]):
        sc.append(dict(name=scenario_name("E7", n_tot, t,
                                          spec["star"], spec["pulsar"],
                                          spec["quasar"], spec["galaxy"]),
                       spec=spec, t_years=t, **base))
    df = simulation.run_grid(sc, 300 if not args.quick else 200, seed)
    seed += 100000
    df.to_csv(RES / "e7_composition.csv", index=False)
    print(f"E7 done: {len(df)} reps")

    # ---------- E8: negative controls ----------
    sc = []
    kw = dict(base)
    # NC1 implemented via mismatch_model injection of fully random b: emulate
    # by 100% substitution + wrong cosines; dedicated flag below.
    sc.append(dict(name="E8|NC1_random_b", spec=A["M7_hybrid_all"],
                   t_years=1e6, **dict(base, nc_random_b=True)))
    sc.append(dict(name="E8|NC2_full_mismatch", spec=A["M7_hybrid_all"],
                   t_years=1e6, **dict(base, p_mismatch=1.0)))
    df = simulation.run_grid(sc, n_mc, seed); seed += 100000
    df.to_csv(RES / "e8_negative_controls.csv", index=False)
    print(f"E8 done: {len(df)} reps")

    # ---------- E9: chirality on/off ----------
    sc = []
    for ch in [False, True]:
        kw = dict(base, chirality=ch)
        sc.append(dict(name=scenario_name("E9", "chir", ch),
                       spec=A["M7_hybrid_all"], t_years=1e7, **kw))
    df = simulation.run_grid(sc, n_mc, seed); seed += 100000
    df.to_csv(RES / "e9_chirality.csv", index=False)
    print(f"E9 done: {len(df)} reps")

    # ---------- E10: diminishing returns ----------
    sc = []
    for cls, n_ in itertools.product(["star", "quasar"],
                                     [1, 3, 10, 20, 50, 100]):
        kw = dict(base, p_mismatch=0.05)
        sc.append(dict(name=scenario_name("E10", cls, n_),
                       spec={cls: n_}, t_years=1e4, **kw))
    df = simulation.run_grid(sc, n_mc, seed); seed += 100000
    df.to_csv(RES / "e10_scaling.csv", index=False)
    print(f"E10 done: {len(df)} reps")

    # ---------- E11: M1b direct-axis landmark ----------
    # Polaris-like "this object points north" scheme: the landmark direction
    # defines the axis at encode time; decode uses the observed direction.
    # Baseline corruption model (permutation, irrelevant to a direction-only
    # scheme) plus a substitution cell where misidentification does corrupt it.
    sc = []
    for t in T:
        sc.append(dict(name=scenario_name("E11", "M1b", t), spec={"star": 1},
                       t_years=t, direct_axis=True, **base))
    kw = dict(base, mismatch_model="substitution", p_mismatch=0.5)
    for t in [1e4, 1e5, 1e6]:
        sc.append(dict(name=scenario_name("E11", "M1b_subst0.5", t),
                       spec={"star": 1}, t_years=t, direct_axis=True, **kw))
    df = simulation.run_grid(sc, n_mc, seed); seed += 100000
    df.to_csv(RES / "e11_m1b.csv", index=False)
    print(f"E11 done: {len(df)} reps")


if __name__ == "__main__":
    main()
