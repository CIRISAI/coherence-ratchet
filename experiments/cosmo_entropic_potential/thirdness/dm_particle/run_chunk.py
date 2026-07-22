#!/usr/bin/env python3
"""Run fetch_grid.worker for a single chunk index (one process per chunk, no pool).

  P4_SIM=TNG100-3 P4_SNAP=99 python3 run_chunk.py 3

Resumable: a partial part_*.npz is picked up at its flushed particle count and the
per-particle deviate stream is replayed so the nested subsamples stay identical.
"""
import sys
import fetch_grid as F

if __name__ == "__main__":
    print(F.worker(int(sys.argv[1])), flush=True)
