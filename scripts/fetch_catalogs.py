#!/usr/bin/env python3
"""Fetch real catalogues (ICRF3, ATNF pulsars, Gaia bright-star sample).

Every fetch persists raw bytes under data/raw/ and appends to
data/acquisition_ledger.csv. Failures are logged, not fatal: the synthetic
pipeline is independent of them.
"""
import json
import sys
import traceback
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from proarch import catalogs  # noqa

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "data" / "catalogue_status.json"


def try_fetch(name, fn):
    try:
        df = fn()
        out = catalogs.save_processed(df, name)
        return {"status": "ok", "n": len(df), "file": str(out)}
    except Exception as e:
        traceback.print_exc()
        return {"status": "failed", "error": str(e)[:300]}


def fetch_gaia_bright():
    """Gaia DR3 bright-star sample via the ESA archive TAP sync endpoint."""
    import urllib.parse
    import urllib.request
    from io import StringIO

    query = ("SELECT TOP 200 source_id, ra, dec, parallax, "
             "pmra, pmdec, radial_velocity, phot_g_mean_mag "
             "FROM gaiadr3.gaia_source WHERE phot_g_mean_mag < 6 "
             "ORDER BY phot_g_mean_mag ASC")
    url = ("https://gea.esac.esa.int/tap-server/tap/sync?"
           + urllib.parse.urlencode({
               "REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "csv",
               "QUERY": query}))
    dest = catalogs.RAW / "gaia_dr3_bright.csv"
    catalogs.RAW.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "proarch/0.1"})
    with urllib.request.urlopen(req, timeout=180) as r:
        dest.write_bytes(r.read())
    catalogs.record(url, dest,
                    "ESA Gaia Archive TAP sync query; public", "DR3")
    raw = pd.read_csv(StringIO(dest.read_text()))
    df = pd.DataFrame({
        "source_id": raw["source_id"].astype(str),
        "source_class": "star",
        "ra_deg": raw["ra"], "dec_deg": raw["dec"],
        "distance_optional": 1000.0 / raw["parallax"].clip(lower=0.01),
        "proper_motion_ra_optional": raw["pmra"],
        "proper_motion_dec_optional": raw["pmdec"],
        "radial_velocity_optional": raw["radial_velocity"],
        "metadata_json_optional": raw["phot_g_mean_mag"].apply(
            lambda m: json.dumps({"phot_g_mean_mag": float(m)})),
    })
    return df


def main():
    status = {}
    status["icrf3"] = try_fetch("icrf3_quasars", catalogs.fetch_icrf3)
    status["atnf"] = try_fetch("atnf_pulsars", catalogs.fetch_atnf)
    status["gaia_dr3_bright"] = try_fetch("gaia_dr3_bright", fetch_gaia_bright)
    STATUS.parent.mkdir(exist_ok=True)
    STATUS.write_text(json.dumps(status, indent=2))
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
