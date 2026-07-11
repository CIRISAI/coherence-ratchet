#!/usr/bin/env python3
"""
Abacus cross-code probe — GPU-FREE model-C run on AbacusSummit small box ph3000.
The full corner curve (k->38000, k(z=3)=184) needs the 16GB GPU; under persistent GPU
contention we run the frozen MODEL-C pipeline (PSD by construction -> CPU Cholesky log-det)
over the well-populated sub-range a=0.37..0.833 (8 slices) at cap=20000 / thr=2.10e13.
The two highest-z slices (z=3.0, 2.25) are dropped: at any CPU-feasible cap the 500 Mpc/h
box's steep mass-function evolution leaves them with k<40 (documented; not a headline).

Same estimator/cosmology as run_test model-C: xi_R(r)/sigma2_R at halo positions,
Planck c000. DESI window z 0.295..1.7 covered; z=2.33 extrapolated; w_today extrapolated
(no a=1). Reports S(a), interior peak, CPL, real DESI chi2.
"""
import json, sys, time
from pathlib import Path
import numpy as np
from scipy.linalg import cholesky

HERE = Path(__file__).resolve().parent
CEP = HERE.parent
AB = HERE / "abacus_data"
sys.path.insert(0, str(CEP)); sys.path.insert(0, str(HERE))
sys.path.insert(0, str(CEP / "desi_likelihood_v2"))
import s_of_a as S
import analyze_measured as AM

S.OM, S.OL, S.OB, S.H0H, S.NS, S.SIGMA8 = 0.315192, 0.684808, 0.0493, 0.6736, 0.9649, 0.8080
BOX = 500.0
CAP = 20000
# well-populated sub-range (drop z=3.0, z=2.25 which have k<400 at this cap)
ZSTR = ["z1.700", "z1.400", "z1.025", "z0.800", "z0.575", "z0.500", "z0.350", "z0.200"]
TILE = 2000

T0 = time.time()
def log(m): print(f"[{time.time()-T0:7.1f}s] {m}", flush=True)

ps = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8)
XIM = ps.xi_spline(1.0); SIG2M = ps.sigma2_R(1.0)

# threshold from the FULL 10-slice set (cap=20000) so it matches the documented selection
ALLZ = ["z3.000", "z2.250"] + ZSTR
allmass = [np.load(AB / f"abacus_{z}.npz")["mass"].astype(np.float64) for z in ALLZ]
thr = max(np.sort(m)[-(CAP + 1)] if len(m) > CAP else 0.0 for m in allmass)

snap = []
for zs in ZSTR:
    d = np.load(AB / f"abacus_{zs}.npz")
    snap.append(dict(z=float(d["z"]), a=float(d["a"]),
                     pos=d["pos"][d["mass"].astype(np.float64) > thr].astype(np.float64)))
snap.sort(key=lambda s: s["a"])

def build_C(pos):
    n = len(pos); C = np.empty((n, n))
    for i0 in range(0, n, TILE):
        i1 = min(i0 + TILE, n)
        d2 = np.zeros((i1 - i0, n))
        for ax in range(3):
            dx = np.abs(pos[i0:i1, ax][:, None] - pos[None, :, ax])
            np.minimum(dx, BOX - dx, out=dx); dx *= dx; d2 += dx
        r = np.sqrt(d2, out=d2)
        C[i0:i1] = XIM(r) / SIG2M
    np.fill_diagonal(C, 1.0)
    return C

def logdet_chol(C):
    for jit in (0.0, 1e-10, 1e-8):
        try:
            Cc = C if jit == 0.0 else (C + jit * np.eye(len(C)))
            L = cholesky(Cc, lower=True, overwrite_a=(jit != 0.0))
            return float(-2.0 * np.log(np.diag(L)).sum()), jit
        except np.linalg.LinAlgError:
            continue
    return None, None

out = {"box": BOX, "sim": "AbacusSummit_small_c000_ph3000 (CPU, sub-range)",
       "cosmology": "c000 Planck", "cap": CAP, "thr": float(thr),
       "a_range": "0.37..0.833 (z=3.0,2.25 dropped: k<400 at CPU-feasible cap)",
       "estimator": "model-C xi_R/sigma2_R, CPU Cholesky log-det (PSD)",
       "caveat": "no a=1 (w_today extrapolated); DESI z<=1.7 covered, z=2.33 extrapolated",
       "records": []}
RES = HERE / "abacus_cpu_results.json"
def flush(): RES.write_text(json.dumps(out, indent=1))

log(f"thr(cap={CAP})={thr:.3e}  slices={len(snap)}")
for s in snap:
    C = build_C(s["pos"]); Sv, jit = logdet_chol(C)
    rec = dict(a=s["a"], z=s["z"], k=len(s["pos"]), S=Sv, jitter=jit)
    out["records"].append(rec); flush()
    log(f"a={s['a']:.3f} z={s['z']:.3f} k={len(s['pos']):5d} S={Sv:.2f}"
        + (f" [jit={jit}]" if jit else ""))

a = np.array([r["a"] for r in out["records"]]); Sa = np.array([r["S"] for r in out["records"]])
out["analysis"] = AM.analyze(a, Sa, "Abacus small c000 ph3000 (CPU sub-range)", project=True)
flush()
r = out["analysis"]; c = r["cpl_dist_BAO+CMB"]; ch = r["desi_chi2_with_cmb"]
log("=" * 70)
log(f"ABACUS(CPU): w(a=0.833)={r['w_today']:+.3f}  interior_peak_z={r['interior_peak_z']}  "
    f"CPL(w0={c['w0']:+.3f},wa={c['wa']:+.3f},cross={c['cross_z']})  DESI chi2={ch['chi2']:.3f}")
log("wrote abacus_cpu_results.json")
