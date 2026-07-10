#!/usr/bin/env python3
"""
Fetch TNG300-1 group-catalog fields (GroupPos, Group_M_Crit200) for halos with
M200c > 1e11 Msun/h at the 10 frozen snapshots. Fields-only ranged HDF5 reads
via fsspec (API key from ~/.tng_api_key, never stored in the repo). Groups are
ordered ~descending in FoF size, so we scan chunks until the running max M200c
over the last 3 chunks falls below THR_KEEP/3, then stop. Idempotent: skips
snapshots whose .npz already exists. One process per snapshot (per-connection
throttle => parallel connections; see memory note on TNG access).
"""
import json, os, sys, time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
DATA.mkdir(exist_ok=True)
SNAPS = [25, 30, 36, 42, 49, 56, 65, 76, 87, 99]
THR_KEEP = 1e11          # Msun/h; keep everything above this
MARGIN = 3.0             # stop when last-3-chunk max M200c < THR_KEEP/MARGIN
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
                        nfiles = int(h["NumFiles"])
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
    with ProcessPoolExecutor(max_workers=10) as ex:
        for msg in ex.map(fetch_snap, SNAPS):
            print(msg, flush=True)
    # manifest
    man = {}
    for s in SNAPS:
        d = np.load(DATA / f"tng300_groups_{s:03d}.npz")
        man[s] = dict(z=float(d["z"]), a=float(d["a"]),
                      n_kept=int(len(d["m200"])), chunks=int(d["chunks_read"]),
                      counts={t: int((d["m200"] > float(t)).sum())
                              for t in ("2e11", "5e11", "1e12", "2e12",
                                        "5e12", "1e13")})
    # python floats in keys above: fix by explicit map
    for s in man:
        d = np.load(DATA / f"tng300_groups_{s:03d}.npz")
        man[s]["counts"] = {lbl: int((d["m200"] > v).sum()) for lbl, v in
                            [("2e11", 2e11), ("5e11", 5e11), ("1e12", 1e12),
                             ("2e12", 2e12), ("5e12", 5e12), ("1e13", 1e13)]}
    with open(HERE / "fetch_manifest.json", "w") as fh:
        json.dump(man, fh, indent=1)
    print("manifest written")
