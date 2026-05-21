"""
Cross-rung tower with the OOM band plugged in as the corridor width.
====================================================================

Path 1 (real data, 2 rung pairs) put the cross-rung/within-rung coupling ratio
at 0.3–3 — one order of magnitude, centred on parity g/J = 1. That is the
principled corridor width for the cross-rung coupling: O(1) coupling is the
existence condition for a stratified-and-integrated hierarchy, and one OOM is
the natural width of a non-fine-tuned bounded band on a log axis.

This re-runs the abstract tower with that band plugged in, REPLACING the
hand-picked nominal τ band of crossrung_tower_scan.py. The cross-rung corridor
is now g/J ∈ (0.3, 3). Question: where does the tower host a multi-rung
corridor — all 6 within-rung ρ_n in band AND g/J in the OOM band — and WHERE
in the OOM band does it sit? Real coordinated systems (Path 1) sit mid-band,
g/J ≈ 0.7–1.15.

Two within-rung structures are tried, to see what we can do:
  heisenberg — XX+YY+ZZ within each rung (the original tower).
  tfi        — transverse-field Ising, ZZ + transverse X (a softer, different
               within-rung structure).
If the original tower only hosts the corridor at the OOM band's top edge
(g/J ≈ 3) while a variant hosts it mid-band (g/J ≈ 1), that variant is the
tower made consistent with real coordinated systems.

RESULT (2026-05-21): the apparent toy-vs-data conflict DISSOLVED. The earlier
"tower needs g/J ≳ 3" (crossrung_tower_scan.py) was an ARTIFACT of that scan's
hand-picked nominal τ floor (0.15) — at low g the cross-rung mutual information
τ fell below 0.15 and the scan rejected it. With the cross-rung corridor set to
the PRINCIPLED OOM band on g/J directly, the within-rung corridors are
satisfiable across the WHOLE band g/J ∈ [0.3, 3], at appropriate T — both
within-rung structures (Heisenberg 28 cells, TFI 35), mid-band included. So the
tower is CONSISTENT with real coordinated systems at g/J ~ 1 (Path 1). It does
not uniquely PREDICT g/J ~ 1 — the structural argument (O(1) coupling is the
existence condition for a stratified-and-integrated hierarchy) and the real
data do that. The toy never needed g/J ≳ 3; the τ floor did.
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
OOM_BAND = (0.3, 3.0)              # cross-rung corridor — one OOM around parity

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
print("Cross-rung tower — OOM band (0.3, 3) plugged in as the corridor width",
      flush=True)
print("=" * 78, flush=True)
print(f"  backend {'cupy/GPU' if GPU else 'numpy/CPU'}; {NRUNG} rungs, dim {D}",
      flush=True)
t0 = time.time()

SX = [site(X, i) for i in range(NQ)]
SY = [site(Y, i) for i in range(NQ)]
SZ = [site(Z, i) for i in range(NQ)]

H_couple = xp.zeros((D, D), dtype=CC)
for n in range(NRUNG - 1):
    H_couple += SZ[2 * n + 1] @ SZ[2 * n + 2]
H_couple = hermit(H_couple)


def within_rung_H(variant):
    H = xp.zeros((D, D), dtype=CC)
    for n in range(NRUNG):
        a, b = 2 * n, 2 * n + 1
        if variant == "heisenberg":
            H += J * (SX[a] @ SX[b] + SY[a] @ SY[b] + SZ[a] @ SZ[b])
        else:  # tfi: transverse-field Ising
            H += J * (SZ[a] @ SZ[b]) + 1.0 * (SX[a] + SX[b]) / 2
    return hermit(H)


G_VALS = [0.3, 0.6, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
T_VALS = [2.4, 3.0, 3.6, 4.2, 4.8, 5.6, 6.8, 8.5]

for variant in ["heisenberg", "tfi"]:
    H_rung = within_rung_H(variant)
    print(flush=True)
    print(f"--- within-rung structure: {variant} ---", flush=True)
    print(f"  {'g/J':>6}{'T':>6}{'within-rho range':>22}{'g/J in OOM?':>14}"
          f"{'multi-rung corridor':>22}", flush=True)
    hits = []
    for g in G_VALS:
        H = hermit(H_rung + g * H_couple)
        E, V = xp.linalg.eigh(H)
        E = E - E.min()
        g_in_oom = OOM_BAND[0] <= g <= OOM_BAND[1]
        for T in T_VALS:
            w = xp.exp(-E / T)
            rho = (V * w) @ V.conj().T
            rho = rho / xp.trace(rho).real
            ez = [xp.trace(rho @ SZ[i]).real for i in range(NQ)]
            rho_n = []
            for n in range(NRUNG):
                a, b = 2 * n, 2 * n + 1
                ezz = xp.trace(rho @ (SZ[a] @ SZ[b])).real
                rho_n.append(float(xp.abs(ezz - ez[a] * ez[b])))
            rho_in = all(RHO_BAND[0] < r < RHO_BAND[1] for r in rho_n)
            ok = rho_in and g_in_oom
            if ok:
                hits.append((g, T))
            if rho_in:                       # only print the interesting rows
                print(f"  {g:>6.1f}{T:>6.1f}"
                      f"   [{min(rho_n):.3f},{max(rho_n):.3f}]".rjust(22)
                      + f"{('yes' if g_in_oom else 'NO'):>14}"
                      + f"{('ALL IN' if ok else 'g/J out of OOM'):>22}",
                      flush=True)
    if hits:
        gs = sorted(set(g for g, _ in hits))
        lo, hi = min(gs), max(gs)
        loc = ("TOP edge (g/J~3)" if lo >= 2.4 else
               "MID band (g/J~1)" if hi <= 1.6 else
               f"spread g/J {lo}-{hi}")
        print(f"  -> multi-rung corridor (OOM band) at {len(hits)} cells; "
              f"g/J in {gs} -- {loc}.", flush=True)
    else:
        print(f"  -> NO multi-rung corridor in the OOM band: this tower's "
              f"within-rung corridors never co-hold with g/J <= 3.", flush=True)

print(flush=True)
print("=" * 78, flush=True)
print("READING", flush=True)
print("=" * 78, flush=True)
print(f"  scan complete ({time.time()-t0:.0f}s).", flush=True)
print("  The OOM band (0.3, 3) is plugged in as the cross-rung corridor width.", flush=True)
print("  Real coordinated systems (Path 1) sit MID-band: g/J ~ 0.7-1.15.", flush=True)
print("  Where each tower variant hosts its multi-rung corridor inside the OOM", flush=True)
print("  band -- top edge vs mid -- is read off above. A variant that hosts it", flush=True)
print("  mid-band is the toy made consistent with the real-data coupling; a", flush=True)
print("  tower that only reaches the top edge over-couples vs real coordinated", flush=True)
print("  systems and needs a structurally different within-rung dynamics.", flush=True)
print("  Honest scope: abstract toy; within-rung band session-calibrated, OOM", flush=True)
print("  band from 2 real rung pairs. Not the channel to particle observables.", flush=True)
