# CKM in the hierarchical measure — the missing half: CKM is TYPICAL of Froggatt-Nielsen, and PMNS is not. Two books, each typical of its own measure.

**Date 2026-07-11.** Pre-commitments in `DECISIONS.md` (written before any ensemble existed);
measure/coefficients/tests/kills all frozen there. Data `results.json`, code `fn_ensemble.py`
(reuses `../run_mixing.py`'s exact functionals — same 3×3 machinery, no reimplementation).

The companion Haar test (`../SUMMARY.md`) showed CKM is Haar-**atypical** (99.98th-pct MI) but
never that it is **typical of anything**. This test supplies that half. The measure is
Froggatt–Nielsen with the top-ranked natural charge texture of arXiv:2306.08026
(Phys. Rev. D 111 (2025) 015042): X_Q=(3,2,0), X_u=(−4,−2,0), X_d=(−3,−3,−3), whose charge
differences reproduce the Wolfenstein CKM hierarchy parameter-free (|V_us|~ε, |V_cb|~ε²,
|V_ub|~ε³). ε = 0.225 (Cabibbo, fixed not fit). O(1) coefficients: |c| log-uniform[⅓,3], phases
uniform. Y_ij = c_ij ε^|X_i−X_j|; V_CKM = U_uL† U_dL from the left singular vectors. N = 100k
primary, 50k per robustness variant.

## Verdict per test

| test | result | verdict |
|---|---|---|
| **(a) CKM marginal** | MI **72.6**, S_onehot 74.7, PR_sv 67.7, d_anarchy 71.0, d_perm 31.1, \|J\| **23.6** — **all six inside central 90%** | **CKM is FN-TYPICAL in every functional.** PASS |
| **(b) joint / double-extremity** | 27.4% of FN samples are ≥ as aligned as CKM; within that aligned subset CKM's \|J\| is at the **46th** pct and \|sinδ\| at the 78th | **The "aligned AND CP-tiny" double extremity is the GENERIC FN outcome** — one fact, not two coincidences. PASS |
| **(c) control — PMNS** | MI **0.0**, S_onehot 0.0, PR_sv 0.0, d_anarchy 0.0 (d_perm 100, \|J\| 100) | **PMNS is maximally FN-ATYPICAL** — the FN quark measure essentially never makes a matrix as anarchic as PMNS. Two-books measure-separation holds. PASS |
| **(d) sensitivity** | CKM MI pct 64.6–78.7, **all six central in every variant**; PMNS MI pct 0.00–0.10 in every variant | **No verdict flips** across 3 c-distributions and ε∈{0.20,0.225,0.25}. Robust. |

## The one-sentence answer

**Yes — the flavor sector is two books, each typical of its own measure.** Quark mixing (CKM)
sits in the bulk of the hierarchical (Froggatt–Nielsen) measure (MI 72.6th pct) while being a
>3.5σ outlier of the Haar/anarchic measure (99.98th pct); lepton mixing (PMNS) is the exact
mirror — Haar-typical (36.7th pct, `../SUMMARY.md`) and maximally FN-atypical (0.0th pct). The
two books are not distinguished by accident but **by measure**: each is a generic draw of a
different generation-coupling law.

## What the numbers say, in full (exhaustive, adverse outcomes included)

1. **The alignment is generic FN, the anarchy is not.** FN-ensemble MI: mean 0.845, median
   0.859, central-90% [0.623, 1.052]; CKM's MI = 0.956 lands at the 72.6th pct — high-bulk, not
   a tail. Haar MI mean was 0.265; CKM there was the 99.98th pct. **The same matrix is bulk in
   one measure and a 3.5σ tail in the other.** That is the whole content of "two books": CKM's
   near-comonotonicity is the *expected* output of a hierarchical charge law and an *extreme
   accident* under structurelessness.

2. **CKM's CP-tininess is FN-generic, not extreme.** Under Haar, CKM's |J| sat at the **0.09th**
   percentile (extreme-CP-conserving); under FN it sits at the **23.6th** percentile — inside
   the bulk. The FN measure *predicts* a small |J| because it predicts alignment, and (test b)
   conditioning on CKM-level alignment leaves |J| dead-central (46th pct). This is the ensemble
   realization of the sakharov-ledger J-bound: ensemble Spearman(MI, |J|) = **−0.50** (alignment
   structurally suppresses CP capacity; cf. −0.72 for Haar). The quark book's tiny CP violation
   is not a separately-tuned small phase — |sinδ|=0.91 is near-maximal and typical (82nd pct) —
   it is the structural shadow of the alignment, and that shadow is generic in *both* measures'
   own terms.

3. **PMNS is off the FN chart on every alignment functional.** MI/S_onehot/PR_sv/d_anarchy all
   at the 0.0th percentile; d_perm and |J| at the 100th (PMNS is *farther* from any permutation
   and *more* CP-violating than any FN quark draw). In 100k FN samples not one is as anarchic as
   the observed PMNS. The measure-separation is not marginal — it is total on the coordination
   axis. (PMNS |sinδ| at the 82nd pct is the one FN-compatible coordinate — orientation is
   generic in both books, only dependence *strength* differs; cf. sakharov note phase
   genericity.)

4. **Robustness (test d), reported straight including the drift.** Weakest CKM-MI percentile was
   64.6 (ε=0.20), strongest 78.7 (ε=0.25) — ε up ⇒ more alignment ⇒ CKM slightly more central;
   the complex-Gaussian and log-normal (the 2306.08026 prior) coefficient distributions give
   70.5 and 76.9. |J| percentile drifts 15.3 (ε=0.25) → 36.8 (ε=0.20) but never leaves the
   bulk. Every single variant keeps all six CKM functionals central and PMNS MI at ~0. No
   cherry-picking was needed and none is hidden: the verdict is a fact about CKM, not about a
   chosen distribution.

## Kills — none fired; both pre-stated kills were the adverse branches and neither occurred

- **"CKM outside FN central 90% on MI ⇒ atypical of both measures (a discovery)"** — did NOT
  fire. CKM is at 72.6th pct (all variants 64.6–78.7). CKM is typical of the hierarchical
  measure.
- **"PMNS FN-typical ⇒ two-books distinction collapses"** — did NOT fire. PMNS is at the 0.0th
  FN percentile. The distinction is maximally intact.

## Standing result added to the record

The Rung-1 flavor read is now **symmetric and complete**: CKM = Haar-atypical / FN-typical;
PMNS = Haar-typical / FN-atypical. Neither book is "structured vs structureless" in the
absolute — each is the *bulk* of its own generation-coupling measure and the *tail* of the
other's. This upgrades the parent SUMMARY's "one comonotone book, one anarchic book" from a
one-sided typicality (only the anarchic/Haar half was a demonstrated typicality) to a genuine
two-measure statement: **the flavor sector is two books, each typical of its own measure**, and
the measures are the two standard sketches physics already uses for the two sectors (Haar
anarchy for leptons [Hall–Murayama–Weiner]; Froggatt–Nielsen hierarchy for quarks).

Kills going forward: this reading dies if the observed CKM leaves the FN central 90% under a
*standard published* charge texture with ε fixed to Cabibbo (no realistic path — robust across
the texture's own paper's prior), or if PMNS is shown FN-typical under such a texture (it is at
the 0th percentile). The already-registered DUNE/Hyper-K δ fork (`../SUMMARY.md`) still governs
the anarchic half.

## Sources (verified this session)
- Froggatt & Nielsen, Nucl. Phys. B147 (1979) 277 — the FN mechanism. [standard]
- arXiv:2306.08026 / Phys. Rev. D 111 (2025) 015042 — the charge texture and O(1)-coefficient
  ensemble taken as the measure. [verified]
- arXiv:2411.05398 — cross-checked SU(5) FN benchmark; not used as primary (its charge
  differences give |V_us|~ε², not Cabibbo). [verified, logged in DECISIONS.md]
