"""Regression tests for reference metadata defects found in QC."""
import re

BIB = "manuscript/references.bib"


def _entries():
    import pathlib
    bib = pathlib.Path(BIB).read_text()
    return re.split(r"\n(?=@)", bib)


def test_atnf_catalogue_doi_is_astronomical_journal():
    """Defect: manchester2005atnf carried DOI 10.1071/AS04053, which resolves to
    an unrelated PASA paper. Correct DOI is 10.1086/428488 (AJ 2005)."""
    bib = open(BIB).read()
    assert "10.1071/AS04053" not in bib
    assert "10.1086/428488" in bib


def test_no_duplicate_dois():
    dois = re.findall(r"doi=\{([^}]+)\}", open(BIB).read())
    assert len(dois) == len(set(dois)), "duplicate DOIs in references.bib"
