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
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    ax.axis("off")
    steps = ["Present terrestrial\norientation $N_0$",
             "Relational encoding\n$b=Q N_0$, Gram, chirality",
             "Deep-time degradation\nloss, drift, mismatch",
             "Future observations\n$Q_{obs}$",
             "Robust reconstruction\nLS / Huber / RANSAC",
             "Recovered orientation\n$\\hat{N}$, $\\epsilon_\\theta$"]
    xs = np.linspace(0.08, 0.92, 3)
    # snake layout: top row L->R (steps 0-2), bottom row R->L (steps 3-5)
    pos = {0: (xs[0], 0.75), 1: (xs[1], 0.75), 2: (xs[2], 0.75),
           3: (xs[2], 0.25), 4: (xs[1], 0.25), 5: (xs[0], 0.25)}
    for i, s in enumerate(steps):
        ax.text(*pos[i], s, ha="center", va="center", fontsize=7.5,
                bbox=dict(boxstyle="round,pad=0.35", fc="#dce9f5",
                          ec="#33587a"))
    for a, b in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]:
        xa, ya = pos[a]
        xb, yb = pos[b]
        dx = 0.16 * np.sign(xb - xa)
        dy = 0.22 * np.sign(yb - ya)
        ax.annotate("", xy=(xb - dx, yb - dy * 0.6),
                    xytext=(xa + dx, ya + dy),
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


# --------------------------------------------------------------------------
# Layer-2 calibration figures (SMPT revision)
# --------------------------------------------------------------------------

def fig_skymap():
    """Observed catalogue sky geometry: Gaia stars, ATNF pulsars, ICRF3."""
    proc = ROOT / "data" / "processed"
    gaia = pd.read_csv(proc / "gaia_dr3_bright.csv")
    atnf = pd.read_csv(proc / "atnf_pulsars.csv")
    icrf = pd.read_csv(proc / "icrf3_quasars.csv")
    fig, ax = plt.subplots(figsize=(6.4, 3.4),
                           subplot_kw={"projection": "aitoff"})
    ax.grid(alpha=0.3)
    ra = np.deg2rad(gaia.ra_deg); ra = np.where(ra > np.pi, ra - 2 * np.pi, ra)
    ax.scatter(ra, np.deg2rad(gaia.dec_deg), s=4, alpha=0.5, label="Gaia DR3")
    ra = np.deg2rad(atnf.ra_deg); ra = np.where(ra > np.pi, ra - 2 * np.pi, ra)
    ax.scatter(ra, np.deg2rad(atnf.dec_deg), s=2, alpha=0.3, label="ATNF")
    ra = np.deg2rad(icrf.ra_deg); ra = np.where(ra > np.pi, ra - 2 * np.pi, ra)
    ax.scatter(ra, np.deg2rad(icrf.dec_deg), s=6, alpha=0.5, label="ICRF3-K")
    ax.legend(loc="upper right", fontsize=7, bbox_to_anchor=(1.02, 1.02))
    ax.set_title("Observed source-population sky geometry")
    fig.savefig(FIG / "fig8_observed_sky.png", bbox_inches="tight")
    plt.close(fig)


def fig_motion():
    """Empirical motion distributions by source class."""
    proc = ROOT / "data" / "processed"
    gaia = pd.read_csv(proc / "gaia_dr3_bright.csv")
    atnf = pd.read_csv(proc / "atnf_pulsars.csv")
    star_pm = np.hypot(gaia.pmra_masyr, gaia.pmdec_masyr)
    psr_pm = atnf.pm_tot_masyr.dropna()
    fig, axes = plt.subplots(1, 3, figsize=(8.6, 2.8))
    axes[0].hist(np.log10(star_pm.clip(lower=1e-3)), bins=25, color="#2c5f8a")
    axes[0].set_title("Gaia stars |PM| (mas/yr)")
    axes[0].set_xlabel("log10 mas/yr")
    axes[1].hist(np.log10(psr_pm.clip(lower=1e-3)), bins=25, color="#7a5230")
    axes[1].set_title("ATNF pulsars PMTOT (mas/yr)")
    axes[1].set_xlabel("log10 mas/yr")
    q = 10 ** np.linspace(-3, -1, 200)
    axes[2].fill_between(np.log10(q), 0, 1, alpha=0.4, color="#3c7a4f")
    axes[2].axvline(np.log10(1e-2), color="#3c7a4f", ls="--")
    axes[2].set_title("Quasar apparent-drift prior")
    axes[2].set_xlabel("log10 mas/yr")
    axes[2].set_ylim(0, 1.05)
    fig.tight_layout()
    fig.savefig(FIG / "fig9_motion_distributions.png", bbox_inches="tight")
    plt.close(fig)


def _cal():
    return pd.read_csv(ROOT / "results" / "calibration" /
                       "calibrated_summary.csv")


def fig_theory_vs_cal():
    """Synthetic vs observation-calibrated performance, n=50 networks."""
    cs = _cal()
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    for cal, syn, mk, col in [
            ("C_star50", "S_star50", "o", "#2c5f8a"),
            ("C_pulsar50", "S_pulsar50", "^", "#7a5230"),
            ("C_quasar50", "S_quasar50", "s", "#3c7a4f")]:
        d = cs[cs.scenario == cal].sort_values("t_years")
        ax.plot(np.log10(d.t_years), d.p_err_lt1, marker=mk, color=col,
                label=cal.replace("C_", "observation-calibrated "))
        d = cs[cs.scenario == syn].sort_values("t_years")
        ax.plot(np.log10(d.t_years), d.p_err_lt1, marker=mk, ls="--",
                color=col, alpha=0.45,
                label=syn.replace("S_", "synthetic "))
    ax.axvspan(7, 8.5, color="0.85", alpha=0.4)
    ax.text(7.05, 0.05, "extrapolative\nstress test", fontsize=6.5)
    ax.set_xlabel("log10(t/yr)")
    ax.set_ylabel("P(eps < 1 deg)")
    ax.set_ylim(-0.02, 1.05)
    ax.legend(fontsize=6)
    fig.savefig(FIG / "fig13_theory_vs_calibrated.png", bbox_inches="tight")
    plt.close(fig)


def fig_opt_vs_random():
    """Random vs D-optimally selected observed-source networks."""
    cs = _cal()
    prim = cs[cs.regime.isin(["observation_anchored", "extended_projection"])]
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    xpos, xtick = [], []
    i = 0
    for cls in ("star", "pulsar", "quasar"):
        for n in sorted({10, 50, 100}):
            rnd = prim[(prim.scenario == f"C_{cls}{n}")
                       & (prim.t_years == 1e5)]
            opt = prim[(prim.scenario == f"C_{cls}{n}_opt")
                       & (prim.t_years == 1e5)]
            if not len(rnd):
                continue
            rv = float(rnd.p_err_lt1.iloc[0]) if len(rnd) else np.nan
            ov = float(opt.p_err_lt1.iloc[0]) if len(opt) else np.nan
            ax.bar(i - 0.2, rv, 0.36, color="#9db8d2")
            ax.bar(i + 0.2, ov, 0.36, color="#2c5f8a")
            xpos.append(i); xtick.append(f"{cls}\nn={n}")
            i += 1
    ax.set_xticks(xpos, xtick, fontsize=6.5)
    ax.set_ylabel("P(eps < 1 deg) at t = 1e5 yr")
    ax.set_ylim(-0.02, 1.05)
    ax.legend(["random", "D-optimal"], fontsize=7)
    fig.savefig(FIG / "fig12_random_vs_optimized.png", bbox_inches="tight")
    plt.close(fig)


def fig_calibrated_horizon():
    """Primary calibrated performance over 1e3-1e6 yr."""
    cs = _cal()
    prim = cs[cs.regime.isin(["observation_anchored", "extended_projection"])]
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    for sc, mk in [("C_star50", "o"), ("C_pulsar50", "^"),
                   ("C_quasar50", "s"), ("C_hybrid_spq", "d")]:
        d = prim[(prim.scenario == sc)].sort_values("t_years")
        ax.plot(np.log10(d.t_years), d.p_err_lt1, marker=mk, label=sc)
    ax.set_xlabel("log10(t/yr)")
    ax.set_ylabel("P(eps < 1 deg)")
    ax.set_ylim(-0.02, 1.05)
    ax.axvline(np.log10(1e6), color="k", ls="--", lw=0.7)
    ax.set_title("Observation-anchored (1e3-1e5 yr) + extended 1e6 yr projection")
    ax.legend(fontsize=7)
    fig.savefig(FIG / "fig11_calibrated_primary.png", bbox_inches="tight")
    plt.close(fig)


def fig_stress():
    """Extrapolative 1e7-1e8 yr stress tests (flagged, not calibrated)."""
    cs = _cal()
    st = cs[cs.regime == "extrapolative_stress"]
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    for sc, mk in [("C_star50", "o"), ("C_pulsar50", "^"),
                   ("C_quasar50", "s"), ("C_hybrid_spq", "d")]:
        d = st[st.scenario == sc].sort_values("t_years")
        ax.plot(np.log10(d.t_years), d.p_err_lt1, marker=mk, label=sc)
    ax.set_xlabel("log10(t/yr)")
    ax.set_ylabel("P(eps < 1 deg)")
    ax.set_ylim(-0.02, 1.05)
    ax.set_title("Extrapolative stress tests (not calibrated forecasts)",
                 fontsize=9)
    ax.legend(fontsize=7)
    fig.savefig(FIG / "fig14_stress_tests.png", bbox_inches="tight")
    plt.close(fig)


def fig_propagation():
    """Angular-linear vs 3D Cartesian propagation on Gaia RV subset."""
    pc = pd.read_csv(ROOT / "results" / "calibration" /
                     "propagation_comparison.csv")
    fig, ax = plt.subplots(figsize=(4.8, 3.0))
    ax.plot(np.log10(pc.t_years), pc.median_deg_angular_linear, "o-",
            label="angular-linear")
    ax.plot(np.log10(pc.t_years), pc.median_deg_3d, "s--",
            label="3D Cartesian")
    ax.fill_between(np.log10(pc.t_years), pc.median_deg_angular_linear,
                    pc.median_deg_3d, alpha=0.15)
    ax.set_xlabel("log10(t/yr)")
    ax.set_ylabel("median displacement (deg)")
    ax.set_yscale("log")
    ax.legend(fontsize=7)
    fig.savefig(FIG / "fig10_propagation_comparison.png",
                bbox_inches="tight")
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
    if (ROOT / "results" / "calibration" /
            "calibrated_summary.csv").exists():
        fig_skymap(); fig_motion(); fig_theory_vs_cal()
        fig_opt_vs_random(); fig_calibrated_horizon(); fig_stress()
        fig_propagation()
    print("figures written to", FIG)


if __name__ == "__main__":
    main()
