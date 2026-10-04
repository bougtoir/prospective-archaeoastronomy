"""Source misidentification models."""
import numpy as np

from . import geometry


def correspondence_permutation(Q_obs, b_obs, p_mismatch, rng):
    """Permute a fraction of the b correspondences (stored labels wrong).

    Each kept source's stored cosine is randomly swapped with probability
    p_mismatch — the label exists but points to the wrong encoded value.
    """
    n = len(b_obs)
    b = b_obs.copy()
    flag = rng.random(n) < p_mismatch
    idx = np.where(flag)[0]
    if len(idx) > 1:
        b[idx] = b[rng.permutation(idx)]
    elif len(idx) == 1:
        b[idx] = rng.uniform(-1, 1)  # single bad label -> unrelated cosine
    return Q_obs, b, flag


def wrong_catalogue_substitution(Q_obs, b_obs, p_mismatch, rng):
    """A fraction of observed directions replaced by unrelated sources
    whose stored cosine still claims they are the original source."""
    n = Q_obs.shape[0]
    flag = rng.random(n) < p_mismatch
    Q = Q_obs.copy()
    Q[flag] = geometry.sample_isotropic(int(flag.sum()), rng)
    return Q, b_obs, flag


def isotropic_injection(Q_obs, b_obs, p_mismatch, rng):
    """Inject additional isotropic sources with junk cosines; flagged rows
    appended at the end (they have no valid stored cosine)."""
    n_new = int(round(p_mismatch * len(b_obs)))
    if n_new == 0:
        return Q_obs, b_obs, np.zeros(len(b_obs), bool)
    Q_new = geometry.sample_isotropic(n_new, rng)
    b_new = rng.uniform(-1, 1, n_new)
    Q = np.vstack([Q_obs, Q_new])
    b = np.concatenate([b_obs, b_new])
    flag = np.concatenate([np.zeros(len(b_obs), bool), np.ones(n_new, bool)])
    return Q, b, flag


MODELS = {
    "permutation": correspondence_permutation,
    "substitution": wrong_catalogue_substitution,
    "injection": isotropic_injection,
}
