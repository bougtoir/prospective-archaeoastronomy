# MODEL VALIDATION REPORT — SMPT revision

Scope: the three-layer simulation of `Observation-Calibrated Celestial
Reference Networks for Long-Horizon Orientation Reconstruction`.
V&V categories follow Sargent (2013, J. Simulation 7:12–24).

## What was validated, and against what

1. Unit/identity tests — `tests/` 16 tests PASS (encoding sufficiency,
   estimator correctness, mirror/chirality, geometry conditioning).
2. Known synthetic truth recovery — zero-noise/drift/loss/mismatch runs
   recover N0 to machine precision (§3.1).
3. Catalogue geometry reproduction — calibrated populations drawn verbatim
   from stored catalogue positions; real anisotropy inherited, not assumed
   (Figure 8).
4. Empirical distribution validation — `source_motion_calibration.csv`:
   Gaia |PM| median 37.4 mas/yr; ATNF measured PMTOT median 8.9 mas/yr
   (n=629); quasar log-uniform prior; missingness quantified in
   `missingness_report.csv` (no silent complete-case filtering).
5. Calibration diagnostics — `calibration_registry.csv` +
   `calibration_parameter_classification.csv`: every parameter classified
   observed/derived/literature-constrained/extrapolated/sensitivity-only.
6. Gaia quality-cut sensitivity — S5: strict subset (ruwe<=1.1,
   visibility>=10) vs baseline pool; effect bounded in
   `sensitivity_summary.csv`.
7. Pulsar complete-case vs imputed sensitivity — primary is complete-case
   (measured PMTOT only); S1 resamples missing PMs from the empirical CDF
   as a declared secondary model with uncertainty propagated per-rep.
8. ICRF defining-source vs broader sensitivity — S6 restricts the pool to
   defining-flag sources; reported in `sensitivity_summary.csv`.
9. Propagation-model comparison — angular-linear vs 3D-Cartesian
   constant-velocity on the RV-measured Gaia subset;
   `propagation_comparison.csv` + Figure 10: agreement <1e-6 deg at 1e3 yr;
   divergence quantified to 1e6 yr (median |diff| 1.22 deg).
10. Repeated population resampling validation — per-replication population
    resampling (fresh subset each rep; D-optimal selections over an
    ensemble of 25 selections): reported P-values are averages over resampled
    populations.
11. Short-horizon sanity — propagation comparison at 1e3 yr agrees with
    directly propagated catalogue values to numerical tolerance.

## What remains unvalidated / domain of validity

- Pulsar PMTOT exists for 629/3470 — a distance/observability selection
  effect bracketed by S1, not eliminated.
- Characteristic age is a proxy timescale, not a lifetime.
- Quasar apparent motion is a literature-constrained prior, not catalogue-
  measured (S4 bounds it x0.1/x10).
- No empirical survival constraint beyond ~10^6 yr: 10^7–10^8 yr results
  are stress tests outside the validated domain.
- Observational noise modelled isotropically; correlated systematics
  untested.

VERDICT: PASS — verification complete, calibration empirical or classified,
missingness reported, residual assumptions bounded, validation domain
stated.

## Finishing-pass re-verification (2026-11-09)

No scientific model, code, configuration or result changed in the
finishing pass (labels/metadata/provenance/package only). Validation items
1-11 stand as audited; resampling terminology remains "repeated population
resampling validation".

VERDICT: PASS (unchanged).
