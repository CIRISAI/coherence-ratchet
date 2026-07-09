# Anesthesia TRAJECTORY: does maintenance (γM / detailed balance) collapse BEFORE, WITH, or AFTER structure (k_eff)?

> ⚠ **PARTIALLY SUPERSEDED (2026-07-04) by the George replication**
> (`spectral_anesthesia_george_summary.md`). Read them together.
>
> - **RETRACTED:** "k_eff collapses under both agents and is the robust correlate of fading
>   consciousness." The collapse is **Chibi-specific**. In George it does not occur and the
>   sign *reverses* (propofol 7.10→7.88, ketamine 5.83→6.94, both rising). Absolute ECoG-field
>   k_eff is not portable across animals and its within-session sign is not stable.
> - **RETRACTED as a replicated result:** the ketamine counter-example below ("structure
>   collapses while maintenance persists") is **n=1**. George shows no structural collapse, so
>   the configuration never arises there; only the "ketamine preserves DB" half replicates.
> - **HOLDS (2/2 animals):** the maintenance split — deep propofol falls below the null (bound),
>   deep ketamine stays above it (coordinating). This is a **drug-specific** signature, not a
>   consciousness correlate: both agents produce unconsciousness in *different* cells.


**The dynamical complement to the static axis-independence proof.** The static run
(`spectral_axis_independence.py`) showed the two axes — STRUCTURE (k_eff / rank) and
MAINTENANCE (detailed balance = the γM term) — vary *independently* at a frozen instant.
This run asks the **dynamical** question the framework actually stakes a claim on: as a real
system loses consciousness under anesthesia, in what ORDER do the two axes collapse? The
framework's load-bearing prediction is that **maintenance is what holds the corridor**, so
γM (Axis 2) should withdraw **BEFORE or WITH** the structural k_eff collapse (Axis 1) — the
maintenance withdrawal *causes* the structural collapse, so it cannot lag it.

## Design

- **Data (real, open).** NeuroTycho (Yanagawa, Fujii; RIKEN) macaque **Chibi**, 128-ch subdural
  ECoG, 1 kHz. The **continuous Session2** recording of each agent spans one uninterrupted
  acquisition: **awake (pre-injection) → anesthetic injection → INDUCTION (graded) → deep
  anesthesia**. This is the cleanest possible substrate for an ordering question — no
  concatenation gaps across the transition.
  - **Propofol** `20120730PF` Session2: injection @86s, clinician "Anesthetized" 553–1098s.
  - **Ketamine** `20120719KT` Session2: injection @24s, clinician "Anesthetized" 917–1502s.
- **Windowing.** 20 s windows, 5 s step (75% overlap) slid across the whole continuous Session2
  up to the end of the deep epoch; broadband **1–100 Hz** (the two-pole primary band); 50 Hz
  notch; decimate to 250 Hz; per-channel z-score; **no re-reference** (CAR injects spurious
  anticorrelation and biases k_eff). Windows are labelled by epoch from the Condition markers.
- **Awake baseline LEVEL** for each axis is the median over **Session1** (the long, separate
  awake block: ~90 non-overlapping 20 s windows), a more robust reference than the thin
  pre-injection lead-in inside Session2. Deep LEVEL = median over the Session2 deep epoch.
- **Axis 1 (STRUCTURE):** `k_eff` = participation ratio of the 128-ch correlation eigenspectrum
  (`spectral_test.corr_eig` / `participation_ratio`), verbatim. ρ_Kish inverted from k_eff.
- **Axis 2 (MAINTENANCE):** detailed-balance |z| **two validated ways** —
  (a) **winding-rate** |z| (`entropy_production.irreversibility_from_units`, k=4 top modes,
  block-bootstrap null), (b) **direct circulation** ⟨x dy − y dx⟩ vs a **phase-randomized null**
  (`spectral_galaxy_db`-style, 1000 surrogates). Null ceiling for both ≈ 1.5; awake ECoG sits
  modestly above it.
- **Ordering statistic.** For each axis: (i) does it *separate* awake→deep at all (Mann-Whitney +
  Cliff's δ)? (ii) the **midpoint-crossing time** of the lightly-smoothed trajectory within the
  induction search window, with a **block-bootstrap 95% CI** over windows. Ordering is read from
  the crossing times; if a DB axis does not separate or its CI straddles the k_eff crossing, the
  ordering is **UNRESOLVED** — not manufactured.

## Per-window results (both agents): time-bin / epoch / k_eff / DB |z| winding / DB |z| circ

Representative rows (full per-window record in the JSONL / results JSON):

### Propofol (Session2; inj@86s, deep-onset@553s)

| t (s) | epoch | k_eff | ρ_Kish | \|DB z\| winding | \|DB z\| circ |
|------:|-------|------:|-------:|----------------:|--------------:|
| 30  | awake      | 19.8 | 0.044 | 4.1 | 10.4 |
| 70  | awake      | 16.6 | 0.053 | 3.3 | 4.8  |
| 110 | induction  | 18.6 | 0.046 | 3.7 | 6.4  |
| 130 | induction  | 17.6 | 0.049 | 2.3 | 4.2  |
| **150** | **induction** | **5.1** | **0.130** | 1.8 | 4.6 |
| 210 | induction  | 2.4  | 0.220 | 2.9 | 3.5  |
| 290 | induction  | 6.7  | 0.116 | 2.2 | 9.9  |
| 630 | deep       | 7.1  | ~0.11 | 2.3 | ~1   |

k_eff holds its awake value (~17–19) *through* injection and the first ~45 s of induction, then
**collapses sharply between t≈130 and 150 s** (17.6 → 5.1) and stays low. The DB estimators stay
noisy (winding 2–4, circ bouncing 2–10) with **no collapse aligned to the k_eff drop**; the
circulation signal even spikes back to ~10 at t≈290 s — *after* k_eff has already collapsed.

### Ketamine (Session2; inj@24s, deep-onset@917s)

| t (s) | epoch | k_eff | ρ_Kish | \|DB z\| winding | \|DB z\| circ |
|------:|-------|------:|-------:|----------------:|--------------:|
| 10   | awake     | 15.3 | 0.058 | 4.0 | 6.8  |
| 85   | induction | 15.8 | 0.056 | 6.2 | 9.9  |
| 235  | induction | 11.7 | 0.079 | 3.3 | 6.4  |
| 385  | induction | 7.2  | 0.133 | 3.5 | 3.8  |
| 610  | induction | 6.1  | 0.157 | 4.9 | 7.5  |
| 910  | induction | 6.4  | 0.149 | 4.1 | 5.4  |
| 985  | deep      | 5.3  | 0.182 | 1.9 | 8.5  |
| 1285 | deep      | 4.5  | 0.218 | 2.1 | 9.6  |
| 1495 | deep      | 5.5  | 0.175 | 3.3 | 3.6  |

k_eff declines **gradually** from awake (~15) to deep (~5) over t≈85–460 s, then stays low.
But the DB estimators **do not fall at all** — winding hovers 2–9 and circulation stays **high
(6–10) throughout the deep epoch**, both well above the ~1.5 null. Deep ketamine still **breaks
detailed balance**: maintenance is *not* withdrawn.

## Axis levels and transition times

| agent | axis | awake | deep | Cliff's δ | p | midpoint-crossing t (95% CI) |
|-------|------|------:|-----:|----------:|--:|:----------------------------:|
| propofol | **k_eff** (Axis 1) | 13.93 | 6.20 | **1.00** | 1e-33 | **142 s [140, 147]** |
| propofol | DB winding (Axis 2a) | 3.10 | 2.34 | 0.44 | 1e-07 | 128 s [115, 250] |
| propofol | DB circ (Axis 2b) | 5.43 | 0.93 | 0.82 | 5e-23 | 183 s [86, 245] |
| ketamine | **k_eff** (Axis 1) | 13.77 | 5.25 | **1.00** | 2e-34 | **176 s [175, 270]** |
| ketamine | DB winding (Axis 2a) | 3.27 | **4.34** ↑ | 0.32 | 1e-04 | *(spurious; no drop)* |
| ketamine | DB circ (Axis 2b) | 5.56 | **6.86** ↑ | 0.19 | 0.02 | *(spurious; no drop)* |

(propofol awake levels are the Session1 baseline; the Session2 pre-injection lead-in agrees:
k_eff 17.7, |wind| 3.4, |circ| 6.1.)

## Ordering verdict

**Headline: the framework's dynamical prediction — that maintenance (γM) withdrawal drives, and
therefore PRECEDES or ACCOMPANIES, the structural (k_eff) collapse — is NOT supported. In neither
agent does the detailed-balance signal drop cleanly before k_eff, and ketamine is a decisive
counter-example: k_eff collapses fully while detailed balance is entirely PRESERVED.** The one
robust dynamical fact is that k_eff (Axis 1) collapses under both agents as consciousness is lost;
the maintenance axis is agent-specific, not a universal driver.

**Propofol.** The **structural collapse is a crisp, well-localized event: k_eff crosses its
midpoint at t = 142 s (CI ±4 s)** — ~56 s after injection, i.e. physiological propofol
loss-of-consciousness, and ~410 s *before* the clinician's "Anesthetized" mark (553 s), as
expected. The **maintenance collapse is real by its endpoints** — both DB estimators drop, and
the stronger circulation estimator falls from |z|=5.4 (breaks DB, awake) to |z|=0.93 (**below the
~1.5 null → DB-satisfying**) in deep anesthesia, exactly the "maintenance withdrawn = bound"
reading. **But its TIMING is not resolvable:** the winding midpoint (128 s) and circulation
midpoint (183 s) **bracket** the k_eff crossing, their bootstrap CIs are wide ([115,250] and
[86,245]) and both **straddle** the sharp k_eff time, and the two estimators disagree on the
direction (winding −14 s ≈ *with*; circ +41 s ≈ *after*). So for propofol the ordering is
**UNRESOLVED**, and — importantly — the data give **no support for the predicted
"maintenance-before-structure" ordering.** If anything the strong circulation signal's central
estimate *lags* the structural collapse (and visibly persists to t≈290 s, well after k_eff has
dropped), the opposite of the prediction.

**Ketamine (the decisive case).** k_eff collapses just as completely (13.8 → 5.25, Cliff's δ=1.0,
crossing ≈176 s), but **both detailed-balance estimators fail to drop — they are flat-to-rising**:
winding 3.27 → 4.34 (δ=0.32, *up*), circulation 5.56 → 6.86 (δ=0.19, *up*), both staying far above
the ~1.5 null throughout deep anesthesia. So the "crossing times" the detector reports for ketamine
DB (46 s, 121 s) are **spurious noise crossings of a signal that never separates**, and are scored
**UNRESOLVED**. The substantive result: **deep ketamine loses consciousness (k_eff collapses) with
detailed balance fully preserved (still breaks DB).** This is a clean counter-example to
"maintenance withdrawal is what removes the corridor structure" — here the structure goes and the
maintenance stays. (It also reproduces the two-pole test's finding that ketamine's DB is flat/rising,
not dropping, and matches ketamine pharmacology: a dissociative that produces an *activated*, not a
quiescent, cortical state.)

**Cross-agent synthesis — two different trajectories through the 2×2.** By deep anesthesia the two
agents sit in **different cells**: propofol is low-rank **+ DB-satisfying** (k_eff 6.2, circ |z|=0.93
< null) = the **bound** cell; ketamine is low-rank **+ breaks-DB** (k_eff 5.25, circ |z|=6.9, wind
|z|=4.3 ≫ null) = the **coordinating** cell. Loss of consciousness is therefore **not a single path
through the 2×2**: the shared correlate is the Axis-1 (k_eff) collapse; the Axis-2 (maintenance)
behaviour is agent-specific. This is the *dynamical* echo of the static axis-independence result —
here a real system moves such that Axis 1 collapses while Axis 2 does or does not, independently.

## Honest caveats (load-bearing)

- **GRAIN.** ECoG is a mesoscopic neural **field**, not single units. Residual shared-field
  structure inflates absolute correlation, so only **within-session temporal differences** are
  read; absolute k_eff / |z| are field/reference-confounded. A field measurement can also blur a
  fast maintenance transient — the ordering resolution is capped by this grain.
- **DB is a WEAK signal in ECoG.** Awake winding |z| sits only ~3 (barely above the ~1.5 null),
  and the winding awake→deep separation is modest (Cliff's δ=0.44). The circulation estimator is
  the stronger/ cleaner one (δ=0.82, deep drops below null). The two disagreeing on the ordering
  direction is itself the honest headline: **the maintenance-transition time is not measurable to
  the precision needed to beat the k_eff transition**, whose CI is ±4 s.
- **Temporal resolution.** 20 s windows / 5 s step. A |Δt| below ~one window (20 s) is scored
  "WITH". The k_eff crossing is sharp (CI ±4 s); the DB crossings are not (CI spans ~130–160 s),
  so the comparison is limited by the DB estimator, not by k_eff.
- **BAND.** Broadband 1–100 Hz (two-pole primary, where propofol's DB drop held). The two-pole
  test showed the *exit pole* can flip with band; this run does not re-scan bands, so the ordering
  is **not established as band-robust** — a stated limitation.
- **Nonstationarity / edge effects.** The first awake windows show inflated DB (filter-edge /
  onset transient); induction is intrinsically nonstationary, so any DB estimate there mixes
  transient relaxation with residual γM. This is exactly why the DB crossing is noisy.
- **k_eff "recovers" slightly inside deep** (≈6–8 vs induction lows ≈2–5): burst-suppression /
  changing deep-plane dynamics, not a return of coordination (ρ_Kish stays high, DB stays low).
- **One monkey (Chibi), one session per agent.** Replication (monkey George; both agents available
  at the same source) is the obvious next step. The k_eff collapse is a large within-session effect
  (δ=1.0) so it is not fragile, but the cross-agent 2×2 divergence rests on a single session each.
- **Ketamine's awake lead-in inside Session2 is only ~3 windows** (injection at 24 s), so its awake
  baseline is carried by the separate Session1 block; the two agree for k_eff and DB, but this is a
  cross-sub-recording comparison, not fully within-continuous-segment as for propofol.
- **In BOTH agents the k_eff collapse precedes the clinician's "Anesthetized" annotation** by
  several minutes (propofol 142 s vs 553 s; ketamine 176 s vs 917 s) — consistent with rapid
  physiological LOC, and a reason the "deep" LEVEL (median over the annotated deep epoch) is a clean
  reference while the *induction* epoch is where the action is.

## Bottom line

**The dynamical two-pole/maintenance claim does not survive a real graded transition.** Sliding a
window across continuous macaque ECoG through propofol- and ketamine-induced loss of consciousness:
the **structural axis (k_eff) collapses under both agents** and is the robust dynamical correlate of
fading consciousness (propofol sharp at 142 s; ketamine gradual, crossing 176 s; both well before the
clinical annotation). The **maintenance axis (detailed balance / γM) does NOT behave as the framework
predicts.** Under propofol it does eventually withdraw (circulation |z| 5.4 → 0.9, dropping below the
null into the DB-satisfying "bound" cell) but its transition is noisy and **not resolvably before**
k_eff — the two DB estimators straddle the k_eff time (winding −14 s, circ +41 s) with wide CIs, so
the ordering is **UNRESOLVED**, and the strong estimator if anything **lags**. Under **ketamine the
maintenance axis does not withdraw at all** — deep ketamine stays firmly in the "breaks-DB /
coordinating" cell while k_eff collapses — a **clean counter-example** to maintenance-withdrawal being
what removes the corridor structure. Net: **γM does not drop before k_eff; the prediction is not
supported, and is falsified in the necessity direction by ketamine.** What the run *does* show
positively is the **dynamical independence of the two axes** — a real system driven to unconsciousness
moves so that Axis 1 collapses while Axis 2 collapses (propofol) or persists (ketamine), the two
anesthetics landing in **different cells of the 2×2**. Carried honestly: ECoG is a mesoscopic field
(grain caveat), the DB signal is weak/noisy (winding barely clears null), the ordering is limited by
the DB estimator not by k_eff, and it is one monkey per agent in a single broadband analysis.

*Outputs: `spectral_results_anesthesia_trajectory.json` (meta + per-window arrays + baselines +
ordering), `trajectory_windows_{propofol,ketamine}.jsonl` (per-window, flushed live),
`baseline_windows_{propofol,ketamine}.json`, `anesthesia_trajectory_ordering.json`,
`spectral_anesthesia_trajectory.png` (both axes vs time). Script
`spectral_anesthesia_trajectory.py` (+ `_post.py`); estimators reused verbatim from
`spectral_test.py`, `entropy_production.py`, and `spectral_galaxy_db.py`-style circulation. Real
data only; no commit; no `.lean` edits.*
