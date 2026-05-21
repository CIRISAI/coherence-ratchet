"""
pp_cp — the corridor shape observable on CP-violation structure across decay modes.
=====================================================================================

Candidate: per parent particle, the set of measured CP asymmetries A_CP across
its decay modes. Honest prior: NULL (E4 found particle decay-channel branching
fractions show no tight corridor band). See PREREGISTRATION.md, committed before
this script's results.

Construction problem: A_CP can be NEGATIVE and the values are not a probability
distribution, so k_eff = 1/Σpᵢ² does not apply directly. PRE-REGISTERED repair
(PRIMARY): take magnitudes aᵢ=|A_CP,i|, form power weights wᵢ=aᵢ², normalise to
a simplex pᵢ=wᵢ/Σwⱼ, then k_eff and ρ measure how CONCENTRATED CP violation is
among modes vs how spread.

Confound control (inherited from E4): A_CP measurement counts vary wildly across
parents (B+ ~166, B0 ~64, D0 ~103, D+ ~31) and k_eff inflates with N, so the
PRIMARY analysis fixes N_FIX = 12 top-|A_CP| modes per parent — a completeness-
independent concentration measure. An all-modes ρ is reported for transparency
only and is NOT the corridor test.

Corridor bar (pre-registered): per-parent ρ cluster in a TIGHT band width ≤ 0.18,
inside the A3+ reference corridor ρ ∈ [0.17,0.35], with ≥ 3/4 parents in band.
A wide window is not a corridor.

Data: PDG 2025, `pdg` package v0.2.2. Real data only.
"""
import numpy as np
import pdg

api = pdg.connect()

N_FIX = 12                       # pre-registered fixed channel count
CORR_LO, CORR_HI = 0.17, 0.35    # A3+ reference corridor
BAND_WIDTH_MAX = 0.18            # pre-registered tight-band width ceiling
PARENTS = ["B+", "B0", "D0", "D+"]   # name-resolvable parents with A_CP data


def kish(p):
    p = np.asarray(p, float)
    p = p / p.sum()
    N = len(p)
    k_eff = 1.0 / np.sum(p ** 2)
    rho = (N / k_eff - 1.0) / (N - 1.0)
    return k_eff, rho


def acp_magnitudes(name):
    """All measured (non-limit) |A_CP| for a parent particle, descending."""
    p = api.get_particle_by_name(name)
    vals = []
    for pr in p.properties():
        desc = getattr(pr, "description", "") or ""
        if not desc.startswith("A(CP)"):
            continue
        try:
            s = pr.best_summary()
        except Exception:
            continue
        if s is None:
            continue
        if getattr(s, "is_limit", False):
            continue
        v = getattr(s, "value", None)
        if v is None:
            continue
        a = abs(float(v))
        if a > 0:
            vals.append(a)
    return sorted(vals, reverse=True)


print("=" * 78)
print(f"pp_cp — CP-asymmetry corridor test  (PRIMARY: fixed N_FIX = {N_FIX})")
print("=" * 78)
print(f"  {'parent':<8}{'N_all':>7}{'k_eff':>9}{'rho':>9}{'topfrac':>10}"
      f"   regime")

rows = []
for name in PARENTS:
    mags = acp_magnitudes(name)
    if len(mags) < N_FIX:
        print(f"  {name:<8} only {len(mags)} clean A_CP modes < N_FIX -- dropped")
        continue
    top = np.array(mags[:N_FIX])
    w = top ** 2                                  # CP-violation power weights
    k_eff, rho = kish(w)
    topfrac = w[0] / w.sum()                      # secondary descriptive stat
    regime = ("rigidity" if rho > 0.55 else
              "chaos" if rho < 0.12 else "interior")
    rows.append((name, len(mags), k_eff, rho, topfrac, regime))
    print(f"  {name:<8}{len(mags):>7}{k_eff:>9.2f}{rho:>9.3f}{topfrac:>10.3f}"
          f"   {regime}")

print()
print("  Secondary (transparency only, NOT the corridor test): all-modes rho")
for name in PARENTS:
    mags = acp_magnitudes(name)
    if len(mags) < 3:
        continue
    w = np.array(mags) ** 2
    k_eff, rho = kish(w)
    print(f"  {name:<8} N={len(mags):>4}  k_eff={k_eff:>7.2f}  rho_all={rho:.3f}")

print()
print("=" * 78)
print("VERDICT  (pre-registered bar, read off the numbers above)")
print("=" * 78)

if len(rows) < 2:
    print("  CONSTRUCTION / DATA FAILURE: fewer than 2 parents yield N_FIX clean")
    print("  A_CP modes. The shape observable cannot be tested here.")
else:
    rho_vals = np.array([r[3] for r in rows])
    lo, hi = rho_vals.min(), rho_vals.max()
    width = hi - lo
    n_in_ref = int(np.sum((rho_vals >= CORR_LO) & (rho_vals <= CORR_HI)))
    n_rig = int(np.sum(rho_vals > 0.55))
    n_chaos = int(np.sum(rho_vals < 0.12))
    frac_req = max(3, int(np.ceil(0.75 * len(rows))))
    print(f"  parents tested: {len(rows)}  "
          f"({', '.join(r[0] for r in rows)})")
    print(f"  rho values: {np.round(rho_vals,3).tolist()}")
    print(f"  range [{lo:.3f}, {hi:.3f}]  width {width:.3f}  "
          f"(tight-band ceiling {BAND_WIDTH_MAX})")
    print(f"  in A3+ reference corridor [{CORR_LO},{CORR_HI}]: "
          f"{n_in_ref}/{len(rows)}  (need >= {frac_req})")
    print(f"  pole pile-up: rigidity {n_rig}, chaos {n_chaos}")
    print()

    tight = width <= BAND_WIDTH_MAX
    in_ref = n_in_ref >= frac_req
    if n_rig >= frac_req or n_chaos >= frac_req:
        print("  NULL -- POLE PILE-UP. CP-violation power concentration piles at a")
        print("  pole. No corridor band.")
    elif tight and in_ref:
        print("  CORRIDOR. The pre-registered bar is cleared: rho clusters in a")
        print("  tight band inside the A3+ reference corridor. (Caveat from")
        print("  PREREGISTRATION section 0: A_CP across modes is NOT a coordinated")
        print("  rung; even this hit is a descriptive coincidence, not framework")
        print("  support.)")
    else:
        print("  NULL -- BROAD SPREAD. The shape observable produces a number per")
        print("  parent but the rho values do not form a tight band meeting the")
        print("  pre-registered corridor bar. CP asymmetries across decay modes")
        print("  are not the kind of object the corridor observable detects -- ")
        print("  consistent with the honest prior and with E4's decay-BF null.")
