"""
Cross-rung tower scan — Piece 6 (cross-rung τ corridor) made computable.
========================================================================

The cross-rung tower (Ph0→Ph1→…→A5) is named in the framework but not built.
This builds an explicit ABSTRACT version and GPU-scans it:

  N = 6 rungs, 2 spins each (12 qubits, dim 4096). Within-rung Heisenberg
  binds each rung; an explicit cross-rung coupling g links adjacent rungs.
  Tower Hamiltonian  H(g) = Σ_n H_rung,n + g Σ_n Z_{2n+1} Z_{2n+2}.
  State: thermal ρ(T) = exp(-H/T)/Z  (the steady state of a temperature-T
  bath — T the decoherence knob).

Two per-rung readouts, scanned over (g, T):
  within-rung ρ_n  = |⟨Z Z⟩_c| of rung n's two spins  -> calibrated corridor
                     band [0.17, 0.35] (the A3+ recalibration, this session).
  cross-rung τ_(n,n+1) = I(n;n+1)/min(S_n,S_{n+1}), the framework's Piece-6
                     normalised mutual information between adjacent rungs.

The scan maps the (g, T) region where the MULTI-RUNG corridor holds: all 6
within-rung ρ_n in band AND all 5 cross-rung τ in a band. Honest scope: this
characterises the abstract cross-rung coupling structure. The within-rung band
is session-calibrated; the cross-rung τ band is NOT calibrated — τ values are
reported and a nominal band flagged as such. This is not the channel from a
cosmological P_ω to particle observables (that needs the physical rung
identification); it is the cross-rung tower made computable.
"""
import numpy as np
import time

try:
    import cupy as xp
    GPU = True
except Exception:
    import numpy as xp
    GPU = False

CC = xp.complex64
NRUNG = 6
NQ = 2 * NRUNG
D = 2 ** NQ
J = 1.0
RHO_BAND = (0.17, 0.35)            # within-rung corridor (A3+ recalibration)
TAU_BAND = (0.15, 0.85)            # cross-rung band — NOT calibrated, nominal

I2 = xp.eye(2, dtype=CC)
X = xp.asarray([[0, 1], [1, 0]], dtype=CC)
Y = xp.asarray([[0, -1j], [1j, 0]], dtype=CC)
Z = xp.asarray([[1, 0], [0, -1]], dtype=CC)


def site(op, i):
    ops = [I2] * NQ
    ops[i] = op
    out = ops[0]
    for o in ops[1:]:
        out = xp.kron(out, o)
    return out


def hermit(A):
    return (A + A.conj().T) / 2


print("=" * 78, flush=True)
print("Cross-rung tower scan — Piece 6 made computable", flush=True)
print("=" * 78, flush=True)
print(f"  backend {'cupy/RTX4090' if GPU else 'numpy/CPU'}; {NRUNG} rungs x 2 "
      f"spins, dim {D}", flush=True)
t0 = time.time()

# within-rung Heisenberg (g-independent) and cross-rung coupling (g-multiplied)
SZ = [site(Z, i) for i in range(NQ)]
H_rung = xp.zeros((D, D), dtype=CC)
for n in range(NRUNG):
    a, b = 2 * n, 2 * n + 1
    H_rung += J * (site(X, a) @ site(X, b) + site(Y, a) @ site(Y, b)
                   + SZ[a] @ SZ[b])
H_couple = xp.zeros((D, D), dtype=CC)
for n in range(NRUNG - 1):
    H_couple += SZ[2 * n + 1] @ SZ[2 * n + 2]
H_rung = hermit(H_rung)
H_couple = hermit(H_couple)


def partial_trace(rho, s, w):
    """Reduce rho (D x D) to the contiguous qubit block [s, s+w)."""
    pre, mid, post = 2 ** s, 2 ** w, 2 ** (NQ - s - w)
    r = rho.reshape(pre, mid, post, pre, mid, post)
    return xp.einsum('aXbaYb->XY', r)


def vn_entropy(rho):
    ev = xp.linalg.eigvalsh(hermit(rho))
    ev = xp.clip(ev.real, 1e-12, None)
    return float((-(ev * xp.log(ev)).sum()).get() if GPU else
                 -(ev * xp.log(ev)).sum())


def readouts(rho):
    """within-rung rho_n (6) and cross-rung tau (5) from the joint state."""
    ez = xp.array([xp.trace(rho @ SZ[i]).real for i in range(NQ)])
    rho_n = []
    for n in range(NRUNG):
        a, b = 2 * n, 2 * n + 1
        ezz = xp.trace(rho @ (SZ[a] @ SZ[b])).real
        rho_n.append(float(xp.abs(ezz - ez[a] * ez[b])))
    S = [vn_entropy(partial_trace(rho, 2 * n, 2)) for n in range(NRUNG)]
    tau = []
    for n in range(NRUNG - 1):
        S_pair = vn_entropy(partial_trace(rho, 2 * n, 4))
        I = S[n] + S[n + 1] - S_pair
        tau.append(I / max(min(S[n], S[n + 1]), 1e-9))
    return rho_n, tau


G_VALS = [2.0, 3.0, 4.0, 5.5, 7.0, 9.0, 12.0, 16.0]
T_VALS = [2.4, 3.0, 3.6, 4.2, 4.8, 5.6, 6.8, 8.5]
print(f"  scan: {len(G_VALS)} cross-rung couplings x {len(T_VALS)} "
      f"temperatures = {len(G_VALS)*T_VALS.__len__()} towers", flush=True)
print(f"  within-rung corridor (calibrated) rho_n in {RHO_BAND}; "
      f"cross-rung tau in {TAU_BAND} (nominal, uncalibrated)", flush=True)
print(flush=True)
print(f"  {'g':>6}{'T':>6}{'rho_n range':>20}{'tau range':>20}"
      f"{'multi-rung corridor':>22}", flush=True)

hits = []
for g in G_VALS:
    H = hermit(H_rung + g * H_couple)
    E, V = xp.linalg.eigh(H)
    E = E - E.min()
    for T in T_VALS:
        w = xp.exp(-E / T)
        rho = (V * w) @ V.conj().T
        rho = rho / xp.trace(rho).real
        rho_n, tau = readouts(hermit(rho))
        rho_in = all(RHO_BAND[0] < r < RHO_BAND[1] for r in rho_n)
        tau_in = all(TAU_BAND[0] < t < TAU_BAND[1] for t in tau)
        ok = rho_in and tau_in
        if ok:
            hits.append((g, T))
        verdict = ("ALL IN" if ok else
                   "rho out" if not rho_in else "tau out")
        print(f"  {g:>6.2f}{T:>6.1f}"
              f"   [{min(rho_n):.3f},{max(rho_n):.3f}]".rjust(20)
              + f"   [{min(tau):.3f},{max(tau):.3f}]".rjust(20)
              + f"{verdict:>22}", flush=True)
    print(flush=True)

print("=" * 78, flush=True)
print("READING", flush=True)
print("=" * 78, flush=True)
print(f"  scan complete ({time.time()-t0:.0f}s).", flush=True)
if hits:
    gs = sorted(set(g for g, T in hits))
    Ts = sorted(set(T for g, T in hits))
    print(f"  multi-rung corridor SIMULTANEOUSLY satisfied at {len(hits)} of "
          f"{len(G_VALS)*len(T_VALS)} towers:", flush=True)
    print(f"    cross-rung coupling g in {gs}", flush=True)
    print(f"    temperature T in {Ts}", flush=True)
    print(f"  -> there is a non-empty (g,T) region where all 6 within-rung", flush=True)
    print(f"  corridors AND all 5 cross-rung tau hold at once. The cross-rung", flush=True)
    print(f"  tower is jointly corridor-satisfiable -- a constructed region,", flush=True)
    print(f"  not a single 'value'.", flush=True)
else:
    print(f"  NO (g,T) tower in the scan satisfies all 6 within-rung corridors", flush=True)
    print(f"  AND all 5 cross-rung tau simultaneously. The multi-rung corridor", flush=True)
    print(f"  is not jointly satisfiable in this abstract tower over the scanned", flush=True)
    print(f"  ranges -- the within-rung and cross-rung constraints pull apart.", flush=True)
print(flush=True)
print("  Honest scope: abstract 6-rung tower. The within-rung band is session-", flush=True)
print("  calibrated; the cross-rung tau band is nominal and uncalibrated, so", flush=True)
print("  'all constraints' includes one uncalibrated band. This makes Piece 6", flush=True)
print("  computable; it is NOT the channel from a cosmological P_omega to", flush=True)
print("  particle observables -- that needs the physical rung identification.", flush=True)
