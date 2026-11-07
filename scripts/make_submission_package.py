"""Assemble submission_package/ and ASR_submission_package.zip from the
current generated outputs. Run after `make all` so the package always
carries the latest numbers/figures.
"""
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "manuscript" / "build"
MS = ROOT / "manuscript"
PKG = ROOT / "submission_package"
ZIP = PKG / "ASR_submission_package.zip"

FLAT_FILES = [
    BUILD / "manuscript_final.docx",
    BUILD / "manuscript_inline.docx",
    BUILD / "manuscript_final.pdf",
    MS / "highlights.md",
    MS / "cover_letter.md",
    MS / "declarations.md",
    MS / "supplementary.md",
    MS / "references.bib",
    MS / "graphical_abstract.png",
    MS / "ASR_GUIDE_AUDIT.md",
    ROOT / "FINAL_USER_FIELDS_REQUIRED.txt",
    ROOT / "FINAL_HANDOFF.txt",
]

REQUIRED = [
    BUILD / "manuscript_final.docx",
    BUILD / "manuscript_inline.docx",
]

QC_BUNDLE = [
    "ADVERSARIAL_REVIEW_FINAL.md",
    "FINAL_ADVERSARIAL_DECISION.md",
    "HARDCODE_AUDIT.md",
    "NUMERIC_PROVENANCE_AUDIT.csv",
    "FINAL_PUBLIC_END_TO_END_REPRODUCIBILITY_AUDIT.md",
    "FINAL_REFERENCE_AND_CITATION_AUDIT.md",
    "reference_audit.csv",
    "FINAL_FIGURE_TABLE_CITATION_AUDIT.md",
    "FINAL_TEXT_FIGURE_TABLE_CONSISTENCY_AUDIT.md",
    "OMML_STRUCTURAL_AUDIT.md",
    "OMML_EQUATION_INVENTORY.csv",
    "FINAL_VISUAL_RENDER_AUDIT.md",
    "ASTERISK_FORMATTING_AUDIT.md",
    "LINE_WRAP_AUDIT.md",
    "FINAL_ASR_SUBMISSION_QC.md",
    "qc_report.md",
]


def write_abstract():
    """Extract the Abstract section of the built manuscript to abstract.txt
    (ASR asks for a separate abstract for copy-paste into Editorial Manager)."""
    text = (BUILD / "manuscript_final.md").read_text()
    m = re.search(r"## Abstract\n\n(.+?)\n\n## ", text, re.S)
    if not m:
        raise SystemExit("abstract section not found in manuscript_final.md")
    (BUILD / "abstract.txt").write_text(m.group(1).strip() + "\n")
    return BUILD / "abstract.txt"


def render_pdf():
    """Render the final DOCX to PDF for QC/archive when LibreOffice exists."""
    pdf = BUILD / "manuscript_final.pdf"
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        for cand in ("/usr/lib/libreoffice/program/soffice",
                     "/usr/bin/soffice", "/usr/bin/libreoffice"):
            if Path(cand).exists():
                soffice = cand
                break
    if not soffice:
        print("warning: no soffice found; PDF not rendered")
        return None
    subprocess.run(
        [soffice, "--headless", "--convert-to", "pdf",
         "--outdir", str(BUILD), str(BUILD / "manuscript_final.docx")],
        check=True, capture_output=True, timeout=300)
    return pdf if pdf.exists() else None


def main():
    missing = [p.name for p in REQUIRED if not p.exists()]
    if missing:
        raise SystemExit(
            f"missing required outputs: {missing} — run `make manuscript-results package` after a build"
        )
    abstract = write_abstract()
    render_pdf()
    if PKG.exists():
        shutil.rmtree(PKG)
    (PKG / "figures").mkdir(parents=True)
    (PKG / "tables").mkdir(exist_ok=True)
    (PKG / "qc").mkdir(exist_ok=True)
    for src in FLAT_FILES:
        if src.exists():
            shutil.copy2(src, PKG / src.name)
    shutil.copy2(abstract, PKG / "abstract.txt")
    for name in QC_BUNDLE:
        src = ROOT / "qc" / name
        if src.exists():
            shutil.copy2(src, PKG / "qc" / name)
    for src in sorted((ROOT / "figures").glob("fig*.png")):
        shutil.copy2(src, PKG / "figures" / src.name)
    for src in sorted((ROOT / "tables").glob("table*.csv")):
        shutil.copy2(src, PKG / "tables" / src.name)
    if not list((PKG / "figures").iterdir()) or not list((PKG / "tables").iterdir()):
        raise SystemExit("no figures or tables copied — run `make figures tables` first")
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(PKG.rglob("*")):
            if f.is_file() and f != ZIP:
                z.write(f, f.relative_to(PKG))
    print(ZIP)


if __name__ == "__main__":
    main()
