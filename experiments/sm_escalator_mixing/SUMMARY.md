# Rung-1 mixing test — REGISTERED CLAIM HIT: the ledger reads the flavor sector as two books, one comonotone (quarks), one anarchic (leptons)

**Date 2026-07-10.** The one registered claim (`REGISTRATION.md`, staked in
`sm_escalator_map.md` §4 before this experiment existed) vs 200,000 Haar-random U(3)
matrices; everything else discovery-mode. Data: `results.json`, script `run_mixing.py`.
Parameters: CKM PDG 2024; PMNS NuFit-6.0 NO (both octants + a δ=π control),
arXiv:2410.05380.

## The registered claim: HIT, both halves

| | MI percentile in Haar | verdict |
|---|---|---|
| PMNS (lower octant) | **36.7** | Haar-typical (central 90%) ✓ |
| PMNS (upper octant) | **37.8** | Haar-typical ✓ |
| CKM | **99.98** | beyond 99.9 ✓ |

The asymmetry is real and parameter-free: **lepton mixing is statistically indistinguishable
from a Haar-random (anarchic) generation coupling; quark mixing is a >3.5σ-equivalent
outlier toward the aligned pole.** Rung 1 stands: the PMNS matrix is readable by the ledger,
and the CKM matrix is conceded to the marginal (mass-hierarchy/GST) sector, exactly as
staked.

## Discovery panel (exhaustive, all functionals)

**PMNS is Haar-typical in EVERY functional computed** — not just the primary one: MI 37,
one-hot S 35, singular-value participation 33, distance-to-anarchy 34, distance-to-nearest-
permutation 74, |Jarlskog| **58**. Six independent reads, all in the bulk. The typicality of
|J| is its own result: the leptonic CP-violation invariant sits at the Haar median — the
observed δ ≈ −1.98 is exactly what a structureless coupling predicts.

**CKM is extreme in every functional, in the *consistent* direction**: MI 99.98, one-hot S
100.00, participation 99.9, d_anarchy 99.97, d_perm 0.06 (within 0.10 of an exact
permutation), |J| **0.09**. The quark coupling is simultaneously maximally aligned AND
maximally CP-conserving relative to Haar — one coherent statement: it is close to a real
(phase-free) near-identity matrix.

**The magnitudes** (the ledger's actual read): CKM MI = 0.956 nats = **87% of the ln3
ceiling** — the up-type and down-type generation labels are nearly one book. PMNS MI = 0.19
nats = 17% of ceiling — the charged-lepton and neutrino books are nearly independent.

**The one wrinkle (flagged, not scored):** PMNS sin²θ₁₃ = 0.022 sits at the **4.4th** Haar
percentile — the single marginally-atypical coordinate (the known mild anarchy tension). It
is the same 1–3 corner where CKM is most extreme (percentile 0.00). If better data pushed it
lower, θ₁₃ is where Haar-typicality would crack first.

## Sideways pass (the discovery, not the scoreboard)

1. **What the asymmetry says physically, in ledger language:** coordination between two mass
   bases is evidence they were written by one mechanism. The quark books are ~87%
   comonotone — up and down Yukawas are one coordinated book (consistent with one Higgs
   mechanism + GST-correlated hierarchies). The lepton books are ~17% — consistent with the
   neutrino mass ledger being **a different book entirely** (seesaw/Majorana), uncoordinated
   with the charged-lepton one. The ledger cannot say *what* the second mechanism is
   (provenance line), but "two books vs one book" is its native verdict, and it lands on the
   side modern neutrino physics already suspects.
2. **Naming correction to sm_escalator_map.md §2:** the map called PMNS "high coordination
   (near-Haar)". On the functional the poles invert: **Haar/anarchy = independence = LOW
   coordination; alignment = comonotone = HIGH.** The quark sector is the coordinated one.
   The map's substantive claim (PMNS near-Haar, CKM near-pole) was correct; its label was
   backwards.
3. **A discriminating observable against the adjacent literature.** Thaler &
   Trifinopoulos (arXiv:2410.23343, verified) propose entanglement *minimization* in 2→2
   scattering as a selection principle, predicting *suppressed* leptonic CP violation. Our
   anarchy read says |J| is Haar-typical and should STAY large (δ far from CP-conserving).
   The δ=π control shows what failure looks like: |J| percentile crashes to 0.00 while MI
   stays typical. **DUNE/Hyper-K's δ measurement discriminates**: δ → CP-conserving kills
   the Haar-typicality of J (and favors minimization-type structure); δ staying near-maximal
   keeps anarchy. This is a genuine forward-looking fork, registered here before the data.
4. **Selection is still not claimed.** The result is a *reading*: the ledger characterizes
   the two measured couplings against the structureless ensemble. WHY the quark book is
   comonotone and the lepton book anarchic is upstream provenance — Thaler-type dynamical
   principles live there; the ledger does not (and cannot) adjudicate them.

## Kills going forward (dated debts)

- **PMNS Haar-typicality dies** if any functional's percentile leaves the central 99% with
  improved data — θ₁₃ (currently 4.4) and a CP-conserving δ (|J| → percentile ~0) are the
  two live threats. Either fires → lepton mixing is structured → Rung 1 collapses into the
  marginal no-go and the "two books" read loses its anarchic half.
- **The asymmetry claim dies** trivially if CKM re-measurement moves it into the Haar bulk
  (no realistic path; recorded for completeness).

## Rigor pass

**Date 2026-07-11.** Referee-proofing statistics around the already-scored claim (confirmation
mode — the claim's status changes only per its pre-registered kills). Same seeded 200k Haar
ensemble as `run_mixing.py`, **regenerated bit-exactly** (max Haar-mean abs diff vs
`results.json` = 0.0). Code + data: `rigor/{rigor.py, rigor_results.json}`; statistics
pre-stated in the `rigor.py` header before running. Parameters re-verified against NuFit-6.0
(arXiv:2410.05380 Table 1) and PDG-2024.

**1. Joint typicality (the 6 correlated functionals, not just their marginals).** Individually-
typical can be jointly atypical; it is not, for PMNS. Three depths, each percentiled against
the empirical Haar null (outlyingness percentile: ~50 typical, >95 outlier, >99.9 pole):

| | Mahalanobis (raw) | normal-scores rank Mahalanobis | spatial (L1) depth |
|---|---|---|---|
| PMNS lower octant | 1.3 | 5.2 | 15.9 |
| PMNS upper octant | 2.3 | 7.4 | 15.9 |
| CKM | **99.995** | **99.60** | **99.98** |

All three agree unanimously: **PMNS is jointly typical — in fact more central than a typical
Haar draw (D²≈0.8 vs cloud); the six functionals do not conspire into a tail. CKM is jointly
extreme in every depth** (raw D²=965). The joint-typicality worry is resolved in the claim's
favour. Across the full measurement band (Stat 3) PMNS joint outlyingness never exceeds the
~77th percentile — it never approaches the outlier line.

**2. The θ₁₃ look-elsewhere.** sin²θ₁₃=0.022 sits at the 4.4th Haar marginal percentile — the
one soft spot. Computed directly on the ensemble (angles are NOT independent under Haar):
**P(at least one of the three angles ≤ its own 4.4th marginal percentile) = 12.65%** (≈ the
independence baseline 12.66% — the angles' lower tails are effectively independent under Haar;
two-sided version 24.2%). Since 12.65% ≳ 10%, **the wrinkle dissolves as look-elsewhere**:
finding one angle that atypical among three is an expected ~1-in-8 Haar fluctuation, not a
flagged tension. The θ₁₃ soft spot is demoted to noise.

**3. Error bands (3000 split-normal MC draws per case; NuFit-6.0 / PDG-2024 1σ).** Bands are
[2.5, 50, 97.5] percentiles of each functional's Haar percentile. **Registered claim robust:**
CKM MI band **[99.98, 99.981, 99.981]** (every functional holds its pole; stays beyond 99.9);
PMNS MI bands **lower [33.8, 39.0, 43.7]**, **upper [37.1, 41.6, 45.8]** (both wholly inside the
central 90%). Every PMNS functional stays within the central 99% across the full band. The
PMNS-Haar-typical / CKM-beyond-99.9 asymmetry survives the entire parameter band.

- **Flag (discovery-panel item, NOT the registered MI claim).** The frozen run used
  δ_PMNS = −1.98 rad (≡246.6°), stale vs current NuFit-6.0 (212° with-SK / 177° without-SK).
  δ barely enters the magnitude functionals (MI claim untouched, confirmed above), but it drives
  |J|: under current NuFit-6.0 δ the leptonic |J| percentile drops from the frozen ~58th toward
  the median/low (lower-octant MC median 40th, upper-octant median **17th**, lower band edge
  ~1st). Still Haar-typical (>0.5, kill not fired), but the discovery-panel "|J| sits at the
  Haar median" statement softens and the CP-conserving |J|→0 kill sits nearer than `results.json`
  implied — the upper octant (without-SK δ=177°) is already close to CP-conserving. This
  sharpens, not resolves, the registered DUNE/Hyper-K δ fork.
