#!/usr/bin/env python3
"""
abacus_cross gate v2 (fair-regime subvolume gate) + science runs.
Amendment logged in DECISIONS.md before this ran. Gate v2 validates the nested-tile estimator
at the corner-equivalent grain/density where exact-det IS reachable per 125-Mpc/h subvolume
(exact vs nested-tile of 62.5-Mpc/h sub-tiles), on the fractional-S and dlnS/dlna metric (NOT
the conditioning-suspect CPL maha of v1). If v2 passes: corner-equivalent + full-population
runs + original decision rule. Preserves the v1 gate already in results.json.
"""
import json, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
CEP = HERE.parent
ABACUS = CEP / "proxy_upgrade" / "abacus_data"
EPOCH = CEP / "epoch_check"; DESIV2 = CEP / "desi_likelihood_v2"
sys.path.insert(0, str(CEP))
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
def maha_pt(w0, wa, c0=-0.838, c1=-0.62):
    d = np.array([w0-c0, wa-c1]); return float(np.sqrt(d @ COVINV @ d))
OM_PROJ = 0.3155
BOX = 500.0
SEED_BASE = 20260711
TILE_MAX = 38000
LCDM_3SIGMA = 3.28
CORNER = 7.425e11
FLOOR = 2.109e11

S.OM, S.OL, S.H0H = 0.315192, 0.684808, 0.6736
S.OB = 0.02237 / S.H0H**2
S.NS, S.SIGMA8 = 0.9649, 0.807952

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
    side = BOX / T
    idx = np.clip(np.floor(pos / side).astype(int), 0, T-1)
    tid = idx[:, 0]*T*T + idx[:, 1]*T + idx[:, 2]
    S_intra = 0.0; reps = []; occ = []; nflag = 0
    for t in range(T**3):
        sel = pos[tid == t]; n = len(sel); occ.append(int(n))
        if n == 0: continue
        reps.append(sel.mean(axis=0))
        if n > TILE_MAX:
            nflag += 1
            sel = sel[np.random.RandomState(seed0 + t).choice(n, TILE_MAX, replace=False)]
        s = S_gpu(sel, BOX, XR, XV)
        if s is not None: S_intra += s
    reps = np.array(reps)
    S_inter = S_gpu(reps, BOX, XR, XV) if len(reps) >= 3 else 0.0
    return dict(S_intra=float(S_intra), S_inter=float(S_inter or 0.0),
                S_total=float(S_intra + (S_inter or 0.0)),
                occ_min=int(min(occ)), occ_max=int(max(occ)),
                n_tiles=int(sum(o > 0 for o in occ)), n_flagged=int(nflag))

def subtile_S(pos, origin, sub=125.0, ntile=2):
    """Nested-tile S inside a subvolume: ntile^3 sub-tiles of side sub/ntile.
    Local coords; plain Euclidean via S_gpu(box=huge so min-image never wraps)."""
    local = pos - origin
    side = sub / ntile
    idx = np.clip(np.floor(local / side).astype(int), 0, ntile-1)
    tid = idx[:, 0]*ntile*ntile + idx[:, 1]*ntile + idx[:, 2]
    S_intra = 0.0; reps = []
    for t in range(ntile**3):
        sel = local[tid == t]
        if len(sel) < 1: continue
        reps.append(sel.mean(axis=0))
        if len(sel) >= 3:
            s = S_gpu(sel, 1e9, XR, XV)
            if s is not None: S_intra += s
    reps = np.array(reps)
    S_inter = S_gpu(reps, 1e9, XR, XV) if len(reps) >= 3 else 0.0
    return S_intra + (S_inter or 0.0)

def analyze(a, Sa):
    a = np.asarray(a, float); Sa = np.asarray(Sa, float)
    ok = np.isfinite(Sa) & (Sa > 0); a_ok, S_ok = a[ok], Sa[ok]
    o = np.argsort(a_ok); a_ok, S_ok = a_ok[o], S_ok[o]
    if len(a_ok) < 4: return {"z_peak": None}
    imax = int(np.argmax(S_ok))
    w0, wa, c2 = project_distance(make_f_fw(a_ok, S_ok), Om=OM_PROJ, use_cmb=True)
    prof = lf.profile_fixedshape(lf.make_f_fw(a_ok, S_ok), use_cmb=True)
    return dict(z_peak=float(1/a_ok[imax]-1), peak_at_endpoint=bool(imax in (0, len(a_ok)-1)),
                w0=float(w0), wa=float(wa), thawing=bool(wa < 0), cross_z=crossing_z(w0, wa),
                maha=maha_pt(w0, wa), chi2=float(prof["chi2"]),
                chi2_minus_lcdm=float(prof["chi2"]-LCDM_CHI2))

# ---- load ----
T0 = time.time(); log = lambda m: print(f"[{time.time()-T0:7.1f}s] {m}", flush=True)
snapdata = []
for f in sorted(ABACUS.glob("abacus_z*.npz")):
    d = np.load(f)
    snapdata.append(dict(z=float(d["z"]), a=float(d["a"]),
                         pos=d["pos"].astype(np.float64), mass=d["mass"].astype(np.float64),
                         pm=float(d["particle_mass"])))
snapdata.sort(key=lambda s: s["a"])
A = np.array([s["a"] for s in snapdata])
ps = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8)
XR, XV, SIG2 = make_xi_table(ps)
LCDM_CHI2 = lf.profile_fixedshape(lf.f_lcdm, use_cmb=True)["chi2"]
log(f"loaded {len(snapdata)} snaps; LCDM chi2={LCDM_CHI2:.4f}")

RES = HERE / "results.json"
out = json.load(open(RES))          # preserve v1 gate
out["lcdm_chi2"] = LCDM_CHI2
def flush():
    with open(RES, "w") as fh: json.dump(out, fh, indent=1)

# =========================================================================
# GATE V2 — subvolume fair-regime gate at the corner threshold
# =========================================================================
log("=== GATE V2 (subvolume, corner threshold 7.425e11) ===")
NSUB = 4; SUB = 125.0
sub_idx = np.random.RandomState(SEED_BASE).choice(64, NSUB, replace=False)
log(f"chosen subvolumes (of 64): {sub_idx.tolist()}")
gv2 = {"threshold_Msun_h": CORNER, "subvolume_Mpch": SUB, "subtile_Mpch": SUB/2,
       "chosen_subvolumes": sub_idx.tolist(), "per_subvolume": []}
def sub_origin(si):
    ix = si // 16; iy = (si // 4) % 4; iz = si % 4
    return np.array([ix, iy, iz]) * SUB
frac_meds, dln_meds, zpeak_ok = [], [], 0
for si in sub_idx:
    org = sub_origin(int(si))
    S_ex, S_ti, ncnt = [], [], []
    for sd in snapdata:
        sel = sd["mass"] > CORNER
        p = sd["pos"][sel]
        inbox = np.all((p >= org) & (p < org + SUB), axis=1)
        pv = p[inbox]; ncnt.append(int(len(pv)))
        se = S_gpu(pv - org, 1e9, XR, XV)     # exact, plain Euclidean (local coords)
        st = subtile_S(pv, org, SUB, 2)       # nested-tile, 62.5 sub-tiles
        S_ex.append(se); S_ti.append(st)
    S_ex = np.array(S_ex, float); S_ti = np.array(S_ti, float)
    frac = np.abs(S_ti - S_ex) / S_ex
    dex = S.dln_dlna(A, S_ex); dti = S.dln_dlna(A, S_ti)
    ddln = np.abs(dti - dex)
    zpe = float(1/A[np.argmax(S_ex)]-1); zpt = float(1/A[np.argmax(S_ti)]-1)
    # within one snapshot: adjacent index of argmax
    ie, it = int(np.argmax(S_ex)), int(np.argmax(S_ti))
    zmatch = abs(ie - it) <= 1
    zpeak_ok += int(zmatch)
    frac_meds.append(float(np.median(frac))); dln_meds.append(float(np.median(ddln)))
    rec = {"subvolume": int(si), "counts": ncnt,
           "S_exact": S_ex.tolist(), "S_tiled": S_ti.tolist(),
           "frac_err": frac.tolist(), "frac_err_median": float(np.median(frac)),
           "frac_err_max": float(np.max(frac)),
           "dlnS_dlna_exact": dex.tolist(), "dlnS_dlna_tiled": dti.tolist(),
           "dlnS_dlna_abserr_median": float(np.median(ddln)),
           "dlnS_dlna_abserr_max": float(np.max(ddln)),
           "z_peak_exact": zpe, "z_peak_tiled": zpt, "z_peak_within_one_snap": bool(zmatch)}
    gv2["per_subvolume"].append(rec); out["gate_v2"] = gv2; flush()
    log(f"  sub {si}: n[{min(ncnt)},{max(ncnt)}] fracS med={np.median(frac)*100:.2f}% max={np.max(frac)*100:.2f}% "
        f"| dlnS med={np.median(ddln):.4f} max={np.max(ddln):.4f} | zpeak ex={zpe:.3f} ti={zpt:.3f} match={zmatch}")
mean_frac = float(np.mean(frac_meds)); mean_dln = float(np.mean(dln_meds))
gate_v2_pass = bool(mean_frac <= 0.02 and mean_dln <= 0.15 and zpeak_ok >= 3)
gv2["summary"] = {"mean_median_frac_err": mean_frac, "mean_median_dlnS_abserr": mean_dln,
                  "n_zpeak_match": zpeak_ok, "n_subvolumes": NSUB,
                  "criteria": {"frac<=0.02": bool(mean_frac <= 0.02),
                               "dlnS<=0.15": bool(mean_dln <= 0.15),
                               "zpeak>=3of4": bool(zpeak_ok >= 3)},
                  "PASS": gate_v2_pass}
out["gate_v2"] = gv2; flush()
log(f"GATE V2: mean_frac={mean_frac*100:.2f}% mean_dlnS={mean_dln:.4f} zpeak_match={zpeak_ok}/4 -> "
    f"{'PASS' if gate_v2_pass else 'FAIL'}")

if not gate_v2_pass:
    out["VERDICT"] = {"word": "ESTIMATOR-BLOCKED",
                      "detail": "gate v2 (fair regime) failed; cross-code genuinely estimator-blocked on Abacus",
                      "gate_v2_summary": gv2["summary"]}
    flush(); log("GATE V2 FAILED — cross-code estimator-blocked. STOPPING per amendment."); sys.exit(0)

# =========================================================================
# SCIENCE RUNS — corner-equivalent + full population (primary tile T=8, gated grain)
# =========================================================================
BEST_T = 8
def run_config(thr, key):
    rec = {}
    for T in (2, 4, 8):
        Stot, Sint, per = [], [], []
        for si, sd in enumerate(snapdata):
            pos = sd["pos"][sd["mass"] > thr]
            r = tiled_S(pos, T, SEED_BASE + 1000000*T + 1000*si)
            r.update(a=sd["a"], z=sd["z"], n=int(len(pos)))
            per.append(r); Stot.append(r["S_total"]); Sint.append(r["S_intra"])
        an_t = analyze([p["a"] for p in per], Stot)
        an_e = analyze([p["a"] for p in per], Sint)
        rec[str(T)] = {"per_snap": per, "S_total_analysis": an_t, "S_extensive_analysis": an_e}
        out[key] = rec; flush()
        nfl = sum(p["n_flagged"] for p in per)
        log(f"  [{key}] T={T}: z_peak={an_t['z_peak']:.3f} w0={an_t['w0']:.3f} wa={an_t['wa']:.3f} "
            f"thaw={an_t['thawing']} maha={an_t['maha']:.3f} chi2dL={an_t['chi2_minus_lcdm']:+.3f} "
            f"occ_max={max(p['occ_max'] for p in per)} flagged={nfl}")
    return rec

log("=== CORNER-EQUIVALENT 7.425e11 ===")
out["corner_7.425e11"] = run_config(CORNER, "corner_7.425e11"); flush()
log("=== FULL POPULATION 2.109e11 ===")
out["full_2.109e11"] = run_config(FLOOR, "full_2.109e11"); flush()

# ---- grid caveat ----
tng = json.load(open(CEP / "large_volume" / "results.json"))
recs = tng["stage2_primary"]["records"]
a_tng = np.array([r["a"] for r in recs]); S_tng = np.array([r["S"] for r in recs])
full = analyze(a_tng, S_tng)
a_ab = np.array(sorted(s["a"] for s in snapdata))
S_re = np.exp(np.interp(np.log(a_ab), np.log(a_tng), np.log(S_tng)))
regrid = analyze(a_ab, S_re)
out["grid_caveat"] = {
    "method": "TNG300 large_volume corner S(a) reprojected on Abacus a-grid (truncated a<=0.8333)",
    "tng_full_grid": {k: full[k] for k in ("z_peak", "w0", "wa", "cross_z", "maha")},
    "tng_on_abacus_grid": {k: regrid[k] for k in ("z_peak", "w0", "wa", "cross_z", "maha")},
    "delta": {"w0": regrid["w0"]-full["w0"], "wa": regrid["wa"]-full["wa"],
              "cross_z": (regrid["cross_z"] or np.nan)-(full["cross_z"] or np.nan),
              "maha": regrid["maha"]-full["maha"]}}
flush()
log(f"GRID CAVEAT: TNG full ({full['w0']:.3f},{full['wa']:.3f}) -> Abacus-grid "
    f"({regrid['w0']:.3f},{regrid['wa']:.3f}) Dw0={out['grid_caveat']['delta']['w0']:+.3f} "
    f"Dwa={out['grid_caveat']['delta']['wa']:+.3f} Dmaha={out['grid_caveat']['delta']['maha']:+.3f}")

# ---- verdict (corner, primary tile T=8, S_total) ----
v = out["corner_7.425e11"][str(BEST_T)]["S_total_analysis"]
def verdict(a):
    interior = a["z_peak"] is not None and 0.3 <= a["z_peak"] <= 1.0 and not a["peak_at_endpoint"]
    thaw = a["wa"] < 0; beats = a["maha"] < LCDM_3SIGMA
    n = sum([interior, thaw, beats])
    if n == 3: return "LAW-LIKE"
    if n == 0: return "CODE-SPECIFIC"
    return "PARTIAL"
vw = verdict(v); vfull = verdict(out["full_2.109e11"][str(BEST_T)]["S_total_analysis"])
out["VERDICT"] = {"word": vw, "gate": "v2 (fair-regime subvolume) PASS", "best_tile": BEST_T,
                  "config": "corner_7.425e11 S_total", "z_peak": v["z_peak"],
                  "peak_at_endpoint": v["peak_at_endpoint"], "w0": v["w0"], "wa": v["wa"],
                  "thawing": v["thawing"], "maha": v["maha"], "beats_lcdm": bool(v["maha"] < LCDM_3SIGMA),
                  "chi2_minus_lcdm": v["chi2_minus_lcdm"],
                  "n_corner": out["corner_7.425e11"][str(BEST_T)]["per_snap"][-1]["n"],
                  "full_population_companion_verdict": vfull,
                  "components": {"interior_peak": bool(0.3 <= (v["z_peak"] or -9) <= 1.0 and not v["peak_at_endpoint"]),
                                 "thawing": bool(v["wa"] < 0), "beats_lcdm": bool(v["maha"] < LCDM_3SIGMA)}}
flush()
log("=" * 70)
log(f"VERDICT: {vw}  corner T={BEST_T} z_peak={v['z_peak']:.3f} w0={v['w0']:.3f} wa={v['wa']:.3f} "
    f"thaw={v['thawing']} maha={v['maha']:.3f} beats_lcdm={v['maha']<LCDM_3SIGMA} | full-pop: {vfull}")
log("DONE"); flush()
