# Acta Astronautica — Guide for Authors audit

Checked: 2026-09-24 (UTC). Primary source: ScienceDirect Guide for Authors,
Acta Astronautica, ISSN 0094-5765
(https://www.sciencedirect.com/journal/acta-astronautica/publish/guide-for-authors).

| Requirement | Source | Compliance |
|---|---|---|
| Scope: space science/technology; astrodynamics, space transportation and communications, extraterrestrial intelligence, reference systems | ScienceDirect guide + IAA journal page (iaaspace.org/publications/acta-astronautica) | Manuscript framed as celestial reference-network robustness for long-duration astronautical information systems; SETI relevance secondary |
| Article types: original research papers and Notes | Guide for Authors, "Types of Contributions" | Original research paper |
| Submission checklist: corresponding author + contact, keywords, figures with captions, tables with titles, figure/table citations matching files, spellcheck, all references cited in text and vice versa, competing-interest statement | Guide for Authors, "Submission checklist" | See manuscript package: title page, 6 keywords, figures/tables as separate files with captions, QC audit cross-checks citations |
| Declaration of competing interest required even if none | Guide for Authors | declarations.md includes competing-interest statement (single-author default; confirmation tracked in FINAL_USER_FIELDS_REQUIRED.txt) |
| Generative-AI declaration required if AI tools used in manuscript preparation | Guide for Authors | AI-use statement included in declarations.md (Devin/Cognition AI used for code + drafting pipeline; Elsevier template wording) |
| Abstract: concise, factual, self-contained; avoid references and non-standard abbreviations | Guide for Authors (PDF mirror) | Abstract states problem, methods, quantitative results, conclusions; no citations |
| Keywords: max 6, American spelling | Guide for Authors | 6 keywords supplied |
| Highlights: required by journal workflow (3–5 bullets, ≤85 chars each) | ScienceDirect submission workflow / Elsevier highlights spec | manuscript/highlights.md, 5 bullets ≤85 chars |
| Graphical abstract: where applicable | Submission checklist | manuscript/graphical_abstract.png generated (schematic, code-produced) |
| Reference style: numeric, square brackets, in order of appearance (Elsevier numeric with titles) | Paperpile/CSL dependent style acta-astronautica (elsevier-with-titles) | build_manuscript.py numbers citations in order of appearance and emits the list accordingly; qc checks all keys cited |
| Article structure: Introduction / M&M / Theory / Results / Discussion / Conclusions / Appendices | Guide for Authors | Manuscript follows this order; Methods precede Results |
| Data availability statement required | Guide for Authors ("Data statement") | Declarations include data + code availability pointing to public repository |
| Supplementary material: separate file, referenced in text | Guide for Authors | supplementary.md holds extended tables; cited in text |
| Ethics/declarations, funding, author contributions (CRediT) | Guide for Authors | declarations.md with CRediT + funding statements (defaults; FINAL_USER_FIELDS_REQUIRED.txt tracks author confirmation) |

## Notes
- No fixed word limit for research papers was identified in the current guide; length is governed by article type norms. We keep to typical Acta length (~8–10k words equivalent).
- Current official instructions take precedence over this audit where they differ at submission time.
