#!/usr/bin/env python3
"""
Post-analysis + figure for the anesthesia two-axis TRAJECTORY.

Reads spectral_results_anesthesia_trajectory.json (+ baseline_windows_*.json) and:
  1. Tests whether each axis actually SEPARATES awake -> deep (Mann-Whitney,
     Cliff's delta): only a separated axis has a meaningful "collapse time".
  2. Locates each axis's transition midpoint time (robust: smoothed midpoint
     crossing on the induction window) with a block-bootstrap CI over windows.
  3. Emits the ORDERING (DB drop before / with / after k_eff), or UNRESOLVED.
  4. Plots k_eff and DB |z| (both estimators) vs time with the injection and
     deep-onset markers and the collapse-time bands.

Real data only. No commit.
"""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "spectral_results_anesthesia_trajectory.json")

def cliffs_delta(a, b):
    a = np.asarray(a); b = np.asarray(b)
    gt = sum((x > b).sum() for x in a); lt = sum((x < b).sum() for x in a)
    return (gt - lt) / (len(a)*len(b))

def mannwhitney(a, b):
    from scipy.stats import mannwhitneyu
    try: return float(mannwhitneyu(a, b, alternative="two-sided").pvalue)
    except Exception: return float("nan")

def smooth(y, k=5):
    return np.array([np.median(y[max(0,i-k//2):i+k//2+1]) for i in range(len(y))])

def midpoint_time(ts, y, awake_lvl, deep_lvl, lo, hi, ksm=5):
    ys = smooth(y, ksm); mid = 0.5*(awake_lvl+deep_lvl)
    for i in range(1, len(ts)):
        if ts[i] < lo or ts[i] > hi: continue
        if (ys[i-1]-mid)*(ys[i]-mid) < 0 and ys[i] != ys[i-1]:
            f = (mid-ys[i-1])/(ys[i]-ys[i-1])
            return float(ts[i-1]+f*(ts[i]-ts[i-1]))
    return None

def analyze_agent(agent, sess, base):
    rows = sess["windows"]
    inj = sess["injection_t"]; d0 = sess["deep_t0"]; d1 = sess["deep_t1"]
    ts = np.array([r["t_center"] for r in rows])
    out = {"injection_t": inj, "deep_t0": d0, "deep_t1": d1}
    # awake-baseline window arrays (Session1)
    bpath = os.path.join(HERE, f"baseline_windows_{agent}.json")
    bwin = json.load(open(bpath)) if os.path.exists(bpath) else []
    deep_rows = [r for r in rows if r["epoch"] == "deep"]
    keys = [("k_eff","k_eff",False), ("db_z_winding","db_winding",True),
            ("db_z_circ_sum","db_circ",True)]
    lo, hi = (inj or 0), ((d0+90) if d0 else ts.max())
    out["search_window"] = [lo, hi]
    for jkey, name, ab in keys:
        aw = np.array([abs(r[jkey]) if ab else r[jkey] for r in bwin]) if bwin else np.array([])
        dp = np.array([abs(r[jkey]) if ab else r[jkey] for r in deep_rows])
        y  = np.array([abs(r[jkey]) if ab else r[jkey] for r in rows])
        awake_lvl = float(np.median(aw)) if len(aw) else float("nan")
        deep_lvl  = float(np.median(dp)) if len(dp) else float("nan")
        sep = dict(awake=awake_lvl, deep=deep_lvl,
                   separated = bool(np.isfinite(awake_lvl) and np.isfinite(deep_lvl)),
                   mw_p = mannwhitney(aw, dp) if len(aw) and len(dp) else float("nan"),
                   cliffs = cliffs_delta(aw, dp) if len(aw) and len(dp) else float("nan"))
        tmid = midpoint_time(ts, y, awake_lvl, deep_lvl, lo, hi) if sep["separated"] else None
        # block-bootstrap CI on tmid (resample windows in blocks of 5, recompute)
        cis = []
        if sep["separated"]:
            rng = np.random.default_rng(0); n=len(ts); blk=5
            for _ in range(200):
                idx = np.sort(rng.integers(0, n, n))
                tt, yy = ts[idx], y[idx]
                o = tt.argsort(); tt, yy = tt[o], yy[o]
                tc = midpoint_time(tt, yy, awake_lvl, deep_lvl, lo, hi)
                if tc is not None: cis.append(tc)
        ci = [float(np.percentile(cis,2.5)), float(np.percentile(cis,97.5))] if len(cis)>20 else None
        out[name] = dict(sep=sep, t_mid=tmid, t_mid_ci=ci,
                         cliffs_abs=abs(sep["cliffs"]) if np.isfinite(sep["cliffs"]) else float("nan"))
    return out

def verdict(a):
    tk = a["k_eff"]["t_mid"]
    lines = []
    for name in ("db_winding","db_circ"):
        db = a[name]
        if not db["sep"]["separated"] or abs(db["sep"]["cliffs"]) < 0.33 or db["t_mid"] is None:
            lines.append(f"  vs {name}: UNRESOLVED "
                         f"(DB awake={db['sep']['awake']:.2f} deep={db['sep']['deep']:.2f}, "
                         f"|cliff|={db['cliffs_abs']:.2f}, p={db['sep']['mw_p']:.2g}) "
                         f"-- DB does not cleanly separate/collapse")
            continue
        td = db["t_mid"]
        if tk is None:
            lines.append(f"  vs {name}: k_eff has no crossing (?)"); continue
        d = td - tk
        rel = "WITH" if abs(d) < 30 else ("AFTER k_eff" if d>0 else "BEFORE k_eff")
        lines.append(f"  vs {name}: k_eff@{tk:.0f}s  DB@{td:.0f}s  ->  DB drops {rel} (Δ={d:+.0f}s)")
    return lines

def plot(results, post):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    agents = list(results["sessions"].keys())
    fig, axes = plt.subplots(len(agents), 1, figsize=(10, 4.2*len(agents)), squeeze=False)
    for ai, agent in enumerate(agents):
        s = results["sessions"][agent]; rows = s["windows"]; a = post[agent]
        ts = np.array([r["t_center"] for r in rows])
        keff = np.array([r["k_eff"] for r in rows])
        wind = np.abs([r["db_z_winding"] for r in rows])
        circ = np.abs([r["db_z_circ_sum"] for r in rows])
        ax = axes[ai][0]
        ax.plot(ts, keff, color="#1f77b4", lw=1.6, label="k_eff (Axis 1)")
        ax.set_ylabel("k_eff", color="#1f77b4"); ax.tick_params(axis="y", labelcolor="#1f77b4")
        ax2 = ax.twinx()
        ax2.plot(ts, smooth(wind,5), color="#d62728", lw=1.3, alpha=.85, label="|DB z| winding")
        ax2.plot(ts, smooth(circ,5), color="#ff7f0e", lw=1.3, alpha=.85, label="|DB z| circ")
        ax2.axhline(1.5, color="gray", ls=":", lw=1, label="null ceiling ~1.5")
        ax2.set_ylabel("|DB z| (Axis 2)")
        if s["injection_t"]: ax.axvline(s["injection_t"], color="k", ls="--", lw=1)
        if s["deep_t0"]: ax.axvspan(s["deep_t0"], min(s["deep_t1"], ts.max()), color="gray", alpha=.12)
        tk = a["k_eff"]["t_mid"]
        if tk: ax.axvline(tk, color="#1f77b4", ls="-.", lw=1.2)
        ax.set_title(f"{agent}: inj@{s['injection_t']:.0f}s, deep-onset@{s['deep_t0']:.0f}s "
                     f"(shaded); k_eff collapse@{tk:.0f}s" if tk else agent)
        ax.set_xlabel("time (s)")
        l1,lab1 = ax.get_legend_handles_labels(); l2,lab2 = ax2.get_legend_handles_labels()
        ax.legend(l1+l2, lab1+lab2, fontsize=8, loc="upper right")
    fig.tight_layout()
    p = os.path.join(HERE, "spectral_anesthesia_trajectory.png")
    fig.savefig(p, dpi=130); print("wrote", p)

def main():
    results = json.load(open(RES))
    post = {}
    print("=== ANESTHESIA TRAJECTORY POST-ANALYSIS ===")
    for agent in results["sessions"]:
        a = analyze_agent(agent, results["sessions"][agent], results["baseline"].get(agent))
        post[agent] = a
        print(f"\n{agent}: search window {a['search_window'][0]:.0f}-{a['search_window'][1]:.0f}s")
        for name in ("k_eff","db_winding","db_circ"):
            r = a[name]; s = r["sep"]
            print(f"  {name:11s} awake={s['awake']:6.2f} deep={s['deep']:6.2f} "
                  f"|cliff|={r['cliffs_abs']:.2f} p={s['mw_p']:.2g}  "
                  f"t_mid={('%.0f'%r['t_mid']) if r['t_mid'] is not None else 'None':>5s}s "
                  f"CI={r['t_mid_ci']}")
        print("  ORDERING:")
        for line in verdict(a): print(line)
    json.dump(post, open(os.path.join(HERE, "anesthesia_trajectory_ordering.json"), "w"), indent=1)
    plot(results, post)

if __name__ == "__main__":
    main()
