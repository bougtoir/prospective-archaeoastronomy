FINAL POST-MERGE QC — prospective-archaeoastronomy
=================================================
Date: 2026-09-24 UTC
Scope: post-#497 validation + submission preparation per user directive.

1. MERGED STATE VERIFIED
------------------------
- Canonical merged commit: 7cbaed7450690a8bdaf39154596230b96ed34b06
  ("Merge pull request #497"), containing the corrected E6 storage-precision
  quantization and stored-edge decoder logic (c19d32d3) plus sync-map
  update (abea0ad5).
- `git status` clean; zero uncommitted/unintended changes at checkout.
- Follow-up review fixes went on branch
  `devin/1790240102-proarch-e6b-edgecheck` (commits b1bf5152, cd341dd4,
  eb1436cc + regen commit), per post-merge convention — master itself
  untouched.

2. TESTS RUN
------------
- `pytest tests/` — 12/12 pass (10 prior + 2 new regression tests:
  `test_edge_check_drops_injected_sources`,
  `test_edge_check_all_drop_fails_not_fakes`).
- `qc_audit.py` — PASS, 0 issues (numeric citations, placeholders,
  reference coverage, figure/table citations all verified against the
  corrected build).

3. CLEAN-BUILD RESULT
---------------------
- `make all` executed from the merged state + review-fix commits:
  test → simulate (E1–E10 + E6b + E6c) → summarize → figures → tables →
  manuscript_values → build_manuscript → qc_audit. Completed with no
  failures; qc PASS 0 issues.

4. E6 RERUN STATUS
------------------
- E6 regenerated: 96 000 reps (4 encodings × 4 precisions × 3 archs ×
  2000), identical seed stream (per-experiment offset +100000 from
  master_seed 20260924). Stored cosines and edge weights are quantized
  to the declared `bits` (uniform, 2^bits−1 levels, [−1,1]) BEFORE
  decode — nominal bit counts now correspond to actual precision.
- NEW experiment E6b (added post-merge): knn vs b_only ×
  {permutation, substitution, injection} × 3 archs at p_mismatch = 0.5,
  t = 1e7 yr, 36 000 reps → results/e6b_edgebenefit.csv.
- NEW experiment E6c (added post-merge): b_chir/knn_chir × {8,32} bits ×
  {M5_quasars_50, M7_hybrid_all} at t = 1e4 yr, 16 000 reps →
  results/e6c_precision.csv.

5. CORRECTED 8-BIT RESULT
-------------------------
- At t = 1e7 yr (E6) the precision axis is flat: 8–64 bits differ within
  Monte-Carlo noise because secular drift dominates the error budget.
- At t = 1e4 yr (E6c, precision-limited regime) 8-bit storage measurably
  degrades decode exactly as the manuscript claims: quasar-50 median
  error 0.0406° (8 bit) vs 0.0016° (32 bit) — ~25×.
- Manuscript §3.7 wording updated to report both facts (flat axis at
  1e7; degradation at 1e4) instead of the blanket claim.

6. STORED-EDGE DECODER VALIDATION
---------------------------------
- Edges ARE used: pre-estimation check drops any source whose observed
  pairwise cosines disagree with >50% of its surviving stored edges
  (tol = 3·(σ_i+σ_j) + 4/levels).
- Three Devin-Review flags on #497 fixed in this branch:
  (a) injected rows (no stored correspondence) now dropped — previously
      escaped with degree 0;
  (b) all-rows-flagged case now yields an empty observation set →
      `insufficient_sources` failure instead of a baseless solution;
  (c) E6 could not measure the edge effect (permutation-only grid) →
      E6b added.
- Measured effect (M5_quasars_50, p_mismatch=0.5, t=1e7):
  substitution 0.8135 → 0.8350 (helps, detects wrong sources);
  injection 1.0 → 1.0 (accuracy unchanged — RANSAC already rejects
  injected outliers; injected rows are nonetheless now excluded);
  permutation 0.9955 → 0.9965 (cannot detect — corrupts b only; stated
  as a limitation in manuscript §3.7 and code comment).

7. CHIRALITY-EQUIVALENCE VALIDATION
-----------------------------------
- Preserved implementation; it is NOT a defect. The chirality check runs
  `check_chirality(Q_obs, triples)` on the observed frame and uses
  `frac = f` when unmirrored, `frac = 1−f` when mirrored. Because a
  reflection negates the sign of every triple product,
  `agree(R·Q_obs) = 1 − agree(Q_obs)`, so `frac` is identically the
  agreement of the UNMIRRORED interpretation on both branches. The
  decision `frac < 0.5` and the reflect-or-not actions are equivalent to
  computing the check on the reflected frame directly.
- Empirical validation on the current code (2000 reps, quasar-50,
  t=1e3, mirror_ambiguity=True): chirality on → 0 mirror_wrong, 100%
  correct decisions; chirality off → mirror_wrong 0.49, P(<1°) ≈ 0.52,
  matching the coin-flip theory. Both directions confirmed.

8. ALL REGENERATED ARTIFACTS
----------------------------
- results/e1..e10 + e6b_edgebenefit + e6c_precision (raw) and
  results/summary_*.csv
- figures/fig1..fig7 (renumbered to citation order) +
  manuscript/graphical_abstract.png
- tables/table1–table4.csv
- manuscript/values.json (77 placeholder values)
- manuscript/build/manuscript_final.md + .docx + reference_map.json
- manuscript/highlights.md, cover_letter.md (contain no generated point
  values — qualitative claims only, verified)
- qc/numerical_traceability.csv (every placeholder → value → generator),
  qc/qc_report.md

9. NUMERICAL TRACEABILITY / CONSISTENCY / REFERENCE / ACTA AUDITS
---------------------------------------------------------------
- Traceability: all 77 placeholders resolve from regenerated summaries
  (qc_audit PASS). New keys (edge_*, prec_*) included.
- Figure/table audit: Figures 1–7 now cited in order of first mention
  (Fig1 added to §2.6; numbering remapped old4→2, old2→3, old3→4,
  old7→5, old6→6, old5→7); Tables 1–4 cited in order; abstract,
  Results, Discussion, tables and figures report identical numbers
  (single source: values.json).
- Reference audit: 18 references, Vancouver numbered in order of
  appearance; all verified real (qc/reference_audit.csv).
- Acta compliance: ACTA_ASTRONAUTICA_GUIDE_AUDIT.md covers structure,
  highlights ≤85 chars, graphical abstract, declarations (author
  placeholders flagged `[author to complete]`).

10. HOSTILE INTERNAL-REVIEWER AUDIT OUTCOMES
------------------------------------------
- nominal-bit-only claims → RESOLVED: quantization reaches the decoder;
  §3.7 now reports the actual measured behavior.
- described-but-unused edge info → RESOLVED: edges used for
  misidentification checking; §3.7 states where they help and where they
  cannot.
- mismatch robustness overclaim → RESOLVED: §3.7 numbers limited to the
  tested models; permutation stated as undetectable.
- code/wording mismatches → fixed §3.7 (injection no longer claimed as
  improved — it is unchanged; text says why).
- deep-time overclaiming → audited: usability/drift are declared
  scenario assumptions (§2.x); Discussion lists limits; no astrophysical
  predictability asserted.
- Figure-citation-order defect → FIXED (see §9).

11. PUBLIC REPOSITORY SYNC
--------------------------
- bougtoir/prospective-archaeoastronomy created and populated by the
  sync-to-repos workflow (verified by clone): contains the corrected
  canonical pipeline — quantization, edge check incl. injection-drop and
  all-drop handling, E6b/E6c code, updated §3.7.
- Scheduled sync had not fired; triggered it via push-trigger entries
  added for the two proarch branches in
  .github/workflows/sync-to-repos.yml.

12. CHANGES TO MANUSCRIPT CONCLUSIONS
-------------------------------------
- None structural. Two wording corrections in §3.7: (i) 8-bit claim now
  supported by E6c at t=1e4 and the flat 1e7 axis is stated; (ii) edge
  benefits reported model-by-model (helps substitution, neutral under
  injection, impossible under permutation) instead of a generic claim.
  Headline results (H1–H6 verdicts, P values) unchanged.

13. UNRESOLVED LIMITATIONS
--------------------------
- Permutation-type correspondence corruption remains geometrically
  undetectable (declared in text).
- Usability/drift parameters are declared scenario assumptions, not
  fitted astrophysics (declared).
- Author placeholders remain in Declarations (affiliation, funding,
  CRediT) — flagged for the author.
- Injection edge-check benefit is not visible in accuracy at tested
  parameters because RANSAC already rejects such outliers (honest
  result, reported as such).

14. SUBMISSION-READY FILE LIST
------------------------------
- manuscript/build/manuscript_final.docx (primary submission file) and
  manuscript_final.md
- manuscript/highlights.md (Acta format, ≤85 chars)
- manuscript/graphical_abstract.png
- manuscript/cover_letter.md
- manuscript/declarations.md
- manuscript/supplementary.md
- manuscript/references.bib (18 verified refs)
- figures/fig1_architecture.png, fig2_p_vs_time.png,
  fig3_redundancy.png, fig4_error_vs_n.png, fig5_geometry.png,
  fig6_pareto.png, fig7_heatmap.png (separate files per journal rule)
- tables/table1–table4.csv
- qc/ evidence pack + reproducibility_report.md
- results/ raw + summary CSVs; data/ catalogue snapshots + ledger;
  Makefile (`make all`); tests/; handoffs/PHASE_00..20 + FINAL_HANDOFF

STATUS: submission-ready pending only author-side Declarations fields.
