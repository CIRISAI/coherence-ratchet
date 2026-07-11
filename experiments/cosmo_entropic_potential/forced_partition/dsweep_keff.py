#!/usr/bin/env python3
"""D-sweep: does k_eff at the maintained steady state SATURATE as total dimension
grows, per allocation rule? Sideways follow-up to forced_partition.py (orchestrator,
same day). Exact block-Kish spectra (no d=1 sectors; per-sector eigenvalues
(d-1)x(1-rho) and 1x(1+(d-1)rho)); heterogeneous sectors, growing count.
Dynamics identical to the parent run: drho_k/dt = a(1-rho_k) - gamma*m_k,
per-unit budget b, allocation weights per rule, a=gamma=1."""
import json
import numpy as np
from scipy.integrate import solve_ivp

A = GAMMA = 1.0
S_of = lambda d, r: (d - 1) * (-np.log(1 - r)) - np.log(1 + (d - 1) * r) + 0 * r  # exact block log-det... see below
# exact block log-det: -ln det = -( (d-1)ln(1-rho) + ln(1+(d-1)rho) )
def S_block(d, r):
    return -((d - 1) * np.log(1 - r) + np.log(1 + (d - 1) * r))

def weights(rule, d, r):
    if rule == "A_equal":
        return np.ones_like(r)
    if rule == "B_stock":
        return np.maximum(S_block(d, np.clip(r, 1e-9, 1 - 1e-9)), 1e-12) / d
    if rule == "C_rate":
        return A * (1 - r) / (1 - np.clip(r, 0, 1 - 1e-9)) * 0 + A  # rate of S under drift: dS/dt = dS/drho * a(1-rho)
    if rule == "D_need":
        return A * (1 - r)
    raise ValueError(rule)

def dSdrho(d, r):
    return (d - 1) / (1 - r) - (d - 1) / (1 + (d - 1) * r)

def rhs(rule, d, b):
    Dtot = d.sum()
    def f(t, r):
        r = np.clip(r, 0.0, 1 - 1e-9)
        if rule == "C_rate":
            w = np.abs(dSdrho(d, r) * A * (1 - r)) / d
        else:
            w = weights(rule, d, r)
        w = np.maximum(w, 1e-12)
        m = b * Dtot * (w * d) / (w * d).sum() / d      # per-unit allocation, budget b*Dtot total
        return A * (1 - r) - GAMMA * m
    return f

def keff(d, r):
    ev = []
    for dk, rk in zip(d, r):
        dk = int(dk)
        ev += [1 - rk] * (dk - 1) + [1 + (dk - 1) * rk]
    ev = np.array(ev)
    return (ev.sum() ** 2) / (ev ** 2).sum()

out = {"note": "growing-D sweep at fixed per-unit budget; sectors heterogeneous (d=2 and d=5 alternating); no d=1 sectors", "b": 0.55, "rows": []}
for m in (1, 2, 4, 8, 16, 32, 64):
    d = np.array(([2.0, 5.0] * m))
    Dtot = int(d.sum())
    row = {"m": m, "n_sectors": len(d), "D": Dtot, "keff": {}, "rho_range": {}}
    for rule in ("A_equal", "B_stock", "C_rate", "D_need"):
        sol = solve_ivp(rhs(rule, d, 0.55), [0, 4000], np.full(len(d), 0.3),
                        rtol=1e-10, atol=1e-12, method="LSODA")
        r = np.clip(sol.y[:, -1], 0, 1 - 1e-9)
        row["keff"][rule] = round(float(keff(d, r)), 3)
        row["rho_range"][rule] = [round(float(r.min()), 4), round(float(r.max()), 4)]
    out["rows"].append(row)
    print(f"D={Dtot:4d}: " + "  ".join(f"{ru}: keff={row['keff'][ru]:8.2f} rho=[{row['rho_range'][ru][0]:.3f},{row['rho_range'][ru][1]:.3f}]" for ru in row["keff"]))

with open("dsweep_keff_results.json", "w") as fh:
    json.dump(out, fh, indent=1)
print("wrote dsweep_keff_results.json")
