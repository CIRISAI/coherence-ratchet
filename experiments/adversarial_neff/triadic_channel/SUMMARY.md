# Triadic-deception channel — does the second law cover the Third, and is the Third invisible?

**Date 2026-07-20.** THREAD 2 of the Third prenup (`papers/notes/the_third_prenup.md`),
prediction 3 / kill K3 — the safety blind-spot leg. Method + thresholds frozen in
`DECISIONS.md` before any number was computed. Code: `triadic_blindspot.py`; data:
`results.json`; Lean: `formal/CoherenceRatchet/Core/TriadicChannel.lean` (builds green,
`lake build CoherenceRatchet.Core.TriadicChannel` -> 1592/1592). No empirical data — constructed
distributions demonstrating a math fact (the XOR/GHZ witness generalized). Every information
estimate carries a shuffle null.

## Headline (both readings, at true strength)

- **PRONG A — the second law DOES cover the Third, CONDITIONALLY.** Multi-information /
  total correlation is **un-forgeable by any LOCAL operation** — a standard, cited theorem,
  and the un-forgeability route is relative-entropy DPI, **not** the Fischer's-inequality route
  `FourLaws.RestrictedSecondLaw` found blocked. The one condition, load-bearing and honest:
  **local ops only**. A genuinely joint operation *can* create coordination (XOR turns two
  independent bits, `TC = 0`, into parity, `TC = 1` bit) — that is a real shared cause, which
  is what coordination *is*, not a forgery.
- **PRONG B — the Third IS invisible to the pairwise floor. K3's blind-spot leg FIRES.** A
  purely-triadic coordination hides **~100% of its `I_total`** from the pairwise Neff/S/rho-bar
  detector, which reads not merely "blind" but **`Neff_PR = n` (MAXIMAL independence — the
  safest possible verdict)**, `rho-bar = 0`, `S/2 = 0`, at every noise level. Both the linear and the
  **copula** `S` (the exact object the DE pipeline reads) are blind. The blind spot is
  structural (`thirdness_line`: `I_total` is not a functional of `C`), not finite-sample.

**One line:** the coordination is un-forgeable in the QUANTITY and invisible in the
INSTRUMENT — two independent facts. The pairwise safety floor is **not** triadically complete;
the fix is a multi-information instrument, and the coordination it would read is provably real.

---

## PRONG A — does the DPI extend to the full `I_total`? (analysis + Lean)

**Object.** Total correlation (multi-information) is a relative entropy:
`TC(X1,...,Xn) = sum_i H(Xi) - H(X) = D(P || prod_i Pi)`, the KL divergence of the joint from the
product of its marginals (Watanabe 1960).

**The theorem, precise class of operations.** Total correlation is **non-negative and
monotone non-increasing under LOCAL operations** — each party/axis processed by its own channel
`Lambda_i`, i.e. a product channel `Lambda = tensor_i Lambda_i` (confirmed standard: *"total
correlation is monotone non-increasing under local operations — it does not increase under the
local discarding of information,"* the multipartite data-processing inequality; classical finite
case Cover-Thomas Thm 2.8.1 / Csiszar; the quantum/multipartite total-information version in
Modi-Paterek-Son-Vedral-Williamson, PRL 104, 080501, 2010). Proof in two facts:

1. **COMMUTING** — a product channel maps the product-of-marginals of `P` to the
   product-of-marginals of `Lambda P` (`Lambda(prod_i Pi) = prod_i Lambda_i Pi`, and the `i`-th
   marginal of `Lambda P` is `Lambda_i Pi`).
2. **RELATIVE-ENTROPY DPI** — `D(Lambda P || Lambda Q) <= D(P || Q)` (same channel both arguments).

Then `TC(Lambda P) = D(Lambda P || prod Lambda_i Pi) = D(Lambda P || Lambda(prod Pi)) <=
D(P || prod Pi) = TC(P)`. QED

**Verdict against the pre-registered rule: CONDITIONALLY UN-FORGEABLE.** Un-forgeable by any
**local** attacker (cannot manufacture `I_total` — the Third included — by tuning axes one at a
time). Forgeable only by a genuinely **joint** operation, which is a real coordinating cause.
Naming the condition is the content, not a hedge.

**Load-bearing distinction from `FourLaws`.** `FourLaws.RestrictedSecondLaw` records the general
DPI as blocked on **Fischer's inequality** `det Sigma <= prod det(blocks)`. That is the Gaussian
ln-det **subset-monotonicity** route (adding variables raises `TC`). The **channel / DPI** route
above is *different* and is the correct tool for un-forgeability; it needs relative-entropy
monotonicity, which mathlib v4.14 lacks in channel form (no `klDiv`). So Prong A **relocates**
the open Lean step: the un-forgeability of the Third does not wait on Fischer — it waits on a
channel-form relative-entropy DPI.

**Lean (`Core/TriadicChannel.lean`, builds green).** `local_op_does_not_increase_TC` **proves
the reduction**: given the commuting law and relative-entropy DPI as hypotheses, `TC` is
non-increasing under the local channel (pure algebra — mirrors `FourLaws.tc_group_chain_rule`'s
reduction-proved/input-named house style). Records `TriadicSecondLaw` (reduction proved, input
named, condition stated) and `TriadicBlindSpot` (both blind-spot kernels proved, gap measured).

---

## PRONG B — the blind spot, measured

### Scenario 1 — discrete parity family (EXACT, from the pmf; no estimation)

`n`-bit even-parity uniform + independent symmetric bit-flip noise `eps`. The pairwise detector is
a **flat line at the independent baseline** across the *entire* family, while true coordination
ranges from 1 bit to 0:

| n | eps | `I_total` (bits, exact) | `S/2` | `Neff_PR` | `rho-bar` | hidden frac | O-info (bits) | triple <s s s> | max pairwise |
|---|---|---|---|---|---|---|---|---|---|
| 3 | 0.00 | **1.000** | 0 | **3.000** | 0 | **1.00** | -1.000 (synergy) | -1.000 | 0 |
| 3 | 0.05 | 0.428 | 0 | 3.000 | 0 | 1.00 | -0.428 | -0.729 | 0 |
| 3 | 0.10 | 0.198 | 0 | 3.000 | 0 | 1.00 | -0.198 | -0.512 | 0 |
| 3 | 0.20 | 0.034 | 0 | 3.000 | 0 | 1.00 | -0.034 | -0.216 | 0 |
| 3 | 0.30 | 0.003 | 0 | 3.000 | 0 | 1.00 | -0.003 | -0.064 | 0 |
| 4 | 0.00 | 1.000 | 0 | **4.000** | 0 | 1.00 | -2.000 | **0** | 0 |
| 5 | 0.00 | 1.000 | 0 | **5.000** | 0 | 1.00 | -3.000 | **0** | 0 |

- **100% hidden at every grain.** `S/2 = 0`, `rho-bar = 0`, `Neff_PR = n` exactly — the detector
  reports **maximal independence** on a state locked by a parity constraint. It is not blind in
  the neutral sense; it reads the *opposite of the truth*.
- **The synergy probes recover it.** O-information is negative (synergy-dominated) for every
  coordinated case; it is the sign-flip that flags "this looks independent but isn't."

### Scenario 2 — continuous sign-parity x amplitude (`Xi = Ui * Ai`, N=200k, shuffle-null controlled)

The `S`-relevant case: `Xi` pairwise independent by construction, so **both** the linear `S` and
the **copula** `S` (normal-scored — the exact functional the cosmic/DE pipeline uses) are blind.

| p(parity) | `I_total` (bits, bias-corrected) | linear `S/2` | **copula `S/2`** | `Neff_cop` | hidden frac | **copula 3-pt <g g g> (z)** | pairwise copula z (max) |
|---|---|---|---|---|---|---|---|
| 1.00 | **0.989** | 3e-6 | 3e-6 | 3.000 | **0.99999** | **0.508 (z=228)** | 0.96 (noise) |
| 0.90 | 0.703 | 2e-5 | 2e-5 | 3.000 | 0.99996 | 0.458 (z=209) | 2.33 (noise) |
| 0.75 | 0.456 | 2e-5 | 2e-5 | 3.000 | 0.99994 | 0.383 (z=187) | 2.05 (noise) |
| 0.60 | 0.277 | 5e-6 | 5e-6 | 3.000 | 0.99997 | 0.306 (z=136) | 1.25 (noise) |
| 0.50 | 0.189 | 2e-5 | 2e-5 | 3.000 | 0.99986 | 0.252 (z=114) | 2.51 (noise) |

(z = departure from the shuffle-null floor, not a physical sigma; the pairwise-copula z is
non-monotonic in p and floor-consistent — no signal. `I_total` binned/plug-in, bias removed by
the per-column shuffle null.)

- **Copula-`S` is as blind as linear-`S`** — a purely-triadic coordination survives the copula
  transform untouched (the exact operational point the Thirdness prenup makes).
- **The cosmic Thirdness estimator is the right tool.** The copula 3-point <g1 g2 g3> — the same
  amplitude-blind higher-order probe as `experiments/cosmo_entropic_potential/thirdness/` — fires
  at z >= 114 where the pairwise copula reads pure noise.

### Verdict against the pre-registered rules

- **INVISIBLE — decisively.** `I_total` bounded away from 0 (discrete exact >= 0.1 bit; continuous
  shuffle-z >= 100) with `|S/2| < 0.01`, `|rho-bar| < 0.02`, `Neff_PR` within 2% of n. Hidden
  fraction ~ 1.0. **K3's blind-spot leg fires: the pairwise safety floor has a real triadic blind spot.**
- **CATCHABLE — yes, with a recursion caveat.** O-information (all orders) and the full
  bias-corrected multi-information recover the signal. BUT a **fixed-order** probe has its own
  blind spot at higher order: the 3-point <s s s> is **exactly zero** for n>=4 parity (a
  3-subset of an order-n coordination is independent — see the n=4,5 rows). Only an
  **order-complete** probe (full-set O-information / multi-information) catches coordination at
  arbitrary order. The blind spot recurses with interaction order; the fix must be full-set, not
  triple-only.

---

## Is CIRIS's safety floor triadically complete? (both readings)

**No — the pairwise semantic layer is not.** The Neff/CEG detector in `SPEC.md` and
`trace_harness/harness_neff.py` is built entirely on the pairwise correlation matrix
(`Neff_PR`, `rho-bar`, equicorrelation `k_eff`). A **purely-triadic deception** — constraint axes
each individually and *pairwise* in-distribution, but the joint triple (or higher tuple)
satisfying a parity-like forbidden-combination that carries the deceptive content — posts
**exactly zero** to it and reads as **maximally independent (Neff = full rank)**, the safest
possible score. This is structural, not a sampling artifact.

**Two honest mitigations, and their limits:**

1. **Un-forgeability (Prong A) does not, by itself, close the blind spot.** It guarantees a
   *local* attacker cannot manufacture `I_total`. But the adversarial threat model is a **joint
   author** — the agent writes the whole trace at once — so the deceptive coordination is
   *deliberately created* by a genuine joint cause, exactly the case Prong A's condition permits.
   Un-forgeability's real safety value is different and still real: it certifies that the
   coordination a *complete* detector would read is a **robust quantity that cannot be faked up
   by benign local noise** — which is what licenses building the detector.
2. **The CEG attestation substrate is orthogonal to this blind spot.** The triadic blind spot is
   a property of pairwise *correlation* instruments. CEG is a conformance-frozen cryptographic
   attestation surface — not a correlation detector — so "triadic blind spot" does not apply to
   it the same way; its irreducible floor stands. The security that survives a triadic deception
   lives in CEG, **not** in the pairwise semantic Neff.

**The fix (detector sketch).** Add, alongside the pairwise `Neff`, a **higher-order interaction
probe over constraint-feature tuples**: (a) O-information over each triple/tuple (sign flags
synergy-dominated structure the pairwise rho-bar cannot); (b) the copula k-point <gi gj g...> on
normal-scored features (cheap, the validated cosmic-Thirdness estimator); (c) a bias-corrected
full multi-information where dimensionality allows — each with a shuffle null. To be
**order-complete** it must run to the interaction order of concern, not stop at triples (the n>=4
result). The adversarial-Neff run should therefore report a **synergy channel** next to the
pairwise one: `Neff_pairwise` (current) + `TC/O-information` (new) + the CEG substrate floor.

## Caveats (honest limits; none touch the two verdicts)

- Constructed distributions, not measurements — z-scores are departures from the estimator's own
  shuffle-null floor, not physical sigma. Scenario 1 is EXACT (no estimation).
- The continuous binned `I_total` is a plug-in estimate; the shuffle null removes its bias, and
  the point estimate (0.989 bits at p=1) matches the exact 1-bit sign-parity content.
- Prong A's Lean file proves the *reduction*; the channel-form relative-entropy DPI is the named
  analytic input (absent from mathlib v4.14). The un-forgeability itself is a standard cited
  theorem, mechanization pending that lemma.
