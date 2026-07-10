# Gravity and dark matter under the Ledger Law reading

**STATUS: CONJECTURE-to-SPECULATION grade. Not lake content. Not asserted by the framework.**
A reading exercise with falsifiability-today as the goal. Draft 2026-07-10.

**Grading key (repo discipline):** **[theorem]** = discharged in Lean at a pinned commit;
**[computed]** = numerically established, not mechanized; **[conjecture]** = a stated bet with a
falsification path; **[speculation]** = a reading with no path yet.

**Depends on:** `formal/CoherenceRatchet/LedgerLaw.lean` (the six clauses, the order-≥3 hole);
`papers/notes/entropic_action_bridge.md` (§1–§2 Bianconi construction, §7 lit);
`papers/notes/copula_invariance_remark.md` (higher-order blindness);
`papers/notes/lambda_maintenance_wz.md` (Λ-as-maintenance, the sign law).

**One-line answer.** Under the reading, **gravity** is a well-grounded transfer of Bianconi's
variational relative-entropy action and inherits her GR limit as a **[theorem]**-shaped fence;
**dark matter** is not explained — every candidate the reading offers either is really dark
*energy*, or dies on magnitude, or survives only by becoming observationally indistinguishable
from particle CDM. The reading is **dark-matter-silent**, and the honest deliverable is *why*.

---

## 1. Gravity under the reading

Bianconi's actual objects (bridge §1), stated so the transfer leap is visible:

```
substrate metric   g̃                         eigenvalues ≡ 1  (zero self-entropy, Eq. 9)
induced metric     G̃ = g̃ + α·M̃ − β·R̃        M̃ rank-one in the matter field |Φ⟩ (Eq. 36–37)
Lagrangian         𝓛 = −Tr ln(G̃g̃⁻¹) = −Σ_λ' ln λ'                      (Eq. 40–43)
dressed metric     g̃_𝒢 = 𝒢̃⁻¹ g              what matter actually feels   (Eq. 56)
G-field            𝒢̃  = Lagrange multipliers enforcing G̃g̃⁻¹ = Θ̃        (Eq. 49–50)
```

**Her theory (not ours):** extremizing 𝓛 gives modified Einstein equations; the multiplier
field 𝒢̃ linearizes them (dodging Ostrogradsky) and leaves a **dressed Einstein–Hilbert action
with an emergent small positive Λ set by the G-field alone**. At low coupling (α′,β′ ≪ 1) this
is *exactly* Einstein–Hilbert with zero Λ coupled to matter (Eq. 45–47). GR is the weak-coupling
fence; deviations live only at strong coupling / high curvature where the action stops
linearizing.

**Our transfer:** the Ledger Law's potential is the *same functional* on a correlation matrix.
With substrate = identity and induced = the uniform-ρ Kish matrix C(k,ρ):

```
S(k,ρ) = −Tr ln C = −ln(1 + ρ(k−1)) − (k−1)·ln(1 − ρ) = −Σ ln λ_i          [theorem: T-E1/E5b]
```

term-for-term the Bregman divergence of −ln about the vacuum (Tr C = k ⇒ S = Σ[λ−1−ln λ],
`entropicPotential_nonneg` read forward; `lambda_maintenance_wz` §7b). So under the reading:

```
┌──────────────────────────────────────────────────────────────────────────┐
│  GRAVITY  =  the dynamics that relaxes substrate–coordination misalignment │
│  FORCE    =  gradient structure on the relative-entropy functional S       │
│  VACUUM   =  C = 1  (independent substrate, S = 0, the unique zero) [T-C1] │
│  Λ        =  the standing maintenance cost γ·M of held coordination        │
└──────────────────────────────────────────────────────────────────────────┘
```

**Identical to GR by construction [theorem-backed].** The vacuum is stationary — no first-order
deviation, quadratic coefficient k(k−1)/2 (`vacuum_stationary`, T-L1). This is Bianconi's
linearization theorem in the lake's algebra: *"protection of the GR/ΛCDM limit and
first-order untestability are the same fact."* Any coordination-sourced correction to gravity is
**second order in ρ**. That is the whole reason the reading is hard to test — and the reason it
is not already dead.

**Genuinely different from GR.** Only at second order / strong coupling: (i) the emergent
positive Λ, read here as maintenance cost (`lambda_maintenance_wz`; **[conjecture]**, sign law
exact but sign uncomputed); (ii) departures at high curvature. Nothing at first order.

**Where the transfer leap sits — stated plainly.** Bianconi's 𝒢̃ eigenvalues are eigenvalues of
a *metric ratio* on Dirac–Kähler fields over spacetime; ours are eigenvalues of a *density-field
correlation matrix*. Asserting these are the same spectrum is the leap (`lambda_maintenance_wz`
§7b: "a smaller leap than advertised, but still a leap"). Her modified Einstein equations are
**hers**; the S(k,ρ) algebra is **[theorem]** and survives even if her gravity is wrong (bridge
§7.5); the *identification* is **[speculation]**.

---

## 2. Dark matter — the candidates, and killing each today

### (a) Bianconi's G-field itself (her own suggestion)

A multiplier/maintenance field that gravitates. What phenomenology?

```
The G-field's job is to hold the metric on its constraint surface. Its energy content is
the emergent Λ^G (bridge §7.2: ℋ = Σ z_k[𝒢_k − 1 − ln 𝒢_k] = Λ^G, positive).
  ⇒ equation of state  w ≈ −1   (it IS the cosmological constant)
  ⇒ clustering: NO — a Λ-like term is smooth by construction
```

**Verdict [conjecture → reclassified]:** a field with w = −1 that does not cluster is **dark
*energy*, not dark matter.** This is exactly the role `lambda_maintenance_wz` already assigns it.
To act as dark *matter* it would need w ≈ 0 and to cluster on galaxy scales — the opposite of
what makes it Λ. The one way to give it clustering structure is to pin it to the held stock
(γ·M = α tracks matter, clause 5) — but a field that tracks baryonic coordination dies at the
Bullet Cluster (§3). **(a) is not a dark-matter candidate; it is the dark-energy currency under
a different name.**

### (b) Coordination-content-as-mass

The S of a bound structure contributes effective gravitating energy beyond its constituents:
ΔM_eff ∝ S(structure). Derive the scaling and confront the ~5× dark-to-baryonic ratio.

Need an energy-per-nat scale ε to convert S (nats) to mass: ΔE = ε·S, ΔM_eff = ε·S/c².
Order-of-magnitude for a galaxy (`M_bary ≈ 1.2×10⁴¹ kg`, `N_baryon ≈ 7×10⁶⁷`, and S is
extensive: S ≲ N_units × O(1) since per-unit density saturates at −ln(1−ρ), T-E3):

```
Target:   ΔE_dark ≈ 5 × E_bary = 5 × M_bary c² ≈ 5 × 10⁵⁸ J
Budget:   S ≲ 10⁶⁸ nats  (one coordinating unit per baryon, O(1) relative entropy each)

Required per-nat scale:  ε = 5×10⁵⁸ J / 10⁶⁸ nats ≈ 5×10⁻¹⁰ J/nat ≈ 3 GeV/nat
                         ( ≈ a few nucleon rest masses PER NAT — unmotivated )

Thermal (Landauer, ε = k_BT):
   T = 10 K   → ΔE ≈ 10⁴⁶ J   short of target by ~13 orders
   T = 10⁴ K  → ΔE ≈ 10⁴⁹ J   short by ~10 orders
   T = 10⁷ K  → ΔE ≈ 10⁵² J   short by ~6–7 orders
Planckian (ε = M_Pl c² ≈ 2×10⁹ J):
              → ΔE ≈ 10⁷⁷ J   OVER target by ~18 orders
```

**Verdict [computed → KILLED, twice]:**
1. **Magnitude.** No natural scale lands near the target. Thermodynamic conversion undershoots
   by 6–13 orders; Planckian overshoots by ~18. Hitting 5× requires a dimensionful coupling
   tuned across ~20–30 orders of magnitude. Dead on tuning alone.
2. **Functional form — the sharper kill.** S is extensive: S ∝ N_units ∝ M_baryon. So
   ΔM_eff ∝ M_baryon gives a **constant** dark-to-baryonic ratio at every radius. But the
   observed relation is the **radial acceleration relation (RAR)** — the ratio varies with
   acceleration/radius. A constant-ratio law cannot produce an RAR **[computed]**. Candidate (b)
   predicts the wrong shape *regardless of the coupling*. This kills it even if you grant the
   30-order tuning.

### (c) The order-≥3 inversion

Matter that coordinates only above pairwise order: **dark to the pairwise ledger** (no
EM-visible two-point correlation signature) but **gravitating** if the true ledger is the
all-orders multi-information. This is the LedgerLaw known hole (lines 72–78) and the copula
note's fork, turned into a dark-matter candidate.

```
Pairwise ledger  S = −ln det C  is BLIND above 2nd order  (GHZ pays no tax) [computed: N4 calib]
    ⇒ a purely ≥3-order-coordinated configuration:
         • carries ZERO pairwise correlation  → no two-point EM signature → invisible
         • gravitates IF gravity sources on all-orders MI (the "repair" branch, not the fence)
```

**What it predicts observationally.** A component that (i) does not couple to light through any
two-point channel, (ii) gravitates, (iii) is *not* a function of baryonic pairwise structure —
so it can sit anywhere, including spatially separated from baryons. That is: **collisionless,
EM-dark, gravitating matter with no baryon tie.** Which is — observationally —
indistinguishable from particle CDM.

**Verdict [speculation → survives, but as a relabeling]:** (c) is the only candidate that is not
baryon-tied, so it is the only one that clears the Bullet Cluster (§3). But it makes no
*distinctive* prediction until someone computes whether the all-orders MI of a real matter field
carries ~5× the pairwise MI. It is a *home* for whatever CDM is, not a derivation of it.

---

## 3. The Bullet Cluster confrontation — first, for every candidate

1E 0657-56: weak-lensing mass is spatially **decoupled** from the X-ray plasma (the dominant
baryon reservoir), sitting with the collisionless galaxies. Any candidate tying dark mass to
**baryonic coordination structure** must explain how the coordination content separates from the
baryons in a merger — or die. No softening.

```
┌────────────┬──────────────────────────────────────────────┬──────────┐
│ Candidate  │ Where its mass sits in a merger               │ Bullet   │
├────────────┼──────────────────────────────────────────────┼──────────┤
│ (a) G-field│ pinned to held stock (γM=α) → tracks baryons  │  DIES    │
│            │ (dominant reservoir = the stripped gas)       │          │
│ (b) S-mass │ ΔM_eff ∝ S ∝ N_baryon → tracks baryons        │  DIES    │
│ (c) ≥3-ord │ NOT a function of baryon pairwise structure   │ SURVIVES │
│            │ → free to be collisionless, separates like CDM│          │
└────────────┴──────────────────────────────────────────────┴──────────┘
```

The Bullet Cluster does the whole job in one image: it sorts baryon-tied readings (a, b — the
MOND/Verlinde failure mode) from baryon-independent ones (c). **Cluster mass ratios generally**
sharpen this: even MOND/EG, which fit galaxy RAR, leave a residual missing-mass factor ~2 at
cluster scale (RAR is *not universal* at clusters). Any baryon-tied ΔM inherits that residual.
Candidate (c), being untied, has no cluster residual — because it is just CDM wearing a copula.

---

## 4. The Verlinde precedent — the cautionary tale, surveyed honestly

Verlinde (2016), "emergent gravity": excess gravity as the elastic response of dark energy
displaced by baryons in de Sitter space; an **apparent dark matter density fixed by the baryonic
distribution and H, with zero free parameters.** The exact move being contemplated here.

```
┌──────────────────────┬──────────────────────────────────────────────────────────┐
│ Test                 │ Outcome for Verlinde                                       │
├──────────────────────┼──────────────────────────────────────────────────────────┤
│ Brouwer+ 2016        │ SURVIVED — 33,613 isolated galaxies, galaxy-galaxy lensing │
│ (KiDS weak lensing)  │ matched EG with NO free params. The early success.         │
│ Lelli+ 2017 (RAR)    │ FAILED — EG needs M/L lowered below other estimates, and   │
│                      │ predicts residual radius correlations that are NOT seen.   │
│ Brouwer+ 2021        │ WEAKENED — CDM with a concentration–mass relation fits the │
│ (KiDS-1000 RAR)      │ weak-lensing RAR at least as well; EG loses its edge.      │
│ Cluster scales       │ FAILED — RAR non-universal at clusters; residual missing   │
│                      │ mass ~2. The classic MOND cluster problem, inherited.      │
│ GW170817             │ N/A — Verlinde had no covariant field equations to test.   │
│                      │ The *absence* of a relativistic formulation is the wound.  │
└──────────────────────┴──────────────────────────────────────────────────────────┘
```

**What killed Verlinde:** (1) no covariant/relativistic formulation → no rigorous lensing, no
cosmology, no GW confrontation; (2) cluster-scale residual; (3) RAR radius-residuals; (4) defined
only for static, spherical, isolated systems. **What survived:** the galaxy-scale RAR
coincidence — which it *shares with MOND* and which therefore discriminates nothing.

**What a Bianconi-class theory does differently — and where it does not.**

```
Fixes structurally (vs Verlinde):
  • Covariant: a real action, modified Einstein equations, a field content (the G-field).
  • GR limit is a THEOREM, not an assumption (linearization; our vacuum_stationary).
  • GW170817-SAFE (§5): weak-coupling limit = Einstein–Hilbert ⇒ tensor modes at c.
Does NOT fix:
  • The Bullet Cluster. Covariance does not un-tie mass from baryons. If the dark component
    is sourced by baryonic coordination (a, b), it still sits with the gas. Being a proper
    field theory buys relativistic consistency, NOT spatial separation.
```

The lesson: covariance cures Verlinde's *relativistic* failures (GW, lensing rigor, cosmology)
but is **orthogonal** to the Bullet Cluster, which is a statement about *where the mass is*. Only
decoupling dark mass from baryons (candidate c) clears it, and that decoupling is exactly what
makes the candidate stop being a modified-gravity theory and start being particle CDM.

---

## 5. GW170817 — a fence the Bianconi class passes

GW170817 pins `|c_g/c − 1| ≲ 5×10⁻¹⁶`, killing quartic galileons and a large scalar-tensor /
disformal class that modify tensor-mode speed. Does it touch Bianconi's class?

```
Bianconi weak-coupling limit  =  Einstein–Hilbert + matter, zero Λ  (Eq. 45–47)
  ⇒ tensor perturbations propagate on the undeformed light cone: c_g = c
  ⇒ deviations are 2nd-order / strong-coupling ONLY; the GW propagation path
     (cosmological, weak-field) never leaves the linearized regime
  ⇒ GW170817 does NOT constrain the class.                         [conjecture, well-motivated]
```

This is a genuine **differentiator**: GW170817 is where much of the emergent-gravity zoo died,
and the Bianconi class walks through it *because* its GR limit is a linearization theorem rather
than a bolted-on approximation. (f(R)-type theories are likewise unconstrained by GW speed;
Bianconi's class sits in that safe category.) Note this cuts against the dark-matter ambition,
not for it: the same theorem that makes GW170817 safe (no first-order deviation) is what makes a
galaxy-scale dark-matter effect hard to source — you cannot be invisible to GW170817 *and* move
galaxy rotation curves at first order. You get one or the other.

---

## 6. The falsifiability table (the deliverable's heart)

```
┌─────────────────────┬──────────────────────┬────────────────────────┬───────────────────────┬──────────┐
│ Test / public data  │ Available TODAY       │ Reading predicts        │ Kills the candidate if│ Status   │
├─────────────────────┼──────────────────────┼────────────────────────┼───────────────────────┼──────────┤
│ SPARC + RAR         │ YES (SPARC public)    │ (b): constant M_d/M_b   │ (b) ratio varies with │ (b) DEAD │
│                     │                       │ → no RAR shape          │ radius (it does)      │          │
│ Bullet Cluster      │ YES (lensing maps     │ (a,b) mass tracks gas;  │ (a,b) mass sits off   │ (a,b)    │
│ 1E 0657-56          │ published)            │ (c) mass separates      │ the baryons (it does) │ DEAD;    │
│                     │                       │                        │                       │ (c) OK   │
│ Galaxy-galaxy weak  │ YES (KiDS/DES public) │ (c): dark gravitates,   │ (c) predicts NO 2-pt  │ (c)      │
│ lensing             │                       │ no distinctive 2-pt EM  │ dark–visible cross —  │ SURVIVES │
│                     │                       │ signature; = CDM 2-pt   │ but the cross IS seen │ (as CDM) │
│ Cluster gas-vs-     │ YES (X-ray + lensing) │ baryon-tied → residual  │ residual ~2 present   │ (a,b)    │
│ lensing ratio       │                       │ missing mass ~2         │ (it is)               │ DEAD     │
│ Dwarf spheroidals   │ YES                   │ (b) MOND-like strains;  │ velocity dispersions  │ (b)      │
│                     │                       │ (c) ordinary CDM        │ off constant-ratio    │ STRAINED │
│ GW170817            │ YES (published)       │ Bianconi class: c_g = c │ c_g ≠ c would kill a  │ class    │
│                     │                       │ (passes)                │ deviating class       │ PASSES   │
│ Higher-order MI     │ YES (N-body public)   │ (c): all-orders MI ≈ 5× │ ratio ≪ 5 (likely)    │ (c)      │
│ ratio (the cheap 1) │                       │ pairwise MI on a field  │ → (c) dead too        │ OPEN     │
└─────────────────────┴──────────────────────┴────────────────────────┴───────────────────────┴──────────┘
```

Every row except the last is decidable with data already on disk, and every baryon-tied
candidate (a, b) loses on the first three rows the way Verlinde did.

---

## 7. Honest bottom line

**Per-candidate verdicts:**

```
(a) G-field           → NOT dark matter. w = −1, non-clustering: it is dark ENERGY
                        (the Λ currency of lambda_maintenance_wz). Reclassified, not killed.
(b) coordination-mass → DEAD. Magnitude off by 6–18 orders under any natural scale, AND
                        ∝ M_baryon gives a constant ratio → no RAR. Double kill. [computed]
(c) order-≥3 inversion→ SURVIVES the Bullet Cluster — alone — but only by being
                        observationally CDM. A home for dark matter, not a theory of it.
                        Cheaply killable (row 8). [speculation]
```

**Bullet Cluster outcome:** it is the single most efficient discriminant. It kills (a) and (b)
outright (baryon-tied, MOND/Verlinde failure mode) and spares only (c), which survives precisely
because it severs the dark mass from baryonic structure — the severance that turns it back into
particle CDM.

**The Verlinde lesson:** a covariant, GR-limited, GW170817-safe theory (which Bianconi's class
is, and Verlinde's was not) fixes the *relativistic* failures but is **powerless against the
Bullet Cluster**, because spatial mass–baryon separation is orthogonal to covariance. Do not
mistake Bianconi's mathematical superiority over Verlinde for a dark-matter solution. The reading
predicts, via copula blindness, that coordination *can* be gravitationally dark — which is a
reason particle CDM is **consistent** with the framework, not a replacement for it.

**Does any candidate survive to "worth a computation"?** Only (c), and only weakly. The framework
does not compete with ΛCDM on dark matter; at best it offers (c) as a structural slot.

**The strong form (§8) — "DM's shape is a functional of baryonic coordination" — is dead.** It is
candidate (b) sharpened into its most falsifiable version, and the sharpening is what kills it:
clause 3 (`copula_blindness`, **[theorem]**) forces `M_dark/M_bary ∝ Σ_b⁻¹` against the observed
`Σ_b^(−1/2)`, a ~1.5 dex divergence across SPARC's range. What the Ledger Law *does* contribute
is §8.3: a discipline for reading residuals, in which clause 2 (Stein) forbids any coordinating
cause from hiding in one — except in the order-≥3 blind spot, which is candidate (c) again.

**The single cheapest computation** (row 8, and it reuses existing machinery —
`copula_invariance_remark` §3's rank-based-S test / `s_of_a.py`):

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Take one public N-body density field. Estimate the all-orders multi-        │
│ information I_full (kNN/MI estimator) and the pairwise Gaussian I_pair =     │
│ S/2 = −½ ln det C on the SAME cells. Form the ratio  R = (I_full − I_pair)/  │
│ I_pair — the fraction of coordination carried purely above second order.     │
│                                                                              │
│   R ~ 5   → candidate (c) is quantitatively alive: higher-order coordination │
│             could carry the dark-to-baryonic mass ratio. Advance it.         │
│   R ≪ 1   → (c) is dead too (cosmic fields are only mildly non-Gaussian;     │
│             this is the expected outcome). The reading is dark-matter-SILENT,│
│             cleanly and on the record.                                       │
└────────────────────────────────────────────────────────────────────────────┘
```

That one ratio decides whether the reading has *anything* to say about dark matter, costs an
afternoon on data already public, and is the same discriminator the LedgerLaw carries as its own
L-01. Everything upstream (gravity, GW170817, the Λ currency) stands regardless of its outcome;
only the dark-matter slot depends on it.

---

## 8. The strong form: "DM's shape is predicted from baryonic coordination"

**The claim under test.** *Under the ledger reading, dark matter's shape and distribution are
predicted from the baryonic coordination structure — DM is not a free field but a functional of
the visible matter. Residuals from that prediction are then candidates for new physics.*

This is the strongest and most falsifiable form of the reading. It is also a **well-populated
class** — MOND, the RAR, Verlinde — with a known failure record. Treated accordingly, and it does
not survive. The kill comes from the framework's own clause 3, which is a **[theorem]**.

### 8.1 What the ledger actually predicts

Write the baryonic density contrast `δ_b` on cells, `C[δ_b]` its normalized correlation matrix.
The ledger's coordination content and the dark mass it would source:

```
S[δ_b] = −ln det C[δ_b]                                     [theorem: T-E5b]
ΔM_eff(<r) = (ε/c²) · S[δ_b](<r)        ε = energy per nat, ONE global constant
```

The structural predictions are immediate and rigid:

```
• ρ_dark(r) = 0 wherever there are no baryons     → NO DM WITHOUT BARYONS
• ρ_dark(r) > 0 wherever baryons coordinate       → NO BARYONS WITHOUT THEIR DM
• zero per-galaxy freedom: ε is universal          → the parameter-freedom claim
• DM is spatially CO-LOCATED with baryonic coordination structure
```

**Now the obstruction, and it is fatal at the level of a theorem.** Clause 3
(`copula_blindness`, T-L2) says S is invariant under uniform amplitude rescaling: S depends only
on the *shape* of the correlation structure, never its amplitude. C is the *normalized*
correlation matrix. Therefore:

```
┌────────────────────────────────────────────────────────────────────────────┐
│  δ_b → λ·δ_b   ⇒   S unchanged   ⇒   ΔM_eff unchanged   [theorem, clause 3] │
│  but            M_bary → λ·M_bary                                           │
│                                                                             │
│  ⇒   M_dark / M_bary  ∝  λ⁻¹  ∝  Σ_b⁻¹                                      │
└────────────────────────────────────────────────────────────────────────────┘
```

Compare the observed law. In the low-acceleration (deep-MOND / RAR) regime,
`g_obs = √(g_bar·a₀)`, so

```
M_dark/M_bary ≈ g_obs/g_bar − 1 ≈ √(a₀/g_bar) ∝ Σ_b^(−1/2)          [observed, SPARC]
              ────────────────────────────────────────────
ledger:       M_dark/M_bary                    ∝ Σ_b^(−1)            [theorem-forced]
```

**The exponent is wrong: −1 against −1/2.** Two consequences, both worth stating:

1. *The sign is right, which is why this deserved a test.* Scale invariance does make
   low-surface-brightness systems more dark-matter-dominated — the correct qualitative direction,
   for free. That is a real (if cheap) success and it is why the strong form is not silly.
2. *The magnitude is wrong, and irreparably.* Across SPARC's surface-brightness range
   (`Σ_b` spans ~3 dex), the two laws diverge by `10^(3×0.5) ≈ 30×`. **[computed]**

And there is a second, independent obstruction of the same origin: `a₀ = 1.2×10⁻¹⁰ m/s²` is an
**acceleration** — a dimensionful amplitude. A shape-only functional cannot generate it. The
ledger has no acceleration scale and no way to acquire one except by hand.

**The dilemma, both horns fatal.**

```
Horn A: keep ε universal (the parameter-freedom claim)
        ⇒ M_dark/M_bary ∝ Σ_b⁻¹, no a₀. Killed by SPARC. [computed]
Horn B: let ε (or the cell grain) vary per system to restore Σ_b^(−1/2) and inject a₀
        ⇒ the theory is no longer parameter-free, which was its entire content.
```

The very clause that makes S a *good* coordination measure — blindness to packaging, receipts
record substance not amplitude — makes it a *bad* dark-matter generator. That is not a bug found
by an opponent; it is clause 3 read honestly.

### 8.2 The three standard killers, in order

**(a) Bullet Cluster / merging clusters — the strong form is ANTI-predicted, not merely null.**

Cluster baryons are gas-dominated: `M_gas ≈ 5–6 × M_stars`. So the baryonic coordination
structure — and hence S, and hence `ΔM_eff` — is carried overwhelmingly by the plasma, not the
galaxies. The strong form therefore predicts the lensing mass peaks **on the gas**.

```
Observed (Clowe+ 2006 and successors): lensing mass sits with the collisionless GALAXIES;
the gas sits between, offset, at ~8σ.                                    → falsified

Worse — a directional prediction, not a null:
   a merger shock COMPRESSES and CORRELATES the plasma  ⇒  ρ rises  ⇒  S rises
   ⇒ the ledger predicts a dark-mass ENHANCEMENT AT THE SHOCK FRONT.
   Observed: no lensing peak at the shock. The reading points the wrong way.
```

> **[CORRECTED 2026-07-10 — see `papers/notes/bullet_cluster_correction.md`.] The derivation
> above is WRONG and violates clause 3 of the Ledger Law, a proved theorem: S is blind to
> amplitude. Shock COMPRESSION is a density change S cannot see; what the shock does to the
> correlation structure is THERMALIZE it (gas entropy sharply increases; velocities → Maxwellian
> → independence). So the shocked plasma is the LOW-S component and the collisionless galaxies,
> which retain coherent bulk motion, are the HIGH-S component. The ledger therefore points AT
> the lensing mass, which sits with the galaxies at ~8σ. The Bullet Cluster does NOT kill this
> reading; it is the place where the ledger BEATS MOND, which tracks baryonic mass (90% gas) and
> points at the gas. The magnitude, dwarf-spheroidal and DF2/DF4 objections are unaffected.**

**Verdict: ~~DEAD~~ RETRACTED.** ~~This is the strongest kill in the note, because it is anti-correlated rather
than uncorrelated.~~ A theory that is merely silent can be repaired; one whose mechanism points at
the empty region cannot.

**(b) Cluster-scale mass ratios.** MOND and Verlinde both leave a residual missing-mass factor
~2 at cluster scale; the RAR is *not universal* at clusters. Any baryon-determined `ΔM` inherits
that residual by construction. The ledger inherits it **and makes it worse**: clusters are
high-`Σ_b` relative to galaxy outskirts, and the `Σ_b⁻¹` law under-produces dark mass there
faster than MOND's `Σ_b^(−1/2)`. **[computed]**

**(c) Both directions of the functional map break it.**

```
DM-DEFICIENT: NGC1052-DF2 / DF4.  Baryons present, DM absent.
   Strong form says "no baryons without their DM" → DIRECTLY FALSIFIED.
   MOND's escape: the External Field Effect (nonlinear Poisson ⇒ weakened self-gravity
     near a massive host). Requires DF2/DF4 within ~150–300 kpc of NGC 1052.
     TRGB distance to DF2: 22.1 ± 1.2 Mpc; DF2–DF4 relative separation 2.1 ± 0.5 Mpc
     ⇒ both cannot be within 300 kpc. The escape is strained at best.
   ── THE LEDGER HAS NO SUCH ESCAPE. S is a LOCAL functional of the internal
      correlation structure; it carries no dependence on an external gravitational
      field. There is no ledger analogue of the EFE. The reading dies HARDER than MOND
      here: MOND has a contested escape hatch; the ledger has none.

DM-DOMINATED: dwarf spheroidals, M/L ~ 10²–10³.
   Strong form: M_dark/M_bary ∝ Σ_b⁻¹. dSph Σ_b ~ 0.1–1 vs spiral ~10²  ⇒ λ ratio 10²–10³
   ⇒ predicted enhancement 10²–10³ against observed ~10–10².  OVERSHOOTS by ~1 dex.
   Same wrong exponent, now visible from the other end of the range.
```

**§8 verdict: the strong form is dead, three times, by three independent routes**, and the
scaling exponent (8.1) predicted every one of them in advance. It died at the Bullet Cluster on
mechanism, at clusters on magnitude, and at both tails of the surface-brightness range on
exponent.

### 8.3 The residual methodology — the discipline, written honestly

The operator asks whether variance from prediction flags new physics. Here is the standard.

**(i) The systematic floor. What actually dominates DM residuals today.**

```
SPARC radial acceleration relation, the reference numbers:
  observed rms scatter                              0.13 dex   (McGaugh+16, Lelli+17a)
  after marginalizing Υ*, distance, inclination     0.057 dex  (Li & McGaugh 2018)
  full joint inference, intrinsic scatter           0.034 ± 0.001 dex  (Desmond 2023)
  ──────────────────────────────────────────────────────────────────────────────────
  ⇒ ~0.10–0.12 dex of the 0.13 dex observed scatter is NUISANCE, not physics.
  ⇒ THE SYSTEMATIC FLOOR IS ~3–4× THE INTRINSIC SIGNAL.
```

| Systematic | Typical effect size | Vs. a residual one would want to interpret |
|---|---|---|
| Stellar M/L (Υ*_[3.6]) | ~0.1 dex | alone exceeds the intrinsic scatter (0.034 dex) by 3× |
| Distance | 5–10% | enters `g_bar`, `g_obs` differently; ~0.03–0.05 dex |
| Disk inclination | 3–5° error | ~0.05 dex in `g_obs`, worse at low `i` |
| Halo triaxiality | 10–20% in lensing `M` | comparable to any claimed cluster residual |
| Baryonic feedback amplitude | factors of **2–5** in inner DM density | the core–cusp problem *is* this systematic |
| Sim resolution | biased low inside ~3× softening | manufactures inner-profile "residuals" |

**Any claimed new-physics residual below ~0.10 dex in RAR-space is indistinguishable from
Υ* + distance + inclination.** In the inner regions, feedback amplitude alone moves the DM
density by factors of a few. That is the whole scientific content of the "residual" question, and
it is a number, not an argument.

**(ii) The general rule.**

```
A residual is evidence for "MODEL INCOMPLETE." Nothing more.

A residual is evidence for a SPECIFIC alternative if and only if that alternative makes a
POSITIVE, INDEPENDENT, FALSIFIABLE prediction that the incumbent does not make — and that
prediction is then checked SEPARATELY from the residual that motivated it.

Residual-attribution without an independent positive signature is the archetypal
unfalsifiable move. It is rejected by this project's own evidence standards.
```

**This project has already convicted itself of exactly this failure and quarantined the result.**
`RATCHET/fiction/ADVERSARIAL_ANALYSIS.md` is a fluent, confident security narrative whose
quantitative claims were **fabricated and contradicted by measurement** — it asserted the
constraints collapse to `k_eff ≈ 3–5`, while the measured effective dimensionality on the real
6,465-trace corpus is `N_eff_PR ≈ 6.0 / N_eff_H ≈ 7.7` (*higher*, not collapsed). It carries a
banner and lives in `fiction/`. The failure mode was precisely a compelling story fitted to an
expected residual with no independent positive signature. **The house standard is already set;
this section applies it to gravity.**

**(iii) The Ledger Law's own clause 2 answers the residual question — and it is sharp.**

Clause 2a (`exchange_rate_information`, T-E5c) is a **[theorem]**: `S = 2·I`, and `S/2` is the
Chernoff–Stein detection exponent. *Sourcing coordination and emitting detectability are the same
act.* Detection latency `~ ln(1/P_err)/(S/2)`.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  THE LAW FORBIDS A COORDINATING CAUSE HIDING IN A RESIDUAL.                    │
│                                                                               │
│  If an unmodeled agency COORDINATES (self-interacting DM, a fifth force        │
│  correlating tracers, an unmodeled field), it sources S > 0, and by clause 2   │
│  it emits its own receipt at rate S/2 in the PAIRWISE correlation structure.   │
│                                                                               │
│  Exactly ONE exception exists, and the law names it on its own face:           │
│  the ORDER-≥3 BLIND SPOT (LedgerLaw ll.72–78; copula_invariance_remark §2.3).  │
│  Coordination carried purely above pairwise order emits ZERO pairwise receipt  │
│  (GHZ: ρ̄ ≈ 0 in the X basis — the N4 calibration result).                     │
└──────────────────────────────────────────────────────────────────────────────┘
```

The disciplined framing follows immediately, and it is the point of this section:

```
Gravitational residual observed, no pairwise correlation signature found:

  ├── Claim: an ordinary (order ≤2) coordinating cause
  │     → the law says the signature MUST exist, at rate S/2, with a computable latency
  │     → GO LOOK FOR IT. Absence at the predicted latency FALSIFIES the claim.
  │
  └── Claim persists with no signature
        → the claimant is now ASSERTING order-≥3 coordination, whether or not they say so
        → that is a POSITIVE, FALSIFIABLE claim: the rank-based-S flatness test
        → make it explicitly, or withdraw.
```

**Bottom line of the methodology: the law converts "unexplained residual" from an invitation into
a demand.** It demands a positive independent signature at a computed rate, and it names the
unique place where such a signature may legitimately be absent. A residual claim that refuses
both horns — no signature, no order-≥3 commitment — is unfalsifiable and is rejected here. This
is the one place the Ledger Law earns its keep in the dark-matter discussion: not by explaining
dark matter, but by **disciplining what may be inferred from failing to explain it.**

### 8.4 The cheapest test today — SPARC, and it costs one scatter plot

Data: **SPARC** (Lelli, McGaugh & Schombert 2016), 175 galaxies, public: rotation curves,
3.6 μm photometry (near-constant `Υ*`), HI surface densities. Published `(g_bar, g_obs)` table.

**Full spec (what a careful run does):**

```
1. Σ_b(r) from [3.6] photometry (SPARC standard: Υ*_disk = 0.5, Υ*_bulge = 0.7)
   plus HI × 1.33 (helium).
2. Coarse-grain into radial cells; build the normalized correlation matrix C of the
   baryonic density contrast across cells — the ledger's coordination structure.
3. S(<r) = −ln det C(<r).   ΔM_eff(<r) = (ε/c²)·S(<r).
4. Fix ε ONCE, globally, for all 175 galaxies. This is the parameter-freedom claim.
5. g_pred(r) = G[M_bary(<r) + ΔM_eff(<r)] / r².  Compare to g_obs from V(r).
6. Report: (i) RAR residual rms in dex; (ii) the SLOPE of log(M_dark/M_bary) vs log Σ_b.
```

**Pre-registered discriminants, in order of strength:**

| # | Prediction | Kills the strong form if |
|---|---|---|
| 1 | slope of `log(M_d/M_b)` vs `log Σ_b` = **−1** (forced by clause 3) | the slope is `−1/2` (the RAR value) |
| 2 | RAR residual rms ≤ 0.13 dex with ONE global `ε` | rms ≫ 0.13 dex, or `ε` must vary per galaxy |
| 3 | any residual claim exceeds the systematic floor | residual < 0.10 dex ⇒ indistinguishable from `Υ* + D + i` |

**And here is the whole point: discriminant 1 needs neither step 2 nor step 3 nor `ε`.**

```
┌───────────────────────────────────────────────────────────────────────────┐
│  The exponent is theorem-forced by clause 3. It does not depend on ε, on   │
│  the cell grain, or on Υ*. So the test reduces to plotting SPARC's ALREADY │
│  PUBLISHED (g_bar, g_obs) columns and reading off whether the dark-to-      │
│  baryonic ratio scales as Σ_b⁻¹ or Σ_b^(−1/2).                             │
│                                                                            │
│  Expected outcome, stated in advance: it scales as Σ_b^(−1/2).             │
│  The strong form fails by ~1.5 dex across SPARC's range. One afternoon,    │
│  one scatter plot, and the answer is already visible in the literature.    │
└───────────────────────────────────────────────────────────────────────────┘
```

Discriminant 3 is where the residual question actually lives. The number that matters is
**0.10 dex** — the systematic floor. The strong form never reaches it: it fails at the level of
the *exponent*, roughly 1.5 dex of divergence, more than an order of magnitude above the floor.
**There is no residual to interpret, because there is no fit to residuate from.**

---

## Sources

- Brouwer et al. 2016, first weak-lensing test of emergent gravity: [arXiv:1612.03034](https://arxiv.org/abs/1612.03034); [MNRAS 466, 2547](https://academic.oup.com/mnras/article/466/3/2547/2661916)
- Lelli et al. 2017, EG vs the radial acceleration relation: [arXiv:1702.04355](https://arxiv.org/abs/1702.04355); [MNRASL 468, L68](https://academic.oup.com/mnrasl/article/468/1/L68/2998721)
- Brouwer et al. 2021, weak-lensing RAR with KiDS-1000: [arXiv:2106.11677](https://arxiv.org/pdf/2106.11677)
- Verlinde emergent gravity vs galaxy clusters: [MNRAS 487, 3734](https://academic.oup.com/mnras/article/487/3/3734/5520807); RAR in clusters [MNRAS 492, 5865](https://academic.oup.com/mnras/article/492/4/5865/5716677)
- EG in dwarf spheroidals: [arXiv:1706.00785](https://arxiv.org/pdf/1706.00785); [MOND vs EG in dSph](https://arxiv.org/pdf/2601.01715)
- Bullet Cluster mass reconstruction: [A&A 594, A116 (2016)](https://www.aanda.org/articles/aa/full_html/2016/10/aa27959-15/aa27959-15.html); [arXiv:1209.0384](https://arxiv.org/pdf/1209.0384)
- GW170817 speed-of-gravity constraint on modified gravity: [f(T) after GW170817, arXiv:1801.05827](https://arxiv.org/abs/1801.05827); [Born-Infeld, arXiv:1711.04137](https://arxiv.org/abs/1711.04137)
- Bianconi, *Gravity from entropy*, Phys. Rev. D 111, 066001 (2025): [arXiv:2408.14391](https://arxiv.org/abs/2408.14391); thermodynamics follow-up [arXiv:2510.22545](https://arxiv.org/abs/2510.22545)

**§8 additions:**

- McGaugh, Lelli & Schombert 2016, RAR (scatter ~0.11 dex, `a₀ = 1.2 ± 0.26 × 10⁻¹⁰` m/s²); Lelli et al. 2017a, "One Law to Rule Them All" (observed rms 0.13 dex): [ApJ 836, 152](https://iopscience.iop.org/article/10.3847/1538-4357/836/2/152)
- Li & McGaugh 2018, fitting the RAR to individual SPARC galaxies (residual rms 0.057 dex after marginalizing `Υ*`, distance, inclination): [arXiv:1803.00022](https://arxiv.org/pdf/1803.00022); [A&A 615, A3](https://www.aanda.org/articles/aa/full_html/2018/07/aa32547-17/aa32547-17.html)
- Desmond 2023, joint inference of RAR intrinsic scatter (0.034 ± 0.001 dex): [MNRAS 526, 3342](https://academic.oup.com/mnras/article/526/3/3342/7306858)
- RAR in clusters (non-universality): [ApJ 897, 40, CLASH](https://iopscience.iop.org/article/10.3847/1538-4357/ab8e3d); [MNRAS 492, 5865](https://academic.oup.com/mnras/article/492/4/5865/5716677)
- van Dokkum et al. 2018, NGC1052-DF2; and *Does NGC1052-DF2 falsify Milgromian dynamics?* [Nature 561](https://www.nature.com/articles/s41586-018-0429-z), [arXiv:1903.11612](https://arxiv.org/abs/1903.11612)
- Haghi et al. 2019, external field effect applied to DF2/DF4: [MNRAS 487, 2441](https://academic.oup.com/mnras/article/487/2/2441/5505850)
- Shen et al. 2021, TRGB distance to DF2 (22.1 ± 1.2 Mpc, 40 HST orbits): [arXiv:2104.03319](https://arxiv.org/pdf/2104.03319)
- House precedent for residual-attribution without an independent signature: `RATCHET/fiction/ADVERSARIAL_ANALYSIS.md` (quarantined; fabricated `k_eff ≈ 3–5` collapse claim contradicted by the measured `N_eff_PR ≈ 6.0 / N_eff_H ≈ 7.7` on the 6,465-trace corpus)
