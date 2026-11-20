"""Information-cost model for a stored encoding record.

B(S) = source-ID cost + relational-value cost + chirality cost + metadata cost

- source-ID cost: ceil(log2(N_catalogue)) bits per source; N_catalogue is a
  configurable parameter (default 2**40 for a Gaia-scale source index).
- relational-value cost: `bits` per stored cosine (each b_i and each stored
  edge weight).
- chirality cost: index triples (~3*log2(n)) + 1 sign bit each.
- metadata cost: fixed METADATA_BITS per record.
"""
import numpy as np

METADATA_BITS = 128
SOURCE_ID_BITS = 40  # log2 of catalogue size (~1e12 addresses a Gaia-scale index)


def bit_cost(n_sources, n_edges=0, n_chirality=0, bits=32,
             source_id_bits=SOURCE_ID_BITS, metadata_bits=METADATA_BITS):
    ids = n_sources * source_id_bits
    rel = (n_sources + n_edges) * bits          # b_i plus edge weights
    ch = n_chirality * (3 * int(np.ceil(np.log2(max(n_sources, 2)))) + 1)
    return ids + rel + ch + metadata_bits


def cost_for_encoding(rec, bits=32, **kw):
    return bit_cost(n_sources=rec["n"],
                    n_edges=len(rec.get("edges", [])),
                    n_chirality=len(rec.get("chirality", [])),
                    bits=bits, **kw)
