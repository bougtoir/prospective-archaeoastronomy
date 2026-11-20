# Canonical freeze — prospective-archaeoastronomy

    project                        = prospective-archaeoastronomy
    canonical_branch               = main
    scientific_canonical_commit    = f1dd191bb34ea89c172239206bfb09532861c8e4
    final_submission_package_commit = b20b61480d6f0e8c049aa6b169a993ef31a02d0a

## Scientific vs package commit distinction (FIX 1 resolution)

A real tree/diff comparison between
f1dd191bb34ea89c172239206bfb09532861c8e4 and
08d6af6e45952b901809c7a0f53bcd4bc029ad1a shows every changed file is one of:

- metadata / manuscript wording (main.md phrasing, highlights, cover letter,
  declarations);
- QC files and audit documents;
- package assembly (file renames figure/table, zip, docx/pdf rebuild);
- label/classification wording in calibration registry/classification CSVs
  and src/proarch/calibration.py docstrings (no numeric values changed);
- reference metadata (Manchester journal field);
- supplementary.md removal.

No scientific code path, configuration, input data, calibration numerical
model, simulation output, numerical result, figure curve, or table value
changed. Classification rows changed only their label text
("observed" -> "sensitivity-only"), not any number.

Therefore:

- Scientific canonical commit: f1dd191bb34ea89c172239206bfb09532861c8e4
  — full clean-clone `make all` verified (pytest 16/16, values.json
  byte-identical, all CSVs identical within float noise). All scientific
  outputs were clean-clone reproduced at this commit.
- Final submission/package commit: b20b61480d6f0e8c049aa6b169a993ef31a02d0a
  (the tip containing the targeted-pass + finishing-pass corrections).
- Subsequent package/QC commits do not modify scientific dependencies and
  do NOT redefine the scientific canonical commit.

The public repository tip may advance for metadata or unrelated maintenance;
such later commits do not change the canonical scientific version for this
submission.

## Historical freezes (preserved, not overwritten)

- f1dd191bb34ea89c172239206bfb09532861c8e4 — SMPT scientific canonical
  (full clean-clone `make all` verified).

- b4b2cd52a1ef50ae4b5e9999dc0cd0f3b1978b7e — Advances in Space Research (ASR)
  submission version. Verified by clean public clone `make all` at that commit
  (~49 min, all outputs identical). Remains the historical reproducibility
  point for the ASR manuscript; the SMPT revision does not redefine it.

The canonical commit advances only for:
  - a genuine scientific correction;
  - a code defect affecting reported results;
  - a manuscript revision requiring changed generated outputs;
  - an explicit user instruction to create a new canonical version.

In that case a new explicit canonical version is created, the previous frozen
commit is documented, and affected reproducibility/QC checks are rerun — the
historical provenance is never overwritten silently.
