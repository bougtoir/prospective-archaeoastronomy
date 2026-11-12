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
import re
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

# Extended schema used by the SMPT revision: the calibrated pipeline keeps
# extra per-source measurement columns alongside the base schema.
EXTRA_COLS = ("pm_tot_masyr", "defining_flag", "ra_unc_s", "dec_unc_arcsec",
              "corr_radec", "mjd_first", "mjd_last", "n_sessions",
              "p0_s", "p1_ss", "age_yr", "dist_kpc", "dist1_kpc",
              "parallax_mas", "pmra_masyr", "pmdec_masyr",
              "radial_velocity_kms", "phot_g_mean_mag", "ruwe",
              "astrometric_excess_noise", "visibility_periods_used",
              "astrometric_params_solved")


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
    """ICRF3 K-band source list (IERS data center).

    Full-column parse for the SMPT revision: defining-source flag,
    formal position uncertainties, RA-Dec correlation, mean/first/last
    observation MJD, and session/delay/rate counts.
    """
    dest = dest or RAW / "icrf3k.txt"
    if not dest.exists():
        _download(ICRF3_URL, dest)
        record(ICRF3_URL, dest,
               "IERS Data Center, ICRF3 K-band catalogue; public",
               "K-band, Charlot et al. 2020")
    pat = re.compile(
        r"^(ICRF\s+\S+)\s+(\S+)\s+(D\s+)?"
        r"(\d{2})\s+(\d{2})\s+([\d.]+)\s+"
        r"([+-]?\d{2})\s+(\d{2})\s+([\d.]+)\s+"
        r"([\d.]+)\s+([\d.]+)\s+([+-]?[\d.]+)\s+"
        r"([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+"
        r"(\d+)\s+(\d+)\s+(\d+)")
    rows = []
    for line in open(dest, errors="replace"):
        m = pat.match(line)
        if not m:
            continue
        (name, iers, dflag, rh, rm, rs, dd, dm, ds,
         ura, udec, corr, mean_mjd, first_mjd, last_mjd,
         n_sess, n_del, n_rat) = m.groups()
        ra = 15.0 * (int(rh) + int(rm) / 60 + float(rs) / 3600)
        sgn = -1.0 if dd.startswith("-") else 1.0
        dec = sgn * (abs(int(dd)) + int(dm) / 60 + float(ds) / 3600)
        rows.append((name, "quasar", ra, dec, bool(dflag),
                     float(ura), float(udec), float(corr),
                     float(first_mjd), float(last_mjd), int(n_sess)))
    df = pd.DataFrame(rows, columns=[
        "source_id", "source_class", "ra_deg", "dec_deg",
        "defining_flag", "ra_unc_s", "dec_unc_arcsec", "corr_radec",
        "mjd_first", "mjd_last", "n_sessions"])
    for c in ("distance_optional", "proper_motion_ra_optional",
              "proper_motion_dec_optional", "radial_velocity_optional"):
        df[c] = np.nan
    df["metadata_json_optional"] = df.apply(
        lambda r: json.dumps({"catalogue": "ICRF3-K",
                              "iers_des": str(r.name)}), axis=1)
    return df


def fetch_atnf(dest=None):
    """ATNF Pulsar Catalogue via psrcat proc_form, short column format.

    Requests JName, RAJ, DecJ, P0, P1, PMRA, PMDec, PMTot, Age, Dist, Dist1
    in whitespace-separated columns with '*' marking missing values, so the
    parse is column-order based (no positional guessing). Missingness is
    preserved as NaN and reported downstream, never imputed silently.
    """
    url = ("https://www.atnf.csiro.au/research/pulsar/psrcat/"
           "proc_form.php?version=1.71&JName=JName&RaJ=RaJ&DecJ=DecJ&"
           "P0=P0&P1=P1&PMRA=PMRA&PMDec=PMDec&PMTot=PMTot&Age=Age&"
           "Dist=Dist&Dist1=Dist1&"
           "startUserDefined=true&c1_val=&c2_val=&c3_val=&c4_val=&"
           "sort_attr=jname&sort_order=asc&condition=&"
           "pulsar_names=&ephemeris=long&coords_unit=raj/decj&"
           "radius=&coords_1=&coords_2=&style=Short+without+errors&"
           "no_value=*&fsize=3&x_axis=&x_scale=linear&y_axis=&"
           "y_scale=linear&state=query&table_bottom.x=50&table_bottom.y=30")
    dest = dest or RAW / "atnf_psrcat_short.txt"
    if not dest.exists():
        _download(url, dest)
        record(url, dest,
               "ATNF Pulsar Catalogue (psrcat proc_form, short columns); "
               "public", "v1.71")

    def _f(x):
        return np.nan if x == "*" else float(x)

    def _hms(s):
        parts = (s.split(":") + ["0", "0"])[:3]
        return (int(parts[0]) + int(parts[1]) / 60 + float(parts[2]) / 3600)

    hms = r"\d{2}(?::\d{2})?(?::\d{2}(?:\.\d+)?)?"
    pat = re.compile(
        r"^\s*\d+\s+(J\S+)\s+(" + hms + r")\s+"
        r"([+-]?" + hms + r")\s+"
        r"(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)")
    rows = []
    for line in io.open(dest, errors="replace"):
        m = pat.match(line)
        if not m:
            continue
        (name, ra_s, dec_s, p0, p1, pmra, pmdec, pmtot,
         age, dist, dist1) = m.groups()
        try:
            ra = 15 * _hms(ra_s)
            sgn = -1 if dec_s.startswith("-") else 1
            dec = sgn * _hms(dec_s.lstrip("+-"))
            rows.append((name, "pulsar", ra, dec,
                         _f(p0), _f(p1), _f(pmra), _f(pmdec), _f(pmtot),
                         _f(age), _f(dist), _f(dist1)))
        except Exception:
            continue
    df = pd.DataFrame(rows, columns=[
        "source_id", "source_class", "ra_deg", "dec_deg",
        "p0_s", "p1_ss", "pmra_masyr", "pmdec_masyr", "pm_tot_masyr",
        "age_yr", "dist_kpc", "dist1_kpc"])
    df["distance_optional"] = df["dist1_kpc"].fillna(df["dist_kpc"]) * 1e3
    df["proper_motion_ra_optional"] = df["pmra_masyr"]
    df["proper_motion_dec_optional"] = df["pmdec_masyr"]
    df["radial_velocity_optional"] = np.nan
    df["metadata_json_optional"] = json.dumps({"catalogue": "ATNF", "v": "1.71"})
    return df


def save_processed(df, name):
    PROC.mkdir(parents=True, exist_ok=True)
    out = PROC / f"{name}.csv"
    df.to_csv(out, index=False)
    return out
