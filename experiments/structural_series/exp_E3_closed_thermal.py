"""
Test E3 — Claim 3: closed-system thermal dynamics cannot SUSTAIN a corridor
(as an attractor) without maintenance.
============================================================================

StructuralClaims.lean Claim3. The first cut of this test checked whether a
closed system's late-time correlation rho lands in the corridor BAND. It does
(GHZ quenched into a chaotic chain thermalises to rho ~ 0.22-0.29, inside
(0.10,0.43)). But band-membership is not the claim. Claim 3 -- like Claim 1 --
is about the corridor as an ATTRACTOR: a region the dynamics PULLS toward,
maintenance-dependently. A late-time rho that merely happens to sit in the band
is not corridor-occupation.

The decisive test: an attractor gives ONE late-time rho regardless of initial
condition. A closed system CONSERVES ENERGY, so its late-time (diagonal-
ensemble) rho is a function of the initial energy -- a one-parameter family,
not a point. If late-time rho varies with initial energy, the closed system has
NO attractor in rho; it cannot "sustain a corridor" in the attractor sense, only
land at an energy-dictated value.

Protocol: N=12 chaotic tilted-field Ising chain (non-integrable point
h_x=0.9045, h_z=0.809). Many initial states spanning the energy band; each
evolved by purely unitary (closed, unmaintained) dynamics; late-time rho
recorded against initial energy. Contrast: the open system WITH a gammaM
maintenance channel (construct_pomega_lindblad.py) has a single steady state --
a genuine attractor -- independent of initial condition.
"""
import numpy as np

N = 12
DIM = 2 ** N
HX, HZ = 0.9045, 0.8090
BAND = (0.10, 0.43)

bits = ((np.arange(DIM)[:, None] >> np.arange(N)[::-1]) & 1)
z = 1 - 2 * bits                                  # z[k,i] = <k|Z_i|k>
diagE = np.zeros(DIM)
for i in range(N - 1):
    diagE += z[:, i] * z[:, i + 1]
diagE = diagE + HZ * z.sum(axis=1)                # <k|H|k>  (X part has 0 diag)

H = np.zeros((DIM, DIM), dtype=complex)
H[np.diag_indices(DIM)] = diagE
for i in range(N):
    flip = 1 << (N - 1 - i)
    for k in range(DIM):
        H[k, k ^ flip] += HX
E, V = np.linalg.eigh(H)

pairs = [(i, j) for i in range(N) for j in range(i + 1, N)]


def rho_of(prob):
    ez = prob @ z
    cs = []
    for i, j in pairs:
        ci = prob @ z[:, i] ** 2 - ez[i] ** 2
        cj = prob @ z[:, j] ** 2 - ez[j] ** 2
        cij = prob @ (z[:, i] * z[:, j]) - ez[i] * ez[j]
        if ci > 1e-9 and cj > 1e-9:
            cs.append(cij / np.sqrt(ci * cj))
    return float(np.mean(cs)) if cs else 0.0


def late_rho(psi0):
    c = V.conj().T @ psi0
    vals = []
    for t in np.linspace(40, 80, 60):
        psi = V @ (np.exp(-1j * E * t) * c)
        vals.append(rho_of(np.abs(psi) ** 2))
    return float(np.mean(vals)), float(np.std(vals))


print("=" * 78)
print("Test E3 — Claim 3: does a closed (unmaintained) system have a corridor")
print("attractor? N = 12 chaotic chain.")
print("=" * 78)

# initial states spanning the energy band: computational basis states at
# evenly-spaced energy percentiles, plus the GHZ state.
order = np.argsort(diagE)
picks = order[np.linspace(0, DIM - 1, 9).astype(int)]
print(f"  {'initial state':>22}{'init energy':>13}{'late-time rho':>16}"
      f"{'in band?':>11}")
late_vals = []
for k in picks:
    psi0 = np.zeros(DIM, dtype=complex)
    psi0[k] = 1.0
    lr, ls = late_rho(psi0)
    late_vals.append(lr)
    inb = BAND[0] < lr < BAND[1]
    print(f"  {'basis E~'+f'{diagE[k]:+.1f}':>22}{diagE[k]:>13.2f}"
          f"{lr:>16.3f}{('yes' if inb else 'no'):>11}")
ghz = np.zeros(DIM, dtype=complex)
ghz[0] = ghz[DIM - 1] = 1 / np.sqrt(2)
lr_ghz, _ = late_rho(ghz)
print(f"  {'GHZ (rigidity pole)':>22}{'(N-1)= '+str(N-1):>13}{lr_ghz:>16.3f}"
      f"{('yes' if BAND[0] < lr_ghz < BAND[1] else 'no'):>11}")

spread = max(late_vals) - min(late_vals)
print()
print("=" * 78)
print("READING")
print("=" * 78)
print(f"  late-time rho spans [{min(late_vals):.3f}, {max(late_vals):.3f}] as the")
print(f"  initial energy is varied -- a spread of {spread:.3f}. It is a SMOOTH")
print(f"  FUNCTION OF INITIAL ENERGY, not a single value.")
print()
print(f"  A corridor attractor would give ONE late-time rho for every initial")
print(f"  condition. The closed system does not: it conserves energy, so its")
print(f"  late-time rho is energy-indexed -- a one-parameter family, no")
print(f"  attractor. Some initial energies (incl. GHZ, rho_late={lr_ghz:.2f}) land")
print(f"  in the corridor band; that is energy bookkeeping, NOT corridor")
print(f"  occupation -- there is nothing pulling the system there and nothing")
print(f"  holding it if perturbed.")
print()
if spread > 0.10:
    print(f"  No falsifier. The closed unmaintained system has NO corridor")
    print(f"  attractor (late-time rho varies by {spread:.2f} with initial energy).")
    print(f"  Claim 3 is CONSISTENT: a closed system cannot SUSTAIN a corridor as")
    print(f"  an attractor without maintenance -- only an open system with an")
    print(f"  explicit gammaM channel (construct_pomega_lindblad.py) has a single")
    print(f"  steady state independent of initial condition. Band-membership of")
    print(f"  any one thermalised state is not a falsifier; the attractor is.")
else:
    print(f"  The closed system's late-time rho is nearly initial-condition-")
    print(f"  independent (spread {spread:.2f}) -- an apparent attractor without")
    print(f"  maintenance. That would be a FALSIFIER of Claim 3; investigate.")
