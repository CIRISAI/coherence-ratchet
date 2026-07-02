#!/usr/bin/env python3
"""
Does the LOW-RANK finding on S&P returns carry PREDICTIVE power?

The static spectrum (one market mode + sector modes + MP noise bulk) is not a
return forecast — it's a structural fact. The predictive content, if any, is in
the TIME VARIATION of the effective dimensionality k_eff:

  k_eff(t) = participation ratio of the trailing-window return correlation matrix.

Framework claim: drifting to the RIGIDITY pole (rho -> 1, k_eff -> 1) is
coordination collapse. Market translation (Kritzman & Page 2011, "absorption
ratio"): when correlations spike and k_eff collapses, the market is fragile and
forward volatility / drawdowns rise. This script tests that with a strict
trailing->forward split (no lookahead):

  predictor  : trailing 60-day k_eff at time t
  outcome    : forward 20-day realized vol and forward 20-day worst return
  test       : sign + magnitude of the relationship, plus behaviour around the
               2020-03 COVID crash and 2022 drawdown.

No fabricated data (yfinance daily closes). This is an honest yes/no on whether
the effective-dimensionality collapse LEADS turbulence, not a trading strategy.
"""
import numpy as np, json, os
import yfinance as yf, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
SP100 = ("AAPL MSFT AMZN NVDA GOOGL META BRK-B UNH JPM JNJ V PG XOM HD CVX MA "
    "BAC ABBV PFE AVGO COST DIS KO MRK PEP TMO WMT CSCO ACN MCD ABT LIN DHR TXN "
    "NEE VZ ADBE PM NKE WFC BMY UPS RTX ORCL AMD QCOM HON LOW T INTC UNP IBM CAT "
    "GS SBUX AMGN BA GE MMM DE LMT BLK C AXP BKNG MDT ADP GILD CVS MDLZ TJX ISRG "
    "SYK REGN VRTX SCHW MO ZTS CB SO DUK BSX ITW SLB EOG PLD AON APD ICE CME CI "
    "FDX NSC EMR PGR MU COP").split()

def keff_of(Rwin):
    Z = (Rwin - Rwin.mean(0)) / (Rwin.std(0) + 1e-12)
    C = np.corrcoef(Z.T)
    ev = np.clip(np.linalg.eigvalsh(C), 0, None)
    return (ev.sum()**2) / (ev**2).sum()

def main():
    cache = os.path.join(HERE, "finance_returns_cache.parquet")
    if os.path.exists(cache):
        rets = pd.read_parquet(cache)
    else:
        print("Downloading ~100 tickers, 8y...")
        data = yf.download(SP100, period="8y", interval="1d", progress=False, auto_adjust=True)
        close = data["Close"] if isinstance(data.columns, pd.MultiIndex) else data
        close = close.dropna(axis=1, thresh=int(0.98*len(close))).dropna(axis=0, how="any")
        rets = np.log(close).diff().dropna()
        rets.to_parquet(cache)
    dates = rets.index
    R = rets.to_numpy()
    T, N = R.shape
    print(f"panel: T={T} days x N={N} stocks, {dates[0].date()}..{dates[-1].date()}")

    W, F = 60, 20                      # trailing window, forward horizon
    idx, keff, fwd_vol, fwd_dd = [], [], [], []
    mkt = R.mean(1)                    # equal-weight market return proxy
    for t in range(W, T - F):
        k = keff_of(R[t-W:t])
        fv = mkt[t:t+F].std() * np.sqrt(252)
        # forward worst cumulative drawdown over the horizon
        cum = np.cumprod(1 + mkt[t:t+F]); dd = cum.min()/np.maximum.accumulate(cum).max() - 1
        idx.append(dates[t]); keff.append(k); fwd_vol.append(fv); fwd_dd.append(dd)
    keff = np.array(keff); fwd_vol = np.array(fwd_vol); fwd_dd = np.array(fwd_dd)

    # standardize; report Spearman (monotone) + sign
    from scipy.stats import spearmanr, pearsonr
    rv, pv = spearmanr(keff, fwd_vol)
    rd, pd_ = spearmanr(keff, fwd_dd)
    # tercile lift: forward vol when k_eff is in its LOW third (rigidity) vs HIGH third
    q1, q2 = np.quantile(keff, [1/3, 2/3])
    lo = keff <= q1; hi = keff >= q2
    print(f"\nrolling k_eff: mean {keff.mean():.1f}  range {keff.min():.1f}-{keff.max():.1f}")
    print(f"Spearman(k_eff_trailing, forward 20d vol)      = {rv:+.3f}  (p={pv:.1e})")
    print(f"Spearman(k_eff_trailing, forward 20d drawdown)  = {rd:+.3f}  (p={pd_:.1e})")
    print(f"\nforward 20d annualized vol, conditioned on trailing k_eff tercile:")
    print(f"  LOW  k_eff (rigidity, k<= {q1:.1f}):  vol {fwd_vol[lo].mean()*100:5.1f}%   drawdown {fwd_dd[lo].mean()*100:6.2f}%")
    print(f"  HIGH k_eff (diverse,  k>= {q2:.1f}):  vol {fwd_vol[hi].mean()*100:5.1f}%   drawdown {fwd_dd[hi].mean()*100:6.2f}%")
    print(f"  lift (low/high vol) = {fwd_vol[lo].mean()/fwd_vol[hi].mean():.2f}x")

    # crash windows: did k_eff drop INTO the 2020-03 and 2022 turbulence?
    ser = pd.Series(keff, index=pd.DatetimeIndex(idx))
    for label, a, b in [("2019 calm","2019-06-01","2019-12-31"),
                        ("COVID crash 2020-03","2020-02-15","2020-04-15"),
                        ("2022 drawdown","2022-01-01","2022-10-31"),
                        ("2023-24 calm","2023-06-01","2024-06-01")]:
        seg = ser[a:b]
        if len(seg): print(f"  k_eff during {label:22s}: mean {seg.mean():4.1f}  min {seg.min():4.1f}")

    out = dict(N=int(N), T=int(T), window=W, horizon=F,
               spearman_keff_fwdvol=float(rv), p_fwdvol=float(pv),
               spearman_keff_fwddd=float(rd), p_fwddd=float(pd_),
               fwdvol_low_keff=float(fwd_vol[lo].mean()), fwdvol_high_keff=float(fwd_vol[hi].mean()),
               keff_mean=float(keff.mean()), keff_min=float(keff.min()), keff_max=float(keff.max()))
    json.dump(out, open(os.path.join(HERE,"finance_dynamics_results.json"),"w"), indent=1)
    print("\nwrote finance_dynamics_results.json")

if __name__ == "__main__":
    main()
