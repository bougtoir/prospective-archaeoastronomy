#!/usr/bin/env python3
"""Generate Figures 1-7 from results summaries."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RES, FIG = ROOT / "results", ROOT / "figures"
FIG.mkdir(exist_ok=True)
plt.rcParams.update({"figure.dpi": 150, "font.size": 9,
                     "axes.grid": True, "grid.alpha": 0.3})


def S(name):
    return pd.read_csv(RES / name)


def fig1():
    fig, ax = plt.subplots(figsize=(7.2, 2.4))
    ax.axis("off")
    steps = ["Present terrestrial\norientation $N_0$",
             "Relational encoding\n$b=Q N_0$, Gram, chirality",
             "Deep-time degradation\nloss, drift, mismatch",
             "Future observations\n$Q_{obs}$",
             "Robust reconstruction\nLS / Huber / RANSAC",
             "Recovered orientation\n$\\hat{N}$, $\\epsilon_\\theta$"]
    xs = np.linspace(0.05, 0.95, len(steps))
    for i, (x, s) in enumerate(zip(xs, steps)):
        ax.text(x, 0.5, s, ha="center", va="center", fontsize=7.5,
                bbox=dict(boxstyle="round,pad=0.35", fc="#dce9f5",
                          ec="#33587a"))
        if i < len(steps) - 1:
            ax.annotate("", xy=(xs[i + 1] - 0.09, 0.5), xytext=(x + 0.09, 0.5),
                        arrowprops=dict(arrowstyle="->", color="#33587a"))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    fig.savefig(FIG / "fig1_architecture.png", bbox_inches="tight")
    plt.close(fig)


def fig2():
    """Single landmark / triangle / redundant network comparison."""
    s = S("summary_e10.csv")
    fig, ax = plt.subplots(figsize=(4.2, 3.0))
    for cls, mk in [("star", "o"), ("quasar", "s")]:
        d = s[s.cls == cls].sort_values("n")
        lo = np.clip(d["p_err<1.0deg"] - d["p_err<1.0deg_lo"], 0, None)
        hi = np.clip(d["p_err<1.0deg_hi"] - d["p_err<1.0deg"], 0, None)
        ax.errorbar(d["n"], d["p_err<1.0deg"], yerr=[lo, hi],
                    marker=mk, capsize=3, label=cls)
    ax.set_xscale("log"); ax.set_ylim(-0.02, 1.05)
    ax.set_xlabel("number of reference sources")
    ax.set_ylabel("$P(\\epsilon_\\theta < 1°)$")
    ax.set_title("Redundancy vs single landmark (t = $10^4$ yr)")
    ax.legend()
    fig.savefig(FIG / "fig3_redundancy.png", bbox_inches="tight")
    plt.close(fig)


def fig3():
    s = S("summary_e10.csv")
    fig, ax = plt.subplots(figsize=(4.2, 3.0))
    for cls, mk in [("star", "o"), ("quasar", "s")]:
        d = s[(s.cls == cls) & (s.n_valid > 0)].sort_values("n")
        ax.plot(d["n"], d["median_err_deg"], marker=mk, label=cls)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("number of reference sources")
    ax.set_ylabel("median angular error (deg)")
    ax.set_title("Reconstruction error vs source count")
    ax.legend()
    fig.savefig(FIG / "fig4_error_vs_n.png", bbox_inches="tight")
    plt.close(fig)


def fig4():
    s = S("summary_e1.csv")
    keep = ["M1_single_star", "M2_star_triangle", "M3_stars_50",
            "M4_pulsars_20", "M5_quasars_50", "M6_galaxies_20",
            "M7_hybrid_all"]
    fig, ax = plt.subplots(figsize=(5.4, 3.4))
    for a in keep:
        d = s[s.arch == a].sort_values("t")
        ax.plot(np.log10(d["t"]), d["p_err<1.0deg"], marker="o", ms=3,
                label=a)
    ax.set_xlabel("$\\log_{10}(t\\,/\\,\\mathrm{yr})$")
    ax.set_ylabel("$P(\\epsilon_\\theta < 1°)$")
    ax.set_ylim(-0.02, 1.05)
    ax.legend(fontsize=6.5, loc="lower left")
    ax.set_title("Architecture robustness vs time horizon")
    fig.savefig(FIG / "fig2_p_vs_time.png", bbox_inches="tight")
    plt.close(fig)


def fig5():
    s = S("summary_e3.csv")
    piv = s.pivot(index="severity", columns="p_mismatch",
                  values="p_err<1.0deg")
    piv = piv.reindex(["optimistic", "baseline", "pessimistic"])
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    im = ax.imshow(piv.values, vmin=0, vmax=1, cmap="viridis",
                   aspect="auto")
    ax.set_xticks(range(len(piv.columns)), piv.columns)
    ax.set_yticks(range(len(piv.index)), piv.index)
    ax.set_xlabel("misidentification probability $p_{mismatch}$")
    ax.set_ylabel("degradation severity")
    for i in range(piv.shape[0]):
        for j in range(piv.shape[1]):
            ax.text(j, i, f"{piv.values[i, j]:.2f}", ha="center",
                    va="center", fontsize=7, color="w")
    ax.set_title("Hybrid network at $t=10^7$ yr")
    fig.colorbar(im, label="$P(\\epsilon_\\theta<1°)$")
    fig.savefig(FIG / "fig7_heatmap.png", bbox_inches="tight")
    plt.close(fig)


def fig6():
    s = S("summary_e6.csv")
    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    for enc, g in s.groupby("encoding"):
        d = g.sort_values("mean_bits")
        ax.plot(d["mean_bits"], d["p_err<1.0deg"], marker="o", ms=4,
                label=enc)
    ax.set_xscale("log")
    ax.set_xlabel("total information cost (bits)")
    ax.set_ylabel("$P(\\epsilon_\\theta<1°)$")
    ax.set_title("Information cost vs reliability ($t=10^7$ yr)")
    ax.legend(fontsize=7)
    fig.savefig(FIG / "fig6_pareto.png", bbox_inches="tight")
    plt.close(fig)


def fig7():
    """Geometric conditioning vs performance (E5)."""
    s = S("summary_e5.csv")
    order = ["isotropic", "clustered", "banded", "optimized"]
    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    for a, g in s.groupby("arch"):
        d = g.set_index("geometry").reindex(order)
        ax.plot(range(4), d["p_err<1.0deg"], marker="o", label=a)
    ax.set_xticks(range(4), order)
    ax.set_ylabel("$P(\\epsilon_\\theta<1°)$")
    ax.set_ylim(-0.02, 1.05)
    ax.set_xlabel("source geometry")
    ax.set_title("Geometry conditioning vs reconstruction ($t=10^5$ yr)")
    ax.legend(fontsize=7)
    fig.savefig(FIG / "fig5_geometry.png", bbox_inches="tight")
    plt.close(fig)


def graphical_abstract():
    """Schematic graphical abstract for the submission package."""
    fig, ax = plt.subplots(figsize=(5.4, 3.2))
    ax.axis("off")
    rng = np.random.default_rng(2)
    src = np.random.default_rng(2).normal(0, 1, (14, 2))
    src = src / np.linalg.norm(src, axis=1, keepdims=True) * 0.36
    north = np.array([0.0, 0.42])
    for s in src:
        ax.plot([0, s[0]], [0, s[1]], color="#9db8d2", lw=0.8, zorder=1)
    ax.scatter(src[:, 0], src[:, 1], c="#e8a33d", s=22, zorder=2)
    ax.annotate("", xy=north, xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color="#c0392b", lw=2.4))
    ax.text(0.05, 0.43, "$N_0$", color="#c0392b", fontsize=12)
    ax.scatter([0], [0], c="#2c5f8a", s=50, zorder=3)
    ax.text(0, -0.55, "relational encoding $b = Q N_0$ + chirality\n"
            "survives loss, drift, mismatch -> robust reconstruction",
            ha="center", fontsize=8)
    ax.set_xlim(-0.6, 0.6); ax.set_ylim(-0.7, 0.6)
    out = ROOT / "manuscript" / "graphical_abstract.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)


def main():
    fig1(); fig2(); fig3(); fig4(); fig5(); fig6(); fig7()
    graphical_abstract()
    print("figures written to", FIG)


if __name__ == "__main__":
    main()
