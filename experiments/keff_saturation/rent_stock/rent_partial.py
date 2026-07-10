"""Neural-rung replication of exp118's rent-tracks-stock. Orchestrator run.
Clause 5 anchor: does maintenance (DB) correlate positively with held stock S,
within session, controlling for epoch/time?  k=128 channels."""
import json, numpy as np
from scipy import stats
rng = np.random.default_rng(20260710)
K = 128.0

def S_closed(rho, k=K):
    rho = np.clip(rho, 1e-9, 1-1e-9)
    return -np.log(1 + rho*(k-1)) - (k-1)*np.log(1-rho)

def block_boot_spearman_partial(x, y, z, L, B=2000):
    """Spearman partial corr of x,y controlling z; block bootstrap over windows."""
    n = len(x)
    def partial(xi, yi, zi):
        rx = stats.rankdata(xi); ry = stats.rankdata(yi); rz = stats.rankdata(zi)
        def resid(a, b):
            b1 = np.c_[np.ones(n), b]
            return a - b1 @ np.linalg.lstsq(b1, a, rcond=None)[0]
        return np.corrcoef(resid(rx, rz), resid(ry, rz))[0,1]
    pt = partial(x, y, z)
    nb = int(np.ceil(n/L)); out=[]
    for _ in range(B):
        starts = rng.integers(0, max(n-L,1), size=nb)
        idx = np.concatenate([np.arange(s, min(s+L,n)) for s in starts])[:n]
        if len(np.unique(idx)) < 12: continue
        try: out.append(partial(x[idx], y[idx], z[idx]))
        except Exception: pass
    lo, hi = np.percentile(out, [2.5, 97.5]) if out else (np.nan, np.nan)
    return pt, lo, hi

def acf_block(x, maxlag=40):
    x = x - x.mean()
    ac = [1.0]+[np.corrcoef(x[:-l], x[l:])[0,1] for l in range(1, maxlag)]
    ac = np.array(ac)
    first = np.argmax(ac < 1/np.e) if np.any(ac < 1/np.e) else maxlag
    return max(int(first)*2, 4)

print(f"{'session':22s} {'N':>4s} {'maint':>10s} {'partial rho':>12s} {'95% CI':>20s} {'L':>3s}")
print("-"*80)
rows=[]
for animal, tag in [('chibi',''), ('george','_george')]:
    for agent in ['propofol','ketamine']:
        f = f"trajectory_windows_{agent}{tag}.jsonl"
        try: ws=[json.loads(l) for l in open(f)]
        except FileNotFoundError: continue
        rho = np.array([w['rho_kish'] for w in ws])
        S   = S_closed(rho)
        t   = np.array([w['t_center'] for w in ws])
        L   = acf_block(S)
        for maint_key in ['db_z_winding','db_z_circ_sum']:
            m = np.array([w[maint_key] for w in ws])
            pt, lo, hi = block_boot_spearman_partial(S, m, t, L)
            sig = "" if (lo<0<hi) else ("  POSITIVE" if pt>0 else "  NEGATIVE")
            print(f"{animal+'/'+agent:22s} {len(ws):4d} {maint_key.replace('db_z_',''):>10s} "
                  f"{pt:+12.3f} [{lo:+.3f},{hi:+.3f}]{sig}")
            rows.append((animal,agent,maint_key,pt,lo,hi,len(ws)))
print()
# pooled by agent (Fisher z on partials, session-weighted)
for agent in ['propofol','ketamine']:
    for mk in ['db_z_winding','db_z_circ_sum']:
        rs=[r for r in rows if r[1]==agent and r[2]==mk]
        if not rs: continue
        z = np.mean([np.arctanh(np.clip(r[3],-.999,.999)) for r in rs])
        print(f"pooled {agent:10s} {mk.replace('db_z_',''):>10s}: partial rho = {np.tanh(z):+.3f}  (n_sessions={len(rs)})")
