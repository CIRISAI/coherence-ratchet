#!/usr/bin/env python3
"""Full-population companion on T=8 only (clean, no flagging) + grid caveat. Merges into
results.json (preserves gate v2, corner T=2/4/8, partial full T=4). Verdict left to finalize.py.
Operational amendment 3."""
import json, sys, time
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent; CEP = HERE.parent
ABACUS = CEP / "proxy_upgrade" / "abacus_data"; EPOCH = CEP / "epoch_check"; DESIV2 = CEP / "desi_likelihood_v2"
sys.path.insert(0, str(CEP)); import s_of_a as S
csrc = (EPOCH / "cpl_projection.py").read_text(); cpl_ns = {"np": np}
exec("import numpy as np\nfrom scipy.integrate import quad\nfrom scipy.interpolate import CubicSpline\n"
     "from scipy.optimize import minimize\nC_KM = 299792.458\nZ_STAR = 1089.0\n", cpl_ns)
exec(compile(csrc.split("# 2. Backgrounds.")[1].split("# 4. Run.")[0], str(EPOCH / "cpl_projection.py"), "exec"), cpl_ns)
make_f_fw = cpl_ns["make_f_fw"]; project_distance = cpl_ns["project_distance"]; crossing_z = cpl_ns["crossing_z"]
sys.path.insert(0, str(DESIV2)); import likelihood_fit as lf
COV = np.array([[0.055**2, -0.7*0.055*0.20], [-0.7*0.055*0.20, 0.20**2]]); COVINV = np.linalg.inv(COV)
def maha_pt(w0, wa, c0=-0.838, c1=-0.62):
    d = np.array([w0-c0, wa-c1]); return float(np.sqrt(d @ COVINV @ d))
OM_PROJ = 0.3155; BOX = 500.0; SEED_BASE = 20260711; TILE_MAX = 38000; FLOOR = 2.109e11
S.OM, S.OL, S.H0H = 0.315192, 0.684808, 0.6736; S.OB = 0.02237 / S.H0H**2; S.NS, S.SIGMA8 = 0.9649, 0.807952
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
        P = cp.asarray(pos, dtype=cp.float64); C = cp.empty((k, k), dtype=cp.float64)
        for i0 in range(0, k, tile):
            i1 = min(i0+tile, k); d2 = cp.zeros((i1-i0, k), dtype=cp.float64)
            for ax in range(3):
                dx = cp.abs(P[i0:i1, ax][:, None] - P[None, :, ax]); cp.minimum(dx, box-dx, out=dx); dx *= dx; d2 += dx
            cp.sqrt(d2, out=d2); cp.clip(d2, float(xr[0]), float(xr[-1]), out=d2); C[i0:i1] = cp.interp(d2, xr, xv); del d2, dx
        idx = cp.arange(k); C[idx, idx] = 1.0 + 1e-8
        if not _chol(C): del C; cp.get_default_memory_pool().free_all_blocks(); return None
    Sval = float(-2.0 * cp.log(cp.diagonal(C)).sum()); del C; cp.get_default_memory_pool().free_all_blocks()
    return Sval
def tiled_S(pos, T, seed0):
    side = BOX / T; idx = np.clip(np.floor(pos / side).astype(int), 0, T-1); tid = idx[:, 0]*T*T + idx[:, 1]*T + idx[:, 2]
    S_intra = 0.0; reps = []; occ = []; nflag = 0
    for t in range(T**3):
        sel = pos[tid == t]; n = len(sel); occ.append(int(n))
        if n == 0: continue
        reps.append(sel.mean(axis=0))
        if n > TILE_MAX:
            nflag += 1; sel = sel[np.random.RandomState(seed0 + t).choice(n, TILE_MAX, replace=False)]
        s = S_gpu(sel, BOX, XR, XV)
        if s is not None: S_intra += s
    reps = np.array(reps); S_inter = S_gpu(reps, BOX, XR, XV) if len(reps) >= 3 else 0.0
    return dict(S_intra=float(S_intra), S_inter=float(S_inter or 0.0), S_total=float(S_intra + (S_inter or 0.0)),
                occ_min=int(min(occ)), occ_max=int(max(occ)), n_tiles=int(sum(o > 0 for o in occ)), n_flagged=int(nflag))
def analyze(a, Sa):
    a = np.asarray(a, float); Sa = np.asarray(Sa, float); ok = np.isfinite(Sa) & (Sa > 0)
    a_ok, S_ok = a[ok], Sa[ok]; o = np.argsort(a_ok); a_ok, S_ok = a_ok[o], S_ok[o]
    if len(a_ok) < 4: return {"z_peak": None}
    imax = int(np.argmax(S_ok)); w0, wa, c2 = project_distance(make_f_fw(a_ok, S_ok), Om=OM_PROJ, use_cmb=True)
    prof = lf.profile_fixedshape(lf.make_f_fw(a_ok, S_ok), use_cmb=True)
    return dict(z_peak=float(1/a_ok[imax]-1), peak_at_endpoint=bool(imax in (0, len(a_ok)-1)), w0=float(w0), wa=float(wa),
                thawing=bool(wa < 0), cross_z=crossing_z(w0, wa), maha=maha_pt(w0, wa), chi2=float(prof["chi2"]),
                chi2_minus_lcdm=float(prof["chi2"]-lf.profile_fixedshape(lf.f_lcdm, use_cmb=True)["chi2"]))
T0 = time.time(); log = lambda m: print(f"[{time.time()-T0:7.1f}s] {m}", flush=True)
snapdata = []
for f in sorted(ABACUS.glob("abacus_z*.npz")):
    d = np.load(f); snapdata.append(dict(z=float(d["z"]), a=float(d["a"]), pos=d["pos"].astype(np.float64), mass=d["mass"].astype(np.float64)))
snapdata.sort(key=lambda s: s["a"])
ps = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8); XR, XV, SIG2 = make_xi_table(ps)
log(f"loaded {len(snapdata)} snaps")
RES = HERE / "results.json"; out = json.load(open(RES))
def flush():
    with open(RES, "w") as fh: json.dump(out, fh, indent=1)
log("=== FULL POPULATION 2.109e11 T=8 only ===")
Stot, Sint, per = [], [], []
rec = dict(out.get("full_2.109e11", {}))
for si, sd in enumerate(snapdata):
    pos = sd["pos"][sd["mass"] > FLOOR]
    r = tiled_S(pos, 8, SEED_BASE + 8000000 + 1000*si)
    r.update(a=sd["a"], z=sd["z"], n=int(len(pos))); per.append(r); Stot.append(r["S_total"]); Sint.append(r["S_intra"])
    rec["8"] = {"per_snap": per}; out["full_2.109e11"] = rec; flush()
    log(f"    [full T=8] a={sd['a']:.3f} n={len(pos)} S={r['S_total']:.1f} occ[{r['occ_min']},{r['occ_max']}] flagged={r['n_flagged']}")
an_t = analyze([p["a"] for p in per], Stot); an_e = analyze([p["a"] for p in per], Sint)
rec["8"] = {"per_snap": per, "S_total_analysis": an_t, "S_extensive_analysis": an_e}
rec["T4_note"] = "T=4 full-population abandoned per amendment 3 (slow + subsample-contaminated at late snaps); partial rows a=0.249,0.307,0.370 preserved if present"
out["full_2.109e11"] = rec; flush()
log(f"  [full] T=8: z_peak={an_t['z_peak']:.3f} w0={an_t['w0']:.3f} wa={an_t['wa']:.3f} thaw={an_t['thawing']} maha={an_t['maha']:.3f} chi2dL={an_t['chi2_minus_lcdm']:+.3f}")
# grid caveat
tng = json.load(open(CEP / "large_volume" / "results.json")); recs = tng["stage2_primary"]["records"]
a_tng = np.array([r["a"] for r in recs]); S_tng = np.array([r["S"] for r in recs]); full = analyze(a_tng, S_tng)
a_ab = np.array(sorted(s["a"] for s in snapdata)); S_re = np.exp(np.interp(np.log(a_ab), np.log(a_tng), np.log(S_tng))); regrid = analyze(a_ab, S_re)
out["grid_caveat"] = {"method": "TNG300 large_volume corner S(a) reprojected on Abacus a-grid (truncated a<=0.8333)",
    "tng_full_grid": {k: full[k] for k in ("z_peak", "w0", "wa", "cross_z", "maha")},
    "tng_on_abacus_grid": {k: regrid[k] for k in ("z_peak", "w0", "wa", "cross_z", "maha")},
    "delta": {"w0": regrid["w0"]-full["w0"], "wa": regrid["wa"]-full["wa"],
              "cross_z": (regrid["cross_z"] or np.nan)-(full["cross_z"] or np.nan), "maha": regrid["maha"]-full["maha"]}}
flush()
log(f"GRID CAVEAT: TNG full ({full['w0']:.3f},{full['wa']:.3f},cross={full['cross_z']}) -> Abacus-grid "
    f"({regrid['w0']:.3f},{regrid['wa']:.3f},cross={regrid['cross_z']}) Dw0={out['grid_caveat']['delta']['w0']:+.3f} Dwa={out['grid_caveat']['delta']['wa']:+.3f}")
log("DONE full T=8 + grid caveat"); flush()
