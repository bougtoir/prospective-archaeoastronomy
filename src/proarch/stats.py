"""Summary statistics: Wilson CIs, error quantiles, failure rates."""
import numpy as np
import pandas as pd
from scipy import stats as _st


def wilson_ci(k, n, alpha=0.05):
    if n == 0:
        return (np.nan, np.nan, np.nan)
    z = _st.norm.ppf(1 - alpha / 2)
    p = k / n
    den = 1 + z ** 2 / n
    c = (p + z ** 2 / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2)) / den
    return p, max(0.0, c - h), min(1.0, c + h)


def summarize_errors(err_deg, valid):
    """err_deg: angular errors (deg); valid: bool mask of valid solutions."""
    err = np.asarray(err_deg)
    ok = np.asarray(valid)
    n = len(err)
    n_valid = int(ok.sum())
    ev = err[ok]
    row = {
        "n_mc": n,
        "n_valid": n_valid,
        "p_invalid": 1.0 - n_valid / n if n else np.nan,
    }
    for thr in (0.1, 1.0, 5.0):
        k = int((err[ok] < thr).sum())
        p, lo, hi = wilson_ci(k, n)
        row[f"p_err<{thr}deg"] = p
        row[f"p_err<{thr}deg_lo"] = lo
        row[f"p_err<{thr}deg_hi"] = hi
    if n_valid:
        row.update({
            "median_err_deg": float(np.median(ev)),
            "iqr_err_deg": float(np.percentile(ev, 75) - np.percentile(ev, 25)),
            "mean_err_deg": float(np.mean(ev)),
            "p95_err_deg": float(np.percentile(ev, 95)),
            "p_catastrophic": float((err > 30.0).sum() / n),
        })
    else:
        row.update({"median_err_deg": np.nan, "iqr_err_deg": np.nan,
                    "mean_err_deg": np.nan, "p95_err_deg": np.nan,
                    "p_catastrophic": 1.0})
    return row


def summarize_frame(df, by):
    """df: per-replication results with 'err_deg','success'; group + summarize."""
    rows = []
    for keys, g in df.groupby(list(by)):
        row = dict(zip(by, keys if isinstance(keys, tuple) else (keys,)))
        row.update(summarize_errors(g["err_deg"].values, g["success"].values))
        rows.append(row)
    return pd.DataFrame(rows)


def pareto_front(df, cost_col="bits", perf_col="p_err<1.0deg",
                 err_col="mean_err_deg"):
    """Nondominated designs: minimize bits and error, maximize performance."""
    pts = df[[cost_col, perf_col, err_col]].values
    obj = np.column_stack([pts[:, 0], -pts[:, 1], pts[:, 2]])
    keep = np.ones(len(df), bool)
    for i in range(len(df)):
        for j in range(len(df)):
            if i == j:
                continue
            if np.all(obj[j] <= obj[i]) and np.any(obj[j] < obj[i]):
                keep[i] = False
                break
    return df[keep]
