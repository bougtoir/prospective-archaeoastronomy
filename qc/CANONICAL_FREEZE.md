# Canonical freeze — prospective-archaeoastronomy

    project                     = prospective-archaeoastronomy
    canonical_branch            = main
    canonical_scientific_commit = b4b2cd52a1ef50ae4b5e9999dc0cd0f3b1978b7e

This commit is the frozen reproducibility source for the current manuscript
submission (Advances in Space Research). Verified by a fresh public-main clone
running `make all` end-to-end (PASS, ~49 min, all generated outputs identical).

The manuscript and frozen scientific results are reproducible from public commit
b4b2cd52a1ef50ae4b5e9999dc0cd0f3b1978b7e. The public repository tip may later
advance for metadata or unrelated maintenance; such later commits do not change
the canonical scientific version for this submission.

The canonical commit advances only for:
  - a genuine scientific correction;
  - a code defect affecting reported results;
  - a manuscript revision requiring changed generated outputs;
  - an explicit user instruction to create a new canonical version.

In that case a new explicit canonical version is created, the previous frozen
commit is documented, and affected reproducibility/QC checks are rerun — the
historical provenance is never overwritten silently.
