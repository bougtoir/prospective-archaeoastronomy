"""Real-catalogue integration: fetch, standardize, persist, ledger.

Standard internal schema:
    source_id, source_class, ra_deg, dec_deg, distance_optional,
    proper_motion_ra_optional, proper_motion_dec_optional,
    radial_velocity_optional, metadata_json_optional

Every downloaded file is persisted under data/raw/ and recorded in
data/acquisition_ledger.csv (source URL, version/date, UTC fetch time,
local path, size, sha256, license/access note).
"""
import hashlib
import io
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

RAW = Path("data/raw")
PROC = Path("data/processed")
LEDGER = Path("data/acquisition_ledger.csv")

ICRF3_URL = ("https://datacenter.iers.org/products/reference-systems/"
             "celestial/icrf3/icrf3k.txt")


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def record(url, local, note="", version=""):
    size = Path(local).stat().st_size
    row = {"url": url, "local_path": str(local),
           "fetched_utc": datetime.now(timezone.utc).isoformat(),
           "version_or_date": version, "bytes": size,
           "sha256": _sha256(local), "license_access": note}
    if LEDGER.exists():
        df = pd.read_csv(LEDGER)
        df = df[df.local_path != str(local)]
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])
    df.to_csv(LEDGER, index=False)


def _download(url, dest):
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "proarch/0.1"})
    with urllib.request.urlopen(req, timeout=120) as r:
        dest.write_bytes(r.read())
    return dest


def fetch_icrf3(dest=None):
    """ICRF3 K-band source list (IERS data center)."""
    dest = dest or RAW / "icrf3k.txt"
    _download(ICRF3_URL, dest)
    record(ICRF3_URL, dest,
           "IERS Data Center, ICRF3 K-band catalogue; public")
    import re
    pat = re.compile(
        r"^(ICRF\s+\S+)\s+\S+\s+(?:D\s+)?"
        r"(\d{2})\s+(\d{2})\s+([\d.]+)\s+"
        r"([+-]?\d{2})\s+(\d{2})\s+([\d.]+)\s")
    rows = []
    for line in open(dest, errors="replace"):
        m = pat.match(line)
        if not m:
            continue
        name, rh, rm, rs, dd, dm, ds = m.groups()
        ra = 15.0 * (int(rh) + int(rm) / 60 + float(rs) / 3600)
        sgn = -1.0 if dd.startswith("-") else 1.0
        dec = sgn * (abs(int(dd)) + int(dm) / 60 + float(ds) / 3600)
        rows.append((name, "quasar", ra, dec))
    df = pd.DataFrame(rows, columns=["source_id", "source_class",
                                     "ra_deg", "dec_deg"])
    for c in ("distance_optional", "proper_motion_ra_optional",
              "proper_motion_dec_optional", "radial_velocity_optional"):
        df[c] = np.nan
    df["metadata_json_optional"] = json.dumps({"catalogue": "ICRF3-K"})
    return df


def fetch_atnf(dest=None):
    """ATNF Pulsar Catalogue positions via psrcat web query."""
    url = ("https://www.atnf.csiro.au/research/pulsar/psrcat/"
           "psrcat_help.html?type=normal#nohead_1&get_ephemeris=1")
    # The documented non-interactive endpoint:
    url = ("https://www.atnf.csiro.au/research/pulsar/psrcat/"
           "proc_form.php?version=1.71&JName=JName&RaJ=RaJ&DecJ=DecJ&"
           "startUserDefined=true&c1_val=&c2_val=&c3_val=&c4_val=&"
           "sort_attr=jname&sort_order=asc&condition=&"
           "pulsar_names=&ephemeris=long&coords_unit=raj/decj&"
           "radius=&coords_1=&coords_2=&style=Long+with+last+digit+error&"
           "no_value=*&fsize=3&x_axis=&x_scale=linear&y_axis=&"
           "y_scale=linear&state=query&table_bottom.x=50&table_bottom.y=30")
    dest = dest or RAW / "atnf_psrcat.txt"
    _download(url, dest)
    record(url, dest,
           "ATNF Pulsar Catalogue (psrcat web query); public")
    import re as _re
    tpat = _re.compile(r"([+-]?\d{2}:\d{2}:\d{2}(?:\.\d+)?)")
    rows = []
    for line in io.open(dest, errors="replace"):
        m = _re.match(r"\s*\d+\s+(J\S+)", line)
        if not m:
            continue
        times = tpat.findall(line)
        ra_s = next((t for t in times if not t.startswith(("+", "-"))),
                    None)
        dec_s = next((t for t in times if t.startswith(("+", "-"))), None)
        if ra_s is None or dec_s is None:
            continue
        try:
            rh, rm, rs = ra_s.split(":")
            dd, dm, ds = dec_s.split(":")
            ra = 15 * (int(rh) + int(rm) / 60 + float(rs) / 3600)
            sgn = -1 if dd.startswith("-") else 1
            dec = sgn * (abs(int(dd)) + int(dm) / 60 + float(ds) / 3600)
            rows.append((m.group(1), "pulsar", ra, dec))
        except Exception:
            continue
    df = pd.DataFrame(rows, columns=["source_id", "source_class",
                                     "ra_deg", "dec_deg"])
    for c in ("distance_optional", "proper_motion_ra_optional",
              "proper_motion_dec_optional", "radial_velocity_optional"):
        df[c] = np.nan
    df["metadata_json_optional"] = json.dumps({"catalogue": "ATNF"})
    return df


def save_processed(df, name):
    PROC.mkdir(parents=True, exist_ok=True)
    out = PROC / f"{name}.csv"
    df.to_csv(out, index=False)
    return out
