#!/usr/bin/env python3
"""
PREDICTION 4 — stage 1: pull IllustrisTNG DM particle coordinates and reduce them, on the
fly, to CIC/NGP count grids at a ladder of random-subsample densities.  Method frozen in
DECISIONS.md before any number was seen.

Why this shape: nothing is stored at particle level.  PartType1/Coordinates is a CONTIGUOUS,
uncompressed HDF5 dataset, so one h5py open per chunk file yields its byte offset and every
subsequent read is a plain HTTP Range request.  Each worker streams its chunk in slabs and
accumulates straight into the grids; per-particle uniform deviates give NESTED random
subsamples (u < f), independent across replicates.

The API key is read from ~/.tng_api_key at runtime and never written anywhere.
Incremental flush: each worker rewrites its partial grid file every FLUSH_SLABS slabs, so a
kill/restart loses at most one flush interval and completed chunks are skipped.

Usage:  P4_SIM=TNG100-3 P4_SNAP=99 python3 fetch_grid.py        # fetch + combine
        P4_SIM=TNG100-3 P4_SNAP=99 python3 fetch_grid.py combine
"""
import json, os, sys, time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import numpy as np

SIM   = os.environ.get("P4_SIM", "TNG100-3")
SNAP  = int(os.environ.get("P4_SNAP", "99"))
# box size in Mpc/h and number of snapshot chunk files (from the API simulation record)
SIMS  = {"TNG100-3": dict(box=75.0,  nfiles=7,  ndm=94_196_375),
         "TNG300-3": dict(box=205.0, nfiles=16, ndm=244_140_625)}
BOX     = SIMS[SIM]["box"]
NFILES  = SIMS[SIM]["nfiles"]

NG1, NG2 = 64, 128
FRACS    = [4.3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1, 3e-1, 1.0]
NREP     = {4.3e-4: 4, 1e-3: 4, 3e-3: 4, 1e-2: 4, 3e-2: 2, 1e-1: 2, 3e-1: 1, 1.0: 1}
SEED     = 20260721
SLAB     = 250_000          # 6 MB/request (was 1M = 24 MB — throttled under fan-out)
FLUSH_SLABS = 2
OUT   = Path(os.environ.get("P4_SCRATCH",
             "/tmp/claude-1000/-home-emoore-coherence-ratchet/"
             "047db89f-06e6-45f4-a014-34f932c0bc32/scratchpad/p4"))


def key():
    return open(os.path.expanduser("~/.tng_api_key")).read().strip()


def url(c):
    return f"https://www.tng-project.org/api/{SIM}/files/snapshot-{SNAP}.{c}.hdf5"


# ---------------------------------------------------------------- layout probe
def probe(c):
    import fsspec, h5py
    fs = fsspec.filesystem("http", headers={"API-Key": key()})
    for attempt in range(5):
        try:
            with h5py.File(fs.open(url(c), "rb", block_size=2**16,
                                   cache_type="readahead"), "r") as f:
                d = f["PartType1"]["Coordinates"]
                hdr = dict(f["Header"].attrs)
                assert d.chunks is None and d.compression is None, "not contiguous"
                return dict(chunk=c, offset=int(d.id.get_offset()), n=int(d.shape[0]),
                            dtype=str(d.dtype), box=float(hdr["BoxSize"]),
                            z=float(hdr["Redshift"]),
                            ntot=int(np.asarray(hdr["NumPart_Total"])[1]),
                            mdm=float(np.asarray(hdr["MassTable"])[1]))
        except Exception as e:
            if attempt == 4:
                raise
            time.sleep(5 * (attempt + 1))


def get_layout():
    p = OUT / f"layout_{SIM}_{SNAP:03d}.json"
    if p.exists():
        return json.loads(p.read_text())
    with ProcessPoolExecutor(max_workers=NFILES) as ex:
        rows = list(ex.map(probe, range(NFILES)))
    lay = dict(sim=SIM, snap=SNAP, box_mpch=BOX,
               chunks=sorted(rows, key=lambda r: r["chunk"]),
               z=rows[0]["z"], boxsize_ckpch=rows[0]["box"], ntot=rows[0]["ntot"],
               mdm_1e10=rows[0]["mdm"])
    OUT.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(lay, indent=1))
    return lay


# ---------------------------------------------------------------- assignment
def cic_add(grid, pos, L, ng):
    if pos.shape[0] == 0:
        return
    x = (pos % L) / L * ng
    i0 = np.floor(x).astype(np.int64)
    d = x - i0
    i0 %= ng
    i1 = (i0 + 1) % ng
    for dx in (0, 1):
        wx = d[:, 0] if dx else 1.0 - d[:, 0]
        ix = i1[:, 0] if dx else i0[:, 0]
        for dy in (0, 1):
            wy = d[:, 1] if dy else 1.0 - d[:, 1]
            iy = i1[:, 1] if dy else i0[:, 1]
            xy = (ix * ng + iy) * ng
            wxy = wx * wy
            for dz in (0, 1):
                wz = d[:, 2] if dz else 1.0 - d[:, 2]
                iz = i1[:, 2] if dz else i0[:, 2]
                grid += np.bincount(xy + iz, weights=wxy * wz, minlength=ng**3)


def ngp_add(grid, pos, L, ng):
    if pos.shape[0] == 0:
        return
    idx = (np.floor((pos % L) / L * ng).astype(np.int64)) % ng
    grid += np.bincount((idx[:, 0] * ng + idx[:, 1]) * ng + idx[:, 2], minlength=ng**3)


# ---------------------------------------------------------------- worker
def kname(kind, ng, f, r):
    return f"{kind}_ng{ng}_f{f:.6g}_r{r}"


def new_grids():
    g = {}
    for f in FRACS:
        for r in range(NREP[f]):
            g[kname("cic", NG1, f, r)] = np.zeros(NG1**3)
        g[kname("ngp", NG1, f, 0)] = np.zeros(NG1**3)
        g[kname("cic", NG2, f, 0)] = np.zeros(NG2**3)
    return g


def worker(c):
    import urllib.request
    lay = get_layout()
    row = [r for r in lay["chunks"] if r["chunk"] == c][0]
    n, off = row["n"], row["offset"]
    rec = 3 * np.dtype(row["dtype"]).itemsize
    outp = OUT / f"part_{SIM}_{SNAP:03d}_{c:02d}.npz"
    grids = new_grids()
    start = 0
    if outp.exists():
        try:
            d = np.load(outp)
            if bool(d["done"]):
                return f"chunk {c}: cached"
            start = int(d["n_done"])
            for k in grids:
                grids[k] += d[k].astype(np.float64)
        except Exception:
            start = 0
            grids = new_grids()
    K = key()
    maxrep = max(NREP.values())
    rngs = [np.random.default_rng([SEED, SNAP, c, r]) for r in range(maxrep)]
    if start:                      # replay deviate stream so the subsample stays nested
        for r in range(maxrep):
            rngs[r].random(start)
    t0 = time.time()
    done_p, slab_i = start, 0
    while done_p < n:
        m = min(SLAB, n - done_p)
        b0 = off + done_p * rec
        buf = None
        for attempt in range(6):
            try:
                req = urllib.request.Request(
                    url(c), headers={"API-Key": K,
                                     "Range": f"bytes={b0}-{b0 + m*rec - 1}"})
                buf = urllib.request.urlopen(req, timeout=180).read()
                if len(buf) != m * rec:
                    raise IOError(f"short read {len(buf)} != {m*rec}")
                break
            except Exception as e:
                if attempt == 5:
                    raise RuntimeError(f"chunk {c} slab @{done_p}: {e}")
                time.sleep(4.0 * (attempt + 1))
        pos = (np.frombuffer(buf, dtype=row["dtype"]).reshape(m, 3) / 1000.0)  # -> Mpc/h
        del buf
        us = [rngs[r].random(m) for r in range(maxrep)]
        for f in FRACS:
            for r in range(NREP[f]):
                sel = pos if f >= 1.0 else pos[us[r] < f]
                cic_add(grids[kname("cic", NG1, f, r)], sel, BOX, NG1)
                if r == 0:
                    ngp_add(grids[kname("ngp", NG1, f, 0)], sel, BOX, NG1)
                    cic_add(grids[kname("cic", NG2, f, 0)], sel, BOX, NG2)
        del pos, us
        done_p += m
        slab_i += 1
        flushed = slab_i % FLUSH_SLABS == 0 or done_p >= n
        if flushed:
            tmp = outp.with_suffix(".tmp.npz")
            np.savez(tmp, done=(done_p >= n), n_done=done_p, n_tot=n,
                     **{k: v.astype(np.float32) for k, v in grids.items()})
            os.replace(tmp, outp)
        print(f"chunk {c}: {done_p/1e6:.1f}/{n/1e6:.1f} M "
              f"[{time.time()-t0:.0f}s]{' flush' if flushed else ''}", flush=True)
    return f"chunk {c}: DONE {n} particles in {time.time()-t0:.0f}s"


# ---------------------------------------------------------------- combine
def combine():
    lay = get_layout()
    parts = [OUT / f"part_{SIM}_{SNAP:03d}_{c:02d}.npz" for c in range(NFILES)]
    miss = [p.name for p in parts if not p.exists()]
    if miss:
        raise SystemExit(f"missing partial files: {miss}")
    tot, ndone = None, 0
    for p in parts:
        d = np.load(p)
        if not bool(d["done"]):
            raise SystemExit(f"{p.name} incomplete ({int(d['n_done'])}/{int(d['n_tot'])})")
        ndone += int(d["n_done"])
        keys = [k for k in d.files if k not in ("done", "n_done", "n_tot")]
        if tot is None:
            tot = {k: d[k].astype(np.float64) for k in keys}
        else:
            for k in keys:
                tot[k] += d[k]
    outp = OUT / f"grids_{SIM}_{SNAP:03d}.npz"
    np.savez(outp, ntot=ndone, z=lay["z"], box=BOX, ng1=NG1, ng2=NG2,
             **{k: v.astype(np.float32) for k, v in tot.items()})
    print(f"combined {ndone} particles (header {lay['ntot']}) -> {outp}")
    return outp


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    if len(sys.argv) > 1 and sys.argv[1] == "combine":
        combine()
    else:
        lay = get_layout()
        print(f"{SIM} snap {SNAP}: z={lay['z']:.4f} box={BOX} Mpc/h  Ntot={lay['ntot']}  "
              f"bytes={lay['ntot']*3*np.dtype(lay['chunks'][0]['dtype']).itemsize/1e9:.2f} GB",
              flush=True)
        # I/O concurrency only (not a method parameter): 7 concurrent Range streams
        # were throttled to a standstill by the TNG API on 2026-07-21. Default 3.
        nw = int(os.environ.get("P4_WORKERS", "3"))
        with ProcessPoolExecutor(max_workers=nw) as ex:
            for msg in ex.map(worker, range(NFILES)):
                print(msg, flush=True)
        combine()
