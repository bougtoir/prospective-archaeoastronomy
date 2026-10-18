# Internal Reviewer Pass — Acta Astronautica submission

Reviewer-style critique of the manuscript package (applied before final checks).

## 1. Framing
- Lead is astronautics: celestial reference systems, orientation encoding, decode-after-loss. Archaeology terminology confined to a labeled secondary term. OK.

## 2. Likely reviewer objections and responses
- "Weibull usability parameters are assumed, not fitted." — Declared as scenario assumptions (Methods 2.4); sensitivity grid (severity x p_mismatch, Fig 5, E3) maps dependence on the assumption. Acceptable for a feasibility/sensitivity study but reviewers may push for astrophysical justification — kept explicitly as scenario language throughout.
- "Drift rates are stylized." — Same treatment: scenario values spanning orders of magnitude per class; results reported as regimes, not point predictions.
- "Monte Carlo counts modest." — n_mc=2000 peripheral / 10000 core; Wilson 95% CIs reported beside every headline rate.
- "Encoding is low-bandwidth (single cosines)." — Acknowledged; augmentation variants (kNN relations, chirality triples, precision bits) evaluated in E6 with explicit bit cost.
- "Single-star failure trivial." — That is the point: it is the negative baseline satisfying the predeclared acceptance criterion.

## 3. Claim-language audit
- Headline claims use "statistically reconstructable under the specified scenarios" phrasing; no claim that orientation can be physically "preserved".
- No claim that any real future observer exists or will decode the encoding.
- Hypotheses H1–H6 each answered by a named experiment; conclusions restate only measured outcomes.

## 4. Completeness checks (pre-build)
- Every figure/table cited in text (enforced by qc_audit.py).
- Every reported number traces to results/*.csv via values.json (no hard-coded results).
- References limited to verifiable entries; unverifiable candidates removed (qc/reference_audit.csv).
- Negative controls NC1/NC2 show solutions are information-dependent.

## 5. Remaining reviewer-visible limitations (stated in Discussion)
- Synthetic pipeline; catalogue integration reported separately as descriptive context.
- Usability/drift parameters are scenario assumptions, not measured.
- No relativistic / galactocentric-frame effects modeled beyond secular drift rates.
