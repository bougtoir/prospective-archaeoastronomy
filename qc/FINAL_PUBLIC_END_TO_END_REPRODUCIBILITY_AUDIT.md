# Final Public End-to-End Reproducibility Audit — ASR submission

    Source tested: PUBLIC MAIN
    Repository:    https://github.com/bougtoir/prospective-archaeoastronomy
    Branch:        main
    Commit:        b4b2cd52a1ef50ae4b5e9999dc0cd0f3b1978b7e
    Fresh clone:   YES (new directory, git clone of the public URL)
    Hidden local files: NO
    Canonical command:
        python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"
        make all PYTHON=.venv/bin/python
    Result: PASS

Duration: 56m57s wall — test (16 passed), simulate (763,400 MC replications,
master_seed 20260924), summarize, figures, tables, manuscript-results, package, qc.

Per-artifact comparison against the final ASR submission state:

| artifact | result |
|---|---|
| results/e*.csv (14 raw result files) | PASS — identical row sets (sort-order equal) |
| results/summary_*.csv (14 summary files) | PASS — identical |
| manuscript/values.json (101 injected values) | PASS — identical |
| manuscript/build/manuscript_final.md | PASS — byte-identical |
| tables/table1-4 .csv | PASS — identical |
| figures/fig1-7 .png | PASS — byte-identical |
| manuscript_final.docx / manuscript_inline.docx | PASS — built; content identical (docx zip timestamps only) |
| submission_package/ASR_submission_package.zip | PASS — built |

This commit is the frozen canonical scientific commit (see qc/CANONICAL_FREEZE.md);
the repository tip may later advance for metadata-only changes without redefining
it. This run is the canonical check: fresh clone of PUBLIC MAIN at the canonical
submission commit. Earlier branch-level runs are superseded.

Verdict: PASS.
