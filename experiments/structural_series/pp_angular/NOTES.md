# pp_angular — tt-bar spin-density matrix corridor test — 2026-05-21

Third particle-physics shape-observable test. See PREREGISTRATION.md (committed
before any result, commit 0dcff33).

## Data availability assessment (task's first requirement)

**Partial.** HEPData's search and download/REST API are behind a Cloudflare
challenge in this environment (search → JS challenge page; `/download/...` and
`/record/...?format=json` → HTTP 403). Automated programmatic access to HEPData
tables is NOT available here.

However, a clean real table was already on disk from a prior (rate-limited)
run of this task: `cms_fullmatrix_inclusive_mtt.json`. Its provenance was
independently verified via the DataCite DOI API (`api.datacite.org`, which is
NOT Cloudflare-blocked): DOI 10.17182/hepdata.153301.v1/t1 resolves to

  CMS Collaboration, "Measurements of polarization and spin correlation and
  observation of entanglement in top quark pairs using lepton+jets events from
  proton-proton collisions at sqrt(s) = 13 TeV", 2024.
  HEPData record ins2829523 / 153301; reaction P P --> TOP TOPBAR at 13 TeV.

The file's 15 coefficients are exactly the standard tt-bar spin-density-matrix
parametrisation (c, P_{r,n,k}, Pbar_{r,n,k}, C_{rr,nn,kk}, C_{nr,rk,nk}^{+/-})
with stat and syst errors — the "full matrix inclusive from m(tt)" table,
Figure 17. The data is real and DOI-verified. No fabrication.

## Result

The shape observable: the 4x4 tt-bar two-qubit spin-density matrix R is
assembled from the 15 coefficients; its 4 eigenvalues form a probability
distribution on the 4-simplex; rho = Kish correlation of that spectrum.

Central value:
- R is a valid density matrix: Tr R = 1.000000, eigenvalues
  (0.4198, 0.2517, 0.2445, 0.0840), all positive.
- k_eff = 3.263 of 4;  **rho = 0.0753**.
- tr[C] = 0.663 — consistent with CMS's reported strong tt-bar spin
  correlation; -tr[C]-1 = -1.66, table 'c' proxy = 0.938 (different
  normalisation, only a sanity cross-check).

MC error propagation (20000 draws, stat+syst in quadrature, errors treated
independent — full covariance not in the table):
- **rho median 0.0762, 16-84 interval [0.0709, 0.0816], width 0.011.**
- 0/20000 draws produced a negative eigenvalue — R is robustly physical.

SM cross-check: the Powheg+P8 predicted coefficients give rho_SM = 0.0727,
**statistically identical** to the measurement (diff 0.0026, well inside the
0.011 MC width). The observable carries nothing the SM Lagrangian did not
already fix — exactly as PREREGISTRATION section 0 anticipated.

## Verdict — NULL (pole pile-up, chaos pole)

rho = 0.076 sits decisively BELOW the 0.12 chaos boundary and far below the
pre-registered A3+ corridor band [0.17, 0.35]. The MC interval [0.071, 0.082]
does not come near the corridor. Physically: the tt-bar spin-density matrix is
close to maximally mixed (R ~ I/4) — one moderately-elevated eigenvalue ~0.42
on top of three near-equal ~0.25/0.25/0.08. The participation ratio piles at
the chaos pole.

This matches the pp_cp run (CP-violation structure → chaos-pole concentration)
and is consistent with E4 (decay branching fractions → broad NULL). All three
particle-physics shape candidates return NULL.

This is the LEAST-surprising of the three nulls: a spin-density matrix is the
right *kind* of object (a genuine matrix shape observable, scale-invariant
within fixed Tr = 1, eigenvalues basis-independent), but the tt-bar spin state
is explicitly NOT a coordinated rung (PREREG sec 0): a single-shot quantum
state living ~1e-25 s, fixed by the production matrix element, with no
time-extended dynamics dρ/dt and no maintenance work γ·M(t). The framework's
corridor claim attaches to coordinated rungs with maintained dynamics; this
substrate has none, and the data reflects that — it sits at a pole, not in a
corridor.

The naive |coeff|^2 participation ratio of the 15-vector gives rho = 0.60 (a
rigidity-side number), but that is NOT a matrix shape observable — it depends
on the arbitrary coefficient parametrisation and basis choice, and is reported
only as a contrast. The eigenvalue spectrum is the basis-independent object and
it gives 0.076.

## What this closes

The particle-physics shape-observable line of investigation is now NULL across
all three candidates tested in-environment (E4 branching fractions, pp_cp CP
asymmetries, pp_angular spin-density matrix). The honest conclusion: the
corridor does not recur at the particle-physics rung under any of the three
shape constructions. This is consistent with the framework's own scoping — the
corridor is claimed for coordinated rungs with maintenance dynamics, and
particle observables (set by the Standard Model Lagrangian, single-shot, no
γ·M(t)) are not such rungs. A null here is the framework-consistent outcome,
not a falsification of Claim 4 — Claim 4 ranges over *coordinated* rungs, and
none of these three substrates qualifies.
