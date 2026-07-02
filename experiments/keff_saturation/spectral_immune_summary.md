# Adaptive-immune repertoire — does it SATURATE or read CRITICAL?

Adversarial breadth test on the criticality camp's flagship **biological** system:
the antibody (BCR/IgH) repertoire. Mora, Walczak, Bialek & Callan and collaborators
argue immune-repertoire statistics are **critical** — the clone-size distribution
is Zipf/power-law and max-entropy models sit near a critical point. Here the
criticality reading is the *published prior*, so a clean saturation would be
strong and a power-law is an honest bound.

We report **both** observables, because they are not the same measurement.

## Dataset

**Observed Antibody Space (OAS)**, Briney et al. 2019, *"Commonality despite
exceptional diversity in the baseline human antibody repertoire"* (Nature) — the
canonical baseline-repertoire study: 9 healthy human donors, heavy-chain (IgH)
bulk repertoires, biological + technical replicates. Streamed directly (no login)
from `https://opig.stats.ox.ac.uk/webapps/ngsdb/unpaired/Briney_2019/csv/`.
170 of the 296 `Heavy_Bulk` data units → **161 usable samples across 10 subject
labels** (9 donors + 1 extra label). AIRR columns: `v_call`, `j_call`, `cdr3_aa`,
`Redundancy` (duplicate-read count = abundance proxy). Real data only; synthetics
calibrate the discriminator only.

## Two constructions

- **(a) Clone-size / abundance (the criticality camp's observable).** Per
  repertoire, clonotype = (V-gene, J-gene, CDR3-aa); clone size = summed
  `Redundancy`. Fit discrete power-law (Clauset–Shalizi–Newman MLE + KS-chosen
  `xmin`); Vuong likelihood-ratio test power-law vs lognormal.
- **(b) Covariance-spectrum saturation (our observable).** Feature = V-J
  germline-gene-usage fraction; observation = sample. Matrix **N = 202 V-J
  features × T = 161 samples** (features present in ≥60% of samples). Correlate
  features across the population; PR/k_eff, MP + permutation eff-rank, subsampling
  β, spectrum power-law α.

Discriminator calibration (synthetic, N=200,T=800): low-rank r=3 → β=0.03, 3
modes; power-law α=1.0 → β=0.24; power-law α=0.6 → β=0.63; pure noise → β=0.89.

## Observable (a) — CLONE-SIZE: POWER-LAW (criticality reproduced)

| quantity | value |
|---|---|
| per-repertoire power-law exponent α (P(size) ∝ size^−α) | **median 2.34**, IQR [2.29, 2.37] |
| repertoires favoring power-law over lognormal (Vuong z>0) | **96%** |
| significantly power-law (z>0, p<0.1) | **91%** |
| significantly lognormal (z<0, p<0.1) | 2% |

The clone-size distribution is **heavy-tailed and power-law-consistent** in
essentially every repertoire — lognormal is rejected in its favor 91% of the time.
α ≈ 2.3 (rank/Zipf slope ≈ 0.75) is squarely the published immune clone-size
exponent. **The criticality camp's own observable reproduces: this system is
power-law by clone-size.**

## Observable (b) — COVARIANCE: INTERMEDIATE / soft power-law (NOT clean saturation)

| readout | value | reading |
|---|---|---|
| PR / k_eff | **25.5** (ceiling N=202) | bounded well below N |
| top eigenvalues | 23.3, 15.3, 14.9, 11.4, 11.1, 7.7, 6.5, 6.1 … | **graded cascade**, not one spike + flat bulk |
| eff_rank (MP edge 4.49) | **9** | 9 modes over noise |
| eff_rank (permutation null, 99th pct = 4.77) | **9** | confirmed by the proper cross-sectional null |
| eff_rank (time-surrogate) | 1 | *discarded* — phase-randomization assumes an ordered time axis; samples are unordered individuals |
| subsample β (N′∈[20,202]) | **0.189** | between low-rank (0.03) and mild power-law (0.24) |
| spectrum power-law α (λ_k ∝ k^−α) | **0.91** | soft power-law decay |
| subsampling curve | 7.9 (N′=10) → 25.5 (N′=202), still rising | **no clean plateau** |

Unlike the framework's other biological substrates (C. elegans: β≈0, 2–4 sharp
spikes over a flat bulk, PR plateaus), the immune gene-usage covariance shows a
**graded 9-mode cascade**, a **soft-power-law spectrum (α≈0.9)**, and a
**subsampling curve still climbing at N=202** (β=0.19, nearest the mild-power-law
calibrator, far from the low-rank β≈0). k_eff is bounded (25.5 ≪ 202), so it is
*not* extensive/noise — but this is **intermediate, leaning mildly critical, not
the sharp low-rank saturation** the discriminator found elsewhere.

## Do the two observables agree? YES — both read heavy-tailed here

This is the load-bearing result. In the framework's other substrates the two can
split ("power-law by clone-size, bounded by covariance"). **Here they agree in the
power-law direction:** clone-size is clearly Zipf, and the covariance is a soft
power-law rather than a clean plateau. The immune repertoire is the substrate
where our discriminator does **not** overturn the criticality reading — it softly
corroborates it.

## Honest bottom line

**The adaptive-immune repertoire reads mildly CRITICAL, not saturating, on this
construction — an honest bound on the universality claim.** Clone-size is
power-law (as published, 91% of repertoires), and the V-J gene-usage covariance is
a soft power-law (β=0.19, 9 graded modes, α_spec≈0.9, curve still rising), not the
sharp low-rank saturation seen in the worm/fly/galaxy substrates. This is the
first substrate in the sweep where the criticality prior is corroborated rather
than ruled out.

**Is it even the right kind of unit? Probably not — and this is the deeper
caveat.** Three reasons the verdict should not be over-read as "the framework
fails on immunity":

1. **Coordination is indirect.** One person's repertoire is a *population of
   clones under shared antigenic + thymic/germline selection*. The shared driver
   is real, but clones do not signal or actively co-manage each other — there is
   no `γ·M(t)` maintenance loop between clones. So neither a saturation nor a
   criticality verdict here is diagnostic of a *coordinating* unit in the
   framework's sense; a power-law clone-size is expected from neutral
   birth–death/Yule and antigen-driven clonal expansion **without** any corridor
   mechanism.
2. **Observable (b) is population-level, not one repertoire's own dynamics.** It
   measures how V-J usage co-varies *across 161 samples from ~9 donors*, i.e. the
   collective modes of composition across a healthy population — a real object,
   but not "does one repertoire coordinate." The faithful single-unit test is
   **longitudinal clone tracking** (clone × timepoint covariance), which Briney's
   cross-sectional replicates do not provide and which is intrinsically low-T.
3. **The subsampling has a hard germline ceiling.** Features are germline V-J
   categories (~50 V × 6 J), so there is no true N→∞ limit; β over N′∈[20,202] is
   informative but the asymptotic-saturation question is partly moot — the "more
   constituents" axis is bounded by the genome, not the data.

So the fair statement: **by both observables the immune repertoire leans
power-law, not saturating** — but it is a *population under a shared driver*, not
a coordinating unit with active coherence-management, so it is arguably outside
the framework's intended domain rather than a counterexample inside it. The clean
single-unit test (longitudinal clonal covariance) remains the honest next step.

Artifacts: `spectral_immune.py`, `spectral_results_immune.json`,
`spectral_immune_run.log`. No commit; no `.lean` edits.
