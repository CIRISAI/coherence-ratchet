#!/usr/bin/env python3
"""
Stage C: measured-C vs model-C comparison (the headline). For model-C and each
measured-C normalization (1.0x/0.5x/2.0x): w_today, interior-peak epoch, CPL
(w0,wa,crossing) via the representative-error distance projection (verbatim from
epoch_check/cpl_projection.py), and the REAL DESI DR2 BAO chi2 (reusing the
desi_likelihood_v2 module, only S(a) swapped). Reports the proxy->measured shift.
"""
import json, sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize

HERE = Path(__file__).resolve().parent
CEP = HERE.parent
LV = CEP / "large_volume" / "results.json"
sys.path.insert(0, str(CEP / "desi_likelihood_v2"))
import likelihood_fit as lf          # loads real DESI DR2; cheap at import

C_KM = 299792.458
Z_STAR = 1089.0
OM_PROJ = 0.3155
# DESI DR2 representative errors (verbatim from cpl_projection.py) for the CPL fit
DESI_Z = np.array([0.295, 0.510, 0.706, 0.930, 1.317, 1.491, 2.330])
SIG_DM = np.array([0.030, 0.016, 0.011, 0.009, 0.013, 0.026, 0.030])
SIG_DH = np.array([0.030, 0.021, 0.015, 0.012, 0.020, 0.035, 0.018])
SIG_CMB = 3.0e-4
DESI_CPL = dict(w0=-0.838, wa=-0.62)


def make_f_fw(a, Sa):
    sp = CubicSpline(np.log(a), np.log(Sa)); S1 = np.exp(sp(0.0))
    amin = a.min(); lnSmin = sp(np.log(amin))
    def f(aa):
        aa = np.atleast_1d(np.asarray(aa, float))
        lnS = np.where(aa >= amin, sp(np.log(np.clip(aa, 1e-6, 1.0))), lnSmin)
        return np.exp(lnS) / S1
    return f

def f_cpl(a, w0, wa):
    a = np.asarray(a, float)
    return a ** (-3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * (1.0 - a))

def E_of(f_de, Om):
    def E(a):
        a = np.asarray(a, float)
        return np.sqrt(Om * a ** -3.0 + (1.0 - Om) * f_de(a))
    return E

def comoving_DM(zt, Ef):
    val, _ = quad(lambda z: 1.0 / float(np.ravel(Ef(1.0 / (1.0 + z)))[0]), 0.0, zt, limit=200)
    return C_KM * val

def DH(zt, Ef):
    return C_KM / float(np.ravel(Ef(1.0 / (1.0 + zt)))[0])

def project_distance(f_fw, Om=OM_PROJ, use_cmb=True):
    Efw = E_of(f_fw, Om)
    zc = np.concatenate([DESI_Z, [Z_STAR]]) if use_cmb else DESI_Z
    DM_fw = np.array([comoving_DM(z, Efw) for z in zc])
    DH_fw = np.array([DH(z, Efw) for z in DESI_Z])
    def chi2(p):
        w0, wa = p
        Ecpl = E_of(lambda a: f_cpl(a, w0, wa), Om)
        DM_c = np.array([comoving_DM(z, Ecpl) for z in zc])
        DH_c = np.array([DH(z, Ecpl) for z in DESI_Z])
        res_dm = np.log(DM_fw) - np.log(DM_c); res_dh = np.log(DH_fw) - np.log(DH_c)
        wdm = 1.0 / np.concatenate([SIG_DM, [SIG_CMB]]) ** 2 if use_cmb else 1.0 / SIG_DM ** 2
        wdh = 1.0 / SIG_DH ** 2
        k = (np.sum(res_dm * wdm) + np.sum(res_dh * wdh)) / (np.sum(wdm) + np.sum(wdh))
        sig_dm = np.concatenate([SIG_DM, [SIG_CMB]]) if use_cmb else SIG_DM
        c2 = np.sum(((res_dm - k) / sig_dm) ** 2) + np.sum(((res_dh - k) / SIG_DH) ** 2)
        return c2
    r = minimize(chi2, [-0.85, -0.5], method="Nelder-Mead",
                 options=dict(xatol=1e-4, fatol=1e-8, maxiter=4000))
    return float(r.x[0]), float(r.x[1])

def crossing_z(w0, wa):
    if wa == 0: return None
    a_c = 1.0 + (1.0 + w0) / wa
    return None if a_c <= 0 else 1.0 / a_c - 1.0

def phys_crossing_z(a, Sa):
    sp = CubicSpline(np.log(a), np.log(Sa))
    aa = np.linspace(a.min(), 1.0, 2000); d = sp(np.log(aa), 1)
    sgn = np.sign(d); idx = np.where((sgn[:-1] > 0) & (sgn[1:] <= 0))[0]
    return None if len(idx) == 0 else 1.0 / aa[idx[-1]] - 1.0

def analyze(a, Sa, label, project=True):
    a = np.asarray(a, float); Sa = np.asarray(Sa, float)
    ok = np.isfinite(Sa) & (Sa > 0); a, Sa = a[ok], Sa[ok]
    order = np.argsort(a); a, Sa = a[order], Sa[order]
    sp = CubicSpline(np.log(a), np.log(Sa)); d = sp(np.log(a), 1)
    w = -1.0 - d / 3.0
    res = dict(label=label, n=int(len(a)), w_today=float(w[-1]),
               dlnS_dlna_today=float(d[-1]),
               ols_global_slope=float(np.polyfit(np.log(a), np.log(Sa), 1)[0]),
               interior_peak_z=phys_crossing_z(a, Sa),
               S_first_last=[float(Sa[0]), float(Sa[-1])])
    if project:
        f = make_f_fw(a, Sa)
        w0, wa = project_distance(f, use_cmb=True)
        res["cpl_dist_BAO+CMB"] = dict(w0=w0, wa=wa, cross_z=crossing_z(w0, wa))
        # REAL DESI DR2 chi2 with S(a) swapped in
        prof = lf.profile_fixedshape(f, use_cmb=True)
        res["desi_chi2_with_cmb"] = dict(chi2=prof["chi2"], Om=prof["Om"])
        prof0 = lf.profile_fixedshape(f, use_cmb=False)
        res["desi_chi2_bao_only"] = dict(chi2=prof0["chi2"], Om=prof0["Om"])
    return res

def main():
  # ---- model baseline (frozen) ----
  lv = json.load(open(LV))
  mrec = lv["stage2_primary"]["records"]
  a_model = np.array([r["a"] for r in mrec]); S_model = np.array([r["S"] for r in mrec])

  gpu = json.load(open(HERE / "results_gpu.json"))
  out = {"model_C": analyze(a_model, S_model, "model-C corner (frozen)"),
         "measured_C": {}, "desi_baseline": {}}
  lc = lf.profile_fixedshape(lf.f_lcdm, use_cmb=True)
  cpl = lf.profile_cpl(use_cmb=True)
  out["desi_baseline"] = dict(LCDM_chi2=lc["chi2"], LCDM_Om=lc["Om"],
                              CPL_chi2=cpl["chi2"], CPL_w0=cpl["w0"], CPL_wa=cpl["wa"],
                              n_data=lf.N_BAO + 1)
  for name in ("1.0x", "0.5x", "2.0x"):
      recs = gpu["records"].get(name, [])
      a = np.array([r["a"] for r in recs if r.get("S") is not None])
      Sv = np.array([r["S"] for r in recs if r.get("S") is not None])
      if len(a) >= 4:
          out["measured_C"][name] = analyze(a, Sv, f"measured-C {name}", project=True)

  m = out["model_C"]; meas = out["measured_C"]["1.0x"]
  def dd(k, sub=None):
      mv = m[k] if sub is None else m[k][sub]
      xv = meas[k] if sub is None else meas[k][sub]
      return xv - mv
  out["proxy_systematic_1.0x"] = {
      "d_w_today": dd("w_today"),
      "d_interior_peak_z": (None if (m["interior_peak_z"] is None or meas["interior_peak_z"] is None)
                            else meas["interior_peak_z"] - m["interior_peak_z"]),
      "d_cpl_w0": dd("cpl_dist_BAO+CMB", "w0"),
      "d_cpl_wa": dd("cpl_dist_BAO+CMB", "wa"),
      "d_cpl_cross_z": (None if (m["cpl_dist_BAO+CMB"]["cross_z"] is None or
                                 meas["cpl_dist_BAO+CMB"]["cross_z"] is None)
                        else meas["cpl_dist_BAO+CMB"]["cross_z"] - m["cpl_dist_BAO+CMB"]["cross_z"]),
      "d_desi_chi2_cmb": dd("desi_chi2_with_cmb", "chi2"),
      "d_desi_chi2_bao": dd("desi_chi2_bao_only", "chi2"),
  }
  (HERE / "comparison.json").write_text(json.dumps(out, indent=1))

  def row(tag, r):
      c = r.get("cpl_dist_BAO+CMB", {}); ch = r.get("desi_chi2_with_cmb", {})
      pk = r["interior_peak_z"]; pk = f"{pk:.3f}" if pk is not None else "none"
      cz = c.get("cross_z"); cz = f"{cz:.3f}" if cz is not None else "none"
      print(f"  {tag:22s} w_today={r['w_today']:+.3f}  peak_z={pk:>6s}  "
            f"CPL(w0={c.get('w0',float('nan')):+.3f},wa={c.get('wa',float('nan')):+.3f},cross={cz})  "
            f"chi2={ch.get('chi2',float('nan')):.3f}")
  print("=" * 100)
  print(f"DESI DR2 real likelihood baselines: LCDM chi2={lc['chi2']:.3f}  "
        f"CPL chi2={cpl['chi2']:.3f} (w0={cpl['w0']:+.3f},wa={cpl['wa']:+.3f})  n={lf.N_BAO+1}")
  print("-" * 100)
  row("model-C (frozen)", out["model_C"])
  for name in ("1.0x", "0.5x", "2.0x"):
      if name in out["measured_C"]:
          row(f"measured-C {name}", out["measured_C"][name])
  print("-" * 100)
  ps = out["proxy_systematic_1.0x"]
  print("PROXY SYSTEMATIC (measured 1.0x - model):",
        {k: (round(v, 3) if isinstance(v, float) else v) for k, v in ps.items()})
  print("\nwrote comparison.json")
  return out

if __name__ == "__main__":
    main()
