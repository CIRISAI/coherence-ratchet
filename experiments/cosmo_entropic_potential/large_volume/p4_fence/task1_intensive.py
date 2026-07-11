#!/usr/bin/env python3
"""
P4 intensive fence, Task 1: S/k from the frozen primary records.
Pure CPU. Reads large_volume/results.json (stage2_primary.records), computes
the intensive measure S/k(a), its spline dlnS/dlna slope (s_of_a.dln_dlna) and
the global OLS slope in ln-ln. Verdict: rising (phantom, w<-1) or falling.
Incremental write to p4_fence/results.json.
"""
import json, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
LV = HERE.parent
CEP = LV.parent
sys.path.insert(0, str(CEP))
import s_of_a as S  # dln_dlna cubic-spline slope; CAMELS globals irrelevant here

recs = json.load(open(LV / "results.json"))["stage2_primary"]["records"]
a = np.array([r["a"] for r in recs])
k = np.array([r["k"] for r in recs], float)
Sext = np.array([r["S"] for r in recs])
order = np.argsort(a)
a, k, Sext = a[order], k[order], Sext[order]

def report(name, avals, yvals):
    avals = np.asarray(avals, float); yvals = np.asarray(yvals, float)
    d = S.dln_dlna(avals, yvals)          # spline dlnY/dlna at each node
    w = -1.0 - d / 3.0                     # entropic-potential w mapping
    ols = float(np.polyfit(np.log(avals), np.log(yvals), 1)[0])
    return {
        "name": name,
        "a": avals.tolist(),
        "y": yvals.tolist(),
        "dlnY_dlna_spline": d.tolist(),
        "w_spline": w.tolist(),
        "dlnY_dlna_today": float(d[-1]),
        "w_today": float(w[-1]),
        "ols_global_slope": ols,
        "w_from_ols": float(-1.0 - ols / 3.0),
        "y_first_last": [float(yvals[0]), float(yvals[-1])],
        "argmax_idx": int(np.argmax(yvals)),
        "peak_a": float(avals[np.argmax(yvals)]),
        "peak_interior": bool(0 < np.argmax(yvals) < len(yvals) - 1),
        # phantom = ANY rising node (spline slope > 0)
        "n_rising_nodes": int((d > 0).sum()),
        "max_spline_slope": float(d.max()),
        "phantom_anywhere": bool((d > 0).any()),
    }

out = {
    "task": "P4 intensive fence — Task 1 (S/k from frozen primary records)",
    "note": "phantom (w<-1) <=> measure RISING (dlnY/dlna > 0)",
    "intensive_S_over_k": report("S/k", a, Sext / k),
    "extensive_S_reference": report("S (extensive, reference)", a, Sext),
}
with open(HERE / "results.json", "w") as fh:
    json.dump(out, fh, indent=1)

for key in ("extensive_S_reference", "intensive_S_over_k"):
    r = out[key]
    print(f"\n=== {r['name']} ===")
    print(f"  y first->last: {r['y_first_last'][0]:.5g} -> {r['y_first_last'][1]:.5g}")
    print(f"  peak at a={r['peak_a']:.3f} (interior={r['peak_interior']})")
    print(f"  OLS global slope (ln-ln): {r['ols_global_slope']:+.4f}  -> w={r['w_from_ols']:+.3f}")
    print(f"  spline slope today:       {r['dlnY_dlna_today']:+.4f}  -> w_today={r['w_today']:+.3f}")
    print(f"  rising nodes: {r['n_rising_nodes']}/{len(r['a'])}  max slope {r['max_spline_slope']:+.4f}  phantom_anywhere={r['phantom_anywhere']}")
print("\nwrote p4_fence/results.json")
