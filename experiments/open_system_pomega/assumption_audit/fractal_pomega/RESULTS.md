# P_ω — the fractal / RG-nested construction — results

**Date:** 2026-05-22. **Falsification handle:** F-11 / F-12.
**Pre-registration:** `fractal_pomega/PREREGISTRATION.md` (committed before this
run). **Build:** `build_fractal_pomega.py` (reuses `build_history_pomega.py`,
R2's sequential-emergence simulator, via `../R1xR2_conjunction/`).
**Raw:** `results_fractal.json`, `run_fractal.log`.

---

## VERDICT: EMPTY — H2′ fails (the joint functional dilutes under the genuine RG-nested coupling)

The fractal construction — R1's non-additive joint Kish participation-ratio
functional, on R2's open sequential history-space frame, with the cross-rung
coupling replaced by the framework's genuine **RG-nested / fractal** topology
(Piece 6, the MERA binary nesting tree) — **horns EMPTY**.

`ρ_joint` runs to the chaos pole with depth under the RG-nested coupling
**exactly as it did under the chain**. The chain gave `ρ_joint ~ R^-1.09`; the
RG-flow coupling gives `R^-1.14`, the ultrametric binary-tree coupling gives
`R^-1.17` — the dilution is **not broken; it is marginally steeper**. The joint
`k_eff` is fully **extensive** (`~ R^0.97-0.99`) for all three topologies. The
pre-registered decisive hypothesis H2′ — that the fractal coupling gives a
power-law spectrum, sub-extensive k_eff, bounded `ρ_joint` — is **refuted**.

Per the binding terminal commitment in the pre-registration: **F-11 fires for
real.** The RG-nested / fractal topology is the framework's *actual* rung
topology — there is no more-faithful topology to test. The no-go now holds for
the framework's genuine structure, not a 1D-chain artifact.

Reported flat, per the pre-registration. EMPTY is a valid two-sided result.

---

## The construction

**Frame (from R2), reused unchanged.** `build_history_pomega.py` — universe
trajectories, rungs Ph0…A5 emerging sequentially over cosmic time, each rung's
within-rung ρ_n(t) evolving by Piece 2 dynamics `dρ/dt = α − γM`, held in its
corridor by active management. The all-emerged sub-ensemble is what the
post-selection acts on. Identical module to the R1∧R2 conjunction.

**Functional (from R1∧R2), reused verbatim.** `ρ_joint` = the Kish-inverse of
the participation ratio `(Tr C_w)² / Tr(C_w²)` of the corridor-weighted R×R
rung-correlation matrix `C_w = D C D`, `D = diag(√w_n)`, `w_n = soft(ρ_n at
t_f)`. Constituents are the R corridor-capped rungs. Piece 1 (Kish), the
participation-ratio reading of k_eff, Piece 3 (the band). Nothing invented; the
functional was not re-chosen.

**The one fix — the cross-rung coupling topology.** The chain set `C_w[n,m] = 0`
for `|n-m| > 1`. The framework's rungs are not a 1D chain: Piece 6 builds them
as RG coarse-grainings, and the P_ω history (`construct_p_omega_mera.py`) built
MERA isometry towers — rung n+1 is block-decimated *from* rung n, so the rungs
are the leaves of a binary nesting tree and every higher rung contains the
lower ones. Two genuine RG-nested topologies were built, both reported:

- **rgflow (RG-flow Toeplitz):** `C[n,m] ∝ c₁^|n-m|`. Scale-distance k ↔ k
  coarse-graining steps ↔ a self-similar contraction `c₁^k` (RG composition is
  multiplicative; the same RG factor at every step).
- **ultrametric (binary nesting tree):** `C[n,m] ∝ c₁^treedist(n,m)`, where the
  tree distance is the depth of the lowest common ancestor on the MERA binary
  tree (`treedist = bitlength(n XOR m)`). This is the genuine hierarchical /
  fractal structure: rungs sharing a recent common coarse-graining are strongly
  coupled, rungs whose common ancestor is deep are weakly coupled.

In both, the per-pair coupling was the trajectory's own cross-rung correlation
(`soft(ρ_via)`, exactly as R1∧R2 read the adjacent entry — for a non-adjacent
pair, the geometric mean of the spanned-bond couplings) multiplied by the
RG-nesting decay template, then corridor-weighted by `C_w = D C D`. The chain
topology was recomputed in the same run as the in-run baseline.

**c₁ is not tuned.** The per-scale RG contraction `c₁` is the framework's
*measured* adjacent cross-rung / within-rung coupling ratio: the 26-cell g/J
campaign (`Corridor Dynamics.tex` §sec:crossrung) found O(1), with three
rung-pair medians 0.31 / 0.72 / 1.15. `c₁` was fixed at the geometric mean of
those three measured medians, `c₁ = 0.6355`, before the run; it was not swept.
The trajectory's own `soft(ρ_via)` additionally multiplies every entry, so the
coupling carried into the matrix is data × measured geometry. The pre-
registration's self-sealing check (stop if c₁ must be chosen to manufacture a
bounded ρ_joint) did not trigger — c₁ is the measured value and the verdict is
whatever the construction returned.

CUDA throughout (cupy 13.6.0, RTX 4090, float64). Per-depth progress printed;
results flushed to `results_fractal.json` after every rung-depth; resume from
on-disk partials **verified before the long run** (dropped R=4 from the JSON,
re-ran, confirmed R=3 skipped and R=4 recomputed bit-identical). Depths 3–20,
N up to 20 M histories; total runtime 842 s.

**Bug found and fixed before the reported run.** A first run mis-signed the
log-cumsum used for the multi-bond geometric mean (`+|span|` instead of
`-|span|`), inflating non-adjacent entries. It was caught by the joint-work
diagnostic returning absurd values (`~1e22`), the geommean was corrected to be
a genuine mean in (0,1], and the **entire scan was re-run from scratch**. The
corrected chain row reproduces the R1∧R2 conjunction's published table
exactly (R=3: ρ_joint 0.1694, shuffle_gap 0.1071, in-band 0.7359; R=9: ρ_joint
0.0498, n_in_band 61; R=13/20 in-band 0) — a direct cross-check that the
construction is faithful and the only change from R1∧R2 is the topology.

---

## The three hypotheses

### Data — ρ_joint(ps) and k_eff(ps) across depth, three topologies

| R  | ρ_joint chain | ρ_joint rgflow | ρ_joint ultra | ρ·R chain | ρ·R rgflow | ρ·R ultra | k_eff chain | k_eff rgflow | k_eff ultra |
|----|---------------|----------------|---------------|-----------|------------|-----------|-------------|--------------|-------------|
| 3  | 0.1694 | 0.1499 | 0.1486 | 0.508 | 0.450 | 0.446 | 2.26 | 2.34 | 2.34 |
| 4  | 0.1286 | 0.1117 | 0.1101 | 0.515 | 0.447 | 0.440 | 2.91 | 3.03 | 3.05 |
| 5  | 0.1007 | 0.0845 | 0.0812 | 0.504 | 0.423 | 0.406 | 3.60 | 3.78 | 3.82 |
| 6  | 0.0810 | 0.0657 | 0.0622 | 0.486 | 0.394 | 0.373 | 4.31 | 4.56 | 4.63 |
| 7  | 0.0670 | 0.0531 | 0.0499 | 0.469 | 0.372 | 0.349 | 5.03 | 5.36 | 5.44 |
| 8  | 0.0568 | 0.0444 | 0.0427 | 0.454 | 0.355 | 0.341 | 5.77 | 6.16 | 6.22 |
| 9  | 0.0498 | 0.0388 | 0.0364 | 0.449 | 0.350 | 0.327 | 6.48 | 6.92 | 7.03 |
| 11 | 0.0402 | 0.0315 | 0.0291 | 0.442 | 0.346 | 0.320 | 7.90 | 8.43 | 8.58 |
| 13 | 0.0339 | 0.0268 | 0.0252 | 0.440 | 0.349 | 0.328 | 9.30 | 9.90 | 10.05 |
| 20 | 0.0228 | 0.0188 | 0.0182 | 0.455 | 0.376 | 0.364 | 14.03 | 14.82 | 14.95 |

Power-law fits (log-log least squares over R = 3…20):

| topology | ρ_joint ~ R^p | k_eff ~ R^q |
|----------|---------------|-------------|
| chain (R1∧R2 baseline) | **R^-1.091** | R^0.973 |
| rgflow (RG-flow Toeplitz) | **R^-1.144** | R^0.988 |
| ultrametric (binary nesting tree) | **R^-1.166** | R^0.992 |

### H2′ — no dilution under the RG-nested coupling (DECISIVE): **FAILS**

This is the pre-registered decisive hypothesis: the chain gave `ρ_joint ~
1/count → 0`; H2′ is that the fractal coupling gives a power-law correlation
spectrum, a **sub-extensive** k_eff, and a **bounded** ρ_joint off the chaos
pole to the framework's 9 rungs and beyond.

It fails, decisively and in the opposite direction to the hypothesis:

- **The dilution law is unchanged.** The chain reproduces R1∧R2's
  `ρ_joint ~ R^-1.09` to two decimals (`R^-1.091`). The RG-flow coupling gives
  `R^-1.144`; the ultrametric binary-tree coupling gives `R^-1.166`. The
  RG-nested topologies do **not** break the `1/R` law — they dilute *slightly
  faster* than the chain.
- **k_eff is extensive, not sub-extensive.** `k_eff ~ R^0.97–0.99` for all
  three topologies — to within fit error, exactly linear in R. H2′ predicted
  sub-extensive (`q < 1`) k_eff; the measured `q ≈ 0.99` for the fractal
  topologies is *more* extensive than the chain's `q ≈ 0.97`, not less.
- **The band floor is crossed before the framework's 9 rungs.** `ρ_joint(ps)`
  crosses the corridor lower edge 0.10 downward at R ≈ 5 for the chain and at
  R ≈ 4–5 for both fractal topologies — *earlier* under the RG-nested coupling.
  At the framework's 9 rungs `ρ_joint(ps)` is 0.050 / 0.039 / 0.036
  (chain / rgflow / ultra) — all roughly half the band floor, chaos-side.
- **The ω-set is empty at depth.** In-band fraction at R=9 is 0.0022 / 0.0008 /
  0.0007; the band-reachability extreme (any in-band history at all) holds only
  to R = 11 for all three and is exactly 0 from R = 13 — before and past the
  framework's 9 rungs.

**Why the fractal coupling makes it worse, not better.** The pre-registration's
H2′ rested on the intuition that a hierarchical coupling gives a power-law
*correlation spectrum* and hence a sub-extensive participation ratio. The
arithmetic of `k_eff = (Tr C_w)²/Tr(C_w²)` does not work that way. Adding
cross-scale entries (rgflow: every rung gains a partner at every scale;
ultrametric: every rung gains partners through every common ancestor)
*increases* the off-diagonal mass of `C_w` — and that mass scales **with R**,
because each of the R rungs carries it. So `Tr(C_w²) = Σ_{n,m} C_w[n,m]²` still
grows ∝ R, `k_eff` stays linear in R, and `ρ_joint = (R/k_eff − 1)/(R−1) ~
const/R → 0`. The extra off-diagonal mass *raises* k_eff a little (the fractal
k_eff sits above the chain k_eff at every depth), which is exactly why the
fractal ρ_joint is *lower* and the dilution exponent slightly *steeper*. The
chaos-pole dilution is the trace-ratio structure of the Kish participation
ratio meeting **any** coupling whose per-rung off-diagonal mass does not *grow*
with R — and an RG-nested coupling, like a chain and like a generic all-to-all
template, has bounded per-rung off-diagonal mass. The geometric / ultrametric
decay makes the per-rung mass converge to a finite constant; only a per-rung
off-diagonal mass that itself *grows* with R would hold ρ_joint off the floor,
and no self-similar topology delivers that. (R1's all-to-all control did not
dilute precisely because its off-diagonal entries were O(1) at every distance —
*no* decay — so the per-rung mass grew with R. That is the non-framework
topology Piece 6 explicitly does not license: the framework's coupling is
adjacency-dominated with a cross-rung corridor, i.e. it decays with
scale-distance, which is exactly the regime that dilutes.)

### H1 — non-decomposability (segment-shuffle): real at low R, **shrinks with R**

| R  | shuffle_gap chain | rgflow | ultrametric |
|----|-------------------|--------|-------------|
| 3  | 0.1071 | 0.3034 | 0.3775 |
| 5  | 0.0692 | 0.0752 | 0.0882 |
| 9  | 0.0500 | 0.0370 | 0.0303 |
| 13 | 0.0458 | 0.0198 | 0.0176 |
| 20 | 0.0355 | 0.0170 | 0.0188 |

The fractal coupling carries a **larger** segment-shuffle gap than the chain at
low R — markedly so (R=3: ultrametric 0.378 vs chain 0.107, 3.5×). The RG-nested
matrix mixes rung pairs at every scale, so the joint weight genuinely depends on
cross-rung structure that independent per-rung draws cannot reproduce; this is
real joint structure and it is *stronger* under the fractal coupling than the
chain. But the H1 criterion is gap **real and growing with R**. The gap **falls
monotonically** with depth — for the fractal topologies it falls an order of
magnitude (ultrametric 0.378 → 0.018). The non-additive functional does carry
joint structure the shuffle destroys, more than R2's additive weight whose gap
was ≈ 0 — but that structure **dilutes away exactly as H2′'s dilution sets in**.
Once ρ_joint is pinned near the chaos floor, the band-indicator weight is flat
(its argument is far below the band), every history scores the same near-zero
weight, and shuffling changes nothing. H1's question is moot under H2′'s
failure: a functional diluted to a constant is trivially decomposable. H1 is
not met (gap real but shrinking, like R1∧R2's).

### H3 — joint work: real and selective, but **the joint object is empty at depth**

The cross-rung coupling is non-inert: turning it off (cross entries → 0) shifts
ρ_joint by `cross_delta_mean` 0.085 / 0.040 / 0.031 at R=3 (chain / rgflow /
ultra) — the joint weight genuinely responds to the cross-rung structure, and
the fractal topologies are selective (in-band fraction at R=3: 0.74 / 0.41 /
0.37, a narrow target). But H3 requires the joint object **non-empty and
well-defined to 9 rungs**. In-band fraction at R=9 is 0.0022 / 0.0008 / 0.0007
(effectively zero) and exactly 0 from R=13. `cross_delta` itself dilutes with
depth (0.085 → 0.011), tracking the same `1/R` decay. There is no joint object
left to do work on at the framework's rung count. H3 fails — by H2′'s dilution.

---

## Verdict against the pre-registration

The three-way verdict:

- **OPENS** requires H2′ ∧ H1 ∧ H3. H2′ fails (decisively); H1 fails; H3 fails.
  Not OPENS.
- **EMPTY** is ρ_joint diluting even under the genuine RG-nested coupling.
  **This is what happened.** `ρ_joint ~ R^-1.14` (rgflow) and `R^-1.17`
  (ultrametric), against the chain's `R^-1.09` — the dilution law is unchanged
  and the band floor is crossed before the framework's 9 rungs.
- **TRIVIAL** is the functional factorizing while H2′ holds. The functional does
  *not* cleanly factorize at low R (the shuffle gap is real, larger than the
  chain's), but H2′'s dilution is the primary, decisive failure — the shuffle
  gap is moot once the functional has diluted to a constant. The verdict is
  **EMPTY**.

**EMPTY fires F-11 for real**, per the binding terminal commitment. This
construction used the framework's *actual* rung topology — RG-nested / fractal,
the MERA binary nesting tree of Piece 6. There is no more-faithful topology to
test: fractal / RG-nesting is what the framework's rung hierarchy *is*. The
no-go now holds for the framework's genuine structure, not a 1D-chain artifact.

---

## Honest assessment — is the fractal construction the genuine P_ω, or does the no-go hold?

The no-go holds. And it holds on the framework's real structure.

The pre-registration's hypothesis was specific and falsifiable: the chain's
`ρ_joint ~ 1/count` dilution is a **locality artifact** — each constituent has
O(1) partners — and the framework's genuine RG-nested coupling, giving partners
at every scale, would give a power-law correlation spectrum, a sub-extensive
k_eff, and a bounded ρ_joint. That hypothesis is **refuted**. The RG-nested
coupling gives partners at every scale, yes — but with a *decay*, and a decaying
cross-scale coupling has bounded per-rung off-diagonal mass, exactly like a
chain. The participation ratio of such a matrix is extensive; ρ_joint dilutes.
The fractal coupling did not change the *law*; it changed the *constant*
slightly in the unfavourable direction (more off-diagonal mass → higher k_eff →
lower ρ_joint → marginally steeper dilution).

The diagnosis is now sharp and topology-independent. The chaos-pole dilution is
**not** specific to additivity (R2), nor to raw-constituent indexing (R1), nor
to nearest-neighbour locality (the chain) — it is the trace-ratio arithmetic of
`k_eff = (Tr C)²/Tr(C²)` meeting **any cross-rung coupling whose per-rung
off-diagonal mass does not grow with the rung count**. A 1D chain has bounded
per-rung mass (two neighbours). An RG-flow Toeplitz coupling has bounded
per-rung mass (`Σ_k c₁^{2k}` converges). An ultrametric binary-tree coupling has
bounded per-rung mass (the tree-distance spectrum is summable). All three
dilute. The *only* coupling that does not — R1's all-to-all control, every
entry O(1), no decay — has per-rung mass growing with R, and that coupling is
**not framework-faithful**: Piece 6 defines the cross-rung coupling τ_(n,n+1)
as adjacency-structured with its own corridor, and the 26-cell g/J campaign
measured it decaying as the substrate gets finer-grained. A coupling with no
scale-decay is not the framework's rung topology; it is the negation of Piece 6.

So the framework is caught in a genuine pincer. Its rung hierarchy is, by Piece
6, an RG-nested structure with a cross-rung coupling that decays with
scale-distance (the cross-rung corridor, the measured O(1)-and-falling g/J). A
decaying coupling gives an extensive joint participation ratio, hence a
diluting ρ_joint, hence an empty multi-rung backward P_ω at the framework's 9
rungs. The only escape — an all-to-all non-decaying coupling — is the one
topology the framework explicitly does not license. The fractal construction
the audit built specifically to escape the chain artifact lands on the EMPTY
horn, holding every framework constraint, on the framework's actual topology.

This is the strongest available statement of the no-go. The multi-rung *joint
backward* P_ω — the object D1 (Penrose past) and asymptotic conditioning
post-select through — is a documented no-go across the additive ansatz, R1, R2,
R3, the R1∧R2 conjunction, **and now the genuine RG-nested / fractal topology**.
The no-go is not a 1D-chain artifact. F-11 fires.

**Scope — unchanged from R1, R2, and the R1∧R2 conjunction.** Touched: the
multi-rung *joint backward* P_ω only. **Not** touched: the within-rung corridor
(F-10, single-rung, empirically supported on five A3+ substrates), the
engineering tier, or the soft *forward* P_ω (ρ_ss, the open-system Lindblad
steady state — not a joint participation ratio, does not dilute, exists and is
non-empty independently). F-11's firing is specific to the multi-rung joint
backward construction, the universal-scale tier's open formal step. v2's
§sec:open-research records the no-go.

**Limits of this construction.** (1) c₁ is the geometric mean of three measured
g/J medians; a different c₁ in (0,1) shifts the dilution constant but not the
law (the law is "bounded per-rung off-diagonal mass" — true for every c₁ < 1,
and at c₁ = 1 the coupling is the non-framework all-to-all). The dilution is c₁-
independent across the framework-faithful range. (2) The ultrametric tree is a
*binary* nesting tree; a higher-arity RG tree changes the multiplicities in the
tree-distance spectrum but not its summability, hence not the extensivity of
k_eff. (3) The all-to-all escape remains real but remains non-framework-
faithful, and per the pre-registration's terminal commitment it is not pursued:
the framework's own topology has been tested, and the line is drawn here.

---

## Bottom line for the audit

**The fractal / RG-nested P_ω horns — EMPTY.** R1∧R2's non-additive joint Kish
functional, on R2's open sequential history frame, with the cross-rung coupling
replaced by the framework's genuine RG-nested topology (Piece 6's MERA binary
nesting tree — both the RG-flow Toeplitz and the ultrametric tree forms),
dilutes to the chaos pole **exactly as the chain did**: `ρ_joint ~ R^-1.14` to
`R^-1.17` against the chain's `R^-1.09`, joint k_eff extensive (`~R^0.99`), band
floor crossed at R ≈ 4–5, ω-set empty from R = 13. The pre-registered decisive
hypothesis H2′ — that the fractal coupling breaks the `1/R` dilution law — is
refuted: the RG-nested coupling dilutes if anything *faster* than the chain,
because a scale-decaying coupling has bounded per-rung off-diagonal mass and an
extensive participation ratio, like any local coupling. H1 fails (shuffle gap
real but shrinking with R); H3 fails (joint object empty at the framework's 9
rungs).

Per the binding, genuinely-terminal commitment in the pre-registration:
**F-11 fires.** The fractal/RG-nesting topology is the framework's actual rung
topology — there is no more-faithful topology to test. The multi-rung backward
P_ω is a documented no-go on the framework's genuine structure: the additive
ansatz, R1, R2, R3, the R1∧R2 conjunction, and the RG-nested fractal
construction. No further constructions. The within-rung corridor, the
engineering tier, and the forward open-system P_ω are untouched.
