# Observation-Calibrated Celestial Reference Networks for Long-Horizon Orientation Reconstruction

Tatsuki Onishi (corresponding author), Data Science and AI Innovation Research Promotion Center, Shiga University, 1-1-1 Bamba, Hikone, Shiga 522-8522, Japan. E-mail: bougtoir@gmail.com. ORCID: 0000-0001-7261-9062.

## Abstract

Terrestrial orientation is not permanently tied to any single celestial landmark: stars drift, pulsars fade from the beam line, and any individual reference source can be lost or misidentified over timescales far shorter than the horizons relevant to the longest-lived information systems. This paper formulates the recovery of a stored Earth spin-axis direction as a celestial reference-network reconstruction problem and evaluates it in a three-layer simulation study. Layer 1 is a general synthetic theory: a controlled parameter-space experiment that maps the recoverability surface P(recover | drift, loss, mismatch, geometry, precision, estimator, chirality) for seven reference-network architecture classes. Layer 2 is observation-calibrated validation: real Gaia DR3 bright stars (n = {{cal_n_gaia}}), ATNF pulsars (n = {{cal_n_atnf}}), and ICRF3 quasars (n = {{cal_n_icrf3}}) are mapped into that parameter space through measured proper motions, catalogue positions and geometry, and a literature-constrained extragalactic stability prior, and the same reconstruction task is run on networks built from the observed populations. Layer 3 separates far-horizon behaviour: the observation-anchored regime is 10^3–10^5 yr, 10^6 yr is reported as an extended physically constrained projection, and 10^7–10^8 yr runs are reported separately as extrapolative stress tests, not as calibrated forecasts. Under the calibrated models a 50-source ICRF3 quasar network achieved P(error < 1 deg) = {{c_quasar50_p1_t1e+06}} at 10^6 yr, while a single relational landmark still failed almost universally (invalid-solution probability {{single_star_p_invalid_mean}}). Eight pre-declared synthetic conclusions were then classified as confirmed, partially confirmed, reversed, or not testable under observation-based calibration (Section 3.7): redundancy, geometry, chirality control, robust estimation, and single-source fragility survived; quasar dominance and finite-precision relevance were qualified rather than absolute; and heterogeneity was again found not to be automatically beneficial. The central claim is a general recoverability framework whose parameter space can be calibrated with observed celestial source populations, separating physically constrained from extrapolative regimes.

## Keywords

celestial reference systems; robust estimation; simulation validation; observation-calibrated modelling; deep space navigation; redundancy; Monte Carlo methods

## 1. Introduction

Celestial landmarks are time-dependent. The "North Star" role has passed between stars on millennial timescales, and over 10^5–10^8 yr essentially every stellar source drifts far from its catalogue position. Modern astronautics already relies on reference *systems* rather than single objects: the International Celestial Reference System is realized by ensembles of quasars [arias1995icrs, charlot2020icrf3], Gaia maintains a kinematically non-rotating optical frame from hundreds of thousands of extragalactic sources [mignard2018gaiacrf2, lindegren2018gaiadr2, lindegren2021gaiaedr3], and spacecraft attitude determination fuses many stellar measurements rather than trusting any single star [spratling2009starid]. Pulsar-based navigation and timing extend the same logic to a second source class [downs1974pulsar, sheikh2006xnav, becker2013pulsarnav], and pulsar proper motions have been measured in bulk for decades [hobbs2005pulsarpm].

Encoding terrestrial orientation for recovery after 10^3–10^8 yr is therefore an extreme reference-system robustness problem, not a search for a future North Star. The engineering question is which *network* of sources, encoded with what relational information, leaves the original direction statistically reconstructable despite source loss, secular motion, misidentification, and finite measurement precision. The Pioneer plaque and Voyager pulsar map are early instances of exactly this encoding idea — terrestrial position was expressed relative to a pulsar network rather than to any single object [drake1972message, sagan1978murmurs] — but they were never analysed as a quantitative reconstruction problem with quantified failure regimes.

A persistent weakness of deep-time simulation studies, including earlier versions of this one, is that their headline numbers rest on ad-hoc scenario parameters: invented drift rates, invented survival curves, invented noise floors. This revision is organized to make that dependence explicit and then remove it where observations allow. The paper has three layers. Layer 1 is a synthetic parameter-space experiment that treats source drift, usability, misidentification, geometry, storage precision, estimator, and chirality as controlled variables and maps the recoverability surface and its failure boundaries — a theory of where reconstruction works. Layer 2 maps real observed celestial source populations into that same parameter space: Gaia DR3 bright stars with measured five/six-parameter astrometry [gaiadr3, lindegren2021gaiaedr3], ATNF pulsars with measured timing and kinematics [manchester2005atnf, hobbs2005pulsarpm], and ICRF3 sources with VLBI positions, defining-source geometry, and literature-constrained stability [charlot2020icrf3, charlot1990structure, titov2011aberration]. The reconstruction task is then re-run on networks built from the observed populations, and each synthetic conclusion is explicitly classified as confirmed, partially confirmed, reversed, or not testable under the calibrated models. Layer 3 separates the horizons: 10^3–10^5 yr is the observation-anchored regime, 10^6 yr is an extended physically constrained projection, and 10^7–10^8 yr are extrapolative stress tests, never calibrated forecasts.

Only after this quantitative framework is in place do we introduce the secondary conceptual term *prospective archaeoastronomy*: the design of celestial reference encodings intended to remain decodable by a future observer whose own sky differs from ours. We introduce the term as a framing device, not as an established field, and the engineering results stand independently of it.

## 2. Materials and methods

### 2.1 Problem formulation

Let L_Earth(t0) be Earth's spin angular-momentum vector at the reference epoch and N0 = L_Earth(t0)/||L_Earth(t0)|| the terrestrial north direction. For a set of n reference sources with unit direction vectors q_i, we write Q = [q_1^T; ...; q_n^T]. Given the observed source directions Q_obs at the recovery epoch and stored relational information derived from Q at the reference epoch, the reconstruction problem is to estimate n_hat minimizing the discrepancy between stored and observed relations subject to ||n_hat|| = 1. The primary outcome is the angular error eps_theta = arccos(n_hat^T N0) and the success probability P(eps_theta < 1 deg). The two layers below share this formulation; they differ only in how source populations, motions, and usability are generated.

### 2.2 Relational orientation encoding

The encoding stores, per source, the cosine b_i = q_i^T N0 of its angle to north, i.e. b = Q N0. Source–source relations are captured by the Gram matrix G = Q Q^T with G_ij = cos(theta_ij); sparse relational graphs store only a subset of edges. Chirality constraints are stored as a sparse subset of signed triple products H_ijk = sign(det(q_i, q_j, q_k)). Given Q_obs and the stored b, the core solve is n_hat = argmin_{||n||=1} ||Q_obs n - b||^2. Relational encodings based on angular information determine the configuration only up to an orthogonal transformation; when det(O) = -1 the recovered frame is mirrored and north is reflected across an unknown plane. When a stored chirality subset exists, sign disagreement of surviving triple products flags the mirror and the candidate is reflected back; without it the mirror ambiguity is unresolved.

### 2.3 Synthetic parameter-space experiment

Layer 1 is a controlled experiment in the parameter space P(recover | drift, loss, mismatch, geometry, precision, estimator, chirality). Seven architecture classes span minimal to redundant designs (Table 1): M1 single stellar landmark; M2 stellar triangle; M3 multi-star networks (n = 1,3,10,20,50,100); M4 pulsar networks (n = 10,20,50); M5 quasar/ICRF-like networks (n = 10,20,50,100); M6 galaxy/cluster networks (n = 10,20,50); M7 heterogeneous hybrids. One additional benchmark, M1b, is evaluated separately: a direct-axis landmark in which the source direction itself encodes the axis (N0 = q1 at encode time) and the future-observed direction is decoded directly with no relational scalar — a Polaris-like "this object points north" scheme that separates the algebraic underdetermination of the M1 relational encoding from the physical fragility of a single landmark. Synthetic populations are sampled isotropically on the sphere unless a geometry scenario (clustered, banded, D-optimally selected) specifies otherwise; all configuration is driven by configs/default.yaml (Table 2).

In the synthetic layer, source *usability* is a Weibull survival curve S_k(t) = exp(-(t/tau_k)^a_k) per source class with characteristic times 3e5 yr (stars), 3e6 yr (pulsars), 3e8 yr (quasars), 1e8 yr (galaxies/clusters) and severity multipliers 0.3/1/3, and surviving directions receive class-specific tangent-plane drift at 5e-7, 1e-7, 1e-9, 2e-9 rad/yr. These are declared scenario parameters of the theory layer, deliberately swept so the response surface and its failure boundaries can be measured; they are not used in the calibrated layer, whose motion and usability models are defined in Sections 2.8 and 2.9. Misidentification is modeled primarily as correspondence permutation; wrong-catalogue substitution and isotropic injection are secondary models. The mirror-ambiguity prior is 0.5 (a stored handedness bit resolves it when present); the RANSAC estimator uses a 2 deg cosine-domain inlier tolerance with 120 minimal-subset iterations. The information cost B(S) combines source-ID cost (40 bits/source), relational-value cost (8–64 bits/value), chirality cost, and a fixed 128-bit record, and Pareto-efficient designs are identified as nondominated (bits, P(eps<1 deg)) points. Each replication samples a fresh population, a random true N0, encodes it, applies degradation/drift/noise/mismatch, reconstructs, applies the mirror rule, and records diagnostics (Figure 1), with a fixed master seed; negative controls NC1 (random b) and NC2 (fully permuted correspondence) verify that success is information-driven.

### 2.4 Observational source catalogues

Layer 2 uses three published catalogues (Table 3). Gaia DR3 [gaiadr3, lindegren2021gaiaedr3] provides stellar positions, parallaxes, proper motions, radial velocities, and astrometric quality metrics. The ATNF Pulsar Catalogue [manchester2005atnf] provides pulsar positions, periods, period derivatives, characteristic ages, distances, and proper motions where measured. ICRF3 [charlot2020icrf3] provides VLBI positions of extragalactic reference sources with defining-source flags and session counts. Every acquisition is recorded in data/acquisition_ledger.csv with the exact query or source URL, UTC acquisition time, file size, SHA-256 checksum, and licence note; raw snapshots are immutable and all processing is re-run by make all with no live-API dependency.

### 2.5 Gaia stellar calibration

The Gaia subset is a sky-tiling bright-star sample: the 24 contiguous NESTED-healpix source_id ranges that partition the DR3 sky were each queried for the 100 brightest sources satisfying G < 12 mag, parallax > 0.1 mas, non-null proper motions, ruwe < 1.4, and visibility_periods_used > 8, yielding {{cal_n_gaia}} stars after deduplication. All calibrated rows carry measured proper motions and parallax; radial velocity is missing for a fraction {{miss_gaia_radial_velocity_kms}} and is never imputed — propagation falls back to angular-linear motion for those rows (Section 2.8). The measured total proper-motion distribution has median {{cal_star_med_pm}} mas/yr and 90th percentile {{cal_star_p90_pm}} mas/yr. Acquisition metadata, cuts, and checksums are in Table 3 and the ledger; the epoch is Gaia DR3's reference epoch J2016.0 and all angular rates are in mas/yr.

### 2.6 ATNF pulsar calibration

The ATNF snapshot contains {{cal_n_atnf}} pulsars. Measured total proper motion (PMTOT) is available for only {{cal_n_atnf_pm_meas}} of them (missing fraction {{miss_atnf_pm_tot_masyr}}); measured values have median {{cal_psr_med_pm}} mas/yr and 90th percentile {{cal_psr_p90_pm}} mas/yr. No proper motions are fabricated: pulsar networks are built from the measured-PM subset, and a sensitivity branch (S1, Section 2.14) re-draws missing PMs from the empirical CDF of measured values to bound the selection effect. Characteristic age is available for all but a fraction {{miss_atnf_age_yr}} (median {{cal_psr_median_age}} yr); it is used as a proxy timescale in the usability model of Section 2.9 and is explicitly not treated as exact remaining lifetime. Period derivatives are missing for a fraction {{miss_atnf_p1_ss}} and are not used where absent.

### 2.7 ICRF3 extragalactic calibration

The ICRF3 K-band source list contributes {{cal_n_icrf3}} extragalactic sources, of which {{cal_n_icrf3_defining}} carry the defining-source flag [charlot2020icrf3]. Their observed sky distribution is used verbatim — it is anisotropic, reflecting the VLBI observing network and defining-source selection, and calibrated networks inherit that geometry rather than an isotropic assumption. ICRF3 provides no apparent-motion field, so extragalactic positional stability is a literature-constrained prior: apparent source motion (from source structure and centroid wander [charlot1990structure] and frame-level systematics such as secular aberration [titov2011aberration]) is drawn log-uniformly over 10^-3–10^-1 mas/yr per source per replication, with factor-ten sensitivity runs in both directions (S4, Section 2.14). Provenance is recorded in the calibration registry; defining-flag membership is retained as an observable covariate.

### 2.8 Source-motion propagation

Stars: each Gaia row's measured proper motion is propagated either angular-linearly (direction moves along the local tangent at the measured PM rate) or in 3D Cartesian constant-velocity form using distance 1/parallax and measured radial velocity where present; the two are compared directly as a propagation check. Pulsars: measured PMTOT rates propagate angular-linearly; rows without measured PMTOT appear only in the S1 sensitivity model. Quasars/ICRF3: per-source apparent drift is drawn from the log-uniform 10^-3–10^-1 mas/yr prior each replication. Galaxies/clusters are demoted to the synthetic layer only: no defensible observational calibration of their structure-dominated apparent motion exists in these catalogues, so they appear in no primary calibrated scenario.

### 2.9 Source-usability modeling

Usability is decomposed as usable = exists AND identifiable AND observable AND sufficiently stable for matching. *Exists*: stars are assigned survival probability exp(-t/tau_s) with tau_s = 5e9 yr (range 5e8–2e10 in S2) reflecting main-sequence finite lifetime; pulsars exp(-t/(k x median characteristic age)) with k = 1 (range 0.3–3 in S3), an order-of-magnitude beaming/luminosity proxy — a true 10^6-yr pulsar survival probability is not estimable from catalogue data and is therefore bracketed, not asserted; extragalactic sources are assigned existence probability 1 over the modelled horizons — current existence is observed, but continued persistence is not: it is a conditional assumption classified sensitivity-only in Table 4, and all far-horizon quasar results are conditional on source persistence and the specified apparent-motion model. *Identifiable* and *observable* are the measured-astrometry and quality-cut membership of each catalogue row plus a per-scenario mismatch probability. Every calibrated parameter is classified observed, derived, literature-constrained, extrapolated, or sensitivity-only in results/calibration/calibration_parameter_classification.csv (Table 4); no parameter is silently fixed.

### 2.10 Network construction and optimization

Calibrated networks are built two ways: random subsets of each observed population (the default) and D-optimally selected subsets that greedily maximize log det(Q^T Q) over the candidate pool [fedorov1972] when the pool is at least four times the target size — the same objective used in the synthetic geometry scenarios, here applied to real sky positions. Equal-count comparisons pair, for example, a 50-source quasar network against a 50-source hybrid (20 stars + 10 pulsars + 20 quasars), so class-composition effects are separated from size effects. The calibrated grid covers star networks (n = 10, 50, 100), pulsar networks (10, 50), quasar networks (10, 50, 100), a 10+10+10 star/pulsar/quasar hybrid, and the equal-count 50-source hybrid, each random and optimized.

### 2.11 Reconstruction algorithms

Three estimators are compared: ordinary least squares with renormalization (LS); iteratively reweighted Huber regression (c = 1.345) [huber1964robust]; and a RANSAC-like consensus estimator that solves minimal 3-source systems and refits on the largest inlier set [fischler1981ransac]. The mirror rule of Section 2.2 is applied after estimation. Stored source–source edges additionally act as an identity check — a source whose observed pairwise cosines contradict most of its surviving stored edges is dropped before estimation.

### 2.12 Observation-calibrated validation

The primary calibrated analysis runs all networks of Section 2.10 at observation-anchored horizons 10^3, 10^4, 10^5 yr under baseline observational noise sigma_obs = 1e-4 rad and p_mismatch = 0.05, with N_MC = 2000 replications per scenario and a fixed master seed. Calibrated scenarios are name-prefixed C_ and run alongside matched synthetic scenarios (prefix S_) identical in size and estimator so theory–calibration differences are attributable to the population/motion/usability models alone. Estimator sweeps (LS/Huber/RANSAC at p_mismatch in {0, 0.2, 0.5}) and a precision check (8- vs 32-bit storage) are repeated on the calibrated hybrid and quasar networks. Wilson 95% intervals accompany all success proportions [wilson1927].

### 2.13 Extended physically constrained projection

The 10^6 yr runs reuse the identical calibrated machinery on a longer horizon. They remain informed by observed populations and physical propagation, but the uncertainty is larger and validation indirect: measured proper motions and the pulsar existence proxy are stretched well beyond the timescales on which they were estimated. Results at 10^6 yr are therefore reported separately in Section 3.8 as an extended projection, not grouped with the observation-anchored regime.

### 2.14 Extrapolative stress testing

The same calibrated networks are additionally run at 10^7 and 10^8 yr. These runs share the calibrated motion models but extend the existence model far beyond any observational constraint; they are reported separately in Section 3.9 as stress tests bounding where the framework — not the sky — remains viable, and are never presented as calibrated forecasts.

### 2.15 Sensitivity analysis

Six pre-declared sensitivity branches isolate the remaining non-empirical parameters and data choices: S1 re-draws missing pulsar proper motions from the empirical measured-PM CDF; S2 varies the stellar existence timescale over 5e8–2e10 yr; S3 varies the pulsar existence multiplier over k in {0.3, 3}; S4 rescales the quasar apparent-motion prior by x0.1 and x10; S5 restricts the Gaia pool to a stricter astrometric-quality subset (ruwe <= 1.1, visibility_periods_used >= 10); S6 restricts the ICRF3 pool to defining sources only. Each branch varies exactly one assumption so that residual arbitrariness is bounded rather than hidden.

### 2.16 Reproducibility

All computations use NumPy/SciPy [harris2020numpy]. make all re-runs catalogue processing, both simulation layers, calibration summaries, figures, tables, value interpolation, and the DOCX build from a clean checkout; the master seed is fixed in configs/default.yaml; raw catalogue snapshots and checksums live in data/; per-figure/table scripts record which results files they consume. Each Monte Carlo replication records source availability, corruption state, information cost, reconstruction error, estimator diagnostics, and chirality status; the complete machine-readable schema, result-file inventory, and acquisition artefacts are documented in REPRODUCIBILITY.md in the repository. Model verification and validation — unit/identity tests, known-truth recovery, catalogue geometry reproduction, empirical distribution checks, propagation comparison, and quality-cut sensitivity — follow the V&V categories of Sargent [sargent2013verification] and are compiled in qc/MODEL_VALIDATION_REPORT.md.

## 3. Results

### 3.1 General synthetic response surface

With no noise, loss, or mismatch, all estimators recovered N0 to numerical precision (machine-level residuals; unit tests) — the encoding is sufficient. A single stellar landmark storing only the source–north relational scalar (M1) produced a valid solution in essentially no replication (invalid-solution probability {{single_star_p_invalid_mean}}): one scalar constrains the recovered north only to a cone. The direct-axis control M1b produced valid solutions while its landmark survived (P(eps<1 deg) = {{m1b_p1_t1e+03}} at 10^3 yr, {{m1b_p1_t1e+04}} at 10^4 yr) but was capped near 0.5 because it stores no handedness, then collapsed under drift and loss ({{m1b_p1_t1e+05}} at 10^5 yr; invalid fraction {{m1b_p_invalid_t1e+06}} at 10^6 yr). Under the baseline synthetic scenario (Table 5, Figure 2) the 50-source quasar network reached P = {{quasars50_p1_t1e+07}} at 10^7 yr versus {{stars50_p1_t1e+07}} for the equal star network, and redundancy saturated: P rose from {{quasar_10_p1_t1e4}} (n = 10) to {{quasar_50_p1_t1e4}} (50) and {{quasar_100_p1_t1e4}} (100) at 10^4 yr (Figures 3 and 4).

### 3.2 Synthetic failure boundaries

The synthetic layer maps where recoverability fails in parameter space. Estimators: at t = 10^6 yr on the hybrid, LS/Huber/RANSAC achieved P(eps<1 deg) = {{hybrid_ls_pm0.0}}/{{hybrid_huber_pm0.0}}/{{hybrid_ransac_pm0.0}} with clean correspondences; at p_mismatch = 0.5: {{hybrid_ls_pm0.5}}/{{hybrid_huber_pm0.5}}/{{hybrid_ransac_pm0.5}} — robust estimators dominate under corruption. Chirality: with it stored, the mirror was wrong in {{chir_on_pmirror_wrong}} of replications versus {{chir_off_pmirror_wrong}} without, raising P at 10^7 yr from {{chir_off_p1}} to {{chir_on_p1}}. Geometry: clustered and banded populations degraded conditioning and measurably reduced P relative to isotropic or D-optimal selection (Figure 5). Information cost: the bit-reliability frontier was flat across 8–64 bits at long horizons but 8-bit storage measurably degraded short-horizon decode (median error {{prec_bchir_8b_median_err}}deg vs {{prec_bchir_32b_median_err}}deg at 32 bits on quasar-50 at 10^4 yr), and stored edges rescued substitution-type misidentification (P {{edge_bchir_substitution_p1}} -> {{edge_knnchir_substitution_p1}} at p_mismatch = 0.5, t = 10^7 yr) but not permutation (Figure 6). Composition: the best synthetic allocation at 10^7 yr was {{best_alloc_t1e+07}} (P = {{best_alloc_p1_t1e+07}}) — homogeneous quasars — and the severity x mismatch heatmap (Figure 7) shows failure concentrated at pessimistic degradation with p_mismatch >= 0.3 (worst cell P = {{hybrid_p1_t1e7_worst}}). The estimator comparison, chirality on/off, and negative-control outcomes are summarized in Table 6.

### 3.3 Observed source-population characteristics

The three catalogues contribute complementary observed populations (Table 3). Figure 8 shows their actual sky geometry: the Gaia sample is sky-tiled by construction; ATNF pulsars concentrate toward the Galactic plane; ICRF3 sources cover the sky anisotropically, reflecting the VLBI observing network, and {{cal_n_icrf3_defining}} carry defining-source flags. Measured proper motions (Figure 9) span {{cal_star_med_pm}} mas/yr median (90th percentile {{cal_star_p90_pm}}) for stars and {{cal_psr_med_pm}} mas/yr median ({{cal_psr_p90_pm}}) for the {{cal_n_atnf_pm_meas}} pulsars with measured PMTOT — real distributions far from the flat synthetic drift constants. Missingness is reported in full: radial velocity is absent for {{miss_gaia_radial_velocity_kms}} of stars, PMTOT for {{miss_atnf_pm_tot_masyr}} and characteristic age for {{miss_atnf_age_yr}} of pulsars, and no missing field is imputed in the primary analysis.

### 3.4 Empirical calibration of motion/stability

source_motion_calibration.csv summarizes the three motion models: observed Gaia PM distribution (median {{cal_star_med_pm}} mas/yr), observed ATNF PMTOT subset (median {{cal_psr_med_pm}} mas/yr, n = {{cal_n_atnf_pm_meas}}), and the log-uniform 10^-3–10^-1 mas/yr quasar apparent-motion prior. Table 7 contrasts each synthetic assumption with its calibrated replacement or classification. The propagation check (Figure 10) compares angular-linear and 3D-Cartesian constant-velocity propagation of the Gaia sample: median angular displacement is identical to within {{prop_diff_deg_t1e+03}} deg at 10^3 yr, diverging to {{prop_diff_deg_t1e+05}} deg at 10^5 yr and {{prop_diff_deg_t1e+06}} deg at 10^6 yr as radial motion accumulates — a small, quantified model error for the primary horizons. Every calibrated parameter is registered with its class (observed/derived/literature-constrained/extrapolated/sensitivity-only) in Table 4.

### 3.5 Observation-calibrated network performance

Table 8 and Figure 11 give the calibrated results. In the observation-anchored regime the ordering is already set: at 10^5 yr the 50-source quasar network achieved P(eps<1 deg) = {{c_quasar50_p1_t1e+05}} and the 50-source star network {{c_star50_p1_t1e+05}}. At the extended 10^6 yr projection the 50-source quasar network achieved P(eps<1 deg) = {{c_quasar50_p1_t1e+06}} (median error {{c_quasar50_med_t1e+06}} deg), the 50-source star network {{c_star50_p1_t1e+06}}, the 50-source pulsar network {{c_pulsar50_p1_t1e+06}}, and the equal-count hybrid {{c_hybrid50_p1_t1e+06}}. Matched synthetic scenarios give {{s_quasar50_p1_t1e+06}}, {{s_star50_p1_t1e+06}}, {{s_pulsar50_p1_t1e+06}}, and {{s_hybrid_spq_p1_t1e+06}} respectively — the calibration gap is itself a result: it measures how far the declared synthetic scenario parameters sat from the observed populations. Calibrated estimator behaviour mirrored the synthetic layer: at 10^6 yr and p_mismatch = 0.5, LS/Huber/RANSAC achieved {{cest_ls_pm0.5_t1e+06}}/{{cest_huber_pm0.5_t1e+06}}/{{cest_ransac_pm0.5_t1e+06}}, and 8- versus 32-bit storage on quasar-50 at 10^4 yr gave P = {{cprec_q50_8b_t1e+04}} versus {{cprec_q50_32b_t1e+04}} (medians {{cprec_q50_8b_med_t1e+04}}deg vs {{cprec_q50_32b_med_t1e+04}}deg).

### 3.6 Random versus optimized observed-source networks

Figure 12 pairs random and D-optimal selections of the same observed populations. At 10^5 yr the optimized quasar network reached {{c_quasar50_opt_p1_t1e+05}} versus {{c_quasar50_p1_t1e+05}} random; the optimized star network {{c_star50_opt_p1_t1e+05}} versus {{c_star50_p1_t1e+05}}; the optimized pulsar network {{c_pulsar50_opt_p1_t1e+05}} versus {{c_pulsar50_p1_t1e+05}}. Geometric optimization on real sky distributions retains the synthetic-layer prediction that conditioning matters, while its size is bounded by the anisotropy actually present in the catalogues.

### 3.7 Theory versus calibrated results

Table 9 and Figure 13 classify the eight pre-declared synthetic conclusions under observation-based calibration: (A) redundancy improves recoverability — {{tvc_a}}; (B) geometry matters — {{tvc_b}}; (C) chirality removes mirror ambiguity — {{tvc_c}} (a property of the encoding itself, unchanged by population); (D) robust estimators tolerate misidentification — {{tvc_d}}; (E) finite precision binds in precision-limited regimes — {{tvc_e}}; (F) heterogeneity is not automatically beneficial — {{tvc_f}}, with the equal-count hybrid trailing the equal-count quasar network ({{c_hybrid50_p1_t1e+06}} vs {{c_quasar50_p1_t1e+06}} at 10^6 yr); (G) quasar dominance at long horizons — {{tvc_g}}; (H) single-source fragility — {{tvc_h}}. Sensitivity runs bound the residual non-empirical parameters: S1 (pulsar missing-PM resample) changed pulsar-50 performance to {{sens1_pulsar50_missingpm_resampled_p1_t1e+06}} at 10^6 yr; S2 (stellar tau over 5e8–2e10 yr) gave {{sens2_star50_tau5e+08_p1_t1e+06}}–{{sens2_star50_tau2e+10_p1_t1e+06}}; S3 (pulsar k over 0.3–3) {{sens3_pulsar50_k0p3_p1_t1e+06}}–{{sens3_pulsar50_k3p0_p1_t1e+06}}; S4 (quasar prior x0.1/x10) {{sens4_quasar50_driftx0p1_p1_t1e+07}}–{{sens4_quasar50_driftx10p0_p1_t1e+07}} at 10^7 yr. No calibrated conclusion is forced; the classification is computed from the output tables, not asserted.

### 3.8 Extended 10^6 yr projection

At 10^6 yr, beyond the observation-anchored regime but still inside physically constrained propagation, the 50-source quasar network achieved P(eps<1 deg) = {{c_quasar50_p1_t1e+06}} (median error {{c_quasar50_med_t1e+06}} deg), the equal-count hybrid {{c_hybrid50_p1_t1e+06}}, the 50-source pulsar network {{c_pulsar50_p1_t1e+06}}, and the 50-source star network {{c_star50_p1_t1e+06}}. These values carry the extended-projection caveat of Section 2.13: they are informed by observations but validated only indirectly.

### 3.9 Extrapolative 10^7–10^8 yr stress tests

At extrapolative horizons the calibrated motion models still apply but existence modelling dominates. The 50-quasar network achieved {{c_quasar50_p1_t1e+07}} at 10^7 yr and {{c_quasar50_p1_t1e+08}} at 10^8 yr; the equal-count hybrid {{c_hybrid50_p1_t1e+07}} and {{c_hybrid50_p1_t1e+08}}; star networks collapse to {{c_star50_p1_t1e+07}} at 10^7 yr under any tau_s in the sensitivity range. These numbers are stress tests of the framework, not calibrated forecasts: no empirical constraint on 10^7–10^8 yr source survival exists, and that limitation is stated rather than smoothed over (Figure 14).

### 3.10 Robustness / negative controls

Negative controls NC1 (random stored cosines) and NC2 (fully permuted correspondence) achieved P(eps<1 deg) = {{nc1_p1}} and {{nc2_p1}} — reconstruction success is information-driven, not estimator artifact. Quality-cut sensitivity (ruwe < 1.4, visibility > 8) enters the calibrated populations only through measured fields; the S1–S6 grid (Section 3.7) reports each remaining assumption's leverage. The additional data-choice branches behaved as designed: restricting the Gaia pool to the stricter astrometric subset (S5) left star-50 performance within {{sens5_star50_strict_p1_t1e+05}}–{{sens5_star50_strict_p1_t1e+06}} over the anchored-to-extended horizons, and restricting ICRF3 to defining sources only (S6) left the quasar-50 network at {{sens6_quasar50_defining_p1_t1e+06}}–{{sens6_quasar50_defining_p1_t1e+08}} on the primary conclusions.

## 4. Discussion

### 4.1 What the results do and do not show

The three-layer design separates what the framework claims from what any scenario assumes. Layer 1 shows recoverability is governed by redundancy, geometry, chirality, estimator robustness, and precision only in bounded regimes — a map of the parameter space. Layer 2 shows where observed source populations sit in that map: real Gaia, ATNF, and ICRF3 populations reproduce the architecture-level ordering predicted synthetically, and each synthetic conclusion is re-verdicted against calibrated evidence in Section 3.7. The three-horizon taxonomy — observation-anchored, extended projection, extrapolative stress test — is applied consistently rather than labelling all long horizons as validated. The remaining non-empirical parameters — stellar existence timescale, pulsar existence multiplier, quasar apparent-motion prior — are classified, bracketed by sensitivity runs, and confined to specific conclusions rather than spread silently through every number.

### 4.2 Design implications for long-lived reference systems

For astronautical information systems with extreme lifetimes, the calibrated results argue for (i) allocation weighted toward empirically stable source classes — ICRF3-type extragalactic sources — with heterogeneity added only where it contributes complementary failure resilience, since the equal-count hybrid trailed the equal-count quasar network; (ii) redundancy sized from the failure-side knee of the frontier; (iii) explicit chirality storage, cheap and removing a discrete catastrophic failure mode; and (iv) robust estimators on the decode side. These are the same architectural instincts behind ICRF/Gaia frame construction [arias1995icrs, mignard2018gaiacrf2, charlot2020icrf3], quantified here for a decode-after-loss problem with observed populations rather than assumed ones.

### 4.3 Relation to pulsar maps and interstellar communication

The Pioneer/Voyager pulsar maps [drake1972message, sagan1978murmurs] encode position relationally; this work supplies the missing error analysis — how many sources, of which classes, with what redundancy, under what corruption — now grounded in the real measured properties of the source populations involved, including measured pulsar proper motions [hobbs2005pulsarpm] and extragalactic frame stability [titov2011aberration]. The same formalism applies wherever an orientation must survive channel degradation, including long-lived messages to unknown receivers [cocconi1959searching]. We name the associated design discipline "prospective archaeoastronomy": engineering reference encodings that remain decodable rather than permanent.

### 4.4 Failure regimes and limitations

Dominant failure modes: insufficient surviving sources (n < 3); clustered/banded geometry wrecking conditioning; correspondence corruption beyond robust-estimator breakdown (~0.3–0.5 depending on redundancy); catastrophic star-only designs at long horizons from cumulative stellar motion — now a measured distribution rather than an assumed rate. Real limitations remain: pulsar proper motions are measured for only {{cal_n_atnf_pm_meas}} sources (a distance/observability selection the S1 branch brackets); characteristic age is not a lifetime; the quasar apparent-motion prior is literature-constrained, not catalogue-measured; existence probabilities beyond ~10^6 yr are extrapolation; and no credible galaxy/cluster calibration exists, so that class stays out of the calibrated comparison. Observational noise is modeled isotropically; correlated systematics would be a useful extension.

## 5. Conclusions

A general simulation framework for deep-time orientation recoverability has been defined and, in this revision, calibrated against observed celestial source populations. Theory defines the recoverability landscape — redundancy, geometry, chirality, estimator robustness, and bounded precision regimes; observations determine where real Gaia, ATNF, and ICRF3 source populations lie in that landscape; validation determines which theoretical conclusions survive contact with astrophysical reality. Of the eight pre-declared synthetic conclusions, the architecture-level predictions — redundancy, geometry, chirality, robust estimation, single-source fragility — survive calibration; quasar dominance and finite-precision relevance are qualified rather than absolute; and heterogeneity is again not automatically beneficial, confirmed by equal-count observed-population comparisons. The observation-anchored regime (10^3–10^5 yr) is separated from the extended 10^6 yr projection and the extrapolative stress tests (10^7–10^8 yr), every remaining non-empirical parameter is classified and sensitivity-bounded, and the full pipeline regenerates from a clean public checkout.

## Declarations

- Competing interests: The authors declare no known competing financial or personal interests.
- Funding: This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors.
- CRediT author contributions: Tatsuki Onishi: Conceptualization, Methodology, Software, Formal analysis, Writing — original draft, Writing — review & editing, Supervision.
- Data availability: all simulation outputs, per-replication records, acquisition scripts, catalogue snapshots (where redistribution is permitted), checksums, query manifests, the calibration registry, missingness reports, extended sensitivity outputs, QC documentation, and reproduction instructions are available in the public repository accompanying this article, https://github.com/bougtoir/prospective-archaeoastronomy (see REPRODUCIBILITY.md). Gaia DR3, ATNF, and ICRF3 data are publicly available from their respective archives; acquisition queries and checksums are recorded in the repository.
- Generative AI: during preparation the authors used Devin (Cognition AI) for code generation and drafting support; all content was reviewed and verified by the authors, who take full responsibility.

## Figure captions

Figure 1. Pipeline schematic: present orientation -> relational encoding -> deep-time degradation -> future observations -> robust reconstruction -> recovered orientation.

Figure 2. Synthetic-layer response surface: P(eps_theta < 1 deg) versus log10(t/yr) for architectures M1–M7 under baseline scenario.

Figure 3. Synthetic redundancy: P(eps_theta < 1 deg) versus number of reference sources for homogeneous star and quasar networks at t = 10^4 yr; Wilson 95% intervals.

Figure 4. Synthetic median angular error versus source count at t = 10^4 yr.

Figure 5. Source-geometry conditioning (isotropic, clustered, banded, D-optimal) versus reconstruction performance at t = 10^5 yr.

Figure 6. Information cost versus reconstruction reliability; encodings and numeric precisions at t = 10^7 yr.

Figure 7. Synthetic robustness heatmap: misidentification probability x degradation severity for the hybrid network at t = 10^7 yr.

Figure 8. Observed sky geometry (Aitoff): Gaia DR3 bright subset, ATNF pulsars, and ICRF3 sources as used in calibrated networks.

Figure 9. Observed motion/stability distributions by source class: measured Gaia and ATNF proper motions and the literature-constrained quasar apparent-motion prior.

Figure 10. Propagation check: median angular displacement of the Gaia sample under angular-linear versus 3D-Cartesian constant-velocity propagation, 10^3–10^6 yr.

Figure 11. Calibrated performance: P(eps_theta < 1 deg) versus horizon for observed-population networks; the observation-anchored regime (10^3–10^5 yr) and the extended 10^6 yr projection are marked separately; matched synthetic scenarios dashed.

Figure 12. Random versus D-optimally selected observed-source networks at 10^5 yr.

Figure 13. Theory versus calibration: calibrated and matched synthetic P(eps_theta < 1 deg) curves; shaded region marks the extrapolative regime.

Figure 14. Extrapolative stress tests at 10^7–10^8 yr for calibrated networks — not calibrated forecasts.

## Table captions

Table 1. Reference-network architectures evaluated (M1–M7) with per-class source counts.

Table 2. Simulation and scenario parameters; all values set in configs/default.yaml. Synthetic drift and usability parameters are declared scenario assumptions of the theory layer.

Table 3. Observational data sources: catalogue, acquisition query/snapshot, cuts, epoch, units, missingness summary, citation, acquisition date, checksum.

Table 4. Calibration parameter classification: every calibrated parameter recorded as observed, derived, literature-constrained, extrapolated, or sensitivity-only, with source, derivation script, uncertainty, and manuscript usage.

Table 5. Synthetic-layer primary outcome P(eps_theta < 1 deg) by architecture and time horizon (core scenarios, N_MC = 10 000).

Table 6. Synthetic-layer sensitivity and falsification summary: estimator comparison, chirality on/off, negative controls.

Table 7. Synthetic versus calibrated assumptions: each theory-layer assumption and the observation-calibrated quantity or classification that replaces it.

Table 8. Observation-calibrated results: P(eps_theta < 1 deg) by observed-population network and horizon (10^3–10^5 yr anchored; 10^6 yr extended projection; N_MC = 2000).

Table 9. Theory versus calibrated findings: pre-declared synthetic conclusions A–H classified CONFIRMED / PARTIALLY CONFIRMED / NOT CONFIRMED / REVERSED / NOT TESTABLE under observation-based calibration.
