#!/usr/bin/env python3
"""S&P full-market completeness check: does return-correlation k_eff SATURATE as
N grows from ~20 to the full S&P 500? The prior S&P-100 read (low-rank) used 100
of ~4000 US equities -- a subsample by our own grain criterion. If PR plateaus as
N grows, the market is genuinely low-rank; if it keeps climbing (like cortex /
cosmic web), the S&P-100 saturation was a small-N artifact."""
import numpy as np, json, os, sys
import yfinance as yf, pandas as pd
RNG=np.random.default_rng(0); HERE=os.path.dirname(os.path.abspath(__file__))
def pr(ev): ev=np.clip(ev,0,None); s=ev.sum(); return float(s*s/np.sum(ev*ev)) if s>0 else 0.0
def corr_eig(X):
    Z=(X-X.mean(1,keepdims=True))/(X.std(1,keepdims=True)+1e-12); C=(Z@Z.T)/X.shape[1]
    return np.clip(np.linalg.eigvalsh(C)[::-1],0,None)
def subsample_pr(X,sizes,ndraw=8):
    N=X.shape[0]; out=[]
    for n in sizes:
        if n>N: continue
        ps=[pr(corr_eig(X[np.sort(RNG.choice(N,n,replace=False))])) for _ in range(ndraw)]
        out.append((n,float(np.mean(ps)),float(np.std(ps))))
    return out
# get S&P 500 tickers
import urllib.request
url="https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"
try:
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
    import io
    csv=urllib.request.urlopen(req,timeout=30).read().decode()
    tickers=[r.split(",")[0].replace(".","-") for r in csv.strip().splitlines()[1:]]
    print(f"S&P500 tickers: {len(tickers)}")
except Exception as e:
    print("ticker fetch failed:",e); sys.exit(2)
cache=os.path.join(HERE,"fullmarket_returns.parquet")
if os.path.exists(cache):
    rets=pd.read_parquet(cache)
else:
    print("downloading (may take a few min)...")
    data=yf.download(tickers,period="6y",interval="1d",progress=False,auto_adjust=True,threads=True)
    close=data["Close"] if isinstance(data.columns,pd.MultiIndex) else data
    close=close.dropna(axis=1,thresh=int(0.98*len(close))).dropna(axis=0,how="any")
    rets=np.log(close).diff().dropna(); rets.to_parquet(cache)
X=rets.to_numpy().T; good=np.isfinite(X).all(1)&(X.std(1)>1e-12); X=X[good]
N,T=X.shape; print(f"matrix N={N} stocks x T={T} days")
ev=corr_eig(X); PR=pr(ev)
sizes=[20,30,50,75,100,150,200,300,400,N]
curve=subsample_pr(X,sizes)
cn=np.array([c[0] for c in curve],float); cp=np.array([c[1] for c in curve])
up=cn>=100; beta=float(np.polyfit(np.log10(cn[up]),np.log10(cp[up]),1)[0])
print("\nSATURATION CURVE (PR vs N'):")
for n,p,s in curve: print(f"  N'={n:4d}  PR={p:6.2f} +/- {s:.2f}")
print(f"\nfull-N PR/k_eff={PR:.2f}  beta(>=100)={beta:.4f}  market_mode={ev[0]:.1f} ({100*ev[0]/ev.sum():.1f}%)")
print("top8 eigs:",[round(float(x),1) for x in ev[:8]])
verdict=("SATURATES (low-rank holds at full market)" if beta<0.15 else
         "KEEPS CLIMBING (S&P-100 saturation was small-N artifact)" if beta>0.3 else "PARTIAL")
print("VERDICT:",verdict)
json.dump(dict(N=N,T=T,PR=PR,beta=beta,market_mode_frac=float(ev[0]/ev.sum()),
    saturation_curve=curve,top_eigs=[float(x) for x in ev[:12]],verdict=verdict),
    open(os.path.join(HERE,"finance_fullmarket_results.json"),"w"),indent=1)
print("wrote finance_fullmarket_results.json")
