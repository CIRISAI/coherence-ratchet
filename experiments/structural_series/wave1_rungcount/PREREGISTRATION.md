# Wave 1 — rung-count scaling of the OOM-coupled multi-rung corridor

**Pre-registered:** 2026-05-21. Committed BEFORE any results.

## The question

`crossrung_oom_band.py` showed that with the cross-rung coupling held in the
OOM band `g/J ∈ (0.3, 3)`, an abstract 6-rung tower hosts a multi-rung
corridor — all 6 within-rung corridors `ρ_n` co-hold — across the whole band.
The framework's rung hierarchy (Ph0…A5) is ~9 rungs. Two outcomes:

- **Survives at all N** → the multi-rung corridor is fractal-recurrent at the
  cross-rung level under OOM coupling. Claim 4 (`StructuralClaims.lean`,
  "the corridor recurs at every coordinated rung") is supported up the tower.
- **Degrades at some N\*** → there is a rung budget. Report N\* and the
  numbers — Claim 4 would fail above N\*.

"Survives to N ≳ 9" is the bar, since the framework hierarchy is 9 rungs.

## Tower construction

A 1-D chain of N rungs. Each rung is 2 qubits with a within-rung Heisenberg
bond (the original `crossrung_tower_scan.py` within-rung structure):

```
H_rung,n = J (X_a X_b + Y_a Y_b + Z_a Z_b),   a = 2n, b = 2n+1,  J = 1
```

Adjacent rungs are coupled by a ZZ bond between the inner-facing qubits:

```
H_couple = g Σ_{n=0}^{N-2} Z_{2n+1} Z_{2n+2}
H(g) = Σ_n H_rung,n + H_couple
```

State: thermal `ρ(T) = exp(-H/T)/Z` — the steady state of a temperature-T
bath, T the decoherence knob (identical to `crossrung_oom_band.py`).

Per-rung readout — within-rung corridor coordinate:

```
ρ_n = |⟨Z_a Z_b⟩ − ⟨Z_a⟩⟨Z_b⟩|   (connected ZZ correlator of rung n)
```

This is exactly the `crossrung_oom_band.py` readout, so results are directly
comparable to its N=6 finding.

## Corridor criterion

Within-rung corridor band (A3+ recalibration, the band used by
`crossrung_oom_band.py` and `crossrung_tower_scan.py`):

```
RHO_BAND = (0.17, 0.35)
```

Cross-rung coupling held in the OOM band:

```
OOM_BAND = (0.3, 3.0)
```

The **multi-rung corridor holds** at a tower `(N, g, T)` iff `g/J ∈ OOM_BAND`
**and** every one of the N within-rung `ρ_n` lies strictly inside `RHO_BAND`.

For each `(N, g)` we scan a fixed temperature grid `T_VALS` and ask whether
ANY T makes all N within-rung corridors co-hold. (T is a free bath knob, as in
the prior runs — the question is corridor *existence* at given N, g.)

## Method for scaling N — three methods, stated limits

A 9-rung tower of 2-qubit rungs is 18 qubits, dim 2^18 = 262144. Dense `eigh`
on that is ~550 GB per matrix — infeasible. We use three methods and
cross-check them where they overlap:

### M1 — dense exact (N = 2…7)
Full `exp(-H/T)/Z` by dense eigendecomposition on the GPU. Dim 2^(2N); N=7 is
dim 16384 (~2 GB complex64), feasible on a 16 GB GPU. N=8 (dim 65536, ~32 GB)
is not. **Limit:** none — exact thermal state of the finite tower. This is the
ground truth for N ≤ 7.

### M2 — mean-field rung-chain (N = 2…40)
Self-consistent decoupling of the cross-rung ZZ bonds. Each cross-rung bond
`g Z_{2n+1} Z_{2n+2}` is replaced by its mean-field form
`g (Z_{2n+1}⟨Z_{2n+2}⟩ + ⟨Z_{2n+1}⟩Z_{2n+2} − ⟨Z⟩⟨Z⟩)`. The chain decouples
into per-rung 4-dim thermal problems coupled only through the boundary fields
`m = ⟨Z⟩` on the inner qubits; solved by fixed-point iteration to
self-consistency. `ρ_n` is read off each converged 4-dim rung.
**Limit:** mean-field neglects cross-rung *quantum* correlations and
fluctuations. It is exact in the infinite-coordination / weak-fluctuation
limit and is the standard honest large-N tool. It can under- or over-state
`ρ_n` relative to the exact tower; M2 is validated against M1 on N ≤ 7 and the
discrepancy is reported. M2 is the method that reaches N ≳ 9.

### M3 — operator-on-fixed-space tower (N = 2…40)
The `deadzone_rung_scaling.py` trick: hold the Hilbert space at a fixed
dimension D and grow the *number* of rung operators acting on it, with tunable
non-commutativity. Used as an independent stress test of whether *adding
rung-operators* alone (without growing the literal Hilbert space) degrades the
joint corridor. **Limit:** the rungs are operators on a shared space, not
genuine tensored subsystems — a model, and (for independent rungs) the worst
case for joint-corridor survival. M3 is a robustness check, not ground truth.

## What "survives" vs "degrades at N\*" means numerically

For each method, at each N from 6 upward, define the tower **corridor-viable**
at N iff there exists at least one `(g ∈ OOM_BAND, T ∈ T_VALS)` cell where all
N within-rung corridors co-hold.

- **SURVIVES**: the tower is corridor-viable for every N up to N_max (with
  N_max ≥ 9 for M2/M3, ≥ 7 for M1). The OOM-band multi-rung corridor is
  fractal-recurrent — no rung budget within reach.
- **DEGRADES at N\***: N\* is the smallest N at which the tower is NOT
  corridor-viable (no `(g,T)` cell in the OOM band co-holds all `ρ_n`). N\* is
  the rung budget. Report N\*, the failing `ρ_n`, and which method shows it.

A method-dependent split (e.g. M1/M2 survive, M3 degrades) is reported as
such and attributed to the method's stated limit, not hidden.

## Honest scope

Abstract toy tower, as in the prior cross-rung runs. The within-rung band is
session-calibrated; the OOM band is from 2 real rung pairs (Path 1). This is
Piece 6 (cross-rung corridor) made computable at large N — NOT a channel from
a cosmological P_ω to particle observables. The verdict bears on Claim 4's
fractal-recurrence form at the cross-rung level under OOM coupling.
