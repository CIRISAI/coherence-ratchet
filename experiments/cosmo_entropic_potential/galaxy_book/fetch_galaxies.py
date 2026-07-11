#!/usr/bin/env python3
"""
Fetch TNG300-1 group-catalog fields (GroupPos, Group_M_Crit200, GroupMassType[:,4]=stellar)
for all 26 frozen snapshots, keeping M200c > 3e10 Msun/h (low enough that all stellar-mass
rungs incl. 10^8.5 are complete). Fields-only ranged HDF5 reads via fsspec (API key from
~/.tng_api_key, never stored in the repo). Groups ~descending in FoF size -> scan chunks until
last-3-chunk max M200c < 1e10, then stop. Idempotent per snapshot. New files
tng300_galaxies_*.npz; does NOT overwrite the halo npz.
"""
import json, os, time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "large_volume" / "data"     # store alongside existing npz
SNAPS = [25, 30, 33, 36, 39, 42, 45, 47, 49, 51, 53, 55, 56, 59, 61,
         63, 65, 67, 70, 72, 74, 76, 79, 82, 87, 99]
THR_KEEP = 3e10          # Msun/h M200c floor (stellar completeness incl. 10^8.5 rung)
STOP_BELOW = 1e10        # stop when last-3-chunk max M200c < this
MAXCHUNK = 800

def fetch_snap(snap):
    import fsspec, h5py
    K = open(os.path.expanduser("~/.tng_api_key")).read().strip()
    outp = DATA / f"tng300_galaxies_{snap:03d}.npz"
    if outp.exists():
        return f"snap {snap}: cached"
    fs = fsspec.filesystem("http", headers={"API-Key": K}, block_size=2**22)
    url = lambda c: (f"https://www.tng-project.org/api/TNG300-1/files/"
                     f"groupcat-{snap}.{c}.hdf5")
    pos_l, m_l, ms_l = [], [], []
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
                                ms = f["Group"]["GroupMassType"][:, 4][keep] * 1e10
                                pos_l.append(p.astype(np.float32))
                                m_l.append(m[keep].astype(np.float32))
                                ms_l.append(ms.astype(np.float32))
                break
            except Exception as e:
                if attempt == 4:
                    raise RuntimeError(f"snap {snap} chunk {c}: {e}")
                time.sleep(2.0 * (attempt + 1))
        tail_max.append(m.max() if len(m) else 0.0)
        tail_max = tail_max[-3:]
        if len(tail_max) == 3 and max(tail_max) < STOP_BELOW:
            c += 1
            break
        c += 1
    pos = np.concatenate(pos_l) if pos_l else np.zeros((0, 3), np.float32)
    m200 = np.concatenate(m_l) if m_l else np.zeros(0, np.float32)
    mstar = np.concatenate(ms_l) if ms_l else np.zeros(0, np.float32)
    np.savez_compressed(outp, pos=pos, m200=m200, mstar=mstar, z=z, a=a,
                        chunks_read=c, snap=snap, thr_keep=THR_KEEP)
    return (f"snap {snap}: z={z:.3f} kept {len(m200)} groups >3e10 "
            f"(M*>=1.1e9: {int((mstar>1.1e9).sum())}; M*>=3.16e8: {int((mstar>10**8.5).sum())}) "
            f"in {c} chunks [{time.time()-t0:.0f}s]")

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=10) as ex:
        for msg in ex.map(fetch_snap, SNAPS):
            print(msg, flush=True)
    man = {}
    for s in SNAPS:
        d = np.load(DATA / f"tng300_galaxies_{s:03d}.npz")
        ms = d["mstar"]; m2 = d["m200"]
        man[s] = dict(z=float(d["z"]), a=float(d["a"]), n_kept=int(len(m2)),
                      chunks=int(d["chunks_read"]),
                      n_Mstar={lbl: int((ms > v).sum()) for lbl, v in
                               [("8.5", 10**8.5), ("9.04(1.1e9)", 1.1e9),
                                ("9.5", 10**9.5), ("10.0", 1e10)]},
                      min_M200_of_Mstar1p1e9=float(m2[ms > 1.1e9].min()) if (ms > 1.1e9).any() else None,
                      min_M200_of_Mstar3e8=float(m2[ms > 10**8.5].min()) if (ms > 10**8.5).any() else None,
                      fetch_floor_M200=3e10)
    with open(HERE / "fetch_manifest.json", "w") as fh:
        json.dump(man, fh, indent=1)
    print("manifest written", flush=True)
