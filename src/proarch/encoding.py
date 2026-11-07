"""Relational encoding of terrestrial orientation into a celestial network."""
import numpy as np


def encode_north(Q, N0):
    """b_i = q_i^T N0 (cosines of source-north angles)."""
    return Q @ N0


def gram_matrix(Q):
    """G_ij = q_i^T q_j = cos(theta_ij)."""
    return Q @ Q.T


def chirality_triples(Q, max_triples=None, rng=None):
    """Signed triple products H_ijk = sign(det(q_i, q_j, q_k)) for a subset.

    Returns list of (i, j, k, sign). A sparse deterministic subset (~2n plus
    n random triples when rng is given) keeps storage cost low while still
    constraining the global handedness of the configuration.
    """
    n = Q.shape[0]
    idxs = set()
    for i in range(n):
        j, k = (i + 1) % n, (i + 2) % n
        if len({i, j, k}) == 3:
            idxs.add((i, j, k))
    stride = max(1, n // 4)
    for i in range(0, n, stride):
        j, k = (i + stride) % n, (i + 2 * stride) % n
        if len({i, j, k}) == 3:
            idxs.add((i, j, k))
    if rng is not None:
        for t in rng.integers(0, n, (n, 3)):
            if len(set(t)) == 3:
                idxs.add(tuple(int(x) for x in t))
    triples = []
    for i, j, k in sorted(idxs):
        s = np.sign(np.linalg.det(np.stack([Q[i], Q[j], Q[k]])))
        if s != 0:
            triples.append((i, j, k, int(s)))
    if max_triples is not None:
        triples = triples[:max_triples]
    return triples


def encode(Q, N0, sparse_edges=None, chirality=False, rng=None):
    """Full encoding record."""
    rec = {"b": encode_north(Q, N0), "n": Q.shape[0]}
    if sparse_edges is not None:
        rec["edges"] = sparse_edges
        rec["edge_w"] = np.array([Q[i] @ Q[j] for i, j in sparse_edges])
    if chirality:
        rec["chirality"] = chirality_triples(Q, rng=rng)
    return rec
