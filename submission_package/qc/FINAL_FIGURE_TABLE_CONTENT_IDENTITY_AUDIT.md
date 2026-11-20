# Final figure/table content-identity audit — SMPT targeted pass

Scope: file exists, filename number, actual content, caption number,
caption description, first in-text citation, citation order, numeric
consistency — verified against the regenerated submission package.

## Figures (filename = caption number = content)

| File | Caption subject | Content verified | First citation |
|---|---|---|---|
| fig1_architecture.png | pipeline schematic | identical (unchanged) | §2.3 |
| fig2_p_vs_time.png | synthetic response surface | identical | §3.1 |
| fig3_redundancy.png | synthetic redundancy | identical | §3.1 |
| fig4_error_vs_n.png | median error vs n | identical | §3.1 |
| fig5_geometry.png | geometry conditioning | identical | §3.2 |
| fig6_pareto.png | information cost | identical | §3.2 |
| fig7_heatmap.png | severity x mismatch heatmap | identical | §3.2 |
| fig8_observed_sky.png | observed sky Aitoff | identical | §3.3 |
| fig9_motion_distributions.png | observed motion distributions | identical | §3.3 |
| fig10_propagation_comparison.png | propagation check | pixel-identical to pre-rename fig14_propagation_comparison | §3.4 |
| fig11_calibrated_primary.png | calibrated performance | pixel-identical to pre-rename fig12_calibrated_primary | §3.5 |
| fig12_random_vs_optimized.png | random vs D-optimal | pixel-identical to pre-rename fig11_random_vs_optimized | §3.6 |
| fig13_theory_vs_calibrated.png | theory vs calibration | pixel-identical to pre-rename fig10_theory_vs_calibrated | §3.7 |
| fig14_stress_tests.png | extrapolative stress tests | pixel-identical to pre-rename fig13_stress_tests | §3.9 |

First-citation order: 1,2,3,4 (§3.1), 5,6,7 (§3.2), 8,9 (§3.3), 10 (§3.4),
11 (§3.5), 12 (§3.6), 13 (§3.7), 14 (§3.9). Ascending — PASS.

## Tables (filename = caption number = content)

| File | Caption subject | Content verified | First citation |
|---|---|---|---|
| table1_architectures.csv | M1–M7 architectures | identical | §2.3 |
| table2_parameters.csv | simulation/scenario parameters | identical | §2.3 |
| table3_data_sources.csv | observational data sources | identical to pre-rename table5_data_sources | §2.4 |
| table4_parameter_classification.csv | calibration parameter classification | regenerated; quasar exists(t) row reclassified observed -> sensitivity-only | §2.9 |
| table5_performance.csv | synthetic primary outcomes | identical to pre-rename table3_performance | §3.1 |
| table6_sensitivity.csv | synthetic sensitivity/falsification | identical to pre-rename table4_sensitivity | §3.2 |
| table7_synth_vs_cal.csv | synthetic vs calibrated assumptions | identical | §3.4 |
| table8_calibrated_primary.csv | observation-calibrated results | identical | §3.5 |
| table9_theory_vs_calibrated.csv | theory vs calibrated verdicts | identical | §3.7 |

First-citation order: 1,2 (§2.3), 3 (§2.4), 4 (§2.9), 5 (§3.1), 6 (§3.2),
7 (§3.4), 8 (§3.5), 9 (§3.7). Ascending — PASS.

Method note: content identity was verified pixel-wise (PNG) and byte-wise
(CSV after sort) against the pre-rename files of record — not merely by
textual mention. The only intentional content change is Table 4's quasar
persistence reclassification (DEFECT 6 fix).

VERDICT: PASS

## Finishing-pass addendum (Figure 13 label correction)

Figure 13 (fig13_theory_vs_calibrated.png) was regenerated from the same
frozen results/calibration/calibrated_summary.csv with corrected legend
labels only: "observation-calibrated star50/pulsar50/quasar50" and
"synthetic star50/pulsar50/quasar50" (the "(observed)"/"(theory)"
suffixes removed). The plotted curves are unchanged — identical data
source, deterministic rendering; filename, caption (Figure 13, theory
versus calibration) and first citation (§3.7) unchanged. No other figure
or table file changed in this pass.

VERDICT: PASS (re-confirmed on the finishing-pass package)
