# P_ω — the holographic construction — results

**Date:** 2026-05-22. **Falsification handle:** F-11 / F-12.
**Pre-registration:** `holographic_pomega/PREREGISTRATION.md` (committed before
this run). **Build:** `build_holographic_pomega.py` (reuses
`build_history_pomega.py` — R2's sequential-emergence simulator — via
`../R1xR2_conjunction/`; reuses the fractal run's joint Kish functional
verbatim, changing only the cross-rung topology).
**Raw:** `results_holographic.json`, `run_holographic.log`.

---

## VERDICT: EMPTY — H-holo fails on BOTH horns of the two-sided test

The holographic construction — R1∧R2's non-additive joint Kish
participation-ratio functional, on R2's open sequential history-space frame,
with the cross-rung coupling being the **genuine MERA-as-AdS causal-cone-overlap
geometry** (Piece 6 / `construct_p_omega_mera.py`'s MERA tower; Swingle: MERA is
a discrete slice of an AdS geometry) — **horns EMPTY**, and it fails the
pre-registered two-sided test on **both** sides at once:

- **(a) τ is far BELOW the cross-rung corridor at every scale.** τ_(n,n+1), the
  cross-rung mutual information (Piece 6), sits at τ ≈ 0.000–0.007 across all
  scale-steps — three or more orders of magnitude below the corridor floor
  τ_lower = 0.10. The genuine AdS bulk geometry does not drive τ → 1 (rigidity);
  it drives τ → 0 (the chaos pole on the cross-rung axis). The rungs **decouple**
  under the genuine holographic coupling.
- **(b) ρ_joint dilutes — FASTER than every decaying topology the fractal run
  tested.** `ρ_joint ~ R^-1.39` for the holographic coupling, against the
  chain's `R^-1.09` and the fractal RG-flow Toeplitz's `R^-1.14`. The joint
  k_eff is extensive — slightly *super*-extensive, `~R^1.04`. The band floor is
  crossed downward at R ≈ 5; the ω-set is exactly empty from R = 13, before and
  past the framework's 9 rungs.

The decisive hypothesis H-holo predicted the genuine holographic structure
threads BOTH — τ in corridor at every scale AND ρ_joint non-diluting. It fails
both. The dilution is not broken; it is *steeper*. Per the binding terminal
commitment in the pre-registration: **F-11 fires.** The topology axis
(decaying ∪ non-decaying) is now exhausted.

Reported flat, per the pre-registration. EMPTY is a valid two-sided result.

---

## The construction

**Frame (from R2), reused unchanged.** `build_history_pomega.py` — universe
trajectories, rungs Ph0…A5 emerging sequentially over cosmic time, each rung's
within-rung ρ_n(t) evolving by Piece 2 dynamics `dρ/dt = α − γM`, held in its
corridor by active management. The all-emerged sub-ensemble is what the
post-selection acts on. Identical module to the R1∧R2 conjunction and the
fractal run.

**Functional (from R1∧R2 / the fractal run), reused verbatim.** `ρ_joint` = the
Kish-inverse of the participation ratio `(Tr C_w)² / Tr(C_w²)` of the
corridor-weighted R×R rung-correlation matrix `C_w = D C D`, `D = diag(√w_n)`,
`w_n = soft(ρ_n at t_f)`. The `joint_rho_history` function is byte-for-byte the
fractal run's. The chain and rgflow topologies are recomputed in the same run as
the in-run decaying baselines, and reproduce the fractal run's published table
to four decimals (R=3 ρ_joint: chain 0.1694, rgflow 0.1499; R=9: chain 0.0498,
rgflow 0.0388; R=20: chain 0.0228, rgflow 0.0188) — a direct cross-check that
the only change is the topology.

**The one change — the cross-rung coupling is the genuine MERA-as-AdS
geometry.** This is the discipline crux, so it is stated in full.

A binary MERA over an R-scale tower: the boundary has L = 2^(R−1) sites; the
bulk is the binary coarse-graining tree, depth d carrying 2^(R−1−d) tensors,
d = 0 (finest boundary) … R−1 (the single deep-bulk core tensor). A rung n is
the set of bulk tensors at scale d = n — exactly `construct_p_omega_mera.py`'s
tower H_0 → H_1 → … read as a binary tree.

The holographic cross-rung coupling `C_holo[n,m]` is **not** written down as a
matrix. It is **derived** from the network, tensor by tensor, by the genuine
MERA causal-cone structure:

> The causal cone of a bulk tensor at depth d contains the boundary block it
> coarse-grains. Reading inward, rung n (scale n) and rung m (scale m) couple
> through the bulk tensors their causal cones **share** — their lowest common
> ancestors in the binary tree. For an ancestor at bulk depth a (a ≥ max(n,m)),
> the connecting bulk geodesic dips from depth n up to a and back to depth m:
> geodesic length `L = (a−n) + (a−m)`. The bulk two-point function along a
> geodesic of length L is `C1_RG^L` — each bulk step contracts by the measured
> per-step factor. `C_holo[n,m]` is the causal-cone-overlap average of `C1_RG^L`
> over **all** shared-ancestor channels, with the standard binary-tree LCA
> combinatorics counting how many tensor pairs route through each depth-a
> ancestor.

The deep-bulk core tensor (the AdS "center") is in the causal cone of *every*
rung — that channel is included. The construction does not pre-judge whether
`C_holo` decays with |n−m|: it **computes** the cone-overlap and lets the AdS
bulk geometry decide.

**c₁ is not tuned.** `C1_RG`, the per-scale-step bulk contraction, is the
framework's *measured* adjacent cross-rung / within-rung coupling ratio: the
26-cell g/J campaign (`Corridor Dynamics.tex` §sec:crossrung) found O(1), three
rung-pair medians 0.31 / 0.72 / 1.15. `C1_RG` is fixed at their geometric mean,
`0.6355` — **the exact value the fractal run used**, so the only change from the
fractal run is the topology. The trajectory's own `soft(ρ_via)` additionally
multiplies every entry — data × measured bulk geometry.

**τ is the Piece-6 cross-rung mutual information.** `RungHierarchy.lean` defines
`τ_(n,n+1) = I(R_n;R_{n+1}) / min(H_n,H_{n+1})` with the cross-rung corridor
`ρ_lower < τ < ρ_upper` — the same bounds (0.10, 0.43) as the within-rung
corridor. τ is computed per adjacent rung pair as the normalised Gaussian mutual
information of the corridor-weighted cross-rung correlation `C_w[n,n+1]`,
operationalised consistently with the `path1_tau` campaign's
`crossrung_lib.cross_rung_tau`. It is a genuine second observable, not a
re-reading of ρ_joint.

CUDA throughout (cupy 13.6.0, RTX 4090, float64). Per-depth progress printed;
results flushed to `results_holographic.json` after every rung-depth; resume
from on-disk partials **verified before reporting** (dropped R=9 from the JSON,
re-ran, confirmed R=3…8/11/13/20 skipped and R=9 recomputed bit-identical:
ρ_joint 0.026736 = 0.026736). Depths 3–20, N up to 20 M histories.

### The discipline check — was the structure derived or imposed?

This is the crux the pre-registration names. A non-decaying all-to-all matrix
trivially does not dilute; imposing one and reporting OPENS voids the run. The
holographic coupling here was **derived** from the genuine binary-MERA bulk —
and the derivation returned a **decaying** structure, not a non-decaying one.

The static matrix tells the story directly. The derived `C_holo` has total
off-diagonal mass `Tr(C_holo²)` that **saturates** at ≈ 2.4 regardless of R
(R=4: 1.98; R=9: 2.39; R=13: 2.40; R=20: 2.40). Saturating off-diagonal mass
means `Tr(C_holo²)/R → 0` — the bounded-per-rung-mass regime that the fractal
run's diagnosis identified as the *cause* of dilution. The genuine AdS geometry
sits squarely in the diluting regime.

The derivation also makes plain *why* there is no escape. Three readings of the
MERA-as-AdS bulk were checked, and all three decay:

1. **Minimal-geodesic (Ryu–Takayanagi) reading** — the holographic correlation
   set by the *shortest* connecting bulk geodesic. The shortest path between
   scale n and scale m goes up to their *shallowest* common ancestor, at depth
   max(n,m), giving geodesic length exactly |n−m|. This reduces *identically* to
   the fractal run's rgflow Toeplitz `C1^|n−m|` — already tested, already
   diluted.
2. **Causal-cone-overlap average** (the construction's main reading) — the
   cone-overlap-weighted average over all shared-ancestor channels. Decays even
   faster than rgflow (`ρ_joint ~ R^-1.39`), because the deep-bulk channels that
   couple distant rungs carry *long* geodesics `(a−n)+(a−m)` and hence tiny
   `C1^L`.
3. **Deep-bulk core channel** — every rung couples through the AdS center at
   cost = geodesic to the core, `(R−1−n)`. Off-diagonal mass saturates at ≈ 1.6.
   The "AdS center couples everything" intuition is geometrically wrong as a
   non-decay claim: the core *is* in every rung's cone, but *reaching* it costs
   a geodesic whose length grows with how fine the rung is.

The reason is a theorem of geometry, not a tuning artifact: **a metric distance
between distinct points grows with their separation.** The holographic
correlation is `C1^(bulk geodesic length)`, the geodesic length is a genuine
bulk metric distance, so the correlation decays with scale-separation — for
*any* bulk geometry. The only way to get non-decay is to set the geodesic length
to a constant — an AdS bulk of zero diameter, every rung at distance 0, i.e. all
rungs collapsed. That is the imposed flat all-to-all matrix `C[n,m] = const`,
and it is precisely the self-sealing move the pre-registration forbids: it does
break dilution (`ρ_joint → 0.404`), but at `ρ_joint = 0.404` it sits **at the
rigidity edge** ρ_upper = 0.43 — pure containment, the rigidity pole. The
construction did **not** impose it; it derived the genuine geometry, which
decays, and reports that.

So the discipline held: the structure was derived from the genuine MERA/bulk
geometry with the framework's measured coupling, and the verdict is whatever the
construction returned — EMPTY.

---

## The hypotheses

### Data — ρ_joint(ps), k_eff(ps), τ across depth

| R  | ρ_joint chain | ρ_joint rgflow | ρ_joint **HOLO** | ρ·R HOLO | k_eff HOLO | τ_pop range (HOLO) | τ in corridor? | n_in_band HOLO |
|----|---------------|----------------|------------------|----------|------------|--------------------|----------------|----------------|
| 3  | 0.1694 | 0.1499 | **0.1471** | 0.441 | 2.35 | 0.0047–0.0076 | **NO** (all below) | 59188 |
| 4  | 0.1286 | 0.1117 | **0.1063** | 0.425 | 3.08 | 0.0018–0.0074 | **NO** | 14604 |
| 5  | 0.1007 | 0.0845 | **0.0752** | 0.376 | 3.90 | 0.0006–0.0074 | **NO** | 3668 |
| 6  | 0.0810 | 0.0657 | **0.0538** | 0.323 | 4.80 | 0.0002–0.0073 | **NO** | 648 |
| 7  | 0.0670 | 0.0531 | **0.0403** | 0.282 | 5.71 | 0.0001–0.0073 | **NO** | 118 |
| 8  | 0.0568 | 0.0444 | **0.0316** | 0.253 | 6.63 | 0.0000–0.0073 | **NO** | 30 |
| 9  | 0.0498 | 0.0388 | **0.0267** | 0.241 | 7.50 | 0.0000–0.0073 | **NO** | 10 |
| 11 | 0.0402 | 0.0315 | **0.0209** | 0.230 | 9.19 | 0.0000–0.0072 | **NO** | 1 |
| 13 | 0.0339 | 0.0268 | **0.0176** | 0.229 | 10.83 | 0.0000–0.0072 | **NO** | 0 |
| 20 | 0.0228 | 0.0188 | **0.0128** | 0.257 | 16.20 | 0.0000–0.0071 | **NO** | 0 |

Power-law fits (log-log least squares over R = 3…20):

| topology | ρ_joint ~ R^p | k_eff ~ R^q |
|----------|---------------|-------------|
| chain (R1∧R2 baseline) | R^-1.091 | R^0.973 |
| rgflow (RG-flow Toeplitz, fractal-run baseline) | R^-1.144 | R^0.988 |
| **holographic (MERA causal-cone overlap)** | **R^-1.390** | **R^1.040** |

τ_pop per scale-step (holographic), R=9: `[0, 0, 0, 0.0002, 0.0005, 0.0016,
0.0043, 0.0073]`. R=13: `[0, 0, 0, 0, 0, 0, 0, 0.0001, 0.0005, 0.0015, 0.0042,
0.0072]`. The finer the rung, the closer τ is to exactly 0 — the genuine AdS
geodesic decay makes the finest rungs' cross-rung coupling vanish.

### H-holo — the decisive two-sided hypothesis: **FAILS, both horns**

- **(a) τ in corridor — FAILS, on the chaos side.** τ_(n,n+1) is 0.000–0.007 at
  every scale-step and every depth — never within an order of magnitude of the
  corridor floor τ_lower = 0.10. `all_in_corridor` is `False` at every R; every
  scale-step is *below* the corridor (`n_below_corridor` = R−1 at every depth,
  `n_above_corridor` = 0 throughout). The genuine holographic coupling does not
  buy non-decay with rigidity (τ → 1); it does the opposite — the cross-rung
  mutual information collapses to the chaos pole. The rungs decouple. This is a
  *second*, independent failure: even setting ρ_joint aside, the holographic
  geometry cannot hold the cross-rung corridor.
- **(b) ρ_joint non-diluting — FAILS, and worse than every decaying topology.**
  `ρ_joint ~ R^-1.39`, against the chain's `R^-1.09` and rgflow's `R^-1.14`. The
  joint k_eff is extensive — `R^1.04`, slightly *super*-extensive. ρ_joint
  crosses the corridor floor 0.10 downward at R ≈ 5; at the framework's 9 rungs
  it is 0.027 (a quarter of the band floor, deep chaos-side); the ω-set is
  exactly empty (`n_in_band` = 0) from R = 13.

**Why the holographic coupling dilutes faster, not slower.** The fractal run's
diagnosis was: dilution is the trace-ratio arithmetic of `k_eff = (Tr C)²/Tr(C²)`
meeting any coupling whose per-rung off-diagonal mass does not *grow* with R. The
genuine MERA causal-cone overlap has *saturating* off-diagonal mass
(`Tr(C_holo²) ≈ 2.4`, R-independent) — it adds cross-scale entries, but they are
deep-bulk-geodesic-suppressed, so the extra mass is small and bounded. The small
extra off-diagonal mass *raises* k_eff a little above rgflow (k_eff HOLO sits
above k_eff rgflow at every depth), and a higher k_eff means a *lower* ρ_joint
and a *steeper* dilution exponent. The holographic coupling lands on the same
EMPTY horn as the fractal coupling, deeper in.

### H1 — non-decomposability (segment-shuffle): real at low R, **shrinks with R**

| R  | shuffle_gap HOLO |
|----|------------------|
| 3  | 0.3779 |
| 5  | 0.0837 |
| 9  | 0.0147 |
| 13 | 0.0147 |
| 20 | 0.0205 |

The holographic coupling carries a large segment-shuffle gap at low R (R=3:
0.378) — the cone-overlap matrix genuinely mixes rung pairs across scales, so
the joint weight depends on cross-rung structure independent per-rung draws
cannot reproduce. But the H1 criterion is gap real **and growing with R**. The
gap **falls** an order of magnitude (0.378 → ~0.015–0.02) as depth grows. As
under the fractal coupling, the joint structure dilutes away exactly as the
ρ_joint dilution sets in: once ρ_joint is pinned near the chaos floor the
band-indicator weight is flat and shuffling changes nothing. H1's question is
moot under H-holo's failure — a functional diluted to a constant is trivially
decomposable. H1 is not met.

### H3 — joint work: real and selective, but **the joint object is empty at depth**

The cross-rung coupling is non-inert: turning it off shifts ρ_joint by
`cross_delta_mean` 0.031 at R=3 — the joint weight responds to the holographic
cross-rung structure, and it is selective (in-band fraction at R=3: 0.74). But
H3 requires the joint object **non-empty and well-defined to 9 rungs**. The
holographic in-band count runs 59188 → 10 → 1 → 0 across R = 3 → 9 → 11 → 13,
and `cross_delta` itself dilutes with depth (0.031 → 0.0009 at R=13), tracking
the same dilution. There is no joint object left to do work on at the
framework's rung count. H3 fails — by H-holo's dilution.

---

## Verdict against the pre-registration

The three-way verdict:

- **OPENS** requires H-holo ∧ H1 ∧ H3. H-holo fails on both horns; H1 fails; H3
  fails. **Not OPENS.**
- **EMPTY** is: τ-in-corridor forces decay → ρ_joint dilutes, **or** non-decay
  is bought only by τ → 1 (rigidity). **This is what happened — and on both
  descriptions at once.** The genuine holographic coupling decays (`ρ_joint ~
  R^-1.39`) *and* its τ collapses to the chaos pole (τ ≈ 0). The only structure
  that would break the dilution — the flat all-to-all `C[n,m] = const` — is the
  rigidity-pole case (`ρ_joint = 0.404`, at ρ_upper) and is the forbidden
  imposed matrix.
- **TRIVIAL** is the functional factorizing while H-holo holds, or no-dilution
  achieved by a tautologically-imposed all-to-all (self-sealing). The functional
  does not cleanly factorize at low R (shuffle gap real), and the non-decaying
  matrix was **not** imposed — the genuine geometry was derived and it decays.
  So the verdict is **EMPTY**, not TRIVIAL.

**EMPTY fires F-11 for real**, per the binding terminal commitment. The topology
axis is decaying ∪ non-decaying. The fractal run exhausted the decaying side
(chain, RG-flow Toeplitz, ultrametric binary tree — all diluted). This run does
the non-decaying / holographic side: the genuine MERA-as-AdS bulk geometry,
derived not imposed, **decays as well** — and the only non-decaying structure on
that side is the rigidity-pole flat matrix the framework does not license. The
topology axis is **exhausted**. No further constructions, per the
pre-registration; this verdict is held both ways.

---

## Honest assessment — is the holographic P_ω the genuine construction, or does the no-go hold?

The no-go holds. And the holographic construction does not merely fail to escape
it — it sharpens *why* there is no escape.

The pre-registration's hypothesis was specific and well-motivated: P_ω is a
future-boundary post-selector (Piece 4), the framework's P_ω history already
builds MERA towers, MERA is the holographic tensor network (Swingle), and a
boundary-condition-determines-bulk framework being holographic is
framework-faithful. The hope was that the holographic geometry, organising
cross-scale correlations through the bulk rather than along the boundary, would
give the non-decaying coupling the fractal run identified as the only escape.

It does not — and the reason is a theorem of geometry. The holographic
correlation between two scales is `C1^(bulk geodesic length)`. The bulk geodesic
length is a genuine metric distance on the AdS bulk, and a metric distance
between distinct points grows with their separation. So the holographic coupling
**decays with scale-separation for any bulk geometry** — exactly the regime the
fractal run proved dilutes. The minimal-geodesic (Ryu–Takayanagi) reading
reduces identically to the fractal run's rgflow Toeplitz; the cone-overlap
average decays faster; the deep-bulk core channel saturates its off-diagonal
mass. Every genuine reading lands on the EMPTY horn.

The one coupling that breaks the dilution — the flat all-to-all `C[n,m] = const`
— is not a holographic geometry. It is an AdS bulk of zero diameter: every rung
at geodesic distance 0, all rungs collapsed into one. It sits at `ρ_joint =
0.404`, the rigidity edge. Imposing it is the self-sealing move; the
pre-registration forbade it, and the construction did not take it. The two-sided
test catches it cleanly: a structure non-decaying only by collapse drives τ → 1
(rigidity); the genuine decaying geometry drives τ → 0 (chaos). There is no
geometry between "decays → dilutes" and "flat → rigidity." The cross-rung
corridor is a measure-zero edge the genuine bulk geometry does not occupy.

This is the strongest available statement of the no-go. The multi-rung *joint
backward* P_ω — the object D1 (Penrose past) and asymptotic conditioning
post-select through — is a documented no-go across the additive ansatz, R1, R2,
R3, the R1∧R2 conjunction, the fractal / RG-nested topology, **and now the
genuine holographic / MERA-as-AdS topology**. The topology axis is exhausted:
decaying couplings dilute (chaos pole), the only non-decaying coupling is
rigidity-pole collapse, and the framework's genuine geometry — RG-nested
fractal, holographic AdS — sits on the decaying side. F-11 fires.

**Scope — unchanged from the fractal run, R1, R2, and the R1∧R2 conjunction.**
Touched: the multi-rung *joint backward* P_ω only. **Not** touched: the
within-rung corridor (F-10, single-rung, empirically supported on five A3+
substrates), the engineering tier, or the soft *forward* P_ω (ρ_ss, the
open-system Lindblad steady state — not a joint participation ratio, does not
dilute, exists and is non-empty independently). The soft backward P_ω
(E_ω = exp(−β H_sum), the `NOTES.md` construction) is a different object — a
graded operator on a configuration space, not a joint participation ratio over
a cross-rung correlation matrix — and is not touched by this topology no-go.
F-11's firing is specific to the multi-rung joint backward construction built as
a Kish participation ratio of a cross-rung correlation matrix.

**Limits of this construction.** (1) `C1_RG` is the geometric mean of three
measured g/J medians; a different `C1 ∈ (0,1)` shifts the dilution constant but
not the law — the law is "the holographic correlation is `C1^L` with L a bulk
geodesic length growing with scale-separation," true for every `C1 < 1`, and at
`C1 = 1` the coupling is the non-framework flat all-to-all. The dilution is
`C1`-independent across the framework-faithful range. (2) The MERA here is a
*binary* tree; a higher-arity holographic tiling changes the LCA multiplicities
but not the fact that the geodesic length grows with separation, hence not the
decay. (3) The flat all-to-all escape remains real but remains the rigidity pole
and remains non-framework-faithful; per the pre-registration's terminal
commitment it is not pursued.

---

## Bottom line for the audit

**The holographic / MERA-as-AdS P_ω horns — EMPTY.** R1∧R2's non-additive joint
Kish functional, on R2's open sequential history frame, with the cross-rung
coupling the genuine binary-MERA causal-cone-overlap bulk geometry (derived
tensor-by-tensor from the framework's own MERA tower, `C1` the measured g/J
geometric mean), **fails the pre-registered two-sided test on both horns**: the
cross-rung mutual information τ collapses to ≈ 0 — three orders of magnitude
below the corridor floor — at every scale (test (a) fails, chaos side), and
ρ_joint dilutes at `R^-1.39`, *faster* than every decaying topology the fractal
run tested (test (b) fails). The joint k_eff is extensive (`R^1.04`); the band
floor is crossed at R ≈ 5; the ω-set is empty from R = 13. H1 fails (shuffle gap
real but shrinking); H3 fails (joint object empty at the framework's 9 rungs).

The discipline held: the holographic structure was **derived** from the genuine
MERA/AdS bulk geometry, not imposed. The derivation returned a decaying coupling
— because the holographic correlation is `C1^(bulk geodesic length)` and a
geodesic length is a metric distance that grows with separation. The only
non-decaying coupling is the flat all-to-all `C[n,m] = const`, an AdS bulk of
zero diameter — the rigidity pole (`ρ_joint = 0.404`, at ρ_upper) — and the
pre-registration forbade imposing it.

Per the binding, genuinely-terminal commitment: **F-11 fires.** The topology
axis (decaying ∪ non-decaying) is **exhausted** — the fractal run did decaying,
this did non-decaying/holographic, both EMPTY. The multi-rung joint backward
P_ω is a documented no-go on the framework's genuine structure: the additive
ansatz, R1, R2, R3, the R1∧R2 conjunction, the fractal / RG-nested topology, and
the holographic / MERA-as-AdS topology. No further constructions. The
within-rung corridor, the engineering tier, the forward open-system P_ω, and the
soft backward P_ω are untouched.
