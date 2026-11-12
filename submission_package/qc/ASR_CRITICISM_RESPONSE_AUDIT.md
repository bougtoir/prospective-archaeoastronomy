# ASR CRITICISM RESPONSE AUDIT — SMPT revision

Desk-rejection criticism addressed:
"key results depend heavily on ad-hoc synthetic scenario parameters without
observation-calibrated astrophysical grounding."

## Old arbitrary assumptions → disposition

| old assumption | disposition |
|---|---|
| fixed stellar drift 5e-7 rad/yr | REMOVED from primary; replaced by measured Gaia DR3 proper motions per source (median 37.4 mas/yr, full distribution used). Kept only inside the explicitly-labelled synthetic theory layer. |
| fixed pulsar drift 1e-7 rad/yr | REMOVED from primary; replaced by measured ATNF PMTOT on the n = 629 measured subset (median 8.9 mas/yr). Missing PMs never fabricated; sensitivity branch S1 resamples from the empirical CDF. |
| fixed quasar drift 1e-9 rad/yr | REMOVED from primary; replaced by a log-uniform 1e-3–1e-1 mas/yr literature-constrained prior (ICRF3 uncertainties + Charlot 1990 structure + Titov et al. 2011 aberration), sensitivity x0.1/x10 (S4). |
| Weibull usability tau (3e5/3e6/3e8/1e8 yr) | DEMOTED to the synthetic theory layer only. Calibrated usability = exists x identifiable x observable (Section 2.9): star exp(-t/tau_s) literature tau 5e9 (S2 bracketed); pulsar exp(-t/(k x median AGE)), k=1 bracketed 0.3–3 (S3), age explicitly not a lifetime; quasar exists = 1 as a conditional persistence assumption (classified sensitivity-only — not observed; quasar results conditional on source persistence and the apparent-motion model). No fabricated 10^6-yr survival curve. |
| isotropic sky geometry | REPLACED by actual catalogue geometry: Gaia sky-tiling sample, ATNF Galactic-plane concentration, ICRF3 anisotropic VLBI geometry with defining flags. |
| galaxy/cluster class | DEMOTED to synthetic layer: no credible observational calibration exists; absent from all primary calibrated scenarios. |
| 10^7–10^8 yr claims | SEPARATED: reported only as extrapolative stress tests, never as calibrated forecasts. |

## Answer to the criticism

- Which old arbitrary assumptions were removed: all class drift constants
  and the Weibull usability curve, from the primary analysis.
- Which were replaced with observed data: star drift (Gaia), pulsar drift
  (ATNF measured subset), sky geometry (all three catalogues), population
  sampling (per-replication resampling of the observed pools).
- Which are literature-constrained: quasar apparent motion (log-uniform
  prior, x0.1/x10 bounded), stellar existence timescale (S2 bracketed).
- Which remain extrapolative: pulsar existence multiplier k (S3 bracketed);
  all existence modelling beyond 10^6 yr (stress-test regime only).
- Whether main conclusions remain robust: 6 of 8 pre-declared conclusions
  CONFIRMED under calibration (redundancy, geometry, chirality, robust
  estimators, heterogeneity-not-beneficial, single-source fragility); 2
  PARTIALLY CONFIRMED (quasar dominance — absolute under calibrated priors
  at primary horizons, dominance at 1e8 remains class-conditional;
  finite precision — binds only in precision-limited regimes).

AUDIT VERDICT: the criticism is answered structurally — conclusions no longer
rest on unclassified ad-hoc parameters; the residual non-empirical parameters
are enumerated, classified, and sensitivity-bounded.
