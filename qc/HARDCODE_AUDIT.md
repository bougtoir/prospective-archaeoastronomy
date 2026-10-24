# Hardcode Audit — ASR submission

Method: grepped manuscript/builders for numeric literals that duplicate simulation outputs; verified every quantitative claim in main.md is a {{placeholder}} resolved by manuscript_values.py from build outputs (values.json, 101 keys).

Findings:
- All headline results (P values, median errors, edge/ablation numbers, precision comparisons) come from generated artifacts (results/*.csv, results/summary). None are hardcoded in manuscript text.
- Constants appearing in text (horizons 1e3-1e8 yr, drift rates, usability times, N_MC=2000/10000, sigma_obs=1e-4 rad, p_mismatch=0.05, c=1.345 Huber, bit widths) are configuration parameters sourced from configs/default.yaml (config-as-truth) — declared scenario assumptions, labeled as such.
- Bibliographic data (years, volumes, pages) is reference metadata, not generated output.
- builders embed no frozen simulation numbers; figures/tables regenerate via make figures / make tables.

Verdict: PASS.
