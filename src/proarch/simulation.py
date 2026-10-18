"""Monte Carlo engine: one replication of the encode -> degrade -> reconstruct
pipeline, plus grid runners producing tidy result frames.
"""
import numpy as np
import pandas as pd

from . import (architectures, degradation, encoding, geometry, misidentify,
               reconstruct)
from .info_cost import cost_for_encoding


def run_replication(spec, t_years, rng, *,
                    severity="baseline", geometry_kind="isotropic",
                    optimize=False,
                    sigma_obs=0.0, p_mismatch=0.0,
                    mismatch_model="permutation",
                    estimator="ransac", chirality=True,
                    mirror_ambiguity=True, n_chirality_store=None,
                    encoding_edges="none", k_knn=3, bits=32,
                    nc_random_b=False, ransac_n_iter=120,
                    ransac_tol_deg=2.0, direct_axis=False):
    """One encode/degrade/reconstruct replication. Returns diagnostics dict."""
    pop = architectures.build_population(spec, rng, geometry_kind, optimize)
    Q, labels = pop["Q"], pop["labels"]
    n = Q.shape[0]
    N0 = geometry.normalize(rng.normal(size=3))  # random true north per rep
    if direct_axis:
        # direct-axis landmark: the source's direction IS the stored axis
        # (a Polaris-like "this object points north" scheme).
        N0 = Q[0].copy()

    edges = None
    if encoding_edges == "knn":
        edges = geometry.knn_graph_edges(Q, k_knn)
    rec = encoding.encode(Q, N0, sparse_edges=edges, chirality=chirality,
                          rng=rng)
    if nc_random_b:  # NC1: stored cosines unrelated to true north
        rec["b"] = rng.uniform(-1.0, 1.0, n)
    bits_cost = cost_for_encoding(rec, bits=bits)

    # --- storage quantization at the declared precision (uniform on [-1, 1])
    levels = 2 ** int(bits) - 1
    rec["b"] = np.clip(np.round((rec["b"] + 1.0) / 2.0 * levels)
                       / levels * 2.0 - 1.0, -1.0, 1.0)
    if "edge_w" in rec:
        rec["edge_w"] = np.clip(np.round((rec["edge_w"] + 1.0) / 2.0 * levels)
                                / levels * 2.0 - 1.0, -1.0, 1.0)

    # --- degradation: independent per-source usability draws
    p_use = degradation.usability_table(labels, t_years, severity)
    usable = rng.random(n) < p_use
    Q_obs = Q[usable].copy()
    b_obs = rec["b"][usable].copy()
    alive_idx = np.where(usable)[0]

    # --- class-specific secular direction drift (proper-motion dispersal)
    # Scenario assumption: characteristic angular drift rate per class (rad/yr).
    DRIFT = {"star": 5e-7, "pulsar": 1e-7, "quasar": 1e-9,
             "galaxy": 2e-9, "galaxy_cluster": 2e-9}
    if len(Q_obs):
        sig_drift = np.array([DRIFT[c] for c in labels[usable]]) * t_years
        sig = np.sqrt(sig_drift ** 2 + sigma_obs ** 2)
        if sig.max() > 0:
            # per-source perturbation magnitude
            e1 = np.cross(Q_obs, np.tile([0.0, 0.0, 1.0], (len(Q_obs), 1)))
            badmask = np.linalg.norm(e1, axis=1) < 1e-9
            e1[badmask] = np.cross(Q_obs[badmask],
                                   np.tile([0.0, 1.0, 0.0], (badmask.sum(), 1)))
            e1 = geometry.normalize(e1)
            e2 = np.cross(Q_obs, e1)
            a = rng.normal(0.0, 1.0, len(Q_obs)) * sig
            bb = rng.normal(0.0, 1.0, len(Q_obs)) * sig
            Q_obs = geometry.normalize(Q_obs + a[:, None] * e1 + bb[:, None] * e2)

    # --- misidentification
    Q_obs, b_obs, bad = misidentify.MODELS[mismatch_model](
        Q_obs, b_obs, p_mismatch, rng)

    # --- stored-edge consistency check: a source whose observed pairwise
    # cosines disagree with most of its stored edges is wrongly identified
    # (substitution/injection); drop it before estimation. Permutation
    # corrupts b only and cannot be detected this way.
    if "edges" in rec and len(Q_obs) and len(alive_idx):
        idx_map = {old: new for new, old in enumerate(alive_idx)}
        deg = np.zeros(len(Q_obs), dtype=int)
        bad_e = np.zeros(len(Q_obs), dtype=int)
        for (i, j), cw in zip(rec["edges"], rec["edge_w"]):
            if i in idx_map and j in idx_map:
                a_, b_ = idx_map[i], idx_map[j]
                deg[a_] += 1
                deg[b_] += 1
                tol = 3.0 * (sig[a_] + sig[b_]) + 4.0 / levels
                if abs(float(Q_obs[a_] @ Q_obs[b_]) - cw) > tol:
                    bad_e[a_] += 1
                    bad_e[b_] += 1
        drop = (deg > 0) & (bad_e > 0.5 * deg)
        # rows appended by injection have no stored correspondence at all
        drop[len(alive_idx):] = True
        if drop.any():
            keep = ~drop
            Q_obs, b_obs = Q_obs[keep], b_obs[keep]
            alive_idx = alive_idx[keep[:len(alive_idx)]]
        # if every row was dropped, reconstruct() fails with an empty input
        # rather than returning a baseless solution

    # --- reconstruct
    if direct_axis:
        # decode = the landmark's future-observed direction, used directly as
        # the recovered axis; no relational scalar is inverted. Loss of the
        # landmark (or its misidentified substitution, which corrupts the
        # observed direction in place) propagates straight to the estimate.
        pos = np.where(alive_idx == 0)[0]
        if len(pos) == 0:
            res = {"success": False, "failure_reason": "landmark_lost"}
        else:
            res = {"success": True, "north_vector": Q_obs[pos[0]],
                   "residual": 0.0, "estimator": "direct_axis",
                   "n_sources_used": 1}
    else:
        kw = dict(n_iter=ransac_n_iter, tol_deg=ransac_tol_deg) if estimator == "ransac" else {}
        res = reconstruct.reconstruct(Q_obs, b_obs, estimator=estimator, rng=rng,
                                      **kw)
    out = {"n": n, "n_usable": int(usable.sum()),
           "n_bad": int(bad.sum()), "bits": bits_cost}
    if not res["success"]:
        out.update({"err_deg": np.nan, "success": False,
                    "failure_reason": res["failure_reason"],
                    "mirror_wrong": False, "chirality_used": False})
        return out

    n_hat = res["north_vector"]

    # --- mirror ambiguity & chirality resolution
    # The observer's recovered frame is mirrored with probability 0.5.
    # If mirrored, the correct original-frame north is reflect(n_hat, m).
    # A stored chirality subset lets the observer detect the mirror from sign
    # disagreement of triple products (frac < 0.5 -> decide mirrored).
    mirror_wrong = False
    chirality_used = False
    if mirror_ambiguity:
        mirrored = rng.random() < 0.5
        m = geometry.normalize(rng.normal(size=3))
        frac = None
        if chirality:
            idx_map = {old: new for new, old in enumerate(alive_idx)}
            triples = []
            for i, j, k, s in rec.get("chirality", []):
                if i in idx_map and j in idx_map and k in idx_map:
                    triples.append((idx_map[i], idx_map[j], idx_map[k], s))
            f = reconstruct.check_chirality(Q_obs, triples)
            # a mirrored frame inverts every triple-product sign
            frac = None if f is None else ((1.0 - f) if mirrored else f)
        if frac is not None:
            chirality_used = True
            decided_mirror = frac < 0.5
            # mirrored recovery -> uncorrected answer is the reflected
            # solution; a correct mirror decision undoes the reflection
            if mirrored:
                if not decided_mirror:
                    n_hat = reconstruct.reflect(n_hat, m)
            elif decided_mirror:
                n_hat = reconstruct.reflect(n_hat, m)
            mirror_wrong = (decided_mirror != mirrored)
        else:
            guessed_mirror = rng.random() < 0.5
            if mirrored != guessed_mirror:
                n_hat = reconstruct.reflect(n_hat, m)
            mirror_wrong = (guessed_mirror != mirrored)

    err = geometry.angular_error_deg(n_hat, N0)
    out.update({"err_deg": err, "success": True,
                "failure_reason": "", "residual": res["residual"],
                "estimator": res["estimator"],
                "n_sources_used": res["n_sources_used"],
                "mirror_wrong": mirror_wrong,
                "chirality_used": chirality_used})
    return out


def run_scenario(name, spec, t_years, n_mc, master_seed, **kw):
    rng = np.random.default_rng(master_seed)
    rows = []
    for rep in range(n_mc):
        r = run_replication(spec, t_years, rng, **kw)
        r["scenario"] = name
        r["t_years"] = t_years
        r["rep"] = rep
        rows.append(r)
    return pd.DataFrame(rows)


def run_grid(scenarios, n_mc, master_seed):
    """scenarios: list of dicts {name, spec, t_years, **kw}."""
    frames = []
    for i, sc in enumerate(scenarios):
        sc = dict(sc)
        name = sc.pop("name")
        spec = sc.pop("spec")
        t = float(sc.pop("t_years"))
        frames.append(run_scenario(name, spec, t, n_mc,
                                   master_seed + 7919 * i, **sc))
    return pd.concat(frames, ignore_index=True)
