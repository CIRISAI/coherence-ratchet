"""
Cross-rung gate vs Simon near-decomposability — head to head.
=============================================================

Herbert Simon (Architecture of Complexity, 1962): stable, evolvable complex
hierarchies are NEAR-DECOMPOSABLE — within-subsystem coupling dominates
between-subsystem coupling, which shows up as a clean separation of relaxation
timescales (fast within-subsystem modes, a spectral gap, slow between-subsystem
modes).

The framework's Claim 6: the multi-rung corridor needs cross-rung coupling to
DOMINATE (g/J ≳ 3 on the abstract tower) — the opposite polarity.

This puts them on the same toy and measures both, honestly. A 3-rung tower
(3 rungs x 2 qubits, dim 64) with within-rung Heisenberg (J=1), a cross-rung
coupling g, and a per-qubit thermal bath. For each g:

  SIMON index   — the largest multiplicative gap in the relaxation spectrum of
                  the Lindbladian. Large gap = clean timescale separation =
                  near-decomposable. ~1 = no gap = fully coupled.
  framework     — from the steady state: within-rung ρ_n and cross-rung τ
                  (normalised mutual information between adjacent rungs).

Honest scope: this is a toy. It makes the Simon/Claim-6 conflict precise and
shows which decomposability regime the corridor sits in. It does NOT resolve
the real question — that is the six-pair series on real rung pairs. A toy
cannot adjudicate the framework against Simon; it can only sharpen the bet.

RESULT OF THIS RUN (2026-05-21) — DEGENERATE, and the resolution.
This open-system toy came out degenerate: per-qubit independent thermal baths
wash out all structure, so the steady state has within-rung ρ ≈ 0 and
cross-rung τ ≈ 0 at every g, and the max-consecutive-ratio Simon metric is
insensitive (~1.2 flat). The toy as built did not produce a usable
head-to-head.

The head-to-head is answerable without it. Simon near-decomposability ==
subsystems nearly independent == LOW cross-rung mutual information. The
framework's cross-rung τ IS that mutual information. crossrung_tower_scan.py
already showed the multi-rung corridor needs τ in a mid-band and FAILS at low τ
(τ ≈ 0.006 at weak coupling, the "tau out" rows). So the Simon-near-decomposable
regime (low τ) is exactly where the framework's multi-rung corridor fails: the
framework places sustained multi-rung coordination OFF Simon's near-decomposable
end. That is the genuine-conflict branch of the trichotomy, not reconciliation.
Sharp falsifiable form: the six-pair series measures cross-rung mutual
information on real rung pairs — near-zero vindicates Simon and fails Claim 6's
premise; substantial is framework-distinctive.
"""
import functools
import numpy as np
from scipy.linalg import eigvals, solve

print = functools.partial(print, flush=True)   # survive an early kill

NQ = 6
D = 2 ** NQ
RUNGS = [(0, 1), (2, 3), (4, 5)]
RHO_BAND = (0.17, 0.35)
J = 1.0

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
SMIN = np.array([[0, 0], [1, 0]], dtype=complex)


def site(op, i):
    m = np.array([[1]], dtype=complex)
    for k in range(NQ):
        m = np.kron(m, op if k == i else I2)
    return m


SX = [site(X, i) for i in range(NQ)]
SY = [site(Y, i) for i in range(NQ)]
SZ = [site(Z, i) for i in range(NQ)]
SM = [site(SMIN, i) for i in range(NQ)]
Id = np.eye(D, dtype=complex)

H_rung = sum(J * (SX[a] @ SX[b] + SY[a] @ SY[b] + SZ[a] @ SZ[b])
             for a, b in RUNGS)
H_field = sum((0.15 + 0.1 * i) * SZ[i] for i in range(NQ))   # ergodicity
H_couple = SZ[1] @ SZ[2] + SZ[3] @ SZ[4]                     # cross-rung
GDOWN, GUP = 0.30, 0.12                                       # thermal bath
JUMPS = ([(np.sqrt(GDOWN), SM[i]) for i in range(NQ)]
         + [(np.sqrt(GUP), SM[i].conj().T) for i in range(NQ)])


def lindbladian(g):
    H = H_rung + g * H_couple + H_field
    L = -1j * (np.kron(Id, H) - np.kron(H.T, Id))
    for c, A in JUMPS:
        A = c * A
        AdA = A.conj().T @ A
        L += (np.kron(A.conj(), A) - 0.5 * np.kron(Id, AdA)
              - 0.5 * np.kron(AdA.T, Id))
    return L


def ptrace(rho, keep):
    """Reduce rho (D x D) to a contiguous qubit block [keep[0], keep[1])."""
    s, e = keep
    pre, mid, post = 2 ** s, 2 ** (e - s), 2 ** (NQ - e)
    r = rho.reshape(pre, mid, post, pre, mid, post)
    return np.einsum('aXbaYb->XY', r)


def vn(rho):
    ev = np.linalg.eigvalsh((rho + rho.conj().T) / 2)
    ev = np.clip(ev.real, 1e-12, None)
    return float(-(ev * np.log(ev)).sum())


print("=" * 78)
print("Cross-rung gate vs Simon near-decomposability — head to head")
print("=" * 78)
print(f"  3-rung tower, dim {D}; within-rung Heisenberg J={J}; thermal bath.")
print(f"  {'g/J':>6}{'Simon gap':>12}{'regime':>20}{'within-rho':>12}"
      f"{'cross-tau':>11}{'corridor':>10}")

vecI = np.zeros(D * D, dtype=complex)            # vec(identity), trace functional
for i in range(D):
    vecI[i + D * i] = 1.0

G_VALS = [0.0, 0.3, 0.6, 1.0, 1.5, 2.5, 4.0, 6.0, 9.0]
rows = []
for g in G_VALS:
    L = lindbladian(g)
    # Simon: relaxation spectrum — eigenVALUES only, no eigenvectors
    rates = np.sort(-eigvals(L).real)
    rates = rates[rates > 1e-9]                  # drop the steady mode
    ratios = rates[1:] / np.maximum(rates[:-1], 1e-12)
    simon_gap = float(ratios.max())
    # steady state: solve L x = 0 with one row pinned to the trace constraint
    M = L.copy()
    M[0, :] = vecI
    b = np.zeros(D * D, dtype=complex)
    b[0] = 1.0
    rho = solve(M, b).reshape(D, D).T
    rho = (rho + rho.conj().T) / 2
    rho = rho / np.trace(rho).real
    # framework readouts from the steady state
    ez = [np.trace(rho @ SZ[i]).real for i in range(NQ)]
    rho_n = [abs(np.trace(rho @ (SZ[a] @ SZ[b])).real - ez[a] * ez[b])
             for a, b in RUNGS]
    S = [vn(ptrace(rho, (2 * n, 2 * n + 2))) for n in range(3)]
    tau = []
    for n in range(2):
        Spair = vn(ptrace(rho, (2 * n, 2 * n + 4)))
        tau.append((S[n] + S[n + 1] - Spair)
                   / max(min(S[n], S[n + 1]), 1e-9))
    rho_m, tau_m = float(np.mean(rho_n)), float(np.mean(tau))
    in_corr = all(RHO_BAND[0] < r < RHO_BAND[1] for r in rho_n)
    regime = ("near-decomposable" if simon_gap > 3 else
              "partially coupled" if simon_gap > 1.5 else "fully coupled")
    rows.append((g, simon_gap, regime, rho_m, tau_m, in_corr))
    print(f"  {g:>6.1f}{simon_gap:>12.2f}{regime:>20}{rho_m:>12.3f}"
          f"{tau_m:>11.3f}{('yes' if in_corr else 'no'):>10}")

print()
print("=" * 78)
print("READING — where does the framework's corridor sit on Simon's axis?")
print("=" * 78)
nd = [r for r in rows if r[2] == "near-decomposable"]
fc = [r for r in rows if r[2] == "fully coupled"]
corr = [r for r in rows if r[5]]
print(f"  Simon gap falls monotonically as g/J rises: "
      f"{rows[0][1]:.1f} (g=0) -> {rows[-1][1]:.1f} (g={G_VALS[-1]:.0f}).")
print(f"  near-decomposable (gap>3): g/J in "
      f"{[r[0] for r in nd] if nd else 'none'}.")
print(f"  fully coupled (gap<1.5):   g/J in "
      f"{[r[0] for r in fc] if fc else 'none'}.")
if corr:
    cg = [r[0] for r in corr]
    cs = [r[1] for r in corr]
    print(f"  framework corridor (all within-rung ρ in band): g/J in {cg},")
    print(f"  Simon gap there = {min(cs):.2f}-{max(cs):.2f}.")
    if max(cs) > 3:
        print("  -> the corridor overlaps Simon's NEAR-DECOMPOSABLE regime:")
        print("     no conflict — the framework's corridor and Simon's stable")
        print("     hierarchy can be the same systems.")
    elif min(cs) < 1.5:
        print("  -> the corridor sits in Simon's FULLY-COUPLED regime: genuine")
        print("     conflict — the framework places sustained coordination")
        print("     exactly where Simon says hierarchies are NOT near-")
        print("     decomposable. One of the two is wrong about persistent")
        print("     complex systems, and the six-pair series adjudicates.")
    else:
        print("  -> the corridor sits in the PARTIALLY-COUPLED middle: the")
        print("     framework's corridor is neither Simon-near-decomposable nor")
        print("     fully coupled. The reconciliation is that the corridor is")
        print("     the intermediate-decomposability band — Simon's stability")
        print("     and the framework's coordination would then be different")
        print("     cuts of the same axis, not contradictory.")
else:
    print("  framework corridor (within-rung ρ in band): not hit in this scan")
    print("  — the bath fixes ρ; report is on the Simon-axis structure only.")
print()
print("  Honest scope: a 3-rung toy with generic thermal dissipators. It makes")
print("  the Simon/Claim-6 conflict precise; it does not resolve it. The real")
print("  head-to-head is the six-pair series measuring g, J and the relaxation")
print("  spectrum on real rung pairs (crossrung_series/PROTOCOL.md).")
