# Numeric consistency audit — SMPT revision

Single source of truth: generated outputs in results/ + values.json.
Audit method: manuscript_final.md contains no numeric literals for
result values (all interpolated from values.json); tables/figures read
the same CSVs. qc_audit.py cross-check: PASS 0 issues (every {{token}}
resolved; no token resolved to a value inconsistent with its source key;
caption numbers match the files they reference).

Scope covered: abstract, Results 3.1-3.10, Discussion, Conclusions,
highlights, cover letter, captions, Tables 1-9, Figures 1-14.
(Supplementary material removed in the targeted pass; S1-S6 content is
either integrated in the main text or archived in REPRODUCIBILITY.md.)

VERDICT: PASS — no unexplained numeric discrepancy.
