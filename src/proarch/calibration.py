"""Observation-calibrated source layer (SMPT revision, Layer 2).

Builds reference-network populations from the persisted processed catalogues
(Gaia DR3, ATNF, ICRF3-K), assigns per-source motion rates from measured or
literature-constrained distributions, and decomposes source usability into
explicit, classifiable factors:

    usable(t) = exists(t) x identifiable(t) x observable(t)

stability is handled inside propagation via per-source drift rates, not as a
separate probability. Every calibrated quantity carries a classification:
    observed / derived / literature-constrained / extrapolated / sensitivity-only

Nothing here is loaded inside `make all`'s live network path: inputs are the
persisted files under data/processed/ written by scripts/fetch_catalogs.py.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PROC = ROOT / "data" / "processed"
CAL = ROOT / "results" / "calibration"

MAS_YR_TO_RAD_YR = np.pi / 180.0 / 3600.0 / 1000.0

# ---------------------------------------------------------------------------
# Literature-constrained constants (provenance recorded in the registry)
# ---------------------------------------------------------------------------

# Quasar apparent angular-motion prior. ICRF3 positions are catalogued at the
# ~10-1000 uas level and Gaia EDR3/DR3 quasar proper motions are consistent
# with zero at the uas/yr level (secular aberration is a global dipole term,
# not per-source random motion). The dominant secular angular noise on the
# frame is centroid wander from AGN structure evolution; we place a
# log-uniform prior on the per-source apparent drift rate. Sensitivity varies
# the scale by x10 down/up. Classification: literature-constrained.
QUASAR_DRIFT_LOG10_MASYR = (-3.0, -1.0)   # log10 bounds of prior, mas/yr

# Star remaining-existence factor. Bright-star main-sequence lifetimes are
# Gyr-scale; a first-order existence model is exp(-t/tau_star) with a
# literature-constrained tau bracketed by the massive-star tail (O/B) and the
# solar-type bulk. Classification: literature-constrained.
STAR_EXIST_TAU_YR = 5e9
STAR_EXIST_TAU_RANGE_YR = (5e8, 2e10)

# Pulsar usable-lifetime factor. Characteristic age is NOT treated as the
# remaining lifetime (per task rule); it is used only to place the scale of
# the population's turnover time. The usable factor is exp(-t/tau_psr) with
# tau_psr = k * median(AGE). k=1 baseline; sensitivity k in {0.3, 3}.
# Classification: derived (empirical scale) + literature-constrained form.
PSR_EXIST_K = 1.0
PSR_EXIST_K_RANGE = (0.3, 3.0)


def load_catalogue(name):
    """Load a processed catalogue CSV. Raises if absent (no silent fallback)."""
    p = PROC / f"{name}.csv"
    if not p.exists():
        raise FileNotFoundError(
            f"{p} missing — run scripts/fetch_catalogs.py first")
    return pd.read_csv(p)


def radec_to_unit(ra_deg, dec_deg):
    ra = np.deg2rad(np.asarray(ra_deg, dtype=float))
    dec = np.deg2rad(np.asarray(dec_deg, dtype=float))
    return np.stack([np.cos(dec) * np.cos(ra),
                     np.cos(dec) * np.sin(ra),
                     np.sin(dec)], axis=1)


# ---------------------------------------------------------------------------
# Per-class empirical motion rates
# ---------------------------------------------------------------------------

def star_motion(df):
    """Measured total proper motion in mas/yr for the Gaia bright sample."""
    pm = np.hypot(df["pmra_masyr"], df["pmdec_masyr"])
    return pm.to_numpy()


def pulsar_motion(df):
    """Split the ATNF table into PM-measured and PM-missing frames.

    Missing proper motions are never fabricated. The PM-missing frame is used
    only by the sensitivity branch, which draws from the measured PMTOT
    distribution and records that it did so.
    """
    measured = df[df["pm_tot_masyr"].notna()].copy()
    missing = df[df["pm_tot_masyr"].isna()].copy()
    return measured, missing


def quasar_motion(df, rng):
    """Per-source literature-constrained apparent drift rate (rad/yr)."""
    lo, hi = QUASAR_DRIFT_LOG10_MASYR
    r_mas = 10 ** rng.uniform(lo, hi, size=len(df))
    return r_mas * MAS_YR_TO_RAD_YR


# ---------------------------------------------------------------------------
# Usability decomposition
# ---------------------------------------------------------------------------

def star_exists(t_years, tau=STAR_EXIST_TAU_YR):
    return float(np.exp(-float(t_years) / tau))


def pulsar_exists(t_years, atnf_df, k=PSR_EXIST_K):
    ages = atnf_df["age_yr"].dropna()
    ages = ages[ages > 0]
    if not len(ages):
        raise ValueError("ATNF catalogue has no usable AGE column")
    tau = k * float(ages.median())
    return float(np.exp(-float(t_years) / tau))


def usability_vector(labels, t_years, atnf_df=None):
    """Per-source usable probabilities under the calibrated decomposition.

    exists: class-specific (star: literature tau; pulsar: AGE-derived tau;
            quasar: persistence ~1 assumed — a conditional assumption, not
            observed over modelled horizons (sensitivity-only).
    identifiable: probability the source remains uniquely identifiable in its
            region — dominated by drift, handled in propagation; set to 1.
    observable: instrument-side availability — not estimable from catalogues;
            declared as a scenario factor =1 with sensitivity-only status.
    """
    out = np.empty(len(labels))
    for i, c in enumerate(labels):
        if c == "star":
            e = star_exists(t_years)
        elif c == "pulsar":
            if atnf_df is None:
                raise ValueError("pulsar usability needs the ATNF frame")
            e = pulsar_exists(t_years, atnf_df)
        elif c in ("quasar", "galaxy", "galaxy_cluster"):
            e = 1.0
        else:
            raise ValueError(c)
        out[i] = e * 1.0 * 1.0
    return np.clip(out, 0.0, 1.0)


# ---------------------------------------------------------------------------
# Population construction
# ---------------------------------------------------------------------------

def build_calibrated_population(pool, n, rng, optimize=False, cls=None):
    """Draw n sources from a processed-catalogue pool.

    pool: DataFrame with ra_deg/dec_deg plus the class-specific rate column.
    Returns dict(Q, labels, drift_rad_per_yr, source_ids, frame).
    """
    from . import geometry
    if n > len(pool):
        raise ValueError(f"requested {n} from pool of {len(pool)}")
    if optimize and len(pool) >= 4 * n:
        big = pool.sample(4 * n, random_state=rng.integers(2**31))
        dirs = radec_to_unit(big["ra_deg"], big["dec_deg"])
        sel = geometry.d_optimal_select(dirs, n)
        sub = big.iloc[sel]
        Q = dirs[sel]
    else:
        sub = pool.sample(n, random_state=rng.integers(2**31))
        Q = radec_to_unit(sub["ra_deg"], sub["dec_deg"])
    labels = np.array([cls] * len(sub))
    if cls == "star":
        drift = np.hypot(sub["pmra_masyr"], sub["pmdec_masyr"]).to_numpy()
        drift = drift * MAS_YR_TO_RAD_YR
    elif cls == "pulsar":
        drift = sub["pm_tot_masyr"].to_numpy() * MAS_YR_TO_RAD_YR
        if np.isnan(drift).any():
            raise ValueError("primary pulsar pool must be PM-measured only")
    elif cls == "quasar":
        drift = quasar_motion(sub, rng)
    else:
        raise ValueError(cls)
    return {"Q": Q, "labels": labels, "drift_rad_per_yr": drift,
            "source_ids": sub["source_id"].astype(str).tolist(),
            "frame": sub}


def build_calibrated_hybrid(pools, counts, rng):
    """Concatenate calibrated sub-populations. pools: {cls: DataFrame}."""
    parts = []
    for cls, n in counts.items():
        if n <= 0:
            continue
        parts.append(build_calibrated_population(pools[cls], n, rng,
                                                 cls=cls))
    Q = np.vstack([p["Q"] for p in parts])
    labels = np.concatenate([p["labels"] for p in parts])
    drift = np.concatenate([p["drift_rad_per_yr"] for p in parts])
    ids = sum((p["source_ids"] for p in parts), [])
    return {"Q": Q, "labels": labels, "drift_rad_per_yr": drift,
            "source_ids": ids}


# ---------------------------------------------------------------------------
# Registry / report writers
# ---------------------------------------------------------------------------

def write_registry():
    """Emit calibration_registry.csv: every calibrated parameter."""
    CAL.mkdir(parents=True, exist_ok=True)
    rows = [
        dict(parameter="star drift rate (per source)",
             source_class="star", value_or_distribution="measured |PM| (mas/yr)",
             source="Gaia DR3 gaiadr3.gaia_source, quality-cut bright sample",
             derivation_script="scripts/run_calibrated_simulations.py",
             uncertainty="pmra_error/pmdec_error columns",
             classification="observed",
             manuscript_usage="per-source propagation rate, primary"),
        dict(parameter="quasar apparent drift rate prior",
             source_class="quasar",
             value_or_distribution="log-uniform 1e-3..1e-1 mas/yr (x0.1/x10 sensitivity)",
             source="ICRF3-K formal uncertainties + Gaia EDR3 quasar-frame literature",
             derivation_script="src/proarch/calibration.py:quasar_motion",
             uncertainty="prior width x100",
             classification="literature-constrained",
             manuscript_usage="per-source propagation rate, primary"),
        dict(parameter="pulsar drift rate (measured subset)",
             source_class="pulsar", value_or_distribution="measured PMTOT (mas/yr)",
             source="ATNF Pulsar Catalogue v1.71 proc_form short",
             derivation_script="src/proarch/calibration.py:pulsar_motion",
             uncertainty="catalogue errors; missingness reported",
             classification="observed",
             manuscript_usage="per-source propagation rate, primary"),
        dict(parameter="pulsar drift rate (missing subset)",
             source_class="pulsar",
             value_or_distribution="resampled from measured PMTOT distribution",
             source="empirical CDF of measured PMTOT",
             derivation_script="scripts/run_calibrated_simulations.py --sensitivity",
             uncertainty="documented; complete-case vs resampled compared",
             classification="sensitivity-only",
             manuscript_usage="sensitivity analysis only"),
        dict(parameter="star existence factor tau",
             source_class="star", value_or_distribution=f"{STAR_EXIST_TAU_YR:.2e} yr "
             f"[{STAR_EXIST_TAU_RANGE_YR[0]:.1e}..{STAR_EXIST_TAU_RANGE_YR[1]:.1e}]",
             source="main-sequence lifetime scale (literature)",
             derivation_script="src/proarch/calibration.py:star_exists",
             uncertainty="bracketed sensitivity",
             classification="literature-constrained",
             manuscript_usage="exists(t) factor"),
        dict(parameter="pulsar existence scale tau",
             source_class="pulsar",
             value_or_distribution=f"k*median(AGE), k={PSR_EXIST_K} "
             f"[{PSR_EXIST_K_RANGE[0]}..{PSR_EXIST_K_RANGE[1]}]",
             source="ATNF characteristic-age distribution (empirical scale)",
             derivation_script="src/proarch/calibration.py:pulsar_exists",
             uncertainty="k sensitivity; age is not exact lifetime",
             classification="derived",
             manuscript_usage="exists(t) factor"),
        dict(parameter="quasar existence factor",
             source_class="quasar", value_or_distribution="1.0 at all horizons",
             source="extragalactic persistence over modelled horizons "
                    "(conditional assumption; not observed)",
             derivation_script="src/proarch/calibration.py:usability_vector",
             uncertainty="not bounded by catalogue data; conclusions "
                         "conditional on persistence and the "
                         "apparent-motion model",
             classification="sensitivity-only",
             manuscript_usage="exists(t) factor"),
        dict(parameter="identifiable factor",
             source_class="all", value_or_distribution="1.0 baseline",
             source="dominated by drift, handled in propagation",
             derivation_script="src/proarch/calibration.py:usability_vector",
             uncertainty="n/a", classification="sensitivity-only",
             manuscript_usage="declared; not fitted"),
        dict(parameter="observable factor",
             source_class="all", value_or_distribution="1.0 baseline",
             source="instrument-side availability; not catalogue-estimable",
             derivation_script="src/proarch/calibration.py:usability_vector",
             uncertainty="n/a", classification="sensitivity-only",
             manuscript_usage="declared; not fitted"),
        dict(parameter="galaxy / galaxy_cluster classes",
             source_class="galaxy,galaxy_cluster",
             value_or_distribution="removed from primary calibrated comparison",
             source="no credible calibration path identified",
             derivation_script="results/calibration/calibration_parameter_classification.csv",
             uncertainty="n/a", classification="sensitivity-only",
             manuscript_usage="demoted to sensitivity/exploratory"),
    ]
    df = pd.DataFrame(rows)
    df.to_csv(CAL / "calibration_registry.csv", index=False)
    return df


def write_classification():
    """Emit calibration_parameter_classification.csv: every model parameter
    classified observed / derived / literature-constrained / extrapolated /
    sensitivity-only, per the usability decomposition
    usable = exists x identifiable x observable (+stability in propagation)."""
    CAL.mkdir(parents=True, exist_ok=True)
    cols = ["parameter", "source_class", "component",
            "value_or_distribution", "classification", "basis",
            "sensitivity_handling"]
    rows = [
        # -- stability (propagation rates) --
        ("per-source drift rate", "star", "stability",
         "measured |PM|", "observed",
         "Gaia DR3 pmra/pmdec, quality-cut sample", "n/a"),
        ("per-source drift rate", "pulsar", "stability",
         "measured PMTOT subset", "observed",
         "ATNF measured PMs; PM-missing excluded from primary",
         "PM-missing resampled from empirical CDF (S1)"),
        ("per-source drift rate", "quasar", "stability",
         "log-uniform 1e-3..1e-1 mas/yr", "literature-constrained",
         "ICRF3 uncertainties + Gaia quasar-frame literature; AGN "
         "structure centroid wander", "scale x0.1/x10 (S4)"),
        # -- exists --
        ("exists(t)", "star", "exists", "exp(-t/5e9 yr)",
         "literature-constrained", "main-sequence lifetime scale",
         "tau 5e8..2e10 yr (S2)"),
        ("exists(t)", "pulsar", "exists",
         "exp(-t/(k*median AGE)), k=1", "derived",
         "ATNF characteristic-age distribution sets the scale; age is "
         "NOT used as exact remaining lifetime", "k=0.3/3 (S3)"),
        ("exists(t)", "quasar", "exists", "1.0", "sensitivity-only",
         "current existence is observed; continued persistence over "
         "modelled horizons is a conditional assumption, not observed; "
         "quasar results are conditional on source persistence and the "
         "specified apparent-motion model", "declared baseline"),
        # -- identifiable / observable --
        ("identifiable(t)", "all", "identifiable", "1.0",
         "sensitivity-only",
         "uniqueness loss is dominated by drift (in propagation), so no "
         "separate factor is fitted", "declared baseline"),
        ("observable(t)", "all", "observable", "1.0",
         "sensitivity-only",
         "instrument availability not catalogue-estimable",
         "declared baseline"),
        # -- demoted classes --
        ("galaxy drift/usability", "galaxy", "all", "not calibrated",
         "sensitivity-only",
         "no credible public calibration path (resolved sizes vary, "
         "no stable point reference)", "removed from primary; synthetic "
         "layer only"),
        ("galaxy_cluster drift/usability", "galaxy_cluster", "all",
         "not calibrated", "sensitivity-only",
         "extended sources; centroid definition unstable", "removed from "
         "primary; synthetic layer only"),
        # -- corruption / encoding parameters (unchanged scenario inputs) --
        ("p_mismatch", "all", "corruption model", "0.05 baseline",
         "extrapolated", "declared scenario parameter (not astrophysical)",
         "swept 0..0.5 in E2/E3"),
        ("sigma_obs", "all", "corruption model", "1e-4 rad",
         "extrapolated", "declared observational-noise scenario",
         "swept 1e-6..1e-2 in E4"),
        ("storage bits", "all", "encoding", "32", "extrapolated",
         "encoding design choice", "swept 8..64 in E6"),
    ]
    df = pd.DataFrame(rows, columns=cols)
    df.to_csv(CAL / "calibration_parameter_classification.csv", index=False)
    return df


def motion_summary(cls, rates_masyr, source_note):
    return dict(source_class=cls, n=len(rates_masyr),
                median_masyr=float(np.median(rates_masyr)),
                q25_masyr=float(np.quantile(rates_masyr, 0.25)),
                q75_masyr=float(np.quantile(rates_masyr, 0.75)),
                p90_masyr=float(np.quantile(rates_masyr, 0.9)),
                max_masyr=float(np.max(rates_masyr)),
                source=source_note)
