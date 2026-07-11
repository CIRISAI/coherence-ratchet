# Corridor-ceiling test — SUMMARY

**Date 2026-07-10.** Does a maintained-correlation (equicorrelation OU) system have a
maximum steady-state entropy-production rate `σ_max` that COLLAPSES as coordination
deepens (`ρ → 1`, `k_eff → 1`), so that — joined to `dρ/dt = α − γM` — the corridor's
upper edge is a maintenance supply=demand crossing? Pre-statement in `DECISIONS.md`
(three normalizations + physical pick + kill condition, all fixed before results).

## Headline

**The verdict is normalization-dependent, and the sign flips.** Under the
physically-motivated normalization (N1, bounded *actuated* drive) `σ_max` **collapses**
as `ρ→1` — the ceiling mechanism is **not killed**. Under a defensible alternative (N3,
bounded *bare* stirring power) it **inverts** — `σ_max` grows toward the pole. The
disagreement is the finding, exactly as pre-flagged. The whole result hinges on one
physical question — is the maintenance cost the actuated drive or the bare circulation? —
and I argue (below) it is the actuated drive, which gives collapse. But this is a
*conditional* survival, not a clean confirmation, and it does **not** derive the 0.43
edge parameter-free.

## Formula, verified

OU entropy production `σ = Tr[Qᵀ D⁻¹ Q C⁻¹]` (Godrèche–Luck 2019, arXiv:1807.00694;
Kwon–Ao–Thouless 2005), `Q =` antisymmetric part of `BC`. **Verified two independent
ways** in `sigma_max.py`: (a) against the Sekimoto housekeeping-heat form
`σ = Tr(Bᵀ D⁻¹ B C) − Tr(B)` — agreement to machine precision (err 0.0); (b) against a
direct Euler–Maruyama simulation of the Stratonovich heat rate `⟨F∘dx⟩/dt` — agreement
to 0.2%. In C's eigenbasis, `σ = Σ_{i<j} Q_ij² (1/λ_i + 1/λ_j)`, and the whole question
is which normalization bounds the free `Q_ij` against the diverging `C⁻¹` eigenvalue
`1/(1−ρ)` on the k−1 collapsed modes.

## σ_max(ρ→1) trend under all three normalizations (k ∈ {2,3,5,10,50})

| normalization | what is bounded | `σ_max(ρ→1)` | trend |
|---|---|---|---|
| **N1** fixed noise D=I, **actuated** drive `‖QC⁻¹‖_F² ≤ P` | force the machine applies | `∝ (1−ρ) → 0` | **COLLAPSE** |
| **N2** fixed timescale, spectral `‖B‖₂ ≤ b` | relaxation rate | finite, then hard **feasibility wall** at `ρ = 1−1/b` (→0) | COLLAPSE + cutoff |
| **N3** **bare** stirring `Tr[QᵀQ] ≤ P` | geometry-blind circulation | `∝ 1/(1−ρ) → ∞` (k≥3); `1/(1−ρ²)` (k=2) | **INVERSION** |

Trend is uniform across k (2→50). N1 falls to ~2% of its ρ=0.1 value by the pole; N3
rises ~25–50×. N2 (b=3) declines then hits an infeasibility wall at ρ=0.667 = 1−1/b.

## Why N1 is the physical one (pre-committed reasoning), and the collapse mechanism

To sustain circulation `Q` at covariance `C`, the drift *must* contain `QC⁻¹` (forced by
`B=(D+Q)C⁻¹`) — that is the drive the machine actually actuates, not a free choice. A
real coherence-management system (cell, cortex, institution) is limited by the **force it
can apply at a given noise floor** — N1 — not by an abstract geometry-normalized stirring
rate. N1 and N3 differ by exactly the stiffness gearing `C⁻¹`: exciting a unit circulation
in a collapsed (variance `1−ρ`, stiff) mode needs a force amplified by `1/(1−ρ)`, while it
sweeps only `∝(1−ρ)` phase-space area, so **entropy produced per unit force² `∝ (1−ρ) → 0`**.
Physically: *you cannot stir a rigidly-clamped system.* N3 charges `Q` in bare units and
so never pays the amplification; a real actuator does. (Guard, also pre-stated: I do **not**
charge the divergent *reversible* stiffness `‖C⁻¹‖` against the budget — a stiff
equilibrium trap has detailed balance and zero housekeeping cost, so charging it would
manufacture a false ceiling. N1 charges only the irreversible `QC⁻¹`; N2's wall is
explicitly the reversible-stiffness feasibility limit, flagged as conceptually distinct.)

**So the ceiling mechanism is real under bounded actuation and is killed under bounded
bare-stirring. It survives iff the maintenance budget is actuation-limited — which I argue
it is.** This is the honest crux; a reader who takes the bare-stirring reading gets the
inversion and should reject the mechanism.

## Where the collapse begins relative to 0.43 — and the 0.43 edge is NOT parameter-free

Under N1 the collapse is **smooth and monotone from ρ=0** (`σ_max ∝ 1−ρ`); there is **no
special onset at 0.43**. By ρ=0.43, `σ_max` is already down to 58–70% of its ρ=0.1 value
(k-dependent); it is not a cliff. So 0.43 can only become the corridor edge as a
**supply=demand crossing** `σ_max(ρ) = α(ρ)`. With supply `P(1−ρ)` (falling) and any
increasing demand `α = a·ρ` (drift toward the pole, rising), a crossing is **generic** —
one edge always exists because supply falls and demand rises. But its **location**
`ρ* = 1/(1+a/P)` requires tuning the single ratio `a/P`; hitting 0.43 needs `a/P = 1.326`.
**The mechanism yields a generic upper edge, not the specific value 0.43 without tuning.**
That is weaker than "the first mechanistic derivation of the 0.43 ceiling" hoped for in
the sideways pass — downgrade the claim accordingly.

## Part B (data): the scatter cannot adjudicate — the pole region is unoccupied

Assembled from the `keff_saturation` catalog (real found systems only; `catalog_scatter.py`,
`catalog_scatter.png`), corridor position `k_eff = eff_rank_surr`, irreversibility
circulation `|z|`:

| substrate | k_eff | rho_proxy=1/k_eff | DB `|z|` | class |
|---|---|---|---|---|
| motor cortex (MC_Maze) | ~7 | 0.14 | **12.5** | coordinating |
| visual cortex (Allen movie) | ~6 | 0.17 | 4–7 | coordinating |
| C. elegans (calcium) | ~9 | 0.11 | 2.75 (weak est.) | coordinating |
| galaxy baryon cycle (TNG) | ~2.5 | 0.40 | 0.03–0.62 | bound |
| *phase-randomized dead cell* | *1* | *1.0* | *1.6* | *CONSTRUCTED — flag* |

The occupancy-edge prediction (nothing coordinating with high σ near the pole) is **not
testable here**: every FOUND coordinating system sits at k_eff 6–9 (rho_proxy 0.11–0.17),
deep **inside** the corridor, nowhere near ρ→1. The only near-pole point (k_eff=1) is the
dead cell — reversible **by construction**, so it neither confirms nor kills. Within the
populated band, k_eff and `|z|` are ~independent (Spearman +0.40, p=0.60, n=4 — n.s.; and
the program's own larger matched-N axis-independence run concludes independence): the
lowest-k_eff found system (galaxy) is bound, but for an *independent* reason (cosmic-assembly
transient, no sustained drive), while motor cortex at k_eff~7 breaks DB hardest. **The data
are silent on the ceiling because no found substrate lives near the pole.**

## Bottom line

- σ_max **collapses ∝(1−ρ)** under the physical (bounded-actuation) normalization →
  ceiling mechanism **not killed**; **inverts ∝1/(1−ρ)** under bounded bare-stirring. The
  sign hinges entirely on the actuation-cost argument.
- The collapse is smooth from ρ=0; **0.43 is not special** and is recovered only by tuning
  one supply/demand ratio. The strong claim ("parameter-free derivation of 0.43") is **not
  supported**; the defensible claim is "a generic maintenance-limited upper edge exists,
  location set by α/budget."
- The catalog **cannot test** the occupancy edge (no found system near the pole); k_eff and
  irreversibility read as independent in the populated band.

Files: `DECISIONS.md`, `sigma_max.py`, `catalog_scatter.py`, `results.json`,
`catalog_scatter.png`. Seed 20260710, CPU only, real data only.

---

## Orchestrator sideways pass (2026-07-10)

The conditional verdict is accepted as stated. Three additions from context outside the brief:

**1. The proven instance sides with N1.** The one arena where the inequality is an exact
theorem — flavor space, |J| ≤ J_max(angles) → 0 at the comonotone pole — has NO bare-stirring
reading: the Jarlskog bound is actuated-form by construction (the phase can only act through
the angle structure, paying the full alignment gearing). The single proven member of this
theorem family collapses. That is independent weight for the bounded-actuation pick beyond
the physical argument given above; the N3 reader must also explain why the proven instance
behaves like N1.

**2. a/P = 1.326 is a measurement target, not a tuning knob.** The demand-to-budget ratio
that places the edge at 0.43 is an interpretable physical constant, independently measurable
on any substrate (drive budget and drift are both estimable). Same epistemic shape as k_B:
the mechanism supplies the law σ_max = P(1−ρ), the constant is measured once. The claim
downgrade stands (generic edge, not parameter-free 0.43) — but "one measurable constant"
is the program's normal, not a defeat.

**3. The falsification path is interventional and in-house.** The found-systems catalog
cannot adjudicate (the occupancy pattern IS the explanandum), but the engineering tier can
build the test: the GPU coherence rigs / CIRISArray strain gauges (RATCHET L2) can DRIVE
k_eff toward the pole under controlled actuation budget and measure whether maintainable
circulation collapses ∝(1−ρ). Registered as the decisive test: an engineered substrate
holding high measured σ at ρ ≫ 0.43 under bounded actuation kills the mechanism; the
predicted collapse curve confirms it. This converts the ceiling mechanism from a
normalization argument into a bench experiment.
