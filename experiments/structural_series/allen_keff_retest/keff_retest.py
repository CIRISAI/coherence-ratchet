"""
Allen mouse visual cortex — canonical k_eff re-test.
=====================================================

Owed by papers/Corridor Dynamics.tex sec:robust-rerun: the structural-series
Allen run (data_allen/exp_allen_corridor.py) read mean pairwise neuron rho
~ 0.023, a chaos-pole datum. But the framework's canonical shape observable is
NOT mean pairwise correlation: it is k_eff_emp, the participation ratio of the
activity covariance eigenvalues  (sum lambda)^2 / sum lambda^2.

This script recomputes, on the SAME 25 sessions / SAME spontaneous epoch as the
original run, the three observables side by side:
  - k_eff_emp  : participation ratio of the covariance eigenvalues (canonical)
  - rho_deb    : debiased mean |pairwise corr|, phase-randomized surrogate floor
                 (data_fmri/fmri_corridor.py subject_rho estimator)
  - k_eff_kish : N / (1 + rho_deb (N-1))

Real Allen data only. The 25 session IDs are taken verbatim from the original
run's results.json. NWB files are fetched directly from the Allen Brain
Observatory API (allensdk does not install under this Python), and the
extraction is verified to reproduce the original run's k_eff to 4 decimals on
session 627823695 (11.6923).

Incremental: per-session results are appended to results.json and flushed as
each session completes, so a restart recovers all finished work.
"""
import json
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(HERE, "..", "data_allen", "results.json")
OUT = os.path.join(HERE, "results.json")
NWB_DIR = "/tmp/allen_nwb"
API = "https://api.brain-map.org"
SEED = 0
N_SURROGATE = 20
MIN_ROIS = 10

os.makedirs(NWB_DIR, exist_ok=True)


def api_get(url):
    """GET with curl (sandbox-friendly). Returns decoded JSON."""
    r = subprocess.run(["curl", "-sL", "--max-time", "60", url],
                       capture_output=True, text=True)
    return json.loads(r.stdout)


def download_nwb(exp_id):
    """Fetch the NWBOphys file for an OphysExperiment id. Returns local path."""
    path = os.path.join(NWB_DIR, f"{exp_id}.nwb")
    if os.path.exists(path) and os.path.getsize(path) > 1_000_000:
        return path
    q = (f"{API}/api/v2/data/query.json?criteria=model::OphysExperiment,"
         f"rma::criteria,%5Bid$eq{exp_id}%5D,rma::include,"
         f"well_known_files(well_known_file_type)")
    d = api_get(q)
    link = None
    for m in d["msg"]:
        for w in m.get("well_known_files", []):
            if w.get("well_known_file_type", {}).get("name") == "NWBOphys":
                link = w["download_link"]
    if link is None:
        raise RuntimeError(f"no NWBOphys file for experiment {exp_id}")
    r = subprocess.run(["curl", "-sL", "--max-time", "600", "-o", path,
                        API + link], capture_output=True, text=True)
    if not os.path.exists(path) or os.path.getsize(path) < 1_000_000:
        raise RuntimeError(f"download failed for {exp_id}")
    return path


def load_spont_dff(path):
    """Return the neurons x frames dF/F matrix on the spontaneous epoch."""
    import h5py
    with h5py.File(path, "r") as f:
        dff = f["processing/brain_observatory_pipeline/DfOverF/"
                "imaging_plane_1/data"][:]
        fd = f["stimulus/presentation/spontaneous_stimulus/"
               "frame_duration"][:]
    s0, s1 = int(fd[0, 0]), int(fd[1, 0])
    return np.asarray(dff[:, s0:s1], dtype=np.float64), s0, s1


def phase_randomize(x, rng):
    """Phase-randomize columns of x (T x k): destroys cross-column correlation,
    preserves each column's power spectrum / autocorrelation."""
    n = x.shape[0]
    F = np.fft.rfft(x, axis=0)
    amp = np.abs(F)
    rand = rng.uniform(-np.pi, np.pi, size=F.shape)
    rand[0] = 0.0
    if n % 2 == 0:
        rand[-1] = 0.0
    return np.fft.irfft(amp * np.exp(1j * rand), n=n, axis=0)


def mean_abs_offdiag(C):
    d = C.shape[0]
    return float(np.mean(np.abs(C[~np.eye(d, dtype=bool)])))


def measure(X, rng):
    """X: neurons x frames. Returns dict of the three observables.

    k_eff_emp  : participation ratio of the covariance eigenvalues -- canonical.
    rho_deb    : mean |pairwise corr| debiased by a phase-randomized floor.
    k_eff_kish : N / (1 + rho_deb (N-1)).
    """
    sd = X.std(axis=1)
    X = X[sd > 1e-9]
    n, T = X.shape
    if n < MIN_ROIS:
        return None

    # canonical k_eff: participation ratio of the covariance eigenvalues
    C_cov = np.cov(X)
    w = np.clip(np.linalg.eigvalsh(C_cov), 0, None)
    k_eff_emp = float(w.sum() ** 2 / np.sum(w * w))

    # debiased rho via phase-randomized surrogate floor (fmri_corridor.py)
    Z = ((X - X.mean(axis=1, keepdims=True)) /
         X.std(axis=1, keepdims=True)).T          # T x n
    Ccorr = (Z.T @ Z) / T
    rho_raw = mean_abs_offdiag(Ccorr)
    floors = []
    for _ in range(N_SURROGATE):
        Zs = phase_randomize(Z, rng)
        Zs = (Zs - Zs.mean(axis=0)) / (Zs.std(axis=0) + 1e-12)
        floors.append(mean_abs_offdiag((Zs.T @ Zs) / T))
    floor = float(np.mean(floors))
    rho_deb = float(np.sqrt(max(rho_raw ** 2 - floor ** 2, 0.0)))

    k_eff_kish = float(n / (1.0 + rho_deb * (n - 1.0)))
    return dict(n_neurons=int(n), n_frames=int(T),
                k_eff_emp=k_eff_emp, rho_raw=rho_raw, rho_floor=floor,
                rho_deb=rho_deb, k_eff_kish=k_eff_kish,
                keff_emp_over_n=k_eff_emp / n)


def main():
    orig = json.load(open(ORIG))
    # the 25 sessions with a valid within-rung rho in the original run
    sessions = [(r["id"], r["area"]) for r in orig
                if "dff" in r and isinstance(r["dff"], dict)]
    print(f"re-testing {len(sessions)} Allen sessions (canonical k_eff_emp)")

    # resume from any partial results.json
    results = []
    done = set()
    if os.path.exists(OUT):
        try:
            results = json.load(open(OUT))
            done = {r["id"] for r in results}
            print(f"  resuming -- {len(done)} sessions already done")
        except Exception:
            results = []

    rng = np.random.default_rng(SEED)
    for i, (sid, area) in enumerate(sessions):
        if sid in done:
            continue
        try:
            path = download_nwb(sid)
            X, s0, s1 = load_spont_dff(path)
            m = measure(X, rng)
            if m is None:
                rec = dict(id=sid, area=area, excluded="too_few_rois")
            else:
                rec = dict(id=sid, area=area, spont_frames=s1 - s0, **m)
                print(f"  [{i+1:2d}/{len(sessions)}] {sid} {area:6s} "
                      f"N={m['n_neurons']:3d}  k_eff_emp={m['k_eff_emp']:7.2f}  "
                      f"k_eff_emp/N={m['keff_emp_over_n']:.3f}  "
                      f"rho_deb={m['rho_deb']:.4f}  "
                      f"k_eff_kish={m['k_eff_kish']:.2f}")
        except Exception as ex:
            rec = dict(id=sid, area=area, failed=f"{type(ex).__name__}: "
                       f"{str(ex)[:120]}")
            print(f"  [{i+1:2d}/{len(sessions)}] {sid} {area:6s} FAILED: "
                  f"{rec['failed']}")
        results.append(rec)
        # incremental flush
        with open(OUT, "w") as f:
            json.dump(results, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        # free disk: NWB files are ~300 MB each
        try:
            os.remove(os.path.join(NWB_DIR, f"{sid}.nwb"))
        except OSError:
            pass

    print(f"\nwrote {OUT}")
    analyse(results)


def analyse(results):
    ok = [r for r in results if "k_eff_emp" in r]
    if not ok:
        print("no valid session -- BLOCKED")
        return
    keff = np.array([r["k_eff_emp"] for r in ok])
    nn = np.array([r["n_neurons"] for r in ok])
    ratio = np.array([r["keff_emp_over_n"] for r in ok])
    rdeb = np.array([r["rho_deb"] for r in ok])
    kish = np.array([r["k_eff_kish"] for r in ok])
    print("=" * 70)
    print(f"{len(ok)} sessions.  N range [{nn.min()}, {nn.max()}], "
          f"median {int(np.median(nn))}")
    print(f"k_eff_emp  : [{keff.min():.2f}, {keff.max():.2f}], "
          f"median {np.median(keff):.2f}")
    print(f"k_eff_emp/N: [{ratio.min():.3f}, {ratio.max():.3f}], "
          f"median {np.median(ratio):.3f}")
    print(f"rho_deb    : [{rdeb.min():.4f}, {rdeb.max():.4f}], "
          f"median {np.median(rdeb):.4f}")
    print(f"k_eff_kish : [{kish.min():.2f}, {kish.max():.2f}], "
          f"median {np.median(kish):.2f}")


if __name__ == "__main__":
    main()
