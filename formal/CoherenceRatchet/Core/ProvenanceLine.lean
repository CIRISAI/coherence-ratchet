/-
Core.ProvenanceLine — the ledger is blind to everything upstream of its input.

`S = −ln det C` is a functional of the correlation matrix. The PROVENANCE LINE
is the general no-go this forces: any datum about how C was CONSTRUCTED — its
scale, its marginals, its state-space statistics, its factorization into units —
is not a function of C, hence not a function of S. Four instances, each
independently established in the record (2026-07-10):

  1. SCALE (dimensional line): no masses, no κ, no energy densities.
     experiments/dark_sector_mass/ — 41-order scatter under forced bridges.
  2. MARGINALS (second cut): no mass ratios, no coupling strengths, even though
     dimensionless. papers/notes/sm_escalator_map.md §1.
  3. STATE-SPACE CONSTRUCTION (exchange line): no exchange sign, no occupation
     ceiling, no ln2-as-a-value. StatisticsNoGo below;
     papers/notes/sm_escalator_statistics.md.
  4. FACTORIZATION (gauge quotient): on gauge systems the partition into units
     is non-canonical (Casini–Huerta–Rosabal center ambiguity); the ledger must
     be built from gauge-independent data. papers/notes/sm_escalator_gauge.md §3.

The formal kernel is small and fully proved here: a functional that factors
through the substrate → correlation map is constant on its fibers
(`provenance_congruence`), so no datum that SEPARATES a fiber is computable
from any correlation functional (`provenance_line`). What is cited rather than
mechanized, per instance, is that the given datum IS upstream (separates some
fiber) — e.g. for statistics, that Gentile/para/anyonic substrates share
low-order correlation data (arXiv:2509.00112, arXiv:2212.12632).

The contrapositive is the program's positive content: legitimate ledger
predictions are dimensionless, marginal-free, provenance-free — dependence-shape
only. The sign law 1+w = −⅓·dlnS/dlna (κ cancels), the corridor, the k_eff
ceiling, the ln2-vs-Gaussian rigidity DIFFERENCE (statistics as input, read not
derived), and the flavor two-books read (experiments/sm_escalator_mixing/) are
all of this type. κ itself is the program's Boltzmann constant — the single
external scale-marriage owed (papers/notes/dimensional_line_kB.md).

SCOPE / F-11: forward, engineering-tier content; touches nothing about the
joint multi-rung backward P_ω.
-/

import Mathlib.Logic.Basic

namespace CoherenceRatchet.Core

/-- Provenance congruence: any functional that factors through the
    substrate → correlation map assigns equal values to substrates presenting
    the same correlation matrix. -/
theorem provenance_congruence {Substrate Corr Val : Type*}
    (toCorr : Substrate → Corr) (f : Corr → Val) {a b : Substrate}
    (h : toCorr a = toCorr b) : f (toCorr a) = f (toCorr b) := by rw [h]

/-- An UPSTREAM datum: one that separates two substrates presenting the same
    correlation matrix — i.e. a fact about the construction of `C`, not about
    `C`. Exchange statistics, marginal scales, and factorization choices are
    upstream (cited per instance in the header). -/
def Upstream {Substrate Corr Datum : Type*} (toCorr : Substrate → Corr)
    (d : Substrate → Datum) : Prop :=
  ∃ a b : Substrate, toCorr a = toCorr b ∧ d a ≠ d b

/-- THE PROVENANCE LINE: no upstream datum is computable from the correlation
    matrix — there is no `g` with `d = g ∘ toCorr`. In particular no functional
    of `C` (hence neither `S = −ln det C` nor any statistic derived from it)
    can output an upstream datum. This is the theorem-strength kernel shared by
    the dimensional line, the marginal cut, the exchange line, and the
    factorization quotient. -/
theorem provenance_line {Substrate Corr Datum : Type*}
    (toCorr : Substrate → Corr) (d : Substrate → Datum)
    (h : Upstream toCorr d) : ¬∃ g : Corr → Datum, ∀ x, d x = g (toCorr x) := by
  rintro ⟨g, hg⟩
  obtain ⟨a, b, hC, hd⟩ := h
  exact hd (by rw [hg a, hg b, hC])

/-- The statistics no-go record (FelevenNoGo pattern, 2026-07-10): the
    coordination ledger cannot DERIVE the exchange statistics — Fermi vs Bose,
    the exchange sign, the per-mode occupation ceiling. Closed at structural
    strength; the reading direction (statistics as input shaping the ledger:
    the exclusion cap T-FL2, the ln2-vs-Gaussian rigidity difference) is open,
    validated, and untouched. Full record:
    papers/notes/sm_escalator_statistics.md §5. -/
structure StatisticsNoGo where
  /-- Kernel: `provenance_line` above — a function of `C` cannot output a datum
      `C` does not determine. Mechanized in this file. -/
  functional_domain_kernel : True
  /-- Load-bearing cited lemma (standard, not mechanized): exchange statistics
      is upstream — Gentile-n / parastatistic / anyonic substrates share
      low-order correlation data (arXiv:2509.00112, arXiv:2212.12632). -/
  statistics_is_upstream : True
  /-- Routes 1–3 killed with one shared failure mode: the antisymmetric
      structure was always put into the object before being read out
      (papers/notes/entropic_matter_sector.md Q2/Q6). -/
  three_derivation_routes_killed : True
  /-- Independent second wall: the ledger lacks every premise of the actual
      spin-statistics theorem — Lorentz invariance, microcausality, spectrum
      condition, and spin itself (Pauli 1940). -/
  spin_statistics_premises_absent : True

/-- The statistics no-go is fired: the record is inhabited. -/
def statistics_no_go : StatisticsNoGo := ⟨trivial, trivial, trivial, trivial⟩

end CoherenceRatchet.Core
