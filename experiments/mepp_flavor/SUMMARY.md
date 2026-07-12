# MEPP-flavor — VERDICT: THIN (no distinct DUNE fork; the fill-out stays thin)

**Date 2026-07-12.** Registered forward fork for the one THIN fill-out named in
`sm_from_thermodynamics.md` §4: does the FORCED entropy-production functional sigma_max (N1)
*select* the observed flavor copula, and does sigma-weighting forecast a distinct delta_CP region
from anarchy and from minimization? Pre-registration frozen in `DECISIONS.md` before any result.
Data: `results.json`; code `run_mepp_flavor.py`. Ensemble: the frozen 200k Haar U(3), seed
20260710, bit-identical to `sm_escalator_mixing`.

## Forced-object provenance (both checks pass exactly, before any use)

- **sigma functional** — bench-validated `sigma = Tr[Q^T D^-1 Q C^-1]`, N1 (bounded actuated drive),
  generalized to an arbitrary correlation spectrum. `sigma_max_N1_general(C)` reproduces the frozen
  `corridor_ceiling/sigma_max.py::sigma_max_N1(rho,k)` on the Kish object to 8e-15 relative error.
  Not invented; extended and checked against the frozen source.
- **|V|^2 -> C map** — the one-hot indicator correlation from `run_mixing.py::functionals` (the
  object whose -ln det is `S_onehot`). `-ln det C_copula(V) == functionals(V)['S_onehot']` to 0.0 on
  the observed cases. sigma is applied to the FROZEN copula object, not a fresh construction.

## The four deliverable questions, answered

**1. Does sigma-max concentrate on the observed copula? NO.**
The observed copulas are LOW-sigma, not sigma-extremal: CKM at the 24.4th sigma-percentile, PMNS at
the 33.9th (upper octant 39.8) — all below the Haar median. The moment-matched tilt required to
reproduce the observed PMNS sigma is beta* = -0.19 (NEGATIVE): you must tilt toward *low* sigma to
land on the observed lepton copula. A maximize-sigma (MEPP) principle selects AWAY from what is
observed. `Spearman(sigma_flavor, MI) = 0.063` — nonzero only because N = 2e5 (p~2e-173); effect
size negligible, and its weak sign is toward the comonotone pole, away from anarchic PMNS.

**2. The predicted |J| / |sin delta| distribution — NOT a distinct third prong.**
Where sigma-selection moves CP, it SUPPRESSES it. Top-sigma tail medians vs flat anarchy:

| region | median |J| | median |sin delta| | median MI |
|---|---|---|---|
| flat anarchy | 0.0255 | 0.708 | 0.233 |
| top-10% sigma | 0.0108 | 0.592 | 0.439 |
| top-5% sigma | 0.0076 | 0.555 | 0.512 |
| top-1% sigma | 0.0037 | 0.516 | 0.670 |
| beta*=-0.19 (PMNS-matched) | 0.0251 | 0.705 | 0.237 |

- vs flat anarchy: the tail shift is real, but appears only in the top-sigma tail, which the
  observed copulas do NOT occupy. At the observed sigma level (beta*=-0.19) the sigma-tilted
  |J|/|sin delta|/MI are within Monte-Carlo noise of flat anarchy. For the actual lepton copula,
  MEPP forecasts nothing distinct from anarchy.
- vs minimization: the sigma-max CP shift is SUPPRESSION (|J| 0.0255->0.0037), the SAME sign as
  Thaler-Trifinopoulos entanglement-minimization — it collides with minimization rather than
  opposing it. (The auto-boolean distinct_from_minimization=True compared |sin delta| magnitudes;
  the physically relevant direction agrees. Per DECISIONS.md clause D, a sigma-max that suppresses
  |J| is not a distinct third prong.)

The 3-way DUNE fork does not form: anarchy and MEPP coincide at the observed regime, and MEPP and
minimization share the CP-suppression direction. No delta region is uniquely MEPP's.

**3. Does leptogenesis keep delta observable? NO — usage channel dead.**
sigma_flavor acts through the capacity/angle channel only: Spearman(sigma, J_max(angles)) = -0.034,
Spearman(sigma, MI) = 0.063. The usage channel — rank partial correlation of sigma with |sin delta|
controlling for the three angles — is -0.0013, CI [-0.006, +0.003], consistent with zero. sigma says
nothing about the low-energy phase. Under high-scale leptogenesis (heavy-Majorana-phase CP,
decoupled from low-energy delta), the observable-delta fork is doubly weakened.

**4. THIN or THICKENING? THIN.**
No distinct registered DUNE fork. The registered locator returns a null: sigma-max mis-selects the
observed copula (it is low-sigma; the moment-match needs beta*<0), and where sigma-max moves CP it
suppresses it — colliding with minimization, not opposing it, and coinciding with flat anarchy at
the observed regime. Reported as a null, not retrofitted (the pandey-crosscheck anti-pattern
avoided). The fill-out named in `sm_from_thermodynamics.md` §4 stays thin.

## What is banked (honest positive residue, recognition weight only)

- The forced functional and the frozen copula map compose cleanly and are provenance-checked — the
  machinery to ask "does an entropy-production principle select a flavor copula" now exists and is
  reusable; the answer here is null.
- A real (tail-only) structure: sigma_flavor rises toward the comonotone pole, not the anarchic one
  — the opposite of what the leptogenesis narrative wanted. Filed as the sign, earns nothing.

## Kill / discipline status

Class V (selection, never derivation) — the claim earns nothing without a confirmed distinct-delta
DUNE forecast, and no distinct forecast exists. Not married; not registered as a fork (there is no
fork to register). If a future construction revives it, it must first explain why the observed
copulas are LOW-sigma under N1.

## References (verified)

- Godreche, Luck, J. Phys. A 52, 035002 (2019); arXiv:1807.00694 [verified] — the sigma functional.
- Thaler, Trifinopoulos, arXiv:2410.23343 [verified, secondary] — minimization prong.
- Martyushev, Seleznev, Phys. Rep. 426, 1 (2006); Dewar, J. Phys. A 36, 631 (2003) [verified] — MEPP.
- Fukugita, Yanagida, Phys. Lett. B 174 (1986) 45 [verified] — high-scale leptogenesis.

Internal: `DECISIONS.md`, `sm_from_thermodynamics.md` §4, `sakharov_ledger.md` §2d,
`corridor_ceiling/sigma_max.py`, `sm_escalator_mixing/`.
