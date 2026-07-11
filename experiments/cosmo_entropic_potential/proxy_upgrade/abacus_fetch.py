#!/usr/bin/env python3
"""
Abacus probe — fetch+extract only (network/CPU). For each selected z slice of the
AbacusSummit small box ph3000: download halo_info (blosc asdf, ~1.2GB), extract
halo center positions (SO_central_particle, Mpc/h) shifted to [0,box) + halo mass
(N * ParticleMassHMsun), save a small npz, DELETE the asdf. Peak disk ~1.2GB.

Anonymous HTTPS mirror: data.desi.lbl.gov/public/cosmosim/AbacusSummit/small/.
Box 500 Mpc/h, c000 = Planck base (Om=0.315192, h=0.6736). Lever arm a=0.25..0.833
(small box has NO z<0.2, so no a=1 — flagged in SUMMARY).
"""
import os, sys, json, time, subprocess
from pathlib import Path
import numpy as np
from abacusnbody.data.compaso_halo_catalog import CompaSOHaloCatalog

HERE = Path(__file__).resolve().parent
OUT = HERE / "abacus_data"; OUT.mkdir(exist_ok=True)
SCRATCH = Path("/tmp/claude-1000/-home-emoore-coherence-ratchet/"
               "047db89f-06e6-45f4-a014-34f932c0bc32/scratchpad/abacus_test")
BOX = 500.0
SIM = "AbacusSummit_small_c000_ph3000"
BASE = f"https://data.desi.lbl.gov/public/cosmosim/AbacusSummit/small/{SIM}/halos"
# z slices chosen to mirror the frozen a-grid as closely as the small box allows
ZSTR = ["z3.000", "z2.250", "z1.700", "z1.400", "z1.025",
        "z0.800", "z0.575", "z0.500", "z0.350", "z0.200"]

T0 = time.time()
def log(m): print(f"[{time.time()-T0:7.1f}s] {m}", flush=True)

manifest = {"sim": SIM, "box": BOX, "mirror": BASE, "cosmology": "c000 Planck",
            "slices": []}
for zs in ZSTR:
    npz = OUT / f"abacus_{zs}.npz"
    if npz.exists():
        d = np.load(npz)
        manifest["slices"].append(dict(z=float(d["z"]), a=float(d["a"]),
                                       n=int(len(d["mass"])), cached=True))
        log(f"{zs}: cached ({len(d['mass'])} halos)")
        continue
    zdir = SCRATCH / SIM / "halos" / zs
    hi = zdir / "halo_info"
    hi.mkdir(parents=True, exist_ok=True)
    asdf = hi / "halo_info_000.asdf"
    # header + asdf
    subprocess.run(["curl", "-s", "--max-time", "60", f"{BASE}/{zs}/header",
                    "-o", str(zdir / "header")], check=True)
    if not asdf.exists():
        t = time.time()
        r = subprocess.run(["curl", "-s", "--max-time", "600",
                            f"{BASE}/{zs}/halo_info/halo_info_000.asdf",
                            "-o", str(asdf)])
        if r.returncode != 0 or not asdf.exists():
            log(f"{zs}: DOWNLOAD FAILED rc={r.returncode}")
            manifest["slices"].append(dict(z=zs, error="download_failed"))
            continue
        log(f"{zs}: downloaded {asdf.stat().st_size/1e9:.2f}GB in {time.time()-t:.0f}s")
    cat = CompaSOHaloCatalog(str(zdir), fields=["N", "SO_central_particle"],
                             cleaned=False)
    hdr = cat.header
    z = float(hdr["Redshift"]); a = 1.0 / (1.0 + z)
    pm = float(hdr["ParticleMassHMsun"])
    pos = np.asarray(cat.halos["SO_central_particle"], dtype=np.float64)
    pos = np.mod(pos + BOX / 2.0, BOX)          # center [-250,250] -> [0,500)
    mass = np.asarray(cat.halos["N"], dtype=np.float64) * pm
    np.savez(npz, z=z, a=a, pos=pos.astype(np.float32), mass=mass.astype(np.float32),
             box=BOX, particle_mass=pm)
    log(f"{zs}: z={z:.3f} a={a:.3f} N={len(mass)} Mmax={mass.max():.2e} "
        f"-> {npz.name} ({npz.stat().st_size/1e6:.1f}MB)")
    manifest["slices"].append(dict(z=z, a=a, n=int(len(mass)),
                                   Mmax=float(mass.max()), pm=pm))
    os.remove(asdf)                              # free the 1.2GB immediately
    (HERE / "abacus_manifest.json").write_text(json.dumps(manifest, indent=1))

(HERE / "abacus_manifest.json").write_text(json.dumps(manifest, indent=1))
log(f"done: {len([s for s in manifest['slices'] if 'a' in s])} slices extracted")
