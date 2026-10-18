"""Robust reconstruction of the stored north vector.

Problem: given observed directions Q_obs (n x 3) and stored cosines b,
estimate n_hat = argmin_{||n||=1} ||Q_obs n - b||^2.

Estimators: ordinary least squares (LS), Huber IRLS, RANSAC-like consensus.

Mirror (chirality) model: if the future observer recovers the source
configuration only up to an orthogonal transformation, a det(O) = -1
solution leaves north reflected across an unknown plane through the origin
(mirror ambiguity). A stored subset of signed triple products constrains
the handedness and resolves the ambiguity when enough triples survive.
"""
import numpy as np

from .geometry import normalize


def reflect(v, plane_normal):
    """Reflect v across the plane through the origin with given normal."""
    m = normalize(np.asarray(plane_normal, dtype=float))
    return v - 2.0 * (v @ m) * m


def _finish(n_vec, Q, b, estimator):
    if n_vec is None or not np.all(np.isfinite(n_vec)) or np.linalg.norm(n_vec) < 1e-12:
        return {"success": False, "failure_reason": "invalid_solution",
                "estimator": estimator, "n_sources_used": Q.shape[0]}
    n_hat = normalize(n_vec)
    r = Q @ n_hat - b
    return {"north_vector": n_hat, "success": True,
            "n_sources_used": Q.shape[0], "residual": float(np.linalg.norm(r)),
            "estimator": estimator}


def reconstruct_ls(Q, b):
    if Q.shape[0] < 3:
        return {"success": False, "failure_reason": "insufficient_sources",
                "estimator": "ls", "n_sources_used": Q.shape[0]}
    n_vec, *_ = np.linalg.lstsq(Q, b, rcond=None)
    return _finish(n_vec, Q, b, "ls")


def reconstruct_huber(Q, b, c=1.345, iters=50, tol=1e-10):
    if Q.shape[0] < 3:
        return {"success": False, "failure_reason": "insufficient_sources",
                "estimator": "huber", "n_sources_used": Q.shape[0]}
    n_vec, *_ = np.linalg.lstsq(Q, b, rcond=None)
    for _ in range(iters):
        r = b - Q @ n_vec
        s = np.median(np.abs(r)) * 1.4826 + 1e-12
        u = r / s
        w = np.where(np.abs(u) <= c, 1.0, c / np.maximum(np.abs(u), 1e-12))
        W = np.sqrt(w)
        n_new, *_ = np.linalg.lstsq(Q * W[:, None], b * W, rcond=None)
        if np.linalg.norm(n_new - n_vec) < tol * max(1.0, np.linalg.norm(n_vec)):
            n_vec = n_new
            break
        n_vec = n_new
    return _finish(n_vec, Q, b, "huber")


def reconstruct_ransac(Q, b, n_iter=200, tol_deg=2.0, rng=None):
    """RANSAC: sample minimal triples, score by inlier count, refit LS."""
    rng = rng or np.random.default_rng(0)
    n = Q.shape[0]
    if n < 3:
        return {"success": False, "failure_reason": "insufficient_sources",
                "estimator": "ransac", "n_sources_used": n}
    tol_cos = np.sin(np.deg2rad(tol_deg))  # |q.n - b| inlier threshold
    best_inliers = None
    for _ in range(n_iter):
        idx = rng.choice(n, size=3, replace=False)
        A = Q[idx]
        if abs(np.linalg.det(A)) < 1e-8:
            continue
        n_trial = np.linalg.solve(A, b[idx])
        if np.linalg.norm(n_trial) < 1e-9:
            continue
        n_trial = normalize(n_trial)
        resid = np.abs(Q @ n_trial - b)
        inliers = resid < tol_cos
        if best_inliers is None or inliers.sum() > best_inliers.sum():
            best_inliers = inliers
    if best_inliers is None or best_inliers.sum() < 3:
        return {"success": False, "failure_reason": "ransac_no_consensus",
                "estimator": "ransac", "n_sources_used": n}
    n_vec, *_ = np.linalg.lstsq(Q[best_inliers], b[best_inliers], rcond=None)
    out = _finish(n_vec, Q[best_inliers], b[best_inliers], "ransac")
    out["n_sources_used"] = int(best_inliers.sum())
    return out


ESTIMATORS = {"ls": reconstruct_ls, "huber": reconstruct_huber,
              "ransac": reconstruct_ransac}


def reconstruct(Q, b, estimator="ransac", rng=None, **kw):
    fn = ESTIMATORS[estimator]
    if estimator == "ransac":
        return fn(Q, b, rng=rng, **kw)
    return fn(Q, b, **kw)


def check_chirality(Q_obs, stored_triples):
    """Fraction of stored triples whose sign agrees in the observed frame."""
    agree = 0
    total = 0
    for i, j, k, s in stored_triples:
        if max(i, j, k) >= Q_obs.shape[0]:
            continue
        s_obs = np.sign(np.linalg.det(np.stack([Q_obs[i], Q_obs[j], Q_obs[k]])))
        if s_obs == 0:
            continue
        total += 1
        agree += int(s_obs == s)
    if total == 0:
        return None
    return agree / total
