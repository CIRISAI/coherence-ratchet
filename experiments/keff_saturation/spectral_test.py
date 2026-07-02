#!/usr/bin/env python3
"""
DECISIVE (mechanism-level) test of the criticality-vs-low-rank discriminator,
on raw C. elegans whole-brain calcium (Kato 2015, 12 worms, up to 151 neurons).

The proxy tests (rho*-vs-k slope; cross-session k_eff) are underpowered and
confounded. This goes to the mechanism:

  LOW-RANK (novel):    covariance spectrum = a FEW spikes above a flat
                       Marchenko-Pastur noise bulk. Effective rank small and
                       ~size-independent. PR subsampling curve SATURATES.
  CRITICALITY (trivial): scale-free / power-law spectrum, no clean spike/bulk
                       separation. PR grows as a power of N (0<beta<1).
  PURE NOISE (chaos):  all eigenvalues ~ MP bulk, PR ~ N (beta ~ 1), 0 spikes.

Two readouts per worm:
  (1) effective rank = # eigenvalues above the MP upper edge lambda+ =
      sigma^2 (1+sqrt(N/T))^2 (noise null for an N x T matrix). Small & flat
      across worms of different N  => low-rank.
  (2) PR subsampling exponent beta = dlog(PR)/dlog(N') over the upper range.
      beta ~ 0 => saturation (low-rank); 0<beta<1 => power-law (critical);
      beta ~ 1 => noise/extensive.

No fabricated data; all from the repo parquet. Debiasing cross-check via
phase-randomized surrogates (destroys cross-neuron structure, preserves each
neuron's power spectrum) -> surrogate spike count should be ~0.
"""
import numpy as np, pandas as pd, json, os

PARQUET = os.path.join(os.path.dirname(__file__),
    "../structural_series/corridor_dynamics/celegans/data/kato2015_whole_brain.parquet")
RNG = np.random.default_rng(0)

def worm_matrix(df, worm):
    sub = df[df.worm == worm]
    traces = []
    for _, r in sub.iterrows():
        x = np.asarray(r["calcium_data"], float)
        traces.append(x)
    L = min(len(t) for t in traces)
    X = np.vstack([t[:L] for t in traces])          # N x T
    # drop constant/NaN neurons
    good = np.isfinite(X).all(1) & (X.std(1) > 1e-9)
    return X[good]

def corr_eig(X):
    """z-score neurons, return correlation-matrix eigenvalues (desc), N, T."""
    N, T = X.shape
    Z = (X - X.mean(1, keepdims=True)) / X.std(1, keepdims=True)
    C = (Z @ Z.T) / T                                # N x N correlation
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

def synth_lowrank(N, T, r=3, snr=3.0):
    F = RNG.standard_normal((r, T))
    W = RNG.standard_normal((N, r))
    return W @ F + snr**-1 * RNG.standard_normal((N, T)) * np.sqrt(r)

def synth_powerlaw(N, T, alpha=1.0):
    # eigenvalues ~ k^-alpha (scale-free / criticality-like), built via colored factors
    lam = (np.arange(1, N+1) ** (-alpha))
    lam = lam / lam.sum() * N
    L = np.sqrt(lam)[:, None] * RNG.standard_normal((N, T))
    Q, _ = np.linalg.qr(RNG.standard_normal((N, N)))
    return Q @ L

def synth_noise(N, T):
    return RNG.standard_normal((N, T))

def calibrate():
    print("=== CALIBRATION: does beta separate the hypotheses on known data? ===")
    N, T = 150, 2000
    for name, X in [("low-rank r=3", synth_lowrank(N, T)),
                    ("power-law a=1.0", synth_powerlaw(N, T, 1.0)),
                    ("power-law a=0.6", synth_powerlaw(N, T, 0.6)),
                    ("pure noise", synth_noise(N, T))]:
        ev, n, t = corr_eig(X)
        pr = participation_ratio(ev)
        Xs = phase_randomize(X); evs, *_ = corr_eig(Xs)
        eff = int((ev > evs.max()).sum())
        sizes = [10,15,20,30,40,60,80,100,120,150]
        curve = subsample_pr(X, sizes, ndraw=25)
        cn = np.array([c[0] for c in curve]); cp = np.array([c[1] for c in curve])
        up = cn >= 40
        beta = np.polyfit(np.log10(cn[up]), np.log10(cp[up]), 1)[0]
        print(f"  {name:16s}: PR={pr:6.2f}  eff_rank={eff:3d}  beta_sub={beta:6.3f}")
    print("  (expect: low-rank beta~0 & small rank; power-law beta 0.3-0.8; noise beta~1 rank~0)\n")

def main():
    calibrate()
    df = pd.read_parquet(PARQUET)
    worms = sorted(df.worm.unique(), key=lambda w: -df[df.worm==w].neuron.nunique())
    results = []
    print(f"{'worm':7s} {'N':>4s} {'T':>5s} {'PR':>6s} {'eff_rank':>8s} {'surr_rank':>9s} {'MPedge':>7s} {'beta_sub':>8s}")
    betas, effranks = [], []
    for w in worms:
        X = worm_matrix(df, w)
        N, T = X.shape
        if N < 20: continue
        ev, N, T = corr_eig(X)
        pr = participation_ratio(ev)
        edge = mp_edge(N, T)
        eff_rank = int((ev > edge).sum())
        # surrogate noise floor
        Xs = phase_randomize(X)
        evs, *_ = corr_eig(Xs)
        surr_rank = int((evs > edge).sum())
        surr_top = float(evs.max())
        eff_rank_surr = int((ev > surr_top).sum())   # spikes above the surrogate's largest eig
        # subsampling curve
        sizes = [s for s in [10,15,20,30,40,60,80,100,120,150] if s <= N]
        curve = subsample_pr(X, sizes)
        cn = np.array([c[0] for c in curve]); cp = np.array([c[1] for c in curve])
        upper = cn >= max(20, cn.max()//3)           # fit exponent on the upper range
        beta = np.polyfit(np.log10(cn[upper]), np.log10(cp[upper]), 1)[0] if upper.sum()>=3 else np.nan
        betas.append(beta); effranks.append(eff_rank_surr)
        results.append(dict(worm=w, N=N, T=T, PR=pr, eff_rank_mp=eff_rank,
                            eff_rank_surr=eff_rank_surr, surr_rank_mp=surr_rank,
                            mp_edge=edge, beta_sub=beta,
                            top_eigs=[float(x) for x in ev[:6]],
                            subsample=curve))
        print(f"{w:7s} {N:4d} {T:5d} {pr:6.2f} {eff_rank_surr:8d} {surr_rank:9d} {edge:7.2f} {beta:8.3f}")

    betas = np.array([b for b in betas if np.isfinite(b)])
    effranks = np.array(effranks)
    print("\n=== VERDICT INPUTS (C. elegans substrate, n=%d worms) ===" % len(results))
    print(f"effective rank (spikes above surrogate floor): median {np.median(effranks):.1f}, "
          f"range {effranks.min()}-{effranks.max()}  -> {'SMALL & bounded (low-rank)' if np.median(effranks)<=12 else 'large (not low-rank)'}")
    print(f"PR subsampling exponent beta: mean {betas.mean():.3f} +/- {betas.std():.3f}  (n={len(betas)})")
    print("   interpretation: beta~0 saturation=LOW-RANK ; 0.3-0.8 power-law=CRITICALITY ; ~1 noise/extensive")
    # crude one-sample reads vs the two hypotheses
    from math import sqrt
    se = betas.std()/sqrt(len(betas))
    print(f"   beta 95% CI ~ [{betas.mean()-2*se:.3f}, {betas.mean()+2*se:.3f}]")
    if betas.mean()+2*se < 0.3:
        v = "LOW-RANK (saturation): novel at this substrate"
    elif betas.mean()-2*se > 0.15 and betas.mean()+2*se < 0.9:
        v = "POWER-LAW (criticality-like): trivial-leaning at this substrate"
    else:
        v = "INCONCLUSIVE at beta; lean on effective-rank readout"
    print(f"   BETA VERDICT: {v}")
    json.dump(results, open(os.path.join(os.path.dirname(__file__),"spectral_results.json"),"w"), indent=1)
    print("\nwrote spectral_results.json")

if __name__ == "__main__":
    main()
