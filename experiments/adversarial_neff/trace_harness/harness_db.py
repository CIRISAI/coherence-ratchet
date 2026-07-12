#!/usr/bin/env python3
"""HARNESS B - detailed-balance / rent probe on within-task score dynamics.

The program's validated maintenance-axis estimator (keff_saturation/
entropy_production.py) measures broken detailed balance two ways: transition
EP = Sum P_ij log(P_ij/P_ji) on a coarse-grained state space, and net winding
rate over mode-pairs. Both need LONG trajectories (T >> n_states; brains
T~1e3-1e4). Our within-task thought sequences are SHORT (2-11 thoughts, max 11),
so neither runs per-sequence. The winding estimator is inapplicable here.

HONEST ADAPTATION (stated as such): pool the within-task one-step transitions
across many tasks in a condition onto a SHARED coarse-grained score-state space,
and test that pooled ensemble for directional asymmetry (P_ij vs P_ji). This is
the transition-EP estimator (_counts/_ep, exactly the entropy_production.py
form) applied to a pooled ensemble rather than one long series. It answers "is
constraint resolution a directed cycle in score space?" at the ensemble level.
Minimum requirement is on POOLED transitions: N_trans >> n_states^2, NOT on
individual sequence length. Significance floor = symmetrized-count Markov
surrogates (detailed balance by construction), matching entropy_production.py.

Ordering within task: by `id` (timestamp is scrubbed; see loader.py).

WHAT THIS IS: validation that the pipeline yields STABLE numbers on benign data
and a documented minimum-length/-count requirement -- NOT a deception claim.
On the mesh traces it will ask whether a kept deception breaks detailed balance
in score dynamics even when surface scores pass; here we only calibrate it.
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import loader as L

def pooled_transitions(seqs, axes):
    """seqs: list of within-task ordered rows. Returns (P0, P1) arrays of
    consecutive score-vectors (complete-case on axes) pooled across sequences."""
    P0, P1 = [], []
    for s in seqs:
        vecs = []
        for r in s:
            v = [r.get(a) for a in axes]
            vecs.append([float(x) for x in v] if all(L.is_num(x) for x in v) else None)
        for a, b in zip(vecs[:-1], vecs[1:]):
            if a is not None and b is not None:
                P0.append(a); P1.append(b)
    return np.asarray(P0, float), np.asarray(P1, float)

def ep_pooled(P0, P1, ref_mean, ref_std, proj, edges, n_bins):
    """Discretize pooled (P0->P1) transitions onto the shared grid and compute
    EP = Sum P_ij log(P_ij/P_ji)."""
    def code(P):
        Z = (P - ref_mean) / ref_std
        Y = Z @ proj                      # project to top dims
        c = np.zeros(len(P), dtype=np.int64)
        for a in range(Y.shape[1]):
            c = c*n_bins + np.digitize(Y[:, a], edges[a])
        return c
    M = n_bins ** proj.shape[1]
    ci = code(P0); cj = code(P1)
    C = np.zeros((M, M))
    np.add.at(C, (ci, cj), 1.0)
    Cs = C + 1e-9
    Pm = Cs / Cs.sum()
    ep = float(np.sum(Pm * np.log(Pm / Pm.T)))
    return ep, C

def analyze(rows, axes, label, n_dims=2, seed=0, n_surr=500):
    seqs = L.sequences(rows, min_len=2)
    P0, P1 = pooled_transitions(seqs, axes)
    n_trans = len(P0)
    res = {"label": label, "n_sequences": len(seqs), "n_transitions": int(n_trans),
           "axes": list(axes)}
    if n_trans < 20:
        res["status"] = f"insufficient pooled transitions ({n_trans} < 20) -- EP undefined"
        return res
    # shared state space: standardize on pooled endpoints, PCA to n_dims,
    # adaptive bins so n_states <= n_trans/10 (the T>>n_states requirement).
    allpts = np.vstack([P0, P1])
    mu = allpts.mean(0); sd = allpts.std(0) + 1e-9
    Z = (allpts - mu) / sd
    # PCA
    U, S, Vt = np.linalg.svd(Z - Z.mean(0), full_matrices=False)
    d = min(n_dims, (sd > 1e-9).sum(), Vt.shape[0])
    proj = Vt[:d].T
    # choose bins: largest b with b^d <= n_trans/10, capped at 3, floor 2
    b = 2
    while (b+1)**d <= n_trans/10 and b < 3:
        b += 1
    Yall = ((allpts - mu)/sd) @ proj
    edges = [np.quantile(Yall[:, a], np.linspace(0, 1, b+1)[1:-1]) for a in range(d)]
    ep, C = ep_pooled(P0, P1, mu, sd, proj, edges, b)
    M = b**d
    res.update(n_states=int(M), n_dims=int(d), n_bins=int(b),
               transitions_per_state=float(n_trans/M))
    # significance floor: symmetrize counts (detailed balance by construction),
    # simulate same-length Markov trajectories, recompute EP.
    Csym = (C + C.T)/2
    row = Csym.sum(1, keepdims=True)
    T = np.divide(Csym, row, out=np.zeros_like(Csym), where=row > 0)
    rng = np.random.default_rng(seed)
    p0 = Csym.sum(1)/Csym.sum()
    floor = []
    for _ in range(n_surr):
        st = np.zeros(n_trans+1, dtype=np.int64)
        st[0] = rng.choice(M, p=p0)
        for t in range(n_trans):
            pr = T[st[t]]
            st[t+1] = rng.choice(M, p=pr) if pr.sum() > 0 else rng.choice(M, p=p0)
        Cf = np.zeros((M, M)); np.add.at(Cf, (st[:-1], st[1:]), 1.0)
        Cf += 1e-9; Pf = Cf/Cf.sum()
        floor.append(float(np.sum(Pf*np.log(Pf/Pf.T))))
    floor = np.array(floor)
    z = (ep - floor.mean())/(floor.std()+1e-12)
    # bootstrap EP over transitions (stability of the point estimate)
    boot = []
    for _ in range(300):
        s = rng.integers(0, n_trans, n_trans)
        e, _ = ep_pooled(P0[s], P1[s], mu, sd, proj, edges, b)
        boot.append(e)
    boot = np.array(boot)
    res.update(ep=float(ep), floor_mean=float(floor.mean()), floor_std=float(floor.std()),
               z=float(z),
               ep_boot=dict(median=float(np.median(boot)),
                            lo68=float(np.percentile(boot, 16)), hi68=float(np.percentile(boot, 84))),
               status="ok")
    return res

def run():
    rows = L.load_context()
    out = {"harness": "B / detailed-balance (rent) probe",
           "estimator": "pooled transition-EP on shared coarse-grained score space; "
                        "symmetrized-Markov surrogate floor (entropy_production.py form)",
           "ordering": "within-task by `id` (timestamp scrubbed)",
           "min_requirement": "N_trans >> n_states^2 (pooled); per-sequence winding estimator inapplicable at these lengths",
           "note": "pipeline-stability validation on benign data; NOT a deception result",
           "conditions": {}}
    # PRIMARY axes: core4 (complete-case, no missingness confound)
    specs = [
        ("Ally/real_user_web (benign)", dict(agent="Ally", task_class="real_user_web")),
        ("Ally/unknown (benign)",       dict(agent="Ally", task_class="unknown")),
        ("Ally/qa_eval (benign)",       dict(agent="Ally", task_class="qa_eval")),
        ("Ally/overridden (class-matched set)", dict(agent="Ally", overridden=True)),
        ("Scout (all)",                 dict(agent="Scout")),
        ("Scout/overridden anomalies",  dict(agent="Scout", overridden=True)),
    ]
    for label, sel in specs:
        g = L.group(rows, **sel)
        r = analyze(g, L.CORE4, label)
        out["conditions"][label] = r
        if r.get("status") == "ok":
            print(f"{label:38s} N_trans={r['n_transitions']:5d} states={r['n_states']:2d} "
                  f"EP={r['ep']:.4f} floor={r['floor_mean']:.4f}+/-{r['floor_std']:.4f} z={r['z']:+.2f}")
        else:
            print(f"{label:38s} {r['status']}")
    return out

if __name__ == "__main__":
    out = run()
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_db.json")
    json.dump(out, open(p, "w"), indent=1)
    print("wrote", p)
