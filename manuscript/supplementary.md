# Supplementary material

## S1. Encoding schema

Per replication record: `n`, `n_usable`, `n_bad`, `bits`, `err_deg`,
`success`, `failure_reason`, `residual`, `estimator`, `n_sources_used`,
`mirror_wrong`, `chirality_used`. Per-replication CSVs in `results/`;

scenario names encode experiment | parameter blocks.

## S2. Extended sensitivity tables

- `results/summary_e1.csv` — all 19 architectures x 6 horizons.
- `results/summary_e4.csv` — observational-noise sweep (sigma_obs 0–1e-2 rad).
- `results/summary_e7.csv` — class-allocation grid search (n_tot in {20,30,50}).
- `results/summary_e10.csv` — homogeneous-network scaling curves.
- `results/summary_e11.csv` — M1b direct-axis landmark control (baseline and
  catalogue-substitution variants).

## S3. Scenario assumptions

Usability time constants tau_k and Weibull shapes a_k; class-specific secular
drift rates; mirror prior 0.5; source-ID width 40 bits; metadata 128 bits;
RANSAC inlier tolerance 2 deg (cosine-domain), 120 iterations. All are declared
assumptions listed in Table 2, not measurements.

## S5. Hypothesis status (final)

H2 (heterogeneous networks outperform equal-size homogeneous ones) was not
supported under the baseline scenario: homogeneous quasar networks
outperformed the tested hybrid designs at 10^7–10^8 yr, and the composition
grid search selected homogeneous quasar allocations. Heterogeneity is treated
as condition-dependent, not automatically beneficial. Full per-hypothesis
status: `qc/hypothesis_status_final.csv`.

## S4. Exploratory 10^9 yr

Available on request by rerunning with `time_grid_exploratory_years`; reported
as exploratory only.
