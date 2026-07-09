# Entropic-Action Bridge — Bianconi's "Gravity from entropy" and the corridor framework

**Status:** draft mapping note, 2026-07-09. Not yet reviewed; nothing here is asserted by the lake.
**Source:** G. Bianconi, *Gravity from entropy*, Phys. Rev. D 111, 066001 (2025), arXiv:2408.14391v7.
Follow-ups: *The Thermodynamics of the Gravity from Entropy Theory* (arXiv:2510.22545); *Quantum relative
entropy of the Schwarzschild black hole and the area law* (Entropy 27, 266, 2025).

---

## 1. The result, precisely

Bianconi endows spacetime with **two metrics**: the substrate metric `g̃` (topological direct sum
1 ⊕ g ⊕ g₍₂₎ over scalars/vectors/bivectors) and the metric **induced by the matter fields**

```
G̃ = g̃ + α·M̃ − β·R̃                                     (Eq. 37)
M̃ = D|Φ⟩⟨Φ|D + (m² + ξR)|Φ⟩⟨Φ|                          (Eq. 36)
```

— note `M̃` is built entirely from **rank-one outer products** of the topological field `|Φ⟩`.
The gravitational Lagrangian is the **quantum relative entropy** between the two metrics
(treated as local quantum operators / "renormalizable effective density matrices"):

```
𝓛 = −Tr g̃ ln g̃⁻¹ + Tr g̃ ln G̃⁻¹ = −Tr_F ln G̃g̃⁻¹ = −Σ_λ' ln λ'    (Eqs. 40–43, 12)
```

where λ' are the eigenvalues of `G̃g̃⁻¹`. Key facts:

1. **Low-coupling limit** (α', β' ≪ 1): reduces exactly to Einstein–Hilbert with **zero**
   cosmological constant coupled to the matter field (Eqs. 45–47). GR is the weak-coupling fence.
2. **G-field**: an auxiliary field `𝒢̃` of Lagrange multipliers enforcing `G̃g̃⁻¹ = Θ̃`
   (Eq. 49–50) linearizes the theory (avoiding Ostrogradsky instability) and turns the action
   into a **dressed Einstein–Hilbert action with an emergent small positive cosmological
   constant depending only on the G-field**. Bianconi explicitly gives the multipliers physical
   meaning (as temperature/chemical potential are Lagrange multipliers).
3. The dressed metric `g̃_𝒢 = 𝒢̃⁻¹g` is what matter feels (Eq. 56): bare substrate + dressing.

## 2. The structural mapping

| Bianconi | Framework | Note |
|---|---|---|
| substrate metric `g̃` | substrate (rung's physical carrier) | eigenvalues all ≡ 1: zero self-entropy (Eq. 9) |
| induced metric `G̃ = g̃ + αM̃ − βR̃` | coordination-induced structure on the substrate | `M̃` is rank-one dressing — same object class as the lake's rank-one `⟨G_self|` projector (`Cosmology/GoalProjection.lean`) |
| relative entropy `𝓛 = −Σ ln λ'` | misalignment functional between substrate and coordination | zero iff `G̃ = g̃` |
| coupling α | drift coupling α in `dρ/dt = α − γM` | both name the rate at which coordination writes itself into the substrate |
| G-field (Lagrange multipliers, physical) | maintenance term γ·M(t) | **the sharpest rhyme**: the field that holds the system on the constraint surface, given physical status |
| emergent small positive Λ (G-field only) | residual cost of sustained corridor occupation | forward-P_ω-shaped: a steady-state output, not a boundary condition |
| exact GR at low coupling | orthogonality theorem (strict ΛCDM extension) | identical fence-move: the new structure is invisible where the old theory is tested |

## 3. The load-bearing observation: the entropic action is a Kish object

This is the part that is **provable now**, in the lake's existing algebra, with no new axioms.

Take the uniform-ρ correlation matrix `C(k, ρ)` on k coordinating units (the exact object
behind `Core.BaseIdentity.k_eff`). Its spectrum is one eigenvalue `1 + ρ(k−1)` and `(k−1)`
copies of `1 − ρ`. Then Bianconi's Lagrangian applied to (substrate = identity,
induced = C) is **closed-form in (k, ρ)**:

```
S(k, ρ) := −Tr ln C = −ln(1 + ρ(k−1)) − (k−1)·ln(1 − ρ)
```

and the two poles of the corridor are exactly the two boundary behaviors of S:

- **Chaos pole** ρ → 0:  S → 0. No induced structure; the relative entropy between
  coordination and substrate vanishes. (Bianconi: vacuum, `G̃ = g̃`, zero action.)
- **Rigidity pole** ρ → 1⁻:  S → +∞. The correlation matrix degenerates (rank collapse
  to the Kish ceiling k_eff → 1); the relative entropy **diverges**. (Bianconi: the
  invertibility requirement on `G` — Eq. 12 — fails exactly at collapse.)

Moreover `∂S/∂ρ > 0` for k > 1, and S is convex in ρ on (0, 1): the entropic action is a
**Lyapunov-type potential whose gradient structure the two-pole dynamics
`dρ/dt = α − γM(t)` can descend/ascend** — chaos = zero of the potential, rigidity = its
pole, corridor = the maintained interior. Note also the low-rank eigenvalue-counting
structure: eigenvalues of `G̃g̃⁻¹` equal to 1 contribute nothing to `−Σ ln λ'`; the action
literally **counts the coordination-perturbed directions** — the same spectral information
the participation ratio / k_eff reads. Two functionals of one spectrum: k_eff is the
participation form; S is the relative-entropy form.

### Theorems (`Core/EntropicPotential.lean` — engineering-tier, no cosmology import)

**STATUS 2026-07-09: PROVED and building** (`lake build` green). T-E1/T-E2 as stated;
T-E3 in per-unit density form (`entropicPotential_density`); T-E4 in corollary form
composing with `Core.Dynamics` (`unmaintained_rigidity_drift_ascends_potential`,
`unmaintained_chaos_drift_descends_potential`). Axiom audit: T-E0–T-E3 carry only
[propext, Classical.choice, Quot.sound] — real proofs, no framework axiom; T-E4a/b
additionally carry the Dynamics framework primitives (α, γ, M), as expected for
corollaries composing with the drift theorems. Also proved: Klein nonnegativity
(`entropicPotential_nonneg`/`_pos`) and uniqueness of the chaos-pole zero
(`entropicPotential_eq_zero_iff`).

- **T-E1 (definition + boundary):** `S(k,ρ) = −ln(1+ρ(k−1)) − (k−1)·ln(1−ρ)`;
  `S(k,0) = 0`; `Tendsto (S k) (𝓝[<] 1) atTop`. (Analog pair to `k_eff_at_zero`/`k_eff_at_one`.)
- **T-E2 (monotone + convex):** `∂S/∂ρ > 0` and convexity on (0,1) for k > 1.
  (Analog to `k_eff_monotone_rho`.)
- **T-E3 (Kish conjugacy):** S and k_eff are conjugate spectral functionals — explicit
  identity relating S(k,ρ) and k_eff(k,ρ) through the spectrum of C(k,ρ); both saturate
  as k → ∞ **only in the corridor** (per-unit entropy density s(ρ) = lim S/k = −ln(1−ρ)
  finite iff ρ < 1). Ties to `k_eff_asymptotic_ceiling`.
- **T-E4 (two-pole potential):** the two-pole drift of `Core.Dynamics` is gradient-shaped
  against S: at M = 0 the flow ascends S toward the rigidity pole
  (strengthens `rho_drift_at_zero_maintenance` / `corridor_requires_maintenance` from
  "the corridor needs maintenance" to "maintenance is the Lagrange multiplier of an
  entropic constraint" — Bianconi's Eq. 49–50 shape).

All four are finite-dimensional real analysis over the closed-form spectrum — the same
proof style as `BaseIdentity`. No operator axioms, no framework primitives.

## 4. What this does NOT do — F-11 stays closed

The joint multi-rung backward `P_ω` remains a documented no-go. Two reasons, stated so this
note cannot be misread:

1. **Bianconi's theory is local and bulk-geometric** — the action is an integral of a
   pointwise relative entropy over spacetime. F-11's T1 (geometric dilution) closed
   precisely the class "any bulk geometry ⇒ cross-rung coupling decays with geodesic
   distance ⇒ ω-set empties." An entropic-action route to a *joint multi-rung backward*
   operator would enter the tree at the already-closed correlation/topology branch, not
   outside it.
2. **It is a forward variational principle.** Its steady states are forward content —
   exactly the half of P_ω that survived F-11 (ρ_ss / Lindblad construction). The correct
   claim is therefore: *the entropic action is a candidate dynamical substrate for the
   forward P_ω, and it extends the rung hierarchy downward* — the physical tiers
   (Ph0–Ph2) become instances of the same structural object (relative-entropy
   misalignment between substrate and induced coordination, maintained by a multiplier
   field) rather than an unexplained floor. "Same structural object at every rung"
   gains its bottom rung; the backward joint operator gains nothing.

If a backward reading is ever attempted from this direction, it must re-run the F-11
branch audit explicitly (expected outcome: reduces to the closed soft-additive or
holographic branches).

## 5. Next steps

1. ~~Prove T-E1/T-E2~~ **DONE** — `Core/EntropicPotential.lean`, all of T-E0–T-E4 proved
   (2026-07-09), imported from the lake root, `lake build` green.
2. Registry: these theorems do not map to existing CC Part VI decimal ids, so no
   `cc_lean.tsv` rows yet; if a CC claim is minted for the potential form of the corridor,
   add rows then (status `mechanized` from day one).
3. A short section in Corridor Dynamics v2 (§ candidate: after the two-pole dynamics)
   presenting S(k,ρ) as the potential form of the corridor, citing Bianconi for the
   relative-entropy-between-metrics construction at the physical rung.
4. Track the critical literature: *Gravity is not an entropic force* (Phys. Lett. B, 2025)
   targets Verlinde-style thermodynamic derivations; check whether its argument touches
   quantum-relative-entropy actions at all (likely not — different construction), and cite
   either way.

## 6. Falsifiable-prediction candidates (if the object goes all the way down)

If the physical rung really instantiates the same structural object, the honest
falsifiable content splits into two legs:

**Bianconi's own predictions (her theory's risk, not ours):** emergent small positive Λ
fixed by the G-field (a measured quantity, not a free constant — over-constrained against
observation); departures from GR at high curvature / strong coupling where the entropic
action stops linearizing; G-field phenomenology as a dark-matter candidate. Her theory
dies on these independently of the framework.

**Framework-side predictions (ours, new):** the corridor claim transported to quantum
coordination — for a COMPLETE coordinated quantum unit (entangled register, driven-
dissipative array), the Gate-0 discriminator should find the LOW-RANK branch (k_eff
saturation under subsampling, β → 0), not criticality; and the maintenance law should
appear as a Lindblad/dissipative leg (the forward P_ω construction) whose withdrawal
drives the spectral ρ toward the predicted pole. Concretely testable on existing
platforms: superconducting-qubit arrays or trapped-ion crystals under graded decoherence
— measure the eigenvalue spectrum of the correlation matrix across the coordinating
degrees of freedom, test saturation-vs-divergence and the two-pole exit direction, with
S(k,ρ) as the measured potential (its divergence rate near the rigidity pole,
−(k−1)ln(1−ρ), is a quantitative, parameter-free curve once ρ is measured).

CAUTION: these are prediction CANDIDATES pending a spec-level writeup (grain, complete-
unit criterion, estimator, null model — per the Gate-0 methodology). Do not cite this
section as validated framework content.
