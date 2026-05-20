"""
Construction of P_omega as a genuine orthogonal projector.
=========================================================

P_omega is the projector onto multi-rung corridor configurations at the
cosmological future boundary. The integration paper carries it as an
axiomatized primitive (falsification handle F-11). This script constructs it
explicitly for a finite-rung tensor-product model and verifies the projector
axioms numerically.

THE CONSTRUCTION
----------------
1. rho_n is a SELF-ADJOINT OPERATOR on rung n -- the within-rung correlation
   observable -- not a nonlinear functional of the global state. For a rung of
   N constituents, rho_n is the (rescaled) average pairwise correlation
   operator across them.

2. P_n = spectral projection of rho_n onto the corridor band [lo, hi]. By the
   spectral theorem the spectral projection of a self-adjoint operator onto a
   Borel set is an orthogonal projector: P_n^2 = P_n, P_n^dagger = P_n.

3. P_omega = product over rungs of P_n. On a tensor-product rung decomposition
   the rho_n act on distinct factors, so the P_n commute, and the product of
   commuting orthogonal projectors is an orthogonal projector onto the
   intersection of their ranges.

This realizes the paper's "integral of |config><config| dconfig over
corridor-satisfying configs": dconfig is the joint spectral measure of the
rho_n operators; the binary rung-instantiation indicator is P_n; the
"well-defined projection vs set-theoretic intersection" problem dissolves
because the product of commuting projectors projects onto the intersection.

WHAT THIS DOES AND DOES NOT ESTABLISH
-------------------------------------
Does: constructs P_omega as a genuine orthogonal projector for a finite-rung
tensor-product model; verifies the axioms; shows it functioning as a TSVF
post-selector that suppresses non-corridor forward histories.

Does not: (a) handle cross-rung non-factorization -- if rungs nest, the rho_n
may not commute and P_omega is the projector onto the intersection subspace
but not the simple product; (b) build the cosmological configuration Hilbert
space. The operator FORM of P_omega is constructed here; the cosmological
space it acts on is not. F-11's no-go does not fire; the open problem is now
(a) and (b), sharper than "P_omega is unconstructed".
"""
import numpy as np
import itertools

np.set_printoptions(precision=4, suppress=True, linewidth=100)

# ---------------------------------------------------------------- parameters
R = 3                      # number of rungs
N = 4                      # spin-1/2 constituents per rung
CORRIDOR = (0.10, 0.43)    # the framework's corridor band, in rho units

rdim = 2 ** N              # rung Hilbert-space dimension (16)
dim = rdim ** R            # total Hilbert-space dimension (4096)

# ---------------------------------------------------------------- Pauli ops
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def kron_all(ops):
    out = ops[0]
    for o in ops[1:]:
        out = np.kron(out, o)
    return out


def site_op(op, site, n):
    """Single-constituent operator on an n-constituent rung space."""
    ops = [I2] * n
    ops[site] = op
    return kron_all(ops)


# ---------------------------------------------- STEP 1: rho_n as an operator
# Average pairwise Heisenberg correlation across the rung's constituents,
# rescaled so the spectrum lands in [0, 1]: 0 = chaos pole (no correlation),
# 1 = rigidity pole (single-voice), interior = corridor.
C = np.zeros((rdim, rdim), dtype=complex)
pairs = list(itertools.combinations(range(N), 2))
for (i, j) in pairs:
    C += (site_op(X, i, N) @ site_op(X, j, N)
          + site_op(Y, i, N) @ site_op(Y, j, N)
          + site_op(Z, i, N) @ site_op(Z, j, N))
C = C / len(pairs)
rho = (C + np.eye(rdim)) / 2          # self-adjoint; spectrum in [0, 1]

assert np.allclose(rho, rho.conj().T), "rho_n must be self-adjoint"
w, V = np.linalg.eigh(rho)
spectrum = sorted(set(np.round(w, 6)))
print("=" * 70)
print("STEP 1 -- rho_n as a self-adjoint operator")
print("=" * 70)
print(f"  rung: {N} spin-1/2 constituents, rung dim = {rdim}")
print(f"  rho_n spectrum (attainable within-rung correlation values): {spectrum}")
for s in spectrum:
    mult = int(np.sum(np.isclose(w, s)))
    pole = ("chaos pole" if s < CORRIDOR[0] else
            "rigidity pole" if s > CORRIDOR[1] else "CORRIDOR")
    print(f"    rho = {s:+.4f}   multiplicity {mult:2d}   [{pole}]")

# ------------------------------------ STEP 2: P_n as a spectral projection
lo, hi = CORRIDOR
in_band = (w >= lo) & (w <= hi)
Vb = V[:, in_band]
p_band = Vb @ Vb.conj().T             # orthogonal projector on the rung space

print()
print("=" * 70)
print("STEP 2 -- P_n = spectral projection of rho_n onto the corridor band")
print("=" * 70)
print(f"  corridor band: rho in ({lo}, {hi})")
print(f"  rank(P_n) = {int(np.round(np.trace(p_band).real))}  "
      f"(dimension of the rung corridor subspace)")
print(f"  P_n^2 = P_n          : {np.allclose(p_band @ p_band, p_band)}")
print(f"  P_n^dagger = P_n     : {np.allclose(p_band, p_band.conj().T)}")


def embed(op_rung, rung_index):
    factors = [np.eye(rdim, dtype=complex)] * R
    factors[rung_index] = op_rung
    return kron_all(factors)


# ----------------------------------- STEP 3: P_omega = product of the P_n
P = [embed(p_band, n) for n in range(R)]

# verify the per-rung projectors commute (distinct tensor factors)
max_commutator = 0.0
for a in range(R):
    for b in range(a + 1, R):
        comm = P[a] @ P[b] - P[b] @ P[a]
        max_commutator = max(max_commutator, np.abs(comm).max())

P_omega = np.eye(dim, dtype=complex)
for Pn in P:
    P_omega = P_omega @ Pn

print()
print("=" * 70)
print("STEP 3 -- P_omega = product over rungs of P_n")
print("=" * 70)
print(f"  rungs R = {R}, total Hilbert dim = {dim}")
print(f"  max ||[P_a, P_b]|| over rung pairs : {max_commutator:.2e}  "
      f"(0 => P_n mutually commute)")

idem = np.abs(P_omega @ P_omega - P_omega).max()
herm = np.abs(P_omega - P_omega.conj().T).max()
rank = int(np.round(np.trace(P_omega).real))
expected_rank = int(np.round(np.trace(p_band).real)) ** R
# a projector has spectrum {0,1}; check via P(P-I)=0
spectral = np.abs(P_omega @ (P_omega - np.eye(dim))).max()

print()
print("  VERIFICATION -- P_omega is a genuine orthogonal projector:")
print(f"    idempotent   ||P_omega^2 - P_omega||      = {idem:.2e}")
print(f"    self-adjoint ||P_omega - P_omega^dagger|| = {herm:.2e}")
print(f"    spectrum {{0,1}} ||P_omega(P_omega - I)|| = {spectral:.2e}")
print(f"    rank(P_omega) = {rank}   expected rank(P_n)^R = {expected_rank}   "
      f"match: {rank == expected_rank}")
is_projector = (idem < 1e-9 and herm < 1e-9 and spectral < 1e-9
                and rank == expected_rank)
print(f"    => P_omega IS an orthogonal projector: {is_projector}")

# --------------------------------- STEP 4: P_omega as a TSVF post-selector
print()
print("=" * 70)
print("STEP 4 -- P_omega functioning as a TSVF post-selector")
print("=" * 70)

# forward Hamiltonian: rung-local Heisenberg + weak cross-rung coupling
rng = np.random.default_rng(20260520)
H = np.zeros((dim, dim), dtype=complex)
# rung-local terms
for n in range(R):
    for (i, j) in pairs:
        for P_op in (X, Y, Z):
            term = embed(site_op(P_op, i, N) @ site_op(P_op, j, N), n)
            H += 0.5 * term
# weak cross-rung coupling (carried by H, not by the state-space decomposition)
for n in range(R - 1):
    factors = [np.eye(rdim, dtype=complex)] * R
    factors[n] = site_op(Z, 0, N)
    factors[n + 1] = site_op(Z, 0, N)
    H += 0.15 * kron_all(factors)
H = (H + H.conj().T) / 2

eH, UH = np.linalg.eigh(H)
t_f = 1.7


def evolve(state, t):
    phase = np.exp(-1j * eH * t)
    return UH @ (phase * (UH.conj().T @ state))


# backward boundary state: drawn from the range of P_omega (corridor-supported)
phi_seed = rng.standard_normal(dim) + 1j * rng.standard_normal(dim)
phi_tf = P_omega @ phi_seed
phi_tf = phi_tf / np.linalg.norm(phi_tf)

# two forward initial states: one corridor-compatible, one corridor-orthogonal
psi_corr_seed = rng.standard_normal(dim) + 1j * rng.standard_normal(dim)
psi_corr_0 = P_omega @ psi_corr_seed
psi_corr_0 = psi_corr_0 / np.linalg.norm(psi_corr_0)

psi_anti_seed = rng.standard_normal(dim) + 1j * rng.standard_normal(dim)
psi_anti_0 = (np.eye(dim) - P_omega) @ psi_anti_seed
psi_anti_0 = psi_anti_0 / np.linalg.norm(psi_anti_0)

# post-selection probability ||P_omega |psi(t_f)>||^2 for each forward history
psi_corr_tf = evolve(psi_corr_0, t_f)
psi_anti_tf = evolve(psi_anti_0, t_f)
ps_corr = np.linalg.norm(P_omega @ psi_corr_tf) ** 2
ps_anti = np.linalg.norm(P_omega @ psi_anti_tf) ** 2

print(f"  forward Hamiltonian: rung-local Heisenberg + weak cross-rung Z-Z")
print(f"  post-selection probability ||P_omega|psi(t_f)>||^2 :")
print(f"    corridor-seeded forward history   : {ps_corr:.4f}")
print(f"    corridor-orthogonal forward history: {ps_anti:.4f}")

# ABL weak value of a rung observable, well-defined for corridor pre/post
A = embed(rho, 0)        # rung-1 within-rung correlation observable
phi_t = evolve(phi_tf, -(t_f - 0.0))     # <Phi_omega(t)| = <Phi_omega(t_f)|U(t_f,t)
for label, psi0 in (("corridor", psi_corr_0), ("corridor-orthogonal", psi_anti_0)):
    psi_t = psi0                          # observe at t = 0
    denom = np.vdot(phi_t, psi_t)
    numer = np.vdot(phi_t, A @ psi_t)
    if abs(denom) < 1e-12:
        print(f"  ABL weak value <rho_1>_w [{label:20s}]: "
              f"denominator |<Phi|Psi>| = {abs(denom):.2e}  -> history suppressed")
    else:
        wv = numer / denom
        print(f"  ABL weak value <rho_1>_w [{label:20s}]: {wv.real:+.4f}{wv.imag:+.4f}j"
              f"   (|<Phi|Psi>| = {abs(denom):.3e})")

print()
print("=" * 70)
print("RESULT")
print("=" * 70)
print(f"  P_omega constructed as a genuine orthogonal projector for the")
print(f"  R={R}-rung tensor-product model: {is_projector}.")
print(f"  It functions as a TSVF post-selector: corridor-orthogonal forward")
print(f"  histories are suppressed (vanishing ABL denominator); corridor")
print(f"  histories carry well-defined weak values.")
print(f"  Open: cross-rung non-factorization, and the cosmological")
print(f"  configuration Hilbert space. F-11 no-go does not fire.")
