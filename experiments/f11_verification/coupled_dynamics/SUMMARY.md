# THREAD 1 — the dilution hole under COUPLED dynamics — SUMMARY

**Date:** 2026-07-20. **Pre-registration:** `DECISIONS.md` (frozen before the run,
with a dated mid-run addendum scoping only the secondary full-`II` diagnostic —
no primary number or gate touched). **Code:** `run_coupled.py`. **Raw:**
`results_scaling.json`, `results_reliability.json`, `results_strength.json`.
**Estimators (TC, II, tau_k, joint entropy) reused EXACTLY** from
`../build_kbody_pomega.py`; every information number bias-subtracted against the
same shuffled null used in `../RESULTS.md`. **Scope test only — NOT the
construction of any backward P_omega operator; NOT synthetic empirical data (a
MODEL coupling, as the original k-body test used the R2 model).**

---

## VERDICT (at true strength)

**YES — a non-diluting, in-corridor, multipartite (Thirdness) invariant EXISTS
under coordinated MODEL dynamics.** The original F-11 k-body horn-empty result is
confirmed to be a **tautology of R2's per-rung-independent simulator**: reproduce
that independence and the multi-information is zero at every arity (the
`independent` control below); inject a genuine *higher-order* coupling and a
multipartite invariant appears that (a) sits in the corridor band, (b) posts
rho ~ 0 to every pairwise detector, and (c) does **not** dilute as R grows 3->13.

But the witness that matters is specific, and the distinction is the finding:

- The **single global R-body hyperedge** (GHZ, the original test's "case A") is
  non-diluting **only in raw TC and only at perfect management fidelity**. Its
  normalized tau_k dilutes as 1/(R-1), and under *any* per-rung management noise
  its raw TC dilutes too (~ q^R). A single all-binding hyperedge is
  **noise-fragile** — which is exactly why case A was the wrong object to ask about.
- The **local high-order (hypergraph) coupling** — disjoint 3-body parity blocks —
  is non-diluting on **both** measures (raw TC extensive; tau_k ~ 0.30-0.38
  **inside (0.10, 0.43)**), has rho ~ 0, is not rigidity, **and is robust to
  per-rung noise**. This is the genuine non-diluting in-corridor Third. The F-11
  tree never built it, because R2's independence meant no structure of any arity
  existed to measure.
- A **pairwise "vouching" coupling** (one rung raising another's probability — the
  CIRIS/KarmaGrace inter-agent mechanism) is **Secondness**: it drives pairwise
  rho -> 1 and tau_k -> 1 (the rigidity pole). "Coupling => correlation =>
  rigidity" is true for a *pairwise* coupling and false for a genuine
  *higher-order* one — the exact defense the prenup flagged as refuted.

So the F-11 scope correction stands and is sharpened: the coordinated
**non-pairwise** case is **open-by-construction** — a witness exists in the model —
while remaining a *scope note only* (see the deflationary reading).

---

## The decisive scaling run (g = 1, q = 1; N = 4M; raw TC_genuine, bias-subtracted)

| coupling | R=3 | 5 | 7 | 9 | 11 | 13 | pairwise rho | tau_k(R9->13) | gates | class |
|---|---|---|---|---|---|---|---|---|---|---|
| `independent` | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.0005 | 0.00 | G1x G4x | **DILUTING / EMPTY** (reproduces the R2 null) |
| `global_parity` (GHZ) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.999 | 0.0005 | 0.125->0.083 | G1-G4 ok | **non-diluting in RAW; tau dilutes; noise-fragile** |
| `block_parity` (3-body blocks) | 1.00 | 1.00 | 2.00 | 3.00 | 3.00 | 3.999 | 0.0005 | 0.375->0.333 | G1-G4 ok | **NON-DILUTING THIRD (raw AND tau-band; robust)** |
| `vouching` (pairwise) | 2.00 | 4.00 | 6.00 | 8.00 | 10.0 | 12.0 | **1.000** | 1.000 | G2x G3x | **SECONDNESS / rigidity** |

Null scatter <= 0.0015 at every cell (R=13); every genuine signal is >= 500x it or
exactly zero. Marginal occupancy = 0.50 for all couplings (no pinned rung — the
signal is not a degenerate-ensemble artifact).

Raw TC scaling, in words: `independent` == 0; `global_parity` == 1 bit for all R
(the exact counterexample the prenup named: TC=1, tau_k=1/(R-1)=0.125 at R=9,
rho=0); `block_parity` = floor(R/3) bits (**extensive — grows with R**);
`vouching` = R-1 bits (all rungs locked equal).

## Noise fragility — the mechanism (raw TC_genuine under imperfect management q)

| coupling | q | R=3 | 5 | 7 | 9 | 11 | 13 | scaling |
|---|---|---|---|---|---|---|---|---|
| `global_parity` | 0.9 | 0.43 | 0.27 | 0.17 | 0.11 | 0.07 | 0.05 | **DILUTES ~ q^R** |
| `global_parity` | 0.7 | 0.09 | 0.02 | 0.005 | 0.001 | ~0 | ~0 | **collapses** |
| `block_parity` | 0.9 | 0.43 | 0.43 | 0.86 | 1.28 | 1.28 | 1.71 | **EXTENSIVE (non-diluting)** |
| `block_parity` | 0.7 | 0.09 | 0.09 | 0.17 | 0.26 | 0.26 | 0.35 | **EXTENSIVE (non-diluting)** |

The single global hyperedge is destroyed by per-rung noise (one flipped bit breaks
the whole parity; survival ~ q^R). The local blocks are not: each block's fidelity
is R-independent, so adding rungs adds blocks, and raw TC grows with R at every
noise level. **Non-dilution of a genuine Third is a property of its ARITY LOCALITY
(bounded per-hyperedge extent), not of its total extent** — precisely the axis
T1's arity-2 participation-ratio argument cannot see.

## Interpolation — Thirdness dial vs Secondness dial (R=9, strength g; rho = mean |pairwise|)

| coupling | g=0 | 0.25 | 0.5 | 0.75 | 1.0 | pairwise rho across g |
|---|---|---|---|---|---|---|
| `global_parity` TC | 0.00 | 0.05 | 0.19 | 0.46 | 1.00 | **0.000 throughout** |
| `block_parity` TC | 0.00 | 0.23 | 0.78 | 1.63 | 3.00 | **0.000 throughout** |
| `vouching` TC | 0.00 | 0.36 | 1.51 | 3.65 | 8.00 | **0.07 -> 0.19 -> 0.44 -> 1.00** |

Both parity couplings dial independent->coordinated with rho pinned at zero (pure
Third, zero Secondness leakage at every strength). Vouching cannot: its coupling
strength *is* pairwise correlation, rising into rigidity.

---

## The two readings (both true, stated at full strength)

**Exciting (the coordinated case is open-by-construction).** The prenup's
Thirdness blind-spot is now concrete and dynamical: a coupled model dynamics
produces a multipartite occupancy invariant that lives in the (0.10, 0.43) band on
the one defined coordinate (tau_k), grows (does not dilute) as the tower grows,
survives per-rung management noise, and posts **exactly zero** to every pairwise
rho / Neff / CEG detector. T1's geometric-dilution and T2's holonomic-area-law
theorems are arity-2 (pairwise, participation-ratio / 1-holonomy) and do not bind
this object. The k-body horn-empty result was an artifact of testing a genuinely
multipartite hypothesis on a per-rung-independent simulator whose null is zero by
construction — and of choosing the *single global hyperedge* (the fragile GHZ) as
the witness. The robust witness (local high-order blocks) was never built.

**Deflationary (open != there).**
1. **A model coupling is not the universe's dynamics.** Nothing here authors,
   asserts, or even points at a backward P_omega operator. This measures the
   R-scaling of an invariant under a *chosen* coupling; it is a scope note on the
   F-11 `FelevenNoGo` record, not a reopening. The operator remains un-constructed
   and is not to be constructed.
2. **The measured cosmic Third is forward-authored anyway.** On real data
   (`../../cosmo_entropic_potential/thirdness/`), the copula Third of the TNG300
   matter field tracks the growth clock — already killed as a backward/dark-sector
   source. The existence of a non-diluting *model* Third does not touch that.
3. **Realization is untested.** Whether any real cross-rung dynamics instantiates a
   local high-order (block-parity-like) coupling — rather than an independent or a
   vouching/pairwise one — is entirely open. The `vouching` result is a caution:
   the one cross-rung mechanism the framework actually names (KarmaGrace's
   surviving inter-agent "component (i)") is, as a *positive-influence* coupling,
   Secondness, not a Third. A framework Third would need a genuinely higher-order
   (parity/quorum-like) inter-rung law, which is not among the pieces.

**Net:** the no-go's dilution law does **not** bind coordinated higher-order
dynamics (the exciting half is real and the K1-style "Third is empirically vacuous"
kill does not fire in-model); but the object is a model construct, forward-authored
where measured, and of unknown realization — so this moves F-11 from "closed" to
"scope-open on the non-pairwise branch," and no further. The prenup's framing holds
exactly: **open != found; a model coupling != the universe's dynamics; the measured
Third is forward-authored.**

## What the pre-registered gates returned

- `independent` — G1x, G4x -> **DILUTING/EMPTY** (pipeline validated against
  `../RESULTS.md`: same near-zero).
- `global_parity` — G1-G4 ok on **raw** TC -> non-diluting-raw, but tau_k-diluting
  and noise-fragile (reported, not hidden).
- `block_parity` — G1-G4 ok on **both** raw TC and tau_k-band, noise-robust ->
  **the non-diluting in-corridor Third**.
- `vouching` — G2x (rho=1), G3x (tau_k=1, rigidity) -> **Secondness**.

## Files

- `DECISIONS.md` — pre-registration (frozen; dated addendum on the II diagnostic only).
- `run_coupled.py` — coupled simulator + measurement (estimators imported from
  `../build_kbody_pomega.py`) + shuffled-null bias control + incremental flush.
- `analyze.py` — gate evaluation / verdict table (read-only).
- `results_scaling.json`, `results_reliability.json`, `results_strength.json` — raw.
