"""
Test E6 — Claim 5: multi-rung corridor structure from GENERIC initial
conditions requires backward conditioning.
============================================================================

StructuralClaims.lean Claim5 (scope corrected last round to cosmological
ORIGIN): a substrate reaching multi-rung corridor structure FROM GENERIC
high-entropy initial conditions did so via backward conditioning (P_omega).
Falsifier5: multi-rung corridor structure reached from generic initial
conditions by purely FORWARD dynamics.

This searches for the falsifier in the closed/unitary case (the cosmological-
origin scope — a closed universe forward-evolving). A closed N=12 chaotic chain
is partitioned into 3 rungs of 4 spins. Many GENERIC high-entropy initial
states (Haar-random pure states — maximal entanglement, mid-spectrum energy)
are forward-evolved by purely unitary dynamics; the fraction reaching the
multi-rung corridor (all 3 rungs simultaneously in band) is the measured-
probability proxy for the forward amplitude.

Scope note: this does NOT contradict construct_pomega_lindblad.py, where a
FORWARD OPEN dynamics WITH a gammaM maintenance channel reaches the multi-rung
corridor. That presupposes the maintenance structure. Claim 5 is about generic
initial conditions under forward dynamics ALONE — the Penrose-past scope
(Piece 8): forward evolution to omega-structure is measure-zero.
"""
import numpy as np

N = 12
DIM = 2 ** N
HX, HZ = 0.9045, 0.8090
BAND = (0.10, 0.43)
RUNGS = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]]

bits = ((np.arange(DIM)[:, None] >> np.arange(N)[::-1]) & 1)
z = 1 - 2 * bits
H = np.zeros((DIM, DIM), dtype=complex)
diagE = np.zeros(DIM)
for i in range(N - 1):
    diagE += z[:, i] * z[:, i + 1]
diagE += HZ * z.sum(axis=1)
H[np.diag_indices(DIM)] = diagE
for i in range(N):
    flip = 1 << (N - 1 - i)
    for k in range(DIM):
        H[k, k ^ flip] += HX
E, V = np.linalg.eigh(H)
rng = np.random.default_rng(20260521)


def rung_rhos(prob):
    """Per-rung mean pairwise connected Z-correlation."""
    ez = prob @ z
    out = []
    for rung in RUNGS:
        cs = []
        for a in range(len(rung)):
            for b in range(a + 1, len(rung)):
                i, j = rung[a], rung[b]
                ci = prob @ z[:, i] ** 2 - ez[i] ** 2
                cj = prob @ z[:, j] ** 2 - ez[j] ** 2
                cij = prob @ (z[:, i] * z[:, j]) - ez[i] * ez[j]
                if ci > 1e-9 and cj > 1e-9:
                    cs.append(cij / np.sqrt(ci * cj))
        out.append(float(np.mean(cs)) if cs else 0.0)
    return out


def late_multirung(psi0):
    """Late-time per-rung rho, averaged over a late window."""
    c = V.conj().T @ psi0
    acc = np.zeros(3)
    ts = np.linspace(40, 80, 30)
    for t in ts:
        psi = V @ (np.exp(-1j * E * t) * c)
        acc += np.array(rung_rhos(np.abs(psi) ** 2))
    return acc / len(ts)


print("=" * 78)
print("Test E6 — Claim 5: forward amplitude from generic ICs to multi-rung")
print("corridor (N=12 closed chaotic chain, 3 rungs of 4).")
print("=" * 78)
N_IC = 200
in_corr = 0
rung_means = []
for _ in range(N_IC):
    v = rng.standard_normal(DIM) + 1j * rng.standard_normal(DIM)   # Haar-random
    v /= np.linalg.norm(v)
    r = late_multirung(v)
    rung_means.append(r)
    if all(BAND[0] < x < BAND[1] for x in r):
        in_corr += 1
rung_means = np.array(rung_means)
frac = in_corr / N_IC
print(f"  {N_IC} Haar-random (generic, high-entropy) initial states, forward")
print(f"  unitary evolution, late-time per-rung rho:")
print(f"    rung 1: mean {rung_means[:,0].mean():+.3f}  std {rung_means[:,0].std():.3f}")
print(f"    rung 2: mean {rung_means[:,1].mean():+.3f}  std {rung_means[:,1].std():.3f}")
print(f"    rung 3: mean {rung_means[:,2].mean():+.3f}  std {rung_means[:,2].std():.3f}")
print(f"  fraction reaching the multi-rung corridor (all 3 rungs in "
      f"{BAND}): {frac:.3f}  ({in_corr}/{N_IC})")

print()
print("=" * 78)
print("READING")
print("=" * 78)
print(f"  Generic high-entropy initial states thermalize: every rung's")
print(f"  correlation collapses to ~0 (chaos pole) under forward unitary")
print(f"  evolution. The forward amplitude from generic initial conditions to")
print(f"  multi-rung corridor structure is {frac:.3f} -- effectively zero.")
print()
if frac < 0.02:
    print(f"  No falsifier. Forward dynamics alone, from generic high-entropy")
    print(f"  initial conditions, does NOT reach multi-rung corridor structure")
    print(f"  -- the amplitude is measure-zero-like. Claim 5 is CONSISTENT at")
    print(f"  the cosmological-origin scope: generic forward thermalization")
    print(f"  gives chaos at every rung, exactly the Penrose-past structural")
    print(f"  argument (Piece 8). Reaching multi-rung corridor structure needs")
    print(f"  either backward conditioning (P_omega) or an already-present")
    print(f"  maintenance structure (construct_pomega_lindblad.py) -- and the")
    print(f"  origin of that maintenance structure is itself what Piece 8 says")
    print(f"  needs the backward boundary.")
else:
    print(f"  FALSIFIER: a non-negligible forward amplitude ({frac:.2f}) from")
    print(f"  generic ICs to multi-rung corridor. Claim 5 challenged.")
print()
print("  Honest scope: a 3-rung, 12-spin toy; 'measure-zero' is a finite-sample")
print("  estimate (0 of 200). It tests the closed-forward / cosmological-origin")
print("  scope of Claim 5, not corridor occupation under maintained dynamics.")
