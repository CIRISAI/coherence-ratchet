#!/usr/bin/env python3
"""Analyze the coupled-dynamics scaling results against the pre-registered gates
(DECISIONS.md) and emit the verdict table. Read-only; no data generation."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    p = os.path.join(HERE, name)
    return json.load(open(p)) if os.path.exists(p) else []


def g1(inv, key="TC"):
    """genuine-signal gate: genuine > 5 * null_scatter."""
    d = inv[key]
    return d["genuine"] > 5 * d["null_scatter"], d


def verdict_scaling(recs):
    couplings = ["independent", "global_parity", "block_parity", "vouching"]
    R_grid = sorted({r["R"] for r in recs if r["tag"] == "scaling"})
    out = {}
    for c in couplings:
        rows = sorted([r for r in recs if r["coupling"] == c
                       and r["tag"] == "scaling"], key=lambda r: r["R"])
        if not rows:
            continue
        tc_gen = {r["R"]: r["invariants"]["TC"]["genuine"] for r in rows}
        tc_sc = {r["R"]: r["invariants"]["TC"]["null_scatter"] for r in rows}
        tau_gen = {r["R"]: r["invariants"]["tau_k"]["genuine"] for r in rows}
        rho = {r["R"]: r["pairwise_rho"]["mean_abs_all"] for r in rows}
        occmin = {r["R"]: r["occ_marginal_min"] for r in rows}
        occmax = {r["R"]: r["occ_marginal_max"] for r in rows}
        Rmax = max(tc_gen)
        R3 = min(tc_gen)
        maxtc = max(tc_gen.values())
        # gates
        G1 = all(tc_gen[R] > 5 * tc_sc[R] for R in tc_gen if tc_gen[R] > 1e-9) \
            if maxtc > 1e-6 else False
        G2 = all(rho[R] < 0.10 for R in rho)          # low pairwise rho (Third)
        G3 = all(0.05 < occmin[R] and occmax[R] < 0.95 for R in occmin) \
            and all(tau_gen[R] < 0.90 for R in tau_gen)
        # G4 non-diluting on RAW TC
        tc13 = tc_gen[Rmax]
        G4 = (tc13 >= 0.5 * maxtc) and (tc13 > 5 * tc_sc[Rmax]) if maxtc > 1e-6 \
            else False
        diluting = (maxtc > 1e-6 and (tc13 < 0.2 * tc_gen[R3]
                    or tc13 <= 5 * tc_sc[Rmax]))
        if maxtc < 1e-6:
            cls = "EMPTY (no signal — the R2-like null)"
        elif not G2:
            cls = "SECONDNESS (pairwise rho high — not a Third)"
        elif G1 and G2 and G3 and G4:
            cls = "NON-DILUTING THIRD (passes G1-G4)"
        elif diluting:
            cls = "DILUTING"
        else:
            cls = "AMBIGUOUS"
        out[c] = dict(R_grid=R_grid, tc_gen=tc_gen, tc_scatter=tc_sc,
                      tau_gen=tau_gen, rho=rho, occ_min=occmin, occ_max=occmax,
                      G1=G1, G2=G2, G3=G3, G4=G4, verdict=cls,
                      tc_R3=tc_gen[R3], tc_Rmax=tc13, R3=R3, Rmax=Rmax)
    return out


if __name__ == "__main__":
    sc = load("results_scaling.json")
    v = verdict_scaling(sc)
    print("=" * 78)
    print("SCALING VERDICT (g=1, q=1)  — raw TC_genuine, bias-subtracted")
    print("=" * 78)
    for c, d in v.items():
        print(f"\n{c}:  {d['verdict']}")
        print(f"  {'R':>3} {'TC_gen':>9} {'scatter':>9} {'tau_gen':>8} "
              f"{'rho_all':>8} {'occ_min':>8} {'occ_max':>8}")
        for R in d["R_grid"]:
            if R in d["tc_gen"]:
                print(f"  {R:>3} {d['tc_gen'][R]:>9.4f} {d['tc_scatter'][R]:>9.4f} "
                      f"{d['tau_gen'][R]:>8.4f} {d['rho'][R]:>8.4f} "
                      f"{d['occ_min'][R]:>8.3f} {d['occ_max'][R]:>8.3f}")
        print(f"  gates: G1(signal)={d['G1']} G2(rho<0.10)={d['G2']} "
              f"G3(not-rigid)={d['G3']} G4(non-diluting)={d['G4']}")
        print(f"  TC_gen(R={d['R3']})={d['tc_R3']:.4f} -> "
              f"TC_gen(R={d['Rmax']})={d['tc_Rmax']:.4f}")
