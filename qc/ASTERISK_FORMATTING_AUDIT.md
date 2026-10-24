# Asterisk Formatting Audit — final package-wide pass

Scope: every submission-facing text file in ASR_submission_package.zip plus
README.md and manuscript/main.md sources.

- manuscript/build/manuscript_final.docx: 0 "*" in any w:t text node.
- manuscript/build/manuscript_inline.docx: 0 "*" characters.
- cover_letter.md: 0 formatting asterisks ("*decoded*" -> "decoded"; rewritten first-person singular).
- highlights.md: 0 asterisks.
- supplementary.md: 0 asterisks.
- declarations.md: 0 asterisks.
- README.md: 0 asterisks ("*Advances in Space Research*" -> plain).
- abstract.txt: 0 asterisks (extracted from built manuscript).
- qc/*.md audit files: literal "*" occurrences are glob patterns (e*.csv) or
  documentation of the asterisk check itself — no Markdown emphasis.
- manuscript/main.md retains Markdown emphasis markers in source only; none
  survive into any submitted file (verified by docx XML scan).
- No multiplication operators or math symbols were removed; OMML untouched.

Result: formatting asterisks across all submission-facing files = 0. PASS.
