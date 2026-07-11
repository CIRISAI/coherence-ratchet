#!/usr/bin/env python3
"""
Joint DESI DR2 BAO + theta* + Pantheon+ SNe likelihood comparison of the FROZEN
halo-grain S(a) dark-energy curve vs LCDM vs CPL.

Reuses verbatim:
  - desi_likelihood_v2/likelihood_fit.py   (real DESI DR2 BAO vector+cov, theta* anchor,
                                            F_FW frozen framework curve, f_cpl, f_lcdm,
                                            E_of, chi2_at with analytic beta)
  - data_completion/sne_likelihood.py      (Pantheon+ 1580-SN cosmology sample, analytic
                                            M_B/H0 offset marginalisation)

Total chi2(Om, [w0,wa]) = chi2_BAO(+theta*)  +  chi2_SNe , each with its own nuisance
profiled ANALYTICALLY (beta for BAO/CMB; the mag offset = M_B+... for SNe). Shape params:
  framework / LCDM : Om, beta, M_offset            -> k = 3
  CPL              : Om, beta, M_offset, w0, wa     -> k = 5
Both nuisances (beta, M) are shared identically across all models, so model-vs-model AIC/BIC
deltas see only the +2 CPL shape params. n_data = 13 (BAO) + 1 (theta*) + 1580 (SNe).

Incremental flush to results.json.
"""
import json, sys, time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize

HERE = Path(__file__).resolve().parent
CEP = HERE.parent
sys.path.insert(0, str(CEP / "desi_likelihood_v2"))
sys.path.insert(0, str(HERE))
import importlib.util
spec = importlib.util.spec_from_file_location("lf", CEP / "desi_likelihood_v2" / "likelihood_fit.py")
lf = importlib.util.module_from_spec(spec); spec.loader.exec_module(lf)
import sne_likelihood as sl

T0 = time.time()
def log(m): print(f"[{time.time()-T0:6.1f}s] {m}", flush=True)

RES = HERE / "results.json"
OUT = {}
def flush():
    RES.write_text(json.dumps(OUT, indent=2))

N_SNE = sl.sne()["n"]

# ---------------------------------------------------------------------------
# Per-model total chi2 at fixed shape.
# ---------------------------------------------------------------------------
def total_chi2(f_de, Om, use_cmb=True, use_sne=True):
    c2_bao, beta = lf.chi2_at(f_de, Om, use_cmb=use_cmb)
    c2 = c2_bao
    parts = {"bao_cmb": c2_bao if use_cmb else None, "bao": None if use_cmb else c2_bao}
    if use_sne:
        E = lf.E_of(f_de, Om)
        c2_sne = sl.chi2_sne(E)
        c2 += c2_sne
        parts["sne"] = c2_sne
    return c2, beta, parts

OM_GRID = np.linspace(0.24, 0.42, 181)

def profile_fixedshape(f_de, use_cmb=True, use_sne=True):
    best = (np.inf, None, None, None)
    prof = []
    for Om in OM_GRID:
        c2, beta, parts = total_chi2(f_de, Om, use_cmb, use_sne)
        prof.append((float(Om), float(c2)))
        if c2 < best[0]:
            best = (c2, float(Om), beta, parts)
    return dict(chi2=best[0], Om=best[1], beta=best[2], parts=best[3], profile=prof)

def profile_cpl(use_cmb=True, use_sne=True):
    w0g = np.linspace(-1.2, -0.4, 17)
    wag = np.linspace(-2.2, 1.0, 21)
    best = (np.inf, None, None, None)
    for Om in OM_GRID[::10]:
        for w0 in w0g:
            for wa in wag:
                c2, _, _ = total_chi2(lambda a: lf.f_cpl(a, w0, wa), Om, use_cmb, use_sne)
                if c2 < best[0]:
                    best = (c2, float(Om), float(w0), float(wa))
    def nll(p):
        Om, w0, wa = p
        if not (0.2 < Om < 0.5):
            return 1e6
        c2, _, _ = total_chi2(lambda a: lf.f_cpl(a, w0, wa), Om, use_cmb, use_sne)
        return c2
    r = minimize(nll, [best[1], best[2], best[3]], method="Nelder-Mead",
                 options=dict(xatol=1e-4, fatol=1e-5, maxiter=8000))
    Om, w0, wa = r.x
    c2, beta, parts = total_chi2(lambda a: lf.f_cpl(a, w0, wa), Om, use_cmb, use_sne)
    return dict(chi2=float(c2), Om=float(Om), w0=float(w0), wa=float(wa),
                beta=beta, parts=parts)

def aic_bic(chi2, k, n):
    return chi2 + 2 * k, chi2 + k * np.log(n)

def run(tag, use_cmb, use_sne):
    n = lf.N_BAO + (1 if use_cmb else 0) + (N_SNE if use_sne else 0)
    log(f"[{tag}] framework ...")
    fw = profile_fixedshape(lf.F_FW, use_cmb, use_sne)
    log(f"[{tag}] LCDM ...")
    lc = profile_fixedshape(lf.f_lcdm, use_cmb, use_sne)
    log(f"[{tag}] CPL ...")
    cpl = profile_cpl(use_cmb, use_sne)
    # k: Om+beta(+M) shared. framework/LCDM = 2 + (1 if sne). CPL adds w0,wa.
    kbase = 2 + (1 if use_sne else 0)
    out = {}
    for name, res, k in [("framework", fw, kbase), ("LCDM", lc, kbase), ("CPL", cpl, kbase + 2)]:
        aic, bic = aic_bic(res["chi2"], k, n)
        out[name] = {kk: vv for kk, vv in res.items() if kk != "profile"}
        out[name].update(k_params=k, AIC=float(aic), BIC=float(bic))
    out["n_data"] = n
    out["deltas"] = {
        "chi2_framework_minus_LCDM": fw["chi2"] - lc["chi2"],
        "chi2_framework_minus_CPL": fw["chi2"] - cpl["chi2"],
        "chi2_LCDM_minus_CPL": lc["chi2"] - cpl["chi2"],
        "dAIC_framework_minus_CPL": out["framework"]["AIC"] - out["CPL"]["AIC"],
        "dAIC_framework_minus_LCDM": out["framework"]["AIC"] - out["LCDM"]["AIC"],
        "dBIC_framework_minus_CPL": out["framework"]["BIC"] - out["CPL"]["BIC"],
        "dBIC_framework_minus_LCDM": out["framework"]["BIC"] - out["LCDM"]["BIC"],
    }
    out["framework_profile_Om"] = fw["profile"]
    return out

if __name__ == "__main__":
    OUT["provenance"] = {
        "sne": f"Pantheon+ (PantheonPlusSH0ES/DataRelease), {N_SNE} SNe after "
               "IS_CALIBRATOR==0 & zHD>0.01 cuts; m_b_corr vector + full STAT+SYS "
               "1701x1701 covariance; analytic M_B/H0 offset marginalisation; "
               "Brout et al. 2022 arXiv:2202.04077.",
        "bao_cmb": "inherited from desi_likelihood_v2/likelihood_fit.py (DESI DR2 "
                   "arXiv:2503.14738 + Planck theta* anchor).",
        "n_sne": N_SNE,
    }
    flush()
    OUT["bao_cmb_sne"] = run("BAO+CMB+SNe", use_cmb=True, use_sne=True); flush()
    OUT["bao_sne"] = run("BAO+SNe", use_cmb=False, use_sne=True); flush()
    OUT["sne_only"] = run("SNe only", use_cmb=False, use_sne=False) if False else None
    # SNe-only (no BAO): reuse profiles with a trivial BAO switch -> handle separately
    flush()

    def show(tag, r):
        print("=" * 80)
        print(f"{tag}   (n_data={r['n_data']})")
        print("-" * 80)
        for name in ("framework", "LCDM", "CPL"):
            d = r[name]
            extra = f" w0={d['w0']:+.3f} wa={d['wa']:+.3f}" if name == "CPL" else ""
            print(f"  {name:10s} chi2={d['chi2']:9.2f}  Om={d['Om']:.4f}  k={d['k_params']}"
                  f"  AIC={d['AIC']:9.2f}  BIC={d['BIC']:9.2f}{extra}")
            if "parts" in d and d["parts"]:
                print(f"             parts: {d['parts']}")
        dl = r["deltas"]
        print(f"  Dchi2 fw-LCDM={dl['chi2_framework_minus_LCDM']:+.2f}  "
              f"fw-CPL={dl['chi2_framework_minus_CPL']:+.2f}  "
              f"LCDM-CPL={dl['chi2_LCDM_minus_CPL']:+.2f}")
        print(f"  dAIC fw-CPL={dl['dAIC_framework_minus_CPL']:+.2f} "
              f"fw-LCDM={dl['dAIC_framework_minus_LCDM']:+.2f}  |  "
              f"dBIC fw-CPL={dl['dBIC_framework_minus_CPL']:+.2f} "
              f"fw-LCDM={dl['dBIC_framework_minus_LCDM']:+.2f}")

    print()
    show("BAO + theta* + SNe  (Pantheon+)", OUT["bao_cmb_sne"])
    print()
    show("BAO + SNe  (no CMB anchor)", OUT["bao_sne"])
    print("\nwrote results.json")
