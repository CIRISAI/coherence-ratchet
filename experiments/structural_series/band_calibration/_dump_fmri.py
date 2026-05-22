"""Re-run the fMRI corridor pipeline and dump per-subject debiased rho to JSON.
Reuses fmri_corridor.py's subject_rho exactly. No new data, no synthetic data."""
import json, sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "data_fmri"))
from nilearn import datasets  # noqa
# import the module to reuse subject_rho / constants
import importlib.util
spec = importlib.util.spec_from_file_location(
    "fmri_mod", os.path.join(os.path.dirname(__file__), "..", "data_fmri", "fmri_corridor.py"))
# we cannot exec the module (it runs the whole pipeline at import). Instead replicate.
SEED = 0
N_SUBJECTS = 250

def subject_rho(ts, rng, n_surr=5):
    ts = np.asarray(ts, dtype=float)
    if ts.ndim != 2 or ts.shape[0] < 20 or ts.shape[1] < 10:
        return None
    keep = ts.std(axis=0) > 1e-9
    ts = ts[:, keep]
    T, R = ts.shape
    z = (ts - ts.mean(0)) / ts.std(0)
    C = (z.T @ z) / T
    off = ~np.eye(R, dtype=bool)
    rho_raw = float(np.mean(np.abs(C[off])))
    floors = []
    for _ in range(n_surr):
        zs = np.empty_like(z)
        for r in range(R):
            f = np.fft.rfft(z[:, r])
            ph = rng.uniform(0, 2*np.pi, len(f))
            ph[0] = 0
            if T % 2 == 0:
                ph[-1] = 0
            zs[:, r] = np.fft.irfft(np.abs(f)*np.exp(1j*ph), n=T)
        zs = (zs - zs.mean(0)) / zs.std(0)
        Cs = (zs.T @ zs) / T
        floors.append(float(np.mean(np.abs(Cs[off]))))
    floor = float(np.mean(floors))
    rho_deb = float(np.sqrt(max(rho_raw**2 - floor**2, 0.0)))
    evals = np.linalg.eigvalsh(C)
    evals = np.clip(evals, 0, None)
    k_eff_emp = float((evals.sum()**2) / (np.sum(evals**2)))
    k = R
    k_eff_kish = float(k / (1.0 + rho_deb*(k-1.0)))
    return rho_raw, floor, rho_deb, k_eff_emp, k_eff_kish

print("fetching ABIDE-PCP ...", flush=True)
abide = datasets.fetch_abide_pcp(
    derivatives=["rois_cc200"], pipeline="cpac",
    band_pass_filtering=True, global_signal_regression=False,
    n_subjects=N_SUBJECTS, quality_checked=True, verbose=0)
ts_all = abide["rois_cc200"]
ph = abide["phenotypic"]
dx = np.asarray(ph["DX_GROUP"])
ctrl = dx == 2
rng = np.random.default_rng(SEED)
recs = []
for i in range(len(ts_all)):
    if not ctrl[i]:
        continue
    res = subject_rho(ts_all[i], rng)
    if res is None:
        continue
    recs.append({"rho_raw": res[0], "floor": res[1], "rho_deb": res[2],
                 "k_eff_emp": res[3], "k_eff_kish": res[4]})
    if len(recs) % 20 == 0:
        print(f"  {len(recs)} controls done", flush=True)
out = os.path.join(os.path.dirname(__file__), "_fmri_per_subject.json")
json.dump({"n": len(recs), "records": recs}, open(out, "w"), indent=1)
print(f"wrote {out}: n={len(recs)}", flush=True)
