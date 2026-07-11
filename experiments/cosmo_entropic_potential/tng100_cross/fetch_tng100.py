#!/usr/bin/env python3
"""
Fetch TNG100-1 group-catalog fields (GroupPos, Group_M_Crit200) for halos with
M200c > 1e10 Msun/h at the 10 frozen snapshots. Fields-only ranged HDF5 reads
via fsspec (API key from ~/.tng_api_key, never stored anywhere). Mirror of
../large_volume/fetch_tng300.py with two TNG100-specific changes, both documented
in DECISIONS.md before this ran:
  - THR_KEEP lowered to 1e10 (lower box mass floor; rule reaches deeper).
  - stop heuristic FIX for TNG100's 448-chunk, empty-massive-end layout: the
    last-3 tail is over NON-EMPTY chunks only and the stop is armed only after the
    first kept halo. (The TNG300 heuristic would false-stop on empty early chunks.)
Idempotent: skips snapshots whose .npz already exists. One process per snapshot.
"""
import json, os, time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
DATA.mkdir(exist_ok=True)
SNAPS = [25, 30, 36, 42, 49, 56, 65, 76, 87, 99]
THR_KEEP = 1e10          # Msun/h; keep everything above this
MARGIN = 3.0             # stop when last-3 NON-EMPTY-chunk max M200c < THR_KEEP/MARGIN
MAXCHUNK = 448           # TNG100-1 NumFiles

def fetch_snap(snap):
    import fsspec, h5py
    K = open(os.path.expanduser("~/.tng_api_key")).read().strip()
    outp = DATA / f"tng100_groups_{snap:03d}.npz"
    if outp.exists():
        return f"snap {snap}: cached"
    fs = fsspec.filesystem("http", headers={"API-Key": K}, block_size=2**22)
    url = lambda c: (f"https://www.tng-project.org/api/TNG100-1/files/"
                     f"groupcat-{snap}.{c}.hdf5")
    pos_l, m_l = [], []
    tail_max = []            # over NON-EMPTY chunks only
    started = False          # armed only after first kept halo
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
                                started = True
                break
            except Exception as e:
                if attempt == 4:
                    raise RuntimeError(f"snap {snap} chunk {c}: {e}")
                time.sleep(2.0 * (attempt + 1))
        if len(m):                                  # non-empty chunk -> update tail
            tail_max.append(float(m.max()))
            tail_max = tail_max[-3:]
            if started and len(tail_max) == 3 and max(tail_max) < THR_KEEP / MARGIN:
                c += 1
                break
        c += 1
    pos = np.concatenate(pos_l) if pos_l else np.zeros((0, 3), np.float32)
    m200 = np.concatenate(m_l) if m_l else np.zeros(0, np.float32)
    np.savez_compressed(outp, pos=pos, m200=m200, z=z, a=a,
                        chunks_read=c, snap=snap)
    return (f"snap {snap}: z={z:.3f} kept {len(m200)} halos >1e10 "
            f"in {c} chunks [{time.time()-t0:.0f}s]")

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=10) as ex:
        for msg in ex.map(fetch_snap, SNAPS):
            print(msg, flush=True)
    man = {}
    for s in SNAPS:
        d = np.load(DATA / f"tng100_groups_{s:03d}.npz")
        man[s] = dict(z=float(d["z"]), a=float(d["a"]),
                      n_kept=int(len(d["m200"])), chunks=int(d["chunks_read"]),
                      counts={lbl: int((d["m200"] > v).sum()) for lbl, v in
                              [("1e10", 1e10), ("2e10", 2e10), ("3e10", 3e10),
                               ("5e10", 5e10), ("1e11", 1e11), ("2e11", 2e11),
                               ("5e11", 5e11), ("1e12", 1e12)]})
    with open(HERE / "fetch_manifest.json", "w") as fh:
        json.dump(man, fh, indent=1)
    print("manifest written")
