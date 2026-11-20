# Supplement-removal audit — SMPT targeted pass

Action: `manuscript/supplementary.md` deleted; removed from
`make_submission_package.py` FLAT_FILES. The submission package contains
NO supplementary file.

## Disposition of former supplement content

| Former section | Disposition |
|---|---|
| S1 encoding/output schema | concise sentence added to §2.16 Reproducibility; full schema moved to `REPRODUCIBILITY.md` |
| S2 extended sensitivity/file inventory | moved to `REPRODUCIBILITY.md` with corrected S1–S6 branch names |
| S3 catalogue acquisition/calibration artefacts | scientific essentials already in Methods 2.4–2.8 and Table 3; operational details (queries, hashes, manifests) in `REPRODUCIBILITY.md`; Data Availability points to the repository |
| S4 synthetic-layer scenario assumptions | already visible in main text §2.3 + Table 2; extended to state mirror-ambiguity prior 0.5 and RANSAC tolerance/iterations explicitly |
| S5 theory-vs-calibration status | remains in main manuscript (§3.7, Table 9, Figure 13); CSV recorded in `REPRODUCIBILITY.md` |
| S6 exploratory 10^9 yr | removed; no 10^9-yr mention remains in any submission-facing file |

## Stale-reference sweep

Searched manuscript, cover letter, declarations, README, FINAL_HANDOFF,
package manifest, qc docs for `supplement`/`supplementary`/S1–S6-as-
supplement/`10^9`:

- `manuscript/main.md`, `cover_letter.md`, `declarations.md`,
  `highlights.md`: no supplementary references remain.
- `scripts/make_submission_package.py`: supplementary.md entry removed.
- `qc/FINAL_TEXT_FIGURE_TABLE_CONSISTENCY_AUDIT.md`: updated.
- `qc/final_qc_report.md`: supplementary.md mention removed.
- `manuscript/ASR_GUIDE_AUDIT.md`: historical ASR-era audit kept as a
  provenance record only (it documents the withdrawn ASR submission's
  file list); not a submission-facing statement.
- `REPRODUCIBILITY.md` uses S1–S6 only as sensitivity-branch names —
  correct.
- No `10^9` or "1e9"/"on request" exploratory statement remains in
  submission-facing files (`configs/default.yaml` retains an unused
  exploratory grid key for completeness; it is not referenced anywhere
  in the manuscript or package).

VERDICT: PASS — supplementary material: NONE.
