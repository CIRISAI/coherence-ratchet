#!/usr/bin/env python3
"""
fine_grid: fetch TNG300-1 group fields for the 16 NEW dense-grid snapshots.
Identical fetch logic to ../fetch_tng300.py (fields-only ranged HDF5 reads via
fsspec, API key from ~/.tng_api_key, never stored). Writes npz into ../data/
with the SAME naming (tng300_groups_NNN.npz); idempotent (skips existing).
Disk-tight: fields-only, npz_compressed, block_size 2^22 (no full-file cache).
"""
import json, os, time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"          # SHARED data dir with the 10 original npz
DATA.mkdir(exist_ok=True)
NEW_SNAPS = [33, 39, 45, 47, 51, 53, 55, 59, 61, 63, 67, 70, 72, 74, 79, 82]
THR_KEEP = 1e11
MARGIN = 3.0
MAXCHUNK = 600

def fetch_snap(snap):
    import fsspec, h5py
    K = open(os.path.expanduser("~/.tng_api_key")).read().strip()
    outp = DATA / f"tng300_groups_{snap:03d}.npz"
    if outp.exists():
        return f"snap {snap}: cached"
    fs = fsspec.filesystem("http", headers={"API-Key": K}, block_size=2**22)
    url = lambda c: (f"https://www.tng-project.org/api/TNG300-1/files/"
                     f"groupcat-{snap}.{c}.hdf5")
    pos_l, m_l = [], []
    tail_max = []
    z = a = None
    t0 = time.time()
    c = 0
    while c < MAXCHUNK:
        for attempt in range(5):
            try:
                with h5py.File(fs.open(url(c), "rb"), "r") as f:
                    if z is None:
                        h = dict(f["Header"].attrs)
                        z = float(h["Redshift"]); a = 1.0 / (1.0 + z)
                    if "Group" not in f or "Group_M_Crit200" not in f["Group"]:
                        m = np.zeros(0)
                    else:
                        m = f["Group"]["Group_M_Crit200"][:] * 1e10
                        if len(m):
                            keep = m > THR_KEEP
                            if keep.any():
                                p = f["Group"]["GroupPos"][:][keep] / 1e3
                                pos_l.append(p.astype(np.float32))
                                m_l.append(m[keep].astype(np.float32))
                break
            except Exception as e:
                if attempt == 4:
                    raise RuntimeError(f"snap {snap} chunk {c}: {e}")
                time.sleep(2.0 * (attempt + 1))
        tail_max.append(m.max() if len(m) else 0.0)
        tail_max = tail_max[-3:]
        if len(tail_max) == 3 and max(tail_max) < THR_KEEP / MARGIN:
            c += 1
            break
        c += 1
    pos = np.concatenate(pos_l) if pos_l else np.zeros((0, 3), np.float32)
    m200 = np.concatenate(m_l) if m_l else np.zeros(0, np.float32)
    np.savez_compressed(outp, pos=pos, m200=m200, z=z, a=a,
                        chunks_read=c, snap=snap)
    return (f"snap {snap}: z={z:.3f} kept {len(m200)} halos >1e11 "
            f"in {c} chunks [{time.time()-t0:.0f}s]")

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=8) as ex:
        for msg in ex.map(fetch_snap, NEW_SNAPS):
            print(msg, flush=True)
    THR = 742530285568.0
    man = {}
    for s in NEW_SNAPS:
        d = np.load(DATA / f"tng300_groups_{s:03d}.npz")
        man[s] = dict(z=float(d["z"]), a=float(d["a"]),
                      n_kept=int(len(d["m200"])), chunks=int(d["chunks_read"]),
                      k_at_frozen_thr=int((d["m200"] > THR).sum()))
    with open(HERE / "fetch_manifest_fine.json", "w") as fh:
        json.dump(man, fh, indent=1)
    print("manifest written:", json.dumps(man, indent=1))
