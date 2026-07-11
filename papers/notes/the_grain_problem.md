# The grain problem — the night's conclusion, stated as the DE leg's load-bearing open problem

**Date 2026-07-11 (the night of 07-10).** Written after the full-population tiled read
(`experiments/cosmo_entropic_potential/full_population/`, gate-validated, pre-registered)
returned FAIL on the aperture law. This note states what the converging audits proved, what
survives at every grain, the one open problem they isolate, the candidate resolution with its
expectation pre-registered, and the anti-hedging commitment for DR3.

## 1. What the night's three audits jointly proved

The 1.36σ headline magnitude is conditional on an **underived grain choice** (the corner-rule
threshold ≈ 7.4×10¹¹ M⊙/h), and BOTH escapes from that conditionality are now dead, each by a
pre-registered control:

- **Derive the grain (SHM anchor): DEAD.** The fit-quality extremum tracks the GPU cap, not a
  physical mass scale (C1: extremum follows a moved cap; C2: k-matched thinning erases the
  edge). SHM is a passenger (C5). `retention_v2/CHALLENGES.md`.
- **Dissolve the grain (complete book / aperture law): DEAD.** The nested-tile estimator
  (gate-passed: reproduces the exact result to maha 0.09 at three tile sizes) read ALL halos
  ≥1e11 with no cap: **2.21σ**, z_peak 0.79 — worse than the corner grain, falsifying the
  pre-registered complete-book prediction (≥ 1.36σ). Reading more of the book made the fit
  worse. `full_population/results.json`.

**Mechanism, measured:** S(a)'s shape is carried by the above-threshold count k(a) (constant-k
fence: no interior peak at fixed k), and the fit quality is set by WHERE the count-peak sits.
The corner grain places it at z = 0.546 (DESI's preferred crossing epoch); the complete book
places it at z = 0.79 (too early). Different grains are different clocks, and DESI likes the
galaxy-host clock.

## 2. What survives at EVERY grain tested (the selection-free floor)

At every threshold, every cap, and on the complete zero-selection book: **thawing w(z)
(wₐ < 0), an interior S-peak, and a better DESI DR2 fit than ΛCDM** (complete book: 2.21σ and
Δχ² = −1.1 vs ΛCDM's 3.28σ). The complete-book number contains NO tunable choice (population =
all resolved halos; frozen pipeline) and still beats ΛCDM. That is the honest floor claim:
**grain-free, the framework reads the sky better than Λ; the grain buys the margin from 2.2σ
to 1.36σ.** Also measured: the inter-tile term is negligible (S_total ≡ S_extensive to 3
decimals) — coordination across >100 Mpc contributes nothing to the balance, consistent with
the copula turning Gaussian at large scales (copula_stress tier 3).

## 3. The problem, stated once

**Which units post to the DE ledger?** The gravity ontology (instrument-side) says gravity
reads the complete book — but the complete-book *sourcing* corollary drawn from it tonight
(the aperture law) is data-falsified and is hereby severed; the ontology's own content (BMV/DP
kills, audit-discrepancy dark sector) is untouched. The framework's native answer to unit
structure was never "everything" — it is the **rung hierarchy** (piece 6): coordination is
counted per rung, and the epoch's coordinating rung is galactic. The data's preferred grain
(~7×10¹¹, the galaxy-host scale) is exactly where halos begin hosting substantial galaxies.

## 4. Candidate resolution — the galaxy-defined book (expectation pre-registered here)

Define the unit population by **physical membership at the galactic rung** — halos hosting
galaxies above a stellar-mass floor (TNG SUBFIND M*, fetchable; or an HOD-standard
definition) — fixed BEFORE any fit is seen, then run the frozen pipeline with zero threshold
freedom. This is NOT the killed SHM-extremum claim (which tuned a threshold to fit quality
post hoc); it is a definition from independent physics, made once.

**Pre-registered expectation:** the galaxy-book read lands near the corner result — interior
peak near z ≈ 0.55, fit meaningfully better than the complete book (maha < 1.89, i.e., beats
the ≥2e11 mass-cut at matched selection-freedom). **Kill:** galaxy-book fits like the complete
book (maha ≥ 2.0) or the peak leaves the interior — then physical rung-membership does NOT
select the grain, and the grain stays a free input of the theory (a second constant alongside
κ, with the one-marriage claim of `dimensional_line_kB.md` §5 taking the hit it pre-staked).

## 5. Anti-hedging commitment (binding)

**The registered DR3 bet is the frozen corner-rule pipeline, exactly as preregistered —
crossing epoch z = 0.59 ± 0.03 — and it does not change.** The complete-book read (crossing
z ≈ 1.16) and any future galaxy-book read are logged alternatives for understanding the grain
problem; they are NOT switchable claims. If DR3 lands near a variant's number and not the
registered one, the registered bet LOSES and is reported as lost; no post-hoc grain switching.
One bet, placed, held.

---

## 6. Outcomes (2026-07-11, same-day): complete book FAIL; galaxy book AMBIGUOUS with structure

**§4's pre-registered run is complete** (`experiments/cosmo_entropic_potential/galaxy_book/`):
maha = 1.919, z_peak = 0.645 interior → **AMBIGUOUS** by the rule (missed PASS by 0.03; KILL
did not fire). The bar does not move; the verdict stands. The structure inside it:

**What the galactic rung DOES set — the clock, and it is a genuine pre-registered alignment:**
- The ≥100-star-particle floor selects the galaxy-host mass scale as an OUTPUT (median
  M200 = 3.75×10¹¹, unforced).
- Across the never-promoted stellar-floor ladder (10^8.5 → 10^10), the fit optimum lands
  EXACTLY on the pre-registered floor (maha 2.61 → **1.92** → 1.96 → 2.55), and that floor is
  the UNIQUE rung with an interior count-peak — the one stellar cut that puts the DE clock at
  DESI's epoch (crossing z = 0.543; lower floors drift late, higher floors early).
- The DR3-registered observable (crossing epoch) is therefore carried by physical
  rung-membership with zero threshold freedom.

**What it does NOT set — the amplitude, and the mechanism-candidate died same-hour:** the
naive reading "amplitude = tightness of the membership band" (higher M* floor → tighter host
band → corner amplitude) is REFUTED by the ladder: wₐ strengthens with the floor but the clock
leaves the interior first; no stellar selection reaches the corner's combination (interior
clock AND wₐ ≈ −0.7 AND maha 1.23). Refined two-dial reading, logged as discovery (NOT
registered): the clock median is set by membership; the amplitude is set by **sharpness in the
assembly-epoch variable** — a hard halo-mass cut is sharp in formation clock, while any
stellar cut is smeared across it by SHM scatter. Candidate future test (requires registration
first): selection sharp in a formation-time proxy (concentration / z_form) should recover
amplitude with the galactic clock. Not run; not to be run without a pre-registered rule.

**Complete book (§1's second escape) definitively FAILED same-night** (2.21σ; more book fits
worse). Net for `dimensional_line_kB` §5: the one-marriage kill does NOT fire (interior peak,
maha < 2.0, and the registered crossing observable is derived from physical membership), but
the marriage is not discharged — the grain narrows to "galactic rung sets the clock; the
amplitude's variable is identified as assembly-epoch sharpness and remains underived."

---

## 7. The from-below candidate (2026-07-11, via the Gibbs-paradox mapping — `mystery_map.md` §2)

The classical species' grain mystery (Gibbs) was resolved by the substrate's indistinguishability
structure. The mapped candidate for ours: **the rung hierarchy IS the coordination species'
indistinguishability structure.** A degree of freedom posts to the ledger at rung r iff it is
distinguishable at r while its sub-rung constituents are phase-mixed/symmetrized: virialization
is the symmetrization event (the exchange-rate DEBIT), the galactic-rung host is the
distinguishable unit (the CREDIT), and >100 Mpc modes are independent and post nothing
(measured — the vanishing inter-tile term). The N! divides out permutation-equivalent
microstates; the rung divides out phase-mixed constituents; conversion-X ≈ 1 is the bookkeeping.

**Payoff — §6's discovery item becomes a principled, registerable prediction:** select units on
a FORMATION-TIME / DISTINGUISHABILITY proxy (concentration, z_form — when the unit became a
symmetrized, distinguishable object), not a stellar cut, and the corner AMPLITUDE should return
together with the galactic clock. Data on disk. NOT to be run before its registration is
written (the pre-registration requirement of §6 stands; this section supplies the derivation
that makes the registration principled rather than post-hoc).

**Honest tension, carried:** the classical precedent is itself split (Jaynes 1992;
Versteegh–Dieks 2011: the grain is observer-relative, not from-below) — and our married gravity
ontology sides with observer-relative (the complete-book instrument). So the genus match is not
"grain resolves from below in both species" but "**both species carry the same
observer-vs-substrate grain tension**" — with mysteries 1, 2, and 8 of the map all reducing to
the grain: both thermodynamics keep their deepest problem in the same drawer.
