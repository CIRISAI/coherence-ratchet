"""
P_omega as an open-system steady state.
=======================================

The gate-1 P_omega program built P_omega as a projector on a CLOSED Hilbert
space (Models 1, 1', 1'') and hit a robust dead zone. But a corridor cannot
exist in a closed system -- closed unitary dynamics thermalizes. The framework's
own Piece 2, drho/dt = alpha - gammaM, is an OPEN dissipative equation, and the
gate-1 constructions never used it -- they used only Piece 1 (rho as operator)
and Piece 3 (the corridor band), statically.

This script builds P_omega the way Piece 2 says to: as the steady state of an
open-system (Lindblad) dynamics whose dissipator is gammaM.

Model. 3 rungs, 2 spins each (6 spins, dim 64). One density operator on the
whole space.
  H          : intra-rung Heisenberg (binds each rung) + cross-rung ZZ (Piece 6).
  alpha channel : per-rung collective decay -- drives rho_n -> 1 (rigidity).
                  Different rate per rung (0.6, 1.0, 1.5) so the rungs are not
                  symmetric and a simultaneous-corridor window is a real overlap.
  gammaM channel: per-spin independent bit-flip -- the maintenance term; injects
                  distinction, drives rho_n -> 0 (chaos). Rate gammaM is swept.
  rho_n      : |<Z_2n Z_2n+1>| in the steady state -- within-rung correlation.

P_omega, in this reading, IS the steady-state density operator rho_ss. The
"multi-rung corridor" question becomes: does the single steady state rho_ss
have every rung's rho_n in a corridor band simultaneously -- a property of one
well-defined object, not an intersection of subspaces that can be empty.

What this does and does not show. A Lindbladian steady state ALWAYS exists, so
the dead zone (empty intersection) structurally cannot recur -- that is the
point of the reframe, not a discovered result. The contentful question the
sweep answers is whether a gammaM regime puts all three rungs in a common
intermediate band. This is a toy. It does not validate the universal-scale
tier, and a forward dissipative steady state is in tension with the TSVF
backward-post-selection reading of P_omega -- noted, unresolved.
"""
import numpy as np

np.set_printoptions(precision=4, suppress=True, linewidth=100)

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
SM = np.array([[0, 0], [1, 0]], dtype=complex)        # sigma^- (lowering)

NSPIN = 6
DIM = 2 ** NSPIN


def kron_all(ops):
    out = ops[0]
    for o in ops[1:]:
        out = np.kron(out, o)
    return out


def site(op, i):
    ops = [I2] * NSPIN
    ops[i] = op
    return kron_all(ops)


SX = [site(X, i) for i in range(NSPIN)]
SY = [site(Y, i) for i in range(NSPIN)]
SZ = [site(Z, i) for i in range(NSPIN)]
SMi = [site(SM, i) for i in range(NSPIN)]
rungs = [(0, 1), (2, 3), (4, 5)]

# Hamiltonian: intra-rung Heisenberg binds each rung; cross-rung ZZ = Piece 6 tau
J, g = 1.0, 0.5
H = np.zeros((DIM, DIM), dtype=complex)
for (a, b) in rungs:
    H += J * (SX[a] @ SX[b] + SY[a] @ SY[b] + SZ[a] @ SZ[b])
for n in range(len(rungs) - 1):
    H += g * (SZ[rungs[n][1]] @ SZ[rungs[n + 1][0]])
H = (H + H.conj().T) / 2

# alpha (rigidity drift): per-rung collective decay, different rate per rung
GAMMA_ALPHA = [0.6, 1.0, 1.5]
alpha_jumps = [np.sqrt(rate) * (SMi[a] + SMi[b])
               for rate, (a, b) in zip(GAMMA_ALPHA, rungs)]
# gammaM (maintenance): per-spin bit-flip, rate factored out and swept
bf_ops = [SX[i] for i in range(NSPIN)]

Id = np.eye(DIM, dtype=complex)


def diss_term(L):
    """Row-major-vec Lindblad dissipator superoperator for one jump operator."""
    LdL = L.conj().T @ L
    return (np.kron(L, L.conj())
            - 0.5 * np.kron(LdL, Id) - 0.5 * np.kron(Id, LdL.T))


print("building Liouvillian ...")
# gammaM-independent piece
L0 = -1j * (np.kron(H, Id) - np.kron(Id, H.T))
for Lj in alpha_jumps:
    L0 += diss_term(Lj)
# bit-flip piece (rate factored out): sum_i diss(X_i)
Lbf = np.zeros((DIM * DIM, DIM * DIM), dtype=complex)
for Xi in bf_ops:
    Lbf += diss_term(Xi)

vecI = Id.reshape(-1)


def steady_state(gamma_M):
    """Steady state of L0 + gamma_M*Lbf via the trace-replacement linear solve."""
    M = (L0 + gamma_M * Lbf).copy()
    M[0, :] = vecI                          # one row -> the trace functional
    b = np.zeros(DIM * DIM, dtype=complex)
    b[0] = 1.0
    rho = np.linalg.solve(M, b).reshape(DIM, DIM)
    rho = (rho + rho.conj().T) / 2
    return rho / np.trace(rho).real


def rung_rho(rho):
    return [abs(np.trace(rho @ (SZ[a] @ SZ[b])).real) for (a, b) in rungs]


print("=" * 78)
print("P_omega as the steady state of an open-system (Lindblad) dynamics")
print("=" * 78)
print(f"  6 spins, 3 rungs, dim {DIM}; Liouvillian {DIM*DIM}x{DIM*DIM}")
print(f"  per-rung rigidity drift gamma_alpha = {GAMMA_ALPHA}")
print(f"  gamma_M = per-spin bit-flip (maintenance) rate, swept")
print()
print(f"  {'gamma_M':>8} {'rho_1':>8} {'rho_2':>8} {'rho_3':>8} "
      f"{'purity':>8} {'rank':>6}  {'rho_ss valid':>12}  {'all in band':>12}")

band = (0.10, 0.43)
gm_vals = [0.05, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0]
rows = []
for gm in gm_vals:
    rho = steady_state(gm)
    ev = np.linalg.eigvalsh(rho)
    valid = abs(np.trace(rho).real - 1) < 1e-6 and ev.min() > -1e-8
    purity = float(np.trace(rho @ rho).real)
    rank = int(np.sum(ev > 1e-6))
    rn = rung_rho(rho)
    allband = all(band[0] < r < band[1] for r in rn)
    rows.append((gm, rn, valid, allband))
    print(f"  {gm:>8.2f} {rn[0]:>8.3f} {rn[1]:>8.3f} {rn[2]:>8.3f} "
          f"{purity:>8.4f} {rank:>6d}  {str(valid):>12}  {str(allband):>12}")

print()
print("=" * 78)
print("READING  (exploratory)")
print("=" * 78)
print(f"  steady state rho_ss exists and is a valid density operator at every")
print(f"  gamma_M tested: {all(r[2] for r in rows)}. There is no intersection")
print(f"  to come up empty -- the closed-system dead zone cannot recur here.")
band_gm = [r[0] for r in rows if r[3]]
if band_gm:
    print(f"  gamma_M with ALL three rungs in (0.1, 0.43) simultaneously:")
    print(f"    {band_gm}  -- one steady state occupying the multi-rung corridor.")
else:
    print(f"  no single gamma_M in this sweep puts all three rungs in")
    print(f"  (0.1, 0.43) at once; rho_n still moves smoothly from rigidity")
    print(f"  (small gamma_M) toward chaos (large gamma_M). Common-band location")
    print(f"  is a substrate-calibration question, not an existence one.")
print()
print(f"  rho_ss is generically full rank -- the graded density operator the")
print(f"  soft-vs-hard debate was circling. P_omega as a projector dissolves:")
print(f"  the object is the steady state, and the corridor question is whether")
print(f"  that one state lands in band.")
print(f"  CAVEAT: a forward dissipative steady state is not a TSVF backward")
print(f"  post-selection. This reframes the corridor construction; it does not")
print(f"  by itself rescue the cosmological tier.")
