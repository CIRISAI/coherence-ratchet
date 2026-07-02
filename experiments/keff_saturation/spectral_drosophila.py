#!/usr/bin/env python3
"""
Cross-substrate replication of the criticality-vs-low-rank spectral discriminator
(Cosmology.CriticalityDiscriminator) on a SECOND substrate: Drosophila
central-complex EPG (compass) neurons, Mussells Pires et al. 2024 (60D05 EPG,
NoLaser trials). Raw background-subtracted fluorescence bgsubF (32 EB-wedge ROIs
x ~1e5 frames), 20 flies x up to 9 trials.

Identical analysis core to spectral_test.py (C. elegans): correlation-matrix
eigenvalues -> effective rank vs a Marchenko-Pastur edge AND vs a phase-
randomized surrogate floor; PR subsampling exponent beta over the upper size
range. Same synthetic calibration (low-rank r=3 / power-law / noise) is run first
so the two substrates are read on the same ruler.

Prior expectation (stated before the read): EPG is a canonical ring attractor —
heading is a bump on a 1-D ring, so the population covariance should be strongly
LOW-RANK (effective rank ~ 2-4, beta ~ 0). This substrate is close to a positive
control for low-rank; a criticality (power-law, beta 0.3-0.8) read here would be
the surprise. N=32 ROIs caps the subsampling range, so the effective-rank readout
is the primary discriminator and beta is secondary.

No fabricated data; all from the repo Preproc_60D05.mat (v7.3 HDF5).
"""
import numpy as np, json, os, sys
import h5py

RNG = np.random.default_rng(0)
HERE = os.path.dirname(os.path.abspath(__file__))
PREPROC = os.path.join(HERE,
    "../../.claude/worktrees/agent-a3bebf376142dab4b/experiments/v17_biology/"
    "dan_et_al/Preproc_60D05.mat")

# ---- analysis core (identical to spectral_test.py) --------------------------
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
    ph = np.exp(1j * RNG.uniform(0, 2*np.pi, F.shape))
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

# ---- synthetic calibration (identical) --------------------------------------
def synth_lowrank(N, T, r=3, snr=3.0):
    F = RNG.standard_normal((r, T)); W = RNG.standard_normal((N, r))
    return W @ F + snr**-1 * RNG.standard_normal((N, T)) * np.sqrt(r)
def synth_powerlaw(N, T, alpha=1.0):
    lam = (np.arange(1, N+1) ** (-alpha)); lam = lam / lam.sum() * N
    L = np.sqrt(lam)[:, None] * RNG.standard_normal((N, T))
    Q, _ = np.linalg.qr(RNG.standard_normal((N, N)))
    return Q @ L
def synth_noise(N, T):
    return RNG.standard_normal((N, T))

def calibrate(N=32, T=2000):
    """Calibrate at the DROSOPHILA N (32 ROIs), so beta is read on this N's ruler."""
    print(f"=== CALIBRATION at N={N} (Drosophila ROI count) ===")
    for name, X in [("low-rank r=3", synth_lowrank(N, T)),
                    ("power-law a=1.0", synth_powerlaw(N, T, 1.0)),
                    ("power-law a=0.6", synth_powerlaw(N, T, 0.6)),
                    ("pure noise", synth_noise(N, T))]:
        ev, n, t = corr_eig(X); pr = participation_ratio(ev)
        Xs = phase_randomize(X); evs, *_ = corr_eig(Xs)
        eff = int((ev > evs.max()).sum())
        sizes = [10, 15, 20, 25, 30]
        curve = subsample_pr(X, sizes, ndraw=25)
        cn = np.array([c[0] for c in curve]); cp = np.array([c[1] for c in curve])
        up = cn >= 15
        beta = np.polyfit(np.log10(cn[up]), np.log10(cp[up]), 1)[0]
        print(f"  {name:16s}: PR={pr:6.2f}  eff_rank={eff:3d}  beta_sub={beta:6.3f}")
    print("  (expect: low-rank beta~0 & small rank; power-law beta 0.3-0.8; noise beta~1 rank~0)\n")

# ---- Drosophila loader ------------------------------------------------------
def iter_bgsubF(f):
    root = f['preProcData_60D05_NoLaser']
    trial_refs = root['fly/trial']       # (20,1) refs, one per fly
    for fi in range(trial_refs.shape[0]):
        g = f[trial_refs[fi, 0]]
        if 'bgsubF' not in g:
            continue
        bg = g['bgsubF']                 # (n_trials,1) refs, each -> 32 x T
        for ti in range(bg.shape[0]):
            try:
                M = np.array(f[bg[ti, 0]], dtype=float)   # stored (T,32) or (32,T)
            except Exception:
                continue
            # orient to ROI x time (ROI is the small dim, 32)
            if M.ndim != 2:
                continue
            if M.shape[0] > M.shape[1]:
                M = M.T
            yield fi, ti, M

def main():
    if not os.path.exists(PREPROC):
        print("MISSING:", PREPROC); sys.exit(2)
    calibrate()
    f = h5py.File(PREPROC, "r")
    results = []
    print(f"{'fly':>3s} {'trial':>5s} {'N':>4s} {'T':>7s} {'PR':>6s} "
          f"{'eff_rank':>8s} {'surr_rank':>9s} {'MPedge':>7s} {'beta_sub':>8s}")
    betas, effranks = [], []
    for fi, ti, M in iter_bgsubF(f):
        # drop constant / non-finite ROIs
        good = np.isfinite(M).all(1) & (M.std(1) > 1e-9)
        X = M[good]
        N, T = X.shape
        if N < 20 or T < 200:
            continue
        # cap T for tractability & to match a comparable q=N/T regime; use a
        # contiguous middle segment (avoids trial on/offset transients)
        if T > 6000:
            s = (T - 6000) // 2
            X = X[:, s:s+6000]; T = 6000
        ev, N, T = corr_eig(X)
        pr = participation_ratio(ev)
        edge = mp_edge(N, T)
        eff_rank = int((ev > edge).sum())
        Xs = phase_randomize(X); evs, *_ = corr_eig(Xs)
        surr_rank = int((evs > edge).sum())
        surr_top = float(evs.max())
        eff_rank_surr = int((ev > surr_top).sum())
        sizes = [s for s in [10, 15, 20, 25, 30] if s <= N]
        curve = subsample_pr(X, sizes)
        cn = np.array([c[0] for c in curve]); cp = np.array([c[1] for c in curve])
        upper = cn >= 15
        beta = (np.polyfit(np.log10(cn[upper]), np.log10(cp[upper]), 1)[0]
                if upper.sum() >= 3 else np.nan)
        betas.append(beta); effranks.append(eff_rank_surr)
        results.append(dict(fly=int(fi), trial=int(ti), N=int(N), T=int(T),
                            PR=float(pr), eff_rank_mp=eff_rank,
                            eff_rank_surr=eff_rank_surr, surr_rank_mp=surr_rank,
                            mp_edge=float(edge), beta_sub=float(beta),
                            top_eigs=[float(x) for x in ev[:6]],
                            subsample=curve))
        print(f"{fi:3d} {ti:5d} {N:4d} {T:7d} {pr:6.2f} {eff_rank_surr:8d} "
              f"{surr_rank:9d} {edge:7.2f} {beta:8.3f}")

    betas = np.array([b for b in betas if np.isfinite(b)])
    effranks = np.array(effranks)
    n = len(results)
    print(f"\n=== VERDICT INPUTS (Drosophila EPG, n={n} fly-trials) ===")
    if n == 0:
        print("no usable matrices"); sys.exit(1)
    print(f"effective rank (spikes above surrogate floor): median "
          f"{np.median(effranks):.1f}, range {effranks.min()}-{effranks.max()}"
          f"  -> {'SMALL & bounded (low-rank)' if np.median(effranks)<=8 else 'large (not low-rank)'}")
    print(f"PR subsampling exponent beta: mean {betas.mean():.3f} +/- "
          f"{betas.std():.3f}  (n={len(betas)})")
    from math import sqrt
    se = betas.std()/sqrt(max(len(betas),1))
    lo, hi = betas.mean()-2*se, betas.mean()+2*se
    print(f"   beta 95% CI ~ [{lo:.3f}, {hi:.3f}]")
    if hi < 0.3:
        v = "LOW-RANK (saturation): novel at this substrate"
    elif betas.mean()-2*se > 0.15 and hi < 0.9:
        v = "POWER-LAW (criticality-like): trivial-leaning at this substrate"
    else:
        v = "INCONCLUSIVE at beta; lean on effective-rank readout"
    print(f"   BETA VERDICT: {v}")
    out = os.path.join(HERE, "spectral_results_drosophila.json")
    json.dump(results, open(out, "w"), indent=1)
    print(f"\nwrote {os.path.basename(out)}")

if __name__ == "__main__":
    main()
