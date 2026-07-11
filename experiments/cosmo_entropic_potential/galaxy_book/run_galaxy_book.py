#!/usr/bin/env python3
"""
galaxy_book: does physical galactic-rung membership select the DE grain? (DECISIONS.md)
Frozen pipeline, gate-validated nested tile estimator (T=2 primary, T=4 reported), on the
26-snap dense grid. Primary unit = FoF group with M*>=1.1e9 Msun/h (>=100-star-particle
resolved galaxy). Reference halo-mass cuts (corner, >=2e11, >=1e11) recomputed on the SAME grid
+ estimator for a self-consistent decision. Incremental flush. No cap/subsample.
"""
import json, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
CEP = HERE.parent
DATA = CEP / "large_volume" / "data"
HG = CEP / "halo_grain"; EPOCH = CEP / "epoch_check"; DESIV2 = CEP / "desi_likelihood_v2"
sys.path.insert(0, str(HG)); sys.path.insert(0, str(CEP))
import s_of_a as S
csrc = (EPOCH / "cpl_projection.py").read_text(); cpl_ns = {"np": np}
exec("import numpy as np\nfrom scipy.integrate import quad\n"
     "from scipy.interpolate import CubicSpline\nfrom scipy.optimize import minimize\n"
     "C_KM = 299792.458\nZ_STAR = 1089.0\n", cpl_ns)
exec(compile(csrc.split("# 2. Backgrounds.")[1].split("# 4. Run.")[0],
             str(EPOCH / "cpl_projection.py"), "exec"), cpl_ns)
make_f_fw = cpl_ns["make_f_fw"]; project_distance = cpl_ns["project_distance"]; crossing_z = cpl_ns["crossing_z"]
sys.path.insert(0, str(DESIV2)); import likelihood_fit as lf
COV = np.array([[0.055**2, -0.7*0.055*0.20], [-0.7*0.055*0.20, 0.20**2]]); COVINV = np.linalg.inv(COV)
maha = lambda w0, wa: float(np.sqrt(np.array([w0+0.838, wa+0.62]) @ COVINV @ np.array([w0+0.838, wa+0.62])))
OM_PROJ = 0.3155

import cupy as cp
def make_xi_table(ps, R_smooth=1.0, rmin=0.02, rmax=180.0, n=400_000):
    xi = ps.xi_spline(R_smooth); sig2 = ps.sigma2_R(R_smooth)
    r = np.logspace(np.log10(rmin), np.log10(rmax), n); return cp.asarray(r), cp.asarray(xi(r)/sig2), float(sig2)
def _chol(C, bs=2048):
    from cupyx.scipy.linalg import solve_triangular
    k = C.shape[0]
    for j in range(0, k, bs):
        je = min(j+bs, k); Cjj = C[j:je, j:je]
        if j > 0: Lp = C[j:je, :j]; Cjj -= Lp @ Lp.T
        try: Ld = cp.linalg.cholesky(Cjj)
        except Exception: return False
        if bool(cp.isnan(cp.diagonal(Ld)).any()) or bool((cp.diagonal(Ld) <= 0).any()): return False
        C[j:je, j:je] = Ld
        if je < k:
            panel = C[je:, j:je]
            if j > 0: panel -= C[je:, :j] @ C[j:je, :j].T
            C[je:, j:je] = solve_triangular(Ld, panel.T, lower=True).T
    return True
def S_gpu(pos, box, xr, xv, jitter=0.0, tile=1024):
    k = len(pos)
    if k < 3: return None
    P = cp.asarray(pos, dtype=cp.float64); C = cp.empty((k, k), dtype=cp.float64)
    for i0 in range(0, k, tile):
        i1 = min(i0+tile, k); d2 = cp.zeros((i1-i0, k), dtype=cp.float64)
        for ax in range(3):
            dx = cp.abs(P[i0:i1, ax][:, None] - P[None, :, ax]); cp.minimum(dx, box-dx, out=dx); dx *= dx; d2 += dx
        cp.sqrt(d2, out=d2); cp.clip(d2, float(xr[0]), float(xr[-1]), out=d2); C[i0:i1] = cp.interp(d2, xr, xv); del d2, dx
    idx = cp.arange(k); C[idx, idx] = 1.0 + jitter; cp.get_default_memory_pool().free_all_blocks()
    if not _chol(C):
        del C; cp.get_default_memory_pool().free_all_blocks()
        return S_gpu(pos, box, xr, xv, jitter=1e-8) if jitter == 0.0 else None
    Sval = float(-2.0 * cp.log(cp.diagonal(C)).sum()); del C; cp.get_default_memory_pool().free_all_blocks()
    return Sval

SNAPS = [25, 30, 33, 36, 39, 42, 45, 47, 49, 51, 53, 55, 56, 59, 61,
         63, 65, 67, 70, 72, 74, 76, 79, 82, 87, 99]
BOX = 205.0; TILE_MAX = 38000; SEED_BASE = 20260711
gd = []
for s in SNAPS:
    d = np.load(DATA / f"tng300_galaxies_{s:03d}.npz")
    gd.append(dict(snap=s, z=float(d["z"]), a=float(d["a"]),
                   pos=d["pos"].astype(np.float64), m200=d["m200"].astype(np.float64),
                   mstar=d["mstar"].astype(np.float64)))
S.OM, S.OL, S.OB, S.H0H, S.NS, S.SIGMA8 = 0.3089, 0.6911, 0.0486, 0.6774, 0.9667, 0.8159
ps_tng = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8)
XR, XV, SIG2 = make_xi_table(ps_tng); LCDM_CHI2 = lf.profile_fixedshape(lf.f_lcdm, use_cmb=True)["chi2"]
T0 = time.time(); log = lambda m: print(f"[{time.time()-T0:7.1f}s] {m}", flush=True)

def tiled_S(pos, T, seed0):
    side = BOX / T
    idx = np.clip(np.floor(pos / side).astype(int), 0, T-1)
    tid = idx[:, 0]*T*T + idx[:, 1]*T + idx[:, 2]
    S_intra = 0.0; reps = []; occ = []; nflag = 0
    for t in range(T**3):
        sel = pos[tid == t]; n = len(sel); occ.append(int(n))
        if n == 0: continue
        reps.append(sel.mean(axis=0))
        if n > TILE_MAX:
            nflag += 1; sel = sel[np.random.RandomState(seed0 + t).choice(n, TILE_MAX, replace=False)]
        s = S_gpu(sel, BOX, XR, XV)
        if s is not None: S_intra += s
    reps = np.array(reps)
    S_inter = S_gpu(reps, BOX, XR, XV) if len(reps) >= 3 else 0.0
    return dict(S_intra=float(S_intra), S_inter=float(S_inter or 0.0), S_total=float(S_intra + (S_inter or 0.0)),
                occ_max=int(max(occ)) if occ else 0, n_tiles=int(sum(o > 0 for o in occ)), n_flagged=int(nflag))

def analyze(a, Sa):
    a = np.asarray(a, float); Sa = np.asarray(Sa, float)
    ok = np.isfinite(Sa) & (Sa > 0); a_ok, S_ok = a[ok], Sa[ok]; o = np.argsort(a_ok); a_ok, S_ok = a_ok[o], S_ok[o]
    if len(a_ok) < 4: return {"z_peak": None}
    imax = int(np.argmax(S_ok))
    w0, wa, c2 = project_distance(make_f_fw(a_ok, S_ok), Om=OM_PROJ, use_cmb=True)
    prof = lf.profile_fixedshape(lf.make_f_fw(a_ok, S_ok), use_cmb=True)
    return dict(z_peak=float(1/a_ok[imax]-1), peak_at_endpoint=bool(imax in (0, len(a_ok)-1)),
                w0=float(w0), wa=float(wa), cross_z=crossing_z(w0, wa), maha=maha(w0, wa),
                chi2=float(prof["chi2"]), chi2_minus_lcdm=float(prof["chi2"]-LCDM_CHI2))

def run_cut(select, tag, Tlist):
    """select(sd)->boolean mask on that snapshot's groups."""
    rec = {"tag": tag, "per_T": {}}
    m200_desc = []
    for T in Tlist:
        a_arr, Sint, Stot, ns, occ = [], [], [], [], []
        for si, sd in enumerate(gd):
            mask = select(sd); pos = sd["pos"][mask]
            r = tiled_S(pos, T, SEED_BASE + 1000000*T + 1000*si)
            a_arr.append(sd["a"]); Sint.append(r["S_intra"]); Stot.append(r["S_total"]); ns.append(int(mask.sum())); occ.append(r["occ_max"])
            if T == Tlist[0]:
                mm = sd["m200"][mask]
                m200_desc.append(dict(z=sd["z"], n=int(mask.sum()),
                    m200_med=float(np.median(mm)) if mm.size else None,
                    m200_16=float(np.percentile(mm, 16)) if mm.size else None,
                    m200_84=float(np.percentile(mm, 84)) if mm.size else None))
        rec["per_T"][str(T)] = dict(n_per_snap=ns, occ_max_per_snap=occ,
                                    n_flagged=int(sum(1 for o in occ if o > TILE_MAX)),
                                    S_total_analysis=analyze(a_arr, Stot),
                                    S_extensive_analysis=analyze(a_arr, Sint))
    rec["m200_distribution"] = m200_desc
    at = rec["per_T"][str(Tlist[0])]["S_total_analysis"]
    log(f"  [{tag}] T={Tlist[0]}: TOTAL maha={at['maha']:.3f} z_peak={at['z_peak']:.3f} "
        f"w0={at['w0']:.3f} wa={at['wa']:.3f} chi2dL={at['chi2_minus_lcdm']:+.3f} "
        f"n[{min(rec['per_T'][str(Tlist[0])]['n_per_snap'])},{max(rec['per_T'][str(Tlist[0])]['n_per_snap'])}]")
    return rec

RES = HERE / "results.json"
out = {"date": "2026-07-11", "grid": "26-snap dense", "snaps": SNAPS, "lcdm_chi2": LCDM_CHI2,
       "decision_rule": "PASS maha<1.89 & interior[0.35,0.85]; KILL maha>=2.0 | peak exits; AMBIG [1.89,2.0)",
       "reference_cuts": {}, "galaxy_book": {}, "ladder": {}}
def flush():
    with open(RES, "w") as fh: json.dump(out, fh, indent=1)
flush()
log(f"LCDM chi2={LCDM_CHI2:.4f}. 26-snap grid, {len(gd)} snaps loaded.")

# completeness check
comp = {}
for sd in gd:
    sel = sd["mstar"] > 1.1e9
    comp[sd["snap"]] = dict(n=int(sel.sum()), min_M200=float(sd["m200"][sel].min()) if sel.any() else None)
out["completeness_Mstar1p1e9"] = comp
worst = max(v["min_M200"] for v in comp.values() if v["min_M200"])
log(f"Completeness: max over snaps of min-M200 among M*>=1.1e9 = {worst:.3e} (fetch floor 3e10; want >> floor)")
flush()

# --- reference halo-mass cuts on the SAME 26-snap grid + estimator ---
log("=== REFERENCE halo-mass cuts (26-snap, same tile estimator) ===")
out["reference_cuts"]["corner_7.4253e11"] = run_cut(lambda sd: sd["m200"] > 7.4253e11, "corner>=7.4e11", [2]); flush()
out["reference_cuts"]["ge_2e11"] = run_cut(lambda sd: sd["m200"] > 2e11, ">=2e11", [2]); flush()
out["reference_cuts"]["ge_1e11"] = run_cut(lambda sd: sd["m200"] > 1e11, ">=1e11 (complete book)", [2]); flush()

# --- galaxy book: PRIMARY M*>=1.1e9, T=2 + T=4 ---
log("=== GALAXY BOOK primary M*>=1.1e9 ===")
out["galaxy_book"]["Mstar_ge_1.1e9"] = run_cut(lambda sd: sd["mstar"] > 1.1e9, "M*>=1.1e9", [2, 4]); flush()

# --- robustness ladder (T=2, reported never promoted) ---
log("=== LADDER (robustness, T=2) ===")
for lbl, cut in [("Mstar_ge_1e8.5", 10**8.5), ("Mstar_ge_1e9.5", 10**9.5), ("Mstar_ge_1e10", 1e10)]:
    out["ladder"][lbl] = run_cut(lambda sd, c=cut: sd["mstar"] > c, lbl, [2]); flush()

# --- verdict: primary M*>=1.1e9, T=2, S_total ---
v = out["galaxy_book"]["Mstar_ge_1.1e9"]["per_T"]["2"]["S_total_analysis"]
def verdict(a):
    if a["z_peak"] is None or not (0.35 <= a["z_peak"] <= 0.85): return "KILL (peak exits interior)"
    if a["maha"] < 1.89: return "PASS (rung-membership selects the grain)"
    if a["maha"] >= 2.0: return "KILL (grain is a second free constant)"
    return "AMBIGUOUS (unresolved-with-direction)"
ref2 = out["reference_cuts"]["ge_2e11"]["per_T"]["2"]["S_total_analysis"]["maha"]
out["VERDICT"] = {"word": verdict(v), "primary": "M*>=1.1e9, T=2, S_total",
                  "maha": v["maha"], "z_peak": v["z_peak"], "w0": v["w0"], "wa": v["wa"],
                  "chi2_minus_lcdm": v["chi2_minus_lcdm"],
                  "beats_ge2e11_same_grid": bool(v["maha"] < ref2), "ge2e11_maha_26snap": ref2}
flush()
log(f"VERDICT: {out['VERDICT']['word']}  maha={v['maha']:.3f} z_peak={v['z_peak']:.3f} "
    f"(w0={v['w0']:.3f} wa={v['wa']:.3f}); >=2e11(26snap) maha={ref2:.3f} beats={v['maha']<ref2}")
log("=" * 60); log("GALAXY BOOK DONE"); flush()
