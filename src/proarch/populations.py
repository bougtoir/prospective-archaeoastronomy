"""Synthetic celestial source populations.

Each source class has a direction distribution and scenario-based usability
parameters. No astrophysical survival function is fabricated; usability curves
are scenario assumptions declared in the manuscript.
"""
import numpy as np

from . import geometry

CLASSES = ("star", "pulsar", "quasar", "galaxy", "galaxy_cluster")


def sample_population(cls, n, rng, geometry_kind="isotropic"):
    """Return (n,3) unit directions for a source class."""
    kind = geometry_kind
    if kind == "isotropic":
        q = geometry.sample_isotropic(n, rng)
    elif kind == "clustered":
        q = geometry.sample_clustered(n, rng)
    elif kind == "banded":
        q = geometry.sample_banded(n, rng)
    else:
        raise ValueError(kind)
    return q


def make_population(counts, rng, geometry_kind="isotropic"):
    """counts: dict class->n. Returns dict of arrays + labels."""
    dirs, labels = [], []
    for cls, n in counts.items():
        if n <= 0:
            continue
        dirs.append(sample_population(cls, n, rng, geometry_kind))
        labels += [cls] * n
    Q = np.vstack(dirs)
    return {"Q": Q, "labels": np.array(labels)}
