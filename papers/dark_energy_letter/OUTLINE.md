# A parameter-free dark-energy equation of state from the multi-information of cosmic structure — letter outline

**Date 2026-07-10.** Short-letter class (PRL / JCAP-letter / MNRAS-letter, ~4–5 pp + methods).
Draft skeleton only; nothing here is asserted by the lake. Priority basis: `../notes/de_priority_sweep.md`.
Result basis: `../../experiments/cosmo_entropic_potential/` (`SUMMARY.md`, `large_volume/`,
`PREREGISTRATION.md`, `selfconsistency*/`, `epoch_check/`, `halo_grain/sweep/`).

---

## Title options

1. **A parameter-free dark-energy equation of state from the multi-information of cosmic structure**
2. **The balance of the ledger: dark energy as the maintenance cost of cosmic coordination**
   (evocative; pairs with the "two objects, one relation" framing)
3. **Structure writes its own equation of state: a pre-registered `w(z)` from the log-determinant
   of the density correlation matrix** (foregrounds the pre-registration, the discipline hook)
4. **Dark energy from the correlation entropy of the nonlinear density field** (plainest; safest
   for a hostile referee)

Recommendation: **#1 as title, #2's phrase ("the balance of the ledger") as the opening line.**

---

## Abstract (draft)

> The dark sector admits a single reading with two faces: **dark matter is the medium of cosmic
> coordination, dark energy is the standing cost of maintaining it.** We give that reading one
> falsifiable consequence. Positing that the dark-energy density tracks the **Gaussian
> multi-information** of the matter field, `ρ_DE ∝ S = −ln det C` — the log-determinant of the
> normalized density correlation matrix — the continuity equation yields a **parameter-free sign
> law**, `1 + w(a) = −(1/3) d ln S / d ln a`, in which the proportionality constant cancels. The
> law has structural teeth: `S` is provably invariant under linear growth (it reads correlation
> *shape*, never amplitude), so `w = −1` exactly through the entire linear era and the primary CMB
> is untouched; and for the class of local density transforms `S` can only fall, forbidding a
> phantom past. We **froze the pipeline and its kill conditions before** computing `S(a)` on a
> large-volume (205 Mpc/h) N-body halo catalog across `z = 3 → 0`. The frozen `w(z)` lands
> **1.36σ from the DESI DR2 best-fit `(w₀,wₐ)`, versus 3.28σ for ΛCDM**, with a phantom-divide
> crossing at `z = 0.59 ± 0.03` (physical) inside DESI's interval — driven not by a fitted
> parameter but by the epoch at which above-threshold halo formation peaks. One pre-registered kill
> condition fired (a magnitude bound, by 0.007) and is logged; the structural kill (no interior
> peak) did not. We register the crossing epoch `z = 0.59 ± 0.03` as the framework's prediction for
> DESI DR3. The result is not a fit: it is a computed, pre-registered equation of state with no free
> parameter in the sign law.

Length target: ~180 words. Trim the CMB clause first if over.

---

## Section list

### 1. Introduction (0.75 pp)
- The DESI DR2 evolving-DE signal (`w₀ > −1`, `wₐ < 0`, 2.8–4.2σ dynamical over ΛCDM), and the
  wave of `w₀wₐ` models it produced — **almost all fit fields/potentials to the data.**
- The gap we fill: a `w(z)` **computed from the density field**, not fitted. One relation, no free
  parameter in the sign law.
- The one-paragraph prior-art positioning (from `de_priority_sweep.md`): the entropy-of-structure-
  → `w(z)` idea is not new (Das & Pandey configuration entropy; Sarkar negentropy; Pandey entropic
  backreaction; Bianconi entropic gravity). **What is new is the functional (Gaussian multi-
  information, amplitude-blind), the stock κ-cancelling parameter-free law, and the frozen
  pre-registration.** State this honestly and up front.
- **The crispest single differentiator, worth its own sentence:** the two 2026 information-theoretic
  density-field probes are **complementary, near-orthogonal** to ours. Sarkar's negentropy
  `J = ½ln[σ²(1+σ²)/ln(1+σ²)]` reads the **one-point marginal** non-Gaussianity of δ; our
  `−ln det C` reads the **multi-point correlation copula** — and is provably *blind* to exactly the
  marginal transforms `J` measures. Same field, orthogonal decompositions; Sarkar diagnoses, we
  derive. Framing our functional as the copula-complement of the marginal-non-Gaussianity program is
  both honest and a clean priority statement.

### 2. The sign law (0.75 pp)
- The two-objects-one-relation reading in two sentences (DM = medium, DE = maintenance/balance),
  pointer to `lambda_maintenance_wz.md` and the Bianconi `ℋ = Λ^G` parent.
- Derivation: `ρ_DE = κ·S`, continuity `ρ̇ + 3H(1+w)ρ = 0`, `d/dt = H d/dlna` ⇒
  **`1 + w(a) = −(1/3) dlnS/dlna`**; κ cancels. Corollary table (S const → `w=−1`; rising →
  phantom; falling → thawing).
- **Eq. box** = the sign law. This is the paper's one equation.

### 3. Two structural theorems (0.75 pp)
- **Linear-growth invariance (the amplitude/shape fence).** `C_ij(a) = C_ij(0)` under `δ = D(a)δ₀`;
  `S` depends only on the copula, so `w = −1` exactly in linear theory ⇒ CMB/`r_s`/acoustic peaks
  untouched; all deviation comes from correlation *shape* change (nonlinearity, horizon). This is
  the strict-extension-of-ΛCDM guarantee.
- **Phantom-forbidden for local transforms.** For any pointwise `g`, `S(C_g) ≤ S(C_linear)`
  (Mehler expansion → convex combination of Hadamard powers → Oppenheim; verified 0 violations in
  two independent codebases, ~1700 trials). ⇒ within the local class `w ≥ −1`. **Name the escape
  hatch honestly:** N-body displacement is *nonlocal*, so the theorem does not bind the real field
  — which is exactly why the interior peak (and the DESI-like crossing) can appear.
- **Figure 1**: the fence — `S(a)` flat under linear growth to machine precision, then the
  nonlinear channel pulling it down. Source: `experiments/.../fig1_linear_invariance.png`,
  `fig2_nonlinear_S.png`.

### 4. Pre-registration (0.5 pp)
- The discipline, stated as a *feature*: pipeline + convention + kill conditions frozen at commit
  `a5beb57` **before** the large-volume data (`PREREGISTRATION.md`). Table of the kill conditions
  (K1–K7) compressed to the ones that bear: K3 (no interior peak → dead), K7 (magnitude interval),
  P1 (crossing epoch → DR3 prediction).
- **Be candid** about the retrodiction history: the small-box `−0.841` was a retrodiction with a
  post-hoc extensive/intensive convention; the freeze is what makes the *next* number a prediction.
  A hostile referee will find this anyway — own it (see §7).

### 5. Result: TNG300-1 (1.0 pp) — the core
- Pipeline: 205 Mpc/h box, 10 snapshots `z=3→0`, resolved-corner threshold rule self-selects
  `7.4×10¹¹ M⊙/h`; `C_ij = ξ_R(r_ij)/σ²_R` on real halo positions; GPU Cholesky log-det
  (reproduces CPU at `|ΔS/S| = 1.2×10⁻¹¹`).
- **Table 1 (headline)** — pull from `large_volume/SUMMARY.md` / `results.json`:
  | quantity | framework (TNG300-1) | DESI DR2 | ΛCDM |
  |---|---|---|---|
  | `w_today` | −0.833 ± 0.057 | −0.838 | −1 |
  | `(w₀,wₐ)` CPL-proj. | (−0.767, −0.742) | (−0.838, −0.62) | (−1, 0) |
  | crossing `z` | 0.59 ± 0.03 phys / 0.46 proj | 0.35, 90% [0.19,0.70] | — |
  | Mahalanobis from DESI | **1.36σ** | — | **3.28σ** |
- **Figure 2**: `w(a)` curve vs DESI CPL band, thawing, crossing marked. (Build from
  `epoch_check/cpl_projection.py` outputs; `s_of_a.py` fig3.)
- **Figure 3**: the mechanism — `k(a)` above-threshold halo count peaks `z=0.546`, `S(a)` peaks
  `z=0.590`; crossing tracks halo-formation peak, not a fitted parameter. (From `large_volume`.)
- Kill-condition verdicts: K3 does not fire (interior peak, 8/8 octant jackknife); K7 fires by
  0.007 (logged); P1 registers `z=0.59±0.03` as the DR3 prediction.
- **Figure 4 (optional / supp)**: the small-box → large-box → CAMELS-continuity ladder showing the
  volume increase moved every axis toward DESI (`selfconsistency_tng300/`, `halo_grain/sweep/`).

### 6. Discussion (0.5 pp)
- What the 1.36σ is and is not: a directional + magnitude match from a computation with no `w`
  fitted; **not** a likelihood-level test (point-vs-point vs DESI best fit).
- The thawing prediction `wₐ ≈ −(1+w₀)` (a *line* through ΛCDM, slope −1) vs DESI's steeper
  degeneracy — distinguishable, needs the DESI `(w₀,wₐ)` covariance (flag `desi_likelihood` as
  in-progress).
- **DR3 as the registered test**: crossing `z=0.59±0.03`; agreement = 68% interval overlap with
  DR3's crossing posterior; non-overlap kills the extensive branch (K2).

### 7. What a hostile referee will say — and the prepared answers (0.5 pp; can be a boxed
   "Anticipated objections" or folded into Discussion + Methods)

| Objection | Honest answer |
|---|---|
| **"`C` is a 2-point model-ξ proxy, not the real coordination operator."** | Conceded. `C_ij = ξ_R(r_ij)/σ²_R` uses the model correlation function at real halo positions; linear bias and `D(a)` cancel in the normalized `C` by construction, so only discreteness, the evolving point set, and 2nd-order bias move `S`. A full non-Gaussian `C` (3+-point) is future work; the sign law only needs the shape of the 2-point copula, and the phantom-forbidden theorem shows where higher orders could matter. |
| **"One simulation, one cosmology."** | Conceded and stated. TNG300-1 only; octant jackknife (8/8 interior peaks) is the only error bar and it shares large modes, so it *under*estimates cosmic variance. CAMELS-continuity and small-box ladder are consistency checks, not independent volumes. Independent boxes (Quijote/Abacus) are the registered next step. |
| **"The mass-threshold rule is a hidden dial — the sweep moves `w_today` by 0.28."** | The *rule* (lowest threshold resolving ≥200 halos at z=3) is frozen, not the number; on TNG300 it self-selects `7.4×10¹¹`. The threshold-ladder table is shown in full (§5): the dial is real and disclosed, and the frozen rule — not a chosen value — picks the operating point. |
| **"This is retrodiction until DR3."** | Conceded, explicitly. `−0.841` (small box) was a retrodiction with a post-hoc extensive convention; the pre-registration (§4) exists precisely so the DR3 crossing-epoch comparison is the genuine prediction. We register `z=0.59±0.03` and a 68%-overlap kill criterion. |
| **"The comoving normalization was chosen to give `w=−1`."** | The single weakest link, flagged as such (`lambda_maintenance_wz.md` §7a). `ρ_DE ∝ S` is well-posed only per unit volume, and the comoving choice is the one that makes frozen structure give `w=−1`. It is a physical argument (energy density is extensive in comoving coordination content), **not a theorem.** Named as the deepest open problem, not hidden. |
| **"Extensive-vs-intensive convention is post-hoc and against your own T-E3 intensive discipline."** | Conceded (`PREREGISTRATION.md` §5). The convention was the branch selector and was adopted after seeing B-total land on DESI. Only a derivation of the convention or an independent discriminator removes the stain; neither exists yet. The freeze fixes it forward so it can no longer be reselected per result. |
| **"Why not Shannon configuration entropy (Das–Pandey / Pandey) or negentropy (Sarkar)?"** | The Gaussian multi-information `−ln det C` is **amplitude-blind** (linear-growth invariance theorem), giving the exact-ΛCDM CMB fence and isolating the shape channel; Shannon `S_c` mixes amplitude and shape. Sarkar's negentropy `J` is the **one-point marginal** non-Gaussianity — the copula-orthogonal *complement* of our functional (`−ln det C` is invariant under exactly the marginal transforms `J` measures). We read the correlation structure they cannot see, and we *derive* `w(z)` parameter-free where they *diagnose*. See the priority note. |

### 8. Methods / Supplement
- Full pipeline (`s_of_a.py`, `halo_grain.py::op_B` B-total, `large_volume/run_test.py`), frozen
  hashes, `DECISIONS.md`, the two theorems' proofs (Mehler/Oppenheim), the self-consistency
  (open-loop vs closed-loop) correction, the causal-channel null (§4 of `SUMMARY.md`: horizons
  carry ~`10⁻¹⁶` of `S`).
- Data availability: TNG300 group catalogs (public IllustrisTNG), all scripts + `results.json`.

---

## Figures to pull (source → caption)

| Fig | Source file | Caption gist |
|---|---|---|
| 1 | `experiments/.../fig1_linear_invariance.png` + `fig2_nonlinear_S.png` | The amplitude/shape fence: `S` flat under linear growth (machine ε), falls under nonlinearity. |
| 2 | `epoch_check/cpl_projection.py` + `s_of_a.py` fig3 | `w(a)` thawing curve vs DESI CPL band; crossing at `z=0.59` marked. |
| 3 | `large_volume/results.json` (`k(a)`, `S(a)` peaks) | Mechanism: crossing tracks the halo-formation peak, not a fitted parameter. |
| 4 (supp) | `halo_grain/sweep/figures/fig_w_today_grid.png`, `selfconsistency_tng300/` | Small→large→CAMELS ladder; volume moves every axis toward DESI. |
| Table 1 | `large_volume/SUMMARY.md` | Headline: 1.36σ vs ΛCDM 3.28σ. |

---

## Citation list (from the priority sweep — group as they'll appear)

**The parent premise (gravity/Λ as entropy ledger):** Bianconi, *Gravity from entropy*, PRD 111,
066001 (2025) [arXiv:2408.14391]; Bianconi, *Thermodynamics of GfE* [arXiv:2510.22545]; Jacobson
[gr-qc/9504004; arXiv:1505.04753]; Padmanabhan [arXiv:1905.03529].

**The closest convergent art (entropy-of-structure → `w(z)`) — MUST position against:** Das &
Pandey, MNRAS 482, 3219 (2018) [arXiv:1810.07729]; Das & Pandey, MNRAS 492, 3928 (2020)
[arXiv:1907.00331]; Sarkar, negentropy diagnostic [arXiv:2602.02339]; Pandey, entropic backreaction
[arXiv:2605.28797].

**"configurational entropy DE" phrase already taken (DISTINCT):** Tsallis holographic + config
entropy [arXiv:2011.13135]; holographic DE + config entropy [arXiv:2011.07337]; extended entropic
DE [arXiv:2511.15747].

**Methodological ancestors (information beyond `P(k)`; backreaction):** Rimes & Hamilton (2005/06);
Carron (2011); Carron & Neyrinck (2012); Buchert; Räsänen; Wiltshire timescape.

**The functional itself:** Watanabe (total correlation); log-det entropy [arXiv:1309.0482].

**Data / target:** DESI DR2 BAO [arXiv:2503.14738]; TNG300 (IllustrisTNG); lognormal density field
Coles & Jones (1991); transfer function Eisenstein & Hu (1998).

---

## Open dependencies before this is submittable

1. **`desi_likelihood`** teammate result — a real likelihood-level (not point-vs-point) comparison,
   projecting the DESI posterior onto the thawing line `wₐ = −(1+w₀)`. Table 1's σ values are
   point-vs-point placeholders until then.
2. **arXiv:2602.02339 (Sarkar) resolved** — negentropy is one-point marginal non-Gaussianity, the
   copula-orthogonal complement of our functional (positioning paragraph above reflects this).
   **arXiv:1907.00331 (Das–Pandey 2020) still to re-read in full text** (PDF did not parse) — confirm
   they use no correlation-matrix object before the positioning paragraph is frozen.
3. **Independent-box check** (Quijote/Abacus) or at minimum an honest statement that TNG300 is the
   sole volume — the jackknife under-counts cosmic variance.
4. The comoving-normalization and extensive-vs-intensive open problems (§7) stated as open, not
   resolved.
</content>
