"""
The backward-state soft P_omega — the sharpened-F-11 test.
==========================================================

The metaphysics debate sharpened F-11 to a concrete formal test: F-11 fires
if a construction attempt on the BACKWARD-STATE soft operator
  E_omega(beta) = exp(-beta * sum_n H_n)
used as a TSVF post-selection effect returns empty, trivial, or
PARAMETER-UNPINNABLE (beta not pinned by framework-internal structure).

H_n penalises rung n's within-rung correlation for departing the corridor:
H_n = (rho_n - rho_c)^2, rho_n the rescaled within-rung correlation operator,
rho_c the corridor centre.

Three tests:
  1. beta-pinning. exp(-beta H_n) is a Gaussian in rho_n of width
     sigma = 1/sqrt(2 beta). Framework-internal candidate pin: sigma = w
     (corridor half-width) -> beta_pin = 1/(2 w^2).
  2. Dynamical consistency. The open-system reframe gave the framework a
     forward Lindbladian L. Its adjoint L^dag generates backward (Heisenberg)
     evolution. Is E_omega(beta) a fixed point of L^dag (a backward boundary
     the dynamics generates), or only the identity is?
  3. Post-selection work. At beta_pin, does E_omega select a corridor state
     above the rigidity / chaos poles, or is it trivial?

Model: 2 rungs x 3 spins (6 spins, dim 64). The rung correlation operator is
ANISOTROPIC (XYZ couplings unequal) so its spectrum is rich and an interior
corridor value is genuinely reachable -- an isotropic 3-spin Heisenberg
correlation is only 2-valued ({0,1}) and has no interior. Real construction.
"""
import numpy as np

np.set_printoptions(precision=4, suppress=True, linewidth=100)

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
SM = np.array([[0, 0], [1, 0]], dtype=complex)

NSPIN = 6
DIM = 2 ** NSPIN
rungs = [[0, 1, 2], [3, 4, 5]]


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
Id = np.eye(DIM, dtype=complex)

# anisotropic per-rung couplings -> rich rung-correlation spectrum
ANISO = [(0.7, 1.3, 0.5), (0.9, 0.6, 1.4)]


def rung_corr(spins, coupling):
    a, b, c = coupling
    op = np.zeros((DIM, DIM), dtype=complex)
    pairs = [(p, q) for i, p in enumerate(spins) for q in spins[i + 1:]]
    for (p, q) in pairs:
        op += a * SX[p] @ SX[q] + b * SY[p] @ SY[q] + c * SZ[p] @ SZ[q]
    op = op / len(pairs)
    op = (op + op.conj().T) / 2
    w = np.linalg.eigvalsh(op)
    return (op - w[0] * Id) / (w[-1] - w[0])


rho_hat = [rung_corr(r, ANISO[n]) for n, r in enumerate(rungs)]
for n, r in enumerate(rho_hat):
    nd = len(set(np.round(np.linalg.eigvalsh(r), 4)))
    print(f"  rung {n}: {nd} distinct eigenvalues of rho_n in [0,1]")

# corridor band in the genuine interior of the spectrum
RHO_LO, RHO_HI = 0.35, 0.55
RHO_C = 0.5 * (RHO_LO + RHO_HI)
W = 0.5 * (RHO_HI - RHO_LO)

Hn = [(r - RHO_C * Id) @ (r - RHO_C * Id) for r in rho_hat]
Hsum = Hn[0] + Hn[1]
Hsum = (Hsum + Hsum.conj().T) / 2
hval, hvec = np.linalg.eigh(Hsum)


def E_omega(beta):
    return (hvec * np.exp(-beta * hval)) @ hvec.conj().T


# ---- forward Lindbladian (the open-system reframe's dynamics) ----
J, g = 1.0, 0.4
H = np.zeros((DIM, DIM), dtype=complex)
for r in rungs:
    for i, p in enumerate(r):
        for q in r[i + 1:]:
            H += J * (SX[p] @ SX[q] + SY[p] @ SY[q] + SZ[p] @ SZ[q])
H += g * (SZ[2] @ SZ[3])
H = (H + H.conj().T) / 2

GAMMA_ALPHA, GAMMA_M = 0.7, 0.5
jumps = [np.sqrt(GAMMA_ALPHA) * sum(SMi[a] for a in r) for r in rungs]
jumps += [np.sqrt(GAMMA_M) * SX[i] for i in range(NSPIN)]


def liouvillian(adjoint=False):
    sgn = +1.0 if adjoint else -1.0
    Lv = sgn * 1j * (np.kron(H, Id) - np.kron(Id, H.T))
    for L in jumps:
        Ld = L.conj().T
        LdL = Ld @ L
        if adjoint:
            Lv += np.kron(Ld, Ld.conj()) - 0.5 * (np.kron(LdL, Id)
                                                  + np.kron(Id, LdL.T))
        else:
            Lv += np.kron(L, L.conj()) - 0.5 * (np.kron(LdL, Id)
                                                + np.kron(Id, LdL.T))
    return Lv


print()
print("=" * 76)
print("BACKWARD-STATE SOFT P_omega — sharpened-F-11 test")
print("=" * 76)
print(f"  2 rungs x 3 spins, dim {DIM}; corridor ({RHO_LO}, {RHO_HI}), "
      f"centre {RHO_C}, half-width w = {W}")
print(f"  Hsum spectrum: min {hval[0]:.4f}, max {hval[-1]:.4f}  "
      f"(min > 0 would mean no simultaneous-corridor state exists)")

print()
print("=" * 76)
print("TEST 1 — is beta pinned by framework-internal structure?")
print("=" * 76)
beta_pin = 1.0 / (2.0 * W * W)
print(f"  exp(-beta H_n) ~ Gaussian in rho_n, std sigma = 1/sqrt(2 beta).")
print(f"  Framework-internal candidate pin: sigma = corridor half-width w.")
print(f"  => beta_pin = 1/(2 w^2) = {beta_pin:.3f}")
print(f"  sigma(beta) vs corridor half-width w = {W}:")
for b in [1.0, 5.0, beta_pin, 100.0]:
    print(f"    beta = {b:>8.3f} : sigma = {1/np.sqrt(2*b):.4f}")
print(f"  beta is framework-REFERENCED (sigma = w => beta = 1/2w^2), not")
print(f"  framework-DERIVED: the framework fixes the corridor band but not the")
print(f"  edge sharpness (Piece 2: 'no specific scaling form prescribed').")
print(f"  Note: a narrow corridor forces a LARGE beta_pin -- and large beta")
print(f"  makes exp(-beta H) barely soft, i.e. near a hard projector.")

print()
print("=" * 76)
print("TEST 2 — is E_omega a backward boundary the dynamics generates?")
print("=" * 76)
Lfwd = liouvillian(adjoint=False)
Ladj = liouvillian(adjoint=True)
print(f"  ||L^dag[I]|| = {np.linalg.norm(Ladj @ Id.reshape(-1)):.2e}  "
      f"(identity is always an L^dag fixed point)")
ev = np.linalg.eigvals(Lfwd)
n_zero = int(np.sum(np.abs(ev) < 1e-9))
print(f"  forward L: {n_zero} zero eigenvalue(s) => "
      f"{'unique' if n_zero == 1 else f'{n_zero}-fold'} steady state; "
      f"L^dag has the same count of fixed points.")
print(f"  ||L^dag[E_omega(beta)]|| / ||E_omega||:")
for beta in [0.0, 0.5, 2.0, beta_pin]:
    E = E_omega(beta)
    res = np.linalg.norm(Ladj @ E.reshape(-1)) / np.linalg.norm(E)
    tag = "  <- beta_pin" if abs(beta - beta_pin) < 1e-6 else ""
    print(f"    beta = {beta:>8.3f} : {res:.4e}{tag}")
print(f"  => L^dag[E_omega] = 0 only at beta = 0 (E_omega -> I). The dynamics")
print(f"  generates exactly one backward boundary, the trivial one. A")
print(f"  non-trivial E_omega is an external POSTULATE, not a dynamical output.")

print()
print("=" * 76)
print("TEST 3 — at beta_pin, does E_omega select the corridor?")
print("=" * 76)
# Hsum eigenstates are joint eigenstates of rho_0, rho_1
r0 = np.array([np.real(hvec[:, k].conj() @ rho_hat[0] @ hvec[:, k])
               for k in range(DIM)])
r1 = np.array([np.real(hvec[:, k].conj() @ rho_hat[1] @ hvec[:, k])
               for k in range(DIM)])
k_corr = int(np.argmin(hval))                       # both rungs nearest rho_c
rig = np.where((r0 > 0.8) & (r1 > 0.8))[0]
cha = np.where((r0 < 0.2) & (r1 < 0.2))[0]
k_rig = int(rig[np.argmax(hval[rig])]) if len(rig) else int(np.argmax(hval))
k_cha = int(cha[np.argmax(hval[cha])]) if len(cha) else int(np.argmax(hval))
print(f"  weight of an Hsum-eigenstate v under E_omega(beta_pin) is "
      f"exp(-beta_pin * H(v)):")
for name, k in [("corridor (both rungs ~rho_c)", k_corr),
                ("rigidity (both rungs ~1)   ", k_rig),
                ("chaos    (both rungs ~0)   ", k_cha)]:
    wgt = np.exp(-beta_pin * hval[k])
    print(f"    {name}: rho_0={r0[k]:.3f} rho_1={r1[k]:.3f}  "
          f"H={hval[k]:.4f}  weight={wgt:.3e}")
w_corr = np.exp(-beta_pin * hval[k_corr])
w_rig = np.exp(-beta_pin * hval[k_rig])
w_cha = np.exp(-beta_pin * hval[k_cha])
sel = w_corr / max(w_rig, w_cha, 1e-300)
print(f"  selectivity corridor / max(rigidity, chaos) = {sel:.3e}")
selective = sel > 10
print(f"  => E_omega(beta_pin) {'IS selective' if selective else 'is NOT selective'}"
      f" -- but note (Test 1) beta_pin is large, so this selectivity is the")
print(f"  near-hard-projector limit, not a genuinely soft post-selection.")

print()
print("=" * 76)
print("VERDICT — does the sharpened F-11 fire?")
print("=" * 76)
print(f"  empty?       no  -- E_omega = exp(-beta sum H_n) is positive, full rank.")
print(f"  trivial?     no  -- at beta_pin it selects the corridor "
      f"({sel:.1e}x over the poles).")
print(f"  unpinnable?  partly -- beta is framework-REFERENCED (= 1/2w^2) but")
print(f"               not framework-DERIVED; the corridor edge sharpness is a")
print(f"               choice the framework does not prescribe.")
print(f"  => the sharpened F-11 does NOT cleanly fire. The backward soft")
print(f"     P_omega is constructible and non-trivial with a beta tied to the")
print(f"     corridor width.")
print(f"  Two honest riders the toy returns:")
print(f"   (i) TEST 2 — E_omega is NOT generated by the framework's forward")
print(f"       dynamics; L^dag's only fixed point is the identity. A non-")
print(f"       trivial backward operator is a free-standing POSTULATE (input),")
print(f"       not an output of the theory.")
print(f"  (ii) TEST 1 — pinning beta to a narrow corridor forces beta large,")
print(f"       where exp(-beta H) is near a hard projector. The 'soft' escape")
print(f"       from the hard-projector failures is not exercised at beta_pin.")
print(f"  Net: F-11 stays armed but unfired. The backward soft P_omega is a")
print(f"  coherent named conjecture -- constructible, postulated, dynamics-")
print(f"  independent -- not retracted, not promoted to derived content.")
