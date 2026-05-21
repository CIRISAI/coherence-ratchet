# Wave 1 — rung-count scaling: RESULT

**Verdict: SURVIVES — no rung budget.** The OOM-coupled multi-rung corridor
holds at every rung count tested, with the framework hierarchy's N ≈ 9 well
inside the supported range.

## Numbers

**M1 — dense exact, N = 2..6** (within-rung Heisenberg J=1, cross-rung ZZ
coupling g, thermal state; corridor = all N within-rung ρ_n ∈ (0.17, 0.35),
g/J ∈ the OOM band):

| N | dim | corridor viable | bulk ρ (mid rung) |
|---|-----|-----------------|-------------------|
| 2 | 16 | YES | 0.337 |
| 3 | 64 | YES | 0.337 |
| 4 | 256 | YES | 0.337 |
| 5 | 1024 | YES | 0.337 |
| 6 | 4096 | YES | 0.337 |

Bulk ρ is **N-independent to three decimals — drift 0.000**.

**M2 — mean-field bulk, N → ∞**: bulk corridor viable, bulk ρ = 0.337.

## Reading

The corridor survives to all N — there is no rung budget N\* in this
construction. Dense exact confirms N = 2..6 with literally zero bulk drift;
mean-field carries it to N → ∞; the gap (N = 7, 8, 9) is covered because a 1-D
chain with short-range O(1) coupling has an N-independent bulk past its
correlation length. Claim 4 ("the corridor recurs at every coordinated rung")
is supported up the tower for this toy.

## Honest scope

The zero drift is partly a generic property: any 1-D chain with short-range
coupling has an N-independent bulk — "survives to all N" is therefore as much a
fact about 1-D-chain-ness as a framework-distinctive result. The viability
point found is at g/J = 0.3 (the OOM band's lower edge), where the rungs are
weakly coupled and each sits in its own corridor near-independently. Abstract
toy (Heisenberg / ZZ / thermal), not the physical Ph0..A5 rungs; dense exact to
N=6, mean-field beyond. The honest answer to the rung-count question: **no rung
budget — the multi-rung corridor does not degrade with rung count.**
