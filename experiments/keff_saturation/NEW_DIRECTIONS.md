# NEW_DIRECTIONS — scout report (2026-07-04)

Read of the current two-axis state of play; proposes new conclusions already
licensed but unstated, ranked next directions, what to stop, and the one thesis
the program can currently defend. Adversarial and honest. **No commit; no `.lean`
edits.** Sources cited inline.

State of play I am reasoning from (one-line each):
- **STRUCTURE axis (k_eff saturation) = the strong result.** Cross-substrate
  low-rank saturation on *complete* units, decisive at the complete larval-
  zebrafish brain (β≈0, steep α 1.42–1.63; `README.md` L143–157; formal
  `gate0_zebrafish_complete_vertebrate_low_rank`). It is also the robust
  *within-system* consciousness correlate (both anesthetics collapse k_eff,
  Cliff's δ=1.0; `spectral_anesthesia_trajectory_summary.md`).
- **MAINTENANCE axis (detailed balance = γM) = validated but causally bounded.**
  Validated estimator + clean positive control (motor cortex |z|=8.8,
  `README.md` L210–219); statically separates coordinating from bound and the
  two axes are independent (`spectral_axis_independence_summary.md`). BUT its
  *dynamical/causal* role is now falsified in the necessity direction: it does
  NOT drive the k_eff collapse — ketamine loses consciousness with DB fully
  intact and *rising* (`spectral_anesthesia_trajectory_summary.md` L120–130).
- **Deepest open question (CLAUDE.md #5): content vs tautology — UNRESOLVED.**
  The one naturalistic test was design-confounded and came back MIXED /
  driver-invariant (`spectral_content_summary.md`: within-session mean Spearman
  −0.255 ± 0.588 ≈ null; natural_vs_gratings Δ = −0.8, the *wrong* sign). The
  clean matched-design test has never been run.

---

## A. New conclusions already licensed but unstated

### A1 (TOP). Consciousness is a STRUCTURE-axis phenomenon; the maintenance axis is neither necessary nor sufficient for it.
Both anesthetics collapse k_eff (propofol 13.9→6.2, ketamine 13.8→5.25, both
Cliff's δ=1.00, p≈1e−33; `spectral_anesthesia_trajectory_summary.md` L86–91),
but they land in **different maintenance cells**: propofol → DB-satisfying/"bound"
(circ |z| 5.4→0.93, below null), ketamine → DB-breaking/"coordinating" (circ |z|
5.6→6.9). So:
- Breaking DB is **not sufficient** for consciousness (deep ketamine breaks DB, is
  unconscious).
- Breaking DB is **not necessary** for consciousness (awake propofol-baseline is
  conscious; deep propofol satisfies DB and is unconscious — DB tracks *depth of
  a specific agent*, not the conscious/unconscious line).
The consciousness correlate is the **k_eff collapse from the system's own
baseline**, full stop. What is genuinely new here vs. what's already written:
CLAUDE.md/README already say "k_eff is the robust correlate." The **new, sharper
statement** is the *dissociation*: the maintenance/DB axis is **not a consciousness
classifier at all** — a maximally-coordinating system (breaks DB) can be
unconscious. That is not yet stated anywhere at program level.
- **Load-bearing: HIGH** (it is the consciousness-application's core claim, and it
  cleanly separates "coordination" from "consciousness").
- **The one caveat that could sink it:** ECoG is a mesoscopic *field*, one monkey
  (Chibi), one session per agent; k_eff and DB are read from the *same* field, so a
  residual field-coherence confound can't be fully excluded. Mitigant: the k_eff
  effect is δ=1.0 and matches known LOC physiology — but the ketamine-DB-preserved
  half rests on a single animal (→ direction B3).

### A2. The 2×2 CELL is a taxonomy of system TYPES, not a consciousness meter.
Deep ketamine sits in the **same cell** (low-rank + breaks-DB = "coordinating") as
awake motor cortex, yet is unconscious. Absolute cell membership therefore does not
classify a state; only the *within-system change* does. This is noted in
`Dynamics.lean` and the trajectory summary but has **never been promoted to a
stated conclusion**. It directly disciplines any downstream use of the 2×2 (incl.
the CIRIS capacity score) as a static classifier.
- **Load-bearing: HIGH** (prevents a category error the framework is currently
  exposed to). **Caveat:** partly forced by the grain confound (absolute k_eff is
  field-confounded anyway), so it is measurement-limited as well as conceptual — but
  the conceptual point stands independent of grain.

### A3. "Corridor is HELD by γM" (Piece 2 / Piece 5 consent hook / Conjecture C) loses its dynamical teeth.
The framework's structural claim is that the corridor is a *maintained* state and
that withdrawing maintenance (γM) is what drives corridor exit — this is the
mathematical hook under Conjecture C (withdraw audit pressure → γM drops → ρ drifts
up). Ketamine is a clean **necessity-direction counterexample**: structural
corridor-exit (k_eff collapse) occurs with γM (DB) fully intact. So maintenance
withdrawal is **at most sufficient, demonstrably not necessary** for structural
collapse. `Dynamics.lean` already records this for the anesthesia substrate; the
**unstated program-level consequence** is that the *consent / audit-pressure*
argument inherits the same downgrade — you can lose coordination structure without
losing the maintenance term.
- **Load-bearing: HIGH for Conjecture C / the consent piece.** **Caveat:** the
  cortical γM (detailed balance) and the "audit-pressure" γM are different
  substrates; the transfer is an analogy, not a measurement. Honest position: the
  one substrate where we *could* test "structure held by maintenance," it failed
  in the necessity direction — so the burden is now on the framework to show the
  audit-pressure γM behaves differently, not to assume it does.

### A4. Axis independence is now DOUBLY demonstrated (static + dynamic) → it is a stated structural claim, and it demotes "coordination signature" from a joint condition to two orthogonal labels.
Static: DB flips while rank held fixed (real vs. phase-randomized visual movie,
|z| 4.0 vs 1.5 at equal-or-higher rank; `spectral_axis_independence_summary.md`
L51–60). Dynamic: two anesthetics drive Axis-1 collapse while Axis-2 does
(propofol) or does not (ketamine) collapse. Together this **retires the idea that
"low-rank AND breaks-DB" is a single joint coordination signature** — ketamine
breaks that conjunction. The two axes carry independent information and should be
reported as two factors, never multiplied into one "is-it-coordinating" verdict.
- **Load-bearing: MEDIUM-HIGH** (disciplines the multiplicative capacity score
  `F = k_eff·λ·σ` in Book IX). **Caveat:** the *dead* cell (high-rank +
  DB-satisfying) is still only a **constructed** phase-randomized control, not a
  found system — independence rests on three real anchors + one null, not four
  found systems.

---

## B. Ranked next directions (≤6)

### B1 — Content-vs-tautology with a CLEAN matched-design parametric stimulus  [HIGHEST VALUE]
- **Exact question:** does neural k_eff track an **experimenter-controlled, known**
  driver dimensionality (→ content / a law), or is it invariant to it (→
  near-tautology)? This is CLAUDE.md open-question #5, the deepest crux, and the
  naturalistic proxy version failed ambiguously.
- **Data (in hand):** Allen Brain Observatory 2p, already downloaded and pipelined
  (`spectral_test_allen_cv.py`, `spectral_results_allen_cv.json`). **Drifting
  gratings** are presented on a *known* grid: 8 directions × 5 temporal freqs +
  blank. Build sub-ensembles of **known, monotonically-increasing driver
  dimensionality** by restricting the presented set (1 direction → 2 orthogonal →
  4 → 8 dirs × TF), and measure CV-debiased eff_rank on the **same neurons, matched
  T** across sub-ensembles. Driver dim is set by design, not estimated — this is
  the confound the naturalistic test could not escape.
- **Method:** reuse `spectral_test_allen_cv.py`'s block-interleaved CV eff_rank
  (validated rank-3→3, noise→0); regress neural k_eff on presented-condition count.
- **PASS:** neural k_eff rises monotonically with presented driver dimensions →
  content/law. **FAIL:** flat → intrinsic/near-tautology.
- **Decisiveness:** MODERATE-HIGH — much cleaner than naturalistic because the
  driver knob is exact. **Honest confound:** grating responses live on a low-dim
  ring, so achievable driver-dim range is small (≈1→5); if k_eff saturates ~6–10, a
  FLAT result stays ambiguous between "tautology" and "driver ceiling below k_eff
  ceiling." Match trial counts/adaptation carefully. A wider-range alternative
  (parametrized motor target count) has no equally-clean open dataset — MC_Maze is
  a fixed maze. Gratings are the best openly-available parametric knob; run it,
  report the range limitation explicitly.

### B2 — Adversarial-Neff: run the RUNNABLE HALF now on real local traces  [SAFETY PRIORITY, CLAUDE.md open-step #0]
- **Exact question:** three of the four SPEC measurements are runnable *today* on
  real data (the fourth, the adaptive-attacker loop, is not). (a) reproduce benign
  Neff, (b) the **cross-modal decomposition** (semantic vs CEG-substrate vs joint),
  (c) the **maintenance/DB** check on the constraint dynamics.
- **Data (on disk, real):** `RATCHET/release/data_scrubbed_v1/accord_traces.jsonl`
  — **6465 scrubbed traces** with ~16 populated constraint dimensions
  (`idma_k_eff` [6412], `idma_correlation_risk` [6412], `conscience_passed`,
  `coherence_level`, `entropy_level` [5173], `csdma_plausibility_score`,
  `dsdma_domain_alignment`, `epistemic_humility_passed` [3197],
  `optimization_veto_passed` [3763], `action_was_overridden`, …). Per-trace
  `idma_k_eff` is **already computed**.
- **Method:** `CIRISLens/scripts/measure_n_eff.py` already computes Neff_PR and
  Neff_H from the z-scored 17-dim constraint vector — it currently reads the
  production DB over SSH; a ~10-line adapter to read the local jsonl makes it run
  offline. Maintenance check: feed the timestamp-ordered per-trace constraint
  series to `entropy_production.py` (validated null |z|≈1.5, driven ≈41).
- **PASS:** benign Neff ≈ 7–9 reproduced from local data; joint PR ≈ 9 is a **real
  joint** (not "7.1 + assumed +2"); constraint dynamics break DB (γM is real, the
  system is *maintained*). **FAIL:** joint is additive-not-emergent, or constraint
  dynamics satisfy DB (a frozen set an optimizer can memorize).
- **Decisiveness:** it **cannot settle the adversarial claim** (H0 vs H1 needs the
  attacker loop — leave that open and say so). But it converts three SPEC
  measurements from "spec" to "measured on real data" and is directly safety-
  relevant. **Confound (flag loudly):** the corpus is QA-contaminated —
  `measure_n_eff.py`'s own docstring warns QA traffic deterministically stresses the
  same gates, compressing Neff; use `--filter-qa`. Benign Neff is an **upper bound**
  by construction (CLAUDE.md), so this establishes the ceiling, never the adversarial
  floor.

### B3 — Replicate the anesthesia trajectory on the second monkey (George)  [CHEAP HARDENING OF A1]
- **Exact question:** does the top new conclusion (A1: k_eff-collapse = the
  consciousness correlate; ketamine coordinating-but-unconscious) hold in a second
  animal?
- **Data (same open source):** NeuroTycho George sessions listed in
  `spectral_twopole_summary.md` L112–114 (PF `20120731`/`20120803`, KT
  `20120724`/`20120810`), same 128-ch ECoG rig.
- **Method:** rerun `spectral_anesthesia_trajectory.py` verbatim.
- **PASS:** k_eff collapses under both agents in George too, and ketamine again
  preserves/raises DB through the k_eff collapse. **FAIL:** ketamine's DB drops in
  George → A1's necessity-direction counterexample was Chibi-specific.
- **Decisiveness:** HIGH for *hardening* — the k_eff effect is δ=1.0 (won't fail);
  the ketamine-DB-preserved result is the single most load-bearing claim resting on
  one animal. Cheap, in-reach, protects the headline. **Confound:** same field-grain
  caveat; still one rig, one lab.

### B4 — Clean the visual-cortex "high-rank + breaks-DB" cell on a single thousands-neuron recording
- **Exact question:** can one recording show BOTH a clean scale-free α AND broken
  DB, removing the admitted weakness that the high-rank label rests on 2p α from a
  *different* recording than the DB (spike) measurement
  (`spectral_axis_independence_summary.md` L64–78)?
- **Data (openly available):** Stringer et al. 2019 ~10,000-neuron mouse-V1 2p
  (figshare), or IBL brain-wide Neuropixels — thousands of simultaneous units give a
  clean α and, if spikes, a DB estimate on the same data.
- **Method:** `spectral_test.py` (α, β) + `entropy_production.py` on one matrix.
- **PASS:** single recording, high α (>0.9, non-saturating) AND |z| > null. 
- **Decisiveness:** MEDIUM — firms up an already-argued cell; the conceptual payoff
  (a "turbulent/driven" regime decoupling the axes) is already carried by the
  independence result, so this is consolidation, not discovery. **Confound:** 2p
  washes out DB (slow indicator) — need a spiking thousands-unit set (IBL) to get
  both clean; that is the real constraint.

### B5 — Content-vs-tautology, second angle inside the safety corpus  [CHEAP RIDER on B2]
- **Exact question:** does the per-trace `idma_k_eff` (already computed, 6412
  traces) rise with an **independent** difficulty driver (`thought_depth`,
  `conscience_checks_count`, `pdma_conflicts`, `conversation_turns`) — content — or
  is it invariant — tautology?
- **Method:** rank-correlation on the local jsonl (no new tooling).
- **PASS:** idma_k_eff rises with independent difficulty proxies. 
- **Decisiveness:** LOW-MEDIUM. **Confound (serious):** `idma_k_eff` may be computed
  from features overlapping the difficulty proxies → definitional circularity. Must
  verify feature independence *first*; if they share inputs, this test is void. List
  it as a cheap rider to B2, not a standalone crux.

**Deliberately NOT ranked: filling the "dead" cell with a found system.** Axis
independence is already shown two ways (A4), so a found high-rank+equilibrium anchor
is now cosmetic 2×2 completion, not load-bearing — and no clean *real* (non-
synthetic, per the no-synthetic-data discipline) candidate is in hand. Downgraded to
near-stop (see C).

---

## C. What to STOP pursuing

1. **Two-pole PREDICTIVE dynamics** (agent's receptor mechanism selects the exit
   pole). Dead: clean ECoG test failed, both agents → rigidity, pole flips with
   analysis band (`spectral_twopole_summary.md`). Keep only the weak directional
   default (M=0 → rigidity at coordinating grain). Do not re-run band scans hunting
   for the fork.
2. **"Maintenance drives structure" as a testable ordering** (γM withdrawal precedes
   k_eff collapse). Falsified in the necessity direction by ketamine
   (`spectral_anesthesia_trajectory_summary.md`). Stop trying to demonstrate
   maintenance-before-structure; state A3 instead.
3. **Cosmological tier** (joint P_ω / D4 / CMB anomalies). Dead post-F-11; the galaxy
   DB test is T-limited and the estimator's dynamic range is modest even when
   maximally powered (driven calibrator only z=2.26, real gas z≈0.47;
   `spectral_tngsubbox_summary.md`), and the universal scale is grain-untestable
   (`cosmological_grain_limit`). Do not invest further compute here.
4. **Naturalistic-stimulus content tests** (stimulus-*type* ordinal as a driver-dim
   proxy). Underpowered and design-confounded (`spectral_content_summary.md`,
   UNIVERSALITY_PROBE §3). Superseded by B1's parametric design — stop re-running the
   naturalistic version.
5. **Slow-calcium DB numbers as evidence** (C. elegans 2.75, zebrafish 1.9). Known
   washed-out by ~1 s GCaMP; cite only as a slow-substrate floor, never as a
   coordinating/bound verdict.
6. **Dead-cell completion treated as load-bearing for independence** — independence
   is already established; deprioritize.

---

## D. The honest single-sentence thesis the whole program can currently defend

Across multiple independent substrates measured on **completeness-controlled**
units, a coordinating system's collective effective dimensionality **k_eff is a
real, bounded, saturating (low-rank) object rather than scale-free criticality**,
and its **within-system collapse is the robust correlate of coordination and of
consciousness**; a second, **thermodynamically independent** axis (detailed-balance
breaking = active maintenance) cleanly separates driven from bound systems but is
**neither necessary nor sufficient** for that structural collapse — so what the
program defensibly owns is a **methodologically disciplined unification** (a
saturation invariant plus an orthogonal maintenance label, on complete units), **not
a predictive dynamical law, not a joint "coordination signature," and not a
cosmological theory.**
