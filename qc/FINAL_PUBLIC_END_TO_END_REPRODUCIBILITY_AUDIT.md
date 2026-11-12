# FINAL PUBLIC END-TO-END REPRODUCIBILITY AUDIT — SMPT revision

Date: 2026-10-31 (UTC)
Auditor: Devin session 51f25617f45c4de59532ad268751c01c

## Verdict: PASS

## Method

- Public repository cloned fresh to `/tmp/proarch_public` and checked out at the
  candidate canonical commit **f1dd191bb34ea89c172239206bfb09532861c8e4**
  (public `main` tip after the SMPT revision sync + README retarget sync).
- Reproduction command (exactly as published):

      python3 -m venv .venv && .venv/bin/pip install -e ".[dev]" && make all PYTHON=.venv/bin/python

- `make all` executed in a clean environment (no results, figures, tables,
  values, manuscript builds, or package artifacts present beforehand).

## What was recomputed vs inherited

Per the scientific-freeze rule, this audit reran the full pipeline for
*reproducibility verification only*. In the revision itself, the synthetic
theory layer (E1–E11) was an inherited frozen input, not re-derived for new
science; the observation-calibrated layer (C_*, S_* sensitivity, propagation
comparison, theory-vs-calibrated verdicts) is the new layer executed during the
revision. The clone run demonstrates the combined frozen + new state rebuilds
end-to-end from a public clean clone.

## Results

| Check | Result |
|---|---|
| pytest | 16/16 PASS |
| run_simulations.py (synthetic grid, 763,400 reps) | completed |
| run_calibrated_simulations.py (352,000 reps + 25,000 sensitivity) | completed |
| summarize / theory_vs_calibrated / figures / tables / values / manuscript / package | completed |
| qc_audit.py | PASS, 0 issues |
| `manuscript/values.json` (407 provenance keys) | **byte-identical** to wip working-tree output |
| `results/calibration/calibrated_summary.csv` | identical within float formatting (max abs diff 7.1e-15; non-numeric columns identical) |
| `results/calibration/sensitivity_summary.csv` | byte-identical after sort |
| `results/calibration/theory_vs_calibrated_findings.csv` | identical (A/B/C/D/F/H CONFIRMED; E/G PARTIALLY CONFIRMED) |
| `results/calibration/propagation_comparison.csv` | identical |
| DtypeWarning on summary read | benign (pre-existing, documented) |

Note on float diffs: 216 differing lines in `calibrated_summary.csv` differ only
in the last printed digits of computed means (e.g. 0.005344447561553851 vs
…882); values consumed by the manuscript (values.json) are byte-identical, so
all reported numbers are reproducible exactly as printed.

## Conclusion

The public repository at commit f1dd191bb3 fully regenerates all SMPT
submission artifacts — simulation results, calibrated validation outputs,
figures, tables, manuscript provenance values, docx builds, and the submission
zip — with all QC gates PASS. This commit is therefore recorded as the new
canonical scientific commit in `qc/CANONICAL_FREEZE.md`; the historical ASR
freeze b4b2cd52a1ef50ae4b5e9999dc0cd0f3b1978b7e remains preserved as a
historical reproducibility point.

## Targeted-pass addendum (2026-11-09)

The post-freeze targeted revision changed only manuscript text, file
names, packaging, QC documentation, and two classification labels —
no simulation code, configuration, or raw data (verified by diff
against f1dd191bb3). Per the scientific-freeze rule, simulation outputs
were inherited unchanged. A clean-clone verification at the new public
tip reruns the downstream pipeline (summaries, values, figures, tables,
manuscript, package, qc) against the committed results; full sim rerun
is intentionally skipped as no upstream dependency changed (full clean
`make all` remains verified at f1dd191bb3).

Verification at the targeted-pass public tip 08d6af6e45952b901809c7a0f53bcd4bc029ad1a:
pytest 16/16 PASS; make summarize / theory-vs-cal / figures / tables /
manuscript-results / package / qc all regenerated successfully;
manuscript/values.json and manuscript/build/manuscript_final.md
byte-identical to the wip working tree. VERDICT: PASS.

## Finishing-pass addendum (2026-11-09)

Canonical terminology refined per the provenance-correction pass:
the scientific canonical commit is f1dd191bb34ea89c172239206bfb09532861c8e4
(full clean-clone `make all` verified). The final submission/package
commit is the public tip containing the finishing-pass corrections; a real
tree diff shows it changes no scientific dependency (wording, labels,
filenames, QC docs and package assembly only). Verification of the
finishing-pass public tip repeats the downstream regeneration check
(figures incl. relabelled fig13, tables, manuscript, package, qc) against
the committed frozen results.

Verification at the finishing-pass public tip
b20b61480d6f0e8c049aa6b169a993ef31a02d0a (clean clone, downstream only
per freeze rule): pytest 16/16 PASS; make figures / manuscript-results /
package / qc all regenerate successfully; manuscript/values.json
byte-identical to the wip working tree; regenerated fig13 carries the
corrected legend labels; manuscript_final.pdf is 17 pages;
qc_audit.py PASS 0 issues. VERDICT: PASS.
