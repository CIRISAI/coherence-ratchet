#!/usr/bin/env python3
"""
Functional-falsification: build ALTERNATIVE structure functionals F(a) on the SAME
TNG300-1 halo catalogs, map each through the SAME stock rule rho_DE(a) ~ F(a), and fit
each with the SAME real-DESI-DR2 + theta* likelihood machinery (2 free params: Om, beta).

Pre-committed operationalizations: functional_falsification/DECISIONS.md.
CPU-only. Incremental writes to results.json after every functional.
"""
import json, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
CEP = HERE.parent
DATA = CEP / "large_volume" / "data"
LV = CEP / "large_volume" / "results.json"

# --- reuse the real-DESI likelihood machinery verbatim (imports DESI data on load) ---
sys.path.insert(0, str(CEP / "desi_likelihood_v2"))
sys.path.insert(0, str(CEP / "halo_grain")); sys.path.insert(0, str(CEP))
import importlib.util
spec = importlib.util.spec_from_file_location("lf", CEP / "desi_likelihood_v2" / "likelihood_fit.py")
lf = importlib.util.module_from_spec(spec); spec.loader.exec_module(lf)
import s_of_a as S                       # dln_dlna (same finite-diff operator as the framework)

SNAPS = [25, 30, 36, 42, 49, 56, 65, 76, 87, 99]
BOX = 205.0
NGRID_PRIMARY = 51                       # ~4.02 Mpc/h
NGRID_SENS = {"2Mpc": 102, "4Mpc": 51, "8Mpc": 26}

T0 = time.time()
def log(m): print(f"[{time.time()-T0:6.1f}s] {m}", flush=True)

RES = HERE / "results.json"
OUT = {"date": "2026-07-10", "box": "TNG300-1 205 Mpc/h",
       "decisions": "functional_falsification/DECISIONS.md (pre-committed)",
       "held_fixed": "same catalogs, same stock map rho_DE~F(a), same DESI DR2+theta* "
                     "likelihood, 2 free params (Om,beta), AIC/BIC at matched k=2",
       "grid_primary_Mpc_h": BOX / NGRID_PRIMARY}
def flush():
    RES.write_text(json.dumps(OUT, indent=1))

# ---------------------------------------------------------------------------
# Load catalogs (positions Mpc/h, m200 Msun/h)
# ---------------------------------------------------------------------------
CAT = []
for s in SNAPS:
    d = np.load(DATA / f"tng300_groups_{s:03d}.npz")
    CAT.append(dict(a=float(d["a"]), z=float(d["z"]),
                    pos=d["pos"].astype(np.float64), m200=d["m200"].astype(np.float64)))
A = np.array([c["a"] for c in CAT])
order = np.argsort(A)
CAT = [CAT[i] for i in order]; A = A[order]
log(f"loaded {len(CAT)} snapshots, a = {np.round(A,3).tolist()}")

# ---------------------------------------------------------------------------
# CIC deposit -> normalized density rho (mean 1) and contrast delta
# ---------------------------------------------------------------------------
def cic_density(pos, box, n, weights=None):
    """periodic CIC onto n^3 grid; returns density normalized to mean 1 (flattened)."""
    g = np.zeros((n, n, n), dtype=np.float64)
    x = (pos / box) * n                      # grid coords in [0,n)
    i = np.floor(x).astype(np.int64)
    f = x - i
    w = np.ones(len(pos)) if weights is None else np.asarray(weights, float)
    for dx in (0, 1):
        wx = (1 - f[:, 0]) if dx == 0 else f[:, 0]
        ix = (i[:, 0] + dx) % n
        for dy in (0, 1):
            wy = (1 - f[:, 1]) if dy == 0 else f[:, 1]
            iy = (i[:, 1] + dy) % n
            for dz in (0, 1):
                wz = (1 - f[:, 2]) if dz == 0 else f[:, 2]
                iz = (i[:, 2] + dz) % n
                np.add.at(g, (ix, iy, iz), w * wx * wy * wz)
    g = g.ravel()
    return g / g.mean()                      # mean-1 density

# functional kernels on a mean-1 density field ---------------------------------
def shannon_config_entropy(rho):
    p = rho / rho.sum()
    p = p[p > 0]
    return float(-(p * np.log(p)).sum())

def variance(rho):
    return float(np.var(rho - 1.0))          # Var(delta), delta = rho-1 (mean-0)

def negentropy(rho):
    s2 = variance(rho)
    if s2 <= 0:
        return None
    return float(0.5 * np.log(s2 * (1.0 + s2) / np.log(1.0 + s2)))

# ---------------------------------------------------------------------------
# Fit one F(a) curve through the frozen stock map + real DESI likelihood.
# k_params=2 (Om, beta) exactly like the framework/LCDM rows.
# ---------------------------------------------------------------------------
def sign_law_w(a, Fa):
    d = S.dln_dlna(np.asarray(a, float), np.asarray(Fa, float))
    return -1.0 - d / 3.0                     # w(a)

def peak_epoch_z(a, Fa):
    """interior peak (thaw signature): z at max of F if the max is not the last point."""
    Fa = np.asarray(Fa, float); a = np.asarray(a, float)
    j = int(np.argmax(Fa))
    if j == len(Fa) - 1 or j == 0:
        return None
    return float(1.0 / a[j] - 1.0)

def fit_curve(a, Fa, name):
    a = np.asarray(a, float); Fa = np.asarray(Fa, float)
    ok = np.isfinite(Fa)
    rec = {"name": name, "a": a.tolist(), "F": [None if not np.isfinite(v) else float(v) for v in Fa]}
    if not ok.all():
        rec.update(status="FAILED", reason="non-finite F(a)"); return rec
    if np.any(Fa <= 0):
        rec.update(status="FAILED", reason="F(a)<=0 -> rho_DE<0 unphysical under stock map",
                   min_F=float(Fa.min())); return rec
    w = sign_law_w(a, Fa)
    rec["w_today"] = float(w[-1])
    rec["w_of_a"] = w.tolist()
    rec["peak_epoch_z"] = peak_epoch_z(a, Fa)
    rec["F_first_last"] = [float(Fa[0]), float(Fa[-1])]
    # frozen stock background f_DE(a)=F(a)/F(1), fit (Om,beta) with real DESI likelihood
    f_de = lf.make_f_fw(a, Fa)                # log-log spline, flat below a_min (same as framework)
    for tag, use_cmb in (("with_cmb", True), ("bao_only", False)):
        pr = lf.profile_fixedshape(f_de, use_cmb=use_cmb)
        n = lf.N_BAO + (1 if use_cmb else 0)
        aic, bic = lf.aic_bic(pr["chi2"], 2, n)
        rec[tag] = {"chi2": float(pr["chi2"]), "Om": float(pr["Om"]),
                    "k_params": 2, "AIC": float(aic), "BIC": float(bic), "n": n}
    rec["status"] = "fit"
    return rec

# verdict against the pre-registered DESI-quadrant rule (thaw AND beat LCDM) --------
LCDM_CHI2_CMB = None   # filled from anchors below
def verdict(rec):
    if rec.get("status") != "fit":
        return "FAILED (" + rec.get("reason", "?") + ")"
    thaws = (rec["peak_epoch_z"] is not None) and (-1.0 < rec["w_today"] <= -0.84)
    beats = rec["with_cmb"]["chi2"] < LCDM_CHI2_CMB
    if thaws and beats:
        return "LANDS IN DESI QUADRANT (thaws + beats LCDM)"
    parts = []
    parts.append("thaws" if thaws else f"no-thaw(w_today={rec['w_today']:+.3f},peak_z={rec['peak_epoch_z']})")
    parts.append(f"beats-LCDM(chi2={rec['with_cmb']['chi2']:.2f})" if beats
                 else f"does-NOT-beat-LCDM(chi2={rec['with_cmb']['chi2']:.2f} vs {LCDM_CHI2_CMB:.2f})")
    return "OUTSIDE quadrant: " + ", ".join(parts)

# ---------------------------------------------------------------------------
# ANCHORS: framework (=frozen log-det S(a)), LCDM, CPL, cell-grain (fixed CPL)
# ---------------------------------------------------------------------------
log("computing anchors (framework / LCDM / CPL) via the real DESI machinery ...")
anchors = {}
for name, res, k in [("framework", lf.profile_fixedshape(lf.F_FW, True), 2),
                     ("LCDM", lf.profile_fixedshape(lf.f_lcdm, True), 2)]:
    n = lf.N_BAO + 1
    aic, bic = lf.aic_bic(res["chi2"], k, n)
    anchors[name] = {"chi2": float(res["chi2"]), "Om": float(res["Om"]),
                     "k_params": k, "AIC": float(aic), "BIC": float(bic)}
cpl = lf.profile_cpl(True)
n = lf.N_BAO + 1
aic, bic = lf.aic_bic(cpl["chi2"], 4, n)
anchors["CPL"] = {"chi2": float(cpl["chi2"]), "Om": float(cpl["Om"]), "w0": float(cpl["w0"]),
                  "wa": float(cpl["wa"]), "k_params": 4, "AIC": float(aic), "BIC": float(bic)}
# framework w_today + peak from the frozen S(a) itself
lv = json.load(open(LV)); recs = lv["stage2_primary"]["records"]
aS = np.array([r["a"] for r in recs]); SS = np.array([r["S"] for r in recs])
o2 = np.argsort(aS); aS, SS = aS[o2], SS[o2]
anchors["framework"]["w_today"] = float(sign_law_w(aS, SS)[-1])
anchors["framework"]["peak_epoch_z"] = peak_epoch_z(aS, SS)
LCDM_CHI2_CMB = anchors["LCDM"]["chi2"]

# cell-grain: fixed CPL (w0,wa)=(-0.897,-0.099) through the machinery, k=2 (no free shape)
w0c, wac = -0.897, -0.099
cg = lf.profile_fixedshape(lambda a: lf.f_cpl(a, w0c, wac), True)
aic, bic = lf.aic_bic(cg["chi2"], 2, lf.N_BAO + 1)
anchors["cell_grain_fixedCPL"] = {"chi2": float(cg["chi2"]), "Om": float(cg["Om"]),
    "w0": w0c, "wa": wac, "k_params": 2, "AIC": float(aic), "BIC": float(bic),
    "caveat": "cell scale is a FREE CHOICE (results.json desi_matching_cell_scale) — hidden tuned param"}
OUT["anchors"] = anchors
flush()
log(f"anchors: framework chi2={anchors['framework']['chi2']:.2f} "
    f"LCDM={anchors['LCDM']['chi2']:.2f} CPL={anchors['CPL']['chi2']:.2f} "
    f"cell-grain={anchors['cell_grain_fixedCPL']['chi2']:.2f}")

# ---------------------------------------------------------------------------
# F4 = k(a): unit count above the frozen corner threshold (no correlation content)
# ---------------------------------------------------------------------------
OUT["functionals"] = {}
k_corner = lv["stage0"]["k_at_corner"]
rec = fit_curve(A, np.array(k_corner, float), "F4_k_of_a_count")
rec["desc"] = "halo count above frozen corner threshold (bookkeeping control, no copula)"
OUT["functionals"]["F4_k_of_a"] = rec; flush()
log(f"F4 k(a): {verdict(rec)}")

# ---------------------------------------------------------------------------
# F1/F2/F3: gridded functionals at primary 4 Mpc/h (+ count & mass weights)
# with 2/8 Mpc/h sensitivity for the primary variant.
# ---------------------------------------------------------------------------
def build_grid_functionals(weight, ngrid):
    Sc, Jn, Var = [], [], []
    for c in CAT:
        w = None if weight == "count" else c["m200"]
        rho = cic_density(c["pos"], BOX, ngrid, weights=w)
        Sc.append(shannon_config_entropy(rho))
        Var.append(variance(rho))
        Jn.append(negentropy(rho))
    return np.array(Sc), np.array(Jn, dtype=float), np.array(Var)

for weight in ("count", "mass"):
    Sc, Jn, Var = build_grid_functionals(weight, NGRID_PRIMARY)
    log(f"[{weight}] 4Mpc: S_c={np.round(Sc,3).tolist()}")
    log(f"[{weight}] 4Mpc: J  ={np.round(Jn,3).tolist()}")
    log(f"[{weight}] 4Mpc: var={np.round(Var,4).tolist()}")
    r1 = fit_curve(A, Sc, f"F1_shannon_Sc_{weight}_4Mpc")
    r1["desc"] = f"Das-Pandey Shannon config entropy, {weight}-weighted, 4 Mpc/h"
    r2 = fit_curve(A, Jn, f"F2_negentropy_{weight}_4Mpc")
    r2["desc"] = f"Sarkar one-point negentropy, {weight}-weighted, 4 Mpc/h"
    r3 = fit_curve(A, Var, f"F3_variance_{weight}_4Mpc")
    r3["desc"] = f"variance/amplitude control sigma^2(delta), {weight}-weighted, 4 Mpc/h"
    for key, r in [(f"F1_shannon_{weight}", r1), (f"F2_negentropy_{weight}", r2),
                   (f"F3_variance_{weight}", r3)]:
        OUT["functionals"][key] = r
    flush()
    log(f"[{weight}] F1 {verdict(r1)}")
    log(f"[{weight}] F2 {verdict(r2)}")
    log(f"[{weight}] F3 {verdict(r3)}")

# grid-scale sensitivity (count weight) at 2 and 8 Mpc/h for F1/F2/F3
OUT["grid_sensitivity"] = {}
for tag, ng in (("2Mpc", NGRID_SENS["2Mpc"]), ("8Mpc", NGRID_SENS["8Mpc"])):
    Sc, Jn, Var = build_grid_functionals("count", ng)
    sens = {}
    for nm, curve in [("F1_shannon", Sc), ("F2_negentropy", Jn), ("F3_variance", Var)]:
        r = fit_curve(A, curve, f"{nm}_count_{tag}")
        sens[nm] = {"w_today": r.get("w_today"), "peak_epoch_z": r.get("peak_epoch_z"),
                    "chi2_cmb": r.get("with_cmb", {}).get("chi2"),
                    "status": r["status"], "verdict": verdict(r)}
    OUT["grid_sensitivity"][tag] = sens
    flush()
    log(f"grid {tag}: " + "; ".join(f"{k}:{v['verdict']}" for k, v in sens.items()))

# ---------------------------------------------------------------------------
# F5 = PEDE (analytic zero-parameter benchmark, NOT structure-derived)
# f_DE(a) = 1 - tanh(log10(1/a));  w_today from its own sign law
# ---------------------------------------------------------------------------
def f_pede(a):
    a = np.atleast_1d(np.asarray(a, float))
    return 1.0 - np.tanh(np.log10(1.0 / np.clip(a, 1e-8, 1.0)))
# PEDE F(a) on the same a-grid for the sign-law w_today + fit
Fpede = f_pede(A)
rp = {"name": "F5_PEDE", "desc": "PEDE Omega_DE(z)=Omega_DE0[1-tanh(log10(1+z))]; zero-param benchmark",
      "a": A.tolist(), "F": Fpede.tolist(),
      "w_today": float(sign_law_w(A, Fpede)[-1]), "peak_epoch_z": peak_epoch_z(A, Fpede)}
for tag, use_cmb in (("with_cmb", True), ("bao_only", False)):
    pr = lf.profile_fixedshape(f_pede, use_cmb=use_cmb)
    n = lf.N_BAO + (1 if use_cmb else 0)
    aic, bic = lf.aic_bic(pr["chi2"], 2, n)
    rp[tag] = {"chi2": float(pr["chi2"]), "Om": float(pr["Om"]), "k_params": 2,
               "AIC": float(aic), "BIC": float(bic), "n": n}
rp["status"] = "fit"
OUT["functionals"]["F5_PEDE"] = rp; flush()
log(f"F5 PEDE: {verdict(rp)}")

# ---------------------------------------------------------------------------
# Summary verdict payload
# ---------------------------------------------------------------------------
OUT["verdicts"] = {k: verdict(v) for k, v in OUT["functionals"].items()}
OUT["lcdm_chi2_cmb"] = LCDM_CHI2_CMB
flush()
log("DONE. wrote results.json")
