"""Reference-network architectures M1-M7, configuration-driven."""
import numpy as np

from . import populations


def build_population(spec, rng, geometry_kind="isotropic", optimize=False):
    """spec: dict class->count. Returns {'Q','labels','name'}."""
    pop = populations.make_population(spec, rng, geometry_kind)
    if optimize and pop["Q"].shape[0] >= 4:
        # oversample then D-optimal select
        big = populations.make_population(
            {k: v * 3 for k, v in spec.items()}, rng, "isotropic")
        n = pop["Q"].shape[0]
        sel = _d_optimal_per_class(big, n)
        pop = {"Q": big["Q"][sel], "labels": big["labels"][sel]}
    return pop


def _d_optimal_per_class(big, n):
    from .geometry import d_optimal_select
    return d_optimal_select(big["Q"], n)


ARCHITECTURES = {
    "M1_single_star": {"star": 1},
    "M2_star_triangle": {"star": 3},
    "M3_stars_10": {"star": 10},
    "M3_stars_20": {"star": 20},
    "M3_stars_50": {"star": 50},
    "M3_stars_100": {"star": 100},
    "M4_pulsars_10": {"pulsar": 10},
    "M4_pulsars_20": {"pulsar": 20},
    "M4_pulsars_50": {"pulsar": 50},
    "M5_quasars_10": {"quasar": 10},
    "M5_quasars_20": {"quasar": 20},
    "M5_quasars_50": {"quasar": 50},
    "M5_quasars_100": {"quasar": 100},
    "M6_galaxies_10": {"galaxy": 10},
    "M6_galaxies_20": {"galaxy": 20},
    "M6_galaxies_50": {"galaxy": 50},
    "M7_hybrid_pq": {"pulsar": 10, "quasar": 10},
    "M7_hybrid_spq": {"star": 10, "pulsar": 10, "quasar": 10},
    "M7_hybrid_all": {"star": 5, "pulsar": 5, "quasar": 10, "galaxy": 10},
}
