#!/usr/bin/env python3
"""
ADVERSARIAL, NON-NEURAL substrate for the criticality-vs-low-rank spectral
discriminator (Cosmology.CriticalityDiscriminator): the S&P 500 daily-return
cross-correlation spectrum.

Why this is the key adversarial test. The random-matrix-theory finance literature
(Laloux/Cizeau/Bouchaud/Potters 1999; Plerou/Gopikrishnan/… 2002, cond-mat/0108023)
has a SHARP published prediction for this exact matrix: one giant "market mode"
eigenvalue, a Marchenko-Pastur noise BULK containing the large majority of
eigenvalues, and a handful of "sector mode" eigenvalues poking above the MP edge.
That is precisely the LOW-RANK fingerprint (a few spikes over a flat MP bulk),
NOT a scale-free / power-law (criticality) spectrum. Markets have a criticality
REPUTATION, but that reputation is about temporal tails / volatility clustering,
not the cross-sectional correlation spectrum — so this doubles as a pipeline
validation against a known ground truth AND a genuinely non-neural substrate.

Same analysis core as spectral_test.py / spectral_drosophila.py; synthetic
calibration re-run at this N. Units = stocks, "time" = trading days (log returns).

Data: yfinance daily adjusted closes (open, no credentials). No fabricated data;
synthetics are used ONLY to calibrate the estimator at this N.
"""
import numpy as np, json, os, sys
import yfinance as yf
import pandas as pd

RNG = np.random.default_rng(0)
HERE = os.path.dirname(os.path.abspath(__file__))

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
    ph = np.exp(1j * RNG.uniform(0, 2*np.pi, F.shape)); ph[:, 0] = 1
    return np.fft.irfft(F * ph, n=X.shape[1], axis=1)
def subsample_pr(X, sizes, ndraw=40):
    N = X.shape[0]; out = []
    for n in sizes:
        if n > N: continue
        prs = []
        for _ in range(ndraw):
            idx = RNG.choice(N, n, replace=False)
            ev, *_ = corr_eig(X[idx]); prs.append(participation_ratio(ev))
        out.append((n, float(np.mean(prs)), float(np.std(prs))))
    return out
def synth_lowrank(N, T, r=3, snr=3.0):
    F = RNG.standard_normal((r, T)); W = RNG.standard_normal((N, r))
    return W @ F + snr**-1 * RNG.standard_normal((N, T)) * np.sqrt(r)
def synth_powerlaw(N, T, alpha=1.0):
    lam = (np.arange(1, N+1) ** (-alpha)); lam = lam / lam.sum() * N
    L = np.sqrt(lam)[:, None] * RNG.standard_normal((N, T))
    Q, _ = np.linalg.qr(RNG.standard_normal((N, N))); return Q @ L
def synth_noise(N, T):
    return RNG.standard_normal((N, T))

def calibrate(N, T):
    print(f"=== CALIBRATION at N={N}, T={T} (finance ruler) ===")
    sizes = [s for s in [20,30,40,60,80,100,150,200,300,400] if s <= N]
    for name, X in [("low-rank r=3", synth_lowrank(N, T)),
                    ("power-law a=1.0", synth_powerlaw(N, T, 1.0)),
                    ("power-law a=0.6", synth_powerlaw(N, T, 0.6)),
                    ("pure noise", synth_noise(N, T))]:
        ev, n, t = corr_eig(X); pr = participation_ratio(ev)
        Xs = phase_randomize(X); evs, *_ = corr_eig(Xs)
        eff = int((ev > evs.max()).sum())
        curve = subsample_pr(X, sizes, ndraw=20)
        cn = np.array([c[0] for c in curve]); cp = np.array([c[1] for c in curve])
        up = cn >= max(40, cn.max()//4)
        beta = np.polyfit(np.log10(cn[up]), np.log10(cp[up]), 1)[0]
        print(f"  {name:16s}: PR={pr:7.2f}  eff_rank={eff:3d}  beta_sub={beta:6.3f}")
    print()

SP100 = ("AAPL MSFT AMZN NVDA GOOGL GOOG META TSLA BRK-B UNH JPM JNJ V PG XOM "
    "HD CVX MA BAC ABBV PFE AVGO COST DIS KO MRK PEP TMO WMT CSCO ACN MCD ABT "
    "LIN DHR TXN NEE VZ ADBE PM NKE WFC BMY UPS RTX ORCL AMD QCOM HON LOW T "
    "INTC UNP IBM CAT GS SBUX AMGN BA GE MMM DE LMT BLK C AXP BKNG MDT ADP GILD "
    "CVS MDLZ TJX ISRG SYK REGN VRTX SCHW MO ZTS CB SO DUK BSX ITW SLB EOG PLD "
    "AON APD ICE CME CI FDX NSC EMR PGR MU PANW MS COP").split()

def main():
    print("Downloading S&P-100 daily closes (yfinance, ~6y)...")
    data = yf.download(SP100, period="6y", interval="1d", progress=False,
                       auto_adjust=True)
    close = data["Close"] if isinstance(data.columns, pd.MultiIndex) else data
    close = close.dropna(axis=1, thresh=int(0.98*len(close)))  # drop sparse tickers
    close = close.dropna(axis=0, how="any")
    rets = np.log(close).diff().dropna()
    tickers = list(rets.columns)
    X = rets.to_numpy().T                      # N stocks x T days
    good = np.isfinite(X).all(1) & (X.std(1) > 1e-12)
    X = X[good]; tickers = [t for t,g in zip(tickers,good) if g]
    N, T = X.shape
    print(f"matrix: N={N} stocks x T={T} trading days\n")
    calibrate(N, min(T, 1500))

    ev, N, T = corr_eig(X)
    pr = participation_ratio(ev)
    edge = mp_edge(N, T)
    eff_rank_mp = int((ev > edge).sum())
    Xs = phase_randomize(X); evs, *_ = corr_eig(Xs)
    surr_top = float(evs.max()); surr_rank_mp = int((evs > edge).sum())
    eff_rank_surr = int((ev > surr_top).sum())
    sizes = [s for s in [20,30,40,60,80,100] if s <= N]
    curve = subsample_pr(X, sizes)
    cn = np.array([c[0] for c in curve]); cp = np.array([c[1] for c in curve])
    up = cn >= max(40, cn.max()//4)
    beta = float(np.polyfit(np.log10(cn[up]), np.log10(cp[up]), 1)[0]) if up.sum()>=3 else float("nan")

    frac_bulk = float((ev <= edge).mean())
    market_mode = float(ev[0]); market_frac = float(ev[0]/ev.sum())
    print(f"{'N':>4s} {'T':>5s} {'PR/k_eff':>9s} {'eff_rank_mp':>11s} {'eff_rank_surr':>13s} "
          f"{'MPedge':>7s} {'beta':>6s}")
    print(f"{N:4d} {T:5d} {pr:9.2f} {eff_rank_mp:11d} {eff_rank_surr:13d} {edge:7.2f} {beta:6.3f}")
    print(f"\nmarket mode (largest eig): {market_mode:.1f}  = {100*market_frac:.1f}% of total variance")
    print(f"fraction of eigenvalues INSIDE the MP noise bulk: {100*frac_bulk:.1f}%")
    print(f"top 8 eigs: {[round(float(x),2) for x in ev[:8]]}")
    print(f"phase-randomized surrogate: {surr_rank_mp} eigs above MP edge, top {surr_top:.2f}")

    # verdict
    if eff_rank_surr <= max(8, N//20) and beta < 0.3:
        verdict = "LOW-RANK (market mode + sector spikes over MP bulk): the RMT-predicted structure; NOT criticality"
    elif beta > 0.3 and beta < 0.9:
        verdict = "POWER-LAW (criticality-like)"
    else:
        verdict = "INCONCLUSIVE"
    print(f"\nVERDICT: {verdict}")

    out = dict(substrate="S&P-100 daily log-return cross-correlation",
               n_stocks=N, n_days=T, tickers=tickers, PR_keff=pr, mp_edge=edge,
               eff_rank_mp=eff_rank_mp, eff_rank_surr=eff_rank_surr,
               surr_rank_mp=surr_rank_mp, beta_sub=beta,
               market_mode_eig=market_mode, market_variance_frac=market_frac,
               frac_in_mp_bulk=frac_bulk, top_eigs=[float(x) for x in ev[:12]],
               subsample=curve, verdict=verdict)
    json.dump(out, open(os.path.join(HERE,"spectral_results_finance.json"),"w"), indent=1)
    print("\nwrote spectral_results_finance.json")

if __name__ == "__main__":
    main()
