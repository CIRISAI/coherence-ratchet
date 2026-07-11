# TNG100-1 cross-check — the mechanism is box-robust; the resolved-corner RULE is not

**Date 2026-07-10.** Independent box (75 Mpc/h, ~20× better mass resolution than TNG300-1),
frozen pipeline, decisions pre-committed (`DECISIONS.md`), estimator gate passed. The test:
does the frozen RULE — not the lucky threshold — produce the DESI-quadrant curve? Data:
`results.json`, `data/*.npz`.

## Verdict, in three parts

**1. The mechanism: fifth independent confirmation.** At the rule-selected threshold, k(a)
peaks at z = 1.358 and S(a) peaks at z = 1.287 ± 0.056 (8/8 jackknife) — the S-peak tracks the
formation turnover on this box exactly as on TNG300 (corner + 12-threshold ladder), and as in
all nine counterfactual universes. K3 does not fire; w_today = −0.863 ± 0.026 sits inside the
registered interval (P3 holds).

**2. The S(a) shape at MATCHED unit definition is box-robust.** At threshold 7×10¹¹ M⊙/h
(TNG300's corner) run on TNG100: **S peaks at z = 0.551**, vs TNG300's 0.546 — the same epoch,
from a box with 27× less volume and only ~1,800 halos against 38,000. The physical object —
the coordination history of galaxy-host-scale units — reproduces across simulations.

**3. The resolved-corner rule is resolution-contingent, and this box exposes it.** The rule
("lowest threshold with max k ≤ cap") selected **2.62×10¹⁰ M⊙/h** here — the box's resolution
floor, a dwarf-scale population that forms early (peak z ≈ 1.3) and projects to
(w₀, wₐ) = (−0.821, −0.271), crossing z = 1.94, **2.76σ** from DESI — outside the
DESI-quadrant success of the TNG300 corner. The rule's selection tracks the instrument
(resolution + computational cap), not the physics. **The TNG300 result's threshold was partly
instrumental luck: cap and resolution happened to land the rule on the galaxy-host scale.**

## The honest consequence for the program's claim

The unit definition — *which mass scale constitutes the coordinating units of the cosmological
ledger* — is a **physical input the framework does not yet derive**. The defensible claim
updates from "the rule removes the threshold dial" to: **one declared physical scale
(galaxy-host halos, ~7×10¹¹ M⊙/h), whose coordination history is box-robust (peak z ≈ 0.55 on
both simulations), plus zero fitted shape parameters.** That is still a far leaner object than
any fitted alternative (CPL: two shape parameters), but the scale choice must be stated as an
input, not laundered through a resolution-dependent rule. Deriving the unit scale (why
galaxy-hosts? plausibly: the completeness scale of the visible ledger — flagged as
interpretation, not result) is now a named open problem.

## Guards and technical notes

- The rule-selected dwarf-scale matrices sit at the estimator's validity edge: min eig
  2–7×10⁻⁴, condition ~2–7×10⁵ (vs 0.03 / ~400 at the TNG300 corner) — dense populations
  push C near-singular; another independent reason "densest resolvable" is the wrong anchor.
- Matched-threshold TNG100 values are noisy (k ≤ 1,874): w_today = −0.62 (but w_today is
  retired per `../large_volume/fine_grid/`); the peak epoch is the robust comparator and is
  what reproduces.
- The 5×10¹² ladder row here is volume-starved (k ≤ 252) and not evidential.

## Preregistration linkage

Recorded as an amendment in `../PREREGISTRATION.md`: the registered DR3-facing object is the
galaxy-host-scale unit definition (box-robust peak z ≈ 0.55, projected crossing z = 0.46–0.47
from the TNG300 dense grid), with the resolved-corner rule's resolution-contingency documented.
Frozen-spec values remain on record; nothing silently swapped.

*(Fetch and DECISIONS by the tng100-cross agent; compute executed by the orchestrating session
under the GPU lock after the agent idled; summary by the orchestrator from executed output.)*
