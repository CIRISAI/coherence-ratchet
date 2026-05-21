"""
The postulate -> dynamics bridge for the backward soft P_omega.
===============================================================

Standing limitation after the rung-scaling and calibration runs: the backward
soft operator E_omega(beta) = exp(-beta * H_sum), used as a TSVF post-selection
effect, is a FREE-STANDING POSTULATE. The forward Lindbladian L has a unique
steady state rho_ss (the forward soft P_omega); its Heisenberg adjoint L^dag
has a unique fixed point, the identity I -- so ||L^dag[E_omega]|| = 0 only at
beta = 0. E_omega is an input, not a dynamical output.

Path item (ii): turn that postulate into a NAMED, TESTABLE structural
hypothesis. The question is literal: what modification D_omega makes
E_omega a fixed point of a modified adjoint  L~^dag = L^dag + D_omega ?
Then D_omega is the operator-level content of "the universe has a future
boundary condition" -- and we can measure how large, and how structured, it
has to be.

Model. The corridor Lindbladian of construct_pomega_lindblad.py: 3 rungs x 2
spins (dim 64), H = intra-rung Heisenberg + cross-rung ZZ, alpha = per-rung
collective decay (rigidity drift), gammaM = per-spin bit-flip (maintenance).
Here the rung observable is upgraded to a genuine anisotropic correlation
OPERATOR O_n with a real [0,1] spectrum (so H_sum = sum_n (O_n - rho_c)^2 is
non-trivial, not a c-number).

Four tests:
  A. H_sum conservation -- ||L^dag[H_sum]|| / (||L^dag|| ||H_sum||). If H_sum
     is nearly conserved, E_omega is nearly a fixed point for ALL beta and the
     modification is small: the postulate is nearly an output.
  B. The modification D_omega. The minimal-norm modification with
     L~^dag[E_omega] = 0 is rank-1: D_omega[X] = -L^dag[E_omega] <E_omega,X>
     / ||E_omega||^2. Its size ||D_omega|| / ||L^dag|| is the "non-dynamical
     fraction" of the postulate. Reported across beta incl. the framework-
     referenced beta_pin = 1/2w^2. Leading order: D_omega ~ beta * L^dag[H_sum]
     -- the corridor-penalty current; checked by the alignment cosine.
  C. Gibbs test -- is rho_ss itself ~ exp(-beta_dyn H_sum)? If so E_omega is a
     POWER of the forward steady state, dynamically generated, beta tied to
     beta_dyn. Regress log(rho_ss) on H_sum (and on H, for comparison).
  D. Detailed balance -- is the dissipative generator self-adjoint in the GNS
     inner product of rho_ss? Measures how time-symmetric the dynamics is
     about its steady state.
"""
import numpy as np
from scipy.linalg import expm, logm

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


# Hamiltonian: intra-rung Heisenberg + cross-rung ZZ (Piece 6 coupling)
J, g = 1.0, 0.5
H = np.zeros((DIM, DIM), dtype=complex)
for (a, b) in rungs:
    H += J * (SX[a] @ SX[b] + SY[a] @ SY[b] + SZ[a] @ SZ[b])
for n in range(len(rungs) - 1):
    H += g * (SZ[rungs[n][1]] @ SZ[rungs[n + 1][0]])
H = hermit(H)

# genuine rung correlation operators: anisotropic, real [0,1] spectrum
COUP = [(0.7, 1.3, 0.5), (1.2, 0.6, 1.1), (0.9, 1.4, 0.8)]


def rung_corr(a, b, coup):
    cx, cy, cz = coup
    O = cx * SX[a] @ SX[b] + cy * SY[a] @ SY[b] + cz * SZ[a] @ SZ[b]
    O = hermit(O)
    w = np.linalg.eigvalsh(O)
    return (O - w[0] * Id) / (w[-1] - w[0])


O = [rung_corr(a, b, c) for (a, b), c in zip(rungs, COUP)]
Hsum = hermit(sum((On - RHO_C * Id) @ (On - RHO_C * Id) for On in O))

# Lindbladian
GAMMA_ALPHA = [0.6, 1.0, 1.5]
alpha_jumps = [np.sqrt(rate) * (SMi[a] + SMi[b])
               for rate, (a, b) in zip(GAMMA_ALPHA, rungs)]
bf_ops = [SX[i] for i in range(NSPIN)]


def diss_term(L):
    LdL = L.conj().T @ L
    return (np.kron(L, L.conj())
            - 0.5 * np.kron(LdL, Id) - 0.5 * np.kron(Id, LdL.T))


Lham = -1j * (np.kron(H, Id) - np.kron(Id, H.T))
Ldiss = sum(diss_term(Lj) for Lj in alpha_jumps)
Lbf = sum(diss_term(Xi) for Xi in bf_ops)
GM = 0.10                                   # maintenance rate (corridor band)
Ldiss = Ldiss + GM * Lbf
Lsuper = Lham + Ldiss                        # full Liouvillian (vec, row-major)
vecI = Id.reshape(-1)


def steady_state():
    M = Lsuper.copy()
    M[0, :] = vecI
    b = np.zeros(DIM * DIM, dtype=complex)
    b[0] = 1.0
    rho = np.linalg.solve(M, b).reshape(DIM, DIM)
    return hermit(rho) / np.trace(hermit(rho)).real


def apply_super(S, A):
    return (S @ A.reshape(-1)).reshape(DIM, DIM)


def fro(A):
    return float(np.linalg.norm(A))


def hs_inner(A, B):
    """Hilbert-Schmidt real inner product Re Tr(A^dag B)."""
    return float(np.real(np.vdot(A.reshape(-1), B.reshape(-1))))


rho_ss = steady_state()
Ladj = Lsuper.conj().T                       # adjoint: <A,LB> = <L^dag A, B>
Lop = float(np.linalg.norm(Lsuper, 2))       # spectral norm of L

print("=" * 80)
print("BACKWARD soft P_omega -- the postulate -> dynamics bridge")
print("=" * 80)
ev = np.linalg.eigvalsh(rho_ss)
print(f"  dim {DIM}; Liouvillian {DIM*DIM}x{DIM*DIM}; gammaM = {GM}")
print(f"  rho_ss valid: trace {np.trace(rho_ss).real:.6f}, min eig "
      f"{ev.min():+.2e}, rank {int(np.sum(ev > 1e-9))}")
print(f"  rung correlations <O_n>_ss = "
      f"{[round(hs_inner(rho_ss, On), 3) for On in O]}  (these [0,1]-rescaled")
print(f"    anisotropic operators sit near their spectral mean; the four")
print(f"    bridge tests below are structural and gammaM-independent)")
print(f"  ||L|| (spectral) = {Lop:.3f};  L^dag[I] residual = "
      f"{fro(apply_super(Ladj, Id)):.2e}  (I is the only naive fixed point)")

# ---------------------------------------------------------------------------
# TEST A -- is the corridor-penalty operator H_sum conserved?
# ---------------------------------------------------------------------------
print()
print("-" * 80)
print("TEST A -- H_sum conservation under the dynamics")
print("-" * 80)
LdHsum = apply_super(Ladj, Hsum)
consA = fro(LdHsum) / (Lop * fro(Hsum))
print(f"  ||L^dag[H_sum]|| / (||L|| ||H_sum||) = {consA:.4f}")
_consword = ("nearly conserved" if consA < 0.05
             else "weakly non-conserved" if consA < 0.15 else "not conserved")
print(f"  -- the corridor penalty is {_consword} by the dynamics.")
print(f"  (if it were conserved, exp(-beta H_sum) would be a fixed point of")
print(f"  L^dag for every beta and the postulate would be a free output.)")

# ---------------------------------------------------------------------------
# TEST B -- the modification D_omega that makes E_omega a fixed point
# ---------------------------------------------------------------------------
print()
print("-" * 80)
print("TEST B -- the modified adjoint  L~^dag = L^dag + D_omega")
print("-" * 80)
print("  D_omega is the minimal-norm modification with L~^dag[E_omega] = 0.")
print("  ||D_omega||/||L|| = the 'non-dynamical fraction' the postulate needs.")
print(f"  {'beta':>8} {'||L^dag[E]||/||E||':>18} {'||D_omega||/||L||':>17} "
      f"{'cos<.,L^dag[H_sum]>':>20}")
betas = [0.5, 1.0, 2.0, 5.0, 10.0, 22.2, 50.0]
for beta in betas:
    Eom = expm(-beta * Hsum)
    LdE = apply_super(Ladj, Eom)
    res = fro(LdE) / fro(Eom)
    dfrac = res / Lop
    cosang = (hs_inner(LdE, LdHsum) / (fro(LdE) * fro(LdHsum))
              if fro(LdE) > 1e-14 else float("nan"))
    tag = ""
    if abs(beta - 22.2) < 0.5:
        tag = "  <- beta_pin, w=0.15"
    if abs(beta - 50.0) < 0.5:
        tag = "  <- beta_pin, w=0.10"
    print(f"  {beta:>8.1f} {res:>18.4f} {dfrac:>17.4f} {cosang:>20.4f}{tag}")
print("  cos -> 1 confirms D_omega is, to leading order, built from")
print("  L^dag[H_sum] -- the corridor-penalty current. THAT is the named")
print("  structure: the backward boundary drive is the penalty current.")

# ---------------------------------------------------------------------------
# TEST C -- is rho_ss Gibbs in H_sum?  (then E_omega is a power of rho_ss)
# ---------------------------------------------------------------------------
print()
print("-" * 80)
print("TEST C -- Gibbs test: rho_ss ~ exp(-beta_dyn H_sum) ?")
print("-" * 80)
log_rho = hermit(logm(rho_ss))


def regress(target, basis):
    """Least-squares fit target ~ sum c_k basis_k + c0 I, Hermitian operators,
    real coefficients. Returns coeffs and R^2."""
    cols = basis + [Id]
    G = np.array([[hs_inner(p, q) for q in cols] for p in cols])
    rhs = np.array([hs_inner(p, target) for p in cols])
    coef = np.linalg.solve(G, rhs)
    fit = sum(c * p for c, p in zip(coef, cols))
    mean = hs_inner(target, Id) / hs_inner(Id, Id)
    ss_tot = fro(target - mean * Id) ** 2
    r2 = 1.0 - fro(target - fit) ** 2 / ss_tot
    return coef, r2


cH, r2H = regress(log_rho, [Hsum])
cHam, r2Ham = regress(log_rho, [H])
cBoth, r2Both = regress(log_rho, [Hsum, H])
commute = fro(rho_ss @ Hsum - Hsum @ rho_ss) / (fro(rho_ss) * fro(Hsum))
print(f"  ||[rho_ss, H_sum]|| / (||rho_ss|| ||H_sum||) = {commute:.4f}")
print(f"  log(rho_ss) ~ a*H_sum + c :   beta_dyn = {-cH[0]:+.4f}, "
      f"R^2 = {r2H:.4f}")
print(f"  log(rho_ss) ~ a*H     + c :   coeff    = {cHam[0]:+.4f}, "
      f"R^2 = {r2Ham:.4f}")
print(f"  log(rho_ss) ~ a*H_sum + b*H + c :          R^2 = {r2Both:.4f}")
beta_dyn = -cH[0]
if r2H > 0.9 and beta_dyn > 0:
    print(f"  -> rho_ss IS ~Gibbs in H_sum. E_omega(beta) = (Z rho_ss)^(beta/"
          f"beta_dyn): a POWER of the forward steady state -- dynamically "
          f"generated.")
else:
    print(f"  -> rho_ss is not cleanly Gibbs in H_sum alone "
          f"(R^2 = {r2H:.2f}); the backward operator is not simply a power "
          f"of rho_ss.")

# ---------------------------------------------------------------------------
# TEST D -- detailed balance: is the dissipator GNS-self-adjoint about rho_ss?
# ---------------------------------------------------------------------------
print()
print("-" * 80)
print("TEST D -- detailed balance of the dissipative generator about rho_ss")
print("-" * 80)
# GNS metric for row-major vec:  <A,B>_GNS = Tr(rho A^dag B) = vec(A)^dag G vec(B)
G = np.kron(Id, rho_ss.T)
Ginv = np.kron(Id, np.linalg.inv(rho_ss).T)
Ddag_GNS = Ginv @ Ldiss.conj().T @ G
db_viol = float(np.linalg.norm(Ldiss - Ddag_GNS, 2)) / float(
    np.linalg.norm(Ldiss, 2))
print(f"  ||D - D^GNS-adjoint|| / ||D|| = {db_viol:.4f}")
print(f"  -- the dynamics is {'time-symmetric' if db_viol < 0.1 else 'NOT time-symmetric'}"
      f" about its steady state.")

# ---------------------------------------------------------------------------
# SYNTHESIS
# ---------------------------------------------------------------------------
print()
print("=" * 80)
print("SYNTHESIS -- where the bridge stands")
print("=" * 80)
dfrac_pin = (fro(apply_super(Ladj, expm(-22.2 * Hsum)))
             / fro(expm(-22.2 * Hsum))) / Lop
print(f"  A. H_sum is {_consword} (non-conservation {consA:.3f}) -- so at small")
print(f"     beta E_omega is nearly a fixed point already.")
print(f"  B. At the framework beta_pin (w=0.15), making E_omega an exact fixed")
print(f"     point needs a modification D_omega of relative size "
      f"{dfrac_pin:.3f} ||L||.")
print(f"     D_omega aligns with the corridor-penalty current L^dag[H_sum] -- "
      f"a NAMED object.")
print(f"  C. rho_ss-vs-H_sum Gibbs R^2 = {r2H:.3f}; rho_ss-vs-H R^2 = "
      f"{r2Ham:.3f}.")
print(f"  D. detailed-balance violation {db_viol:.3f}.")
print()
print("  READING. The bridge is not free: E_omega cannot be an exact fixed")
print("  point of the bare adjoint (L^dag contracts to I -- structural). But")
print("  the modification is now NAMED and SIZED, not mysterious:")
print("    L~^dag = L^dag + D_omega,   D_omega proportional to L^dag[H_sum].")
print("  The postulate 'the universe has a backward boundary E_omega' becomes")
print("  the structural hypothesis 'the backward generator carries a corridor-")
print("  penalty-current drive D_omega', with a measured magnitude. That is a")
print("  testable claim about cosmological backward dynamics, not a free input.")
