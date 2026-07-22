# The Thirdness re-visit register — where past results need re-examination now that the Third is in hand

**Date 2026-07-20. READ-ONLY sweep; no result file was edited, no experiment re-run, nothing committed.**
Built against the Third tool established today (`papers/notes/the_third_prenup.md` RESULTS,
`formal/CoherenceRatchet/Core/Thirdness.lean`, `Core/TriadicChannel.lean`,
`experiments/cosmo_entropic_potential/thirdness/discriminator/`,
`experiments/f11_verification/coupled_dynamics/`,
`experiments/adversarial_neff/triadic_channel/`).

## The two edges (the instrument the sweep applies)

- **EDGE 1 — false NEGATIVES (hidden Third).** `S = −ln det C` and `k_eff` (PR of the
  correlation spectrum) are **pairwise** (Secondness); the detailed-balance / γM axis is a
  **mode-*pair* winding**. All three are provably blind to genuine ≥3-order coordination, which
  posts `ρ ≈ 0`, `S/2 = 0`, `k_eff = n`, DB-winding `= 0` (the XOR/GHZ witness, `thirdness_line`).
  So any **"null / independent / ρ≈0 / chaos pole / low-rank / no maintenance / books opened
  empty"** verdict drawn from a pairwise instrument is, structurally, a place a Third could hide.
  A pairwise result is *not* automatically wrong — flag only where higher-order structure could
  plausibly change the verdict.
- **EDGE 2 — false POSITIVES (the K4 lesson, HIGHER priority).** A claimed **detection** that
  used a rank / copula / normal-score / higher-order / bispectrum / 3-point / count-in-cell /
  point-catalog / read-count statistic **without a shot-noise-matched (discreteness-matched)
  null** is an artifact suspect. This is exactly how the cosmic ~20% Third died (K4 FIRED): a
  coordination-free **Poisson** null matched to n̄ and P(k) over-reproduced the frozen signal;
  `argsort∘argsort` on empty cells manufactured 37–63%; CIC halved it. A **continuous / Gaussian /
  Haar / phase-randomized / shuffle** null does not control discreteness. The right control is a
  Poisson / library-size / shot-matched null.

Prioritization = **load-bearing-ness × strength-of-reason**. FP suspects listed first.

---

## THE TIED-FRACTION LAW — the triage test (added 2026-07-22, after three re-visits)

The sweep's whole FP edge collapses to one measurable precondition. The copula/rank
higher-order statistic **manufactures signal in proportion to the empty (tied) cell
fraction** — measured directly on the DM particle field across four decades of density:

| empty fraction | 91.5% | 84% | 68% | 42% | 17% | 2.4% | 0% |
|---|---|---|---|---|---|---|---|
| copula skew | +0.50 | +0.41 | +0.29 | +0.17 | +0.11 | +0.088 | **+0.004** |

**Triage rule — do this BEFORE scheduling any re-run.** Measure the tied/empty fraction of the
field the statistic was computed on.
- **Large tied fraction** (tens of %) ⇒ the rank transform will invent structure; the result is
  an artifact suspect and a **shot-matched null is mandatory**.
- **Small tied fraction** (few %) ⇒ the tie-break cannot bite; the result is likely clean.
- Always replace `argsort∘argsort` tie-breaking with **random** tie-breaking, and prefer CIC
  (anti-aliased) over NGP — NGP inflates the tied fraction 5–20× (0.40–0.58 vs 0.02–0.08).

This converts most of the FP list from "re-run each" into "measure one number each."

## RESOLVED (2026-07-21/22)

- **FP-1 `copula_stress` — SURVIVES_AS_STATED.** Re-run vs the shot-matched null: Δw = **−0.0008**
  (frozen continuous-null value −0.0169), tie artifact **2%** vs a 30% threshold, tied fraction
  only 2.4–8.1% (CIC ng=48). The DE bet's Third-defense holds and is *stronger* under the correct
  null. `copula_stress/shot_null/`.
- **FP-2 macaque |z|=8.8 — SURVIVES.** 0/2000 Poisson-count-matched surrogates (outer z ≈ +12.8);
  the count-matched null (1.66) sits *below* the phase-randomized null it replaced (2.22) —
  discreteness works *against* the signal. Bin sweep: real 8.8→47.0 while the null stays flat at
  ~1.7. Two record corrections owed and made (C-1 the published z was a block-bootstrap *t*-stat
  never referenced to a surrogate, the "~1.5 ceiling" was a synthetic OU calibrator; C-2 the
  "44 vs ~1.5" headline should read 44 vs Poisson 1.7 / phase-randomized 11.3).
  `keff_saturation/macaque_poisson_null/`.
- **FN-1 DM particle-field Third (prenup prediction 4) — ANSWERED, NEGATIVE.** Full 94,196,375
  particles, four decades of density, no excess over the shot null at any density, no plateau.
  The Third is empirically **unobserved on the field itself**.
  `thirdness/dm_particle/SUMMARY.md`.

**Net:** the FP edge was *not* a systemic rot — two load-bearing claims survived their correct
nulls, one strengthened. The one dead result (the cosmic Third) died of the tied-fraction
pathology above, now quantified. Remaining FP entries (FP-3…FP-7) should be triaged by tied
fraction first.

## Prioritized register (table)

| # | File / claim | Edge | Load-bearing? | Why a candidate (method-level) | Re-visit test |
|---|---|---|---|---|---|
| **FP-1** | `cosmo_entropic_potential/copula_stress/` — higher-order gap `I_true−I_Gaussian-copula` "small, inverting, z-flat → Δw≲0.02" | FP | **YES** — the Third-defense of the DR3 bet | Measured on a CIC count field vs a **continuous matched-Gaussian-copula surrogate**; K4 shows a continuous null is the wrong control for a discrete field | Re-run the gap vs a **Poisson/shot-matched (S1-style) null** on the count field; confirm the cancel-in-log-derivative still holds |
| **FP-2** | `keff_saturation/spectral_spikes_summary.md` — macaque motor cortex DB **\|z\|=8.8** coordinating | FP (+FN) | **YES** — CLAUDE.md standing result (Axis 2) | Winding-rate on **20 ms spike counts**; null = phase-randomized / block-bootstrap, **not Poisson**; summary itself notes spike-count Poisson shot inflates PR | Re-run winding \|z\| vs a **Poisson-count-matched null**. (Partial defense already on record: signal *strengthens* as shot is smoothed, so discreteness works against it) |
| **FP-3** | `keff_saturation/spectral_cosmo_summary.md` — SDSS count-in-cell δ, power-law α≈0.75 (non-saturating) | FP | minor (self-hedged "grain-inconclusive") | The **exact K4 artifact profile**: count-in-cell, "α is literally a P(k) diagnostic," null = phase-randomized floor, **no Poisson null** | Poisson/shot-matched null before any citation; treat current read as K4-adjacent, non-citable |
| **FP-4** | `cosmo_entropic_potential/pandey_crosscheck/` — MI-min epoch = S-peak (0.02σ AGREEMENT) | FP | medium — registered cross-check (weighted non-supporting, rule 2) | `dG/dlna=⟨(1+δ)ln(1+δ)⟩` extremum on a **discrete halo count field**; nonlinear ln is empty-cell-sensitive (K4 family); locator already had a spline artifact (O1→z=0) | Re-locate the epoch vs a **shot-matched null** and via smoothing-convergence; confirm 0.02σ is not discreteness-shifted |
| **FP-5** | `keff_saturation/spectral_axis_independence_summary.md` + `spectral_grayscreen_db_summary.md` — Allen spike DB \|z\|=4.0 / 4.87 | FP | medium (already downgraded to "consistent with independence") | Spike-count winding/circulation; null = phase-randomization of own data; summary warns "spike shot noise dominates the covariance eigenspectrum" | Poisson-count-matched null for the winding detection |
| **FP-6** | `structural_series/tcga_debiased/RESULTS.md` + `data_tcga/RESULT.md` — tumor chaos-ward ρ drift | FP (+FN) | medium (12-cancer corridor + chaos-drift) | mean\|Pearson\| ρ on **count-derived RNA-seq**; debiased null = per-gene permutation, **not library-size/Poisson**; raw run had **no floor subtraction at all** (flagged by band_calibration) | Library-size-matched (Poisson) null; report absolute band with the discreteness floor removed |
| **FP-7** | `keff_saturation/spectral_immune_summary.md`, `spectral_avalanche_summary.md` | FP | minor / out-of-domain | Read-count clone-size Zipf (null = lognormal) and avalanche-size power-law on 20 ms counts (Clauset MLE) — no shot/library-size null | Shot-matched null if ever promoted; else leave as honest bounds |
| **FN-1** | `dm_coherence/.../gravity_ledger_instrument.md` (r=0.986–0.999) + prenup **prediction 4** | FN | **YES** — CLAUDE.md "dark ≈ light, same books" | The "no NEW dark coordination" null is pairwise + **2-variable** non-Gaussian MI(r) only; ≥3-order dark coordination **explicitly untested and owned**. K4 killed the *tracer* copula-Third; the **DM particle field** (the true discriminator) was never run | **Bounded-arity multi-information / copula 3-point on the DM particle field** vs a **shot-matched null** — this *is* prenup prediction 4, still open |
| **FN-2** | `keff_saturation/spectral_tngsubbox_summary.md` + `spectral_galaxy_summary.md` — "galaxy baryon cycle z≈0 **bound**" | FN | **YES** — CLAUDE.md standing result (Axis 2 negative anchor) | DB = **mode-*pair* circulation** (2-point winding); a purely-triadic maintained circulation (directed 3-cycle in phase space) posts **exactly zero** to it | A **higher-order / triadic entropy-production** (directed-3-cycle) probe on the baryon-cycle field, shuffle-null controlled |
| **FN-3** | `keff_saturation/spectral_zebrafish_summary.md` (+ `structural_series/data_fmri`, `allen_keff_retest`) — complete-brain **k_eff saturation / low-rank corridor** | FN | **YES** — decisive standing result ("corridor is genuine low-rank structure") | A saturating `k_eff` (ρ̄≈0, k_eff=k) is **exactly** what a pure Third also produces; "low-rank" cannot *exclude* hidden ≥3-order coordination. This is prenup **prediction 2** (the corridor's true coordinate is `I_total`, not ρ) | Compute **O-information / bounded-arity multi-information** on the complete unit; confirm the saturation invariant persists on the `I_total` coordinate and the Third is a bounded finite fraction |
| **FN-4** | Corridor **two-axis discriminator** — the "CHAOS" bin (e.g. `spectral_arousal` coma→chaos; `spectral_flocks` ρ≈0; any real-substrate CHAOS verdict) | FN | medium (discriminator is a standing result) | GHZ-X reads **CHAOS** exactly (`quantum_corridor/CALIBRATION.md`, N4) — owned on the **quantum** side by the ≥2-MUB requirement, but **no MUB analog** exists for neural/cosmic substrates, so a GHZ-like Third there is filed as "chaos/independent" | Add an **O-information / synergy channel** to the discriminator so "CHAOS" is separated from "hidden Third" on non-quantum complete units |
| **FN-5** | `cmb_books/` Bet 11 DISSOLVED + `mystery_map.md` §1 past-hypothesis **S_coord≈0** | FN | medium (past hypothesis is in the stance) | 7-functional battery is **2-point/geometric, no bispectrum channel**; `S_coord=−ln det C` with "independent modes ⇒ C≈I ⇒ S≈0" is the exact XOR/GHZ blind spot. **Mitigation on record:** Planck `f_NL=−0.9±5.1` is cited — the bispectrum *is* the higher-order control, bounding a primordial Third externally | Add an explicit **bispectrum/higher-order channel** to make it airtight; or state plainly that the Third-bound is carried by `f_NL`, not by `S_coord` |
| **FN-6** | `coordination_census_bound.md` — "1-in-10⁶ engineered coordination" | FN | medium-low (a bound; null is the content) | The headline is a bound on **off-diagonal ρ (pairwise)** only; a Third-structured engineered coordination evades it via null-space stealth — **already owned** (§5 fence 3), closed only by the thermodynamic rent | State the census reach explicitly as *pairwise-engineered* coordination; the ≥3-order class is out of gravitational scope by theorem |
| **FN-7** | `sm_escalator_mixing/` — PMNS Haar-typical / CKM FN-typical | FN | low (weak) | Typicality read via pairwise instruments (`MI`, `S_onehot=−ln det C`, \|J\|) — but the datum is the **entire fully-specified unitary** (\|V\|² + \|J\|), leaving little room for a hidden ≥3-order distribution | Note only; a Froggatt–Nielsen higher-order copula check is cheap if ever wanted |
| **FN-8** | `p_omega_construction/`, `open_system_pomega/{holographic,tower/recast}`, `cross_rung_shape` — "rungs decouple / EMPTY / TRIVIAL" | FN | low (already covered) | Pairwise `τ = MI` / `ρ_joint = Kish` "decouple" verdicts could hide a block-parity Third — **already re-examined** by `f11_verification/coupled_dynamics/` (block-parity Third exists in-model; the framework's named couplings are Secondness/independent) | None new; folded into the coupled_dynamics scope note |

---

## Notes on the load-bearing entries

**FP-1 (copula_stress) — the highest-value FP because it guards the bet.** The program's reason
to believe the Third does not move `w(z)` is copula_stress tier 3: the higher-order gap inverts
(2-point *over*-reads by ~10%), is redshift-flat, and cancels in `dlnS/dlna` → Δw ≲ 0.02. The
gap was measured against a **matched Gaussian-copula surrogate** (continuous) on a number-CIC
field. That is exactly the null K4 proved insufficient. The conclusion may well survive — K4's
Poisson null *over*-reproduced the tracer Third, which points the same way (no hidden extra
coordination) — but the control that protects the bet must be re-run with the shot-matched null
it currently lacks. This is the one place the DE leg's Third-robustness rests on a wrong-type null.

**The DR3 bet's own S(a) is NOT this artifact (read sideways).** The load-bearing `w(z)` pipeline
uses `C_ij = ξ_R(r_ij)/σ²_R` over actual halo positions — **PSD-safe by the Schur product
theorem, ξ = FT of a non-negative P(k)** (`SUMMARY.md`, `halo_grain`, `large_volume/p4_fence`),
validated to `rel=1e-11`, cap never hit, `λ_min>0` throughout. It is a **model-ξ** construction,
**not** the `argsort∘argsort` normal-score-on-empty-cells that manufactured the cosmic Third; and
op-A explicitly measures and subtracts shot (`A=(Var−shot)/Var`). So the pairwise bet clears the
K4 failure mode by construction. The Third exposure of the bet is FP-1 (the higher-order *defense*),
not the headline number.

**FN-1 (DM particle field) — the highest-value FN because a real physical Third could still live
there.** K4 fired on **tracers** (halos/galaxies) and could not decisively run the DM particle
field; the prenup's own prediction 4 (copula Third on the DM particle field vs shot-matched
surrogate) is the discriminator that separates "real coordination" from "shot artifact," and it is
**unrun**. The load-bearing "dark ≈ light, r=0.986–0.999, no new dark coordination" is a pairwise
+ 2-variable statement; `gravity_ledger_instrument.md` §4/§5 already own the ≥3-order blind spot
and already *discarded a raw-stellar-MI empty-cell-tie artifact* (the pre-K4 precedent of the same
lesson). Closing prediction 4 with a shot-matched null is the single most informative Third test
left on real data.

**FN-2 / FN-3 — the two axes of the discriminator are both pairwise.** Axis 2 (maintenance) is a
2-point winding, so "galaxy baryon cycle z≈0 bound" is a candidate hidden triadic cycle; Axis 1
(structure) is `k_eff`, so a saturating/low-rank read on the complete zebrafish brain cannot rule
out a GHZ-like Third (which also reads low-rank). Neither undoes the standing results — a Third is
not asserted — but both are exactly the "verdict could change under `I_total`" cases the sweep is
meant to surface, and both map onto prenup predictions 2–3.

---

## Clean survivors (read sideways — a clean pairwise result that survives is a clean result)

- **`entanglement_ledger/` Spearman ~1.0.** Rank statistic, but on **40 continuous couplings from
  exact diagonalization** — no discreteness, no empty cells, no counts. Strong internal control
  (conjugate basis → −1.0). Not a K4-type suspect. Its GHZ blind spot (classical S=0 while
  entanglement is maximal) is the *acknowledged home* of the Third, consistent with EDGE-1.
- **`sm_escalator_mixing/` CKM/PMNS + `ckm_ensemble/`.** Pairwise instruments, but nulls are
  **continuous Haar U(3) / Froggatt–Nielsen** — the correct control for continuous unitary draws;
  no shot noise exists to match. The one count-flavored statistic (θ₁₃ look-elsewhere, 12.65%) is
  evaluated on the Haar ensemble (correct). EDGE-2 does **not** bite the flavor result.
- **`cmb_books/` adverse count ~2.7σ.** Count of flagged marginals with an **isotropic-Gaussian-sky**
  null (the correct null), explicitly non-scoring. Not a discreteness artifact. (The Bet-11 EDGE-1
  gap is FN-5, and it is externally closed by `f_NL`.)
- **`bench_suite/` bets 7/8/10.** Third-law ceiling / maintenance / FT on real GPU jitter with FT
  and pre-registered controls; capacity-law reads on pairwise ρ, no higher-order detection and no
  discreteness null needed. Clean.
- **`dark_sector_mass/` KILL, `dm_coherence/sparc` UNDERPOWERED.** No live positive claim to
  overturn (dead on mechanism/magnitude); the SPARC mechanism died on **mean-blindness**, which is
  clause 3, not a Third question. Not re-visit targets.
- **The cosmic Third (`thirdness/`) and the raw-stellar-MI (`gravity_ledger_instrument.md` §4).**
  Already resolved — K4 FIRED on the first; the second was flagged and discarded as an
  empty-cell-tie artifact before K4 (the lesson's in-house precedent).

## Method appendix — the K4 shot-matched null (for the FP re-runs)

The discriminator that fired K4 (`thirdness/discriminator/DECISIONS.md`) is the template for every
FP re-run above: phase-randomize the real δ to a Gaussian with matched `|δ_k|`; form intensity
`μ=n̄(1+δ_G)`, clip at 0; draw `n_cell ~ Poisson(μ)`; grid identically; this matches n̄ and P(k)
with **pure discreteness + non-negativity and no genuine connected HOC**. For read-count substrates
(RNA-seq, repertoire) the analogue is a **library-size-matched** multinomial/Poisson resample. A
detection survives only if it sits **above** this null by a margin that is a large fraction of the
signal — the bar the cosmic Third failed and the bar these re-runs must clear.
