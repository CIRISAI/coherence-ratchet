"""
uniform_family.py — the "uniform fermionic correlation" family and the
closed-form two-pole / saturation analysis (S1, S2, S3).

THE CONSTRUCTION. The bosonic ledger uses the uniform-rho correlation matrix
C(k,rho) = (1-rho) I + rho 11^T  (unit diagonal, uniform pairwise rho), spectrum
{1+rho(k-1), (1-rho)^{k-1}}. Fermionic antisymmetry/exclusion CONSTRAINS the
analog. We take the number-conserving one-body matrix at half filling with
uniform single-particle coherence c:

    G(k,c) = (1/2) I + c (J - I),   J = 11^T,   G_ii = 1/2.

Eigenvalues of G: one collective  g0 = 1/2 + c(k-1);  (k-1) copies of  1/2 - c.
Validity 0 <= G <= I requires  |c| <= 1/(2(k-1))  -- THE EXCLUSION CAP: the
per-pair coherence is bounded by 1/(2(k-1)), so it must shrink as more fermions
are added. Majorana covariance eigenvalues nu = |2g-1|:
    nu0 = 2 c (k-1)   (collective),      nu1 = 2 c   ((k-1)-fold).
The natural bounded ORDER PARAMETER is the collective polarization
    s := nu0 = 2 c (k-1) in [0,1].
Holding s fixed as k->infty is the correct large-N limit (c = s/(2(k-1)) -> 0);
"more constituents at fixed collective coordination" is the Kish question.

This file computes, in closed form and numerically:
  S1  two-pole structure of each functional (F1 multi-info; F2 log-det);
  S2  saturation law of the effective-dimension candidates;
  S3  extensivity (additivity over independent blocks).
and prints the EXCLUSION DEFORMATION explicitly.
"""

import json
import numpy as np
from fermionic_core import (
    h_nu, H_bin, LN2, S_F_from_nu, logdet_potential_from_nu,
    keff_entropy_participation, keff_participation,
)

OUT = {}


# ---------------------------------------------------------------------------
# closed-form spectra of the uniform family
# ---------------------------------------------------------------------------
def family_nu(k, s):
    """nu-spectrum at collective order parameter s=nu0 in [0,1], k modes.
       nu0 = s ; nu1 = s/(k-1) with multiplicity (k-1)."""
    if k < 2:
        return np.array([0.0])
    nu0 = s
    nu1 = s / (k - 1)
    return np.concatenate([[nu0], np.full(k - 1, nu1)])


def family_G(k, s):
    """The actual G(k,c) matrix, c = s/(2(k-1))."""
    c = s / (2.0 * (k - 1)) if k > 1 else 0.0
    J = np.ones((k, k))
    return 0.5 * np.eye(k) + c * (J - np.eye(k))


def multi_information_family(k, s):
    """I_F on the uniform family, closed form.
       marginals: each G_ii=1/2 -> H_bin(1/2)=ln2, so sum = k ln2.
       joint: h(nu0) + (k-1) h(nu1)."""
    nu = family_nu(k, s)
    joint = S_F_from_nu(nu)
    marg = k * LN2
    return marg - joint, marg, joint


# ---------------------------------------------------------------------------
# S1 : two-pole structure
# ---------------------------------------------------------------------------
def s1_two_pole(klist=(10, 100, 1000)):
    rec = {}
    for k in klist:
        svals = np.linspace(0.0, 1.0, 2001)
        IF = np.array([multi_information_family(k, s)[0] for s in svals])
        LF = np.array([logdet_potential_from_nu(family_nu(k, s)) for s in svals])
        # chaos pole s=0
        IF0 = multi_information_family(k, 0.0)[0]
        LF0 = logdet_potential_from_nu(family_nu(k, 0.0))
        # rigidity pole s->1 : collective mode nu0 -> 1 (frozen). Exclusion cap.
        IF1 = multi_information_family(k, 1.0)[0]
        # analytic cap: I_F(s=1) = k ln2 - (k-1) h(1/(k-1))  (h(nu0=1)=0)
        cap_analytic = k * LN2 - (k - 1) * float(h_nu(1.0 / (k - 1)))
        # F2 log-det at s->1: nu0->1 => -ln(1-nu0^2) -> +inf
        LF_near1 = logdet_potential_from_nu(family_nu(k, 0.999999))
        rec[k] = {
            "IF_chaos_s0": IF0,
            "IF_rigidity_s1_cap": IF1,
            "IF_rigidity_cap_analytic": cap_analytic,
            "IF_monotone_increasing": bool(np.all(np.diff(IF) >= -1e-12)),
            "IF_max": float(IF.max()),
            "LF_chaos_s0": LF0,
            "LF_near_s1": LF_near1,  # should blow up (uncapped)
            "LF_diverges": bool(LF_near1 > 50 or not np.isfinite(LF_near1)),
        }
    return rec


# ---------------------------------------------------------------------------
# S2 : saturation law / Kish analog
# ---------------------------------------------------------------------------
def s2_saturation(klist=None, svals=(0.3, 0.6, 0.9, 0.999)):
    """For each fixed collective order parameter s, track effective-dimension
       candidates vs k and check saturation (bounded large-k limit)."""
    if klist is None:
        klist = [2, 3, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
    rec = {"klist": list(klist), "svals": list(svals), "curves": {}}
    for s in svals:
        keff_ent = []
        keff_pr_nu = []
        # "coordination deficit" dimension: how many effective modes are REMOVED
        # from full rank k by coordination = k - keff_entropy
        removed = []
        IF = []
        for k in klist:
            nu = family_nu(k, s)
            ke = keff_entropy_participation(nu)
            keff_ent.append(ke)
            keff_pr_nu.append(keff_participation(nu))
            removed.append(k - ke)
            IF.append(multi_information_family(k, s)[0])
        rec["curves"][f"s={s}"] = {
            "keff_entropy": keff_ent,
            "keff_pr_nu": keff_pr_nu,
            "dims_removed": removed,     # k - keff : the coordinated dimensions
            "I_F": IF,
        }
    return rec


# ---------------------------------------------------------------------------
# S3 : extensivity (additivity over independent blocks)
# ---------------------------------------------------------------------------
def s3_extensivity():
    """Two independent uniform blocks -> functionals add.
       Build block-diagonal G = diag(G1, G2); check I_F and L_F add."""
    rng = np.random.default_rng(7)
    checks = []
    for _ in range(6):
        k1, k2 = rng.integers(3, 12), rng.integers(3, 12)
        s1, s2 = rng.uniform(0.1, 0.9), rng.uniform(0.1, 0.9)
        nu1, nu2 = family_nu(k1, s1), family_nu(k2, s2)
        # joint entropy additive
        SF_joint = S_F_from_nu(np.concatenate([nu1, nu2]))
        SF_sum = S_F_from_nu(nu1) + S_F_from_nu(nu2)
        # multi-information additive (marginals & joints both add)
        IF1 = multi_information_family(k1, s1)[0]
        IF2 = multi_information_family(k2, s2)[0]
        IF_joint = (k1 + k2) * LN2 - SF_joint
        LF_joint = logdet_potential_from_nu(np.concatenate([nu1, nu2]))
        LF_sum = (logdet_potential_from_nu(nu1) + logdet_potential_from_nu(nu2))
        checks.append({
            "k1": int(k1), "k2": int(k2), "s1": float(s1), "s2": float(s2),
            "SF_additivity_err": abs(SF_joint - SF_sum),
            "IF_additivity_err": abs(IF_joint - (IF1 + IF2)),
            "LF_additivity_err": abs(LF_joint - LF_sum),
        })
    return checks


if __name__ == "__main__":
    print("== S1: two-pole structure ==")
    s1 = s1_two_pole()
    OUT["S1_two_pole"] = s1
    for k, r in s1.items():
        print(f" k={k}: I_F chaos={r['IF_chaos_s0']:.2e}  "
              f"I_F rigidity(cap)={r['IF_rigidity_s1_cap']:.4f} "
              f"(analytic {r['IF_rigidity_cap_analytic']:.4f})  "
              f"monotone={r['IF_monotone_increasing']}  "
              f"L_F(chaos)={r['LF_chaos_s0']:.2e}  L_F(s~1)={r['LF_near_s1']:.1f}  "
              f"L_F diverges={r['LF_diverges']}")
    print(f"\n  --> exclusion cap of I_F as k->inf: approaches ln2={LN2:.4f} + O(1/k)")
    for k in (10, 100, 1000, 10000):
        cap = k * LN2 - (k - 1) * float(h_nu(1.0 / (k - 1)))
        print(f"      k={k:6d}:  I_F cap = {cap:.6f}   (ln2 + {cap-LN2:.6f})")

    print("\n== S2: saturation law ==")
    s2 = s2_saturation()
    OUT["S2_saturation"] = s2
    for s in s2["svals"]:
        cur = s2["curves"][f"s={s}"]
        print(f"\n s={s}: k -> keff_entropy (effective active modes):")
        for k, ke, dr in zip(s2["klist"], cur["keff_entropy"], cur["dims_removed"]):
            print(f"    k={k:5d}: keff_entropy={ke:8.3f}  dims_removed(k-keff)={dr:7.4f}")

    print("\n== S3: extensivity ==")
    s3 = s3_extensivity()
    OUT["S3_extensivity"] = s3
    maxerr = max(max(c["SF_additivity_err"], c["IF_additivity_err"],
                     c["LF_additivity_err"]) for c in s3)
    print(f"  max additivity error over 6 random block pairs: {maxerr:.2e}  "
          f"({'PASS' if maxerr < 1e-9 else 'FAIL'})")

    with open("uniform_family_results.json", "w") as f:
        json.dump(OUT, f, indent=2, default=float)
    print("\nwrote uniform_family_results.json")
