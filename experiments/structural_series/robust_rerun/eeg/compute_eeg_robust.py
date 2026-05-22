"""
Robust re-run — S1 neural OUT-corridor (EEG).
=============================================

Re-runs v1's pathological-EEG out-corridor finding (CHB-MIT seizure vs
interictal; I-CARE post-cardiac-arrest coma) under the structural series'
canonical robust estimator: debiased rho (phase-randomized surrogate
floor) + canonical participation-ratio k_eff.

Windowing IDENTICAL to v1 (10-s non-overlapping, 1-40 Hz Butterworth
band-pass, zero-phase). The ONLY change vs v1 is the rho estimator:
v1 reported raw mean |off-diagonal|; this re-run additionally debiases
against a phase-randomized noise floor and reports canonical k_eff.

See PREREGISTRATION.md (this directory) — thresholds fixed before run.
Real data only. Incremental flushed JSON output.
"""
import os, re, json
import numpy as np
import mne
from scipy.signal import butter, sosfiltfilt
from scipy.io import loadmat

mne.set_log_level("ERROR")

V1 = ("/home/emoore/coherence-ratchet/.claude/worktrees/"
      "agent-a5a5cfc9f224f29b0/experiments/noncorr_biology")
CHBMIT = os.path.join(V1, "data", "chbmit")
ICARE = os.path.join(V1, "data", "icare")
OUT_JSON = ("/home/emoore/coherence-ratchet/experiments/structural_series/"
            "robust_rerun/eeg/results_eeg_robust.json")

WINDOW_S = 10.0
BAND = (1.0, 40.0)
N_SURROGATE = 20
SEED = 0

# I-CARE: exactly the 6 patients / files v1 used (keeps window set identical).
ICARE_V1 = ["0342", "0364", "0411", "0474", "0549", "0571"]


# ---------------------------------------------------------------- estimator
def phase_randomize(X, rng):
    """X: (n_ch, n_t). Phase-randomize each channel independently:
    preserves each channel's power spectrum, destroys cross-channel
    correlation. Mirrors fmri_corridor.py::phase_randomize (rows here)."""
    n = X.shape[1]
    F = np.fft.rfft(X, axis=1)
    amp = np.abs(F)
    rand = rng.uniform(-np.pi, np.pi, size=F.shape)
    rand[:, 0] = 0.0
    if n % 2 == 0:
        rand[:, -1] = 0.0
    Fs = amp * np.exp(1j * rand)
    return np.fft.irfft(Fs, n=n, axis=1)


def mean_abs_offdiag(C):
    d = C.shape[0]
    return float(np.mean(np.abs(C[~np.eye(d, dtype=bool)])))


def window_metrics(X, rng):
    """X: (n_ch, n_t) for one 10-s window. Returns dict with rho_raw, floor,
    rho_deb, k_eff_emp, k_eff_kish — or None if unusable."""
    sd = X.std(axis=1)
    keep = sd > 1e-9
    X = X[keep]
    if X.shape[0] < 4 or X.shape[1] < 30:
        return None
    Z = (X - X.mean(axis=1, keepdims=True)) / X.std(axis=1, keepdims=True)
    T = Z.shape[1]
    C = (Z @ Z.T) / T
    rho_raw = mean_abs_offdiag(C)

    floors = []
    for _ in range(N_SURROGATE):
        Zs = phase_randomize(Z, rng)
        Zs = (Zs - Zs.mean(axis=1, keepdims=True)) / (Zs.std(axis=1, keepdims=True) + 1e-12)
        Cs = (Zs @ Zs.T) / T
        floors.append(mean_abs_offdiag(Cs))
    floor = float(np.mean(floors))
    rho_deb = float(np.sqrt(max(rho_raw ** 2 - floor ** 2, 0.0)))

    ev = np.linalg.eigvalsh(C)
    ev = ev[ev > 1e-9]
    k_eff_emp = float((ev.sum() ** 2) / (ev ** 2).sum())
    k = Z.shape[0]
    k_eff_kish = float(k / (1.0 + rho_deb * (k - 1.0)))
    return {"rho_raw": rho_raw, "floor": floor, "rho_deb": rho_deb,
            "k_eff_emp": k_eff_emp, "k_eff_kish": k_eff_kish}


def make_filter(sfreq, low, high):
    return butter(4, [low, high], btype="band", output="sos", fs=sfreq)


# ---------------------------------------------------------------- CHB-MIT
def parse_summary(path):
    with open(path) as f:
        text = f.read()
    out = []
    for e in re.split(r"File Name: ", text)[1:]:
        lines = e.splitlines()
        fname = lines[0].strip()
        starts = re.findall(r"Seizure(?:\s\d+)? Start Time:\s*(\d+)", e)
        ends = re.findall(r"Seizure(?:\s\d+)? End Time:\s*(\d+)", e)
        seizures = [(int(s), int(t)) for s, t in zip(starts, ends)]
        out.append((fname, seizures))
    return out


def windows_for_segment(data, sfreq, t0_s, t1_s):
    nw = int(WINDOW_S * sfreq)
    i0, i1 = int(t0_s * sfreq), int(t1_s * sfreq)
    return [data[:, s:s + nw] for s in range(i0, i1 - nw + 1, nw)]


def analyze_chbmit_file(edf_path, seizures, sos, rng):
    raw = mne.io.read_raw_edf(edf_path, preload=True, verbose=False)
    sfreq = raw.info["sfreq"]
    bipolar = [ch for ch in raw.ch_names if "-" in ch and not ch.startswith("-")]
    if len(bipolar) < 8:
        bipolar = raw.ch_names
    raw.pick(bipolar[:23])
    data = sosfiltfilt(sos, raw.get_data(), axis=1)
    total_s = data.shape[1] / sfreq

    ictal_segs = []
    for (s0, s1) in seizures:
        ictal_segs.extend(windows_for_segment(data, sfreq, s0, s1))

    mask = np.ones(int(total_s) + 1, dtype=bool)
    for (s0, s1) in seizures:
        mask[max(0, s0 - 600):min(int(total_s), s1 + 600) + 1] = False
    intervals, in_iv, a = [], False, 0
    for i, v in enumerate(mask):
        if v and not in_iv:
            a, in_iv = i, True
        elif (not v) and in_iv:
            intervals.append((a, i)); in_iv = False
    if in_iv:
        intervals.append((a, len(mask)))
    inter_segs = []
    for (s0, s1) in intervals:
        inter_segs.extend(windows_for_segment(data, sfreq, s0, s1))

    ictal = [m for seg in ictal_segs if (m := window_metrics(seg, rng))]
    inter = [m for seg in inter_segs if (m := window_metrics(seg, rng))]
    durs = [s1 - s0 for (s0, s1) in seizures]
    return ictal, inter, durs


# ---------------------------------------------------------------- I-CARE
def load_icare_eeg(mat_path, hea_path):
    m = loadmat(mat_path)
    arr = None
    for k in [k for k in m.keys() if not k.startswith("_")]:
        if isinstance(m[k], np.ndarray) and m[k].ndim == 2:
            arr = m[k]; break
    if arr is None:
        raise RuntimeError(f"no 2D array in {mat_path}")
    sfreq = 256.0
    if hea_path and os.path.exists(hea_path):
        with open(hea_path) as f:
            sfreq = float(f.read().splitlines()[0].split()[2])
    return arr.astype(np.float32), sfreq


def analyze_icare_patient(pdir, rng):
    mats = sorted(f for f in os.listdir(pdir) if f.endswith("_EEG.mat"))
    metrics, files_used = [], []
    sos = None
    for mname in mats[:2]:
        mat_path = os.path.join(pdir, mname)
        if os.path.getsize(mat_path) < 1_000_000:
            continue
        hea_path = mat_path.replace(".mat", ".hea")
        data, sfreq = load_icare_eeg(mat_path, hea_path if os.path.exists(hea_path) else None)
        valid = [i for i in range(data.shape[0])
                 if not np.all(data[i] == 0) and not np.any(np.isnan(data[i]))]
        if len(valid) < 4:
            continue
        data = data[valid]
        data = data[:, :int(min(data.shape[1], 5 * 60 * sfreq))]
        if sos is None:
            sos = make_filter(sfreq, *BAND)
        data = sosfiltfilt(sos, data, axis=1)
        nw = int(WINDOW_S * sfreq)
        for s in range(0, data.shape[1] - nw + 1, nw):
            mm = window_metrics(data[:, s:s + nw], rng)
            if mm:
                metrics.append(mm)
        files_used.append(mname)
    return metrics, files_used


# ---------------------------------------------------------------- summary
def grp(metrics):
    if not metrics:
        return None
    raw = np.array([m["rho_raw"] for m in metrics])
    floor = np.array([m["floor"] for m in metrics])
    deb = np.array([m["rho_deb"] for m in metrics])
    keff = np.array([m["k_eff_emp"] for m in metrics])
    return {
        "n_windows": len(metrics),
        "rho_raw_mean": float(raw.mean()), "rho_raw_median": float(np.median(raw)),
        "rho_raw_std": float(raw.std()),
        "floor_mean": float(floor.mean()),
        "rho_deb_mean": float(deb.mean()), "rho_deb_median": float(np.median(deb)),
        "rho_deb_std": float(deb.std()),
        "k_eff_emp_mean": float(keff.mean()), "k_eff_emp_median": float(np.median(keff)),
    }


def main():
    rng = np.random.default_rng(SEED)
    results = {
        "preregistration": "experiments/structural_series/robust_rerun/eeg/PREREGISTRATION.md",
        "window_s": WINDOW_S, "band_hz": list(BAND),
        "n_surrogate": N_SURROGATE, "seed": SEED,
        "chbmit": {"per_file": []}, "icare": {"per_patient": []},
    }

    def flush():
        with open(OUT_JSON, "w") as f:
            json.dump(results, f, indent=2)

    # ---- CHB-MIT
    summary = parse_summary(os.path.join(CHBMIT, "chb01-summary.txt"))
    seiz_files = [(f, s) for f, s in summary if s]
    print(f"CHB-MIT chb01: {len(seiz_files)} seizure files in summary", flush=True)
    sos = None
    all_ictal, all_inter, durations = [], [], []
    for fname, seizures in seiz_files:
        edf = os.path.join(CHBMIT, fname)
        if not os.path.exists(edf):
            print(f"  {fname}: MISSING on disk, skip (v1 also skipped)", flush=True)
            continue
        raw0 = mne.io.read_raw_edf(edf, preload=False, verbose=False)
        if sos is None:
            sos = make_filter(raw0.info["sfreq"], *BAND)
        ictal, inter, durs = analyze_chbmit_file(edf, seizures, sos, rng)
        all_ictal += ictal; all_inter += inter; durations += durs
        print(f"  {fname}: ictal n={len(ictal)} raw={np.mean([m['rho_raw'] for m in ictal]):.3f} "
              f"deb={np.mean([m['rho_deb'] for m in ictal]):.3f} | "
              f"interictal n={len(inter)} raw={np.mean([m['rho_raw'] for m in inter]):.3f} "
              f"deb={np.mean([m['rho_deb'] for m in inter]):.3f}", flush=True)
        results["chbmit"]["per_file"].append({
            "file": fname, "seizure_durations_s": durs,
            "ictal": ictal, "interictal": inter,
        })
        flush()

    results["chbmit"]["seizure"] = grp(all_ictal)
    results["chbmit"]["interictal"] = grp(all_inter)
    results["chbmit"]["seizure_durations_s"] = durations
    flush()

    # ---- I-CARE
    print(f"\nI-CARE: {len(ICARE_V1)} v1 patients", flush=True)
    good, poor = [], []
    for pid in ICARE_V1:
        pdir = os.path.join(ICARE, pid)
        meta = {}
        with open(os.path.join(pdir, f"{pid}.txt")) as f:
            for ln in f:
                if ":" in ln:
                    k, v = ln.split(":", 1)
                    meta[k.strip()] = v.strip()
        outcome, cpc = meta.get("Outcome", ""), meta.get("CPC", "")
        metrics, files_used = analyze_icare_patient(pdir, rng)
        print(f"  pid={pid} outcome={outcome} cpc={cpc} files={files_used} "
              f"n_win={len(metrics)} "
              f"raw={np.mean([m['rho_raw'] for m in metrics]):.3f} "
              f"deb={np.mean([m['rho_deb'] for m in metrics]):.3f}", flush=True)
        results["icare"]["per_patient"].append({
            "pid": pid, "outcome": outcome, "cpc": cpc,
            "files_used": files_used, "windows": metrics,
        })
        (good if outcome == "Good" else poor).extend(metrics)
        flush()

    results["icare"]["coma_good"] = grp(good)
    results["icare"]["coma_poor"] = grp(poor)
    flush()

    # ---- verdict
    inter = results["chbmit"]["interictal"]
    seiz = results["chbmit"]["seizure"]
    cg = results["icare"]["coma_good"]
    cp = results["icare"]["coma_poor"]
    base_deb = inter["rho_deb_mean"]
    disp = {
        "seizure": seiz["rho_deb_mean"] - base_deb,
        "coma_good": cg["rho_deb_mean"] - base_deb,
        "coma_poor": cp["rho_deb_mean"] - base_deb,
    }
    base_raw = inter["rho_raw_mean"]
    disp_raw = {
        "seizure": seiz["rho_raw_mean"] - base_raw,
        "coma_good": cg["rho_raw_mean"] - base_raw,
        "coma_poor": cp["rho_raw_mean"] - base_raw,
    }
    EPS = 0.005
    rigidity_ward = all(d > EPS for d in disp.values())
    reversed_dir = any(d < -EPS for d in disp.values())
    verdict = "PASS" if rigidity_ward else "FAIL"
    results["displacement_debiased_vs_interictal"] = disp
    results["displacement_raw_vs_interictal"] = disp_raw
    results["verdict"] = verdict
    results["verdict_note"] = (
        "PASS = all pathological groups (seizure, coma-good, coma-poor) "
        "displaced rigidity-ward of healthy interictal under debiased rho "
        f"(>{EPS}). reversed_direction={reversed_dir}.")
    flush()

    print("\n" + "=" * 70)
    print("VERDICT:", verdict)
    print(f"  interictal     rho_deb mean = {base_deb:.4f}  (raw {base_raw:.4f})")
    print(f"  seizure        rho_deb mean = {seiz['rho_deb_mean']:.4f}  "
          f"disp {disp['seizure']:+.4f}  (raw disp {disp_raw['seizure']:+.4f})")
    print(f"  coma good      rho_deb mean = {cg['rho_deb_mean']:.4f}  "
          f"disp {disp['coma_good']:+.4f}  (raw disp {disp_raw['coma_good']:+.4f})")
    print(f"  coma poor      rho_deb mean = {cp['rho_deb_mean']:.4f}  "
          f"disp {disp['coma_poor']:+.4f}  (raw disp {disp_raw['coma_poor']:+.4f})")
    print("=" * 70)
    print(f"written -> {OUT_JSON}")


if __name__ == "__main__":
    main()
