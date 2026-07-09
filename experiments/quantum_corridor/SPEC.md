# Quantum corridor — transporting the Gate-0 discriminator to quantum coordination substrates

**Status: spec, not yet run.** A falsifiable-prediction writeup for the prediction
CANDIDATES in `papers/notes/entropic_action_bridge.md` §6. Nothing here is asserted by
the lake; this document exists so that section cannot be cited as validated content
until a run passes the discipline below (grain fixed before spectrum, estimator
calibrated at the substrate's (N,T), null models declared in advance).

## 0. Read first — what this test is and is not

This is the **classical-outcome-correlation** reading of a quantum register: we build a
correlation matrix from *measured outcomes* (shots, weak-measurement records, or
tomographically-reconstructed observables) and run the criticality-vs-low-rank
discriminator (`experiments/keff_saturation/`, `spectral_test.py` estimator) on its
eigenspectrum. It does **not** measure entanglement structure per se — a correlation
matrix of measured outcomes is basis-dependent and blind to coherence that produces no
outcome correlation in the chosen basis (§7). Two functionals of one spectrum are read:
the participation-ratio subsampling exponent β (saturation vs power-law) and, as the
measured potential, S(k,ρ) = −ln(1+ρ(k−1)) − (k−1)ln(1−ρ) near the rigidity pole.

This spec does **NOT** touch the F-11 no-go (joint multi-rung backward P_ω). It is a
forward, local, spectral test on a single coordinating unit; see §7.4.

## 1. The claim under test (precisely)

For a **complete coordinated quantum unit** U (defined in §3):

- **C1 (branch):** the outcome-correlation spectrum of U falls on the **low-rank /
  bounded** branch — under subsampling of the coordinating degrees of freedom, k_eff
  saturates (β → 0, effective rank small and size-independent), **not** the criticality
  branch (power-law spectrum, β ∈ [0.3,0.8], k_eff growing like a power of N).
- **C2 (pole exit):** under **graded maintenance withdrawal** (a decoherence /
  dissipation ramp, §4.3) ρ exits the corridor toward a **single, pre-declared** pole,
  and the direction is fixed a priori per platform, not read off after the fact.
- **C3 (parameter-free curve):** as ρ → the rigidity pole, the measured potential
  follows S(k,ρ) ≈ −(k−1)ln(1−ρ) — a curve with **no free parameters** once ρ and k are
  measured (the per-unit density leg of T-E3). Its divergence *rate* is the quantitative
  content, not just the sign.

C1 is the primary test and is decidable on a single well-characterized dataset. C2/C3
require a maintenance-ramp series and are the sharper, riskier legs.

## 2. Grain — what counts as the coordinating degrees of freedom

The correlation matrix is over UNITS (rows) × OBSERVATIONS (columns). "What is a unit"
is the load-bearing choice and must be fixed before any spectrum is computed.

**Operationalization A — one qubit = one unit.** Units are the N physical qubits; each
unit's per-observation value is the outcome of a fixed single-qubit observable
(e.g. ⟨Z_i⟩ estimate per window, or the ±1 shot outcome). Correlation matrix
C_ij = corr(o_i, o_j) over shots/windows.
- *Pitfall (basis):* Z-basis outcome correlations miss X/Y coordination entirely. A
  Bell/GHZ register reads ρ≈1 in Z but a graph state can read ρ≈0 in Z while being
  highly coordinated in the stabilizer basis. **The basis must be declared and the test
  re-run in ≥2 mutually-unbiased bases;** a claim that survives only one basis is grain-
  fragile and reported as such.
- *Pitfall (marginals):* GHZ has random single-qubit marginals but perfect pairwise Z
  correlation → correlation-matrix rank 1 → reads as the **rigidity pole**. This is not
  obviously an artifact (GHZ *is* fragile: one error kills the state — consistent with
  rigidity=fragility), but it means "coherent and coordinated" ≠ "corridor" under this
  grain. State the expected classification per state class in advance (§5).

**Operationalization B — one observable-mode = one unit.** Units are a fixed operator
basis on the register (k-local Pauli strings up to weight w, or the tomographic
observable set); values are their per-window expectation estimates. This reads
coordination the single-qubit grain is blind to, at the cost of an operator count that
grows combinatorially and a covariance that inherits tomographic estimation noise.
- *Pitfall (grain inflation):* including too many high-weight operators manufactures
  apparent dimension; fix the operator set (weight cutoff w) structurally, before the
  spectrum, exactly as region-partitions are fixed for fMRI.
- *Pitfall (estimation noise):* tomographic reconstruction adds a noise floor that
  inflates PR; must be debiased against a shot-matched surrogate (§4.4).

**Default:** run A first (cheapest, closest to raw data), in ≥2 MUBs; escalate to B only
where A is basis-ambiguous. Report both grains when they disagree — a disagreement is
itself the result (cf. mouse-V1: level vs saturation disagreed, and saturation was the
intrinsic read).

## 3. Complete-unit criterion for a quantum register

The Gate-0 discipline: a subsample's k_eff is **not** the unit's k_eff (mouse-V1,
cosmology were excluded outcome-independently as wrong grain). For a quantum register the
complete unit is a **bounded, functionally-closed coordinating set of qubits** —
concretely, one of:

- the **full register** participating in a single prepared/stabilized state (all N
  qubits of a GHZ/cluster/variational state, not a chosen sub-block);
- a **complete engineered-dissipation cell** (all sites a Lindblad stabilizer acts on);
- the **complete ion crystal** in one trap (all ions sharing the collective phonon bus).

Why a subsample fails: qubits within a register coordinate through a **shared bus**
(common phonon modes, a shared resonator, engineered dissipation) — the quantum analog of
the GPU's shared memory-controller / power-delivery common cause (F4). Reading k_eff on a
sub-block measures the sub-block's coupling to that shared cause, not the unit's ceiling,
and can read high-dimensional for grain reasons alone. **Completeness is structural and
pre-spectral:** declare the full participating qubit set from the preparation circuit /
Hamiltonian before computing anything. A non-saturating read on an admittedly-incomplete
register is **grain-inconclusive, not a falsification** (same status as the cosmology
subsample).

## 4. Estimator

Reuse the validated core in `experiments/keff_saturation/spectral_test.py` unchanged
where possible; only the matrix-construction front-end is new.

**4.1 What replaces ρ.** Operationally ρ is the **mean off-diagonal of the outcome
correlation matrix** C (the direct corridor variable, as in adversarial_neff §"The
measurements"). k_eff is read two ways that must agree: participation ratio
PR = (Σλ)²/Σλ² of C's spectrum, and the Kish form 1/ρ̄. The rigidity pole is ρ̄ → 1
(rank collapse, k_eff → 1); the chaos pole is ρ̄ → 0 (C → I, k_eff → N).

**4.2 Correlation matrix from repeated shots (Operationalization A).**
- Prepare U, measure all qubits in basis B, record the N-bit shot. Over S shots build
  C_ij = corr over shots of outcomes (o_i, o_j). UNITS N = #qubits, OBSERVATIONS T = S
  (require S ≫ N for a well-conditioned C; T > N throughout, as in the cosmo build).
- β: subsample the qubits at sizes N′ ∈ {…}, draw ndraw random qubit subsets per size,
  fit β = dlog(PR)/dlog(N′) on the upper range (identical to `subsample_pr` +
  `np.polyfit`). β → 0 saturation (C1 low-rank); 0.3–0.8 power-law (criticality).
- **From weak continuous measurement (alternative):** a single-shot weak-measurement
  record gives each qubit an outcome time-series; UNITS = qubits, OBSERVATIONS = time
  windows. This trades ensemble averaging for a within-trajectory correlation and, unlike
  projective shots, also enables the detailed-balance (maintenance) axis (§4.5) — the
  time-ordering is intact.

**4.3 Maintenance-withdrawal ramp (C2/C3).** A monotone knob that removes the active
stabilizing drive/dissipation ("γM" in dρ/dt = α − γM):
- idle-delay ramp: insert increasing wait time τ before readout (T1/T2 relaxation);
- drive-amplitude ramp on a driven-dissipative array (turn down the stabilizing pump);
- added-dephasing ramp (inject calibrated single-qubit noise).
At each ramp step build C, record (ρ̄, PR, k_eff, S). **The predicted exit pole is
declared per platform before the ramp is run** (§5, C2). S is the measured potential; fit
its approach to the pole against the parameter-free −(k−1)ln(1−ρ̄) (C3).

**4.4 Calibration (the defensibility crux — same as every prior substrate).** Push
synthetic controls through the *identical* front-end at the real (N,T): injected low-rank
(r=3) → expect β≈0; power-law α=1.0 → β≈0.25; α=0.6 → β≈0.65; shot-noise-only (random
independent bits at the real shot count) → β≈1, eff-rank 0. Only if β separates the
hypotheses at this (N,T) is the real verdict admissible. Tomographic/estimation noise
(Operationalization B) is debiased against a shot-matched independent surrogate exactly as
`phase_randomize` debiases here.

**4.5 Second axis (bound vs coordinating), if trajectory data exists.** Reuse
`entropy_production.py` (transition entropy production, D_KL(forward‖reverse) vs a
detailed-balance surrogate) on weak-measurement mode trajectories. A *coordinating* unit
(actively maintained, driven-dissipative NESS) should **break detailed balance** (z ≫ null
≈1.5, cf. macaque motor cortex z=8.8); a merely *bound* unit (conservative closed
evolution) is time-reversible. Needs T ≫ n_states — projective shots alone cannot do this
axis.

## 5. Null models — what kills the claim

Declared in advance; any one falsifies for the tested unit (not "grain-inconclusive"
unless the unit is admittedly incomplete):

| # | Falsifier | Reads as |
|---|---|---|
| N1 | A **complete** unit's spectrum is power-law (β ∈ [0.3,0.8], k_eff grows with N′, smooth power-law decay not spikes-over-bulk) in **all** declared bases | C1 fails: criticality on a complete quantum unit |
| N2 | Maintenance ramp drives ρ̄ toward the **wrong** (non-declared) pole, or does not move it monotonically | C2 fails: pole-exit direction wrong |
| N3 | Near the rigidity pole, measured S(k,ρ̄) departs from −(k−1)ln(1−ρ̄) beyond the calibrated error band (wrong divergence rate, not just noise) | C3 fails: not the predicted potential |
| N4 | β verdict flips between the two MUBs and no principled basis is declared | grain-fragile: report as inconclusive, not a pass |
| N5 | Calibration synthetics do **not** separate at the real (N,T) | estimator underpowered here; no verdict admissible |

Pre-declared state-class expectations (Operationalization A, Z-basis + one MUB), so the
test can be wrong: product state → **chaos** (ρ̄≈0, k_eff≈N); GHZ → **rigidity** (ρ̄≈1,
k_eff≈1); random-circuit / cluster / typical variational state → **corridor** (bounded
k_eff, β≈0). If a random-circuit register reads criticality, or a GHZ register reads
corridor, C1's mapping is wrong.

## 6. Candidate platforms and data

Mark every dataset URL "**to verify**" — cited from model knowledge, not confirmed live.

- **Superconducting-qubit arrays (primary; public data most likely).**
  - Google Quantum AI released **Sycamore cross-entropy-benchmarking bitstring datasets**
    (2019 random-circuit sampling) on Dryad — millions of full-register shots, exactly the
    UNITS=qubits × OBSERVATIONS=shots matrix §4.2 wants. doi/URL *to verify*
    (Dryad "Quantum supremacy … Sycamore"; Arute et al., *Nature* 574, 505 (2019)).
    Random-circuit states → predicted **corridor** (§5) → a clean C1 test.
  - **ReCirq** (`github.com/quantumlib/ReCirq`) ships experimental shot data for several
    Google papers (Fermi-Hubbard, OTOC, QAOA) — some with graded-coherence sweeps usable
    for C2. *to verify* which include idle/decoherence ramps.
  - **IBM Quantum** free-tier backends (`qiskit`, `qiskit-experiments`): anyone can
    reproduce — prepare N-qubit states, collect shots, run tomography and RB. This is the
    **easily-reproducible experiment** fallback if no ramp dataset is public. Basis sweeps
    (MUBs) and idle-delay ramps are native.
- **Trapped-ion crystals.**
  - Monroe-group many-body datasets (e.g. **MBL / DTC chains**, Zhang et al. *Nature* 543
    (2017); time-crystal Kyprianidis/Randall) — full-register single-shot readout; complete
    unit = whole chain sharing the phonon bus. Public data *to verify* (some on Zenodo).
  - Penning-trap 2D crystals (Britton/Bohnet, *Science* 352 (2016)) — hundreds of ions,
    engineered spin-spin coupling; large-N for the subsampling β range. *to verify*.
- **Driven-dissipative photonic / circuit-QED arrays.**
  - Best conceptual fit for C2/C3: the stabilizing drive **is** the maintenance term; turn
    it down and the NESS relaxes. Fitzpatrick et al. (Houck), *PRX* 7 (2017) Kerr-cavity
    array; Ma et al. (dissipatively stabilized Mott). Raw correlation data *to verify* —
    may need reproduction rather than a download.

**Recommended first run:** Sycamore XEB bitstrings (public, huge T, complete register) for
C1; IBM free-tier reproduction for the MUB sweep and the idle-delay ramp (C2/C3). This
covers "at least one publicly available dataset" and "easily reproducible experiment."

## 7. Honest scope

**7.1 Measurement backaction.** Projective shots destroy the state; each shot's C-column
comes from an independently re-prepared register — so C measures *ensemble* outcome
correlation, and preparation drift across shots is a confound (bound it with a
re-preparation-interleaved null). Weak continuous measurement keeps one trajectory but
injects backaction that itself correlates qubits — a genuine confound for §4.5; calibrate
the DB estimator against a measurement-only (no-coordination) trajectory.

**7.2 Classical-correlation reading, stated plainly.** C is a matrix of **measured-outcome
correlations**, not an entanglement measure. It is basis-dependent and can read ρ̄≈0 on a
maximally-entangled state in an unlucky basis (§2). We therefore do **not** claim to test
"entanglement corridor"; we test the corridor structure of the *measured coordination* a
register exhibits in declared bases. That is a narrower, honest claim, and the MUB
requirement (N4) is what keeps it from being basis-cherry-picked.

**7.3 GHZ = rigidity is a feature, not a bug — but flag it.** The single-qubit grain maps
GHZ to the rigidity pole (k_eff→1). This is consistent with corridor theory (GHZ is
maximally fragile), but a reviewer may read it as the grain being too coarse. It is called
out as a **weak point** (§9), because "coherent coordinated state classified as collapsed"
is exactly the kind of result whose interpretation is theory-laden.

**7.4 F-11 untouched.** This is a forward, local, single-unit spectral test — the ρ_ss /
Lindblad (forward P_ω) half that survived F-11. It builds **no** joint multi-rung backward
operator and makes no cross-rung claim. Per `entropic_action_bridge.md` §4, any backward
reading from this direction must re-run the F-11 branch audit explicitly; this spec does
not attempt one.

## 8. Pass / fail

| Outcome | Condition |
|---|---|
| **PASS (C1)** | Complete unit: β→0 (95% CI below the calibration criticality band), eff-rank small & size-independent, spikes-over-bulk spectrum, in ≥2 MUBs. Predicted state-class mapping (§5) holds. |
| **PASS (C2)** | Maintenance ramp moves ρ̄ monotonically toward the **pre-declared** pole. |
| **PASS (C3)** | S(k,ρ̄) tracks −(k−1)ln(1−ρ̄) near the rigidity pole within the calibrated band. |
| **FAIL** | Any of N1–N3 on a complete unit; i.e. criticality on a complete register, wrong-direction pole exit, or wrong S divergence rate. |
| **INCONCLUSIVE** | N4 (basis-fragile) or N5 (estimator underpowered at (N,T)); or unit admittedly incomplete (grain, like cosmology). |

Report a documented FAIL as fully as a PASS — a complete quantum unit that reads
criticality would be the first substrate to break the low-rank branch of the corridor, and
that is the most informative outcome available here.
