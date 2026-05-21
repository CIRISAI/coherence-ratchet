"""
Is the backward generator L~^dag = L^dag + D_omega a legitimate Lindbladian?
============================================================================

The bridge run (backward_pomega_dynamics_bridge.py) showed the modification
D_omega that makes E_omega a fixed point of the backward adjoint is NAMED (the
corridor-penalty current L^dag[H_sum]) and SIZED (~2-30% of ||L||). It left one
question open: is L~^dag = L^dag + D_omega itself the adjoint of a legitimate
(completely-positive, trace-preserving) generator? If the modification cannot
be a real Lindbladian, "modified L^dag" is a formal patch, not a dynamics.

A superoperator L generates a CPTP semigroup iff it is (1) Hermiticity-
preserving, (2) trace-preserving, and (3) conditionally completely positive:
the Choi matrix projected off the maximally entangled state is positive
semidefinite (the Gorini-Kossakowski-Sudarshan-Lindblad criterion).

Three tests:
  1. The forward corridor Lindbladian L -- sanity check it passes (it must).
  2. L~ = L + D_omega^dag with the MINIMAL (Hilbert-Schmidt-minimal) D_omega.
     The minimal modification is a raw patch, not built to respect any of the
     three conditions -- expected to fail.
  3. Does a LEGITIMATE backward generator that fixes E_omega exist at all?
     Yes, constructively: pure dephasing in the H_sum eigenbasis. Its single
     Hermitian jump operator is H_sum itself; D_deph^dag[f(H_sum)] = 0 for
     every function f, so it conserves E_omega = exp(-beta H_sum) exactly --
     and a single-jump-operator Lindbladian is manifestly GKSL.

The gap between test 2 and test 3 is the result: a legitimate backward
generator fixing E_omega exists, but it is a structurally distinct dynamics
(non-ergodic, H_sum-conserving) -- not the forward corridor dynamics plus a
small perturbation. Measured by the steady-state degeneracy: forward L is
ergodic (one steady state), the backward generator is non-ergodic (many).
"""
import numpy as np
from scipy.linalg import expm

np.set_printoptions(precision=4, suppress=True, linewidth=100)

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
SM = np.array([[0, 0], [1, 0]], dtype=complex)

NSPIN = 6
DIM = 2 ** NSPIN
RHO_C = 0.5


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
Id = np.eye(DIM, dtype=complex)


def hermit(A):
    return (A + A.conj().T) / 2


# corridor Lindbladian (identical to backward_pomega_dynamics_bridge.py)
J, g = 1.0, 0.5
H = np.zeros((DIM, DIM), dtype=complex)
for (a, b) in rungs:
    H += J * (SX[a] @ SX[b] + SY[a] @ SY[b] + SZ[a] @ SZ[b])
for n in range(len(rungs) - 1):
    H += g * (SZ[rungs[n][1]] @ SZ[rungs[n + 1][0]])
H = hermit(H)

COUP = [(0.7, 1.3, 0.5), (1.2, 0.6, 1.1), (0.9, 1.4, 0.8)]


def rung_corr(a, b, coup):
    cx, cy, cz = coup
    O = cx * SX[a] @ SX[b] + cy * SY[a] @ SY[b] + cz * SZ[a] @ SZ[b]
    O = hermit(O)
    w = np.linalg.eigvalsh(O)
    return (O - w[0] * Id) / (w[-1] - w[0])


O = [rung_corr(a, b, c) for (a, b), c in zip(rungs, COUP)]
Hsum = hermit(sum((On - RHO_C * Id) @ (On - RHO_C * Id) for On in O))

GAMMA_ALPHA = [0.6, 1.0, 1.5]
alpha_jumps = [np.sqrt(rate) * (SMi[a] + SMi[b])
               for rate, (a, b) in zip(GAMMA_ALPHA, rungs)]
bf_ops = [SX[i] for i in range(NSPIN)]


def diss_term(L):
    """Schrodinger-picture Lindblad dissipator for one jump operator (vec)."""
    LdL = L.conj().T @ L
    return (np.kron(L, L.conj())
            - 0.5 * np.kron(LdL, Id) - 0.5 * np.kron(Id, LdL.T))


Lham = -1j * (np.kron(H, Id) - np.kron(Id, H.T))
GM = 0.10
Lsuper = (Lham + sum(diss_term(Lj) for Lj in alpha_jumps)
          + GM * sum(diss_term(Xi) for Xi in bf_ops))
vecI = Id.reshape(-1)


def apply_super(S, A):
    return (S @ A.reshape(-1)).reshape(DIM, DIM)


def fro(A):
    return float(np.linalg.norm(A))


# --- legitimacy diagnostics --------------------------------------------------
Omega = np.zeros(DIM * DIM, dtype=complex)            # |Omega> = sum_i |ii>
for i in range(DIM):
    Omega[i * DIM + i] = 1.0
Pproj = np.eye(DIM * DIM, dtype=complex) - np.outer(Omega, Omega.conj()) / DIM


def choi(G):
    """Choi matrix C[(i,k),(j,l)] = (G[|i><j|])[k,l] for row-major-vec G."""
    T = G.reshape(DIM, DIM, DIM, DIM)               # [k,l,i,j]
    return T.transpose(2, 0, 3, 1).reshape(DIM * DIM, DIM * DIM)


def legitimacy(G, label):
    """Return (herm-pres viol, trace-pres viol, CCP min-eig); print verdict."""
    C = choi(G)
    herm = fro(C - C.conj().T) / max(fro(C), 1e-30)
    trace = fro(vecI.conj() @ G) / max(fro(G), 1e-30)
    PCP = Pproj @ hermit(C) @ Pproj
    mineig = float(np.linalg.eigvalsh(PCP)[0])
    tol = 1e-8 * fro(C)
    ok = herm < 1e-9 and trace < 1e-9 and mineig > -tol
    print(f"  {label}")
    print(f"    Hermiticity-preserving : viol {herm:.2e}   "
          f"{'OK' if herm < 1e-9 else 'FAIL'}")
    print(f"    trace-preserving       : viol {trace:.2e}   "
          f"{'OK' if trace < 1e-9 else 'FAIL'}")
    print(f"    conditionally CP       : min eig {mineig:+.3e}   "
          f"{'OK' if mineig > -tol else 'FAIL'}")
    print(f"    --> {'LEGITIMATE generator' if ok else 'NOT a legitimate generator'}")
    return ok


print("=" * 80)
print("Legitimacy of the modified backward generator")
print("=" * 80)
print(f"  dim {DIM}; corridor Lindbladian, gammaM = {GM}")

# ---------------------------------------------------------------------------
# TEST 1 -- the forward corridor Lindbladian L (must pass)
# ---------------------------------------------------------------------------
print()
print("-" * 80)
print("TEST 1 -- forward corridor Lindbladian L (sanity check)")
print("-" * 80)
legitimacy(Lsuper, "L (forward)")

# ---------------------------------------------------------------------------
# TEST 2 -- L~ = L + D_omega^dag with the minimal D_omega
# ---------------------------------------------------------------------------
print()
print("-" * 80)
print("TEST 2 -- L~ = L + D_omega^dag, minimal (HS-minimal) D_omega")
print("-" * 80)
Ladj = Lsuper.conj().T
beta_pin = 22.2                                       # 1/(2 w^2), w = 0.15
Eom = expm(-beta_pin * Hsum)
LdE = apply_super(Ladj, Eom)
vEom = Eom.reshape(-1)
# minimal modification of the adjoint:  D_omega[X] = -L^dag[E] <E,X>/||E||^2
Domega = -np.outer(LdE.reshape(-1), vEom.conj()) / float(np.vdot(vEom, vEom).real)
Ltil_adj = Ladj + Domega
print(f"  beta = beta_pin(w=0.15) = {beta_pin};  "
      f"L~^dag[E_omega] residual = {fro(apply_super(Ltil_adj, Eom)):.2e} "
      f"(zero by construction)")
Ltil = Lsuper + Domega.conj().T                       # Schrodinger-picture L~
legitimacy(Ltil, "L~ (forward + minimal D_omega^dag)")
print("  the minimal modification is a raw Hilbert-Schmidt patch -- it is not")
print("  built to respect trace-preservation or complete positivity.")

# ---------------------------------------------------------------------------
# TEST 3 -- a legitimate backward generator that fixes E_omega: H_sum dephasing
# ---------------------------------------------------------------------------
print()
print("-" * 80)
print("TEST 3 -- legitimate backward generator: pure dephasing in H_sum basis")
print("-" * 80)
Lback = diss_term(Hsum)                               # single Hermitian jump op
Lback_adj = Lback.conj().T
# does it conserve E_omega and every other function of H_sum?
res_E = fro(apply_super(Lback_adj, Eom)) / fro(Eom)
res_Hs = fro(apply_super(Lback_adj, Hsum)) / fro(Hsum)
rngp = np.random.default_rng(0)
Rrand = hermit(rngp.standard_normal((DIM, DIM)) + 1j * rngp.standard_normal((DIM, DIM)))
res_rand = fro(apply_super(Lback_adj, Rrand)) / fro(Rrand)
print(f"  L_back^dag[E_omega] / ||E_omega||      = {res_E:.2e}  (conserved)")
print(f"  L_back^dag[H_sum]   / ||H_sum||        = {res_Hs:.2e}  (conserved)")
print(f"  L_back^dag[random Hermitian] / ||.||   = {res_rand:.2e}  (not conserved)")
print(f"  -> L_back conserves exactly the functions of H_sum, E_omega among them.")
legitimacy(Lback, "L_back (H_sum dephasing)")

# ---------------------------------------------------------------------------
# TEST 4 -- the gap: forward L is ergodic, L_back is not
# ---------------------------------------------------------------------------
print()
print("-" * 80)
print("TEST 4 -- ergodicity gap (steady-state degeneracy)")
print("-" * 80)
ev_L = np.linalg.eigvals(Lsuper)
ev_B = np.linalg.eigvals(Lback)
tol = 1e-7
deg_L = int(np.sum(np.abs(ev_L) < tol))
deg_B = int(np.sum(np.abs(ev_B) < tol))
hs_eigs = np.linalg.eigvalsh(Hsum)
n_distinct = len(np.unique(np.round(hs_eigs, 6)))
print(f"  forward L  : {deg_L} zero mode(s)  -> "
      f"{'ergodic (unique steady state)' if deg_L == 1 else 'non-ergodic'}")
print(f"  L_back     : {deg_B} zero modes    -> non-ergodic; conserves every")
print(f"               operator diagonal in the H_sum eigenbasis "
      f"({n_distinct} distinct H_sum levels)")

# ---------------------------------------------------------------------------
# SYNTHESIS
# ---------------------------------------------------------------------------
print()
print("=" * 80)
print("SYNTHESIS -- path item (iii)")
print("=" * 80)
print("  The minimal D_omega is NOT a legitimate generator modification: it")
print("  breaks trace-preservation (and complete positivity). It sizes the gap,")
print("  it is not itself a dynamics.")
print()
print("  BUT a legitimate backward generator that fixes E_omega DOES exist --")
print("  pure dephasing in the H_sum eigenbasis. It is a proper Lindbladian")
print("  (single Hermitian jump operator, passes all three GKSL conditions) and")
print("  conserves E_omega exactly. So the backward boundary CAN be generated")
print("  by a legitimate dynamics.")
print()
print("  The catch, and the result: that legitimate backward generator is a")
print("  STRUCTURALLY DISTINCT dynamics. The forward corridor L is ergodic --")
print(f"  one steady state. The backward generator is non-ergodic -- {deg_B}")
print("  conserved modes. They are in different ergodicity classes; one cannot")
print("  be reached from the other by a small perturbation. The backward")
print("  boundary has its OWN generator (a decoherence pinning the corridor-")
print("  penalty observable), not the forward dynamics plus a drive.")
print()
print("  This is the operator-level form of the karma/grace irreducibility:")
print("  forward (what a configuration builds) and backward (what it receives)")
print("  are generated by distinct, legitimate, non-interconvertible dynamics.")
print("  Path item (iii) resolves: the backward generator is legitimate and")
print("  exists; it is not a perturbation of the forward one. CMB drift can be")
print("  computed from a well-defined backward operator.")
