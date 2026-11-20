# Semantic citation audit — SMPT revision (targeted pass)

Gate B of the final reference QC: every reference must support the exact
nearby claim, not merely appear in the bibliography.

| Key | Cited at | Nearby claim | Verdict |
|---|---|---|---|
| arias1995icrs | Intro; Discussion | ICRS is realized by ensembles of quasars | SUPPORTS |
| charlot2020icrf3 | Intro; 2.4; Discussion | ICRF3 VLBI positions, defining sources, sky distribution | SUPPORTS |
| mignard2018gaiacrf2 | Intro; Discussion | Gaia celestial reference frame | SUPPORTS |
| lindegren2018gaiadr2 | Intro | Gaia astrometric solution | SUPPORTS |
| lindegren2021gaiaedr3 | Intro; 2.4 | Gaia EDR3 astrometric solution | SUPPORTS |
| spratling2009starid | Intro | star identification fuses many stellar measurements | SUPPORTS |
| downs1974pulsar | Intro | pulsar-based navigation concept | SUPPORTS |
| sheikh2006xnav | Intro | X-ray pulsar navigation | SUPPORTS |
| becker2013pulsarnav | Intro | autonomous pulsar navigation | SUPPORTS |
| hobbs2005pulsarpm | Intro; 4.3 | pulsar proper motions measured in bulk | SUPPORTS |
| drake1972message | Intro; 4.3 | Pioneer/Voyager pulsar map history | SUPPORTS |
| sagan1978murmurs | Intro; 4.3 | Voyager record / pulsar map history | SUPPORTS |
| gaiadr3 | 1.x; 2.4 | Gaia DR3 catalogue content | SUPPORTS |
| manchester2005atnf | 1.x; 2.4 | ATNF pulsar catalogue | SUPPORTS — bibliographic metadata corrected to AJ 129(4), 1993–2006, DOI 10.1086/428488 |
| charlot1990structure | 2.7 | radio-source structure / centroid wander | SUPPORTS |
| titov2011aberration | 2.7; 4.3 | secular aberration drift / frame stability | SUPPORTS |
| fedorov1972 | 2.10 | D-optimal design objective log det(Q^T Q) | SUPPORTS — moved from Pioneer/Voyager sentence (historical) to optimal-experiment Methods context |
| huber1964robust | 2.11 | Huber regression | SUPPORTS |
| fischler1981ransac | 2.11 | RANSAC consensus estimator | SUPPORTS |
| wilson1927 | 2.12 | Wilson score intervals | SUPPORTS |
| harris2020numpy | 2.16 | NumPy/SciPy | SUPPORTS |
| sargent2013verification | 2.16 | V&V categories | SUPPORTS |
| cocconi1959searching | 4.3 | long-lived messages to unknown receivers | SUPPORTS |

Checks: no historical source is cited for an optimization method; no methods
source is cited as historical evidence; every bibliography entry is cited;
every in-text citation resolves (see FINAL_REFERENCE_AND_CITATION_AUDIT.md).

VERDICT: PASS — 23/23 references semantically support their citation contexts.

## Finishing-pass re-verification (2026-11-09)

Re-run against the finishing-pass manuscript: citation order, contexts and
bibliographic metadata unchanged from the targeted-pass audit above;
Fedorov remains in the D-optimal Methods context and Manchester shows
The Astronomical Journal 129(4) 1993-2006 DOI 10.1086/428488.

VERDICT: PASS — 23/23.
