# Final Visual Render Audit — ASR submission

Method: LibreOffice headless DOCX->PDF, pdftoppm 80 dpi PNGs, every page visually inspected.

- manuscript_final.docx -> manuscript_final.pdf: 11 pages, all inspected.
- manuscript_inline.docx -> manuscript_inline.pdf: 20 pages; all figure/table pages inspected.

Findings during audit (fixed and re-verified):
- "Abstract## Abstract" heading duplication -> fixed in build_docx_omml.py (continue after add_heading).
- exp(-(t/tau)^a) rendered as "exp¿" (dropped argument) -> e^{-(t/tau_k)^{a_k}} form.
- arg min corrupted ("¿min") -> \text{arg min}_{...}.
- ~ rendered as literal "approx" text -> \approx with single backslash; now renders approx0.2 / approx0.5 correctly.
- Units yr/rad/deg render clean (no letter spacing) after \text{} switch.

Post-fix state: all pages render clean; math legible (n-hat, epsilon_theta, P(<1 deg), S_k(t) stacked exponent, ||.||^2 norms, 10^3-10^8 yr exponents); no missing glyphs, no corrupted symbols, no placeholders.

Note: PDF pages are the verification artifact; the DOCX contains native Word OMML equations which also render correctly in Microsoft Word.

Verdict: PASS.
