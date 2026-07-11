# retention_v2 — adversarial audit of the SHM-anchor hit

**Adversarial-validation pass, 2026-07-10.** Goal: break the retention_v2 hit before it is
believed. The hit under test: cumulative-threshold scan, 10 thresholds logspace(1e11→1e13)
Msun/h on TNG300-1; DESI-fit quality (Mahalanobis to DR2 + real DR2 likelihood chi2)
extremizes at log10-thr = **11.89** (maha 1.156, chi2−LCDM = −1.445), 0.09 dex from the
SHM stellar-retention peak (~10^11.8 Msun/h), degrading monotonically on both sides.

All pass/fail criteria below are **pre-stated before running the corresponding control**
(confirmation-mode discipline on a claim boundary). Every outcome — including ones that
vindicate the hit — is reported. Over-killing an audit is the same error as over-reading a
positive.

## The scan as it stands (from results.json)

| log-thr | cap_limited | n_capped/26 | z_peak | maha | chi2−LCDM |
|--------|-------------|-------------|--------|------|-----------|
| 11.00 | yes | 26 (fully) | 3.008 (endpt) | 3.697 | +3.408 |
| 11.22 | yes | 26 (fully) | 3.008 (endpt) | 4.071 | +0.800 |
| 11.44 | yes | 25 | 3.008 (endpt) | 4.089 | +0.954 |
| 11.67 | yes | 23 | 2.002 (endpt) | 4.256 | +0.782 |
| **11.89** | **no** | **0** | **0.546** | **1.156** | **−1.445** |
| 12.11 | no | 0 | 0.503 | 1.971 | −0.551 |
| 12.33 | no | 0 | 0.273 | 2.105 | +4.027 |
| 12.56 | no | 0 | 0.273 | 4.126 | +16.610 |
| 12.78 | no | 0 | 0.153 | 6.596 | +39.235 |
| 13.00 | no | 0 | 0.000 (endpt) | 9.349 | +70.574 |

The extremum sits at the **first fully-uncapped threshold**. That is C1's problem, stated in
the data: the cap boundary and the claimed physical peak coincide.

---

## C1 (SHARPEST) — is the peak the k-budget sweet spot, not SHM physics?

**Artifact hypothesis.** Below 11.89 the cap (38000) subsamples S(a) into a distorted,
fixed-k series (z_peak pinned at the 3.008 endpoint, poor fits). Above 11.89 falling k
degrades the estimator. The "peak" at 11.89 is then just the first threshold where you stop
subsampling — a k-budget sweet spot — not the SHM scale.

**Decisive control.** Rerun {11.67, 11.89, 12.11, 12.33} with the cap **lowered to 20000**.
At cap=20000: 12.33 (max n_above 12129) stays fully uncapped and IDENTICAL to the main run
(maha 2.105); 11.89 becomes capped at ~22/26 snaps; the first-fully-uncapped boundary moves
up to 12.33. Seeds per the DECISIONS formula (SEED_BASE + 1000·thr_index + snap, original
indices 3/4/5/6).

**PASS/FAIL (pre-stated).**
- If the fit-quality extremum **FOLLOWS the cap boundary** — i.e. min-maha (and min-chi2)
  among the four now lands at ~12.33 (the new first-uncapped), and capped-11.89 degrades to
  worse than 12.33 — the artifact hypothesis is **CONFIRMED**; the hit dies as an SHM anchor.
- If the extremum **STAYS at 11.89** even while it is now capped (capped-11.89 maha still
  the minimum of the four, still < 12.33's 2.105), the SHM anchor **survives C1**.

## C2 — is the above-side degradation just falling k (estimator noise)?

**Hypothesis.** 12.11→13.0 degrade because k falls (12.33 has k~12k, 13.0 k~2.5k), so the
log-det estimator gets noisier; the extremum's right shoulder is a k artifact, not physics.

**Control.** At 11.89, subsample halos at each snapshot down to 12.33's per-snapshot count
(k-profile matched to 12.33), 3 independent seeds (seed = SEED_BASE + 100000·rep + snap).
Recompute full S(a) → (w0,wa) → maha/chi2.

**PASS/FAIL (pre-stated).**
- If k-matched-11.89 chi2 degrades to **≈ 12.33's (14.35 ± ~2 across seeds)**, the above-side
  degradation is a k-count artifact → the extremum's shape is not physical (different-k, not
  different-population).
- If k-matched-11.89 chi2 stays **clearly better than 12.33 (< ~12, i.e. toward 11.89's full
  8.87)**, the degradation above is driven by the halo *population* (mass), not the count —
  the extremum shape is physical.

## C3 — look-elsewhere: how surprising is "0.09 dex" on this grid?

**Control (pure arithmetic, no GPU).** Grid spacing is 0.222 dex; the nearest grid node to
10^11.8 is 11.89 (0.089 dex away) by construction. Cap-censoring removes 11.00/11.22/11.44/
11.67 from clean eligibility (4 of 10). Compute the null probability that the extremum of a
10-point (or 6-eligible-point) scan lands within 0.3 dex of 11.8, and that it lands on 11.89
specifically. Report the honest per-trial significance of "0.09 dex."

**PASS/FAIL (pre-stated).** Report only; this reframes, does not kill. Flag as WEAK if
P(land on 11.89 | uniform over eligible) ≳ 0.15 (i.e. the agreement is barely better than
"the extremum hit the grid node closest to the target, which any extremum near the target
must"). Flag as INFORMATIVE only if the target band excludes most of the eligible grid AND
the extremum is sharp (Δmaha to neighbors large).

## C4 — SHM peak provenance and the h-factor

**Control (WebSearch, verify citations).** Verify the SHM efficiency peak halo mass against
Behroozi+2013 / Moster+2013 / Girelli+2020: peak location, uncertainty, and crucially
**whether it is quoted in Msun or Msun/h** (h=0.674 → 0.15 dex shift, which is *larger* than
the claimed 0.09 dex agreement). Adjudicate whether 10^11.8 Msun/h is the correct conversion
of the literature peak and whether the agreement is robust to, or an artifact of, the h-factor.

**PASS/FAIL (pre-stated).**
- If the literature peak, correctly converted to Msun/h, lands in **11.7–12.0** (bracketing
  11.89 within its own uncertainty), the SHM reference is sound.
- If the correct conversion lands **outside 11.6–12.05**, or if the claimed 11.8 arose from a
  missing/double-applied h-factor that happens to land near 11.89, the agreement is an
  h-bookkeeping artifact and the anchor is unsupported.

## C5 — deflation-by-identity: is the SHM agreement the same fact as the mechanism result?

**The three facts.**
(a) SHM efficiency peaks at ~10^11.8 Msun/h (feedback physics — Behroozi/Moster).
(b) In this pipeline the S(a) crossing epoch = the formation/assembly epoch of
    above-threshold halos (the program's own k(a)-peak mechanism); higher threshold → later
    peak → lower z_peak (confirmed in the scan: z_peak monotone-decreasing in threshold).
(c) DESI DR2 wants a phantom crossing at z ≈ 0.4–0.6.

**Challenge.** The best-fit threshold is whatever makes the pipeline's crossing land at
z~0.5. That is fixed by (b)+(c) ALONE — "which halo mass assembles at z~0.5" — with **no SHM
input**. And that best-fit threshold (10^11.89) is essentially the SAME threshold
(7.74e11) as large_volume's already-frozen "corner" (7.425e11, 10^11.87) — 0.02 dex apart.
So retention_v2's extremum re-finds the pipeline's pre-existing threshold; the only *new*
claim is that this threshold ≈ the SHM peak.

**Deliverable (no pass/fail — a dependency graph).** State honestly: which edges are
circular (best-fit-threshold = corner = what the pipeline already used), which is genuine
consilience (SHM-peak mass coinciding with the assemble-at-z~0.5 mass), and what single
observation would *separate* SHM-driver from formation-epoch-driver (e.g. a regime where the
SHM-peak mass and the assemble-at-z~0.5 mass diverge). Verdict: is SHM a driver or a passenger.

---

# OUTCOMES

## C3 — look-elsewhere (COMPLETE)

Grid spacing 0.222 dex; nearest node to 10^11.8 is **11.89 at 0.089 dex — by construction**
(any extremum landing on the target's nearest grid node is ≤0.11 dex, guaranteed). Within
0.3 dex of 11.8: {11.67, 11.89} of the full 10; only {11.89} of the 6 uncapped-eligible
nodes (12.11 is 0.311 dex, just outside).

Per-trial null (extremum equally likely on any eligible node):
- P(extremum on 11.89 | uniform over 6 eligible) = **1/6 ≈ 0.167 (~0.97σ one-sided)**
- P(within 0.3 dex | uniform over 6 eligible) = 1/6 ≈ 0.167 (0.97σ)
- P(on 11.89 | uniform over all 10) = 0.10 (1.28σ); P(within 0.3 dex | all 10) = 0.20 (0.84σ)

**Verdict: WEAK on its own** (meets my pre-stated WEAK flag, P ≳ 0.15). The "0.09 dex" number
is not independent evidence — it is arithmetically forced once the extremum is anywhere near
the target, because the target sits 0.09 dex from a grid node. The honest per-trial
significance is ~1σ. The hit cannot lean on 0.09 dex; it must lean on the extremum being
*genuinely* at the target (C1/C2), on SHM provenance (C4), and on non-circularity (C5). One
mitigant: the extremum IS sharp on the resolved (upper) side — Δmaha 11.89→12.11 = 0.82,
→12.33 = 0.95, monotone up to 9.35 at 13.0 — but the lower side is censored by the cap (C1),
so we only see half the profile cleanly.

## C4 — SHM peak provenance and the h-factor (COMPLETE)

Literature (verified): **Moster+2013** — peak star-formation efficiency at halo mass
**10^11.8 M⊙ (physical) at z=0**, rising to 10^12.5 M⊙ by z=4 (efficiency 23%→9%).
**Behroozi+2013** — most efficient halos ~**10^12 M⊙ (physical)**, roughly constant 0<z<4.
Both quote **physical M⊙, not Msun/h.**

h-factor adjudication (h=0.6774, M[Msun/h] = M[Msun]·h, shift −0.169 dex):
- Moster z=0: 11.80 M⊙ → **11.63 Msun/h**; Behroozi z=0: 12.00 M⊙ → **11.83 Msun/h**.
- DECISIONS.md listed Moster z=0 = 11.60, Behroozi z=0 = 11.80 Msun/h → **the conversion was
  applied, and in the right direction and magnitude.** The reference "10^11.8 Msun/h" =
  physical 10^11.97 M⊙ = the Behroozi z=0 peak. Sound.
- The hit at 11.89 Msun/h = **10^12.06 M⊙ physical** — sits essentially ON the Behroozi z=0
  peak (12.0) and within the Moster z=0→0.5 evolution. The pipeline's assembly/crossing epoch
  is z≈0.5, so the physically apt comparison is the z≈0.5 SHM peak (~10^11.9–12.1 M⊙), which
  brackets the hit.

**Verdict: PASSES — the anchor is NOT an h-bookkeeping artifact.** The h-factor is correctly
applied; the agreement holds in both unit systems (11.89 vs 11.63–11.83 Msun/h, or 12.06 vs
11.8–12.0 M⊙). **Caveat (surfaced):** the SHM peak is a z-dependent BAND, not a point —
~0.3 dex wide over z=0→2, and DECISIONS' z=0.5 Moster entry (11.92 Msun/h) reads ~0.1 dex
high vs a direct read of Moster's evolution (~11.75–11.8 Msun/h at z=0.5). The precision
implied by "0.09 dex" oversells a comparison whose target legitimately spans ~0.2–0.3 dex.
The right claim is "the pipeline threshold lands inside the SHM-peak band," not "0.09 dex."

## C5 — deflation-by-identity (COMPLETE — dependency graph)

**The circular edge (load-bearing).** retention_v2's DESI-fit extremum at 11.89 (7.74e11) is
0.02 dex from large_volume's already-frozen "corner" threshold (7.425e11, 11.87). Worse for
independence: the corner rule is *defined* as "lowest threshold whose peak k(a) reaches the
cap," i.e. it is pinned to the same cap boundary at which retention_v2's extremum sits. So
"DESI-fit quality is best at ~10^11.9" is **not new** — it is large_volume's 1.36σ corner
result re-derived on the same box with the same pipeline at essentially the same threshold.
retention_v2 adds no independent evidence that the pipeline fits DESI.

**What IS new = the consilience claim.** The only novel content is that this
pipeline-preferred threshold coincides with the SHM efficiency peak. Dependency graph:

- Edge (b)+(c) → best-fit threshold: the pipeline's crossing epoch = the assembly epoch of
  above-threshold halos (program's own k(a)-peak mechanism; z_peak monotone-decreasing in
  threshold, confirmed in the scan). DESI wants crossing z≈0.5. Therefore best-fit threshold =
  "the halo mass that assembles at z≈0.5" — fixed by ΛCDM growth + the S(a) map + DESI, with
  **zero SHM input.**
- Edge (a) → SHM peak: set by baryonic feedback (SN below, AGN above ~10^12 M⊙). **Independent
  physics**, no reference to structure-growth timing or DESI.
- The consilience: [assemble-at-z≈0.5 mass] ≈ [SHM-peak mass] ≈ 10^11.9. These are set by
  DIFFERENT physics, so the coincidence is **genuine consilience, not an identity** — and the
  pre-registered test **could have failed** (SHM could have peaked at 10^13; the pipeline
  would still fit DESI at ~10^11.9 and the anchor would have returned the allowed null).

**Verdict: SHM is a PASSENGER, not a driver.** The DESI fit is produced entirely by assembly
epoch + DESI; SHM does no causal work in it. SHM supplies a *reason the unit scale might be
special* ("maximal history storage") but is not needed to produce the result, and the
"extremum fits DESI" half is not independent of prior work. The consilience is real and not
guaranteed, but it is one coincidence of two numbers, at ~1σ look-elsewhere (C3), on a single
box.

**The single separating observation** (SHM-driver vs formation-epoch-driver): vary baryonic
feedback while holding the DM assembly fixed — e.g. CAMELS SN/AGN-feedback variations, which
move the SHM peak by design but leave the DM halo assembly (hence the pipeline's
position-only S(a) and its z_peak) essentially unchanged. If the pipeline best-fit threshold
**stays put** while the SHM peak moves, SHM is confirmed a passenger. If it **tracks** the
shifted SHM peak, SHM is a genuine driver. Equivalently: a probe preferring a crossing at a
different epoch (say z≈1.5) moves the assemble-at-that-epoch mass DOWN while the SHM-peak mass
at that epoch moves UP — opposite directions — so the two hypotheses diverge and are
distinguishable. Until one of these is run, the SHM anchor is a suggestive coincidence, not an
established derivation of the unit scale.

## C1 — cap lowered to 20000 (COMPLETE) — **ARTIFACT CONFIRMED, hit dies as SHM anchor**

| log-thr | n_capped/26 | z_peak | maha | chi2−LCDM | (main-run cap38k) |
|--------|-------------|--------|------|-----------|-------------------|
| 11.67 | 25 | 3.008 (endpt) | 4.790 | +1.379 | (4.256 / +0.782) |
| **11.89** | **23** | **2.002 (endpt)** | **4.531** | **+0.623** | **(was 1.156 / −1.445, uncapped)** |
| 12.11 | 15 | 0.817 | **2.065** | +0.665 | (1.971 / −0.551) |
| 12.33 | 0 | 0.273 | 2.105 | +4.027 | (2.105 / +4.027, identical) |

**The extremum FOLLOWED the cap boundary — exactly the pre-stated artifact-confirmed
condition.** With cap=20000 the min-maha moves up to **12.11 (2.065) / 12.33 (2.105)** — the
new nearly-/fully-uncapped thresholds — while **11.89, now 23/26 capped, collapses from maha
1.156 to 4.531** and its z_peak jumps from the DESI-matching 0.546 to a bad near-endpoint
2.002. The interior-peak/DESI-fit that made 11.89 the "hit" is **not a cap-independent
property of the 10^11.9 halo population**; it is present only when those halos are sampled at
k ≳ 30–36k (cap=38000, where 11.89 is uncapped) and vanishes at k~20k. The best-fit threshold
is set by **where the cap bites**, i.e. by the k-budget (16 GB GPU, cap=38000), not by a fixed
physical mass scale. Move the cap by a factor <2 and the "SHM scale" moves ~0.3–0.4 dex
(11.89 → 12.1–12.3). **The 10^11.8 coincidence is a coincidence of the current cap value.**

## C2 — k-matched 11.89 → 12.33 counts, 3 seeds (COMPLETE) — **k-artifact CONFIRMED, exceeded**

| rep | z_peak | maha | chi2−LCDM |
|----|--------|------|-----------|
| 0 | 0.273 | 3.404 | +9.438 |
| 1 | 0.503 | 2.701 | +7.886 |
| 2 | 0.361 | 1.842 | +5.852 |
| **mean** | — | ~2.65 | **+7.73** |

(full-11.89 = −1.445; 12.33 = +4.027)

Thinning 11.89's halos at each snapshot down to 12.33's per-snapshot count degrades its fit
from chi2−LCDM = **−1.445 to a mean +7.73** — i.e. **not merely down to 12.33's +4.027 but
PAST it** (worse than 12.33 on chi2 in all three seeds; z_peak wanders 0.27–0.50 with large
seed-to-seed scatter). The pre-stated "k-artifact" branch is met and exceeded: 11.89's
superiority over higher thresholds in the main scan is a **k-count effect, not a
halo-population/mass effect.** Matched on the number of halos, the SHM-peak-mass population is
no better than — is worse than — a 0.44-dex-more-massive population. The signal is the k, not
the mass.

---

# OVERALL VERDICT

| challenge | result | effect on the SHM-anchor reading |
|-----------|--------|----------------------------------|
| C1 (cap→20000) | **artifact CONFIRMED** (pre-registered) | **decisive kill**: extremum tracks the cap, not the mass |
| C2 (k-matched) | **k-artifact CONFIRMED** (pre-registered) | **decisive kill**: 11.89's edge is k-count, not population |
| C3 (look-elsewhere) | WEAK (~1σ per-trial) | "0.09 dex" is not independent evidence |
| C4 (SHM provenance/h) | **PASSES** | the SHM reference itself is correctly located; NOT an h-artifact |
| C5 (deflation) | SHM = **passenger** | "fits DESI" not independent of the corner; SHM does no causal work |

**Survival probability of the SHM-ANCHOR reading (that the DE unit mass scale is *fixed by
retention physics* at 10^11.8): ~10%.** C1 and C2 — both pre-registered, both fired — show the
extremum location is set by the computational k-budget (cap), not by a physical mass scale:
lower the cap and the "best" threshold moves ~0.3–0.4 dex; match the k and 11.89 loses its
advantage entirely. The one clean pass (C4) establishes only that the SHM peak is genuinely
near 10^11.8–12.0 — it does not rescue the *anchoring* claim, because the pipeline's extremum
does not robustly sit there. The ~10% residual is for the untested possibility that a proper
**P4 intensive fence (fixed-k across all thresholds)** could re-expose a cap-independent
extremum near the SHM scale; that fence was **not** applied across thresholds in this scan and
is the required next step before any retention-anchor claim can stand.

**Escalation (beyond the SHM claim).** C1/C2 show the interior-peak / DESI-fit signal is a
high-k feature (needs k ≳ 30k at low z) that does not survive k~20k or k-matching. Because
large_volume's headline 1.36σ corner sits at the same cap boundary, its result should be
re-tested for the same k-sensitivity: run the S(a)→w(z) pipeline at the corner threshold with
the cap stepped 38000 → 30000 → 20000 (and/or a fixed-k series) and confirm the interior peak
and 1.36σ survive. This is a robustness flag on the headline, not a refutation of it — the
corner's interior peak was jackknife-validated at cap=38000 — but the k-sensitivity exposed
here means the P4 fence is now load-bearing for the whole DE leg, not just retention_v2.

---

# CORNER CAP-STEP TEST (robustness audit of the standing headline)

**Pre-stated 2026-07-10 BEFORE computing**, per team-lead task. C1/C2 showed the retention
extremum is a k-budget artifact; large_volume's headline 1.36σ corner sits at the same cap
boundary, so its cap-dependence must be tested directly. **What is tested is ONLY
cap-dependence** — the octant jackknife at cap=38000 already validated within-cap stability.

## Configuration (matched to the headline, not to retention_v2)

- **Grid:** the large_volume **10-snapshot** grid (z = 3.008, 2.316, 1.744, 1.358, 1.036,
  0.791, 0.546, 0.329, 0.153, 0.0; snaps 25/30/36/42/49/56/65/76/87/99) — the grid the 1.36σ
  headline lives on, so this is a cap-only test with grid held fixed.
- **Threshold:** the frozen corner **7.4253e11 Msun/h (10^11.871)** held fixed at every cap
  (the corner value is frozen; only the cap's role as a subsampling ceiling is varied).
- **Analysis:** identical frozen chain (global-max z_peak; CPL project_distance → Mahalanobis
  to DESI DR2; real DR2 likelihood chi2), same machinery as C1/C2.
- **cap=38000 baseline (EXISTING, large_volume/results.json):** interior S-peak z=0.590
  (grid argmax z=0.546), **CPL maha = 1.363** (w0=−0.767, wa=−0.742), w_today=−0.833±0.057.
  I recompute the 38k corner point ONCE on this machinery as a **reproduction anchor** (to
  confirm my analyze() reproduces 1.36σ before trusting cap-step deltas) — this is not a
  wasteful recompute, it de-risks the comparison.
- **Runs:** cap ∈ {38000 (anchor), 30000, 20000}; subsample-without-replacement seed =
  SEED_BASE + 1000·cap_index + snap.
- **P4 fence (requested):** ceiling k=20000 at all snaps (use all where n<20000), **2 seeds**
  — record which snaps are subsampled. (Note: for the corner this ceiling equals cap=20000,
  so it functions as 2 extra seed-realizations of cap=20000 → a seed-scatter estimate.)
- **Stronger fence (BONUS, cheap, decisive):** **constant k=8000 at ALL snaps**, 2 seeds —
  the true intensive fence. Holds the sample SIZE fixed across a so S(a) reflects only
  correlation-structure growth, not the growing halo count. If the interior peak survives
  constant-k, it is a structure feature; if S(a) goes monotone, the peak was a count artifact.

## PASS/FAIL (pre-stated, per team-lead)

- **(i) SURVIVES:** interior S-peak stays z ≈ 0.5–0.7 AND DESI maha stays within ~0.5 of the
  38k baseline (i.e. **maha ≲ 1.86**) at BOTH cap=30000 and cap=20000.
- **(ii) DEGRADES-GRACEFULLY:** peak epoch stays interior but maha drifts by >0.5; report the
  drift per cap step — it becomes a **stated systematic** on the headline (e.g. "1.36σ at 38k,
  Xσ at 30k, Yσ at 20k").
- **(iii) KILLED:** z_peak leaves the interior (marches toward an endpoint) OR the fit flips to
  worse-than-ΛCDM (chi2−LCDM > 0 / w0→−1 monotone) at **cap ≤ 30000** — reproducing the C1
  pattern at the corner.
- **Fence criterion:** constant-k=8000 interior peak present → interior peak is (partly)
  structural; monotone/endpoint → the interior peak (hence the whole crossing signal) is a
  halo-count effect.

**Prediction on record (not a criterion):** because the corner is 0.02 dex from C1's 11.89 —
which went z_peak 0.546→2.002 and maha 1.156→4.531 at cap=20000 — I expect KILLED at
cap=20000 and likely (ii)/(iii) at cap=30000. Running it honestly regardless.

## OUTCOMES

**Machinery validated:** the recomputed cap=38000 corner point reproduces the existing
headline **exactly** — maha 1.363, w0=−0.767, wa=−0.742, z_peak=0.546 — so the analysis chain
matches large_volume and the cap-step deltas are trustworthy.

### Fixed-threshold cap-step (threshold frozen at corner(38k)=10^11.871) — KILLED (iii)

| cap | n_subsampled | z_peak | w0 | wa | maha | chi2−LCDM |
|-----|-------------|--------|-----|-----|------|-----------|
| 38000 | 0/10 | 0.546 | −0.767 | −0.742 | **1.363** | **−1.460** |
| 30000 | 7/10 | **1.358** | −0.988 | +0.092 | **3.574** | **+2.640** |
| 20000 | 8/10 | 1.744 | −1.021 | +0.251 | 4.374 | +1.109 |

Holding the threshold value fixed, a single mild cap step 38k→30k fires **both** pre-stated
KILL clauses: z_peak leaves the interior (0.546→1.358) AND the fit flips to worse-than-ΛCDM
(chi2−LCDM −1.46→+2.64); the thawing signal collapses (wa −0.742→+0.092, w0→−0.99≈ΛCDM). The
cause is visible in k(a): at cap=30000 the count is clipped into a **plateau**
[8606,16384,24803,30000,30000,…], erasing the interior count-peak that the whole S(a) signal
rides on. **The specific threshold value 7.425e11 is not special** — its good fit requires the
cap to sit exactly at its raw count peak (which the corner rule places there at cap=38000).

### Intensive fence — constant k=8000 at all snaps (2 seeds)

z_peak = **3.008 (high-z endpoint)** both seeds; S(a) monotone-declining with a
[1346→…→584]. **With sample size held fixed, there is NO interior peak.** The interior S-peak
is therefore an **extensive halo-COUNT feature, not a correlation-structure feature** — which
is what the theory intends (ρ_DE extensive ∝ S ∝ count), but it means the entire crossing
signal rests on the above-threshold count k(a) peaking interior.

### Corner-RULE re-selection cap-step (the fair test — rule re-picks threshold per cap) — DEGRADES-GRACEFULLY (ii)

The frozen object in the pipeline is the **corner RULE** (thr = max over snaps of the
(cap+1)-th largest mass), not the threshold value. Re-selecting the threshold at each cap so
the cap again sits at the raw count peak:

| cap | re-selected thr | z_peak | w0 | wa | maha (CPL) | chi2−LCDM |
|-----|----------------|--------|-----|-----|-----------|-----------|
| 38000 | 10^11.871 | 0.546 | −0.767 | −0.742 | **1.363** | −1.460 |
| 30000 | 10^11.975 | **0.546** | −0.719 | −0.934 | **2.162** | −0.989 |
| 20000 | 10^12.138 | **0.546** | −0.713 | −0.998 | **2.305** | −0.085 |

**The interior peak SURVIVES at z=0.546 at every cap; the thawing persists (wa stays ≈−0.7 to
−1.0); the fit stays closer to DESI than ΛCDM (maha 1.36/2.16/2.31 all < ΛCDM's 3.28).** What
changes is the MAGNITUDE: significance drifts 1.36σ→2.16σ→2.31σ and the DR2-likelihood edge
thins from chi2−LCDM −1.46 → −0.99 → −0.085 (at cap=20000 the likelihood advantage is
essentially gone, though the projected (w0,wa) still beats ΛCDM). This is criterion (ii),
degrades-gracefully — the drift is a **stated cap/resolution systematic**, not a kill.

### Reconciliation (this unifies the whole audit)

The re-selected thresholds — 10^11.87 (38k) → 11.98 (30k) → 12.14 (20k) — land **exactly where
C1's scan-extremum moved** (11.89 at 38k → 12.1–12.3 at 20k). It is one phenomenon: **the
best-fit threshold tracks the cap.** retention_v2's error was reading the cap=38000 operating
point (10^11.89) as a FIXED PHYSICAL SCALE (the SHM peak); it is instead the current-hardware
operating point of a resolution-adaptive rule. large_volume's corner rule treats it correctly
(re-selects with cap), so the headline's KIND of result is cap-robust; only its magnitude is
resolution-dependent.

## CORNER CAP-STEP VERDICT

- **KILLED (iii)** for the **fixed-threshold** reading: 7.425e11 is not a special mass; its
  1.36σ requires the cap at its count peak, and a 38k→30k step flips it to worse-than-ΛCDM.
- **DEGRADES-GRACEFULLY (ii)** for the **frozen-RULE** reading (what the pipeline actually
  does): interior peak + thawing + beats-ΛCDM survive at all caps; significance carries a
  **resolution systematic — quote "1.36σ at cap=38000, ~2.3σ at cap=20000."**
- **The headline is NOT killed**, but two things are now established and should be recorded on
  it: (1) the "1.36σ" is the best-resolved (cap=38000) value, resolution-dependent, not a
  fixed number; (2) the entire signal is the extensive count k(a) (constant-k fence: no
  structural interior peak), so the P4 intensive-fence / cap-systematic is load-bearing for
  the DE leg and should travel with the result. A bigger GPU (higher cap → lower re-selected
  threshold → more halos) is the way to test whether the significance recovers toward/below
  1.36σ; nothing here suggests the cap is inflating the result (lower cap only weakens it).

---

## INTERPRETATION AMENDMENT (aperture-law vs artifact)

**Honesty flag on timing:** this amendment arrived from the team lead **after** the
corner cap-step and rule-reselect runs had already completed and been read. The RUNS were
pre-registered under the original survive/degrade/kill matrix; this re-mapping onto the
amended matrix is therefore a **post-hoc re-interpretation of in-hand data**, not a
pre-registered test. I mark it as such and keep the residual discipline: a down-slope that is
"consistent with" a hypothesis is never support for it.

**The amendment.** Two hypotheses both predict fit degradation as the cap drops:
(a) **k-budget ARTIFACT** — the signal is a computational-aperture accident; (b) **APERTURE
LAW** — fit quality is monotone in completeness of the read, so a *real* complete-book signal
(ρ_DE sourced by S on the complete book, per the married gravity ontology) MUST degrade when
the aperture shrinks. My own **C2 overshoot** (subsampled-11.89 fits *worse* than 12.33 at
matched k → higher-mass units carry more signal per unit at fixed count) is genuine evidence
of **population structure** in the signal, i.e. against *pure* noise-artifact — it cuts toward
(b). So "pure k-artifact" is too strong; there is real population structure.

**Amended matrix and where my results land:**

- **(i) smooth monotone degradation as cap drops, z_peak drifting late/endpoint = consistent
  with BOTH artifact and aperture-law — NOT a kill; log the down-slope as a measured aperture
  systematic.** → **The FIXED-threshold cap-step is clause (i)**, not a kill. It degrades
  smoothly (maha 1.36→3.57→4.37) with z_peak drifting late (0.55→1.36→1.74), and the fit
  washes toward ΛCDM ((w0,wa)→(−0.99,+0.09) ≈ ΛCDM at 30k). This **supersedes the earlier
  "KILLED (iii)" reading** of the fixed-threshold run: under the amended matrix that down-slope
  is non-discriminating, logged as an aperture systematic. (One nuance to preserve: the
  fixed-threshold run loses the interior structure entirely as it washes to ΛCDM, whereas the
  rule keeps it — see below; the discriminating fact between them is that the aperture must be
  *centered* on the count peak to read the book.)
- **(ii) fit IMPROVES or is flat at lower cap = kills aperture-law, supports artifact.** →
  **Not observed.** Neither the fixed nor the rule run improves at lower cap; both degrade. So
  the aperture law is **not falsified downward** by these runs (but is not confirmed either —
  the down-slope is non-discriminating).
- **(iii) z_peak stays interior AND maha within ~0.5 of baseline at 20k = aperture-robust
  (strongest survival).** → **The RULE-reselect run half-meets (iii):** z_peak stays interior
  (0.546) at every cap ✓, but maha drifts 1.36→2.16→2.31, i.e. ~0.95 at 20k, just outside the
  ~0.5 band ✗. So: **interior-peak/thawing/beats-ΛCDM are aperture-robust; the magnitude drifts
  ~0.95σ across a ~2× aperture cut.** Strong (i) with the peak-robustness of near-(iii).
- **constant-k=8000 fence** (smallest aperture): no interior peak, S monotone → consistent
  with aperture-law (smallest aperture = most washed-out) AND with the extensive-count reading.
  Non-discriminating; both say "S scales with the number of units read." Under the aperture
  framing this is just: the aperture at k=8000 is too small to read the book.

**Adversarial hold on the amendment (my job).** The aperture law must not become
heads-I-win: if every downslope is "consistent," its ONLY real test is the single **upward**
run. The amendment stakes that sharply and I endorse the stake: **full-population tiled S,
pre-registered expectation complete-book fit ≥ 1.36σ; if the full read degrades below 1.36σ,
the artifact reading reasserts.** That is genuinely falsifiable and is now the outstanding
decider. Until it runs, the down-slope is logged as an aperture systematic and is **not**
counted as support (a residual is never support). I did **not** start the tiling run (a
design pass was requested first).

**Net under the amended matrix:** the corner headline is **clause (i)/near-(iii) — degrades
gracefully, aperture-consistent, not killed**; the "1.36σ" carries a resolution/aperture
systematic (~2.3σ at cap=20000 under the rule); the decisive adjudication is the upward
full-population read, pre-registered at ≥1.36σ. The retention_v2 SHM-anchor verdict is
**unchanged and still dead** (C1/C2): the aperture framing explains *why* the scan-extremum
tracks the cap but does not restore a fixed physical SHM mass scale.

---

## Orchestrator sideways pass (2026-07-10, after the C1–C5 verdicts): the kill stands for SHM; the remainder read positively opens the APERTURE LAW

The SHM-anchor kill is accepted (C1+C2 fired on pre-stated criteria; C5: SHM is a passenger).
But C1's criterion embedded an assumption — "extremum follows the cap ⇒ artifact" — that a second
hypothesis also satisfies: **the aperture law**: DESI-fit quality is monotone in the completeness
of the read, so a real complete-book signal MUST sit at the cap boundary (max completeness within
budget) and MUST degrade when the cap is lowered. The audit's own data contains two positive
monotonicities that favor structure over artifact:
1. **More units → better fit** (the k-trend across the scan).
2. **More massive units at fixed count → better fit** (the C2 overshoot: subsampled-11.89 fits
   *worse* than 12.33 at matched k — a population effect an artifact reading does not predict).

The framework's own married gravity ontology independently requires this: the S sourcing ρ_DE is
gravity's read of the **complete book** (Gate-0 completeness); every threshold+cap configuration
is an instrumental undersample. Under the aperture law the 1.36σ headline is a **lower bound**,
and the unit-scale question dissolves — there is no privileged mass scale, which is *why* every
scale-anchor attempt (shm v1, retention-v2) dies.

**Status: hypothesis, with a pre-registered two-sided test.** Downward (cap-step, in flight,
interpretation matrix amended before results read): smooth degradation is consistent with BOTH
readings — not a kill either way; flat-or-improving at lower cap KILLS the aperture law.
Upward (decisive): the full-population S(a) via the block-tiling estimator — aperture law
predicts complete-book fit ≥ 1.36σ; degradation on the full read reasserts the artifact and
puts the headline itself at risk. Design pass required before the tiling run.
