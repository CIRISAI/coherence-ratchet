#!/usr/bin/env python3
"""
Criticality-vs-low-rank SPECTRAL discriminator on the iCARE comatose/post-cardiac
-arrest EEG cohort (PhysioNet iCARE 2023, WFDB records).

Reuses the EXACT analysis core of experiments/keff_saturation/spectral_test.py:
  corr_eig (z-score, correlation-matrix eigenvalues), participation_ratio,
  mp_edge, phase_randomize (surrogate floor), subsample_pr, and the synthetic
  calibrate() -- here re-calibrated at the DATA's N (~19-20 scalp channels).

Substrate note: EEG scalp arrays during coma are a possible NEGATIVE / edge case
(coordination structure may be degraded toward noise). N is small (19-20), so the
EFFECTIVE-RANK readout is primary and beta secondary.

Loader: the *_EEG.mat are MATLAB v4 files holding one int16 matrix `val`
(channels x samples, column-major). scipy.io.loadmat misparses the int16 'P' code
on these, so we parse the v4 header directly and read the available int16 payload
(some downloads are truncated relative to the header nsamp -> we read whole columns
actually present). Sampling rate / channel names from the paired .hea when present;
otherwise assumed 256 Hz (iCARE standard) and flagged.

Preprocessing (stated exactly): contiguous mid-segment of up to SEG_SEC seconds at
native rate; per-channel demean; 4th-order Butterworth band-pass 1-40 Hz (removes
DC/drift common-mode and >40 Hz line noise -- standard clinical EEG band). Flat /
near-constant channels (e.g. the Fpz reference, gain 1.0) are dropped by the
std>1e-9 filter inside corr_eig's caller. No re-referencing.
"""
import numpy as np, json, os, glob, struct
from scipy.signal import butter, filtfilt

RNG = np.random.default_rng(0)
DATA = os.path.join(os.path.dirname(__file__),
    "../../.claude/worktrees/agent-a5a5cfc9f224f29b0/experiments/noncorr_biology/data/icare")
SEG_SEC = 120.0          # mid-segment length (s)
DEFAULT_FS = 256.0

# ---- MATLAB v4 int16 loader (scipy misparses these WFDB .mat files) ----
_V4_DTYPE = {0: '<f8', 1: '<f4', 2: '<i4', 3: '<i2', 4: '<u2', 5: '<u1'}

def load_v4(path):
    """Return (val [N x T_available], nrows, ncols_header)."""
    with open(path, 'rb') as f:
        hdr = f.read(20)
        mtype, mrows, ncols, imagf, namelen = struct.unpack('<5i', hdr)
        P = (mtype % 100) // 10
        dt = np.dtype(_V4_DTYPE[P])
        f.read(namelen)                      # variable name
        raw = np.frombuffer(f.read(), dtype=dt)
    ncomplete = (raw.size // mrows)          # whole columns actually present
    val = raw[:ncomplete * mrows].reshape(ncols_order := (ncomplete, mrows)).T  # col-major -> N x T
    return np.asarray(val, float), mrows, ncols

def read_hea(path):
    """Parse WFDB .hea: return dict(fs, names). None if absent."""
    if not os.path.exists(path):
        return None
    with open(path) as f:
        lines = [l for l in f if l.strip() and not l.startswith('#')]
    parts = lines[0].split()
    fs = float(parts[2]); nsig = int(parts[1])
    names = [l.split()[-1] for l in lines[1:1 + nsig]]
    return dict(fs=fs, names=names)

# ---- analysis core (verbatim from spectral_test.py) ----
def corr_eig(X):
    N, T = X.shape
    Z = (X - X.mean(1, keepdims=True)) / X.std(1, keepdims=True)
    C = (Z @ Z.T) / T
    ev = np.linalg.eigvalsh(C)[::-1]
    return np.clip(ev, 0, None), N, T

def participation_ratio(ev):
    return (ev.sum() ** 2) / (ev ** 2).sum()

def mp_edge(N, T, sigma2=1.0):
    q = N / T
    return sigma2 * (1 + np.sqrt(q)) ** 2

def phase_randomize(X):
    F = np.fft.rfft(X, axis=1)
    ph = np.exp(1j * RNG.uniform(0, 2 * np.pi, F.shape))
    ph[:, 0] = 1
    return np.fft.irfft(F * ph, n=X.shape[1], axis=1)

def subsample_pr(X, sizes, ndraw=40):
    N = X.shape[0]
    out = []
    for n in sizes:
        if n > N: continue
        prs = []
        for _ in range(ndraw):
            idx = RNG.choice(N, n, replace=False)
            ev, *_ = corr_eig(X[idx])
            prs.append(participation_ratio(ev))
        out.append((n, float(np.mean(prs)), float(np.std(prs))))
    return out

# ---- synthetics (verbatim) ----
def synth_lowrank(N, T, r=3, snr=3.0):
    F = RNG.standard_normal((r, T)); W = RNG.standard_normal((N, r))
    return W @ F + snr**-1 * RNG.standard_normal((N, T)) * np.sqrt(r)

def synth_powerlaw(N, T, alpha=1.0):
    lam = (np.arange(1, N + 1) ** (-alpha)); lam = lam / lam.sum() * N
    L = np.sqrt(lam)[:, None] * RNG.standard_normal((N, T))
    Q, _ = np.linalg.qr(RNG.standard_normal((N, N)))
    return Q @ L

def synth_noise(N, T):
    return RNG.standard_normal((N, T))

def _beta(curve, floor):
    cn = np.array([c[0] for c in curve]); cp = np.array([c[1] for c in curve])
    up = cn >= floor
    if up.sum() < 3: return np.nan
    return float(np.polyfit(np.log10(cn[up]), np.log10(cp[up]), 1)[0])

def calibrate(N, T, sizes):
    print(f"=== CALIBRATION at data scale N={N}, T={T} ===")
    floor = max(sizes[0], sizes[len(sizes)//2])
    rows = {}
    for name, X in [("low-rank r=3", synth_lowrank(N, T)),
                    ("power-law a=1.0", synth_powerlaw(N, T, 1.0)),
                    ("power-law a=0.6", synth_powerlaw(N, T, 0.6)),
                    ("pure noise", synth_noise(N, T))]:
        ev, n, t = corr_eig(X)
        pr = participation_ratio(ev)
        evs, *_ = corr_eig(phase_randomize(X))
        eff = int((ev > evs.max()).sum())
        beta = _beta(subsample_pr(X, sizes, ndraw=25), floor)
        rows[name] = dict(PR=pr, eff_rank=eff, beta=beta)
        print(f"  {name:16s}: PR={pr:6.2f}  eff_rank={eff:3d}  beta_sub={beta:6.3f}")
    print("  (expect: low-rank beta~0 & small rank; power-law beta 0.3-0.8; noise beta~1 rank~0)\n")
    return rows

def preprocess(val, fs):
    """mid-segment, demean, bandpass 1-40 Hz."""
    N, T = val.shape
    seg = int(min(T, SEG_SEC * fs))
    start = max(0, (T - seg) // 2)
    X = val[:, start:start + seg].astype(float)
    X = X - X.mean(1, keepdims=True)
    hi = min(40.0, 0.45 * fs)
    b, a = butter(4, [1.0 / (fs / 2), hi / (fs / 2)], btype='band')
    return filtfilt(b, a, X, axis=1)

def main():
    mats = sorted(glob.glob(os.path.join(DATA, "*", "*_EEG.mat")))
    print(f"Found {len(mats)} EEG .mat recordings on disk.\n")
    # calibrate once at representative N,T (use 19 ch, 2-min at 256)
    calN, calT = 19, int(SEG_SEC * DEFAULT_FS)
    sizes_cal = [5, 8, 10, 12, 15, 18]
    cal = calibrate(calN, calT, sizes_cal)

    results = []
    print(f"{'subj':6s} {'N':>3s} {'Tseg':>7s} {'fs':>5s} {'PR':>6s} "
          f"{'effR_surr':>9s} {'effR_mp':>7s} {'MPedge':>7s} {'beta':>7s}  hea")
    betas, effranks = [], []
    for m in mats:
        subj = os.path.basename(m).split('_')[0]
        hea = read_hea(m[:-4] + '.hea')
        fs = hea['fs'] if hea else DEFAULT_FS
        val, nrows, ncols_h = load_v4(m)
        X = preprocess(val, fs)
        # drop flat/constant channels
        good = np.isfinite(X).all(1) & (X.std(1) > 1e-9)
        X = X[good]
        N, T = X.shape
        if N < 3:
            print(f"{subj:6s}  only {N} non-flat channels -- skipped"); continue
        ev, N, T = corr_eig(X)
        pr = participation_ratio(ev)
        edge = mp_edge(N, T)
        eff_rank_mp = int((ev > edge).sum())
        evs, *_ = corr_eig(phase_randomize(X))
        eff_rank_surr = int((ev > evs.max()).sum())
        sizes = [s for s in [5, 8, 10, 12, 15, 18, 20] if s <= N]
        curve = subsample_pr(X, sizes)
        floor = max(sizes[0], sizes[len(sizes)//2]) if len(sizes) >= 3 else sizes[0]
        beta = _beta(curve, floor)
        betas.append(beta); effranks.append(eff_rank_surr)
        results.append(dict(subj=subj, N=N, T=T, fs=fs, PR=pr,
                            eff_rank_surr=eff_rank_surr, eff_rank_mp=eff_rank_mp,
                            mp_edge=edge, beta_sub=beta, has_hea=bool(hea),
                            nrows_hdr=int(nrows), ncols_hdr=int(ncols_h),
                            top_eigs=[float(x) for x in ev[:6]], subsample=curve))
        print(f"{subj:6s} {N:3d} {T:7d} {fs:5.0f} {pr:6.2f} {eff_rank_surr:9d} "
              f"{eff_rank_mp:7d} {edge:7.2f} {beta:7.3f}  {'Y' if hea else 'n'}")

    betas = np.array([b for b in betas if np.isfinite(b)])
    effranks = np.array(effranks)
    n = len(results)
    print(f"\n=== VERDICT INPUTS (iCARE comatose EEG, n={n} recordings) ===")
    med_eff = float(np.median(effranks))
    print(f"effective rank (spikes above surrogate floor): median {med_eff:.1f}, "
          f"range {effranks.min()}-{effranks.max()}")
    se = betas.std() / np.sqrt(len(betas))
    ci = (betas.mean() - 2 * se, betas.mean() + 2 * se)
    print(f"PR subsampling exponent beta: mean {betas.mean():.3f} +/- {betas.std():.3f} "
          f"(95% CI [{ci[0]:.3f}, {ci[1]:.3f}], n={len(betas)})")

    # verdict: combine effective-rank (primary, small N) and beta (secondary)
    if med_eff <= 4 and ci[1] < 0.35:
        verdict = "LOW-RANK (few spikes, saturating PR)"
    elif ci[0] > 0.2 and ci[1] < 0.9:
        verdict = "CRITICALITY (power-law-like beta)"
    elif betas.mean() > 0.75 and med_eff <= 2:
        verdict = "NOISE/CHAOS (extensive PR, ~no spikes)"
    else:
        verdict = "INCONCLUSIVE"
    print(f"VERDICT: {verdict}")

    out = dict(substrate="iCARE comatose/post-cardiac-arrest scalp EEG",
               n_recordings=n, n_mat_on_disk=len(mats),
               preprocessing=dict(seg_sec=SEG_SEC, band_hz=[1, 40],
                                  demean=True, reref=False),
               calibration=cal, per_subject=results,
               median_eff_rank=med_eff,
               beta_mean=float(betas.mean()), beta_std=float(betas.std()),
               beta_ci95=[float(ci[0]), float(ci[1])], verdict=verdict)
    json.dump(out, open(os.path.join(os.path.dirname(__file__),
              "spectral_results_icare.json"), "w"), indent=1)
    print("\nwrote spectral_results_icare.json")

if __name__ == "__main__":
    main()
