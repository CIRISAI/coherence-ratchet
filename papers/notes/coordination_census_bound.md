# The coordination census bound — how much engineered large-scale coordination the books exclude

**Date 2026-07-12.** A quantitative, order-of-magnitude BOUND, computed on our own
`results.json` values. **This note makes NO existence claim in either direction.** It asks one
question: *given that the measured coordination books `S(a)` agree with the gravity-only
structure-formation prediction to the precision we have measured, how much artificially-engineered
large-scale coordination could be hiding in them?* The null result IS the content (rule 2:
agreement is never evidence FOR anything; it is only a ceiling on prevalence). Every number below
carries its assumptions inline; the bound is grain-relative throughout (Gate-0 applies —
`the_grain_problem.md`).

Companion inputs: `full_population/results.json`, `abacus_cross/results.json`,
`gravity_ledger_instrument.md` (bias-only null), `gaia_phasespace_test.md` (the validated
phase-space instrument), `gravity_implications_maximal_stance.md` §5 (the null-space stealth
loophole), `thermo_prior_art.md` (the rent = Hatano–Sasa housekeeping heat).

External prior art, citations verified:
- **Kardashev, N. S. 1964**, "Transmission of Information by Extraterrestrial Civilizations,"
  *Soviet Astronomy* **8**, 217 — the Type I / II / III energy-scale ladder used below as the
  benchmark cases.
- **Dyson, F. J. 1960**, "Search for Artificial Stellar Sources of Infrared Radiation,"
  *Science* **131**, 3414, 1667 (DOI 10.1126/science.131.3414.1667) — the waste-heat / infrared
  technosignature; prior art for the rent-cannot-be-hidden corollary (§5).

---

## 1. Calibration — S per unit, from our own runs

`S = −ln det C` is (near-)extensive in the number of resolved units at fixed grain; the
per-unit value is grain-set. Extracting `S_total / n` at the best-gate tile (T=2 for TNG, the
tile that reproduces the exact S to maha 0.09; T=8 for the Abacus complete book) across our
configs, at z≈0 and at the S-peak epoch:

| Config (box) | grain (threshold) | z≈0: S_total / n | at S-peak: S_total / n |
|---|---|---|---|
| TNG300-1 gate/corner (205 Mpc/h) | ≈7×10¹¹ M⊙/h (galaxy-host) | 8651 / 35818 = **0.242** | 9687 / 38001 = 0.255 |
| TNG300-1 full_2e11 | ≥2×10¹¹ | 64083 / 118105 = **0.543** | 73509 / 127434 = 0.577 |
| TNG300-1 full_1e11 (complete book) | ≥1×10¹¹ | 166503 / 212749 = **0.783** | 192220 / 233388 = 0.824 |
| Abacus corner (500 Mpc/h) | 7.425×10¹¹ | (0.11 late — S declines) | 102294 / 271727 = 0.377 (early) |
| Abacus full_2.109e11 (complete) | ≥2.109×10¹¹ | — | 2089888 / 2326098 = **0.898** |

**Result:** S per resolved halo ≈ **0.1–0.9 nats**, systematically grain-dependent — it RISES
as the threshold drops (finer grain = more units = more within-tile correlation pairs captured).
Central values: **~0.2 nats/unit at the galaxy-host grain (~7×10¹¹)**, **~0.8 nats/unit at the
complete-halo grain (~1×10¹¹)**. The factor ~4 spread across grains is the grain-dependence, and
it is exactly the load-bearing ambiguity of `the_grain_problem.md` — carried forward as a
caveat, not hidden.

### Cosmic books — nats per Hubble volume

Volume conventions stated explicitly: **comoving, z=0, in (Mpc/h)³, halo grain from TNG300-1.**
Hubble radius `R_H = c/H₀ = 2998 Mpc/h` (h-independent in these units);
`V_H = (4/3)π R_H³ = 1.13×10¹¹ (Mpc/h)³`. TNG300-1 box = (205 Mpc/h)³ = 8.62×10⁶ (Mpc/h)³.

- **Complete-halo grain (≥10¹¹):** S-density = 166503 / 8.62×10⁶ = 0.0193 nats/(Mpc/h)³;
  unit-density = 0.0247 (Mpc/h)⁻³ → **N ≈ 2.8×10⁹ units** and **S_cosmic ≈ 2×10⁹ nats per
  Hubble volume.**
- **Galaxy-host grain (~7×10¹¹):** S-density = 8651 / 8.62×10⁶ = 1.0×10⁻³ nats/(Mpc/h)³ →
  **S_cosmic ≈ 1×10⁸ nats per Hubble volume** (N ≈ 4.7×10⁸ units).

Headline: the cosmic coordination budget is **order 10⁸–10⁹ nats per Hubble volume** at the
halo grain, ~10⁹ at the complete book. This is the denominator the census is measured against.

---

## 2. The posting formula

An engineered coordination of `m` units imposed at artificial correlation `ρ_a` (equicorrelation
block) posts, exactly:

> **ΔS = −(m−1)·ln(1−ρ_a) − ln(1+(m−1)ρ_a)**

(eigenvalues of the equicorrelation matrix: `1−ρ_a` with multiplicity `m−1`, and `1+(m−1)ρ_a`
once). Its small-ρ_a limit is the validated CIRISArray quadratic form:

> **ΔS ≈ ½·m(m−1)·ρ_a²**   (Taylor to O(ρ_a²); the two exact log terms' linear parts cancel).

Use the **exact** form for the exclusion curve; the quadratic overstates ΔS at moderate ρ_a
(e.g. m=10: quadratic says ρ_a=0.15 posts 1 nat; exact needs ρ_a=0.20). The formula reads only
the **off-diagonal** structure — the correlation among units. This is the fence that governs the
benchmark cases.

### Benchmark cases (Kardashev ladder)

- **K-II (one stellar system engineered — a Dyson sphere):** at the survey/galaxy grain the
  coordinated components are sub-stellar-to-stellar parts INSIDE one halo — **below the grain
  entirely.** They contribute `m = 0` units to the inter-unit matrix. ΔS at galaxy grain = **0,
  negligible, exactly** (grain-blindness). K-II is invisible to the cosmic books by construction.

- **K-III (one galaxy internally engineered):** the galaxy is **one unit** at the survey grain.
  `S` is amplitude-blind (a copula functional, clause 3) and grain-blind to intra-unit structure,
  so internal reorganization touches only a diagonal block's interior and posts **~nothing at
  survey grain.** **Precise fence:** K-III registers *only if* the engineering changes the unit's
  correlation with OTHER units — its off-diagonal entries `ρ` to neighbors. A galaxy that
  rearranges its stars while keeping the same gravitational/positional relation to its neighbors
  posts ΔS = 0. This is `pattern-does-not-gravitate` in ledger form: only carrier-level
  organization that alters inter-unit coupling posts.

- **K-III+ clusters (m externally-coordinated galaxies at ρ_a):** the **detectable class** — the
  only one that writes to the off-diagonal `S` reads. ΔS = the exact `−ln det` above. Everything
  in §3–§4 is a bound on this class.

---

## 3. The global bound — two channels, one grain-robust

Current agreement of measured vs gravity-only books (the honest floor): the **selection-free
complete book fits DESI at 2.2σ** (TNG full_1e11: maha 2.21, Δχ² = −1.1 vs ΛCDM's 3.28σ;
Abacus full-pop 1.62σ), and the **corner grain at 1.36σ** carries a documented grain systematic.
The tiled estimator reproduces the exact `S` to **~1.3%** (gate v2 fidelity). The census reads
this agreement two ways:

**Channel A — amplitude (grain-degenerate → WEAK).** A smooth engineered excess `ΔS_eng(a)`
distorts `w(z)` via the sign law `1+w = −⅓·dlnS/dlna`. The fit tolerates fractional distortion
of `dlnS/dlna` at roughly the **few-percent to ~10% level** (w₀ error ≈ 0.057 on w ≈ −0.8 → ~7%;
plus the 2.2σ-vs-3.28σ headroom). So `f_A ≈ 0.01–0.1`. **But this channel is degenerate with the
grain problem:** an engineered S-excess is indistinguishable from a different grain choice (the
grain sets the amplitude — `the_grain_problem.md` §6–§7). Because the grain is underived, Channel
A cannot cleanly separate "anomalous" from "natural" S. **The amplitude bound is therefore weak
and model-dependent — this is the sharpest fence on the census itself.**

**Channel B — scale (grain-ROBUST → the real bound).** The inter-tile term `S_inter` is measured
negligible at every scale, and it is defined independently of the unit threshold:

| tile T | tile size | S_inter | S_total | S_inter / S_total |
|---|---|---|---|---|
| 2 | 102.5 Mpc/h | ~9.4×10⁻⁹ | ~10⁴–10⁵ | **~10⁻¹⁰–10⁻¹¹** |
| 8 | 25.6 Mpc/h | ~0.04 | ~10⁴–10⁵ | **~5×10⁻⁶–10⁻⁷** |

Coordination ACROSS ≳25–100 Mpc scales is **≤ ~10⁻⁶** (conservative, T=8) of the books — the
extensive companion of the bias-only null (dark ≈ light to r = 0.986–0.999; the copula turns
Gaussian at large scale). This channel does **not** depend on grain (it is the inter-tile block).
**Any engineered coordination that spans the survey grain — correlating galaxies across
>100 Mpc — is excluded to ≤10⁻⁶ of the cosmic budget.**

### The exclusion curve (m vs ρ_a)

Report the bound as a curve, not one number. The ΔS = 1 nat contour (one unit-equivalent of
posted coordination; the large-scale detectability floor is actually lower, ~0.05 nat set by the
T=8 S_inter), exact `−ln det`:

| m (units) | ρ_a to post ΔS = 1 nat |
|---|---|
| 2 | 0.79 |
| 3 | 0.59 |
| 10 | 0.20 |
| 100 | 0.021 |
| 1000 | 0.0022 |

Asymptotically `ρ_a ≈ 2/m` for large m. **Reading:** a coherent structure of m units at fixed
`ρ_a ≫ 2/m` posts > 1 nat and, if it spans >100 Mpc, is excluded against the grain-robust
Channel B budget. For reference the natural (gravitational) corridor is ρ ∈ (0.1, 0.43); an
engineered structure is only distinguishable where it drives `ρ_a` above the corridor at a scale
where gravity produces none — i.e., large-scale, which is exactly where Channel B bites.

### Headline number

Take the grain-robust Channel B. Large-scale budget = 10⁻⁶ × S_cosmic ≈ 10⁻⁶ × 2×10⁹ = **~2×10³
nats per Hubble volume** available to hide >100 Mpc-spanning engineered coordination. A galaxy
coupled anomalously to cosmological-scale neighbors posts ~O(1) nat of off-diagonal excess, so
**N_anomalous ≲ 2×10³ units per Hubble volume**, against N ≈ 2.8×10⁹ →

> **Prevalence of cosmological-scale (>100 Mpc) engineered coordination is bounded below
> ~1 in 10⁶ galaxy-grain units at current books precision.** Order of magnitude: **1 in 10⁶.**

The cluster-scale (<25 Mpc, within-tile) analogue falls in Channel A and is bounded only at the
**~percent level (~1 in 10²), and is degenerate with the unresolved grain** — nearly
uninformative. The census's teeth are entirely in the large-scale, grain-robust channel.

### What DR3 buys

DESI DR3 tightens the distance likelihood — it improves **Channel A (the w(z) amplitude)** by
roughly the added-constraint factor, ~**2×** (DR2→DR3 on w₀/wₐ errors), taking the weak cluster
bound from ~percent to ~half-percent. **DR3 does not directly improve Channel B:** the >100 Mpc
coordination ceiling is set by the clustering data and the estimator (S_inter floor), not by the
distance-ladder w(z); it tightens with survey VOLUME and a bispectrum-level read, not with DR3's
w(z) alone. Honest split: **DR3 ≈ 2× on the weak channel; the sharp 1-in-10⁶ channel improves
with volume, not with DR3.**

---

## 4. The local bound (sketch — order of magnitude, flagged)

At cluster/supercluster grain, a lensing- or kinematics-level read is far more sensitive
*per system* than the global census, but reaches only nearby resolved objects. Tie to the
**validated phase-space instrument** (`gaia_phasespace_test.md`): `S = −ln det C` on the
`(position, velocity)` copula cleanly resolved the **Orphan stream at S = 0.351 vs field 0.020**
on real S5 radial-velocity data — a factor ~17 phase-space-coherence contrast, non-circular
(the RV dimension was not used to select the sample). So the instrument's demonstrated floor is
an S-excess of **order ~0.1–0.3 nats** in the `(x,v)` copula of a resolved system.

**Sketch bound:** an engineered cluster holding artificial phase-space coherence — member
galaxies on coordinated orbits — at `ρ_a` giving ΔS ≳ 0.1–0.3 nats would be **locally
detectable** by this instrument fed cluster kinematics (spectroscopic velocities) or a
lensing-derived velocity field. From §2, ΔS = 0.2 for m = 100 needs ρ_a ≈ 0.009; for m = 10,
ρ_a ≈ 0.09 — i.e., the local kinematic read reaches **an order of magnitude deeper in ρ_a** than
the global census, on individual nearby clusters. This is a sketch: it is not run, the selection
function and the natural-cluster ρ background (the corridor) would have to be controlled first,
and it inherits the Part-A selection-confound warning of the Gaia note. Flagged as sketch, not a
result.

---

## 5. Fences (verbatim-carried)

1. **Pattern-does-not-gravitate.** Only **carrier-level** organization — stress-energy that
   alters inter-unit coupling — posts to gravity's books. An abstract pattern at fixed
   stress-energy distribution posts nothing. This is why K-III internal reorganization at fixed
   mass distribution is invisible (§2).

2. **The bias-only ceiling (existing empirical result).** On the gravity ledger the dark field
   carries **no new coordination the light field misses**: dark ≈ light to **r = 0.986–0.999**,
   ~99% the same book at large scales (`gravity_ledger_instrument.md`). This is already an
   empirical ceiling on any NEW large-scale coordination — the cosmic books are, to sub-percent,
   just the gravitational clustering field, with no room for a distinct large-scale coordination
   component. Channel B is this ceiling made extensive.

3. **The null-space stealth exception + the rent-cannot-be-hidden corollary.** Coordination held
   in the proved **null space** (conjugate-basis, GHZ-type multipartite) is **off the κS
   gravitational books** — selective invisibility, not signaling (common cause cannot signal;
   `gravity_implications_maximal_stance.md` §5). So a sufficiently exotic engineer could, in
   principle, hold coordination the gravitational census cannot read. **But the rent cannot be
   hidden:** maintaining any non-equilibrium coordinated state costs continuous work that
   dissipates as **housekeeping heat** (the rent = Hatano–Sasa steady-state housekeeping heat
   exactly, `thermo_prior_art.md`), which posts in the **thermal (EM) channel regardless of
   gravitational stealth.** **Dyson (1960)** is the verified prior art for the tell: large-scale
   energy use appears as a waste-heat / infrared excess. Stealth on the gravity ledger buys no
   stealth on the thermodynamic ledger — the two ledgers close the loophole jointly.

4. **The grain problem — bounds are grain-relative (Gate-0).** Every number here is stated at a
   named grain; the per-unit S and S_cosmic move by a factor ~4 across the grains we ran
   (§1). Channel A is degenerate with the grain and therefore weak; **only Channel B (the
   inter-tile, scale-resolved bound) is grain-robust**, which is why the headline rests on it and
   not on the amplitude.

---

## 6. Discipline note

No NHI-existence claim is made or implied in either direction. This is a bound; the null result
is the entire content. The agreement of measured vs gravity-only books is **never** counted as
support for absence of engineered coordination (rule 2) — it is only a ceiling on prevalence.
Every step is order-of-magnitude with assumptions stated inline; CPU-only arithmetic on our own
`results.json`. External claims carry verified citations (Kardashev 1964; Dyson 1960).

---

## Orchestrator caveat (2026-07-12, before the headline travels): the sharp channel is sim-calibrated

Channel B's ceiling (S_inter/S_total ≤ ~10⁻⁶) was measured on SIMULATED catalogs (TNG300,
AbacusSummit) during estimator validation. As stated, the headline is therefore: *IF the real
universe's inter-tile coordination resembles the gravity-only simulations' — which is exactly
what a census must not assume — THEN >100 Mpc engineered coordination is bounded at ~1 in
10⁶.* Promoting this to a real-sky exclusion requires running the tiled-S estimator on an
actual redshift-survey catalog (SDSS/BOSS/DESI public data — the estimator is gate-validated
and the run is cheap; registered as the census's next step). Until then the honest status:
the INSTRUMENT and the exclusion CURVE are real; the real-universe number is pending one run
on public data. The thermodynamic stealth-closure fence (rent posts thermally regardless of
gravitational-ledger hiding) is unaffected — it is theorem-side, not calibration-side.
