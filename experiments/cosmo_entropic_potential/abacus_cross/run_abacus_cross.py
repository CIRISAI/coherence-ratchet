#!/usr/bin/env python3
"""
abacus_cross — cross-code test of the DE leg on AbacusSummit_small_c000_ph3000 (500 Mpc/h,
CompaSO). Reuses the gate-validated nested-tile estimator (../full_population) verbatim; frozen
downstream (op_B model-xi with the ABACUS cosmology, sign law, CPL projection, DESI DR2
likelihood). Pre-committed in DECISIONS.md before any Abacus S/w was seen.

Stages: (0) load Abacus snapshots; (1) Abacus-native GATE at a cluster threshold reachable by
exact-det, tiled vs exact; (2) corner-equivalent 7.425e11 Msun/h (verdict config); (3) full
population 2.109e11 Msun/h (100-particle floor, selection-free companion); (4) snapshot-grid
caveat: re-project TNG300 corner S(a) on the Abacus a-grid; (5) verdict. Incremental flush.
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

# ---- lift CPL projection defs verbatim ----
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
def maha_to(w0, wa, w0e, wae):
    d = np.array([w0-w0e, wa-wae]); return float(np.sqrt(d @ COVINV @ d))
OM_PROJ = 0.3155
BOX = 500.0
SEED_BASE = 20260711
TILE_MAX = 38000
LCDM_3SIGMA = 3.28

# ---- Abacus c000 cosmology for the xi model (DECISIONS §7) ----
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

def analyze(a, Sa, w0e=None, wae=None):
    a = np.asarray(a, float); Sa = np.asarray(Sa, float)
    ok = np.isfinite(Sa) & (Sa > 0); a_ok, S_ok = a[ok], Sa[ok]
    o = np.argsort(a_ok); a_ok, S_ok = a_ok[o], S_ok[o]
    if len(a_ok) < 4: return {"z_peak": None}
    imax = int(np.argmax(S_ok))
    w0, wa, c2 = project_distance(make_f_fw(a_ok, S_ok), Om=OM_PROJ, use_cmb=True)
    prof = lf.profile_fixedshape(lf.make_f_fw(a_ok, S_ok), use_cmb=True)
    r = dict(z_peak=float(1/a_ok[imax]-1), peak_at_endpoint=bool(imax in (0, len(a_ok)-1)),
             w0=float(w0), wa=float(wa), thawing=bool(wa < 0), cross_z=crossing_z(w0, wa),
             maha=maha_pt(w0, wa), chi2=float(prof["chi2"]),
             chi2_minus_lcdm=float(prof["chi2"]-LCDM_CHI2))
    if w0e is not None:
        r["maha_to_exact"] = maha_to(w0, wa, w0e, wae)
    return r

# ---------------------------------------------------------------------------
# Stage 0: load Abacus snapshots
# ---------------------------------------------------------------------------
T0 = time.time(); log = lambda m: print(f"[{time.time()-T0:7.1f}s] {m}", flush=True)
snapdata = []
for f in sorted(ABACUS.glob("abacus_z*.npz")):
    d = np.load(f)
    snapdata.append(dict(z=float(d["z"]), a=float(d["a"]),
                         pos=d["pos"].astype(np.float64), mass=d["mass"].astype(np.float64),
                         pm=float(d["particle_mass"])))
snapdata.sort(key=lambda s: s["a"])
PM = snapdata[0]["pm"]
log(f"loaded {len(snapdata)} Abacus snapshots, a={[round(s['a'],3) for s in snapdata]}, pm={PM:.3e}")

ps = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8)
XR, XV, SIG2 = make_xi_table(ps)
LCDM_CHI2 = lf.profile_fixedshape(lf.f_lcdm, use_cmb=True)["chi2"]
log(f"Abacus-cosmology xi table built. LCDM DESI chi2={LCDM_CHI2:.4f}")

RES = HERE / "results.json"
out = {"date": "2026-07-11", "box": "AbacusSummit_small_c000_ph3000 500 Mpc/h",
       "cosmology": dict(Om=S.OM, OL=S.OL, Ob=S.OB, h=S.H0H, ns=S.NS, sigma8=S.SIGMA8),
       "particle_mass_Msun_h": PM, "lcdm_chi2": LCDM_CHI2,
       "a_grid": [s["a"] for s in snapdata], "z_grid": [s["z"] for s in snapdata],
       "counts": {}, "gate": {}, "corner_7.425e11": {}, "full_2.109e11": {},
       "grid_caveat": {}, "VERDICT": {}}
def flush():
    with open(RES, "w") as fh: json.dump(out, fh, indent=1)

# count tables
for thr, tag in [(7.425e11, "corner_7.425e11"), (2.109e11, "full_2.109e11")]:
    out["counts"][tag] = [int((s["mass"] > thr).sum()) for s in snapdata]
log(f"corner counts: {out['counts']['corner_7.425e11']}")
log(f"full   counts: {out['counts']['full_2.109e11']}")

# ---------------------------------------------------------------------------
# Stage 1: GATE — lowest cluster threshold with max-count <= 35000 (exact reachable)
# ---------------------------------------------------------------------------
def maxcount(thr): return max(int((s["mass"] > thr).sum()) for s in snapdata)
lo, hi = 7.425e11, 1e15
for _ in range(60):
    mid = np.sqrt(lo*hi)
    if maxcount(mid) > 35000: lo = mid
    else: hi = mid
GATE_THR = hi
gate_counts = [int((s["mass"] > GATE_THR).sum()) for s in snapdata]
log(f"GATE threshold = {GATE_THR:.3e} Msun/h ({GATE_THR/PM:.0f} particles); counts={gate_counts} max={max(gate_counts)}")

# exact S(a) at gate threshold
gate_exact_S, gate_a = [], []
for si, sd in enumerate(snapdata):
    pos = sd["pos"][sd["mass"] > GATE_THR]
    s = S_gpu(pos, BOX, XR, XV)
    gate_exact_S.append(s); gate_a.append(sd["a"])
    log(f"  gate exact a={sd['a']:.3f}: k={len(pos)} S={s:.2f}")
ex = analyze(gate_a, gate_exact_S)
out["gate"]["exact"] = {"threshold_Msun_h": GATE_THR, "counts": gate_counts,
                        "S_of_a": gate_exact_S, "analysis": ex}
flush()
log(f"  GATE exact: z_peak={ex['z_peak']:.3f} w0={ex['w0']:.3f} wa={ex['wa']:.3f} maha={ex['maha']:.3f}")

# tiled at each T vs exact
out["gate"]["tiled"] = {}
for T in (2, 4, 8):
    Stot = []
    for si, sd in enumerate(snapdata):
        pos = sd["pos"][sd["mass"] > GATE_THR]
        r = tiled_S(pos, T, SEED_BASE + 1000000*T + 1000*si)
        Stot.append(r["S_total"])
    an = analyze(gate_a, Stot, ex["w0"], ex["wa"])
    out["gate"]["tiled"][str(T)] = {"S_total_of_a": Stot, "analysis": an}
    flush()
    log(f"  GATE tiled T={T}: z_peak={an['z_peak']:.3f} maha_to_exact={an['maha_to_exact']:.3f}")

gate_pass = {T: out["gate"]["tiled"][str(T)]["analysis"]["maha_to_exact"] <= 1.0 for T in (2, 4, 8)}
passing = [(T, out["gate"]["tiled"][str(T)]["analysis"]["maha_to_exact"]) for T in (2, 4, 8) if gate_pass[T]]
out["gate"]["pass"] = {str(T): bool(gate_pass[T]) for T in (2, 4, 8)}
if not passing:
    out["gate"]["verdict"] = "ESTIMATOR-FAILURE (no tile reproduces exact on Abacus)"
    out["VERDICT"] = {"word": "ESTIMATOR-FAILURE", "detail": "gate failed on Abacus; no cross-code verdict"}
    flush(); log("GATE FAILED — no tile passes. STOPPING per DECISIONS."); sys.exit(0)
BEST_T = sorted(passing, key=lambda x: x[1])[0][0]
out["gate"]["best_tile"] = BEST_T; flush()
log(f"GATE PASSED. best tile T={BEST_T} (min maha_to_exact={dict(passing)[BEST_T]:.3f})")

# ---------------------------------------------------------------------------
# Stage 2/3: science configs — corner-equivalent + full population, all three T
# ---------------------------------------------------------------------------
def run_config(thr, key):
    rec = {}
    for T in (2, 4, 8):
        Stot, Sint, per = [], [], []
        for si, sd in enumerate(snapdata):
            pos = sd["pos"][sd["mass"] > thr]
            r = tiled_S(pos, T, SEED_BASE + 1000000*T + 1000*si)
            r.update(a=sd["a"], z=sd["z"], n=int(len(pos)))
            per.append(r); Stot.append(r["S_total"]); Sint.append(r["S_intra"])
            out[key][str(T)] = {"per_snap": per}; flush()
        an_t = analyze([p["a"] for p in per], Stot)
        an_e = analyze([p["a"] for p in per], Sint)
        rec[str(T)] = {"per_snap": per, "S_total_analysis": an_t, "S_extensive_analysis": an_e}
        out[key] = {**out.get(key, {}), **rec}; flush()
        nfl = sum(p["n_flagged"] for p in per)
        log(f"  [{key}] T={T}: TOTAL z_peak={an_t['z_peak']:.3f} maha={an_t['maha']:.3f} "
            f"wa={an_t['wa']:.3f} thaw={an_t['thawing']} chi2dL={an_t['chi2_minus_lcdm']:+.3f} "
            f"| occ_max={max(p['occ_max'] for p in per)} flagged={nfl}")
    return rec

log("=== CORNER-EQUIVALENT 7.425e11 Msun/h ===")
out["corner_7.425e11"] = run_config(7.425e11, "corner_7.425e11"); flush()
log("=== FULL POPULATION 2.109e11 Msun/h (100-particle floor) ===")
out["full_2.109e11"] = run_config(2.109e11, "full_2.109e11"); flush()

# ---------------------------------------------------------------------------
# Stage 4: snapshot-grid caveat — TNG300 corner S(a) re-projected on the Abacus a-grid
# ---------------------------------------------------------------------------
tng = json.load(open(CEP / "large_volume" / "results.json"))
recs = tng["stage2_primary"]["records"]
a_tng = np.array([r["a"] for r in recs]); S_tng = np.array([r["S"] for r in recs])
full = analyze(a_tng, S_tng)                      # TNG full grid (has a=1)
a_ab = np.array(sorted(s["a"] for s in snapdata))
# regrid TNG S(a) onto the Abacus a-values (log-interp), truncated to a<=0.8333 (Abacus max)
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
log(f"GRID CAVEAT: TNG full-grid (w0,wa,cross)=({full['w0']:.3f},{full['wa']:.3f},{full['cross_z']}) "
    f"-> Abacus-grid ({regrid['w0']:.3f},{regrid['wa']:.3f},{regrid['cross_z']}) "
    f"Dw0={out['grid_caveat']['delta']['w0']:+.3f} Dwa={out['grid_caveat']['delta']['wa']:+.3f}")

# ---------------------------------------------------------------------------
# Stage 5: verdict (read at corner-equivalent, best gate tile, S_total)
# ---------------------------------------------------------------------------
v = out["corner_7.425e11"][str(BEST_T)]["S_total_analysis"]
def verdict(a):
    interior = a["z_peak"] is not None and 0.3 <= a["z_peak"] <= 1.0 and not a["peak_at_endpoint"]
    thaw = a["wa"] < 0
    beats = a["maha"] < LCDM_3SIGMA
    if interior and thaw and beats: return "LAW-LIKE"
    if (not interior) or (not thaw) or (not beats):
        # CODE-SPECIFIC if any hard-fail; PARTIAL if some transfer
        n = sum([interior, thaw, beats])
        return "CODE-SPECIFIC" if n == 0 else ("PARTIAL" if n < 3 else "LAW-LIKE")
    return "PARTIAL"
vw = verdict(v)
vfull = verdict(out["full_2.109e11"][str(BEST_T)]["S_total_analysis"])
out["VERDICT"] = {"word": vw, "best_tile": BEST_T, "config": "corner_7.425e11 S_total",
                  "z_peak": v["z_peak"], "peak_at_endpoint": v["peak_at_endpoint"],
                  "w0": v["w0"], "wa": v["wa"], "thawing": v["thawing"], "maha": v["maha"],
                  "chi2_minus_lcdm": v["chi2_minus_lcdm"], "beats_lcdm": bool(v["maha"] < LCDM_3SIGMA),
                  "n_corner": out["corner_7.425e11"][str(BEST_T)]["per_snap"][-1]["n"],
                  "full_population_companion_verdict": vfull}
flush()
log("=" * 70)
log(f"VERDICT: {vw}  (corner best-tile T={BEST_T}) z_peak={v['z_peak']:.3f} "
    f"w0={v['w0']:.3f} wa={v['wa']:.3f} thaw={v['thawing']} maha={v['maha']:.3f} "
    f"beats_lcdm={v['maha']<LCDM_3SIGMA}")
log(f"full-population companion: {vfull}")
log("DONE"); flush()
