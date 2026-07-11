#!/usr/bin/env python3
"""
GPU-independent measured-vs-model comparison at a CPU-feasible, rule-clean threshold
(2e12 Msun/h: k(a)=1469..13118, k(z=3)=1469>=200, good xi statistics). Same estimator
as DECISIONS.md; computes BOTH measured-C and model-C at the SAME 2e12 halo point set on
CPU (eigvalsh + 1e-12 clip, identical to the frozen op_B), then the full comparison
(w, interior peak, CPL, real DESI chi2). This is the robustness / fallback headline that
does not depend on the contended GPU. Flushes cpu_fallback_results.json incrementally.
"""
import json, sys, time
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline

HERE = Path(__file__).resolve().parent
CEP = HERE.parent
DATA = CEP / "large_volume" / "data"
sys.path.insert(0, str(CEP)); sys.path.insert(0, str(HERE))
import s_of_a as S
import analyze_measured as AM      # analyze(), CPL + DESI chi2 machinery (functions only)

SNAPS = [25, 30, 36, 42, 49, 56, 65, 76, 87, 99]
BOX = 205.0
THR = 2e12
R_MIN, R_MAX, NBINS, TABLE_RMAX, R_SMOOTH = 0.1, BOX / 2.0, 32, 180.0, 1.0
TILE = 2000
CLIP = 1e-12                       # op_B eigenvalue clip

# TNG300 Planck2015 cosmology (matches run_test model-C)
S.OM, S.OL, S.OB, S.H0H, S.NS, S.SIGMA8 = 0.3089, 0.6911, 0.0486, 0.6774, 0.9667, 0.8159
ps = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8)
XI_MODEL = ps.xi_spline(R_SMOOTH); SIG2_MODEL = ps.sigma2_R(R_SMOOTH)

T0 = time.time()
def log(m): print(f"[{time.time()-T0:7.1f}s] {m}", flush=True)

LOG_EDGES = np.logspace(np.log10(R_MIN), np.log10(R_MAX), NBINS + 1)
R_CENT = np.sqrt(LOG_EDGES[:-1] * LOG_EDGES[1:])
VBOX = BOX ** 3
VSHELL = (4.0 / 3.0) * np.pi * (LOG_EDGES[1:] ** 3 - LOG_EDGES[:-1] ** 3)


def periodic_dist_tiled(pos, callback):
    n = len(pos)
    for i0 in range(0, n, TILE):
        i1 = min(i0 + TILE, n)
        d2 = np.zeros((i1 - i0, n))
        for ax in range(3):
            dx = np.abs(pos[i0:i1, ax][:, None] - pos[None, :, ax])
            np.minimum(dx, BOX - dx, out=dx); dx *= dx; d2 += dx
        callback(i0, i1, np.sqrt(d2, out=d2))


def xi_hat_of(pos):
    n = len(pos); counts = np.zeros(NBINS, dtype=np.int64)
    def cb(i0, i1, r):
        rr = r.ravel(); m = (rr >= R_MIN) & (rr <= R_MAX)
        counts[:] += np.bincount(np.digitize(rr[m], LOG_EDGES) - 1,
                                 minlength=NBINS + 1)[:NBINS].astype(np.int64)
    periodic_dist_tiled(pos, cb)
    rr = n * (n - 1) * VSHELL / VBOX
    return counts / rr - 1.0


def measured_table(xi, sig_factor=1.0):
    ok = np.isfinite(xi) & (xi > -1.0)
    sp = CubicSpline(np.log(R_CENT[ok]), np.log1p(xi[ok]))
    sig2 = float(np.expm1(sp(np.log(sig_factor * R_SMOOTH))))
    rlo, rhi = R_CENT[ok].min(), R_CENT[ok].max()
    def fn(r):
        v = np.expm1(sp(np.log(np.clip(r, rlo, rhi))))
        v = np.where(r > R_MAX, 0.0, v)
        return v / sig2
    return fn, sig2


def build_C(pos, valfn):
    n = len(pos); C = np.empty((n, n))
    def cb(i0, i1, r):
        C[i0:i1] = valfn(r)
    periodic_dist_tiled(pos, cb)
    np.fill_diagonal(C, 1.0)
    return C


FLOOR = 1e-3           # clip-robust: drop the near-null noise spectrum below this
def S_decomp(ev, n):
    neg = float(np.abs(ev[ev < 0]).sum() / np.abs(ev).sum())
    n_nonpos = int((ev <= CLIP).sum())
    S_clip = float(-np.log(np.clip(ev, CLIP, None)).sum())          # as-is (op_B)
    clip_contrib = n_nonpos * (-np.log(CLIP))
    S_floor = float(-np.log(ev[ev > FLOOR]).sum())                  # robust (drop noise)
    return dict(S_clip=S_clip, S_floor=S_floor, min_eig=float(ev.min()),
                neg_mass=neg, n_nonpos=n_nonpos,
                clip_frac=float(clip_contrib / S_clip) if S_clip > 0 else 0.0,
                n_below_floor=int((ev <= FLOOR).sum()))


out = {"thr": THR, "box": BOX, "note": "CPU measured-vs-model at 2e12, eig-clip 1e-12",
       "records": []}
RES = HERE / "cpu_fallback_results.json"
def flush(): RES.write_text(json.dumps(out, indent=1))

for s in SNAPS:
    d = np.load(DATA / f"tng300_groups_{s:03d}.npz")
    z, a = float(d["z"]), float(d["a"])
    pos = d["pos"][d["m200"] > THR].astype(np.float64)
    k = len(pos)
    # model-C (one eigvalsh; PSD by construction)
    valm = lambda r: XI_MODEL(r) / SIG2_MODEL
    Cm = build_C(pos, valm); evm = np.linalg.eigvalsh(Cm)
    dm = S_decomp(evm, k)
    # measured-C: build+eig only the 1.0x matrix; 0.5x/2.0x are affine maps of it
    #   C_f = alpha_f*(C_1 - I) + I with alpha_f = sig2_1/sig2_f -> ev_f = alpha_f*ev1 + (1-alpha_f)
    xi = xi_hat_of(pos)
    fn1, sig2_1 = measured_table(xi, 1.0)
    Cx = build_C(pos, fn1); ev1 = np.linalg.eigvalsh(Cx)
    rec = dict(snap=s, z=z, a=a, k=k,
               S_model=dm["S_clip"], model_min_eig=dm["min_eig"],
               model_n_nonpos=dm["n_nonpos"])
    for name, f in (("1.0x", 1.0), ("0.5x", 0.5), ("2.0x", 2.0)):
        _, sig2_f = measured_table(xi, f)
        alpha = sig2_1 / sig2_f
        dd = S_decomp(alpha * ev1 + (1.0 - alpha), k)
        rec[f"S_meas_{name}"] = dd["S_clip"]
        rec[f"S_meas_floor_{name}"] = dd["S_floor"]
        rec[f"neg_mass_{name}"] = dd["neg_mass"]
        rec[f"clip_frac_{name}"] = dd["clip_frac"]
        rec[f"n_nonpos_{name}"] = dd["n_nonpos"]
    rec["S_model_floor"] = dm["S_floor"]
    out["records"].append(rec); flush()
    log(f"snap {s:03d} z={z:5.3f} k={k:5d}  S_model={rec['S_model']:8.1f}  "
        f"S_meas(clip)={rec['S_meas_1.0x']:9.1f}  S_meas(floor)={rec['S_meas_floor_1.0x']:8.1f}  "
        f"clip_frac={rec['clip_frac_1.0x']:.2f}  neg_mass={rec['neg_mass_1.0x']:.2e}")

# ---- analysis: model vs measured, under BOTH estimators (as-is clip; clip-robust floor) ----
a = np.array([r["a"] for r in out["records"]])
res = {}
res["model_C"] = AM.analyze(a, np.array([r["S_model"] for r in out["records"]]),
                            "model-C 2e12 clip", project=True)
res["model_C_floor"] = AM.analyze(a, np.array([r["S_model_floor"] for r in out["records"]]),
                                  "model-C 2e12 floor", project=True)
for name in ("1.0x", "0.5x", "2.0x"):
    res[f"measured_C_{name}"] = AM.analyze(
        a, np.array([r[f"S_meas_{name}"] for r in out["records"]]),
        f"measured-C 2e12 {name} clip", project=True)
res["measured_C_floor_1.0x"] = AM.analyze(
    a, np.array([r["S_meas_floor_1.0x"] for r in out["records"]]),
    "measured-C 2e12 1.0x floor", project=True)
out["analysis"] = res
out["clip_diagnostic"] = {
    "measured_clip_frac_1.0x": [round(r["clip_frac_1.0x"], 3) for r in out["records"]],
    "measured_neg_mass_1.0x": [round(r["neg_mass_1.0x"], 4) for r in out["records"]],
    "measured_n_nonpos_1.0x": [r["n_nonpos_1.0x"] for r in out["records"]],
    "model_n_nonpos": [r["model_n_nonpos"] for r in out["records"]],
    "verdict": "measured-C is NOT PSD; as-is clip S is regularization-dominated (see clip_frac)."}

def syst(mkey, xkey):
    m, x = res[mkey], res[xkey]
    return {
        "d_w_today": x["w_today"] - m["w_today"],
        "d_cpl_w0": x["cpl_dist_BAO+CMB"]["w0"] - m["cpl_dist_BAO+CMB"]["w0"],
        "d_cpl_wa": x["cpl_dist_BAO+CMB"]["wa"] - m["cpl_dist_BAO+CMB"]["wa"],
        "d_cpl_cross_z": (None if (m["cpl_dist_BAO+CMB"]["cross_z"] is None or
                                   x["cpl_dist_BAO+CMB"]["cross_z"] is None)
                          else x["cpl_dist_BAO+CMB"]["cross_z"] - m["cpl_dist_BAO+CMB"]["cross_z"]),
        "d_desi_chi2_cmb": x["desi_chi2_with_cmb"]["chi2"] - m["desi_chi2_with_cmb"]["chi2"]}
out["proxy_systematic_clip"] = syst("model_C", "measured_C_1.0x")
out["proxy_systematic_floor"] = syst("model_C_floor", "measured_C_floor_1.0x")
flush()

def row(tag, r):
    c = r["cpl_dist_BAO+CMB"]; ch = r["desi_chi2_with_cmb"]
    pk = r["interior_peak_z"]; pk = f"{pk:.3f}" if pk is not None else "none"
    cz = c["cross_z"]; cz = f"{cz:.3f}" if cz is not None else "none"
    print(f"  {tag:28s} w_today={r['w_today']:+.3f} peak_z={pk:>6s} "
          f"CPL(w0={c['w0']:+.3f},wa={c['wa']:+.3f},cross={cz}) chi2={ch['chi2']:.3f}")
print("=" * 100)
print("AS-IS clip estimator (op_B 1e-12) -- measured-C is NON-PSD, S clip-dominated:")
row("model-C 2e12", res["model_C"]); row("measured-C 2e12 1.0x", res["measured_C_1.0x"])
print("CLIP-ROBUST floor estimator (drop lambda<1e-3 noise spectrum):")
row("model-C 2e12 floor", res["model_C_floor"]); row("measured-C 2e12 floor", res["measured_C_floor_1.0x"])
print("clip_frac(measured,1.0x) per a:", out["clip_diagnostic"]["measured_clip_frac_1.0x"])
print("proxy systematic (clip):", {k: (round(v, 3) if isinstance(v, float) else v)
                                   for k, v in out["proxy_systematic_clip"].items()})
print("proxy systematic (floor):", {k: (round(v, 3) if isinstance(v, float) else v)
                                    for k, v in out["proxy_systematic_floor"].items()})
print("wrote cpu_fallback_results.json")
