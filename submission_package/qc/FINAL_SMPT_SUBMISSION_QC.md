# FINAL SMPT SUBMISSION QC — Observation-Calibrated Celestial Reference
# Networks for Long-Horizon Orientation Reconstruction

All gates PASS (re-run on the regenerated targeted-pass package).

| gate | artefact | result |
|---|---|---|
| initial manuscript review | built manuscript_final.md | PASS |
| scientific freeze / dependency audit | this pass: no sim rerun; downstream only | PASS |
| hard-coded numbers | HARDCODE_AUDIT.md / NUMERIC_PROVENANCE_AUDIT.csv | PASS |
| reference bibliographic audit | FINAL_REFERENCE_AND_CITATION_AUDIT.md (Manchester fixed) | PASS 23/23 |
| semantic citation audit | SEMANTIC_CITATION_AUDIT.md | PASS 23/23 |
| figure/table content identity | FINAL_FIGURE_TABLE_CONTENT_IDENTITY_AUDIT.md | PASS — fig/table filenames = captions = content |
| text/figure/table numeric consistency | FINAL_TEXT_FIGURE_TABLE_CONSISTENCY_AUDIT.md | PASS |
| formatting asterisks | ASTERISK_FORMATTING_AUDIT.md | PASS 0 |
| manual wrapping | LINE_WRAP_AUDIT.md | PASS 0 |
| OMML native | OMML_STRUCTURAL_AUDIT.md | PASS 154 objects, 0 residue |
| visual render (every page) | FINAL_VISUAL_RENDER_AUDIT.md | PASS 17 pp |
| highlights format | HIGHLIGHTS_LENGTH_AUDIT.md | PASS 5 bullets, max 75 chars |
| model validation | MODEL_VALIDATION_REPORT.md | PASS items 1-11 (resampling wording corrected) |
| supplement removal | SUPPLEMENT_REMOVAL_AUDIT.md | PASS — Supplementary material: NONE |
| ASR criticism answered | ASR_CRITICISM_RESPONSE_AUDIT.md | yes (quasar persistence reclassified) |
| hostile review | SMPT_HOSTILE_REVIEW.md / SMPT_FINAL_DECISION.md | PASS |
| pytest | tests/ | 16 passed |
| qc_audit.py | package + manuscript cross-check | PASS 0 issues |

## STOP CONDITIONS (targeted pass)

[x] Figures 10-14 file/content/caption numbering fixed
[x] Tables 3-6 file/content/caption numbering fixed
[x] Manchester 2005 bibliographic metadata fixed (AJ 129(4) 1993-2006)
[x] Fedorov citation moved to D-optimal Methods context
[x] semantic citation audit PASS
[x] highlights 3-5 bullets, each <=85 chars
[x] quasar persistence reclassified observed -> sensitivity-only
[x] held-out/out-of-sample wording corrected
[x] stale S1-S4 supplementary references removed
[x] supplementary material eliminated (NONE)
[x] synthetic assumptions visible in main text (2.3 + Table 2)
[x] theory-vs-calibration results visible in main text (3.7 + Table 9)
[x] 10^9-yr exploratory mention removed
[x] Data/Code Availability points to repository artefacts
[x] no frozen science rerun without dependency reason
[x] hardcode audit PASS / refs bibliographic PASS / refs semantic PASS
[x] figure/table content identity PASS / numeric consistency PASS
[x] OMML PASS / LaTeX residue 0 / asterisks 0 / hard wraps 0 / tracked
    changes+comments 0
[x] regenerated DOCX full visual audit PASS
[x] final package regenerated and directly audited
[x] scientific canonical commit recorded (qc/CANONICAL_FREEZE.md)
[x] public clean-clone reproduction PASS at previous canonical
    f1dd191bb3; for this text/package-only pass, simulation inputs are
    unchanged (configs, src/proarch, data snapshots untouched), and the
    clean-clone check for the new canonical commit is repeated on the
    public tip after merge (see FINAL_PUBLIC_END_TO_END_REPRODUCIBILITY_AUDIT.md)

## FINISHING PASS (post-package targeted QC/provenance pass)

Gates re-verified on the regenerated finishing-pass package. No frozen
science was rerun: all changes are labels, journal metadata, audit wording,
provenance bookkeeping, and package assembly.

[x] scientific vs package canonical commit distinction resolved
    (scientific = f1dd191bb3, full clean-clone make all verified;
     package commit = post-pass tip; tree diff shows no scientific
     dependency changed — see qc/CANONICAL_FREEZE.md)
[x] reproducibility statement points to the correct scientific state
[x] final PDF actual page count derived from file: 17 pages
[x] every page (17/17) of that exact final PDF visually inspected — PASS
[x] Figure 13 legend no longer labels simulated performance "(observed)";
    labels now "observation-calibrated star/pulsar/quasar50" and
    "synthetic star/pulsar/quasar50"; curves/numbers unchanged (same
    frozen CSV inputs, deterministic regeneration)
[x] SMPT guide audit uses JCR quartile as primary basis: JIF 4.6,
    JCR Q1 in COMPUTER SCIENCE, SOFTWARE ENGINEERING and Q2 in
    COMPUTER SCIENCE, INTERDISCIPLINARY APPLICATIONS (both stated);
    SJR/CiteScore listed secondarily only
[x] stale held-out/out-of-sample wording swept from manuscript and
    submission-facing docs
[x] Supplement absent (verified in regenerated ZIP manifest)
[x] Figure 10-14 identity mapping PASS
[x] Table 3-6 identity mapping PASS
[x] Manchester metadata PASS (AJ 129(4) 1993-2006, DOI 10.1086/428488)
[x] Fedorov semantic placement PASS (D-optimal Methods)
[x] highlights 5 bullets, max 75 chars
[x] quasar persistence classification PASS (sensitivity-only/conditional)
[x] S1-S6 wording PASS
[x] 10^9-yr mention absent
[x] semantic citation audit PASS 23/23
[x] figure/table content-identity audit PASS
[x] OMML structural audit PASS; LaTeX residue 0
[x] tracked changes/comments 0
[x] final visual render audit PASS (17 pp)
[x] final submission QC PASS
[x] final ZIP extracted and contents directly audited
