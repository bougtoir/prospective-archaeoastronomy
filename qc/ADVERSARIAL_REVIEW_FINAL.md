# Adversarial (Hostile) Review — ASR submission

Reviewer posture: skeptical Methods/Systems reviewer for Advances in Space Research, instructed to find reasons to reject.

## A. Positioning / scope
- A1: "Prospective archaeoastronomy" reads as speculative SETI-adjacent framing. RESOLVED: abstract/introduction lead with celestial reference systems, astrometry, ICRF/Gaia practice, pulsar navigation; the term is introduced only after the engineering framework and explicitly labeled a framing device. Title is reference-network oriented.
- A2: Results are synthetic-scenario claims. ACCEPTED AS LIMITATION: text states conclusions are conditional on declared scenarios; usability/drift are scenario assumptions, not measurements (Table 2 caption says so).

## B. Statistics and methodology
- B1: Success proportions reported without intervals in headline text -> Wilson 95% intervals are computed (wilson1927 cited; intervals in figures/tables). PASS.
- B2: arccos domain: clipping applied in estimators (verified in code: np.clip to [-1,1]). PASS.
- B3: RANSAC thresholds, Huber c=1.345, chirality handling, mismatch permutation vs substitution vs injection are implemented and separately ablated (e2_estimators, e6b_edgebenefit). PASS.
- B4: Condition numbers kappa(Q^T Q) reported in geometry experiment (e5_geometry). PASS.
- B5: Quantization is decode-side only — encode stores full precision; matches claim. PASS.
- B6: Seeds fixed (master seed in configs/default.yaml); MC replications counted per scenario; reproducible via make all. PASS.
- B7: H2 unsupported -> honestly reported as a negative finding. PASS.

## C. Document integrity (the defect that caused the Acta desk rejection)
- C1: Equations must be Word-native. 117 OMML oMath objects; zero LaTeX/$/ASCII-math in visible text; every page visually inspected post-render. PASS.
- C2: "*"-formatting: zero literal asterisks in docx. PASS.
- C3: Manual wrapping: none. PASS.

## D. References
- D1: DEFECT FOUND — ATNF catalogue DOI pointed to unrelated paper. FIXED (10.1086/428488) + regression test.
- D2: All other DOIs verified (Crossref/doi.org). PASS.

## E. Citation order
- E1: DEFECT FOUND — Figure 4 cited before Figure 3. FIXED; order now sequential. PASS.

## F. Reproducibility
- F1: make all re-runs full pipeline; public-repo clean-clone verification logged in FINAL_PUBLIC_END_TO_END_REPRODUCIBILITY_AUDIT.md.
- F2: Downloaded catalogue data persisted under data/raw with acquisition ledger (incl. Crossref verification responses from this audit).

## Remaining known limitations (disclosed in paper)
- Scenario-conditional results; usability curves are assumptions; no correlated systematics; no real-source drift covariances; real-catalogue layer is supplementary.
