# Visual render audit — manuscript_final.docx -> PDF (LibreOffice), 17 pages

Every page rendered and inspected (pdftoppm rasters + pdftotext) on the
regenerated DOCX of the targeted pass:

- p1 title/author + abstract: three-layer wording, calibrated headline,
  stress-test disclaimer render correctly.
- p2 keywords + Introduction start: Pioneer/Voyager citation now [11,12]
  (Fedorov removed); clean.
- p3 Methods start: OMML equations (N0, Q, b_i, G, H_ijk, argmin solve,
  det) render as typeset math with proper subscripts/superscripts.
- p4: 2.3 declared assumptions incl. mirror-ambiguity prior 0.5 and
  RANSAC 2 deg/120 iterations; no clipped content.
- p5-6: catalogue/calibration/propagation sections; inline math
  (Q^T Q, log-uniform bounds) typeset; Manchester cite [14] correct.
- p7: 2.9 quasar persistence reworded as conditional sensitivity-only
  assumption; 2.10 cites [17] (Fedorov) at D-optimal selection.
- p8: sections 2.12-2.16 numbered correctly; S1-S6; REPRODUCIBILITY.md
  pointer in 2.16.
- p9-10: Results 3.1-3.5; Table 6 citation added in 3.2; numbers
  consistent with values.json.
- p11: 3.6-3.9; quasar conditional wording present; no placeholders,
  no {{tokens}}, no code fences, no backticks.
- p12: 3.10 + Discussion 4.1-4.2; horizon taxonomy consistent.
- p13: 4.3-4.4 + Conclusions; no supplementary claims.
- p14: Declarations incl. strengthened data availability and Generative
  AI statement.
- p14-15: figure captions 1-14 and table captions 1-9 complete;
  filenames now match caption numbers.
- p15-17: 23 numbered references in citation order; DOIs present;
  [14] Manchester shows The Astronomical Journal (2005).

Global checks: literal '*' = 0; backticks = 0; residual LaTeX = 0;
placeholders = 0; tracked changes/comments = 0; black text throughout;
Times New Roman 12 pt body; no manual fixed-character wrapping.

VERDICT: PASS — 17/17 pages inspected.
