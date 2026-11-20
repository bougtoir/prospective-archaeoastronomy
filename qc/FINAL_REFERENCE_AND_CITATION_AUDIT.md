# Reference & citation audit — SMPT revision

- bibliography entries: 23
- entries cited in text: 23
- uncited entries: 0
- citation style: Elsevier numbered, ordered by first appearance
  (scripts/build_manuscript.py renumbers [key] -> [n] and emits the list in
  first-appearance order, so first-citation order is correct by construction).
- DOI metadata present for all journal articles (references.bib).
- new calibration references added: hobbs2005pulsarpm (MNRAS 360, 974),
  charlot1990structure (AJ 99, 1309), lindegren2021gaiaedr3 (A&A 649, A2),
  titov2011aberration (A&A 529, A91), sargent2013verification
  (J. Simulation 7, 12). All are real, standard, and support the claims at
  their citation points.

Targeted-pass corrections:
- manchester2005atnf: journal corrected from 'Publications of the
  Astronomical Society of Australia' to The Astronomical Journal,
  129(4), 1993-2006, DOI 10.1086/428488 (verified against the
  authoritative record for the ATNF catalogue paper).
- fedorov1972: moved from the Pioneer/Voyager historical sentence to
  the D-optimal network-construction Methods context (Section 2.10).

Gate A (bibliographic validity): all journal articles carry title,
authors, journal, year, volume/issue where applicable, pages, DOI in
references.bib; spot-verified metadata for the corrected ATNF entry.
Gate B (semantic validity): see qc/SEMANTIC_CITATION_AUDIT.md — 23/23
references support their citation contexts.

VERDICT: PASS
