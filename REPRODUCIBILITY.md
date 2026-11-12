# Reproducibility documentation — prospective-archaeoastronomy

Repository documentation (not part of the journal submission package).

## Reproduction

    python3 -m venv .venv && .venv/bin/pip install -e ".[dev]" && make all PYTHON=.venv/bin/python

`make all` = pytest (16) → synthetic grid → calibrated scenarios (352,000 reps)
→ sensitivity branches S1–S6 (25,000 reps) → summaries → theory-vs-calibrated
verdicts → figures → tables → manuscript values → DOCX builds → package → QC.

Master seed: 20260924 (configs/default.yaml). Calibrated seed = master+5555;
sensitivity seed = master+900. N_MC = 2000 (calibrated), 10,000 (synthetic core).

## Per-replication output schema

Each Monte Carlo replication records: `n`, `n_usable`, `n_bad`, `bits`,
`err_deg`, `success`, `failure_reason`, `residual`, `estimator`,
`n_sources_used`, `mirror_wrong`, `chirality_used`. Per-replication CSVs live
in `results/` and `results/calibration/`; scenario names encode experiment |
parameter blocks (calibrated scenarios are prefixed `C_`, matched synthetic
`S_`, sensitivity branches `S1`–`S6`).

## Result file inventory

- `results/summary_e1.csv` — all 19 architectures x 6 horizons (synthetic).
- `results/summary_e4.csv` — observational-noise sweep (sigma_obs 0–1e-2 rad).
- `results/summary_e7.csv` — class-allocation grid search (n_tot in {20,30,50}).
- `results/summary_e10.csv` — homogeneous-network scaling curves.
- `results/summary_e11.csv` — M1b direct-axis landmark control (baseline and
  catalogue-substitution variants).
- `results/calibration/calibrated_reps.csv` — all calibrated per-replication
  records including random/optimized tags and stress horizons.
- `results/calibration/calibrated_summary.csv` — per-scenario calibrated
  summaries with Wilson 95% intervals.
- `results/calibration/sensitivity_summary.csv` — S1–S6 sensitivity branches:
  S1 pulsar missing-PM empirical-CDF resample; S2 stellar existence timescale
  5e8–2e10 yr; S3 pulsar existence multiplier k in {0.3, 3}; S4 quasar
  apparent-motion prior x0.1/x10; S5 Gaia strict astrometric quality
  (ruwe <= 1.1, visibility >= 10); S6 ICRF3 defining sources only.

## Catalogue acquisition and calibration artefacts

- `data/acquisition_ledger.csv` — per-file URL/query, UTC time, size, SHA-256.
- `data/raw/gaia_slices_20261030/QUERY_MANIFEST.txt` — the 24 sky-tiling
  Gaia TAP queries (one contiguous source_id range per slice).
- `results/calibration/calibration_registry.csv` — every calibrated parameter
  with source, derivation script, uncertainty, and manuscript usage.
- `results/calibration/calibration_parameter_classification.csv` — the
  observed/derived/literature-constrained/extrapolated/sensitivity-only
  classification (Table 4 of the manuscript).
- `results/calibration/missingness_report.csv` — per-field missingness for
  all three catalogues; no imputation in the primary analysis.
- `results/calibration/source_motion_calibration.csv` — measured motion
  distributions and the quasar apparent-motion prior.
- `results/calibration/propagation_comparison.csv` — angular-linear versus
  3D-Cartesian propagation of the Gaia sample.
- `results/calibration/theory_vs_calibrated_findings.csv` — the eight
  pre-declared findings (A–H) with computed synthetic evidence, computed
  calibrated evidence, and the classification used in Table 9.
- `qc/` — all QC audit reports (model validation, hardcode, references,
  semantic citations, figure/table identity, OMML, visual render,
  reproducibility).

## Canonical provenance

`qc/CANONICAL_FREEZE.md` records the canonical scientific commit. The
historical ASR freeze b4b2cd52a1ef50ae4b5e9999dc0cd0f3b1978b7e is preserved
as a historical reproducibility point and is never overwritten.
