#!/usr/bin/env python3
"""HARNESS A - constraint-axis N_eff on the public CIRIS traces.

Computes, per (agent, task_class) group, the effective dimensionality of the
constraint-score system two ways:

  N_eff_PR  = (Sum lambda_i)^2 / Sum lambda_i^2   (participation ratio of the
              correlation-matrix eigenvalues) -- the ROBUST headline, matches
              SPEC's Neff_PR, well-defined for any correlation matrix.
  k_eff_eq  = k / (1 + rho_bar*(k-1))             (the program's equicorrelation
              identity, Core/BaseIdentity.lean). rho_bar = mean off-diagonal
              correlation. Only meaningful for rho_bar>0 near-equicorrelation;
              with mixed-sign correlations it can exceed k or go negative -- we
              report it WITH rho_bar and a validity flag, never alone.

Error bars: nonparametric bootstrap over TRACES within the group (B resamples),
report median and 68% / 95% percentile intervals.

IMPORTANT CAVEATS (see DECISIONS.md, printed in output):
 - trace_context exposes 8 summary constraint scores, NOT the paper's
   standardized 16-dim H3ERE feature vector. N_eff here is a coarse <=8-axis
   proxy and is NOT numerically comparable to the paper's 7.1 / 9.
 - idma_k_eff, idma_correlation_risk are version-dependent; cross-version
   comparisons are confounded.
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import loader as L

def corr(X):
    """Pearson correlation matrix of columns; drops zero-variance columns."""
    sd = X.std(0)
    keep = sd > 1e-9
    Xk = X[:, keep]
    if Xk.shape[1] < 2:
        return None, keep
    return np.corrcoef(Xk, rowvar=False), keep

def neff_pr(R):
    w = np.linalg.eigvalsh(R)
    w = np.clip(w, 0, None)
    s1, s2 = w.sum(), (w**2).sum()
    return float(s1*s1/s2) if s2 > 0 else float("nan")

def rho_bar(R):
    k = R.shape[0]
    off = (R.sum() - np.trace(R)) / (k*(k-1))
    return float(off)

def keff_eq(R):
    k = R.shape[0]
    rb = rho_bar(R)
    denom = 1 + rb*(k-1)
    val = k/denom if abs(denom) > 1e-9 else float("nan")
    valid = rb > 0 and denom > 0            # equicorrelation identity domain
    return float(val), rb, bool(valid)

def analyze(rows, axes, label, B=2000, seed=0, min_n=8):
    X, idx = L.axis_matrix(rows, axes, complete_case=True)
    n = X.shape[0]
    res = {"label": label, "axes": list(axes), "n_traces_group": len(rows),
           "n_complete_case": int(n), "k_axes": len(axes)}
    if n < min_n:
        res["status"] = f"insufficient complete-case n ({n} < {min_n})"
        return res
    R, keep = corr(X)
    if R is None:
        res["status"] = "insufficient non-constant axes"; return res
    res["axes_used"] = [a for a, k in zip(axes, keep) if k]
    res["k_used"] = int(R.shape[0])
    res["neff_pr"] = neff_pr(R)
    ke, rb, valid = keff_eq(R)
    res["rho_bar"] = rb
    res["keff_equicorr"] = ke
    res["keff_equicorr_valid"] = valid
    res["corr_matrix"] = np.round(R, 3).tolist()
    # bootstrap over traces
    rng = np.random.default_rng(seed)
    pr, ke_b, rb_b = [], [], []
    for _ in range(B):
        s = rng.integers(0, n, n)
        Rb, kk = corr(X[s])
        if Rb is None: continue
        pr.append(neff_pr(Rb))
        k2, r2, _ = keff_eq(Rb)
        ke_b.append(k2); rb_b.append(r2)
    pr = np.array(pr)
    def ci(a):
        a = np.asarray(a); a = a[np.isfinite(a)]
        return dict(median=float(np.median(a)),
                    lo68=float(np.percentile(a, 16)), hi68=float(np.percentile(a, 84)),
                    lo95=float(np.percentile(a, 2.5)), hi95=float(np.percentile(a, 97.5)))
    res["neff_pr_boot"] = ci(pr)
    res["rho_bar_boot"] = ci(rb_b)
    res["status"] = "ok"
    return res

def run():
    rows = L.load_context()
    out = {"harness": "A / constraint-axis N_eff",
           "ordering": "n/a (per-trace)",
           "caveats": [
               "8 summary scores, NOT the paper's 16-dim H3ERE vector; N_eff is a coarse proxy, not comparable to 7.1/9.",
               "idma_k_eff & idma_correlation_risk are version-dependent (v2.0-2.5 vs v2.7); cross-version comparison confounded.",
               "small-n groups (Scout n=36) have wide bootstrap intervals -- read the CI, not the point.",
           ],
           "groups": {}}
    # matched-class headline + context groups
    specs = [
        ("Scout/real_user_web",  dict(agent="Scout", task_class="real_user_web")),
        ("Ally/real_user_web",   dict(agent="Ally",  task_class="real_user_web")),
        ("Ally/qa_eval",         dict(agent="Ally",  task_class="qa_eval")),
        ("Ally/unknown",         dict(agent="Ally",  task_class="unknown")),
        ("Scout/wakeup_ritual",  dict(agent="Scout", task_class="wakeup_ritual")),
        ("Ally/real_user_web/overridden", dict(agent="Ally", task_class="real_user_web", overridden=True)),
    ]
    for label, sel in specs:
        g = L.group(rows, **sel)
        entry = {}
        entry["core4"] = analyze(g, L.CORE4, label + " [core4]")
        entry["all8"]  = analyze(g, L.ALL8,  label + " [all8]")
        out["groups"][label] = entry
        c = entry["core4"]
        if c.get("status") == "ok":
            b = c["neff_pr_boot"]
            print(f"{label:34s} core4 N_eff_PR={c['neff_pr']:.2f} "
                  f"[{b['lo68']:.2f},{b['hi68']:.2f}]68 rho_bar={c['rho_bar']:+.3f} "
                  f"(n_cc={c['n_complete_case']}, k={c['k_used']})")
        else:
            print(f"{label:34s} core4 {c['status']}")
    return out

if __name__ == "__main__":
    out = run()
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_neff.json")
    json.dump(out, open(p, "w"), indent=1)
    print("wrote", p)
