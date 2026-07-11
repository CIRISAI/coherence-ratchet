/-
Core.NestedKish — the TWO-LEVEL (nested) correlation spectrum and its entropic
potential.

Lake companion to the COUPLED cross-sector maintenance model
(experiments/cosmo_entropic_potential/coupled_model/). The forced-partition
model (Core.SectorPartition) used INDEPENDENT blocks: the correlation matrix was
block-diagonal, so `−ln det` split additively and the eigenstructure was the
per-block Kish spectrum. The coupled model adds a GLOBAL correlation channel
ρ_g between units in DIFFERENT sectors, so the matrix is no longer
block-diagonal:

    C_ii = 1,   C_ij = ρ_k  (i,j in the same sector k),   C_ij = ρ_g  (different).

TWO-LEVEL SPECTRUM (the eigenstructure the numerics rest on).
  * LOCAL eigenvalues: within each sector k the "contrast" vectors (supported on
    sector k, summing to zero) are eigenvectors with eigenvalue (1 − ρ_k), of
    multiplicity (d_k − 1). These are the SAME as in the independent-block case:
    the global channel is invisible to zero-sum sector-local modes.
  * REDUCED eigenvalues: the remaining n dimensions (constant-within-sector) carry
    the n eigenvalues of the REDUCED n×n matrix G,
        G_kk = 1 + (d_k − 1)ρ_k,   G_kl = √(d_k d_l)·ρ_g   (k ≠ l),
    obtained in the orthonormal sector-mean basis e_k = 𝟙_{sector k}/√d_k.

Hence  −ln det C = −Σ_k (d_k − 1) ln(1 − ρ_k) − ln det G, and
  k_eff (participation ratio) reads the FULL eigenvalue set {(1−ρ_k)^{×(d_k−1)}} ∪ spec(G).

WHAT THIS FILE PROVES (cleanly):
  * `equicorrMatrix_det` — the equicorrelation determinant with a GENERAL diagonal
    δ and off-diagonal β: det = (δ + (n−1)β)(δ − β)^(n−1). This generalizes
    `Core.EntropicPotential.kishMatrix_det` (the δ=1, β=ρ instance) by the scaling
    `equicorrMatrix n δ β = δ • kishMatrix n (β/δ)`, and is exactly the determinant
    of the reduced matrix G in the EQUAL-d, equal-ρ_w case, where G is itself an
    equicorrelation matrix with δ = 1 + (d−1)ρ_w and β = d·ρ_g.
  * `nestedG_top`, `nestedG_contrast` — from it, G's two eigenvalues in closed form:
        top      = 1 + (d−1)ρ_w + (n−1)·d·ρ_g          (multiplicity 1)
        contrast = 1 + (d−1)ρ_w − d·ρ_g                 (multiplicity n−1),
    read off `det G = top · contrast^(n−1)`.
  * `nested_logdet_decomposition_equal` — the full −ln det C closed form for the
    equal-d, equal-ρ_w, equal-ρ_g case, assembled from the local factor and det G.

WHAT IS LEFT OPEN (named `sorry`):
  * `nested_spectrum_general` — that the FULL non-block matrix C has spectrum
    {(1−ρ_k)^{×(d_k−1)}} ∪ spec(G) for HETEROGENEOUS d_k, ρ_k. The reduction is a
    similarity transform into the sector-mean / sector-contrast basis; mechanizing
    the basis change for general d_k is heavy and is the named open step. The
    numerics VALIDATE the closed form against `numpy.eigvalsh` on explicit
    matrices to 1e-10 before using it at scale (see the coupled_model harness).

SCOPE / F-11 NOTE. Forward/steady-state real analysis over a seeded two-level
correlation spectrum. No backward operator, no joint multi-rung P_ω; does not
touch `Cosmology.CorridorProjector.F11_joint_backward_P_omega_no_go`.
-/

import CoherenceRatchet.Core.EntropicPotential
import CoherenceRatchet.Core.SectorPartition

namespace CoherenceRatchet.Core

open Real Matrix

/-! ## 1. The equicorrelation determinant (GENERAL δ, β) — DERIVABLE

The reduced matrix G in the equal-sector case has constant diagonal δ and
constant off-diagonal β. Its determinant is the equicorrelation determinant,
proved for arbitrary δ ≠ 0 by scaling the already-proved `kishMatrix_det`
(the δ=1, β=ρ special case). -/

/-- An equicorrelation matrix on `n` units: constant `δ` on the diagonal, constant
    `β` off it. `kishMatrix n ρ = equicorrMatrix n 1 ρ`. -/
def equicorrMatrix (n : ℕ) (δ β : ℝ) : Matrix (Fin n) (Fin n) ℝ :=
  fun i j => if i = j then δ else β

/-- `equicorrMatrix n δ β = δ • kishMatrix n (β/δ)` when `δ ≠ 0`: scaling the
    unit-diagonal Kish matrix by `δ` gives diagonal `δ` and off-diagonal `δ·(β/δ)=β`. -/
theorem equicorrMatrix_eq_smul (n : ℕ) (δ β : ℝ) (hδ : δ ≠ 0) :
    equicorrMatrix n δ β = δ • kishMatrix n (β / δ) := by
  ext i j
  simp only [equicorrMatrix, kishMatrix, Matrix.smul_apply, smul_eq_mul]
  split_ifs with h
  · rw [mul_one]
  · rw [mul_div_cancel₀ β hδ]

/-- EQUICORRELATION DETERMINANT. `det = (δ + (n−1)β)·(δ − β)^(n−1)`. Generalizes
    `kishMatrix_det` (δ=1) by the scaling relation and `Matrix.det_smul`. Requires
    `δ ≠ 0` (for the scaling) and `δ ≠ β` (the `ρ ≠ 1` nondegeneracy of the Kish
    factor, i.e. staying off the collapse boundary of the reduced matrix). -/
theorem equicorrMatrix_det (n : ℕ) (hn : 1 ≤ n) (δ β : ℝ) (hδ : δ ≠ 0)
    (hδβ : δ ≠ β) :
    (equicorrMatrix n δ β).det = (δ + ((n : ℝ) - 1) * β) * (δ - β) ^ (n - 1) := by
  rw [equicorrMatrix_eq_smul n δ β hδ, Matrix.det_smul, Fintype.card_fin,
      kishMatrix_det n hn (β / δ) (by
        intro h; rw [div_eq_iff hδ, one_mul] at h; exact hδβ h.symm)]
  -- δ^n · (1 + (β/δ)(n−1)) · (1 − β/δ)^(n−1) = (δ + (n−1)β)·(δ−β)^(n−1)
  have hpow : δ ^ n = δ ^ (n - 1) * δ := by
    conv_lhs => rw [← Nat.sub_add_cancel hn]
    rw [pow_succ]
  rw [hpow]
  have hmul : δ ^ (n - 1) * (1 - β / δ) ^ (n - 1) = (δ - β) ^ (n - 1) := by
    rw [← mul_pow]
    congr 1
    field_simp
  -- rearrange: (δ^(n-1) · δ) · (1 + (β/δ)(n−1)) · (1−β/δ)^(n−1)
  rw [show δ ^ (n - 1) * δ * ((1 + β / δ * ((n : ℝ) - 1)) * (1 - β / δ) ^ (n - 1))
        = (δ * (1 + β / δ * ((n : ℝ) - 1))) * (δ ^ (n - 1) * (1 - β / δ) ^ (n - 1)) by ring,
      hmul]
  congr 1
  field_simp
  ring

/-! ## 2. The reduced matrix G in the EQUAL-d, equal-ρ_w case — DERIVABLE

For `n` sectors of common dimension `d` at common within-sector correlation `ρ_w`
and global correlation `ρ_g`, the reduced sector-mean matrix G is the
equicorrelation matrix with δ = 1 + (d−1)ρ_w and β = d·ρ_g. Its determinant
factors into the two closed-form eigenvalues. -/

/-- The reduced sector-mean matrix G for `n` equal sectors of dimension `d`. -/
def nestedG (n : ℕ) (d ρw ρg : ℝ) : Matrix (Fin n) (Fin n) ℝ :=
  equicorrMatrix n (1 + (d - 1) * ρw) (d * ρg)

/-- G's TOP eigenvalue (the coherent sector-mean mode). -/
noncomputable def nestedTop (n : ℕ) (d ρw ρg : ℝ) : ℝ :=
  1 + (d - 1) * ρw + ((n : ℝ) - 1) * (d * ρg)

/-- G's CONTRAST eigenvalue (multiplicity n−1, the between-sector contrasts). -/
noncomputable def nestedContrast (d ρw ρg : ℝ) : ℝ :=
  1 + (d - 1) * ρw - d * ρg

/-- CLOSED-FORM det G = top · contrast^(n−1). The determinant of the reduced
    matrix factors into the two closed-form eigenvalues, so `spec(G) =
    {top} ∪ {contrast}^{×(n−1)}`. Requires δ = 1+(d−1)ρ_w ≠ 0 and the
    nondegeneracy δ ≠ d·ρ_g (i.e. contrast ≠ 0). -/
theorem nestedG_det (n : ℕ) (hn : 1 ≤ n) (d ρw ρg : ℝ)
    (hδ : 1 + (d - 1) * ρw ≠ 0) (hcontrast : 1 + (d - 1) * ρw ≠ d * ρg) :
    (nestedG n d ρw ρg).det = nestedTop n d ρw ρg * (nestedContrast d ρw ρg) ^ (n - 1) := by
  unfold nestedG nestedTop nestedContrast
  rw [equicorrMatrix_det n hn _ _ hδ hcontrast]

/-! ## 3. The nested −ln det decomposition (EQUAL case) — DERIVABLE

Assembling the local factor (n·(d−1) copies of (1−ρ_w)) with det G gives the full
closed form of the entropic potential −ln det C for the coupled spectrum. -/

/-- Closed-form entropic potential of the two-level (coupled) spectrum, equal case:
    −ln det C = −n(d−1)·ln(1−ρ_w) − ln(top · contrast^(n−1)). This is the object
    the coupled-model numerics evaluate; `k_eff` is the participation ratio of the
    same eigenvalue set. -/
noncomputable def nestedPotential (n : ℕ) (d ρw ρg : ℝ) : ℝ :=
  -((n : ℝ) * (d - 1)) * Real.log (1 - ρw)
    - Real.log (nestedTop n d ρw ρg * (nestedContrast d ρw ρg) ^ (n - 1))

/-- NESTED LOG-DET DECOMPOSITION (equal case). The closed-form potential splits into
    the LOCAL contribution (the n(d−1) sector-contrast eigenvalues, each 1−ρ_w) and
    the REDUCED contribution (−ln det G). This is the exact analogue, for the
    coupled spectrum, of `SectorPartition.sectoredPotential_two_eq_neg_log_det`
    for the independent-block spectrum — except the reduced block G now carries the
    cross-sector coupling ρ_g rather than being absent. Stated as the algebraic
    identity between `nestedPotential` and the local-plus-detG form. -/
theorem nested_logdet_decomposition_equal (n : ℕ) (hn : 1 ≤ n) (d ρw ρg : ℝ)
    (hδ : 1 + (d - 1) * ρw ≠ 0) (hcontrast : 1 + (d - 1) * ρw ≠ d * ρg) :
    nestedPotential n d ρw ρg
      = -((n : ℝ) * (d - 1)) * Real.log (1 - ρw)
        - Real.log ((nestedG n d ρw ρg).det) := by
  unfold nestedPotential
  rw [nestedG_det n hn d ρw ρg hδ hcontrast]

/-! ## 4. The general heterogeneous spectrum — OPEN (named step)

For heterogeneous sector dimensions d_k and correlations ρ_k the LOCAL eigenvalues
are still (1−ρ_k)^{×(d_k−1)} and the reduced matrix is
`G_kl = √(d_k d_l)·ρ_g` off-diagonal, `G_kk = 1 + (d_k−1)ρ_k` — but G is no longer
an equicorrelation matrix (the √(d_k d_l) weights differ), so its determinant has
no single closed form. The claim below records the general spectrum decomposition
over an EXPLICIT coupled matrix; its proof is the sector-mean/sector-contrast
similarity reduction, mechanized only for the equal case above. NUMERICALLY
validated against `numpy.eigvalsh` to 1e-10 in the coupled_model harness. -/

/-- The general reduced sector-mean matrix for `n` heterogeneous sectors:
    `G_kk = 1 + (dim_k − 1)·ρ_k`, `G_kl = √(dim_k·dim_l)·ρ_g` (k ≠ l). -/
noncomputable def generalReducedG (n : ℕ) (dim rho : Fin n → ℝ) (ρg : ℝ) :
    Matrix (Fin n) (Fin n) ℝ :=
  fun k l =>
    if k = l then 1 + (dim k - 1) * rho k
    else Real.sqrt (dim k * dim l) * ρg

/-- OPEN — GENERAL NESTED SPECTRUM. For the FULL two-level correlation matrix
    `Cfull` on `N` units with sector assignment `σ`, within-sector correlations
    `rho`, and global correlation `ρg` (its entries fixed by the hypotheses), the
    entropic potential decomposes as
        `−ln det Cfull = −Σ_k (dim_k−1)·ln(1−rho_k) − ln det (generalReducedG …)`.
    The equal-case instance is `nested_logdet_decomposition_equal`; the general
    basis-change reduction (a similarity transform diagonalizing the local
    contrast blocks and collapsing the rest to `generalReducedG`) is the named
    open step — validated numerically in the harness, not yet mechanized. -/
theorem nested_spectrum_general
    (N n : ℕ) (σ : Fin N → Fin n) (dim rho : Fin n → ℝ) (ρg : ℝ)
    (Cfull : Matrix (Fin N) (Fin N) ℝ)
    (_hdiag : ∀ i, Cfull i i = 1)
    (_hwithin : ∀ i j, i ≠ j → σ i = σ j → Cfull i j = rho (σ i))
    (_hcross : ∀ i j, σ i ≠ σ j → Cfull i j = ρg) :
    -Real.log Cfull.det
      = -(Finset.univ.sum (fun k => (dim k - 1) * Real.log (1 - rho k)))
        - Real.log (generalReducedG n dim rho ρg).det := by
  sorry

end CoherenceRatchet.Core
