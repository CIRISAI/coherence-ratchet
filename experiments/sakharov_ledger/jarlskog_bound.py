"""Sakharov ledger, part (2a): is 'aligned book => T-symmetric book' a THEOREM?

The Jarlskog invariant obeys the algebraic identity
    J = c12 s12 c23 s23 c13^2 s13 sin(delta)
so |J| <= J_max(angles) = c12 s12 c23 s23 c13^2 s13, with the global ceiling
    J_max_global = max over ALL angles = 1/(6 sqrt 3) ~ 0.09623 (all mixing maximal).

Decompose the observed T-violation of each mixing book into
  - a STRUCTURAL factor  J_max(angles)/J_max_global  (forced by the mixing angles = alignment)
  - a CHOSEN factor      |sin delta|                 (the phase, a near-free choice)
so observed |J|/J_max_global = structural x chosen.

Then TEST the claim 'coordination structurally suppresses T-violation capacity' across the
Haar ensemble: correlate the coordination read (MI of |V|^2, and distance to nearest
permutation) against |J|. If high-coordination (near-permutation, high-MI) samples carry
systematically smaller |J|, the two-point CKM/PMNS statement is the tail of an ensemble law,
not a coincidence.

Discovery mode, exhaustive. Seed fixed. No pre-registration (this is a self-contained
algebraic/ensemble check, not a claim vs a known target).
"""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "jarlskog_bound.json")
rng = np.random.default_rng(20260710)
LN3 = np.log(3.0)
J_MAX_GLOBAL = 1.0 / (6.0 * np.sqrt(3.0))  # ~0.09623


def mixing_matrix(s12, s23, s13, delta):
    c12, c23, c13 = np.sqrt(1 - s12**2), np.sqrt(1 - s23**2), np.sqrt(1 - s13**2)
    e = np.exp(-1j * delta)
    return np.array([
        [c12 * c13, s12 * c13, s13 * e],
        [-s12 * c23 - c12 * s23 * s13 / e, c12 * c23 - s12 * s23 * s13 / e, s23 * c13],
        [s12 * s23 - c12 * c23 * s13 / e, -c12 * s23 - s12 * c23 * s13 / e, c23 * c13],
    ])


def jarlskog(V):
    return float(np.imag(V[0, 0] * V[1, 1] * np.conj(V[0, 1]) * np.conj(V[1, 0])))


def jmax_angles(s12, s23, s13):
    c12, c23, c13 = np.sqrt(1 - s12**2), np.sqrt(1 - s23**2), np.sqrt(1 - s13**2)
    return c12 * s12 * c23 * s23 * c13**2 * s13


def mi_of(V):
    M = np.abs(V) ** 2
    P = M / 3.0
    Psafe = np.clip(P, 1e-300, None)
    H = -np.sum(P * np.log(Psafe))
    return 2 * LN3 - H  # uniform marginals


PERMS = [np.eye(3)[list(p)] for p in
         [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]]


def d_perm_of(V):
    M = np.abs(V) ** 2
    return min(np.linalg.norm(M - Q) for Q in PERMS)


# ---- measured books ----
CASES = {
    "CKM":  dict(s12=0.22500, s23=0.04185, s13=0.00369, delta=1.144),
    "PMNS": dict(s12=np.sqrt(0.308), s23=np.sqrt(0.470), s13=np.sqrt(0.0220), delta=-1.98),
}

res = {"J_max_global": J_MAX_GLOBAL, "cases": {}}
for name, p in CASES.items():
    V = mixing_matrix(p["s12"], p["s23"], p["s13"], p["delta"])
    Jm = jmax_angles(p["s12"], p["s23"], p["s13"])
    Jobs = abs(jarlskog(V))
    sind = abs(np.sin(p["delta"]))
    structural = Jm / J_MAX_GLOBAL           # fraction of global ceiling the angles allow
    res["cases"][name] = dict(
        angles_deg=dict(th12=float(np.degrees(np.arcsin(p["s12"]))),
                        th23=float(np.degrees(np.arcsin(p["s23"]))),
                        th13=float(np.degrees(np.arcsin(p["s13"]))),
                        delta_deg=float(np.degrees(p["delta"]))),
        J_max_angles=float(Jm),
        J_observed=float(Jobs),
        sin_delta_abs=float(sind),
        structural_factor=float(structural),        # J_max(angles)/J_max_global
        chosen_factor=float(sind),                   # |sin delta|
        saturation_of_phase_ceiling=float(Jobs / Jm),  # = |sin delta|, sanity check
        MI=float(mi_of(V)),
        d_perm=float(d_perm_of(V)),
    )

# how much of the CKM/PMNS asymmetry in observed |J| is structural vs chosen?
c, l = res["cases"]["CKM"], res["cases"]["PMNS"]
res["asymmetry"] = dict(
    ratio_J_observed=float(l["J_observed"] / c["J_observed"]),
    ratio_structural=float(l["J_max_angles"] / c["J_max_angles"]),   # angle-driven part
    ratio_chosen=float(l["sin_delta_abs"] / c["sin_delta_abs"]),      # phase-driven part
)

# ---- Haar ensemble: does coordination suppress |J|? ----
N = 200_000
Z = (rng.standard_normal((N, 3, 3)) + 1j * rng.standard_normal((N, 3, 3))) / np.sqrt(2)
MI = np.empty(N); AJ = np.empty(N); DP = np.empty(N)
for i in range(N):
    Q, R = np.linalg.qr(Z[i])
    V = Q * (np.diagonal(R) / np.abs(np.diagonal(R)))
    MI[i] = mi_of(V); AJ[i] = abs(jarlskog(V)); DP[i] = d_perm_of(V)

# Spearman via rank correlation
def spearman(a, b):
    ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])

res["haar_ensemble"] = dict(
    n=N,
    spearman_MI_vs_absJ=spearman(MI, AJ),        # coordination vs T-violation capacity
    spearman_dperm_vs_absJ=spearman(DP, AJ),     # dist-to-permutation vs T-violation
    # mean |J| in top/bottom coordination deciles
    meanabsJ_top_MI_decile=float(np.mean(AJ[MI >= np.percentile(MI, 90)])),
    meanabsJ_bottom_MI_decile=float(np.mean(AJ[MI <= np.percentile(MI, 10)])),
    meanabsJ_near_permutation_decile=float(np.mean(AJ[DP <= np.percentile(DP, 10)])),
    meanabsJ_far_permutation_decile=float(np.mean(AJ[DP >= np.percentile(DP, 90)])),
    meanabsJ_all=float(np.mean(AJ)),
)

json.dump(res, open(OUT, "w"), indent=1)
print(json.dumps(res, indent=1))
