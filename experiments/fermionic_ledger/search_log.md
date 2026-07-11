# Fermionic coordination ledger — search log

Mode: SOLUTION-ASSUMED SEARCH. Every formulation tried is logged in order with its
grade against S1–S5. Criteria: S1 two-pole, S2 saturation (Kish analog), S3 extensivity,
S4 instrument/bridge, S5 maintenance. A PRINCIPLED, exactly-characterized deformation
(mechanism + closed form) counts as a solution; a missing structure does not.

Conventions and machinery: `fermionic_core.py` (Majorana covariance, nu-spectrum,
functionals, self-tested). Seeds fixed.

---

## Formulation 1 — F2 raw log-det on the covariance:  L_F = -ln det(I - M^T M) = -sum ln(1-nu_j^2)

- **S1 (two-pole): PASS, bosonic-shaped.** Chaos pole L_F=0 at nu=0; rigidity pole
  L_F -> +inf as any nu_j -> 1. Verified on the uniform family (`uniform_family.py`,
  `s1_two_pole`): L_F(s~1) blows up (>13 at s=0.999999, ->inf). This is the *undeformed*
  bosonic divergence — exclusion does NOT cap it because L_F is a raw spectral log-det,
  not an entropy.
- **S3 (extensivity): PASS.** Additive over independent blocks (max err 3.6e-15).
- **Grade so far:** a legitimate "coordination potential" that reproduces the bosonic
  two-pole shape on the fermionic covariance. BUT it is not an information/entropy
  quantity and it double-counts the same mode as it approaches purity. Kept as the
  "log-det twin" of the entropy ledger; the SPLIT between it and F1 is a finding.

## Formulation 2 — F1 fermionic multi-information:  I_F = sum_i S_F(marginal_i) - S_F(joint)

- **S1 (two-pole): PASS, with a PRINCIPLED EXCLUSION DEFORMATION.**
  - Chaos pole: I_F = 0 at s=0 (uncorrelated). Confirmed (<1e-13).
  - Rigidity pole: **CAPPED, not divergent.** On the uniform family the collective mode
    nu0 = s -> 1 freezes (h(nu0)->0), and
        I_F(s=1)  =  k ln2 - (k-1) h(1/(k-1))  ->  ln2 + O(1/k).
    Numerically: cap = 0.7488 (k=10), 0.6982 (k=100), 0.6936 (k=1000), -> ln2=0.69315.
    **Mechanism:** Pauli exclusion bounds the per-pair coherence c <= 1/(2(k-1)); the
    collective coherence nu0 saturates at 1 (one frozen mode), so the multi-information
    cannot diverge. Bosonic S -> +inf; fermionic I_F -> ln2 (one bit).
  - Monotone increasing in s between the poles. Confirmed.
- **S2 (saturation / Kish analog): PASS, closed form derived and sympy-verified.**
  Effective active dimension k_eff = participation ratio of per-mode entropies h(nu_j).
  It does NOT collapse (stays ~k); the SATURATING object is the number of dimensions
  REMOVED by coordination:
        lim_{k->inf} [ k - k_eff(k,s) ]  =  ( 1 - h(s)/ln2 )^2  =: mu(s)^2,
    mu(s) = 1 - h(s)/ln2 in [0,1] the normalized coordination of the collective mode.
    Verified to 5 digits at s=0.3/0.6/0.9/0.999 and confirmed exactly by sympy
    (`(1-h/ln2)^2` matches the k->inf limit symbolically). mu(0)=0 (removes nothing),
    mu(1)=1 (removes exactly ONE dimension). **Kish deformation:** bosons remove
    k - 1/rho -> infinity (condensation collapses dimensionality); fermions remove
    <= 1 per collective mode (exclusion forbids the collapse). For rank-R coordination
    (R collective modes), removed -> sum_r mu(s_r)^2 <= R (extensivity).
- **S3 (extensivity): PASS.** I_F additive over independent blocks (err 3.6e-15).
- **Grade so far (S1,S2,S3): PASS with exclusion deformation.** This is the fermionic
  information ledger. The deformation is the content: exclusion caps both the rigidity
  pole (I_F -> ln2) and the dimensional collapse (removed -> mu^2 <= 1 per mode).

## The SPLIT (finding, not a failure)
Bosonically  S = -ln det C = 2 x multi-information  (T-E5c): the log-det and the
multi-information COINCIDE. Fermionically they SPLIT:
  - F1 (multi-information, entropy-based): rigidity pole CAPPED at ln2 by exclusion.
  - F2 (log-det on covariance): rigidity pole DIVERGES (bosonic shape).
The degeneracy the bosonic ledger enjoys is lifted by fermionic statistics. Which one
the classical instrument S shadows is the S4 question (bridge, next).

---

## Formulation 3 — F3 the instrument route (S4 bridge), `bridge.py`
Classical S = -ln det C of single-site observables vs the fermionic-native
functionals across the Kitaev topological transition (mu=2) and XY criticality.
- **Kitaev: PASS, |Spearman| = 1.0.** Classical S (occupation basis) tracks the
  fermionic multi-information I_reg at Spearman = -1.00 and the entanglement
  entropy S_half at -0.96; the conjugate (X) basis flips sign to +1.00 / +0.96 —
  the SAME basis-blindness discipline as the bosonic entanglement bridge. The two
  F1-family functionals agree (S_half vs I_reg = +0.96); the F2 log-det does NOT
  track the entropy here (-0.28) — the split again.
- **XY-field: WEAK in the naive local basis (|Spearman|~0.31).** Honest negative:
  the XY order parameter is a Jordan-Wigner STRING (nonlocal in fermions), so the
  local single-site instrument is a poor shadow — a grain failure, not a ledger
  failure (the fermionic-internal S_half~I_reg is +0.99). Documented, not hidden.
- **Grade:** the classical instrument is a faithful (rank-1) shadow of the
  fermionic multi-information WHEN the coordination is visible in a local basis
  (Kitaev); it degrades exactly when the order parameter is stringy (XY) — Gate-0
  grain discipline reproduced on fermions.

## Formulation 4 — F1 under free dissipation (S5 maintenance), `maintenance.py`
Lindblad on Gaussian states -> closed covariance ODE; on the uniform family it
reduces EXACTLY to  ds/dt = alpha(s_target) - (alpha+gamma)s  (corridor equation).
- **PASS.** Validated family reduction against the full-matrix ODE (err 4e-12).
  D1 dephasing alone -> CHAOS pole (I_F -> 0): free dissipation selects chaos.
  D2 maintenance on -> NESS at s* = alpha s_t/(alpha+gamma) in the corridor
  interior (closed form matches numeric to 1e-4). D3 over-drive -> RIGIDITY pole,
  I_F CAPPED at ~ln2 (0.690 vs cap 0.698), NO divergence — the exclusion cap
  reappears dynamically. This is the drho/dt = alpha - gamma M structure, with
  the fermionic twist that the rigidity attractor is a finite frozen mode.

## VALIDATION (out-of-search set), `validation.py`
Untouched until the functional was fixed. Free-fermion route validated vs ED
covariance (err 2e-14).
- **V1 SSH chain (Ncells=40): PASS.** I_F extensive and bounded; per-mode
  I_F max = 0.6923 = ln2 to 3 digits — the exclusion cap (ln2 per collective
  mode) confirmed extensively on an out-of-search system. S_half vs I_reg |rank|=1;
  local number-instrument tracks at |0.485| (partial — SSH coordination is in the
  coherence, second-order in local number correlations).
- **V2 2D free-fermion patch (6x6): PASS.** Structure survives in 2D; classical
  number-instrument tracks I_A at Spearman 0.905; S_A vs I_A 0.913; I_F bounded.
- **V3 Hubbard ED (Nsites=4, NON-GAUSSIAN): PASS with documented blindness.**
  At U=0 the Gaussian functional = truth exactly. As U grows the one-body Gaussian
  I_F INVERTS relative to the true multi-information (rank -1.0) and the gap
  S_F(cov) - S_vN grows to 1.97: coordination migrates into the higher-order
  (Mott/spin) sector the one-body covariance cannot see. This is the fermionic
  clause-3 (the bosonic GHZ/conjugate-basis blindness): the covariance ledger reads
  one-body coordination faithfully and is blind (inverts) on genuinely many-body
  coordination. S_F(cov) >= S_vN always (max-entropy Gaussian bound).

## VERDICT
**FOUND** (with a principled, exactly-characterized exclusion deformation).
Functional: **F1 fermionic multi-information** I_F = sum_i S_F(marginal_i) - S_F(joint),
S_F = sum_j h(nu_j). It passes S1-S5. The deformations (the real content):
  (1) EXCLUSION CAPS THE RIGIDITY POLE: bosonic S -> +inf; fermionic I_F -> ln2
      per collective mode (closed form I_F(k,1) = k ln2 - (k-1)h(1/(k-1)) -> ln2).
  (2) EXCLUSION CAPS DIMENSIONAL COLLAPSE (Kish deformation): bosons remove
      k - 1/rho -> inf effective dims; fermions remove (1-h(s)/ln2)^2 <= 1 per
      collective mode. Closed form sympy-verified.
  (3) THE BOSONIC LOG-DET/MULTI-INFO DEGENERACY SPLITS: F2 (-ln det(I-M^2)) keeps
      the divergent bosonic pole; F1 (entropy) is capped. Distinct functionals.
N formulations tried: 4 (F2 log-det; F1 multi-info; F3 instrument bridge; F1 under
dissipation). Found on F1 (formulation 2). Validated out-of-search on SSH, 2D
patch, and non-Gaussian Hubbard ED.

---

# SUMMARY / SIDEWAYS PASS (folded in here; harness blocks a separate SUMMARY.md)

## The functional (exactly)
Fermionic multi-information  I_F = sum_i S_F(marginal_i) - S_F(joint),  S_F = sum_j h(nu_j),
h(nu) = binEntropy((1-nu)/2). Direct fermionic analog of the bosonic Gaussian multi-information
(bosonic S = -ln det C = 2x it). Passes S1-S5 with an exclusion deformation that IS the content.

## S1-S5 (one line each)
- S1 two-pole: chaos pole I_F=0; rigidity pole CAPPED, closed form I_F(k,1)=k ln2-(k-1)h(1/(k-1)) -> ln2.
- S2 saturation: dims removed -> (1-h(s)/ln2)^2 <= 1 per collective mode (sympy-verified). Kish deformation.
- S3 extensivity: additive over independent blocks (err 3.6e-15).
- S4 bridge: Kitaev |Spearman|=1.0 (classical S vs I_F); grain-limited on stringy XY (honest).
- S5 maintenance: dephasing->chaos; alpha->NESS in corridor; over-drive->capped rigidity.

## The deformations (real content, full weight)
1. Exclusion caps the rigidity pole: bosonic S->+inf; fermionic I_F->ln2/collective mode (T-FL2, proved).
2. Exclusion caps dimensional collapse: bosons remove k-1/rho->inf dims; fermions remove <=1/mode.
3. Bosonic log-det/multi-info degeneracy SPLITS: F2 -ln det(I-M^2) diverges; F1 (entropy) capped.
4. Fermionic clause-3: on non-Gaussian Hubbard the one-body ledger inverts (coordination -> Mott
   higher-order sector it can't see); gap S_F(cov)-S_vN grows to 1.97. Exact at U=0.

## Search-mode honesty
4 formulations tried; found on F1 (formulation 2); validated OUT OF SEARCH on SSH (per-mode cap
= 0.6923 = ln2), 2D patch (bridge 0.905), non-Gaussian Hubbard ED (blindness documented).

## SIDEWAYS PASS (against CLAUDE.md CURRENT STANCE)
TOP: Exclusion is an ATTACK-INVARIANT FLOOR on k_eff -> a design principle for the adversarial-Neff
gap. The safety worry is an optimizer driving constraint rho->1 (k_eff->1, rigidity). Under exclusion
that collapse is STRUCTURALLY FORBIDDEN (removes <=1 dim/mode). Design claim: make the orthogonal CEG
attestation constraints mutually EXCLUSIVE (anti-bunching), not merely independent -> the rigidity
collapse an adversary exploits is unavailable. Bosonic-class constraints have no such floor; fermionic
do. Falsifiable: exclusion-structured constraints should resist adversarial rho->1 that condensable
ones don't.
2ND: substrate mechanism for the 2x2's open high-rank cells. Exclusion/anti-correlation keeps k_eff~k
(no saturation) even under strong coordination -> a system whose DOF anti-bunch is high-rank BY
STATISTICS, not criticality/wrong-grain. The substrates that DO saturate (neural/market/GPU/galaxy)
are all condensable (bosonic) class.
3RD: sharpens "three ledgers, one corridor" -> the corridor spans bosonic AND fermionic statistics,
with the difference between them (which pole is reachable) in closed form. TFIM was already free
Majoranas; now native.

## Fences
Exact but small (ED N<=14; free-fermion route validated vs ED err 2e-14, scaled to N=80 SSH / 36 2D;
Hubbard Nsites=4). Uniform family = single-collective-mode; rank-R via extensivity. Saturation k->inf
limit numeric+sympy; Lean proves finite-k bounds, states asymptotic as named open step.
