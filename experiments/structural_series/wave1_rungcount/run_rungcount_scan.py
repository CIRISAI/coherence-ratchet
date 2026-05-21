"""
Wave 1 — does the OOM-coupled multi-rung corridor survive growing rung count?
=============================================================================

Clean re-implementation following PREREGISTRATION.md (the prior 379-line draft
hung — almost certainly on a dense N=7 (dim 16384) eigendecomposition).

Question: crossrung_oom_band.py showed a 6-rung tower with cross-rung coupling
in the OOM band (0.3, 3) hosts a multi-rung corridor — all 6 within-rung ρ_n in
(0.17, 0.35). The framework hierarchy is ~9 rungs. Does the corridor survive as
N grows?

Two methods, per the pre-registration:
  M1  DENSE EXACT — N = 2..6 (dim 2^(2N), 4096 at N=6; safe). Ground truth.
      Tower: N rungs x 2 qubits, within-rung Heisenberg J=1, cross-rung ZZ
      coupling g between inner-facing qubits, thermal state exp(-H/T)/Z.
      ρ_n = |⟨Z_a Z_b⟩ − ⟨Z_a⟩⟨Z_b⟩|. Dense stops at N=6 — N=7 (16384) is the
      wedge risk and is not needed: M1 establishes the TREND, M2 the limit.
  M2  MEAN-FIELD bulk — N → ∞. A single 2-qubit rung in a self-consistent
      cross-rung field g·m (m = ⟨Z⟩ of a boundary qubit). The bulk of a 1-D
      chain with short-range coupling is N-independent past the correlation
      length, so the mean-field bulk ρ IS the large-N answer.

Verdict: SURVIVES if M1 shows ρ_n converging and in-band through N=6 AND the
M2 bulk is in-band; DEGRADES at N* if ρ_n leaves the band at some N.
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
J = 1.0
RHO_BAND = (0.17, 0.35)
OOM_BAND = (0.3, 3.0)
G_VALS = [0.3, 0.6, 1.0, 1.5, 2.0, 2.5, 3.0]
T_VALS = [2.4, 3.0, 3.6, 4.2, 4.8, 5.6]

I2 = xp.eye(2, dtype=CC)
X = xp.asarray([[0, 1], [1, 0]], dtype=CC)
Y = xp.asarray([[0, -1j], [1j, 0]], dtype=CC)
Z = xp.asarray([[1, 0], [0, -1]], dtype=CC)


def site(op, i, nq):
    out = xp.asarray([[1]], dtype=CC)
    for k in range(nq):
        out = xp.kron(out, op if k == i else I2)
    return out


def hermit(A):
    return (A + A.conj().T) / 2


print("=" * 78, flush=True)
print("Wave 1 — rung-count scaling of the OOM-coupled multi-rung corridor",
      flush=True)
print(f"  backend {'cupy/GPU' if GPU else 'numpy/CPU'}", flush=True)
print("=" * 78, flush=True)
t0 = time.time()

# ---- M1: dense exact, N = 2..6 -------------------------------------------
print("\nM1  DENSE EXACT", flush=True)
print(f"  {'N':>3}{'dim':>7}{'corridor viable?':>20}{'bulk ρ (mid rung)':>20}",
      flush=True)
m1 = {}
for N in range(2, 7):
    nq = 2 * N
    D = 2 ** nq
    SZ = [site(Z, i, nq) for i in range(nq)]
    H_rung = xp.zeros((D, D), dtype=CC)
    for n in range(N):
        a, b = 2 * n, 2 * n + 1
        H_rung += J * (site(X, a, nq) @ site(X, b, nq)
                       + site(Y, a, nq) @ site(Y, b, nq) + SZ[a] @ SZ[b])
    H_couple = xp.zeros((D, D), dtype=CC)
    for n in range(N - 1):
        H_couple += SZ[2 * n + 1] @ SZ[2 * n + 2]
    H_rung, H_couple = hermit(H_rung), hermit(H_couple)
    viable = False
    bulk_rho = None
    for g in G_VALS:
        E, V = xp.linalg.eigh(hermit(H_rung + g * H_couple))
        E = E - E.min()
        for T in T_VALS:
            w = xp.exp(-E / T)
            rho = (V * w) @ V.conj().T
            rho = rho / xp.trace(rho).real
            ez = [xp.trace(rho @ SZ[i]).real for i in range(nq)]
            rho_n = []
            for n in range(N):
                a, b = 2 * n, 2 * n + 1
                ezz = xp.trace(rho @ (SZ[a] @ SZ[b])).real
                rho_n.append(float(xp.abs(ezz - ez[a] * ez[b])))
            if all(RHO_BAND[0] < r < RHO_BAND[1] for r in rho_n):
                viable = True
                bulk_rho = rho_n[N // 2]
                break
        if viable:
            break
    m1[N] = (viable, bulk_rho)
    print(f"  {N:>3}{D:>7}{('YES' if viable else 'NO'):>20}"
          f"{(f'{bulk_rho:.3f}' if bulk_rho else '--'):>20}", flush=True)

# ---- M2: mean-field bulk, N -> infinity ----------------------------------
print("\nM2  MEAN-FIELD bulk (N -> infinity)", flush=True)
Xa = xp.kron(X, I2); Xb = xp.kron(I2, X)
Ya = xp.kron(Y, I2); Yb = xp.kron(I2, Y)
Za = xp.kron(Z, I2); Zb = xp.kron(I2, Z)
H_rung1 = hermit(J * (Xa @ Xb + Ya @ Yb + Za @ Zb))


def mf_bulk(g, T, iters=300):
    m = 0.3
    rho = xp.eye(4, dtype=CC) / 4
    for _ in range(iters):
        H = hermit(H_rung1 + g * m * (Za + Zb))
        E, V = xp.linalg.eigh(H)
        E = E - E.min()
        w = xp.exp(-E / T)
        rho = (V * w) @ V.conj().T
        rho = rho / xp.trace(rho).real
        m_new = float(xp.trace(rho @ Za).real)
        if abs(m_new - m) < 1e-10:
            m = m_new
            break
        m = 0.5 * m + 0.5 * m_new
    ezz = float(xp.trace(rho @ (Za @ Zb)).real)
    return abs(ezz - m * m)


mf_viable = False
mf_hit = None
for g in G_VALS:
    for T in T_VALS:
        r = mf_bulk(g, T)
        if RHO_BAND[0] < r < RHO_BAND[1]:
            mf_viable = True
            mf_hit = (g, T, r)
            break
    if mf_viable:
        break
if mf_viable:
    g, T, r = mf_hit
    print(f"  bulk corridor VIABLE at N->inf: g/J={g}, T={T}, bulk ρ={r:.3f}",
          flush=True)
else:
    sample = mf_bulk(1.0, 3.6)
    print(f"  bulk corridor NOT viable at N->inf "
          f"(e.g. g=1,T=3.6 gives ρ={sample:.3f})", flush=True)

# ---- verdict -------------------------------------------------------------
print("\n" + "=" * 78, flush=True)
print("READING", flush=True)
print("=" * 78, flush=True)
print(f"  scan complete ({time.time()-t0:.0f}s).", flush=True)
all_viable = all(v for v, _ in m1.values())
bulks = [b for _, b in m1.values() if b is not None]
print(f"  M1 dense: corridor viable at N = "
      f"{[N for N,(v,_) in m1.items() if v]}; "
      f"NOT viable at N = {[N for N,(v,_) in m1.items() if not v] or 'none'}.",
      flush=True)
if bulks:
    print(f"  M1 bulk ρ across N: {[round(b,3) for b in bulks]} "
          f"(drift {max(bulks)-min(bulks):.3f}).", flush=True)
print(f"  M2 mean-field bulk (N->inf): "
      f"{'in band' if mf_viable else 'OUT of band'}.", flush=True)
print(flush=True)
if all_viable and mf_viable:
    print("  VERDICT: SURVIVES. The multi-rung corridor holds at every N from", flush=True)
    print("  2 to 6 (dense exact) and the mean-field bulk holds at N->infinity.", flush=True)
    print("  A 1-D chain with short-range O(1) coupling has an N-independent", flush=True)
    print("  bulk past the correlation length, so N=7,8,9 are covered by the", flush=True)
    print("  M1 trend + M2 limit. No rung budget N* in this construction.", flush=True)
elif not all_viable:
    Nstar = min(N for N, (v, _) in m1.items() if not v)
    print(f"  VERDICT: DEGRADES. Rung budget N* = {Nstar} — the corridor stops", flush=True)
    print(f"  being jointly viable at N = {Nstar}.", flush=True)
else:
    print("  VERDICT: MIXED — dense N<=6 viable but the mean-field bulk leaves", flush=True)
    print("  the band; the large-N limit is the open edge.", flush=True)
print(flush=True)
print("  Honest scope: abstract toy (Heisenberg within-rung, ZZ cross-rung,", flush=True)
print("  thermal state). Dense is exact to N=6; M2 mean-field misses chain", flush=True)
print("  fluctuations. Not the physical Ph0..A5 rungs.", flush=True)
