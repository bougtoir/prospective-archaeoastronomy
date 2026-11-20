# Advances in Space Research — Guide for Authors audit

Journal: Advances in Space Research (ASR), ISSN 0273-1177, official journal of COSPAR
(https://www.sciencedirect.com/journal/advances-in-space-research/publish/guide-for-authors;
submission via Editorial Manager https://www.editorialmanager.com/AISR).
Audited 2026-10-22 against the live ScienceDirect guide.

| Requirement | Source | Compliance action |
|---|---|---|
| Scope: all areas of space research, incl. astrophysics from space, fundamental physics in space, the Earth–Moon system, long-duration space systems; life-sciences papers excluded (go to LSSR) | ScienceDirect aims & scope | Manuscript framed as deep-time celestial reference-network reconstruction for long-duration space information systems — astrometry/reference-frame engineering, in scope; "prospective archaeoastronomy" kept secondary, not in title or abstract lead |
| Peer review: single anonymized; editor screening then >=2 reviewers | Guide | Cover letter states novelty, findings, and negative H2 result up front |
| File format: Word or PDF; initial submission may be a single file containing title page, abstract, keywords, text, figures with captions, tables, references, supplementary | Guide for authors / ASR EM instructions | `manuscript_inline.docx` (title page + text + figures + tables + references embedded, all math as native OMML) is the primary review file; `manuscript_final.docx` (text only) also provided; separate figure/table files included |
| Math formulae: editable equation objects (Word equation editor / OMML); no plain-text or image math | Elsevier math formulae policy + Acta rejection cause | ALL math converted to OMML via scripts/build_docx_omml.py; zero LaTeX syntax in visible text; verified by qc/OMML_STRUCTURAL_AUDIT.md + full-page PDF render audit |
| Abstract: separate abstract for copy-paste into EM | Guide | `abstract.txt` generated from manuscript_final.md and included in the package |
| Keywords | Elsevier/ASR norms | 6 keywords after the abstract |
| Highlights: optional, recommended; 3–5 bullets, <=85 chars each | Elsevier highlights policy | manuscript/highlights.md (5 bullets, <=85 chars, ASR header) |
| Title page: authors, affiliations, corresponding author with e-mail (phone requested by EM; ORCID welcome) | Guide | Title block carries name, affiliation, e-mail, ORCID; telephone is an EM-entry field — flagged in FINAL_USER_FIELDS_REQUIRED.txt |
| Suggested reviewers: 3–6 recommended, entered in EM | ASR EM instructions | Not fabricated; flagged as an author-time EM field in FINAL_USER_FIELDS_REQUIRED.txt |
| References: Elsevier numbered style, in order of appearance | Elsevier reference policy / dependent CSL style | build_manuscript.py numbers citations [n] in order of appearance; every bibliography entry cited; verified by reference audit |
| Declaration of competing interests: mandatory; EM declarations tool output uploaded as .docx | Guide | declarations.md provided; note that EM's declarations tool output is generated at submission time |
| Funding: standard disclosure format | Guide | "received no specific grant" statement present |
| Generative AI disclosure: mandatory if used | Guide | Devin (Cognition AI) disclosure present in declarations |
| Data/code availability | Guide | Public repo URL stated in declarations and cover letter; `make all` reproduces all outputs; verified by public-repo end-to-end audit |
| Graphical abstract: optional | Elsevier policy | Included (graphical_abstract.png) |
| Supplementary material: separate file allowed | Guide | supplementary.md included |
| Charges: no page charge except printed color figures | ASR guide | All figures monochrome-safe |

## Positioning decisions

- Title retained: "Deep-Time Celestial Reference Networks for Reconstructing
  Terrestrial Orientation" — celestial-reference framing leads;
  "prospective archaeoastronomy" appears only as a late-paper framing term.
- Keywords: celestial reference systems; robust estimation; deep space
  navigation; redundancy; Monte Carlo methods; information theory.
- Readership pivot: abstract/introduction already lead with ICRS/ICRF/Gaia and
  pulsar-map practice — no structural rewrite needed for a space-research
  readership beyond the cover letter retarget.
