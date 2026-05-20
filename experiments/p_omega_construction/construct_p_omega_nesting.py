"""
P_omega under cross-rung non-factorization (residual (a) of F-11).
==================================================================

The factorizing construction (construct_p_omega.py) assumed each rung is a
distinct tensor factor, so the rho_n commute and P_omega = product of P_n.
The framework's real rungs NEST: rung n+1 is built from coarse-grainings of
rung n. Then rho_n and rho_{n+1} are fine- vs coarse-grained observables on
the SAME Hilbert space, and generically do not commute.

This script builds a nesting toy and constructs P_omega for it.

THE NESTING MODEL
-----------------
One Hilbert space: M = 8 spin-1/2 constituents (dim 256). Three RG-style rungs
on the same space:
  rung 0 -- the 8 individual spins; rho_0 = avg pairwise correlation.
  rung 1 -- 4 blocks of 2 spins; rho_1 = avg correlation of block-collective
            spin variables.
  rung 2 -- 2 blocks of 4 spins; rho_2 = correlation of the two half-block
            collective spin variables.
rho_0, rho_1, rho_2 are self-adjoint operators on the same 256-dim space.
They are fine/medium/coarse-grained, so they generically do not commute.

THE CONSTRUCTION
----------------
Per rung: P_n = spectral projection of rho_n onto the corridor -- the OPEN
interior of its spectrum, excluding the bottom eigenvalue (chaos pole) and
top eigenvalue (rigidity pole).

P_omega = projector onto the intersection of the three corridor subspaces.
Because the P_n do not commute, P_omega is NOT the simple product. It is
constructed two independent ways and cross-checked:
  (1) von Neumann / Halperin alternating projections:
      P_omega = lim_k (P_0 P_1 P_2)^k.
  (2) the eigenvalue-1 eigenspace of (P_0 + P_1 + P_2)/3 -- a vector lies in
      all three ranges iff the averaged projector fixes it.

THE DEBATABLE NUMBER
--------------------
dim(P_omega) = the dimension of the simultaneous-corridor-at-every-rung
subspace under genuine nesting. Large => corridor-everywhere is easy to
satisfy. Tiny or zero => corridor-everywhere is a fine-tuned / rare
condition, in tension with the asymptotic-conditioning theorem's "-> 1".
"""
import numpy as np
import itertools

np.set_printoptions(precision=4, suppress=True, linewidth=100)

M = 8                       # spin-1/2 constituents
dim = 2 ** M                # 256

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def kron_all(ops):
    out = ops[0]
    for o in ops[1:]:
        out = np.kron(out, o)
    return out


def S(op, site):
    """Single-spin Pauli operator at `site`, on the full M-spin space."""
    ops = [I2] * M
    ops[site] = op
    return kron_all(ops)


# precompute single-site operators
SX = [S(X, i) for i in range(M)]
SY = [S(Y, i) for i in range(M)]
SZ = [S(Z, i) for i in range(M)]


def correlation(groups):
    """Average pairwise Heisenberg correlation between collective-spin
    variables. `groups` is a list of lists of site indices; the collective
    spin of a group is the mean of its members' Pauli vectors."""
    def collective(g, P):
        return sum(P[i] for i in g) / len(g)
    gx = [collective(g, SX) for g in groups]
    gy = [collective(g, SY) for g in groups]
    gz = [collective(g, SZ) for g in groups]
    op = np.zeros((dim, dim), dtype=complex)
    pairs = list(itertools.combinations(range(len(groups)), 2))
    for (a, b) in pairs:
        op += gx[a] @ gx[b] + gy[a] @ gy[b] + gz[a] @ gz[b]
    return op / len(pairs)


# --- the three nested rungs, all on the same 256-dim space ---
rung0 = [[i] for i in range(M)]                       # 8 individual spins
rung1 = [[2 * b, 2 * b + 1] for b in range(M // 2)]   # 4 blocks of 2
rung2 = [list(range(0, M // 2)), list(range(M // 2, M))]  # 2 blocks of 4

rho = [correlation(rung0), correlation(rung1), correlation(rung2)]
labels = ["rung 0 (8 spins)", "rung 1 (4 blocks)", "rung 2 (2 blocks)"]

print("=" * 72)
print("STEP 1 -- three nested rho_n operators on one 256-dim Hilbert space")
print("=" * 72)
P = []
for n, (r, lab) in enumerate(zip(rho, labels)):
    assert np.allclose(r, r.conj().T), f"rho_{n} not self-adjoint"
    w, V = np.linalg.eigh(r)
    spec = sorted(set(np.round(w, 6)))
    lo, hi = spec[0], spec[-1]
    interior = (w > lo + 1e-9) & (w < hi - 1e-9)   # corridor = open interior
    Vb = V[:, interior]
    Pn = Vb @ Vb.conj().T
    P.append(Pn)
    print(f"  {lab}: spectrum {spec}")
    print(f"    chaos pole rho={lo:+.4f}, rigidity pole rho={hi:+.4f}, "
          f"corridor rank(P_{n})={int(round(np.trace(Pn).real))}")

# --- do the rungs commute? ---
print()
print("=" * 72)
print("STEP 2 -- non-commutation check")
print("=" * 72)
for a in range(3):
    for b in range(a + 1, 3):
        c = np.abs(P[a] @ P[b] - P[b] @ P[a]).max()
        print(f"  ||[P_{a}, P_{b}]|| = {c:.4e}   "
              f"({'commute' if c < 1e-9 else 'DO NOT commute'})")

# --- P_omega construction (1): von Neumann / Halperin alternating projections
print()
print("=" * 72)
print("STEP 3 -- P_omega via alternating projections  lim (P0 P1 P2)^k")
print("=" * 72)
Mprod = P[0] @ P[1] @ P[2]
A = Mprod.copy()
prev = A.copy()
for k in range(2, 4001):
    A = A @ Mprod
    delta = np.abs(A - prev).max()
    prev = A.copy()
    if delta < 1e-12:
        print(f"  converged at k={k}, ||A_k - A_(k-1)|| = {delta:.2e}")
        break
else:
    print(f"  did not converge to 1e-12 within k=4000; last delta {delta:.2e}")
P_omega_ap = (A + A.conj().T) / 2     # symmetrize tiny numerical asymmetry
rank_ap = int(round(np.trace(P_omega_ap).real))
idem_ap = np.abs(P_omega_ap @ P_omega_ap - P_omega_ap).max()
print(f"  limit: rank {rank_ap}, ||L^2 - L|| = {idem_ap:.2e}, "
      f"self-adjoint resid {np.abs(A - A.conj().T).max():.2e}")

# --- P_omega construction (2): eigenvalue-1 space of the averaged projector
print()
print("=" * 72)
print("STEP 4 -- P_omega via eigenvalue-1 space of (P0+P1+P2)/3  [independent]")
print("=" * 72)
avg = (P[0] + P[1] + P[2]) / 3
wa, Va = np.linalg.eigh(avg)
one_space = wa > 1 - 1e-9
Vone = Va[:, one_space]
P_omega_ev = Vone @ Vone.conj().T
rank_ev = int(round(np.trace(P_omega_ev).real))
print(f"  intersection dimension (eigenvalue-1 multiplicity) = {rank_ev}")

# --- cross-check the two constructions ---
print()
print("=" * 72)
print("STEP 5 -- cross-check + the debatable number")
print("=" * 72)
match = np.abs(P_omega_ap - P_omega_ev).max()
print(f"  ||P_omega(alt-proj) - P_omega(eigenspace)|| = {match:.2e}   "
      f"({'AGREE' if match < 1e-6 else 'DISAGREE'})")

P_omega = P_omega_ev
rank = rank_ev
indep_ranks = [int(round(np.trace(p).real)) for p in P]
naive_product = np.prod([r / dim for r in indep_ranks]) * dim
print(f"  per-rung corridor ranks: {indep_ranks}  (of dim {dim})")
print(f"  if rungs were independent, expected ~ {naive_product:.1f}")
print(f"  ACTUAL dim(P_omega) [simultaneous corridor, all rungs] = {rank}")
frac = rank / dim
print(f"  simultaneous-corridor subspace is {rank}/{dim} = {frac:.4%} of "
      f"the Hilbert space")

# --- TSVF post-selection with the non-commuting P_omega ---
print()
print("=" * 72)
print("STEP 6 -- P_omega as TSVF post-selector (non-commuting rungs)")
print("=" * 72)
if rank == 0:
    print("  dim(P_omega) = 0: the simultaneous-corridor subspace is EMPTY.")
    print("  No corridor configuration satisfies all three rungs at once in")
    print("  this nesting toy. P_omega is the zero operator; TSVF post-")
    print("  selection through it annihilates every state.")
else:
    rng = np.random.default_rng(20260520)
    psi_corr = P_omega @ (rng.standard_normal(dim) + 1j * rng.standard_normal(dim))
    psi_corr /= np.linalg.norm(psi_corr)
    psi_anti = (np.eye(dim) - P_omega) @ (rng.standard_normal(dim)
                                          + 1j * rng.standard_normal(dim))
    psi_anti /= np.linalg.norm(psi_anti)
    print(f"  post-selection prob ||P_omega|psi>||^2 :")
    print(f"    corridor state        : {np.linalg.norm(P_omega@psi_corr)**2:.4f}")
    print(f"    corridor-orthogonal   : {np.linalg.norm(P_omega@psi_anti)**2:.4e}")

print()
print("=" * 72)
print("RESULT")
print("=" * 72)
print(f"  Under genuine cross-rung nesting the P_n do not commute, yet")
print(f"  P_omega is still constructible: alternating projections and the")
print(f"  averaged-projector eigenspace agree to {match:.0e}.")
print(f"  The simultaneous-corridor subspace has dimension {rank} "
      f"({frac:.3%} of {dim}).")
print(f"  Residual (a) of F-11 is addressed: non-commuting rungs do not")
print(f"  block the construction. The debatable result is the SIZE of the")
print(f"  intersection and what it implies for asymptotic conditioning.")
