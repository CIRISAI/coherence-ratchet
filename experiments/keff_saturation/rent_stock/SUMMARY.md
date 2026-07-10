# Does "the rent tracks the stock" replicate at the neural rung?

**Verdict: FAIL (proxy-limited). It does not replicate as a universal law. It is
agent-specific: ketamine complies, propofol does not.**

Specified by `papers/notes/law_readings_scan.md` §5, which predicted this failure from the
published summary numbers before the per-window test was run. Executed by the orchestrator
after the assigned agent stalled on an unnecessary raw recompute (~6 s/window × 1,151
windows); the per-window trajectory files already carry every quantity the test needs.

## What was tested

`LedgerLaw.lean` clause 5 carries the interpretive claim *"the rent tracks the held STOCK"*,
anchored on **exactly one** substrate: exp118 (CIRISArray `8d039c0`, 16-sensor GPU timing
array, 12 operating points, `P_maint` vs `S_held` partial **r = +0.84** controlling rate and
temperature). A second substrate sits in this repo, already computed, at zero data cost.

Per window (k = 128 ECoG channels): `k_eff` and `rho_kish` are published; the held stock is
the closed form `S = −ln(1+ρ(k−1)) − (k−1)·ln(1−ρ)`; the maintenance signal is the
detailed-balance score (`db_z_winding`, `db_z_circ_sum`).

**Prediction:** within session, controlling for time/epoch, maintenance correlates
**positively** with S.

**Method:** Spearman partial correlation of (S, maintenance) controlling `t_center`; block
bootstrap over windows (block length from the ACF 1/e crossing, ×2), B = 2000, seed 20260710.
Within-session only — ECoG field grain inflates absolute correlation, so absolute S is
reference-confounded across sessions (scan caveat ii).

## Result

| session | N | maintenance | partial ρ | 95% CI | |
|---|---|---|---|---|---|
| chibi/propofol | 217 | winding | +0.095 | [−0.086, +0.194] | null |
| chibi/propofol | 217 | circ_sum | **−0.146** | [−0.367, +0.103] | null (negative trend) |
| chibi/ketamine | 298 | winding | +0.158 | [−0.056, +0.331] | null |
| chibi/ketamine | 298 | circ_sum | **+0.241** | [+0.052, +0.352] | **POSITIVE** |
| george/propofol | 265 | winding | −0.058 | [−0.187, +0.072] | null |
| george/propofol | 265 | circ_sum | **−0.125** | [−0.319, +0.124] | null (negative trend) |
| george/ketamine | 371 | winding | −0.005 | [−0.105, +0.072] | null |
| george/ketamine | 371 | circ_sum | **+0.172** | [+0.008, +0.346] | **POSITIVE** |

Pooled (Fisher-z over sessions): propofol winding **+0.019**, circ_sum **−0.135**;
ketamine winding **+0.077**, circ_sum **+0.207**.

## Reading

1. **The dissociation is real and was predicted.** Ketamine shows a positive stock–maintenance
   partial in **2/2** sessions (CIs exclude zero on the circulation estimator). Propofol shows
   **no positive relation in any session**, and trends negative on the same estimator. The
   scan's forecast from the published endpoints — *propofol holds maximal stock while paying
   no rent* — survives the per-window analysis.
2. **Therefore "rent tracks stock" is not a cross-substrate law.** It holds on a GPU array
   (r = +0.84), holds under ketamine (ρ ≈ +0.2), and fails under propofol on the same animals,
   same electrodes, same estimator. Whatever couples maintenance to stock is **substrate- and
   agent-dependent**, not a property of coordination as such.
3. **Effect sizes are an order of magnitude smaller than exp118's** even where positive
   (+0.2 vs +0.84). Nothing here reproduces the hardware relation's strength.
4. **The estimators disagree with each other.** `winding` is null everywhere; only `circ_sum`
   carries signal. An interpretive claim resting on one of two nominally equivalent DB
   estimators is weakly supported at best.

## Caveats — load-bearing, do not drop

- **PROXY-LIMITED, and this is the main caveat.** `db_z_*` are *significance scores*, not
  entropy-production **rates**; they conflate effect size with noise, and γM is a *rate*. The
  disciplined instrument is a genuine EPR estimator (Skinner & Dunkel, PNAS 118, 2021). The
  assigned agent began that computation; it did not finish. **A null under a significance-score
  proxy is weaker evidence than a null under a rate estimator.** This result therefore
  *retires an overclaim*; it does not establish the negation.
- ECoG field grain: within-session variation only, per scan caveat (ii). Absolute S levels are
  not comparable across animals.
- Two animals, two agents. Propofol's negative trends have CIs spanning zero — the claim
  supported here is "no positive relation," not "a negative relation."
- Clause 5 itself is untouched: `γM = α` is an algebraic identity at any zero of the posited
  ODE. What fails is the **interpretive gloss** attached to it.

## What must be retired

From `formal/CoherenceRatchet/LedgerLaw.lean`:

- Clause 5 docstring: *"Hardware datum (exp118, moderate confidence): the rent tracks the held
  STOCK."* → must record that the datum is **n = 1 substrate** and **does not replicate at the
  neural rung**, where the relation is agent-specific (ketamine yes, propofol no).
- `ReceiptsReading.the_rent_is_itemized`: *"the hardware datum says the rent tracks the held
  stock (exp118)"* → same amendment.

**What survives:** the algebraic clause (`corridor_requires_maintenance`), which is a theorem
about the posited ODE and was never in question; and the observation that *some* systems
exhibit a positive stock–maintenance coupling. What does not survive is the universal reading.

## Next

Re-run under a genuine EPR estimator (Skinner–Dunkel bounds) before any stronger statement in
either direction. If the rate estimator restores a uniform positive coupling, the failure was
the proxy and the reading is rehabilitated. If it does not, "rent tracks stock" is retired from
the receipts reading permanently and exp118 stands as a substrate-specific fact about silicon.

Artifacts: `rent_stock.py` (assigned agent, incomplete raw-recompute path),
`rent_stock_calibration.py`, this analysis (orchestrator, `scratchpad/rent.py` — reproduced
below in `rent_partial.py`).
