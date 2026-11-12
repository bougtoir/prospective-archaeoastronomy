#!/usr/bin/env python3
"""Aggregate per-replication results -> results/summary_*.csv."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from proarch.stats import summarize_frame  # noqa

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"


def load(name):
    return pd.read_csv(RES / name)


def parse_scenario(df):
    parts = df["scenario"].str.split("|", expand=True)
    df["exp"] = parts[0]
    for i in range(1, parts.shape[1]):
        df[f"k{i}"] = parts[i]
    return df


def main():
    df = parse_scenario(load("e1_architecture_time.csv"))
    df["arch"] = df["k1"]; df["t"] = df["k2"].astype(float)
    summarize_frame(df, ["arch", "t"]).to_csv(RES / "summary_e1.csv", index=False)

    df = parse_scenario(load("e1c_core.csv"))
    df["arch"] = df["k1"]; df["t"] = df["k2"].astype(float)
    summarize_frame(df, ["arch", "t"]).to_csv(RES / "summary_e1c.csv", index=False)

    df = parse_scenario(load("e2_estimators.csv"))
    df["arch"] = df["k1"]; df["estimator"] = df["k2"]
    df["p_mismatch"] = df["k3"].astype(float)
    summarize_frame(df, ["arch", "estimator", "p_mismatch"]).to_csv(
        RES / "summary_e2.csv", index=False)

    df = parse_scenario(load("e3_heatmap.csv"))
    df["severity"] = df["k1"]; df["p_mismatch"] = df["k2"].astype(float)
    summarize_frame(df, ["severity", "p_mismatch"]).to_csv(
        RES / "summary_e3.csv", index=False)

    df = parse_scenario(load("e4_noise.csv"))
    df["sigma_obs"] = df["k1"].astype(float)
    summarize_frame(df, ["sigma_obs"]).to_csv(RES / "summary_e4.csv", index=False)

    df = parse_scenario(load("e5_geometry.csv"))
    df["geometry"] = df["k1"]; df["arch"] = df["k2"]
    summarize_frame(df, ["geometry", "arch"]).to_csv(
        RES / "summary_e5.csv", index=False)

    df = parse_scenario(load("e6_infocost.csv"))
    df["encoding"] = df["k1"]; df["prec_bits"] = df["k2"].astype(int)
    df["arch"] = df["k3"]
    s = summarize_frame(df, ["encoding", "prec_bits", "arch"])
    s = s.merge(df.groupby(["encoding", "prec_bits", "arch"])["bits"].mean()
                .rename("mean_bits").reset_index(),
                on=["encoding", "prec_bits", "arch"])
    s.to_csv(RES / "summary_e6.csv", index=False)

    df = parse_scenario(load("e6b_edgebenefit.csv"))
    df["encoding"] = df["k1"]; df["mismatch_model"] = df["k2"]
    df["arch"] = df["k3"]
    summarize_frame(df, ["encoding", "mismatch_model", "arch"]).to_csv(
        RES / "summary_e6b.csv", index=False)

    df = parse_scenario(load("e6c_precision.csv"))
    df["encoding"] = df["k1"]; df["prec_bits"] = df["k2"].astype(int)
    df["arch"] = df["k3"]
    summarize_frame(df, ["encoding", "prec_bits", "arch"]).to_csv(
        RES / "summary_e6c.csv", index=False)

    df = parse_scenario(load("e7_composition.csv"))
    df["n_tot"] = df["k1"].astype(int); df["t"] = df["k2"].astype(float)
    for i, c in enumerate(["n_star", "n_pulsar", "n_quasar", "n_galaxy"], start=3):
        df[c] = df[f"k{i}"].astype(int)
    summarize_frame(df, ["n_tot", "t", "n_star", "n_pulsar",
                         "n_quasar", "n_galaxy"]).to_csv(
        RES / "summary_e7.csv", index=False)

    df = parse_scenario(load("e8_negative_controls.csv"))
    summarize_frame(df, ["scenario"]).to_csv(RES / "summary_e8.csv", index=False)

    df = parse_scenario(load("e9_chirality.csv"))
    df["chirality"] = df["k2"] == "True"
    s = summarize_frame(df, ["chirality"])
    s["p_mirror_wrong"] = df.groupby("chirality")["mirror_wrong"].mean().values
    s["p_chirality_used"] = (df.groupby("chirality")["chirality_used"]
                             .mean().values)
    s.to_csv(RES / "summary_e9.csv", index=False)

    df = parse_scenario(load("e10_scaling.csv"))
    df["cls"] = df["k1"]; df["n"] = df["k2"].astype(int)
    summarize_frame(df, ["cls", "n"]).to_csv(RES / "summary_e10.csv", index=False)

    df = parse_scenario(load("e11_m1b.csv"))
    df["variant"] = df["k1"]; df["t"] = df["k2"].astype(float)
    summarize_frame(df, ["variant", "t"]).to_csv(
        RES / "summary_e11.csv", index=False)

    print("summaries written")


if __name__ == "__main__":
    main()
