#!/usr/bin/env python3
"""Build manuscript_omml.docx: prose identical to manuscript_final.md;
known math expressions are converted to native Word OMML equations.
"""
import re
from pathlib import Path

from docx import Document
from docx.shared import Pt
from latex2mathml.converter import convert as latex_to_mathml
from docx_equation import mathml_to_omml

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "manuscript" / "build" / "manuscript_final.md"
OUT = ROOT / "manuscript" / "build" / "manuscript_omml.docx"

# Ordered rules: (regex, replacement latex template). Longest first.
RULES = [
    (r"n_hat = argmin_\{\|\|n\|\|=1\} \|\|Q_obs n - b\|\|\^2",
     r"\hat{n} = \arg\min_{\|n\|=1} \|Q_{\mathrm{obs}}\, n - b\|^{2}"),
    (r"eps_theta = arccos\(n_hat\^T N0\)",
     r"\varepsilon_{\theta} = \arccos(\hat{n}^{T} N_{0})"),
    (r"S_k\(t\) = exp\(-\(t/tau_k\)\^a_k\)",
     r"S_{k}(t) = \exp(-(t/\tau_{k})^{a_{k}})"),
    (r"N0 = L_Earth\(t0\)/\|\|L_Earth\(t0\)\|\|",
     r"N_{0} = L_{\mathrm{Earth}}(t_{0}) \,/\, \|L_{\mathrm{Earth}}(t_{0})\|"),
    (r"Q = \[q_1\^T; \.\.\.; q_n\^T\]",
     r"Q = [q_{1}^{T};\; \ldots;\; q_{n}^{T}]"),
    (r"H_ijk = sign\(det\(q_i, q_j, q_k\)\)",
     r"H_{ijk} = \mathrm{sign}(\det(q_{i}, q_{j}, q_{k}))"),
    (r"b_i = q_i\^T N0", r"b_{i} = q_{i}^{T} N_{0}"),
    (r"b = Q N0", r"b = Q\, N_{0}"),
    (r"G = Q Q\^T", r"G = Q\, Q^{T}"),
    (r"G_ij = cos\(theta_ij\)", r"G_{ij} = \cos(\theta_{ij})"),
    (r"det\(O\) = -1", r"\det(O) = -1"),
    (r"kappa\(Q\^T Q\)", r"\kappa(Q^{T} Q)"),
    (r"P\(eps_theta < 1 ?deg\)", r"P(\varepsilon_{\theta} < 1\,\mathrm{deg})"),
    (r"P\(eps ?< ?1 ?deg\)", r"P(\varepsilon < 1\,\mathrm{deg})"),
    (r"P\(<1 ?deg\)", r"P(\varepsilon < 1\,\mathrm{deg})"),
    (r"log10\(t/yr\)", r"\log_{10}(t/\mathrm{yr})"),
    (r"log det", r"\log\,\det"),
    (r"B\(S\)", r"B(S)"),
    # token = value constructs
    (r"(sigma_obs|p_mismatch|p_invalid|N_MC|n_total|n_mc|tau_k|n)\s*"
     r"(>=|<=|=|<|>)\s*([0-9][0-9.,;e^+-]*(?:\s*(?:yr|rad|deg))?)",
     "__TOKVAL__"),
    (r"\bt = 10\^(\d+) ?yr", r"t = 10^{\1}\,\mathrm{yr}"),
    (r"\b([ntcP]) ?(>=|<=|=|<|>) ?([0-9][0-9.,;]*)", r"\1 \2 \3"),
    (r"\bL_Earth\(t0\)", r"L_{\mathrm{Earth}}(t_{0})"),
    # scientific notation
    (r"(?<![\w.])(\d+)e(-?\d+)(?![\w.])", r"\1 \times 10^{\2}"),
    (r"10\^(\d+)", r"10^{\1}"),
    # standalone identifier tokens
    (r"\beps_theta\b", r"\varepsilon_{\theta}"),
    (r"\bsigma_obs\b", r"\sigma_{\mathrm{obs}}"),
    (r"\bp_mismatch\b", r"p_{\mathrm{mismatch}}"),
    (r"\bp_invalid\b", r"p_{\mathrm{invalid}}"),
    (r"\bn_total\b", r"n_{\mathrm{tot}}"),
    (r"\bN_MC\b", r"N_{\mathrm{MC}}"),
    (r"\bn_mc\b", r"n_{\mathrm{mc}}"),
    (r"\bL_Earth\b", r"L_{\mathrm{Earth}}"),
    (r"\bQ_obs\b", r"Q_{\mathrm{obs}}"),
    (r"\bn_hat\b", r"\hat{n}"),
    (r"\bS_k\b", r"S_{k}"),
    (r"\btau_k\b", r"\tau_{k}"),
    (r"\ba_k\b", r"a_{k}"),
    (r"\bG_ij\b", r"G_{ij}"),
    (r"\bH_ijk\b", r"H_{ijk}"),
    (r"\btheta_ij\b", r"\theta_{ij}"),
    (r"\bN0\b", r"N_{0}"),
    (r"\bt0\b", r"t_{0}"),
    (r"\bq_i\b", r"q_{i}"),
    (r"\bq_j\b", r"q_{j}"),
    (r"\bq_k\b", r"q_{k}"),
    (r"\bq_1\b", r"q_{1}"),
    (r"\bq_n\b", r"q_{n}"),
    (r"\bb_i\b", r"b_{i}"),
    (r"\bchi\b", r"\chi"),
]
TOKMAP = {
    "sigma_obs": r"\sigma_{\mathrm{obs}}",
    "p_mismatch": r"p_{\mathrm{mismatch}}",
    "p_invalid": r"p_{\mathrm{invalid}}",
    "N_MC": r"N_{\mathrm{MC}}",
    "n_total": r"n_{\mathrm{tot}}",
    "n_mc": r"n_{\mathrm{mc}}",
    "tau_k": r"\tau_{k}",
    "n": r"n",
}
UNITMAP = {"yr": r"\,\mathrm{yr}", "rad": r"\,\mathrm{rad}",
           "deg": r"\,\mathrm{deg}"}


def tokval(m):
    tok, op, val = m.group(1), m.group(2), m.group(3)
    val_lx = re.sub(r"(\d+)e(-?\d+)",
                    lambda m: rf"{m.group(1)}\times10^{{{m.group(2)}}}", val)
    val_lx = re.sub(r"10\^(\d+)",
                    lambda m: rf"10^{{{m.group(1)}}}", val_lx)
    for w, lx in UNITMAP.items():
        val_lx = re.sub(rf"\s*{w}\b", lambda m, lx=lx: lx, val_lx)
    op_lx = {"=": "=", "<": "<", ">": ">",
             ">=": r"\geq", "<=": r"\leq"}[op]
    return f"{TOKMAP[tok]} {op_lx} {val_lx.strip()}"


COMPILED = [(re.compile(p), r) for p, r in RULES]


def split_math(text):
    """Return list of ('text'|'math', content-or-latex)."""
    out, pos = [], 0
    n = len(text)
    while pos < n:
        best = None
        for pat, tmpl in COMPILED:
            mm = pat.search(text, pos)
            if mm and (best is None or mm.start() < best[0] or
                       (mm.start() == best[0] and
                        mm.end() > best[1])):
                best = (mm.start(), mm.end(), tmpl, mm)
        if best is None:
            out.append(("text", text[pos:]))
            break
        s, e, tmpl, mm = best
        if s > pos:
            out.append(("text", text[pos:s]))
        if tmpl == "__TOKVAL__":
            lx = tokval(mm)
        else:
            lx = tmpl
            for g in range(mm.re.groups, 0, -1):
                lx = lx.replace(f"\\{g}", mm.group(g) or "")
        out.append(("math", lx))
        pos = e
    return out


ITALIC = re.compile(r"\*([^*\n]+)\*")


def add_plain(p, seg):
    last = 0
    for m in ITALIC.finditer(seg):
        if m.start() > last:
            p.add_run(seg[last:m.start()])
        p.add_run(m.group(1)).italic = True
        last = m.end()
    if last < len(seg):
        p.add_run(seg[last:])


def main():
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(12)
    problems = []
    for line in SRC.read_text().splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("# "):
            p = doc.add_heading(s[2:], 0)
        elif s.startswith("## "):
            p = doc.add_heading(s[3:], 1)
        elif s.startswith("### "):
            p = doc.add_heading(s[4:], 2)
        elif re.match(r"^[-*] ", s):
            p = doc.add_paragraph(style="List Bullet")
            s = s[2:]
        else:
            p = doc.add_paragraph()
        for kind, seg in split_math(s):
            if kind == "text":
                add_plain(p, seg)
            else:
                try:
                    omml = mathml_to_omml(latex_to_mathml(seg))
                    p._element.append(omml)
                except Exception as exc:
                    problems.append((seg, str(exc)))
                    p.add_run(seg)
    doc.save(OUT)
    print("wrote", OUT)
    for seg, e in problems:
        print("FALLBACK", repr(seg), e)


if __name__ == "__main__":
    main()
