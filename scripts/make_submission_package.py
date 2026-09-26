"""Assemble submission_package/ and ACTA_submission_package.zip from the
current generated outputs. Run after `make all` so the package always
carries the latest numbers/figures.
"""
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "manuscript" / "build"
PKG = ROOT / "submission_package"
ZIP = PKG / "ACTA_submission_package.zip"

FLAT_FILES = [
    BUILD / "manuscript_final.docx",
    BUILD / "manuscript_inline.docx",
    ROOT / "manuscript" / "highlights.md",
    ROOT / "manuscript" / "cover_letter.md",
    ROOT / "manuscript" / "declarations.md",
    ROOT / "manuscript" / "supplementary.md",
    ROOT / "manuscript" / "references.bib",
    ROOT / "manuscript" / "graphical_abstract.png",
    ROOT / "manuscript" / "ACTA_ASTRONAUTICA_GUIDE_AUDIT.md",
]


REQUIRED = [
    BUILD / "manuscript_final.docx",
    BUILD / "manuscript_inline.docx",
]


def main():
    missing = [p.name for p in REQUIRED if not p.exists()]
    if missing:
        raise SystemExit(
            f"missing required outputs: {missing} — run `make manuscript-results package` after a build"
        )
    if PKG.exists():
        shutil.rmtree(PKG)
    (PKG / "figures").mkdir(parents=True)
    (PKG / "tables").mkdir(exist_ok=True)
    for src in FLAT_FILES:
        if src.exists():
            shutil.copy2(src, PKG / src.name)
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
