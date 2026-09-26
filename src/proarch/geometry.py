"""Geometry utilities: unit-sphere sampling, perturbations, conditioning."""
import numpy as np


def radec_to_unit(ra_deg, dec_deg):
    ra = np.deg2rad(np.asarray(ra_deg, dtype=float))
    dec = np.deg2rad(np.asarray(dec_deg, dtype=float))
    return np.stack([np.cos(dec) * np.cos(ra),
                     np.cos(dec) * np.sin(ra),
                     np.sin(dec)], axis=-1)


def unit_to_radec(q):
    q = np.asarray(q, dtype=float)
    ra = np.degrees(np.arctan2(q[..., 1], q[..., 0])) % 360.0
    dec = np.degrees(np.arcsin(np.clip(q[..., 2], -1, 1)))
    return ra, dec


def normalize(v):
    v = np.asarray(v, dtype=float)
    return v / np.linalg.norm(v, axis=-1, keepdims=True)


def sample_isotropic(n, rng):
    """Uniform on S^2."""
    z = rng.uniform(-1.0, 1.0, n)
    phi = rng.uniform(0.0, 2.0 * np.pi, n)
    r = np.sqrt(np.clip(1.0 - z * z, 0.0, 1.0))
    return np.stack([r * np.cos(phi), r * np.sin(phi), z], axis=-1)


def sample_clustered(n, rng, n_centers=None, spread_rad=np.deg2rad(15.0)):
    """Mixture of tight clusters on S^2 (vMF-like via tangent Gaussian)."""
    if n_centers is None:
        n_centers = max(1, n // 10)
    centers = sample_isotropic(n_centers, rng)
    assign = rng.integers(0, n_centers, n)
    return perturb_directions(centers[assign], spread_rad, rng)


def sample_banded(n, rng, band_normal=None, band_sigma_rad=np.deg2rad(10.0)):
    """Concentrated near a great-circle band."""
    if band_normal is None:
        band_normal = normalize(rng.normal(size=3))
    u = normalize(np.cross(band_normal, [1.0, 0.0, 0.0]) + 1e-12)
    if np.linalg.norm(u) < 1e-6:
        u = normalize(np.cross(band_normal, [0.0, 1.0, 0.0]))
    v = np.cross(band_normal, u)
    t = rng.uniform(0.0, 2.0 * np.pi, n)
    off = rng.normal(0.0, band_sigma_rad, n)
    dirs = (np.cos(t)[:, None] * u + np.sin(t)[:, None] * v +
            np.tan(off)[:, None] * band_normal[None, :])
    return normalize(dirs)


def perturb_directions(q, sigma_rad, rng):
    """Tangent-plane Gaussian perturbation of unit vectors, renormalized."""
    q = np.asarray(q, dtype=float)
    n = q.shape[0]
    e1 = np.cross(q, np.tile([0.0, 0.0, 1.0], (n, 1)))
    mask = np.linalg.norm(e1, axis=1) < 1e-9
    e1[mask] = np.cross(q[mask], np.tile([0.0, 1.0, 0.0], (mask.sum(), 1)))
    e1 = normalize(e1)
    e2 = np.cross(q, e1)
    a = rng.normal(0.0, sigma_rad, n)
    b = rng.normal(0.0, sigma_rad, n)
    return normalize(q + a[:, None] * e1 + b[:, None] * e2)


def sample_vmf(q, kappa, rng):
    """Approximate von Mises-Fisher perturbation; kappa -> inf gives sigma~1/sqrt(kappa)."""
    sigma = 1.0 / np.sqrt(kappa)
    return perturb_directions(q, sigma, rng)


def condition_metrics(Q):
    """Return (kappa, logdet) of Q^T Q."""
    A = Q.T @ Q
    kappa = np.linalg.cond(A)
    sign, logdet = np.linalg.slogdet(A)
    return kappa, (logdet if sign > 0 else -np.inf)


def knn_graph_edges(Q, k):
    """k-nearest-angular-neighbor edge list (i<j)."""
    G = Q @ Q.T
    np.fill_diagonal(G, -np.inf)
    edges = set()
    for i in range(Q.shape[0]):
        for j in np.argsort(-G[i])[:k]:
            edges.add((min(i, j), max(i, j)))
    return sorted(edges)


def d_optimal_select(candidates, n_select):
    """Greedy D-optimal selection maximizing log det(Q^T Q)."""
    idx = []
    pool = list(range(candidates.shape[0]))
    # start from farthest-from-mean triple for stability
    for _ in range(n_select):
        best, best_val = None, -np.inf
        for j in pool:
            trial = idx + [j]
            A = candidates[trial].T @ candidates[trial]
            sign, ld = np.linalg.slogdet(A + 1e-12 * np.eye(3))
            if sign > 0 and ld > best_val:
                best, best_val = j, ld
        if best is None:
            best = pool[0]
        idx.append(best)
        pool.remove(best)
    return np.array(idx)


def angular_error_deg(n_hat, n0):
    return float(np.degrees(np.arccos(np.clip(np.dot(n_hat, n0), -1.0, 1.0))))
