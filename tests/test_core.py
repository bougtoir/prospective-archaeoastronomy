import numpy as np
import pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from proarch import (encoding, geometry, misidentify, reconstruct,  # noqa
                     simulation, architectures, degradation)


def test_radec_roundtrip():
    ra = np.array([0.0, 123.4, 359.9])
    dec = np.array([-45.0, 0.0, 89.9])
    q = geometry.radec_to_unit(ra, dec)
    ra2, dec2 = geometry.unit_to_radec(q)
    assert np.allclose(ra % 360, ra2, atol=1e-6)
    assert np.allclose(dec, dec2, atol=1e-6)


def test_isotropic_unit():
    q = geometry.sample_isotropic(500, np.random.default_rng(0))
    assert np.allclose(np.linalg.norm(q, axis=1), 1.0)


def test_perfect_reconstruction():
    rng = np.random.default_rng(1)
    Q = geometry.sample_isotropic(30, rng)
    N0 = geometry.normalize(rng.normal(size=3))
    b = encoding.encode_north(Q, N0)
    for est in ("ls", "huber", "ransac"):
        r = reconstruct.reconstruct(Q, b, estimator=est, rng=rng)
        assert r["success"]
        assert geometry.angular_error_deg(r["north_vector"], N0) < 1e-6


def test_insufficient_sources_fail():
    Q = geometry.sample_isotropic(2, np.random.default_rng(0))
    b = Q @ np.array([0, 0, 1.0])
    for est in ("ls", "huber", "ransac"):
        assert not reconstruct.reconstruct(Q, b, estimator=est)["success"]


def test_ransac_beats_ls_under_outliers():
    rng = np.random.default_rng(3)
    N0 = np.array([0, 0, 1.0])
    errs = {"ls": [], "ransac": []}
    for _ in range(50):
        Q = geometry.sample_isotropic(30, rng)
        b = Q @ N0
        bad = rng.random(30) < 0.3
        b[bad] = rng.uniform(-1, 1, bad.sum())
        for est in errs:
            r = reconstruct.reconstruct(Q, b, estimator=est, rng=rng)
            errs[est].append(geometry.angular_error_deg(r["north_vector"], N0))
    assert np.median(errs["ransac"]) < np.median(errs["ls"])


def test_chirality_triples_signs():
    rng = np.random.default_rng(5)
    Q = geometry.sample_isotropic(20, rng)
    triples = encoding.chirality_triples(Q, rng=rng)
    assert triples
    frac = reconstruct.check_chirality(Q, triples)
    assert frac == pytest.approx(1.0)
    # reflected configuration inverts signs
    Qr = Q @ np.diag([1, 1, -1])
    frac_r = reconstruct.check_chirality(Qr, triples)
    assert frac_r == pytest.approx(0.0)


def test_single_landmark_fails_in_simulation():
    rng = np.random.default_rng(7)
    out = simulation.run_replication(
        {"star": 1}, 1e3, rng, sigma_obs=0.0, p_mismatch=0.0,
        mirror_ambiguity=False)
    assert not out["success"]


def test_network_recovers_under_partial_loss():
    rng = np.random.default_rng(11)
    errs = []
    for _ in range(30):
        out = simulation.run_replication(
            {"quasar": 50}, 1e3, rng, sigma_obs=1e-4, p_mismatch=0.0,
            severity="baseline", chirality=True)
        if out["success"]:
            errs.append(out["err_deg"])
    assert np.median(errs) < 0.01  # ~1e-4 rad noise -> < 0.01 deg error


def test_direct_axis_landmark_works_short_horizon():
    rng = np.random.default_rng(13)
    errs = []
    for _ in range(30):
        out = simulation.run_replication(
            {"star": 1}, 1e3, rng, sigma_obs=0.0, p_mismatch=0.0,
            mirror_ambiguity=False, direct_axis=True)
        assert out["success"]
        errs.append(out["err_deg"])
    assert np.median(errs) < 1.0


def test_direct_axis_fails_when_landmark_lost():
    # pessimistic long-horizon: the landmark is almost surely unusable
    rng = np.random.default_rng(17)
    lost = 0
    for _ in range(50):
        out = simulation.run_replication(
            {"star": 1}, 1e8, rng, severity="pessimistic",
            sigma_obs=0.0, p_mismatch=0.0, mirror_ambiguity=False,
            direct_axis=True)
        if not out["success"]:
            lost += 1
            assert out["failure_reason"] == "landmark_lost"
    assert lost > 40


def test_wilson_ci_bounds():
    from proarch.stats import wilson_ci
    p, lo, hi = wilson_ci(90, 100)
    assert 0.8 < lo < p < hi < 1.0


def test_drift_degrades_stars():
    rng = np.random.default_rng(13)
    errs = []
    for _ in range(20):
        out = simulation.run_replication(
            {"star": 50}, 1e5, rng, sigma_obs=0.0, p_mismatch=0.0,
            chirality=True)
        if out["success"]:
            errs.append(out["err_deg"])
    assert len(errs) > 10 and np.median(errs) > 1.0  # drift dominates at 1e5 yr


def test_edge_check_drops_injected_sources():
    rng = np.random.default_rng(17)
    ok = 0
    for _ in range(30):
        out = simulation.run_replication(
            {"quasar": 50}, 1e3, rng, sigma_obs=1e-4, p_mismatch=0.5,
            mismatch_model="injection", encoding_edges="knn",
            chirality=True)
        if out["success"] and out["err_deg"] < 1.0:
            ok += 1
    assert ok >= 25  # injected fakes dropped -> low noise regime reconstructs


def test_edge_check_all_drop_fails_not_fakes():
    rng = np.random.default_rng(19)
    for _ in range(20):
        out = simulation.run_replication(
            {"quasar": 50}, 1e3, rng, sigma_obs=0.0, p_mismatch=1.0,
            mismatch_model="substitution", encoding_edges="knn",
            chirality=True)
        assert not out["success"]  # every stored edge inconsistent -> empty
