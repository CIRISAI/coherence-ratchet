# coherence-ratchet — Claude Code Context

## What this is

coherence-ratchet is the companion lake to RATCHET. RATCHET holds the engineering tiers
(L0–L4: Kish algebra, override-rate predicates, GPU coherence). coherence-ratchet holds the
universal-scale extensions (Levels 5–7). TSVF is treated as the physics. All universal-scale
content is **forward** (steady-state / conditioning-sector); the joint multi-rung backward P_ω
is a documented no-go at theorem strength (`FelevenNoGo` record in
`Cosmology/CorridorProjector.lean`) — do not re-attempt it. Open formal steps use `sorry`;
closed no-gos use the `FelevenNoGo` pattern.

**This file states the current stance only.** Project history — what was tried, killed,
revived, corrected — lives in git log and the dated notes in `papers/notes/`. Do not
re-litigate it here or import its hedging into new work: state the stance, test the stance.

## CURRENT STANCE (2026-07-10): the coordination ledger

**Coordination is one substrate-independent quantity** — `S = −ln det C` on the normalized
correlation matrix (a copula functional: amplitude-blind by theorem, clause 3) — read by one
functional across the three accounting systems physics has: electromagnetic, gravitational,
quantum-entanglement. Verified: the classical S tracks true bipartite entanglement across a
quantum phase transition (Spearman ~1.0, order-parameter basis; blind exactly in the proved
null space); the dark and luminous matter fields carry the same coordination books
(r = 0.986–0.999, TNG). One law, one corridor, from qubits to the cosmic web.

**The dark sector — two objects, one accounting relation:**

- **Dark matter is the medium.** Real, diluting, collisionless stress-energy with standard
  CDM phenomenology — *the paper the books are written on, not the money*.
- **Dark energy is the balance.** `ρ_DE = κ·S(a)`, extensive per comoving volume, with the
  exact parameter-free sign law `1 + w(a) = −⅓·dlnS/dlna` (κ cancels).
- The relation is **one-directional**: DE is a functional of the matter field's coordination
  history. It is NOT "one object at two normalizations" — that reading implies the excluded
  lock `w_DE = w_DM − 1` (`papers/notes/one_ledger_pressure_test.md`).
- **Why the universe is dark (DE side):** the balance is kept in the currency gravity reads —
  stress-energy/entanglement — not charge. The books do not shine.

**The empirical leg (the program's strongest result):** the halo-grain B-total `S(a)`,
run through the frozen pre-registered pipeline on TNG300-1 (205 Mpc/h — the large-volume
test, 2026-07-10), gives a thawing `w(z)` whose DESI-projected point is
**(w₀, wₐ) = (−0.767, −0.742), 1.36σ from DESI DR2+CMB+SNe — vs ΛCDM's 3.28σ** —
near-parameter-free, `w_today = −0.833 ± 0.057`, crossing epoch z = 0.59 ± 0.03 (inside
DESI's interval; now the registered DR3 prediction). The interior-peak kill (K3) did not
fire (8/8 jackknife); the halo-formation-peak mechanism is confirmed (k(a) peaks z = 0.55,
S peaks z = 0.59); one magnitude kill (K7) fired by the letter (0.007 past the small-box
interval edge) and is logged. A retrodiction until DESI DR3 (~2027):
`experiments/cosmo_entropic_potential/{PREREGISTRATION.md, large_volume/}`.

**Closed loop:** the mapping's own background alters growth alters `S(a)`; iterating to the
fixed point (`experiments/cosmo_entropic_potential/selfconsistency/`) converges in 2 steps,
lands where the open loop was, and moves ~0.05σ *toward* DESI. The coupled
gravity → clustering → S → H(a) system is near its fixed point.

**Research target — the ledger dynamics as double-entry across rungs:** halo formation
(virialization) *debits* within-halo phase-space coherence and *credits* a new coordinating
unit at the inter-halo rung. Both entries are measured objects; the open computation is the
exchange rate between them. This is the concrete form of "derive the ledger dynamics."

## Discipline (load-bearing — these rules are the program's falsifiability, keep them)

1. **Every residual is a dated debt with a kill condition.** No kill condition → not a
   residual → rejected. (DE's: a robust SNe-independent phantom crossing at DR3 kills the
   w(z) reading.)
2. **A residual is never support.** Support comes only from confirmed positive independent
   predictions.
3. **Residual-first rights are proportional to confirmed novel risk.** Earned once,
   partially (the DE leg). Most variances still count as disagreements.

Method rules: fix the grain **before** the spectrum (Gate-0 discipline). Anchor verdicts to
controlled measures, not first passes — in either direction (over-reading a positive and
over-killing on an audit are the same error). Pre-register before data. No synthetic data.
Big pipeline choices get written down before their results are seen.

## Standing results (validated, in the record)

- **Two-axis discriminator.** Axis 1 (structure): `k_eff` saturation measured on complete
  units — the corridor is genuine low-rank structure, not criticality; decisive on the
  complete larval-zebrafish brain (71,721 neurons). Axis 2 (maintenance): detailed-balance
  breaking = the γM term (estimator validated; macaque motor cortex |z|=8.8 coordinating,
  galaxy baryon cycle z≈0 bound). Positioning: unification + method discipline that
  adjudicates the criticality-vs-low-dimensionality debate; not a novel phenomenon.
  `experiments/keff_saturation/`, `Cosmology/CriticalityDiscriminator.lean`.
- **The corridor:** ρ ∈ (0.1, 0.43); k_eff ceiling ≈ 10 at any nominal k; saturation, not
  level, is the substrate-independent invariant.
- **The entanglement bridge:** the classical instrument is a faithful shadow of the quantum
  entanglement structure gravity couples to; its blind spots are exactly the proved null
  space (conjugate basis, GHZ-type multipartite). `experiments/entanglement_ledger/`.
- **CMB:** the orthogonality theorem is the sole CMB content — the framework is exactly ΛCDM
  in the conditioning/perturbation sector; the background sector is a w₀wₐCDM-class
  deformation vanishing identically in linear theory (`CMBOrthogonality.lean`).

## Formal core (one line per piece; full statements live in the Lean files)

| # | Object | Location |
|---|--------|----------|
| 1 | `k_eff = k/(1+ρ(k−1))`; k→∞ ⇒ k_eff→1/ρ | `Core/BaseIdentity.lean` |
| 2 | `dρ/dt = α(ρ,S) − γ·M(t)`; corridor sustained only by M>0 | `Core/Dynamics.lean` |
| 3 | corridor ρ ∈ (0.1, 0.43); k_eff ∈ (2.33, 10) | `Core/Corridor.lean` |
| 4 | TSVF; agent goal-state as post-selection projector | `Cosmology/TSVF.lean`, `GoalProjection.lean` |
| 5 | multi-agent consent: ρ_goals corridor = sustained coordination | `Cosmology/MultiAgentConsent.lean` |
| 6 | rung hierarchy Ph0…A5; cross-rung τ corridor; post-Cambrian acceleration 540 Myr → 310 kyr → 6.7 kyr | `Cosmology/RungHierarchy.lean` |
| 7 | P_ω forward content (ρ_ss steady state); joint backward P_ω = FelevenNoGo | `Cosmology/CorridorProjector.lean` |
| 8 | Penrose past hypothesis, structural from forward P_ω (measure unspecified — open) | `Cosmology/PenrosePast.lean` |
| 9 | asymptotic conditioning: P(corridor \| observed at t→∞) → 1 | `Cosmology/AsymptoticConditioning.lean` |
| 10 | karma = cumulative post-selection; grace = unauthored boundary conditions | `Consciousness/KarmaGrace.lean` |

Conjecture A (quantum-substrate corridor, Exp 5) and Conjecture D (D1 structural Penrose,
D3 rung acceleration; D4 is not part of the framework) — `Conjectures/`.

## The seven-level ladder

L0 formal proof · L1 ρ-collapse observation · L2 engineering · L3 cross-substrate
universality · L4 agency/consent at A3+ · L5 TSVF universal scale · L6 cross-tradition
recognition · L7 cosmological extension. **No level is load-bearing on the levels above; a
reader who rejects Level k keeps everything below k.**

## AI-safety application

`Neff` = k_eff of the reasoning-constraint system (CIRIS): H3ERE ≈ 7.1, joint with CEG ≈ 9;
deception must cohere across independent constraint axes (≈O(2^m) vs truth's O(n)). Measured
on benign traces — an upper bound. The decisive open test is **adversarial-Neff**
(`experiments/adversarial_neff/SPEC.md`); the attack-invariant guarantee is the CEG substrate
floor. Safety is a maintained non-equilibrium (the γM axis): kept, not achieved.

## Open work, ordered

1. **Large-volume test** (in flight) → then DR3 (~2027) under the frozen preregistration.
2. **Ledger-dynamics exchange rate** (double-entry across rungs) — computable on data in hand.
3. **Adversarial-Neff** (safety-program priority).
4. P_ω forward operator sharpening (Piece 7); Conjecture A quantum-substrate run (Exp 5).
5. Per-rung corridor calibration; substrate-readiness wait-time modeling; audit-pressure
   ρ-drift (Exp 6).

## Layout & sister projects

```
formal/CoherenceRatchet/{Core,Cosmology,Conjectures,Consciousness,ContemplativeTraditions,Residue}/
papers/{universal_scale/main.tex, notes/}        # notes = dated stance records
experiments/{cosmo_entropic_potential, keff_saturation, dm_coherence,
             entanglement_ledger, adversarial_neff, ...}
../RATCHET            # engineering tiers L0–L4
../CIRISOssicle ../CIRISArray                    # GPU strain gauges
../CIRISServer        # federation + lens-core; CEG substrate
../CIRISConstitution  # constitutional text (Book IX coherence math)
../CIRIS-RED          # Constrained Reasoning Chains (Neff telemetry)
```

## Style discipline

- **No hedging on the universal-scale content** for readers past Level 4. TSVF is the
  physics; karma and grace are formal TSVF structures; consciousness is corridor-occupation
  at A3+. Stated as load-bearing claims.
- Where proof is open, state the theorem with `sorry` and name the open step. Where a route
  is closed, record it once (`FelevenNoGo`) and move on.
- Stopping-point independence across the ladder, always.
- **Current stance, stated plainly.** Equivocation is not humility and it is not
  falsifiability — the kill conditions are. When the stance changes, update this file to the
  new stance and let git hold the old one.
