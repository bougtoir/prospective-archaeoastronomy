# Text / Figure / Table Consistency Audit — ASR submission

Cross-checks between claims in text and the generated artifacts:

- Table 3 (P(eps_theta<1 deg) by architecture/horizon) values are generated from simulation outputs by make_tables.py and injected into text via manuscript_values.py placeholders — no hand-copied numbers; spot check: quasar-50 at 1e7 yr P=1.0, M7 hybrid 0.9711, stars-50 0.0, quasar retention 0.043 at 1e8 yr — consistent between text and Table 3.
- Figure 2 (P vs log t) consistent with Table 3; Figure 3/4 (P, median error vs n at 1e4 yr) consistent with saturation narrative; Figure 5 geometry (isotropic vs clustered/banded/D-optimal) consistent with H3 text; Figure 6 bit-cost/reliability consistent with chirality text; Figure 7 heatmap consistent with robustness text (fails p_mismatch>=0.3-0.5 pessimistic, P=0.719).
- Claim control re-verified: H2 stated as NOT supported; homogeneous quasar network outperforms tested hybrids at 1e8 yr (0.043 vs 0.0138); M1 relational scalar underdetermined; M1b ~0.5 ceiling attributed to benchmark definition; edges benefit stated as corruption-model-specific; long-horizon results scenario-conditional.
- Numbers in Discussion (approx0.3-0.5 mismatch breakdown) consistent with Figure 7 heatmap cells.

Verdict: PASS.
