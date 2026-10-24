# Reference and Citation Audit — ASR submission

- 18 references in references.bib; all 18 cited in text; 0 orphans; 0 duplicate DOIs (regression-tested).
- Numbering [1]–[18] assigned in order of first appearance by build_manuscript.py (reference_map.json verified).
- 14 DOIs verified live: 13 via Crossref works API (metadata saved to data/raw/crossref_20261022/, ledger-recorded), becker2013 Acta Futura DOI resolves via doi.org to the ESA PDF (ESA DOIs are not Crossref-indexed).
- DEFECT FOUND+FIXED: manchester2005atnf DOI 10.1071/AS04053 resolved to an unrelated PASA paper -> corrected to 10.1086/428488 (AJ 2005 ATNF pulsar catalogue); regression test in tests/test_references.py.
- Refs 1,6,10,11 have no DOIs (pre-DOI reports/books); verified by inspection of the reference text.
- All citations support the claims at their positions (reference-system framing, pulsar nav, robust estimation, statistics, tools, catalogues).
- Figure citation order fixed: Figure 4 was cited before Figure 3; "(Figures 2 and 4)" -> "(Figures 3 and 4)"; first-citation order now 1,2,3,4,5,6,7.

Verdict: PASS.
