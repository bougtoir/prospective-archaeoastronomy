# Line Wrap Audit

- manuscript/main.md paragraphs are single logical lines (no fixed-width source wrapping); the docx builders wrap whole paragraphs.
- manuscript/build/manuscript_final.docx / manuscript_inline.docx: every paragraph emitted as a continuous run — no embedded newlines or manual line breaks (w:br count: 0).
- Rendered PDF wraps by page width only; no mid-sentence forced breaks observed in visual audit.
- Tables are Word tables, not text-aligned columns.

Verdict: PASS — no character-count manual wrapping.
