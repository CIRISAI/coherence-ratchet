"""
Does the backward soft P_omega inherit the dead zone? (non-commuting rungs)
===========================================================================

backward_soft_pomega.py found, on a 2-rung COMMUTING toy, that the sharpened
F-11 does not cleanly fire -- but flagged two riders: (i) the framework-
referenced beta_pin = 1/2w^2 is large for a narrow corridor, so exp(-beta H) is
near a hard projector there; (ii) commuting rungs always admit a simultaneous-
corridor state, so that toy could not exhibit the dead zone.

This script runs the decisive case: NON-commuting nested rungs (the regime
where the hard-projector P_omega hit the dead zone -- construct_p_omega_*.py).

The mechanism. The backward soft operator is E_omega(beta) = exp(-beta * Hsum)
with Hsum = sum_n (rho_n - rho_c)^2. Its weight is governed by h_min, the
smallest eigenvalue of Hsum -- the least achievable total corridor penalty.
  - Commuting rungs: a state can sit at rho_c on every rung at once -> h_min ~ 0.
  - Non-commuting rungs: the rho_n cannot be co-minimised (an uncertainty-like
    frustration) -> h_min > 0, bounded away from 0.
At the framework-referenced beta_pin = 1/(2 w^2), the whole operator is
suppressed by ~exp(-beta_pin * h_min) = exp(-h_min / 2w^2). If h_min > 0, a
narrow corridor (small w) drives that to zero exponentially: the backward soft
P_omega becomes exponentially suppressed everywhere -- the dead zone in soft
form. That is the "empty/trivial" leg of the sharpened F-11.

Test: build 3 nested rungs two ways -- isotropic (commuting, control) and
anisotropic (non-commuting). Compute h_min for each. Sweep the corridor width;
report beta_pin * h_min and the soft suppression; cross-check against the
hard-projector intersection rank (the original dead-zone diagnostic).
"""
import numpy as np
import itertools

np.set_printoptions(precision=4, suppress=True, linewidth=100)

M = 8
DIM = 2 ** M
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def kron_all(ops):
    out = ops[0]
    for o in ops[1:]:
        out = np.kron(out, o)
    return out


def site(op, i):
    ops = [I2] * M
    ops[i] = op
    return kron_all(ops)


SX = [site(X, i) for i in range(M)]
SY = [site(Y, i) for i in range(M)]
SZ = [site(Z, i) for i in range(M)]
Idm = np.eye(DIM, dtype=complex)


def correlation(groups, coupling):
    """Average pairwise (anisotropic) correlation of group-collective spins,
    rescaled to [0,1]. coupling=(1,1,1) is isotropic SU(2)."""
    a, b, c = coupling
    def collective(g, P):
        return sum(P[i] for i in g) / len(g)
    gx = [collective(g, SX) for g in groups]
    gy = [collective(g, SY) for g in groups]
    gz = [collective(g, SZ) for g in groups]
    op = np.zeros((DIM, DIM), dtype=complex)
    pairs = list(itertools.combinations(range(len(groups)), 2))
    for (p, q) in pairs:
        op += a * gx[p] @ gx[q] + b * gy[p] @ gy[q] + c * gz[p] @ gz[q]
    op = op / len(pairs)
    op = (op + op.conj().T) / 2
    w = np.linalg.eigvalsh(op)
    return (op - w[0] * Idm) / (w[-1] - w[0])


# three RG-nested rungs on one 256-dim space
rung0 = [[i] for i in range(M)]
rung1 = [[2 * b, 2 * b + 1] for b in range(M // 2)]
rung2 = [list(range(0, M // 2)), list(range(M // 2, M))]
rungs = [rung0, rung1, rung2]

RHO_C = 0.5


def build(couplings, label):
    rho = [correlation(rungs[n], couplings[n]) for n in range(3)]
    cmax = max(np.abs(rho[a] @ rho[b] - rho[b] @ rho[a]).max()
               for a in range(3) for b in range(a + 1, 3))
    Hsum = sum((r - RHO_C * Idm) @ (r - RHO_C * Idm) for r in rho)
    Hsum = (Hsum + Hsum.conj().T) / 2
    hval = np.linalg.eigvalsh(Hsum)
    print(f"  {label}: max ||[rho_a,rho_b]|| = {cmax:.2e}  "
          f"({'commuting' if cmax < 1e-9 else 'NON-commuting'});  "
          f"h_min(Hsum) = {hval[0]:.4f}")
    return rho, hval


def hard_intersection_rank(rho, lo, hi):
    """Rank of the simultaneous-corridor projector (the original dead-zone
    diagnostic): eigenvalue-1 space of the averaged band projector."""
    projs = []
    for r in rho:
        w, V = np.linalg.eigh(r)
        Vb = V[:, (w >= lo) & (w <= hi)]
        projs.append(Vb @ Vb.conj().T)
    avg = sum(projs) / len(projs)
    wa, _ = np.linalg.eigh(avg)
    return int(np.sum(wa > 1 - 1e-9))


print("=" * 78)
print("STEP 1 -- three nested rungs, commuting (control) and non-commuting")
print("=" * 78)
rho_iso, hval_iso = build([(1.0, 1.0, 1.0)] * 3, "isotropic  ")
aniso = [(0.7, 1.3, 0.5), (1.2, 0.6, 1.1), (0.9, 1.4, 0.8)]
rho_ani, hval_ani = build(aniso, "anisotropic")

print()
print("=" * 78)
print("STEP 2 -- soft suppression vs hard dead zone, across corridor width w")
print("=" * 78)
print(f"  band centred at rho_c = {RHO_C}; beta_pin = 1/(2 w^2).")
print(f"  soft weight of the best state = exp(-beta_pin * h_min).")
print()
print(f"  {'w':>6} {'beta_pin':>9} | "
      f"{'iso h_min':>9} {'iso supp.':>11} {'iso hardrank':>13} | "
      f"{'ani h_min':>9} {'ani supp.':>11} {'ani hardrank':>13}")
for w in [0.40, 0.30, 0.20, 0.15, 0.10, 0.05]:
    beta_pin = 1.0 / (2.0 * w * w)
    lo, hi = RHO_C - w, RHO_C + w
    supp_iso = np.exp(-beta_pin * hval_iso[0])
    supp_ani = np.exp(-beta_pin * hval_ani[0])
    rk_iso = hard_intersection_rank(rho_iso, lo, hi)
    rk_ani = hard_intersection_rank(rho_ani, lo, hi)
    print(f"  {w:>6.2f} {beta_pin:>9.1f} | "
          f"{hval_iso[0]:>9.4f} {supp_iso:>11.2e} {rk_iso:>13d} | "
          f"{hval_ani[0]:>9.4f} {supp_ani:>11.2e} {rk_ani:>13d}")

print()
print("=" * 78)
print("READING  (the data contradicts the pre-run expectation)")
print("=" * 78)
print(f"  h_min(Hsum): isotropic {hval_iso[0]:.4f}, anisotropic {hval_ani[0]:.4f}")
print(f"  -- both SMALL. (Honest caveat: the control is confounded -- isotropic")
print(f"  is commuting AND coarse-spectrum, anisotropic is non-commuting AND")
print(f"  rich-spectrum. The toy cannot isolate non-commutativity alone.)")
print()
print(f"  KEY FINDING -- the soft operator does NOT inherit the dead zone.")
print(f"  The hard-projector intersection rank collapses to 0 for narrow bands")
print(f"  (the original dead zone). At the SAME bands the soft operator at")
print(f"  beta_pin keeps order-1 weight (anisotropic: ~0.9 at w=0.15, ~0.7 at")
print(f"  w=0.10, 0.26 at w=0.05). Hard-empty and soft-suppressed do NOT track.")
print()
print(f"  Why: the hard projector demands every rung STRICTLY band-supported")
print(f"  (zero amplitude outside the band). The soft operator scores total")
print(f"  penalty sum_n <(rho_n - rho_c)^2> = sum_n [(mean - rho_c)^2 + var].")
print(f"  A state near-corridor at every rung but with small tails outside the")
print(f"  band is rejected by the hard projector and barely penalised by the")
print(f"  soft one. The dead zone was an artifact of the hard construction's")
print(f"  tail-intolerance; the soft operator escapes it.")
print()
print(f"  VERDICT: the sharpened F-11 does NOT fire at <= 3 non-commuting rungs.")
print(f"  The backward soft P_omega escapes the hard dead zone -- the opposite")
print(f"  of the pre-run expectation that it would inherit it.")
print(f"  CAVEAT: h_min is a sum over rungs and should grow with rung count;")
print(f"  3 rungs gives h_min ~ 0.007-0.03. Whether 6-9 rungs re-triggers soft")
print(f"  suppression is untested -- linear growth keeps it alive, compounding")
print(f"  frustration eventually would not.")
