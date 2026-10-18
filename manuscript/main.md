# Deep-Time Celestial Reference Networks for Reconstructing Terrestrial Orientation

Tatsuki Onishi (corresponding author), Data Science and AI Innovation Research Promotion Center, Shiga University, 1-1-1 Bamba, Hikone, Shiga 522-8522, Japan. E-mail: bougtoir@gmail.com. ORCID: 0000-0001-7261-9062.

## Abstract

Terrestrial orientation is not permanently tied to any single celestial landmark: stars drift, pulsars fade from the beam line, and any individual reference source can be lost or misidentified over timescales far shorter than the horizons relevant to the longest-lived information systems. This paper formulates the recovery of a stored Earth spin-axis direction as a celestial reference-network reconstruction problem and evaluates it quantitatively over horizons of 10^3–10^8 yr. The orientation is encoded relationally as the cosines between the stored north vector and each member of a redundant reference-source network, optionally augmented by sparse source–source angular relations and chirality (signed-triple-product) constraints. Monte Carlo simulation evaluates seven architecture classes — single stellar landmarks, stellar triangles, multi-star, pulsar, quasar (ICRF-like), galaxy/cluster, and heterogeneous hybrid networks — under source loss, source misidentification, observational noise, class-specific secular drift, and unfavorable source geometry, using least-squares, Huber, and RANSAC-like robust reconstruction. Under the baseline scenario, a 50-source quasar network achieved P(error < 1 deg) = {{quasars50_p1_t1e+07}} at 10^7 yr, while the tested heterogeneous hybrid achieved {{hybrid_p1_t1e+07}}; a single landmark carrying only a source–north relational scalar failed to produce a valid solution in essentially all replications (invalid-solution fraction {{single_star_p_invalid_mean}}). Long-horizon performance was governed more strongly by the assumed stability and usability of the included source classes than by heterogeneity itself — homogeneous quasar networks outperformed the tested heterogeneous designs at the longest horizons — while RANSAC-like reconstruction remained reliable at misidentification fractions where least squares collapsed, and negative controls confirmed that reconstructed solutions are information-dependent rather than artifacts of the estimator. We identify robust and failure regimes and derive an information-cost–reliability frontier; the framework is a candidate secondary discipline we term "prospective archaeoastronomy", i.e. the design of celestial reference systems intended to remain decodable rather than permanent.

## Keywords

celestial reference systems; robust estimation; deep space navigation; redundancy; Monte Carlo methods; information theory

## 1. Introduction

Celestial landmarks are time-dependent. The "North Star" role has passed between stars on millennial timescales, and over 10^5–10^8 yr essentially every stellar source drifts far from its catalogue position. Modern astronautics already relies on reference *systems* rather than single objects: the International Celestial Reference System is realized by ensembles of quasars [arias1995icrs, charlot2020icrf3], Gaia maintains a kinematically non-rotating optical frame from hundreds of thousands of extragalactic sources [mignard2018gaiacrf2, lindegren2018gaiadr2], and spacecraft attitude determination fuses many stellar measurements rather than trusting any single star [spratling2009starid]. Pulsar-based navigation and timing extend the same logic to a second source class [downs1974pulsar, sheikh2006xnav, becker2013pulsarnav].

Encoding terrestrial orientation for recovery after 10^3–10^8 yr is therefore an extreme reference-system robustness problem, not a search for a future North Star. The engineering question is which *network* of sources, encoded with what relational information, leaves the original direction statistically reconstructable despite source loss, secular motion, misidentification, and finite measurement precision. The Pioneer plaque and Voyager pulsar map are early instances of exactly this encoding idea — terrestrial position was expressed relative to a pulsar network rather than to any single object [drake1972message, fedorov1972, sagan1978murmurs] — but they were never analysed as a quantitative reconstruction problem with quantified failure regimes.

The missing piece in the reference-system literature is an explicit treatment of *deep-time* orientation recovery under coupled degradation channels: source loss, source misidentification, observational noise, class-specific secular drift, mirror (chirality) ambiguity, and information-storage cost. This paper supplies that treatment. We formulate the reconstruction problem (Section 2), define seven reference architecture classes (M1–M7) and their encodings, and evaluate them in Monte Carlo simulation across six time horizons (10^3–10^8 yr) with predeclared scenario assumptions. Our hypotheses, tested in Section 3, are that (H1) redundant networks outperform minimal systems; (H2) heterogeneous source networks outperform equal-size homogeneous networks under class-specific degradation; (H3) geometrically well-distributed networks improve reconstruction; (H4) robust estimators outperform ordinary least squares under corrupted correspondences; (H5) chirality information reduces mirror/sign ambiguity; and (H6) redundancy exhibits diminishing returns, producing an information–reliability frontier.

Only after this quantitative framework is in place do we introduce the secondary conceptual term *prospective archaeoastronomy*: the design of celestial reference encodings intended to remain decodable by a future observer whose own sky differs from ours. We introduce the term as a framing device, not as an established field, and the engineering results stand independently of it.

## 2. Materials and methods

### 2.1 Problem formulation

Let L_Earth(t0) be Earth's spin angular-momentum vector at the reference epoch and N0 = L_Earth(t0)/||L_Earth(t0)|| the terrestrial north direction. For a set of n reference sources with unit direction vectors q_i, we write Q = [q_1^T; ...; q_n^T]. The encoding stores, per source, the cosine b_i = q_i^T N0 of its angle to north, i.e. b = Q N0. Source–source relations are captured by the Gram matrix G = Q Q^T with G_ij = cos(theta_ij); sparse relational graphs store only a subset of edges. Chirality constraints are stored as a sparse subset of signed triple products H_ijk = sign(det(q_i, q_j, q_k)).

Given the observed source directions Q_obs at the recovery epoch and the stored b, the reconstruction problem is n_hat = argmin_{||n||=1} ||Q_obs n - b||^2. The primary outcome is the angular error eps_theta = arccos(n_hat^T N0) and the success probability P(eps_theta < 1 deg).

### 2.2 Architectures and source populations

Seven architecture classes were evaluated (Table 1): M1 single stellar landmark; M2 stellar triangle; M3 multi-star networks (n = 1,3,10,20,50,100); M4 pulsar networks (n = 10,20,50); M5 quasar/ICRF-like networks (n = 10,20,50,100); M6 galaxy/cluster networks (n = 10,20,50); M7 heterogeneous hybrids (10 pulsars + 10 quasars; 10+10+10 star/pulsar/quasar; 5+5+10+10 star/pulsar/quasar/galaxy). One additional benchmark, M1b, is evaluated separately (§3.1): a direct-axis landmark in which the source direction itself encodes the axis (N0 = q1 at encode time) and the future-observed direction is decoded directly with no relational scalar — a Polaris-like "this object points north" scheme included to separate the algebraic underdetermination of the M1 relational encoding from the physical fragility of a single landmark. M1b intentionally stores only the landmark direction and no independent sign/chirality bit; its roughly 0.5 success ceiling therefore reflects the benchmark definition rather than a fundamental impossibility of all direct-axis landmark schemes. An augmented direct-axis scheme carrying an external sign/chirality marker could remove this specific ambiguity, but would still retain the single-source fragility to loss, drift, and misidentification quantified below. Synthetic populations are sampled isotropically on the sphere unless a geometry scenario (clustered, banded, D-optimally selected) specifies otherwise; all configuration is driven by `configs/default.yaml` (Table 2).

### 2.3 Degradation, noise, and misidentification

Source *usability* — a scenario probability combining physical survival, identifiability, observability, and reference usability — is modeled as a Weibull survival curve S_k(t) = exp(-(t/tau_k)^a_k) per source class, with characteristic times tau_k = 3e5 yr (stars), 3e6 yr (pulsars), 3e8 yr (quasars), 1e8 yr (galaxies/clusters) and severity multipliers 0.3/1/3 for pessimistic/baseline/optimistic scenarios. These are declared scenario assumptions, not fitted astrophysical survival functions; the ranking encodes that stars disperse kinematically and have finite lifetimes while extragalactic positions are quasi-fixed on these horizons. In addition, each surviving source direction receives a class-specific secular drift drawn as a tangent-plane Gaussian with rate 5e-7 rad/yr (stars), 1e-7 rad/yr (pulsars), 1e-9 rad/yr (quasars), and 2e-9 rad/yr (galaxies/clusters), modeling unpredictable proper-motion accumulation; an isotropic observational error sigma_obs is added on top.

Misidentification is modeled primarily as correspondence permutation: a fraction p_mismatch of surviving sources retain a stored cosine belonging to a different source. Wrong-catalogue substitution and isotropic injection are implemented as secondary models. Observational noise sweeps sigma_obs over 0–1e-2 rad.

### 2.4 Estimators and mirror ambiguity

Three estimators are compared: ordinary least squares with renormalization (LS); iteratively reweighted Huber regression (c = 1.345) [huber1964robust]; and a RANSAC-like consensus estimator that solves minimal 3-source systems and refits on the largest inlier set [fischler1981ransac]. Relational encodings based on angular information determine the configuration only up to an orthogonal transformation; when det(O) = -1 the recovered frame is mirrored and north is reflected across an unknown plane. When a stored chirality subset exists, sign disagreement of surviving triple products flags the mirror and the candidate is reflected back; without it, the mirror ambiguity is unresolved and is resolved by chance. Chirality-on versus chirality-off designs are compared directly.

### 2.5 Information cost and optimization

The information cost B(S) = source-ID cost (40 bits/source, a Gaia-scale index) + relational-value cost (b_i and stored edge weights at 8/16/32/64 bits each) + chirality cost + a fixed 128-bit metadata record. Pareto-efficient designs are identified as nondominated points in (bits, P(eps<1 deg), mean error). Class composition is optimized by grid search over allocations of n_total in {20,30,50} across four source classes at 1e6, 1e7, 1e8 yr.

### 2.6 Monte Carlo design, outcomes, controls

Each replication samples a fresh population, a random true N0, encodes it, applies degradation/drift/noise/mismatch, reconstructs with the chosen estimator, applies the mirror rule, and records diagnostics (Figure 1; results schema in code). Default N_MC = 2000 replications per scenario and 10 000 for headline scenarios, with a fixed master seed (Table 2). Success proportions are reported with Wilson 95% confidence intervals [wilson1927]. Negative controls: NC1 stores cosines unrelated to N0 (random b); NC2 uses fully randomized correspondence (p_mismatch = 1). All computations use NumPy/SciPy [harris2020numpy]; the complete pipeline is regenerated by `make all`.

### 2.7 Real-catalogue integration

Where network access permits, the pipeline downloads ICRF3 K-band positions [charlot2020icrf3], the ATNF Pulsar Catalogue [manchester2005atnf], and a Gaia DR3 bright-star subset [gaiadr3] into a common schema (source_id, class, ra, dec, optional kinematics); raw snapshots and checksums are logged in `data/acquisition_ledger.csv`. Catalogue-derived results are reported separately from synthetic results. When catalogues are unavailable the study is entirely synthetic and this is stated explicitly.

## 3. Results

### 3.1 Encoding is sufficient and minimal systems fail

With no noise, loss, or mismatch, all estimators recovered N0 to numerical precision (machine-level residuals; unit tests). A single stellar landmark storing only the source–north relational scalar (M1) produced a valid solution in essentially no replication (invalid-solution probability {{single_star_p_invalid_mean}}): one scalar constrains the recovered north only to a cone, so a single generic reference source carrying only the proposed relational scalar is insufficient for unique 3-D reconstruction. This underdetermination is a property of the relational encoding, not of every conceivable single-landmark scheme. The direct-axis control M1b — where the landmark direction itself defines the axis — produced valid solutions while the landmark survived (P(eps<1 deg) = {{m1b_p1_t1e+03}} at 10^3 yr and {{m1b_p1_t1e+04}} at 10^4 yr), but success was capped near 0.5 because this benchmark stores no handedness information — the unresolved mirror ambiguity is decided by chance under the benchmark definition (an augmented scheme with an independent sign/chirality bit could lift exactly this ceiling; the fragility results below would not change); performance then collapsed under drift and loss ({{m1b_p1_t1e+05}} at 10^5 yr; invalid-solution fraction {{m1b_p_invalid_t1e+06}} at 10^6 yr), and catalogue substitution corrupted the decoded direction unbuffered (P = {{m1b_subst_p1_t1e+04}} at 10^4 yr, p_mismatch = 0.5). M1b thus demonstrates that algebraic identifiability alone is not the limiting issue for a minimal design — single-point fault tolerance is. This supports H1's necessity claim at the minimal end.

### 3.2 Architectures vs time horizon

Table 3 and Figure 2 give P(eps_theta < 1 deg) for each architecture over 10^3–10^8 yr under baseline degradation, sigma_obs = 1e-4 rad, and p_mismatch = 0.05. At 10^7 yr the quasar network (n = 50) achieved P = {{quasars50_p1_t1e+07}}, the hybrid M7 achieved {{hybrid_p1_t1e+07}}, and the star-only network achieved {{stars50_p1_t1e+07}}; at 10^8 yr the quasar network retained {{quasars50_p1_t1e8_e1}}. Median errors track success probabilities (Figures 2 and 4).

### 3.3 Redundancy and diminishing returns

Figures 3 and 4 show reconstruction quality vs source count for homogeneous star and quasar nets at t = 10^4 yr: P(eps<1 deg) rises from {{quasar_10_p1_t1e4}} (n = 10 quasars) to {{quasar_50_p1_t1e4}} (n = 50) and {{quasar_100_p1_t1e4}} (n = 100), with clear saturation — supporting H1 and H6.

### 3.4 Estimators under corrupted correspondences

At t = 10^6 yr on the hybrid architecture, LS/Huber/RANSAC achieved P(eps<1 deg) = {{hybrid_ls_pm0.0}}/{{hybrid_huber_pm0.0}}/{{hybrid_ransac_pm0.0}} with clean correspondences; at p_mismatch = 0.2: {{hybrid_ls_pm0.2}}/{{hybrid_huber_pm0.2}}/{{hybrid_ransac_pm0.2}}; at 0.5: {{hybrid_ls_pm0.5}}/{{hybrid_huber_pm0.5}}/{{hybrid_ransac_pm0.5}} (Table 4). Robust estimators dominate under mismatch (H4), with RANSAC-like consensus the most resilient.

### 3.5 Chirality

With chirality stored, the mirror ambiguity was resolved in every replication (wrong-mirror fraction {{chir_on_pmirror_wrong}} vs {{chir_off_pmirror_wrong}} without, i.e. a coin-flip), raising P(eps<1 deg) at t = 10^7 yr on the hybrid architecture from {{chir_off_p1}} to {{chir_on_p1}} (H5 supported). Chirality storage therefore removes a discrete catastrophic failure mode — a solution consistent with the data but reflected — at negligible information cost.

### 3.6 Geometry

Figure 5 compares isotropic, clustered, banded, and D-optimally selected 50-source networks at t = 10^5 yr. Clustered and banded geometries degrade conditioning (large kappa(Q^T Q), low log det) and measurably reduce P(eps<1 deg); D-optimal selection recovers most of the loss relative to isotropic sampling (H3 supported; Table 4).

### 3.7 Information cost and Pareto frontier

Figure 6 shows the bit-cost/reliability trade-off at t = 10^7 yr across encodings (cosines only; +sparse kNN edges; +chirality; both) and numeric precisions (8–64 bits/value). Chirality adds little storage and the largest reliability gain. At this horizon the precision axis is flat — secular drift dominates the error budget, so moving between 8 and 64 bits changes results negligibly; storage precision only binds in precision-limited short-horizon regimes, where 8-bit storage does measurably degrade decode accuracy (quasar-50 at t = 10^4 yr: median error {{prec_bchir_8b_median_err}}° at 8 bits vs {{prec_bchir_32b_median_err}}° at 32 bits). Nondominated designs are reported rather than a single optimum. Stored edges additionally act as an identity check — a source whose observed pairwise cosines contradict most of its surviving stored edges is dropped before estimation. With chirality stored in both conditions (isolating the edges contribution), at p_mismatch = 0.5 and t = 10^7 yr this raises P(<1°) from {{edge_bchir_substitution_p1}} to {{edge_knnchir_substitution_p1}} under catalogue substitution; under isotropic injection accuracy is unchanged ({{edge_bchir_injection_p1}} → {{edge_knnchir_injection_p1}}) because the consensus estimator already rejects injected outliers; and under correspondence permutation — which corrupts only the stored cosines and is geometrically undetectable — edges cannot help ({{edge_bchir_permutation_p1}} vs {{edge_knnchir_permutation_p1}}).

### 3.8 Optimal class composition

Grid search over n_total in {20,30,50} allocations across four classes found the best baseline-scenario composition at 10^7 yr to be {{best_alloc_t1e+07}} (P(eps<1 deg) = {{best_alloc_p1_t1e+07}}) — a homogeneous quasar allocation with no stars or pulsars. Consistently, the best tested heterogeneous hybrid ({{hybrid_p1_t1e+07}} at 10^7 yr) trailed the homogeneous 50-quasar network ({{quasars50_p1_t1e+07}}), and at 10^8 yr the ordering was {{quasars50_p1_t1e8_e1}} vs {{hybrid_p1_t1e+08}}. H2 is therefore not supported under the baseline scenario: diversity per se is not deep-time robustness, and long-horizon composition is governed by the assumed class-specific stability, usability, and geometry rather than by heterogeneity itself.

### 3.9 Negative controls

NC1 (random b) and NC2 (fully permuted correspondence) achieved P(eps<1 deg) = {{nc1_p1}} and {{nc2_p1}}, i.e. ~0 as required — reconstruction success is driven by stored information, not estimator artifact.

### 3.10 Robustness/failure regimes

The severity x mismatch heatmap (Figure 7) shows the hybrid network tolerating baseline degradation with p_mismatch up to ~0.2, and failing under pessimistic degradation combined with p_mismatch >= 0.3–0.5 (P = {{hybrid_p1_t1e7_worst}}). Noise sweep results (sigma_obs) identify the precision floor.

## 4. Discussion

### 4.1 What the results do and do not show

The simulations show that relational encodings of terrestrial orientation remain *statistically reconstructable* over 10^3–10^8 yr under declared degradation, misidentification, and noise scenarios when the network is redundant, geometrically distributed, and chirality-constrained. They do not show that any real sky will preserve any particular marker, nor do the usability curves measure real source survival — they are scenario parameters swept across pessimistic-to-optimistic ranges. All conclusions are conditional on those scenarios.

The M1b comparison should be read narrowly: it shows that a direct-axis landmark storing *only* the source direction is algebraically valid yet fragile, and that its ~0.5 success ceiling is a consequence of storing no handedness/sign information — not a fundamental limit of direct-axis schemes. An augmented direct-axis encoding carrying an independent sign/chirality bit could remove exactly that ambiguity term; what it could not remove is the single-source fragility to loss, drift, and misidentification measured in §3.1. M1b therefore demonstrates that algebraic identifiability alone is not the limiting issue for minimal designs — single-point fault tolerance is.

### 4.2 Design implications for long-lived reference systems

For astronautical information systems with extreme lifetimes — interstellar probe reference frames, long-duration archives, deep-space beacons — the results argue for (i) source-class allocation weighted toward the assumed most stable and longest-usable classes — under baseline assumptions, quasi-fixed extragalactic sources — with heterogeneity added only where it contributes complementary failure resilience; (ii) redundancy well beyond the algebraic minimum, sized from the failure-side knee of the Pareto frontier rather than nominal performance; (iii) explicit chirality storage, which is cheap and removes a discrete catastrophic failure mode; and (iv) robust estimators on the decode side, which cost nothing at encode time. These are the same architectural instincts behind ICRF/Gaia frame construction, quantified here for a decode-after-loss problem rather than a maintain-the-frame problem [arias1995icrs, mignard2018gaiacrf2, charlot2020icrf3].

### 4.3 Relation to pulsar maps and interstellar communication

The Pioneer/Voyager pulsar maps [drake1972message, sagan1978murmurs] encode position relationally; this work supplies the missing error analysis — how many sources, of which classes, with what redundancy, under what corruption. The same formalism applies wherever an orientation must survive channel degradation, including long-lived messages to unknown receivers [cocconi1959searching]. We name the associated design discipline "prospective archaeoastronomy": engineering reference encodings that remain decodable rather than permanent. The term is a compact label for the problem studied here, not a claim of an existing field.

### 4.4 Failure regimes and limitations

Dominant failure modes: (i) insufficient surviving sources (n < 3); (ii) clustered/banded geometry wrecking conditioning; (iii) correspondence corruption beyond robust-estimator breakdown (~0.3–0.5 depending on redundancy); (iv) catastrophic star-only designs at long horizons from secular drift. Stellar drift rates, usability time constants, and the 0.5 mirror prior are scenario choices; sensitivity grids (Figures 5–7) bound their influence. Observational noise was modeled as isotropic tangent-plane error; correlated systematic errors would be a useful extension. Real-catalogue subsets (Section 2.7) are an enhancement layer; the core claims rest on the declared synthetic scenarios.

## 5. Conclusions

Historical terrestrial orientation remained statistically reconstructable under specified degradation, misidentification, and observational scenarios when encoded as redundant, geometrically distributed, chirality-constrained relations to a celestial source network dominated by long-stable classes. Deep-time recoverability depended on redundant encoding, robust decoding, geometric conditioning, chirality control, and the assumed long-term stability/usability of the chosen source classes — not on heterogeneity per se. A single relational scalar is underdetermined, and even a direct-axis landmark scheme — algebraically valid while its source survives, and improvable only in its mirror-ambiguity term by an additional sign bit — still fails under loss and drift: fault tolerance requires redundancy. The achievable regime is bounded by an information-cost–reliability frontier that system designers can traverse. The framework transfers to any long-duration reference-architecture problem in which the decoding environment is partially out of the encoder's control.

## Declarations

- Competing interests: The authors declare no known competing financial or personal interests.
- Funding: This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors.
- CRediT author contributions: Tatsuki Onishi: Conceptualization, Methodology, Software, Formal analysis, Writing — original draft, Writing — review & editing, Supervision.
- Data availability: simulation outputs, code, and (where fetched) catalogue snapshots with checksums are available in the public repository accompanying this article, https://github.com/bougtoir/prospective-archaeoastronomy.
- Generative AI: during preparation the authors used Devin (Cognition AI) for code generation and drafting support; all content was reviewed and verified by the authors, who take full responsibility.

## Figure captions

Figure 1. Pipeline schematic: present orientation -> relational encoding -> deep-time degradation -> future observations -> robust reconstruction -> recovered orientation.

Figure 2. P(eps_theta < 1 deg) versus log10(t/yr) for architectures M1–M7 under baseline scenario.

Figure 3. P(eps_theta < 1 deg) versus number of reference sources for homogeneous star and quasar networks at t = 10^4 yr; Wilson 95% intervals.

Figure 4. Median angular error versus source count at t = 10^4 yr.

Figure 5. Source-geometry conditioning (isotropic, clustered, banded, D-optimal) versus reconstruction performance at t = 10^5 yr.

Figure 6. Information cost versus reconstruction reliability; encodings and numeric precisions at t = 10^7 yr.

Figure 7. Robustness heatmap: misidentification probability x degradation severity for the hybrid network at t = 10^7 yr.

## Table captions

Table 1. Reference-network architectures evaluated (M1–M7) with per-class source counts.

Table 2. Simulation and scenario parameters; all values set in configs/default.yaml. Drift and usability parameters are scenario assumptions, not measurements.

Table 3. Primary outcome P(eps_theta < 1 deg) by architecture and time horizon (core scenarios, N_MC = 10 000).

Table 4. Sensitivity and falsification summary: estimator comparison, chirality on/off, negative controls.
