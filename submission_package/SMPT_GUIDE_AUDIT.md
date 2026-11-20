# SMPT Guide Audit — Simulation Modelling Practice and Theory (Elsevier)

Audit date: 2026-10-31 (UTC). Sources: ScienceDirect Guide for Authors page,
journal landing page, JCR/WoS journal record (quartiles), Scopus/Scimago
listings as secondary (URLs in reference audit).

## Identification
- Journal: Simulation Modelling Practice and Theory
- ISSN: 1569-190X (print) / 1878-1462 (electronic). Publisher: Elsevier B.V.
- Editorial Manager submission system.

## Quartile / fees (user constraints)
- Quartile basis: JCR (Journal Citation Reports), primary criterion.
  JIF 4.6 (2025 JIF, released June 2026); 5-year JIF 4.5.
  JCR categories (SCIE):
    * COMPUTER SCIENCE, SOFTWARE ENGINEERING — Q1;
    * COMPUTER SCIENCE, INTERDISCIPLINARY APPLICATIONS — Q2.
  => JCR quartile is category-dependent: Q1 in Software Engineering,
     Q2 in Interdisciplinary Applications. Not an unqualified "Q1".
- Secondary metrics (not the quartile basis): Scopus CiteScore 9.9,
  Modeling and Simulation rank 19/397; SJR 0.962 (Scimago Q1).
- Fees: hybrid journal. Subscription route = no mandatory publication fee.
  Optional open-access APC USD 2,970 — NOT chosen; not required.
  => satisfies "JCR Q1 category present + mandatory fee zero".

## Fit
- Scope explicitly solicits: theoretical aspects of modelling and simulation
  (sensitivity analysis, experimental design, meta-modelling, methods and
  algorithms for validation and verification, selection and comparison
  procedures) AND methodology/application of modelling and simulation in any
  application area.
- Application papers must make "model development, computer implementation,
  ... and validation/verification with real data" transparent to readers —
  this matches the revision's two-layer design (synthetic theory layer +
  observation-calibrated validation layer). The application domain
  (archaeoastronomy / terrestrial orientation reconstruction) is admissible
  under "methodology and application ... in any area".

## Article types / requirements (from Guide for Authors)
- Regular research articles; comprehensive surveys/critical reviews also
  considered. No fixed page limit published for regular articles.
- Single-anonymized peer review.
- Declarations required: competing interests, funding, author contributions
  (CRediT), Declaration of generative-AI use (must be declared if used),
  data-availability statement (Elsevier "data statement" mandatory).
- Highlights: required (Elsevier standard, 3-5 bullets, <=85 chars each).
- Abstract: required on title page.
- Keywords: required.
- Math formulae: equations must be editable (Word-native or LaTeX — our
  OMML-native docx satisfies this; this was the Acta desk-reject failure
  mode, now structurally prevented).
- References: Elsevier numbered or author-year styles accepted at
  submission ("your paper your way" applies at first submission); we use
  numbered citations (Vancouver-style), consistent with our builder.
- Figures/tables: cited in text; supplied at acceptable resolution.
- Preprints permitted.
- Suggested reviewers: Editorial Manager prompts; provide author-filled
  list in FINAL_USER_FIELDS_REQUIRED.txt (as before).

## Validation expectations (reading of aims/scope)
- Verification & validation are named scope topics; a V&V section +
  diagnostics (unit tests, known-truth recovery, catalogue-geometry
  reproduction, calibration diagnostics, resampling checks where feasible)
  is the expected standard. Implemented as qc/MODEL_VALIDATION_REPORT.md
  + Methods 2.12–2.15.

## Differences from ASR package
- Abstract/highlights/keywords stay separate files as before.
- Cover letter rewritten for SMPT (no mention of prior rejections).
- Data availability statement names the persisted raw catalogues +
  acquisition ledger + checksums.
- AI-use declaration kept (per Elsevier policy).

## Residual risks
- "your paper your way" first-submission leniency means numbered refs are
  acceptable; production may later request a specific style — acceptable.
- No word-count cap found; keep length comparable to prior package.
