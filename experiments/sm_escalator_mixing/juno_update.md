# JUNO first result vs. the registered anarchic-book fork — status UNCHANGED, context sharpened

**Date 2026-07-11.** Fork-maintenance check against the first JUNO oscillation measurement,
which landed while the Rung-1 mixing claim (`REGISTRATION.md`, `SUMMARY.md`) sat open. Verdict
up front: **neither registered kill is touched, and θ₁₂ stays Haar-unremarkable — now pinned
~1.6× tighter.** JUNO measures the *solar* sector (θ₁₂, Δm²₂₁); our two live threats are θ₁₃
bulk-exit and a CP-conserving δ, both in the sector JUNO did not measure.

## 1. The measurement (verified, collaboration primary source)

JUNO Collaboration, **"First measurement of reactor neutrino oscillations at JUNO"**,
arXiv:2511.14593 (59.1 days of data since detector completion, August 2025; normal ordering):

| parameter | JUNO first result | prior (NuFit-6.0, our registration) |
|---|---|---|
| sin²θ₁₂ | **0.3092 ± 0.0087** | 0.308 (± ~0.012) |
| Δm²₂₁ | (7.50 ± 0.12) × 10⁻⁵ eV² | — (not a mixing-matrix functional) |

A factor ~1.6 improvement in θ₁₂ precision over the prior global combination. JUNO reports
**no** θ₁₃ and **no** δ_CP in this first result — both remain Daya Bay/RENO- and
long-baseline-driven. Δm²₂₁ does not enter any of our PMNS functionals (we read the mixing
matrix's angles+phase, not the mass splittings), so it is irrelevant to the fork.

## 2. Haar-percentile shift for θ₁₂ — negligible, toward typicality

Using the stored Haar marginal of sin²θ₁₂ (`results.json`, n=200k; the marginal is
near-uniform on [0,1], quantiles q25=0.2497, q50=0.4999), interpolation reproduces the
registered NuFit percentile (30.82 vs. stored 30.83 — method validated against the frozen
ensemble):

| value | Haar percentile of sin²θ₁₂ |
|---|---|
| NuFit-6.0, 0.308 (registered) | 30.83 |
| **JUNO, 0.3092** | **30.94** (1σ band [30.07, 31.81] from ±0.0087) |

**Shift: +0.11 percentile toward the Haar median (0.50).** Utterly negligible in value; the
substance is that the *band* tightened (±0.0087 vs. the earlier ±0.012), so θ₁₂ is now
**more sharply pinned** at ~31st percentile — squarely in the anarchic bulk, exactly what a
structureless coupling predicts. This is the opposite of a kill: the coordinate the fork
leans on got measured better and did not move out of the bulk.

## 3. Symmetry-exclusion score — structured tails being pruned; observed value stays generic

Verified: **S. T. Petcov & A. V. Titov, "Viability of A₄, S₄ and A₅ Flavour Symmetries in
Light of the First JUNO Result"**, Phys. Lett. B **874**, 140295 (2026); arXiv:2511.19408.
They adopt the same sin²θ₁₂ = 0.3092 ± 0.0087. Predictions vs. JUNO (their Table 2):

| discrete-symmetry case | predicted sin²θ₁₂ | JUNO verdict |
|---|---|---|
| C5 (S₄/A₅) | 0.256 | **excluded 6.1σ** (4.9σ already by NuFIT) |
| B1 | 0.341 | disfavored 3.8σ |
| B1(A₅) | 0.283 | disfavored 3.3σ |
| B2(S₄) — TM1 | 0.318 | favored, survives |
| B2(A₅) | 0.331 | survives (NO), disfavored 3.5σ (IO) |
| C9(A₅) | 0.331 | survives |

Score: JUNO's tightened θ₁₂ **excludes/corners the discrete-symmetry patterns whose
predictions live in the tails** (0.256, 0.283, 0.341) while the *observed* value sits at the
31st Haar percentile — generic under anarchy. Normal-ordering survivors drop from ~5 to 3;
inverted from ~4 to 2.

**Resisting the over-claim (many-models fallacy).** This is indirect, not confirmation:
1. Excluding specific symmetry models is **not** evidence for anarchy. Anarchy is a
   distribution; θ₁₂ at the 31st percentile is merely *unremarkable* under it, never a
   positive prediction hit.
2. The survivors (B2S₄ 0.318, B2A₅/C9A₅ 0.331) themselves predict **near-Haar-typical**
   values (~32nd–33rd percentile). θ₁₂ alone therefore does **not** discriminate anarchy from
   the viable structured patterns — it only kills the ones that bet on the tails.
3. So the ledger reading is unchanged and slightly firmer *in context*, but earns **no new
   support**. Support requires a confirmed novel positive prediction (discipline rule 2); this
   is a maintained-consistency result, not one.

## 4. Fork bookkeeping — both registered kills untouched

The two staked kills (`SUMMARY.md` §"Kills going forward"):

- **θ₁₃ bulk-exit** (currently 4.4th Haar percentile — the single atypical coordinate):
  **untouched.** JUNO's first result carries no θ₁₃ measurement.
- **CP-conserving δ** (|J| → percentile ~0): **untouched.** No δ_CP in the first result;
  DUNE/Hyper-K remain the discriminators, as registered in `SUMMARY.md` §3.

**Fork status: UNCHANGED.** No functional's percentile moved out of the central 99%; the
asymmetry claim (CKM 99.98 vs. PMNS ~37 MI-percentile) is unaffected. The one live threat that
JUNO *could* have touched — a shift in θ₁₂ — went the harmless direction (+0.11 percentile,
tighter band, still bulk). The next real tests of this fork are still θ₁₃ (better reactor
data) and δ_CP (DUNE/Hyper-K), not JUNO.

## Sources (verified)

- JUNO Collaboration, arXiv:2511.14593 — first measurement, sin²θ₁₂ = 0.3092 ± 0.0087,
  Δm²₂₁ = (7.50 ± 0.12)×10⁻⁵ eV².
- S. T. Petcov, A. V. Titov, Phys. Lett. B 874 (2026) 140295, arXiv:2511.19408 — A₄/S₄/A₅
  viability; C5 excluded 6.1σ, TM1-type survivors.
