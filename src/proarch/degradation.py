"""Scenario-based source usability models over deep time.

IMPORTANT: these are declared scenario assumptions, not fitted astrophysical
survival functions. p_usable combines physical survival, identifiability,
observability, and reference usability into one operational probability.

S_k(t) = exp(-(t / tau_k) ** a_k)   (Weibull form; a_k=1 is exponential)

tau_k is scaled by a scenario multiplier in {pessimistic, baseline, optimistic}.
Orders chosen so that quasars/galaxies are the most durable reference sources,
stars the least, consistent with their qualitative failure modes
(stellar proper-motion dispersal + finite lifetimes vs. quasi-fixed
extragalactic positions); see manuscript Methods and the reference audit.
"""
import numpy as np

# Baseline characteristic usability times (years). Scenario assumptions.
BASE_TAU = {
    "star": 3e5,
    "pulsar": 3e6,
    "quasar": 3e8,
    "galaxy": 1e8,
    "galaxy_cluster": 1e8,
}

# Weibull shape per class (scenario assumption).
BASE_A = {
    "star": 1.0,
    "pulsar": 1.0,
    "quasar": 0.7,
    "galaxy": 0.7,
    "galaxy_cluster": 0.7,
}

TAU_MULTIPLIER = {"pessimistic": 0.3, "baseline": 1.0, "optimistic": 3.0}


def p_usable(cls, t_years, severity="baseline"):
    tau = BASE_TAU[cls] * TAU_MULTIPLIER[severity]
    a = BASE_A[cls]
    t = np.asarray(t_years, dtype=float)
    return np.exp(-((t / tau) ** a))


def usability_table(labels, t_years, severity="baseline"):
    """Vector of p_usable for each source given its class label."""
    return np.array([p_usable(c, t_years, severity) for c in labels])


def piecewise_usable(points, t_years):
    """Piecewise-linear usability from (t, p) control points."""
    xs, ys = zip(*sorted(points))
    return np.clip(np.interp(t_years, xs, ys), 0.0, 1.0)
