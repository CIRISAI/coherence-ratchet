#!/usr/bin/env python3
"""
retention_v2: frozen B-total S(a) on CUMULATIVE mass thresholds (monotone unit set),
scanned across the mass axis, to test whether DESI-fit quality extremizes at the SHM
efficiency peak (~10^11.8 Msun/h). Spec pre-committed in DECISIONS.md.

S_gpu / _cholesky_inplace / make_xi_table copied VERBATIM from ../large_volume/run_test.py
(not imported). CPL projection exec-lifted from ../epoch_check/cpl_projection.py. Real
likelihood reused from ../desi_likelihood_v2/likelihood_fit.py. Incremental flush per
threshold and per snapshot.
"""
import json, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
CEP = HERE.parent
DATA = CEP / "large_volume" / "data"
HG = CEP / "halo_grain"
EPOCH = CEP / "epoch_check"
DESIV2 = CEP / "desi_likelihood_v2"
sys.path.insert(0, str(HG)); sys.path.insert(0, str(CEP))

import s_of_a as S

# ---- exec-lift CPL projection functions (Backgrounds + Projections, no CAMELS load) ----
csrc = (EPOCH / "cpl_projection.py").read_text()
cpl_ns = {"np": np}
exec("import numpy as np\nfrom scipy.integrate import quad\n"
     "from scipy.interpolate import CubicSpline\nfrom scipy.optimize import minimize\n"
     "C_KM = 299792.458\nZ_STAR = 1089.0\n", cpl_ns)
body = csrc.split("# 2. Backgrounds.")[1].split("# 4. Run.")[0]
exec(compile(body, str(EPOCH / "cpl_projection.py"), "exec"), cpl_ns)
make_f_fw = cpl_ns["make_f_fw"]; project_distance = cpl_ns["project_distance"]
crossing_z = cpl_ns["crossing_z"]

# ---- reuse the real DESI likelihood (module-level: loads DESI data + LCDM baseline) ----
sys.path.insert(0, str(DESIV2))
import likelihood_fit as lf

# Mahalanobis to DESI DR2 (identical to run_test.py)
COV = np.array([[0.055**2, -0.7*0.055*0.20], [-0.7*0.055*0.20, 0.20**2]])
COVINV = np.linalg.inv(COV)
maha = lambda w0, wa: float(np.sqrt(np.array([w0+0.838, wa+0.62]) @ COVINV
                                    @ np.array([w0+0.838, wa+0.62])))
OM_PROJ = 0.3155

# ---------------------------------------------------------------------------
# GPU machinery — copied verbatim from ../large_volume/run_test.py
# ---------------------------------------------------------------------------
import cupy as cp

def make_xi_table(ps, R_smooth=1.0, rmin=0.02, rmax=180.0, n=400_000):
    xi = ps.xi_spline(R_smooth)
    sig2 = ps.sigma2_R(R_smooth)
    r = np.logspace(np.log10(rmin), np.log10(rmax), n)
    return cp.asarray(r), cp.asarray(xi(r) / sig2), float(sig2)

def _cholesky_inplace(C, bs=2048):
    from cupyx.scipy.linalg import solve_triangular
    k = C.shape[0]
    for j in range(0, k, bs):
        je = min(j + bs, k)
        Cjj = C[j:je, j:je]
        if j > 0:
            Lp = C[j:je, :j]
            Cjj -= Lp @ Lp.T
        try:
            Ld = cp.linalg.cholesky(Cjj)
        except Exception:
            return False
        if bool(cp.isnan(cp.diagonal(Ld)).any()) or bool((cp.diagonal(Ld) <= 0).any()):
            return False
        C[j:je, j:je] = Ld
        if je < k:
            panel = C[je:, j:je]
            if j > 0:
                panel -= C[je:, :j] @ C[j:je, :j].T
            C[je:, j:je] = solve_triangular(Ld, panel.T, lower=True).T
    return True

def S_gpu(pos, box, xr, xv, jitter=0.0, guards=False, tile=1024):
    from cupyx.scipy.linalg import solve_triangular
    k = len(pos)
    P = cp.asarray(pos, dtype=cp.float64)
    C = cp.empty((k, k), dtype=cp.float64)
    for i0 in range(0, k, tile):
        i1 = min(i0 + tile, k)
        d2 = cp.zeros((i1 - i0, k), dtype=cp.float64)
        for ax in range(3):
            dx = cp.abs(P[i0:i1, ax][:, None] - P[None, :, ax])
            cp.minimum(dx, box - dx, out=dx)
            dx *= dx
            d2 += dx
        cp.sqrt(d2, out=d2)
        cp.clip(d2, float(xr[0]), float(xr[-1]), out=d2)
        C[i0:i1] = cp.interp(d2, xr, xv)
        del d2, dx
    idx = cp.arange(k)
    C[idx, idx] = 1.0 + jitter
    cp.get_default_memory_pool().free_all_blocks()
    lam_max = None
    if guards:
        x = cp.random.RandomState(0).rand(k)
        for _ in range(50):
            x = C @ x; x /= cp.linalg.norm(x)
        lam_max = float(x @ (C @ x))
        del x
    ok = _cholesky_inplace(C)
    if not ok:
        del C
        cp.get_default_memory_pool().free_all_blocks()
        return None
    Sval = float(-2.0 * cp.log(cp.diagonal(C)).sum())
    del C
    cp.get_default_memory_pool().free_all_blocks()
    return dict(S=Sval, k=k, lam_max=lam_max)

# ---------------------------------------------------------------------------
# Data + TNG power spectrum
# ---------------------------------------------------------------------------
SNAPS = [25, 30, 33, 36, 39, 42, 45, 47, 49, 51, 53, 55, 56, 59, 61,
         63, 65, 67, 70, 72, 74, 76, 79, 82, 87, 99]
BOX = 205.0
CAP = 38000
SEED_BASE = 20260710

snapdata = []
for s in SNAPS:
    d = np.load(DATA / f"tng300_groups_{s:03d}.npz")
    snapdata.append(dict(snap=s, z=float(d["z"]), a=float(d["a"]),
                         pos=d["pos"].astype(np.float64),
                         m200=d["m200"].astype(np.float64)))

# TNG cosmology power spectrum (matches run_test.py post-gate patch)
S.OM, S.OL, S.OB, S.H0H, S.NS, S.SIGMA8 = 0.3089, 0.6911, 0.0486, 0.6774, 0.9667, 0.8159
ps_tng = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8)
XR, XV, SIG2 = make_xi_table(ps_tng)

THRESHOLDS = np.logspace(11.0, 13.0, 10)   # Msun/h

# LCDM baseline (real likelihood), computed once
LCDM = lf.profile_fixedshape(lf.f_lcdm, use_cmb=True)
LCDM_CHI2 = LCDM["chi2"]

RES = HERE / "results.json"
out = {"date": "2026-07-10", "box": "TNG300-1 205 Mpc/h", "cap": CAP,
       "cosmology": dict(Om=0.3089, h=0.6774), "Om_proj": OM_PROJ,
       "seed_formula": "SEED_BASE + 1000*thr_index + snap",
       "lcdm_chi2": LCDM_CHI2,
       "thresholds_Msunh": THRESHOLDS.tolist(),
       "thresholds_log10": np.log10(THRESHOLDS).tolist(),
       "snaps": SNAPS, "decisions": "DECISIONS.md (pre-committed)",
       "shm_peak_ref_log10Msunh": 11.8, "shm_band_log10Msunh": [11.80, 11.92],
       "per_threshold": []}
def flush():
    with open(RES, "w") as fh:
        json.dump(out, fh, indent=1)
flush()

T0 = time.time()
def log(m): print(f"[{time.time()-T0:7.1f}s] {m}", flush=True)
log(f"LCDM baseline chi2 = {LCDM_CHI2:.4f} (Om={LCDM['Om']:.4f})")

for ti, thr in enumerate(THRESHOLDS):
    rec = {"thr_Msunh": float(thr), "log10_thr": float(np.log10(thr)),
           "records": []}
    n_capped = 0
    for sd in snapdata:
        sel = sd["m200"] > thr
        pos = sd["pos"][sel]
        n_above = int(len(pos))
        capped = n_above > CAP
        if capped:
            n_capped += 1
            seed = SEED_BASE + 1000 * ti + sd["snap"]
            rs = np.random.RandomState(seed)
            idx = rs.choice(n_above, CAP, replace=False)
            pos_use = pos[idx]
        else:
            pos_use = pos
        r = {"a": sd["a"], "z": sd["z"], "n_above": n_above, "capped": bool(capped)}
        if len(pos_use) < 3:
            r["S"] = None; r["k"] = int(len(pos_use))
        else:
            g = S_gpu(pos_use, BOX, XR, XV)
            if g is None:
                g = S_gpu(pos_use, BOX, XR, XV, jitter=1e-8)
                if g is None:
                    raise RuntimeError(f"Cholesky failed thr={thr:.2e} a={sd['a']:.3f}")
                g["jitter"] = 1e-8
            r["S"] = g["S"]; r["k"] = g["k"]
        rec["records"].append(r)
        flush()
        log(f"thr={np.log10(thr):.2f} a={sd['a']:.3f} z={sd['z']:.2f} "
            f"n_above={n_above} k={r['k']} cap={capped} S={r['S']}")
    rec["n_capped_snaps"] = n_capped
    rec["fully_capped"] = bool(n_capped == len(snapdata))
    rec["cap_limited"] = bool(n_capped > 0)

    # ---- frozen analysis on this threshold's S(a) ----
    a = np.array([x["a"] for x in rec["records"]], float)
    Sa = np.array([x["S"] if x["S"] is not None else np.nan for x in rec["records"]], float)
    ok = np.isfinite(Sa) & (Sa > 0)
    a_ok, S_ok = a[ok], Sa[ok]
    order = np.argsort(a_ok)
    a_ok, S_ok = a_ok[order], S_ok[order]
    rec["n_valid"] = int(len(a_ok))
    if len(a_ok) >= 4:
        # global-max peak epoch (robust; NOT the spline sign-change finder)
        imax = int(np.argmax(S_ok))
        a_peak = float(a_ok[imax])
        rec["z_peak_globalmax"] = float(1.0 / a_peak - 1.0)
        rec["S_max"] = float(S_ok[imax])
        rec["peak_at_endpoint"] = bool(imax == 0 or imax == len(a_ok) - 1)
        # CPL projection -> Mahalanobis to DESI
        f = make_f_fw(a_ok, S_ok)
        w0, wa, c2proj = project_distance(f, Om=OM_PROJ, use_cmb=True)
        rec["cpl"] = dict(w0=float(w0), wa=float(wa),
                          cross_z=crossing_z(w0, wa), maha=maha(w0, wa),
                          proj_chi2=float(c2proj))
        # real DESI DR2 likelihood chi2 (fixed frozen shape)
        prof = lf.profile_fixedshape(lf.make_f_fw(a_ok, S_ok), use_cmb=True)
        rec["likelihood"] = dict(chi2=float(prof["chi2"]), Om=float(prof["Om"]),
                                 chi2_minus_lcdm=float(prof["chi2"] - LCDM_CHI2))
        log(f"  thr={np.log10(thr):.2f} DONE: z_peak={rec['z_peak_globalmax']:.3f} "
            f"maha={rec['cpl']['maha']:.3f} chi2={rec['likelihood']['chi2']:.3f} "
            f"(dLCDM={rec['likelihood']['chi2_minus_lcdm']:+.3f}) "
            f"cap_limited={rec['cap_limited']} fully={rec['fully_capped']}")
    else:
        rec["z_peak_globalmax"] = None
        log(f"  thr={np.log10(thr):.2f} too few valid snaps ({len(a_ok)})")
    out["per_threshold"].append(rec)
    flush()

log("=" * 70)
log("ALL THRESHOLDS DONE")
flush()
