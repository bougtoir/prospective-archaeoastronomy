#!/usr/bin/env python3
"""Fetch real catalogues (ICRF3, ATNF pulsars, Gaia bright-star sample).

SMPT revision: the Gaia sample is taken in HEALPix-order source_id slices
(TOP-N brightest per slice) so the pool covers the whole sky — the Gaia TAP
sync endpoint cannot run the full-table ORDER BY the old query needed.

Every fetch persists raw bytes under data/raw/ and appends to
data/acquisition_ledger.csv. Failures are logged, not fatal: the synthetic
pipeline is independent of them.
"""
import json
import sys
import time
import traceback
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from proarch import catalogs  # noqa

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "data" / "catalogue_status.json"

# Gaia source_id = (NESTED level-12 healpix id) << 35; ids span 0..12*4^12.
# NESTED ordering makes contiguous id ranges contiguous sky patches, and the
# TAP backend prunes partitions on a source_id range, so N contiguous ranges
# tile the whole sky with ~1/N scan cost per query.
HPX_TOTAL = 12 * 4**12
N_SLICES = 24
HPX_SLICE_W = HPX_TOTAL // N_SLICES
TOP_PER_SLICE = 100  # brightest sources kept per slice


def try_fetch(name, fn):
    try:
        df = fn()
        out = catalogs.save_processed(df, name)
        return {"status": "ok", "n": len(df), "file": str(out)}
    except Exception as e:
        traceback.print_exc()
        return {"status": "failed", "error": str(e)[:300]}


def _tap_sync(query, dest):
    import urllib.parse
    import urllib.request
    url = ("https://gea.esac.esa.int/tap-server/tap/sync?"
           + urllib.parse.urlencode({
               "REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "csv",
               "QUERY": query}))
    req = urllib.request.Request(url, headers={"User-Agent": "proarch/0.2"})
    with urllib.request.urlopen(req, timeout=300) as r:
        dest.write_bytes(r.read())
    return url


def fetch_gaia_bright():
    """Gaia DR3 bright-star pool: TOP-per-slice across the whole sky.

    Columns kept: source_id, ra, dec, parallax(+err), pmra/pmdec(+err),
    radial_velocity(+err), G mag, ruwe, astrometric_excess_noise,
    visibility_periods_used, astrometric_params_solved.
    """
    import io
    raw_dir = catalogs.RAW / f"gaia_slices_{pd.Timestamp.utcnow():%Y%m%d}"
    raw_dir.mkdir(parents=True, exist_ok=True)
    step = HPX_SLICE_W * 2**35
    frames = []
    first_url = None
    for s in range(N_SLICES):
        lo = s * step
        hi = (s + 1) * step if s < N_SLICES - 1 else HPX_TOTAL * 2**35
        q = ("SELECT TOP {top} source_id, ra, dec, parallax, parallax_error, "
             "pmra, pmra_error, pmdec, pmdec_error, radial_velocity, "
             "radial_velocity_error, phot_g_mean_mag, ruwe, "
             "astrometric_excess_noise, visibility_periods_used, "
             "astrometric_params_solved FROM gaiadr3.gaia_source "
             "WHERE source_id >= {lo} AND source_id < {hi} "
             "AND phot_g_mean_mag < 12 AND parallax > 0.1 "
             "AND pmra IS NOT NULL AND pmdec IS NOT NULL AND ruwe < 1.4 "
             "AND visibility_periods_used > 8 "
             "ORDER BY phot_g_mean_mag ASC").format(
                 top=TOP_PER_SLICE, lo=lo, hi=hi)
        dest = raw_dir / f"gaia_slice_{s:02d}.csv"
        url = _tap_sync(q, dest)
        first_url = first_url or url
        try:
            frames.append(pd.read_csv(io.BytesIO(dest.read_bytes())))
        except Exception:
            print(f"slice {s}: parse failed, skipped")
        time.sleep(1.0)
    # ledger: one row for the manifest + the first slice's URL
    manifest = raw_dir / "QUERY_MANIFEST.txt"
    manifest.write_text(first_url + "\n" + "\n".join(
        f.name for f in sorted(raw_dir.glob("gaia_slice_*.csv"))))
    catalogs.record(first_url, manifest,
                    "ESA Gaia Archive TAP sync; 24 contiguous source_id "
                    "ranges tiling the sky x TOP 100 brightest, G<12, "
                    "parallax>0.1 mas, ruwe<1.4, vis>8; public", "DR3")
    raw = pd.concat(frames, ignore_index=True)
    raw = raw.drop_duplicates("source_id")
    df = pd.DataFrame({
        "source_id": raw["source_id"].astype(str),
        "source_class": "star",
        "ra_deg": raw["ra"], "dec_deg": raw["dec"],
        "distance_optional": 1000.0 / raw["parallax"].clip(lower=0.01),
        "proper_motion_ra_optional": raw["pmra"],
        "proper_motion_dec_optional": raw["pmdec"],
        "radial_velocity_optional": raw["radial_velocity"],
        "parallax_mas": raw["parallax"],
        "pmra_masyr": raw["pmra"], "pmdec_masyr": raw["pmdec"],
        "radial_velocity_kms": raw["radial_velocity"],
        "phot_g_mean_mag": raw["phot_g_mean_mag"],
        "ruwe": raw["ruwe"],
        "astrometric_excess_noise": raw["astrometric_excess_noise"],
        "visibility_periods_used": raw["visibility_periods_used"],
        "astrometric_params_solved": raw["astrometric_params_solved"],
        "metadata_json_optional": raw["phot_g_mean_mag"].apply(
            lambda m: json.dumps({"phot_g_mean_mag": float(m)})),
    })
    return df


def main():
    status = {}
    status["icrf3"] = try_fetch("icrf3_quasars", catalogs.fetch_icrf3)
    status["atnf"] = try_fetch("atnf_pulsars", catalogs.fetch_atnf)
    status["gaia_dr3_bright"] = try_fetch("gaia_dr3_bright",
                                         fetch_gaia_bright)
    STATUS.parent.mkdir(exist_ok=True)
    STATUS.write_text(json.dumps(status, indent=2))
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
