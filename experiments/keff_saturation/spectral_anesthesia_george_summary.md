# Anesthesia two-axis TRAJECTORY — REPLICATION on monkey GEORGE (vs Chibi)

**What this is.** An exact replication of the Chibi anesthesia-trajectory analysis on a
**second monkey, George**, to test whether the two headline findings are animal-specific or
reproduce: (1) does k_eff (Axis 1, STRUCTURE) collapse under both anesthetics? (2) does the
**ketamine counter-example** replicate — k_eff collapsing while detailed balance (Axis 2,
MAINTENANCE) stays PRESERVED/above-null, i.e. ketamine landing in the *coordinating* cell, not
withdrawing γM — while propofol lands in the *bound* cell (DB drops below null)?

Same source (NeuroTycho / RIKEN, Yanagawa–Fujii), same pipeline and estimators, same ordering
statistics as the Chibi run. Sessions: **propofol `20120731PF_George`**, **ketamine
`20120724KT_George`**, 128-ch subdural ECoG, continuous Session2, 20 s / 5 s windows, broadband
1–100 Hz, no re-reference. Estimators reused verbatim: k_eff = participation ratio of the channel
correlation spectrum (`spectral_test`); DB = winding |z| (`entropy_production`) + direct
phase-randomized circulation |z| (`spectral_galaxy_db` style). Awake-baseline LEVEL from the
long Session1 awake block; deep LEVEL from the Session2 Anesthetized epoch. Ordering = smoothed
midpoint-crossing time with block-bootstrap CI, plus Mann–Whitney + Cliff's δ for awake→deep
separation.

## George-specific quirks (flagged, load-bearing)

- **George's ABSOLUTE k_eff is much lower than Chibi's** (George awake k_eff ≈ 5–7 vs Chibi
  ≈ 14–18). **Absolute k_eff is field/reference-confounded and NOT comparable across animals** —
  George's electrodes evidently see stronger shared-field / higher raw correlation. **Every
  verdict below is a WITHIN-session contrast against George's own awake baseline; no cross-monkey
  absolute k_eff comparison is made or implied.** The consequence is that George's k_eff *dynamic
  range* is compressed, so an Axis-1 collapse has less room to manifest — read the direction and
  the within-session effect size, not the absolute level.
- **Estimator disagreement (already visible in propofol George):** the winding |z| stays ≈3–3.4
  into deep while the direct circulation |z| falls to ≈1 (below null). Consistent with the Chibi
  finding that **the winding estimator is the weaker/nosier one in ECoG; the direct
  phase-randomized circulation null is the trustworthy readout.** Both are reported.
- **Ketamine George received TWO injections** (a top-up: markers at 41 s and 1352 s, with
  Anesthetized annotated 1417–1869 s). The first injection sets the awake→induction boundary; the
  deep reference is the annotated Anesthetized epoch. The double dose makes the induction unusually
  long and is noted.
- **ECoG grain:** mesoscopic field, not single units (as for Chibi). One session per agent, one
  monkey. Broadband only (band-robustness not established; the two-pole test showed band-lability).

## Propofol George

Continuous Session2: injection @84 s, Anesthetized 785–1335 s. 265 windows.

| t (s) | epoch | k_eff | ρ_Kish | \|DB z\| winding | \|DB z\| circ |
|------:|-------|------:|-------:|----------------:|--------------:|
| 50   | awake     | 7.3 | 0.13 | 3.6 | 6.8  |
| 130  | induction | 7.7 | 0.12 | 3.2 | 6.2  |
| 410  | induction | 5.9 | 0.16 | 2.4 | 1.7  |
| 610  | induction | 7.1 | 0.13 | 4.4 | 0.3  |
| 770  | induction | 7.9 | 0.11 | 3.8 | 0.1  |
| 900  | deep      | 9.0 | 0.10 | 2.6 | 1.2  |
| 1130 | deep      | 7.0 | 0.13 | 2.6 | 0.9  |
| 1330 | deep      | 2.4 | 0.42 | 3.4 | 0.04 |

k_eff (median) does **not** collapse — awake 7.10 → deep **7.88** (rises; wide variance incl.
burst-suppression swings). DB circulation **falls from 5.24 → 1.07, below the ~1.5 null → the
BOUND cell**, while winding drops only to 2.40 (the estimator disagreement the coordinator
flagged; circulation is the trustworthy readout).

## Ketamine George (the decisive test)

Continuous Session2: injection @41 s (+top-up @1352 s), Anesthetized 1417–1869 s. 371 windows.

| t (s) | epoch | k_eff | ρ_Kish | \|DB z\| winding | \|DB z\| circ |
|------:|-------|------:|-------:|----------------:|--------------:|
| 10   | awake     | 6.5 | 0.15 | 4.1 | 5.3  |
| 290  | induction | 7.1 | 0.13 | 3.9 | 3.1  |
| 640  | induction | 5.8 | 0.17 | 5.8 | 9.0  |
| 1360 | induction | 6.8 | 0.14 | 4.9 | 4.3  |
| 1435 | deep      | 7.5 | 0.13 | 2.0 | 1.9  |
| 1585 | deep      | 6.8 | 0.14 | 5.7 | 6.5  |
| 1735 | deep      | 7.4 | 0.13 | 7.4 | 8.8  |
| 1860 | deep      | 7.5 | 0.13 | 4.4 | 7.3  |

k_eff (median) does **not** collapse — awake 5.83 → deep **6.94** (rises). **Both** DB estimators
**RISE and stay well above the ~1.5 null**: winding 3.13 → 4.71, circulation 2.90 → **4.62**.
Deep ketamine **still breaks detailed balance → the COORDINATING cell.** Maintenance is *not*
withdrawn. This is the decisive replication of the Chibi ketamine counter-example.

## Axis levels and transition times (George; within-session, own awake baseline)

| agent | axis | awake | deep | Cliff's δ | p | deep vs ~1.5 null | cell |
|-------|------|------:|-----:|----------:|--:|:-----------------:|------|
| propofol | k_eff (Axis 1) | 7.10 | **7.88** ↑ | 0.51 | 1.5e-3 | — | *no collapse* |
| propofol | DB winding | 3.37 | 2.40 | 0.54 | 7.5e-4 | ≈null | (ambiguous) |
| propofol | **DB circ** (trustworthy) | 5.24 | **1.07** | 0.78 | 9.8e-7 | **BELOW** | **BOUND** |
| ketamine | k_eff (Axis 1) | 5.83 | **6.94** ↑ | 0.44 | 2.7e-7 | — | *no collapse* |
| ketamine | DB winding | 3.13 | **4.71** ↑ | 0.63 | 1.1e-13 | ABOVE | breaks DB |
| ketamine | **DB circ** (trustworthy) | 2.90 | **4.62** ↑ | 0.38 | 8.2e-6 | **ABOVE** | **COORDINATING** |

(Baselines: propofol awake = its own Session2 pre-injection block, n=15; ketamine awake =
Session1, n=95 — ketamine's pre-injection lead-in is only ~1 window, so Session1 is its
within-animal awake reference. Both are within-George; **no cross-monkey comparison is made**.
The **cell is fixed by the DEEP circulation level vs the null**, which is baseline-independent.)

## Ordering verdict (George)

**UNRESOLVED — and, in George, moot.** The framework's dynamical prediction is that maintenance
(γM) withdrawal *drives* a k_eff collapse, so DB should drop before/with k_eff. **But in George
k_eff does not collapse under either agent** (medians rise: PF 7.10→7.88, KT 5.83→6.94), so there
is no structural collapse for a maintenance withdrawal to precede. The reported midpoint-crossings
are crossings of non-collapsing / rising signals and are not meaningful ordering events (PF: k_eff
"cross" 128 s CI[119,647]; KT: DB winding "cross" 438 s CI[62,455] — CIs span the whole induction).
Consistent with Chibi, **the maintenance-before-structure ordering is not supported**; here it is
additionally undefined because Axis 1 never moves.

## TWO-MONKEY VERDICT

**The maintenance-axis 2×2 divergence REPLICATES; the k_eff-collapse correlate does NOT.**

1. **The ketamine counter-example REPLICATES (the decisive claim).** In *both* monkeys, deep
   ketamine keeps its detailed-balance circulation **well above the ~1.5 null** (Chibi deep circ
   |z|≈6.9; George deep circ |z|=**4.62**, winding also rising 3.13→4.71) — ketamine lands in the
   **coordinating cell**, γM is *not* withdrawn. It is **not** an animal-specific artifact.

2. **Propofol → BOUND replicates.** In both monkeys, deep propofol drives the circulation
   |z| **below the null** (Chibi 0.93; George **1.07**) — the **bound cell**, maintenance
   withdrawn. (Winding is the weaker estimator and only partly drops; circulation is decisive.)

3. **So the cross-agent DIVERGENCE — propofol→bound vs ketamine→coordinating — holds across Chibi
   AND George.** Two monkeys, two anesthetics, same qualitative split on the maintenance axis.

4. **BUT the k_eff (Axis-1) collapse is NOT a robust cross-animal correlate of unconsciousness.**
   Chibi's k_eff collapsed cleanly under both agents (14→5–6); **George's k_eff does not move**
   (awake ≈6–7, deep ≈7–8 by median, both agents). George's absolute k_eff sits far lower than
   Chibi's (field/reference confound — George's electrodes see stronger shared structure), leaving
   **no dynamic range for an Axis-1 collapse**. Honestly: in George the entire anesthetic
   discrimination lives in **Axis 2 alone** (bound vs coordinating), with Axis 1 flat for both
   agents — which, read charitably, is itself a clean demonstration of **axis independence** (the
   two anesthetics are separated by maintenance while structure is held fixed), but read strictly
   is a **non-replication of the "k_eff collapse tracks loss of consciousness" reading** and a
   reminder that absolute k_eff is not portable across preparations.

**Net:** the load-bearing finding — that the two anesthetics DIVERGE on the maintenance axis
(propofol withdraws detailed balance → bound; ketamine preserves it → coordinating) — is
**confirmed in a second monkey**. The structural-collapse story is **monkey/preparation-specific**
and must be stated as a within-session contrast, never a cross-animal absolute. The
maintenance-before-structure *ordering* remains **UNRESOLVED/unsupported** in both animals.

## Honest caveats

- Absolute k_eff not comparable across monkeys (field/reference confound) — within-session only.
- ECoG field grain; one session per agent per monkey; broadband only (not band-robustness tested).
- DB winding estimator is weak/noisy in ECoG; the direct circulation null is the trustworthy one.
- Ketamine George's double-injection lengthens induction; deep = the annotated Anesthetized epoch.
- Where the data cannot resolve an ordering, it is scored UNRESOLVED, not manufactured.

*Outputs: `spectral_results_anesthesia_trajectory_george.json` (both agents + baselines +
ordering), `trajectory_windows_{propofol,ketamine}_george.jsonl`,
`baseline_windows_{propofol,ketamine}_george.json`,
`anesthesia_trajectory_ordering_george.json`, `spectral_anesthesia_trajectory_george.png`.
Scripts: `spectral_anesthesia_trajectory.py` (parametrized via TRAJ_TAG/TRAJ_ONLY),
`spectral_anesthesia_george_assemble.py`, `spectral_anesthesia_trajectory_post.py`. Real data
only; no commit.*
