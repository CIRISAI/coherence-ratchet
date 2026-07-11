# The double-entry exchange rate — FIRST TOY MEASUREMENT

**Date 2026-07-10.** The first number for the ledger-dynamics research target
(`papers/notes/one_ledger_pressure_test.md` §5; CLAUDE.md "Research target"): the conversion
factor between the two entries of a halo-formation transaction — within-halo phase-space
coherence **debited** at virialization vs inter-halo halo-grain coordination **credited** per
halo formed. Methods and all pre-committed choices: `DECISIONS.md`. Data: `results.json`,
`run.log`.

## The number

```
DEBIT   = 0.262 ± 0.091 nats/halo   (sd 0.385, n = 18 halos, 89% positive; N-stable
                                     0.2616 @ N=5000 vs 0.2656 @ N=2000)
CREDIT  = 0.308 ± 0.018 nats/halo   (dS_total/dk, TNG300 growing branch, cap-excluded)
X       = 0.850 ± 0.299             (nats debited per nat credited)
```

**X is consistent with unity within 35% errors — and that sentence must NOT be read as
"coordination is conserved across rungs."** The deflationary reading, stated in the same
breath: the debit and the credit are S values on **two different grains** (a 6-variable x–v
copula per halo's particles vs the halo-grain log-det per unit), measured on **two different
simulations** (TNG100 debit, TNG300 credit) at **mass-mismatched populations** (debit sample
at M200c ≈ 1.0–1.1×10¹², above the 7.4×10¹¹ credit threshold; only 1/18 halos literally
crosses the threshold in the window). The nat units are formally commensurate; that they are
the *same currency* is exactly the unestablished claim the pressure-test note flagged. At this
precision, X ≈ 1 may be a coincidence of scale choices (subsample N, threshold, epoch pair).

## What IS established by this measurement

1. **The debit is real and has the predicted sign.** Tracking a fixed particle set (progenitor
   IDs at z = 1 ∩ descendant IDs at z = 0.5, ~85% survival) through virialization, the x–v
   copula coherence FALLS in 16/18 halos. The control matters: on **whole FOF groups** the
   sign inverts (S 0.48 → 1.91) because the growing infall envelope dominates corr(x,v) —
   same-material tracking is the load-bearing methodological choice, and it was made for a
   stated physical reason (isolate virialization from envelope growth), not tuned to a result.
2. **The debit is a lower bound.** The z = 1 progenitor is already partly bound, so S_before
   understates the true cold-infall coherence.
3. **Both entries are measurable objects** with stable estimators — the double-entry structure
   proposed in the pressure-test note is operationally realizable, not just a metaphor.
4. The 2/18 negative debits are small (e.g. −0.010 vs sample sd 0.385) and consistent with
   halos still accreting coherently through the window (late assemblers), not with estimator
   failure.

## What would make X meaningful (the promotion criteria, stated in advance)

- Stability across **mass bins** (the current single bin is the biggest gap — the credit
  threshold population must be sampled directly), **epoch pairs**, and subsample conventions.
- A **derivation** relating the two grains' units (the exchange-rate law), or failing that, X
  measured on a substrate where the answer is independently known.
- Same-simulation measurement of both sides (TNG100 credit curve, or TNG300 debit sample).

Until then X = 0.85 ± 0.30 is a ratio of two separately-measured nat-quantities — the first
data point of the research program, not a law.

## Caveats (full)

Single mass bin; single epoch pair (z = 1 → 0.5); two different simulations; n = 18;
pairwise-copula shadow (multi-stream folds invisible — order-≥3 blind spot); progenitor
partial binding (debit lower bound); selection skew from `order_by=-mass` (documented in
DECISIONS.md §debit-2); credit side inherits the 2-point proxy C and the frozen-pipeline
conventions of the large-volume test.

## Files

`DECISIONS.md` (pre-committed choices incl. the same-material tracking rationale) ·
`exchange_rate.py` · `results.json` (per-halo table: S_before/S_after/debit at N=5000 and
N=2000, survival fractions, masses) · `run.log`.

*(Summary written by the orchestrating session from the agent's completed results.json,
run.log, and DECISIONS.md after the agent idled; all numbers are the agent's executed output.)*
