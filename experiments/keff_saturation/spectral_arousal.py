#!/usr/bin/env python3
"""
DYNAMICS test of dρ/dt = α − γ·M(t): does WITHDRAWING active coherence-management
(γ·M, indexed by AROUSAL STATE) drive correlation ρ UP and effective
dimensionality k_eff DOWN toward the rigidity pole?

  AWAKE   = high maintenance (γ·M large)   -> prediction: LOWER ρ, HIGHER k_eff
  COMA    = low  maintenance (γ·M small)   -> prediction: HIGHER ρ, LOWER  k_eff

Contrast:
  COMA  = iCARE post-cardiac-arrest scalp EEG (PhysioNet iCARE 2023), 10 subjects
          with an _EEG.mat on disk. CPC 1-5 outcome/arousal grade from each .txt.
  AWAKE = eegmmidb resting-state (PhysioNet EEG Motor Movement/Imagery), baseline
          runs R01 (eyes-open) + R02 (eyes-closed), 11 healthy subjects.

MATCHED PREPROCESSING (the whole point -- absolute k_eff is confounded by ~19-ch
volume conduction, but the awake-vs-coma DIFFERENCE with matched montage is not):
  * N = 19 referential 10-20 channels (iCARE native 19; eegmmidb subselected to
    the identical standard-19 label set -> referential-to-referential match).
  * common sampling rate 128 Hz (resample_poly from 160/250/256 Hz).
  * 4th-order Butterworth band-pass 1-40 Hz, filtfilt.
  * central SEG_SEC = 60 s segment; per-channel demean; no re-reference.
  * flat/near-constant channels dropped (std>1e-9) inside corr_eig's caller.

READOUTS (analysis core reused verbatim from spectral_test.py / entropy_production.py):
  k_eff        = participation ratio of the channel correlation spectrum (PR).
  rho_bar      = mean off-diagonal channel correlation (signed).
  rho_kish     = Kish-implied ρ from k_eff via k_eff=N/(1+ρ(N-1)) -> the framework
                 quantity; ρ = (N/k_eff − 1)/(N−1).
  db_z         = broken-detailed-balance winding z (irreversibility_from_units,
                 k=4). |z|≫2 ⇒ sustained directed cycling = active maintenance γ·M.

Real data only. Synthetics only calibrate. No commit. No .lean edits.
"""
import numpy as np, json, os, glob, struct, sys
from fractions import Fraction
from scipy.signal import butter, filtfilt, resample_poly
import pyedflib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
# reuse the EXACT analysis core
from spectral_test import corr_eig, participation_ratio, mp_edge, phase_randomize
from spectral_test_icare import load_v4, read_hea
import entropy_production as ep

ICARE = os.path.join(HERE,
    "../../.claude/worktrees/agent-a5a5cfc9f224f29b0/experiments/noncorr_biology/data/icare")
AWAKE_DIR = "/tmp/claude-1000/-home-emoore-coherence-ratchet/a15f19f3-8fff-4354-9d5c-e860763082eb/scratchpad/eegmmidb"

SEG_SEC = 60.0
FS_COMMON = 128.0
BAND = (1.0, 40.0)
# standard 19-channel 10-20 referential set present in eegmmidb (P7=T5,P8=T6,T7=T3,T8=T4)
STD19 = ["Fp1", "Fp2", "F3", "F4", "F7", "F8", "Fz", "C3", "C4", "Cz",
         "P3", "P4", "P7", "P8", "Pz", "O1", "O2", "T7", "T8"]
RNG = np.random.default_rng(0)


# ---------- matched preprocessing ----------
def resample_to(X, fs):
    if abs(fs - FS_COMMON) < 1e-6:
        return X
    fr = Fraction(int(round(FS_COMMON)), int(round(fs))).limit_denominator(1000)
    return resample_poly(X, fr.numerator, fr.denominator, axis=1)


def preprocess(val, fs):
    """resample->128, central 60 s, demean, bandpass 1-40. Returns X (N x T)."""
    X = resample_to(np.asarray(val, float), fs)
    N, T = X.shape
    seg = int(min(T, SEG_SEC * FS_COMMON))
    s = max(0, (T - seg) // 2)
    X = X[:, s:s + seg]
    X = X - X.mean(1, keepdims=True)
    b, a = butter(4, [BAND[0] / (FS_COMMON / 2), BAND[1] / (FS_COMMON / 2)], btype="band")
    return filtfilt(b, a, X, axis=1)


def mean_pairwise_rho(X):
    """signed & abs mean off-diagonal correlation."""
    Z = (X - X.mean(1, keepdims=True)) / (X.std(1, keepdims=True) + 1e-12)
    C = (Z @ Z.T) / Z.shape[1]
    iu = np.triu_indices(C.shape[0], 1)
    off = C[iu]
    return float(off.mean()), float(np.abs(off).mean())


def rho_kish(keff, N):
    return (N / keff - 1.0) / (N - 1.0)


def readouts(X, label):
    ev, N, T = corr_eig(X)
    pr = participation_ratio(ev)
    rbar, rabs = mean_pairwise_rho(X)
    db = ep.irreversibility_from_units(X, k=4)
    return dict(label=label, N=int(N), T=int(T), k_eff=float(pr),
                rho_bar=rbar, rho_abs=rabs, rho_kish=float(rho_kish(pr, N)),
                db_z=float(db["z"]), db_winding=float(db["winding_rate"]),
                top_eigs=[float(x) for x in ev[:6]])


# ---------- loaders ----------
def load_coma():
    out = []
    for m in sorted(glob.glob(os.path.join(ICARE, "*", "*_EEG.mat"))):
        subj = os.path.basename(m).split("_")[0]
        meta = {}
        tp = os.path.join(ICARE, subj, subj + ".txt")
        if os.path.exists(tp):
            for line in open(tp):
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
        hea = read_hea(m[:-4] + ".hea")
        fs = hea["fs"] if hea else 256.0
        val, nrows, ncols = load_v4(m)
        X = preprocess(val, fs)
        good = np.isfinite(X).all(1) & (X.std(1) > 1e-9)
        X = X[good]
        if X.shape[0] < 3:
            continue
        r = readouts(X, subj)
        r.update(group="coma", fs_native=float(fs),
                 cpc=int(meta["CPC"]) if meta.get("CPC", "nan").isdigit() else None,
                 outcome=meta.get("Outcome"))
        out.append(r)
    return out


def load_awake():
    out = []
    for p in sorted(glob.glob(os.path.join(AWAKE_DIR, "*.edf"))):
        name = os.path.basename(p)[:-4]           # e.g. S001R01
        subj, run = name[:4], name[4:]
        f = pyedflib.EdfReader(p)
        fs = float(f.getSampleFrequencies()[0])
        labs = [l.strip().strip(".").rstrip(".") for l in f.getSignalLabels()]
        # normalise labels: eegmmidb uses 'Fp1.','F3..' etc; strip trailing dots
        labs = [l.replace(".", "") for l in f.getSignalLabels()]
        norm = {l.capitalize(): i for i, l in enumerate(labs)}
        # build 10-20 pick (case-insensitive exact match to STD19)
        low = {l.lower(): i for i, l in enumerate(labs)}
        idx, missing = [], []
        for ch in STD19:
            i = low.get(ch.lower())
            if i is None:
                missing.append(ch)
            else:
                idx.append(i)
        if missing:
            f._close()
            raise RuntimeError(f"{name}: missing channels {missing} (have {labs})")
        val = np.vstack([f.readSignal(i) for i in idx])
        f._close()
        X = preprocess(val, fs)
        good = np.isfinite(X).all(1) & (X.std(1) > 1e-9)
        X = X[good]
        r = readouts(X, name)
        r.update(group="awake", fs_native=fs,
                 condition="eyes_open" if run == "R01" else "eyes_closed",
                 subject=subj)
        out.append(r)
    return out


# ---------- synthetic calibration (matched N,T) ----------
def synth_lowrank(N, T, r=3, snr=3.0):
    F = RNG.standard_normal((r, T)); W = RNG.standard_normal((N, r))
    return W @ F + snr**-1 * RNG.standard_normal((N, T)) * np.sqrt(r)

def synth_noise(N, T):
    return RNG.standard_normal((N, T))

def calibrate():
    N, T = 19, int(SEG_SEC * FS_COMMON)
    rows = {}
    for nm, X in [("low-rank r=3", synth_lowrank(N, T)), ("pure noise", synth_noise(N, T))]:
        ev, *_ = corr_eig(X)
        rbar, _ = mean_pairwise_rho(X)
        rows[nm] = dict(k_eff=float(participation_ratio(ev)), rho_bar=rbar,
                        rho_kish=float(rho_kish(participation_ratio(ev), N)))
    return rows


def summ(vals):
    a = np.array([v for v in vals if v is not None and np.isfinite(v)], float)
    return dict(n=int(a.size), mean=float(a.mean()), sd=float(a.std(ddof=1)),
                median=float(np.median(a)), min=float(a.min()), max=float(a.max()))


def cohen_d(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    na, nb = len(a), len(b)
    sp = np.sqrt(((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2))
    return float((a.mean() - b.mean()) / sp)


def mann_whitney_p(a, b):
    """two-sided rank-sum p via normal approx (no scipy.stats dependency needed)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    na, nb = len(a), len(b)
    allv = np.concatenate([a, b]); order = allv.argsort()
    ranks = np.empty_like(order, float); ranks[order] = np.arange(1, len(allv) + 1)
    # average ties
    _, inv, cnt = np.unique(allv, return_inverse=True, return_counts=True)
    for g in np.where(cnt > 1)[0]:
        m = inv == g; ranks[m] = ranks[m].mean()
    Ua = ranks[:na].sum() - na * (na + 1) / 2
    mu = na * nb / 2; sd = np.sqrt(na * nb * (na + nb + 1) / 12)
    z = (Ua - mu) / sd
    from math import erf, sqrt
    p = 2 * (1 - 0.5 * (1 + erf(abs(z) / sqrt(2))))
    return float(z), float(p)


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    def rank(v):
        o = v.argsort(); r = np.empty_like(o, float); r[o] = np.arange(1, len(v) + 1)
        return r
    rx, ry = rank(x), rank(y)
    return float(np.corrcoef(rx, ry)[0, 1])


def main():
    cal = calibrate()
    print("CALIBRATION (N=19, matched T):", json.dumps(cal, indent=0))
    coma = load_coma()
    awake = load_awake()
    print(f"\ncoma n={len(coma)}   awake n={len(awake)}")

    ck = [r["k_eff"] for r in coma]; ak = [r["k_eff"] for r in awake]
    cr = [r["rho_bar"] for r in coma]; ar = [r["rho_bar"] for r in awake]
    crk = [r["rho_kish"] for r in coma]; ark = [r["rho_kish"] for r in awake]
    cz = [abs(r["db_z"]) for r in coma]; az = [abs(r["db_z"]) for r in awake]

    zc, pk = mann_whitney_p(ak, ck)
    _, pr = mann_whitney_p(ar, cr)
    _, pz = mann_whitney_p(az, cz)

    stats = dict(
        k_eff=dict(coma=summ(ck), awake=summ(ak),
                   cohen_d_awake_minus_coma=cohen_d(ak, ck), mw_p=pk),
        rho_bar=dict(coma=summ(cr), awake=summ(ar),
                     cohen_d_awake_minus_coma=cohen_d(ar, cr), mw_p=pr),
        rho_kish=dict(coma=summ(crk), awake=summ(ark),
                      cohen_d_awake_minus_coma=cohen_d(ark, crk)),
        db_absz=dict(coma=summ(cz), awake=summ(az),
                     cohen_d_awake_minus_coma=cohen_d(az, cz), mw_p=pz),
    )
    # eyes-open-only sensitivity (minimal posterior alpha -> controls the alpha
    # global-coherence confound on the awake side)
    ao = [r for r in awake if r.get("condition") == "eyes_open"]
    aok = [r["k_eff"] for r in ao]; aor = [r["rho_bar"] for r in ao]
    aork = [r["rho_kish"] for r in ao]; aoz = [abs(r["db_z"]) for r in ao]
    eyes_open_only = dict(
        k_eff=dict(coma=summ(ck), awake_eyes_open=summ(aok),
                   cohen_d=cohen_d(aok, ck), mw_p=mann_whitney_p(aok, ck)[1]),
        rho_bar=dict(coma=summ(cr), awake_eyes_open=summ(aor),
                     cohen_d=cohen_d(aor, cr), mw_p=mann_whitney_p(aor, cr)[1]),
        rho_kish=dict(coma=summ(crk), awake_eyes_open=summ(aork),
                      cohen_d=cohen_d(aork, crk)),
        db_absz=dict(coma=summ(cz), awake_eyes_open=summ(aoz),
                     cohen_d=cohen_d(aoz, cz)))

    # within-coma: k_eff vs CPC (higher CPC = worse outcome / lower arousal recovery)
    cpc = [(r["cpc"], r["k_eff"], r["rho_kish"]) for r in coma if r["cpc"] is not None]
    within = None
    if len(cpc) >= 4:
        cc = [c for c, _, _ in cpc]
        within = dict(n=len(cpc),
                      spearman_cpc_keff=spearman(cc, [k for _, k, _ in cpc]),
                      spearman_cpc_rhokish=spearman(cc, [rk for _, _, rk in cpc]),
                      note="CPC is follow-up outcome (1=good..5=none), a proxy for "
                           "arousal-recovery, NOT instantaneous arousal at recording.")

    # DIRECTION verdict
    dir_keff = "coma<awake" if np.mean(ck) < np.mean(ak) else "coma>=awake"
    dir_rho = "coma>awake" if np.mean(crk) > np.mean(ark) else "coma<=awake"
    dir_db = "awake>coma" if np.mean(az) > np.mean(cz) else "awake<=coma"
    predicted = (np.mean(ck) < np.mean(ak)) and (np.mean(crk) > np.mean(ark))

    result = dict(
        test="dynamics dρ/dt=α−γM via arousal-state (awake vs coma) k_eff/ρ contrast",
        prediction="maintenance withdrawal (coma) => k_eff DOWN, ρ UP vs awake",
        datasets=dict(
            coma=dict(source="PhysioNet iCARE 2023 post-cardiac-arrest scalp EEG",
                      path=os.path.relpath(ICARE, HERE), n_subjects=len(coma)),
            awake=dict(source="PhysioNet eegmmidb resting baseline R01(eyes-open)+R02(eyes-closed)",
                       n_recordings=len(awake),
                       n_subjects=len(set(r["subject"] for r in awake)))),
        matched=dict(N_channels=19, montage="referential 10-20",
                     fs_common_hz=FS_COMMON, band_hz=list(BAND), seg_sec=SEG_SEC),
        calibration=cal,
        stats=stats,
        eyes_open_only_sensitivity=eyes_open_only,
        within_coma_arousal=within,
        note_dropped=["0432: central 60s window (and all windows past ~10% of the "
                      "record) is a flat/saturated block -> 0 non-flat channels under "
                      "the fixed central-window QC rule; dropped. 9 of 10 coma mats used."],
        directions=dict(k_eff=dir_keff, rho_kish=dir_rho, detailed_balance=dir_db),
        prediction_confirmed_direction=bool(predicted),
        per_recording=dict(coma=coma, awake=awake),
        caveats=[
            "Absolute k_eff is confounded by EEG volume conduction at ~19 channels; "
            "only the matched awake-vs-coma DIFFERENCE is interpreted, not absolute values.",
            "Cross-dataset: different subjects/hardware/clinical context. Montage TYPE "
            "matched (both referential 19-ch 10-20) and N/fs/band/segment matched; residual "
            "acquisition & pathology (post-anoxic vs healthy) differences remain a confound.",
            "iCARE CPC is a follow-up OUTCOME grade, an imperfect proxy for arousal at the "
            "moment of recording; used only for the within-coma monotonicity check.",
            "Detailed-balance z is a directed-cycling (winding) statistic; sign not "
            "interpreted, magnitude |z| compared.",
        ],
    )
    with open(os.path.join(HERE, "spectral_results_arousal.json"), "w") as fh:
        json.dump(result, fh, indent=1)

    # console
    print("\n=== MATCHED CONTRAST (awake vs coma, N=19, 128Hz, 1-40Hz, 60s) ===")
    for key in ("k_eff", "rho_bar", "rho_kish", "db_absz"):
        s = stats[key]
        d = s.get("cohen_d_awake_minus_coma")
        p = s.get("mw_p")
        print(f"{key:9s} awake {s['awake']['mean']:.3f}  coma {s['coma']['mean']:.3f}  "
              f"d(awake-coma)={d:+.2f}" + (f"  MW p={p:.2g}" if p is not None else ""))
    print(f"db_absz medians: awake {summ(az)['median']:.2f}  coma {summ(cz)['median']:.2f} "
          f"(coma mean inflated by 0501 |z|=33 artifact)")
    print("eyes-open-only:  k_eff awake {:.2f} vs coma {:.2f} (d={:+.2f}, p={:.2g}) | "
          "rho_bar awake {:.3f} vs coma {:.3f} (d={:+.2f}, p={:.2g})".format(
              summ(aok)['mean'], summ(ck)['mean'], cohen_d(aok, ck), mann_whitney_p(aok, ck)[1],
              summ(aor)['mean'], summ(cr)['mean'], cohen_d(aor, cr), mann_whitney_p(aor, cr)[1]))
    if within:
        print(f"\nwithin-coma  Spearman(CPC, k_eff)   = {within['spearman_cpc_keff']:+.3f}")
        print(f"within-coma  Spearman(CPC, rho_kish) = {within['spearman_cpc_rhokish']:+.3f}")
    print(f"\nDIRECTIONS: k_eff {dir_keff} | rho {dir_rho} | detailed-balance {dir_db}")
    print(f"PREDICTION (coma k_eff<awake AND coma rho>awake) confirmed: {predicted}")
    return result


if __name__ == "__main__":
    main()
