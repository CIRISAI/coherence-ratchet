# Pre-registration — the tt-bar spin-density matrix as a corridor candidate

Date: 2026-05-21. Committed BEFORE results. One of three parallel particle-physics
shape-observable investigations (alongside E4 decay branching fractions and
pp_cp CP-violation structure). Honest prior: NULL (see E4 and pp_cp).

## 0. Is the tt-bar spin-density matrix a coordinated rung?

State it plainly, before any data. **No — not in the framework's sense. This
test is run as an honest check, not because the framework predicts a hit.**

The framework's corridor claim (CLAUDE.md, Piece 3; StructuralClaims Claim 4)
attaches to *coordinated rungs* — substrates with sustained coordination and
identifiable active maintenance work γ·M(t) (Piece 2; dρ/dt with a corridor
attractor). The two-particle spin state of a tt-bar pair produced at the LHC is
none of these:

- The tt-bar spin state is a *single-shot* quantum object. It is created at the
  production vertex by the QCD/EW matrix element and decays ~10⁻²⁵ s later
  before hadronisation. There is no time-extended dynamics dρ/dt, no
  equilibrium, no attractor — and therefore no maintenance work γ·M(t) to be in
  balance with. It is a kinematic object, not a coordinated rung.
- The spin-correlation coefficients C_ij are fixed by the Standard Model
  Lagrangian (the tt production matrix element + the top → Wb decay as a spin
  analyzer). They are a prediction, not a maintained state.
- This is the same disqualification E4's decay channels suffered: a particle
  observable is set by the Lagrangian, not by an actively-coordinated process.

So the honest framework-internal expectation is that the corridor does not
apply, OR applies only as a descriptive statistic with no corridor meaning.
This is nonetheless the *least-null* of the three candidates because the
spin-density matrix is a genuine shape observable within a fixed bulk: the
production cross-section (total rate) and the trace normalisation are fixed,
and the spin-correlation pattern is the scale-invariant shape within that bulk
— which matches the structure of the CMB orthogonality theorem
(CMBOrthogonality.lean: shape sector orthogonal to bulk power). The candidate
is well-chosen; the prior remains null.

## 1. The data

CMS Collaboration, "Measurements of polarization and spin correlation and
observation of entanglement in top quark pairs using lepton+jets events from
proton-proton collisions at √s = 13 TeV" (2024). HEPData record ins2829523 /
153301, DOI 10.17182/hepdata.153301.v1/t1, Table "Results for full matrix
inclusive from m(tt)", Figure 17 upper panel.

Provenance verified via the DataCite DOI API: creator "CMS Collaboration",
publisher HEPData, publicationYear 2024, reaction "P P --> TOP TOPBAR" at
13000 GeV. The local file `cms_fullmatrix_inclusive_mtt.json` was downloaded in
a prior run of this task; its 15 coefficients are exactly the standard tt-bar
spin-density-matrix parametrisation. Real data only. No fabrication. The
HEPData download/search API is Cloudflare-blocked in this environment; the
record page (https://www.hepdata.net/record/153301) and the DataCite DOI
record both resolve and confirm the file's identity.

The table gives 15 measured coefficients (column "Measured coefficient value",
with stat and syst errors): the net polarizations and the spin-correlation
matrix elements of the inclusive tt-bar sample.

## 2. The shape construction

The tt-bar two-particle spin state is fully described by the 4×4 spin-density
matrix (one qubit per top, in the {r, k, n} helicity basis):

  R = (1/4) [ I⊗I + Σ_i B_i⁺ (σ_i⊗I) + Σ_i B_i⁻ (I⊗σ_i)
              + Σ_{i,j} C_ij (σ_i⊗σ_j) ]

with i,j ∈ {r,k,n}. R is a 4×4 Hermitian, unit-trace, positive-semidefinite
density matrix. Its four real eigenvalues {λ₁,...,λ₄} sum to 1 (Tr R = 1) and
are non-negative — i.e. they form a genuine probability distribution on the
4-simplex. **The eigenvalue spectrum of R is the matrix shape observable the
task specifies.** It is the right object: eigenvalues are basis-independent
(unaffected by helicity-frame choice), scale-invariant within the fixed Tr = 1
bulk, and a real spectrum, not a hand-built distribution.

### Building R from the 15 coefficients (pre-registered mapping)

The CMS table coefficients map to the parametrisation as:
- Net polarizations: P_r, P_n, P_k → B⁺ = (B_r⁺, B_k⁺, B_n⁺) for the top;
  P̄_r, P̄_n, P̄_k → B⁻ for the antitop.
- Diagonal spin correlations: C_rr, C_nn, C_kk.
- Off-diagonal: the table gives the symmetric/antisymmetric combinations
  C_ij⁺ = C_ij + C_ji and C_ij⁻ = C_ij − C_ji for (i,j) ∈ {(n,r),(r,k),(n,k)}.
  Recover C_ij = (C_ij⁺ + C_ij⁻)/2 and C_ji = (C_ij⁺ − C_ij⁻)/2.
- The coefficient "c" (value ≈ 0.938) is the CMS entanglement-proxy quantity
  (−tr[C]−1 form), NOT a matrix element; it is excluded from R, used only as a
  cross-check that C_rr+C_nn+C_kk reproduces it.

R is then assembled and symmetrised (R ← (R+R†)/2), and its eigenvalues
computed by `numpy.linalg.eigvalsh`.

### The shape observable (PRIMARY)

1. λ = sorted eigenvalues of R, descending. (N = 4.)
2. If any λ_i < 0 within measurement error, clip to 0 and renormalise Σλ = 1
   (small negative eigenvalues from measurement noise are physical-positivity
   violations, reported explicitly; not a construction failure unless large).
3. k_eff = 1/Σλ_i², ρ = (N·/k_eff − 1)/(N − 1) with N = 4.
4. Interpretation: ρ→1 = one eigenvalue dominates (a near-pure two-qubit state,
   rigidity); ρ→0 = the four eigenvalues equal, R ∝ I (maximally mixed, chaos);
   a corridor = a bounded interior band.

### Uncertainty propagation (mandatory — single dataset)

Unlike E4/pp_cp this is ONE measurement, not an ensemble of parents, so the
corridor-band test cannot be "do parents cluster". Instead the spread is the
*measurement uncertainty* on ρ. Pre-registered: a Monte-Carlo error
propagation. Draw each of the 15 coefficients from a Gaussian with mean = the
measured value and σ = quadrature sum of its stat and syst errors (errors
treated as independent — a stated approximation, the full covariance is not in
the table), assemble R, compute ρ, repeat 20000 times. Report the ρ
distribution: median and 16/84 percentiles.

### Cross-checks (reported, not the test)

- The four eigenvalues of the central-value R, and whether R is a valid density
  matrix (all λ ≥ 0 within error).
- ρ computed from the SM-predicted coefficients (the table's "Powheg+P8
  predicted coefficient" column, group 1) — does the SM prediction land in the
  same place as the measurement? This is the analogue of E4's confound check:
  if data and SM prediction give the same ρ, then ρ carries no information the
  SM Lagrangian didn't already fix (expected — see section 0).
- ρ of the 15-coefficient vector treated naively as a flat distribution
  (|coeff|² normalised) — reported for contrast with the eigenvalue construction
  but explicitly NOT a matrix shape observable.

## 3. What counts as a corridor — the pre-registered bar

A corridor claim is NOT "ρ landed somewhere in (0,1)". For a single-dataset
measurement the tight-band criterion is applied to the MC ρ distribution:

- **CORRIDOR (framework hit):** the MC ρ distribution has its 16–84 percentile
  interval ENTIRELY inside the A3+ reference corridor ρ ∈ [0.17, 0.35], AND the
  interval width ≤ 0.18 (it will be far narrower — this is one measurement —
  so effectively: the median sits inside [0.17, 0.35] with the measurement
  error not straddling a boundary). A hit additionally OWES, per task
  discipline, an explanation of why this substrate qualifies as a coordinated
  rung when E4's decay channels did not — and section 0 already states it does
  not, so a numerical hit would be reported as a coincidence of the descriptive
  statistic, not framework support.
- **NULL — pole pile-up:** the ρ distribution sits at a pole, ρ > 0.55
  (rigidity: R near-pure) or ρ < 0.12 (chaos: R near-maximally-mixed).
- **NULL — outside the corridor band:** ρ lands in (0.12, 0.17) or (0.35, 0.55)
  — a value, but not in the A3+ corridor band.
- **NULL — uninformative:** ρ is dominated by measurement error spanning more
  than the 0.18 band width, OR ρ equals the SM-prediction ρ within error (the
  observable carries nothing the Lagrangian didn't fix).
- **CONSTRUCTION FAILURE:** R has a large-magnitude negative eigenvalue beyond
  measurement error (the assembled matrix is not a physical density matrix) —
  report and stop, do not force a verdict.

A wide window is explicitly NOT a corridor. E4's 0.43-wide window was the
explicit anti-criterion. The bar is the tight band ρ ∈ [0.17, 0.35] above.

## 4. Honest commitments

- The prior is NULL. A corridor claim must clear section 3's bar to be reported
  as anything other than null.
- The tt-bar spin-density matrix is not a coordinated rung (section 0); even a
  numerical "hit" inside [0.17, 0.35] would be a coincidence of where a 4×4
  single-shot quantum state's eigenvalue concentration happens to land, not
  framework support, and would be reported with that caveat. The framework owes
  — and cannot pay — an account of maintenance dynamics γ·M(t) for a state that
  lives 10⁻²⁵ s.
- Nulls reported as nulls.
- Real data only. The data-availability outcome is itself reported: HEPData's
  API is Cloudflare-blocked here; this analysis succeeds only because a clean
  real table was already on disk from a prior run and its provenance is
  independently DOI-verifiable.
