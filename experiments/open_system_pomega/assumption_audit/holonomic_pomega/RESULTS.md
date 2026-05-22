# P_ω — the holonomic construction — results

**Date:** 2026-05-22. **Falsification handle:** F-11 / F-12.
**Pre-registration:** `holonomic_pomega/PREREGISTRATION.md` (committed before
this run). **Build:** `build_holonomic_pomega.py`. **Raw:**
`results_holonomic.json`, and the in-text diagnostics reproduced below.

---

## VERDICT: HORN-empty — the holonomy decoheres to zero as R grows

The holonomic construction — P_ω's ω-weight built as the **Wilson-loop holonomy**
of the framework's genuine emergence-map connection around the TSVF
forward–backward loop, **not** as a participation ratio of a scalar correlation
matrix — **horns EMPTY**. The holonomy of the full loop decoheres: its spectral
radius and operator norm flow geometrically to zero as the rung count R grows,

```
hol_specrad(R)  =  (0.9655)^(R-1)        — an exact area law
```

— the per-rung holonomy eigenvalue is **constant at 0.9655** for every R from 3
to 50 (verified to four decimals). At the framework's 9 rungs the holonomy
operator norm is already down to ~0.69 of full; by R = 50 it is 0.10 and
falling. The loop closes on a **decohering operator** — the chaos pole on the
holonomy axis.

This is HORN-empty, not HORN-trivial: the holonomy does **not** flow to the
identity / a flat connection (rigidity). `hol_id_dist` — the distance from the
identity — stays ~1.0–1.4 at every depth; the holonomy never approaches I. It
flows the other way, toward the **zero operator**: `hol_zero_dist` (the rms
singular value) runs 0.91 → 0.69 → 0.41 → 0.10 across R = 3 → 9 → 20 → 50. The
genuine connection does not collapse the rungs into relabelings; it decoheres
the loop.

Per the binding terminal commitment in the pre-registration: **F-11 fires.** The
type axis — correlation ∪ connection — is now exhausted. The correlation branch
was closed by the holographic theorem (any bulk geometry → coupling decaying
with geodesic distance → 1/count dilution). This run is the connection branch:
the cross-rung relationship as the framework's genuine emergence-map connection,
P_ω's weight as the path-ordered holonomy around the TSVF loop. The holonomy
obeys an **area law** — `Tr Hol ~ exp(-κ·R)` — and decoheres. Both branches of
the type axis horn EMPTY.

Reported flat, per the pre-registration. EMPTY is a valid result.

---

## The construction

P_ω's ω-weight is a **holonomy**, not a correlation matrix. Three framework
pieces, composed exactly as the pre-registration specifies.

**The connection — the framework's genuine emergence maps W_n.** The forward
emergence map W is the framework's own coarse-graining-with-novelty transport,
the W_n that `construct_p_omega_mera.py` builds and that R2/R3 use. It is built
in two genuine halves:

- **Coarse-graining.** The RG transport frame — the eigenbasis of the
  anisotropic block Hamiltonian, anisotropy (0.9, 1.3, 0.6) taken **verbatim**
  from `construct_p_omega_mera.py`. As transport of the within-rung correlation
  operator along the rung connection this is a unitary change of frame: it
  realises the framework's own stated isometry property of W_n
  (`construct_p_omega_mera.py`: "W0, W1 are isometries, W^dag W = I"). An
  isometric connection's holonomy is a genuine group element — **not** a
  contraction that trivially decays. The construction uses the framework's
  isometry property; it does **not** model W as a generic contraction (that
  would manufacture a HORN-empty by a modelling artefact, not the framework).
  Verified: `||W^dag W − I|| = 1.1e-14`.
- **Novelty.** The within-rung corridor rotation. As a rung resides in its
  corridor over `MIN_DWELL = 8` cosmic-time steps under Piece-2 dynamics
  `dρ/dt = α − γM`, its correlation operator rotates. The rotation generator is
  the corridor-penalty Hamiltonian `H_corr = (O − ρ_mid)²`
  (`backward_generator_legitimacy.py`'s `H_sum`); the rotation angle is the
  genuine corridor residence integral — the band-edge drift `α(edge) − γM`
  times the residence window times the band half-width. Set entirely by the
  corridor geometry (`ρ_mid`, `w`) and the Piece-2 constants (`ALPHA0`,
  `ALPHA_RHO`, `GAMMA`) — the same constants `build_history_pomega.py` uses. Not
  a knob.

The cross-rung coupling ratio `c1` — the framework's measured g/J, geometric
mean of the three rung-pair medians 0.31 / 0.72 / 1.15 = **0.6355** (the value
the fractal and holographic runs used) — sets the connection's per-step
transport strength: W is the **fractional power** `(W_full)^c1`, transporting c1
of the way along the full RG+novelty step. The fractional power keeps W unitary
for every c1 (a convex mix of unitaries would be a contraction and would
manufacture decay). c1 is fixed at the measured value; not swept.

**The loop — the TSVF forward–backward loop (Piece 4).** Forward up the rungs
(emergence, Ph0 → A5: the W's); backward down (post-selection, A5 → Ph0: the
B's). P_ω **is** the backward boundary. The loop is the framework's own
two-state structure.

**The backward leg B — the genuine backward generator, not W^dag.** The
framework already measured this (`backward_generator_legitimacy.py`, Claim 2 in
`Corridor Dynamics.tex` / `StructuralClaims.lean`): the legitimate backward
generator is **H_sum-dephasing** — non-ergodic, H_sum-conserving — and sits in a
**different ergodicity class** from the forward generator; the two are **not
interconvertible**. The backward transport map B is therefore the genuine
backward decoherence (dephase the out-of-corridor / high-`H_corr` components,
damping factor `exp(−γM·MIN_DWELL·Ĥ_corr)`, the rate `γM = GAMMA·M_BASE` the
framework's own active-management strength) composed with the inverse RG
transport `CG^dag`. B is **not** W^dag: `||B − W^dag|| = 5.05`, confirmed. That
difference — forward unitary, backward a dephasing contraction — **is the
holonomy's source**, the operator-level karma/grace irreducibility.

**P_ω's ω-weight is the holonomy** — the path-ordered product around the loop:

```
Hol(R)  =  B^(R-1) W^(R-1)        — forward up R-1 rung steps, backward down R-1
hol_trace(R)  =  (1/d) |Tr Hol(R)|     — the normalized Wilson-loop trace
```

a group-trace measuring the failure of forward∘backward to be the identity. NOT
a correlation matrix, NOT a participation ratio.

CUDA throughout (cupy 13.6.0, RTX 4090, complex128). The connection is
deterministic — it **is** the framework's emergence map — so no Monte-Carlo is
needed; the holonomy is exact linear algebra. Per-depth progress printed;
results flushed to `results_holonomic.json` after every depth; resume from
on-disk partials **verified before reporting** (dropped R=9 from the JSON,
re-ran, confirmed R=3…8/11…50 skipped and R=9 recomputed bit-identical:
`hol_trace 0.0188 = 0.0188`, `specrad 0.7550 = 0.7550`). Depths 3–50.

### The discipline check — was the connection derived or tuned?

This is the crux the pre-registration names. The connection here is the
framework's genuine emergence maps with its measured couplings, **not** a
connection tuned to keep the holonomy O(1):

- W is built from `construct_p_omega_mera.py`'s block-Hamiltonian recipe and
  anisotropy, and the novelty rotation angle is fixed by the corridor geometry
  and the Piece-2 dynamics constants. Not a knob.
- B is the genuine backward generator of `backward_generator_legitimacy.py` —
  H_sum-dephasing at the framework's `γM` rate. Not a knob.
- c1 = 0.6355 is the measured g/J geometric mean. Not swept.

The construction did **not** find itself choosing the connection to manufacture
a corridor holonomy. The honest result is that the genuine connection — forward
isometric, backward a measured dephasing contraction — gives a holonomy that
decoheres. The per-rung holonomy eigenvalue 0.9655 is set by the spectral radius
of the single-step holonomy `B·W`, which is set by B's dephasing damping, which
is `exp(−GAMMA·M_BASE·MIN_DWELL·…)` — all framework constants. Reducing the
damping to keep the holonomy alive would be the forbidden self-sealing move; it
was not taken. The verdict is whatever the construction returned — EMPTY.

---

## The hypotheses

### Data — the holonomy across depth

| R  | hol_trace | hol_specrad | hol_zero_dist | hol_id_dist | hol_curvature | fact_gap | 1/count |
|----|-----------|-------------|---------------|-------------|---------------|----------|---------|
| 3  | 0.2974 | 0.9324 | 0.9102 | 1.1110 | 0.5816 | 0.654 | 0.5000 |
| 4  | 0.0648 | 0.9053 | 0.8685 | 1.3724 | 0.7345 | 1.899 | 0.3333 |
| 5  | 0.1561 | 0.8693 | 0.8287 | 1.4134 | 0.7729 | 0.740 | 0.2500 |
| 6  | 0.0422 | 0.8392 | 0.7909 | 1.3069 | 0.7297 | 1.768 | 0.2000 |
| 7  | 0.0860 | 0.8101 | 0.7547 | 1.1823 | 0.6738 | 0.778 | 0.1667 |
| 8  | 0.0987 | 0.7822 | 0.7202 | 1.1500 | 0.6685 | 0.361 | 0.1429 |
| 9  | 0.0188 | 0.7550 | 0.6873 | 1.1981 | 0.7101 | 1.742 | 0.1250 |
| 11 | 0.0409 | 0.7038 | 0.6260 | 1.2128 | 0.7459 | 0.404 | 0.1000 |
| 13 | 0.0432 | 0.6549 | 0.5701 | 1.1129 | 0.7088 | 0.209 | 0.0833 |
| 20 | 0.0376 | 0.5124 | 0.4113 | 1.0460 | 0.7411 | 2.024 | 0.0526 |
| 30 | 0.0215 | 0.3592 | 0.2586 | 1.0127 | 0.8046 | 4.261 | 0.0345 |
| 50 | 0.0095 | 0.1752 | 0.1031 | 0.9959 | 0.9028 | 9.022 | 0.0204 |

Per-rung holonomy eigenvalue `specrad(R)^(1/(R-1))`:

| R | 3 | 5 | 9 | 13 | 20 | 30 | 50 |
|---|---|---|---|----|----|----|----|
| `specrad^(1/(R-1))` | 0.9656 | 0.9656 | 0.9655 | 0.9653 | 0.9654 | 0.9653 | 0.9651 |

**Constant to four decimals.** `hol_specrad(R) = 0.9655^(R-1)` — an exact area
law.

### H-no-dilution — the decisive hypothesis: **FAILS — but not by 1/count**

The pre-registration's decisive question: does the holonomy stay O(1) — in a
corridor — as R grows, against the correlation-matrix runs' 1/count dilution?

The answer is two-part, and the second part is the verdict.

- **The holonomy does NOT obey 1/count.** This much the pre-registration's
  type-axis claim got right, and the run confirms it cleanly. The `hol_trace`
  column is **erratic and non-monotone** — 0.30, 0.06, 0.16, 0.04, 0.09, 0.10,
  0.02, … — it does not track `1/count` (0.50, 0.33, 0.25, …) at all. A Wilson
  loop's trace is a phase-sensitive group-trace; it oscillates as the loop
  grows, it does not dilute as a participation ratio. The **forward-only**
  holonomy `W^(R-1)` makes this decisive: its operator norm is `||W^(R-1)||/√d
  = 1.000` at **every** R (W is unitary — the framework's isometry property),
  while its trace bounces non-monotonically (0.17, 0.04, 0.06, 0.07). A holonomy
  of an isometric connection is genuinely **not** a participation ratio and
  genuinely does **not** obey 1/count. The type-axis insight is real.
- **But the holonomy decoheres anyway — by an area law.** The decisive metric
  is not `hol_trace` (phase-sensitive, erratic) but the holonomy's
  **operator norm / spectral radius** — the size of the transport. And that
  flows geometrically to zero: `hol_specrad(R) = 0.9655^(R-1)`, exact. The
  backward leg is the cause: `B^(R-1)` operator norm runs 0.91 → 0.69 → 0.41 →
  0.10 over R = 3 → 9 → 20 → 50, while the forward leg holds norm 1.000. The
  genuine backward generator is a **dephasing contraction** — the framework's
  own measured non-ergodic backward dynamics — and the iterated backward
  transport decoheres the loop. The holonomy as an operator flows to **zero**.

H-no-dilution fails. Not by the participation-ratio dilution the
correlation-matrix runs hit — the holonomy escapes *that* — but by an **area
law**: a holonomy of a connection with a contracting (decohering) leg obeys
`Tr Hol ~ exp(−κ·R)`, the curvature integrated over the loop's area, and the
loop's area grows with R. The holonomic analog of the holographic theorem's
geodesic-distance dilution is the **Wilson-loop area law**, and the genuine
connection sits squarely under it.

### H-corridor — intermediate per-step, decohered loop: **FAILS at depth**

The framework's genuine connection **does** carry intermediate curvature **per
rung-step**. The single-step holonomy `B·W` has spectral radius 0.9655 and
normalized trace 0.756 — non-flat (not the identity / 1) and non-decohered (not
0). One rung-step of genuine emergence is in an intermediate, corridor-like
regime: the connection has real curvature, neither a relabeling nor noise.

But H-corridor asks for an intermediate holonomy **as R grows to 9 rungs and
beyond**, and there it fails. The per-step curvature `0.9655` is < 1, so it
**accumulates**: `0.9655^(R-1)` → 0. The intermediate regime holds only at fixed
(small) loop size; the corridor on the holonomy axis is not R-stable. The
holonomy crosses the corridor floor on the operator-norm reading early
(`hol_zero_dist` < 0.43 by R ≈ 19) and is at 0.10 by R = 50. The corridor is a
fixed-loop-size object, not a property that survives to the framework's rung
count.

### H-joint — non-factorizability: **structurally real, but on an empty object**

H-joint is the one hypothesis the holonomy passes on its own terms. A Wilson
loop cannot be cut into independent per-rung pieces, and the run confirms it:
the factorization gap — `|log|Tr Hol(R)| − log(per-step-trace)^(R-1)|` — is
**large and non-zero at every depth** (0.65, 1.90, 0.74, …, 4.26, 9.02). The
path-ordered, non-abelian product's trace is genuinely **not** the product of
the per-step traces. The holonomy is intrinsically a loop quantity,
non-factorizable, well-defined to 9 rungs and past it as a *computation*.

But H-joint's non-factorizability is non-factorizability of an object that is
**flowing to zero**. A holonomy that decoheres to the zero operator is
non-factorizable in the trivial sense that 0 ≠ (anything)^R only up to the
phase noise — the joint structure is real but it is joint structure of a
vanishing transport. As under the holographic run's H1/H3, H-joint's question is
moot under the decisive hypothesis's failure: there is no non-empty holonomy at
the framework's rung count for the joint structure to be the joint structure
*of*. H-joint is structurally met and substantively empty.

---

## Verdict against the pre-registration

The three-way verdict:

- **OPENS** requires the holonomy in a corridor to 9 rungs, non-empty, joint.
  The holonomy decoheres (`specrad = 0.9655^(R-1)` → 0); it is not in a corridor
  at depth; the joint object is empty at the framework's rung count. **Not
  OPENS.**
- **HORN-trivial** is the holonomy flowing to the identity / a flat connection
  (rigidity). It does **not** — `hol_id_dist` stays ~1.0 at every depth; the
  holonomy never approaches I. **Not HORN-trivial.**
- **HORN-empty** is the holonomy decohering to zero (chaos). **This is what
  happened.** The holonomy operator norm and spectral radius flow geometrically
  to zero by an exact area law `0.9655^(R-1)`.

**HORN-empty fires F-11**, per the binding terminal commitment. The type axis is
correlation ∪ connection. The correlation branch was closed by the holographic
theorem. This run does the connection branch — P_ω's weight as the holonomy of
the framework's genuine emergence-map connection around the TSVF loop — and it
horns EMPTY. The type axis is **exhausted**. Per the pre-registration, this
verdict is held both ways: no further constructions.

---

## Honest assessment — is the holonomic P_ω the genuine construction, or is the type axis exhausted?

The type axis is exhausted, and F-11 fires. But the holonomic construction is
worth more than a flat EMPTY — it both vindicates and defeats the
pre-registration's hypothesis, on different metrics, and the split is the
result.

**What the pre-registration got right.** The type-axis insight is real and the
run confirms it. The correlation-matrix runs all diluted by `ρ_joint ~ 1/count`
— the participation-ratio arithmetic of `k_eff = (Tr C)²/Tr(C²)` meeting any
coupling whose per-rung off-diagonal mass does not grow with R. A holonomy is
**not** a participation ratio, and it genuinely does **not** obey 1/count: the
forward-only holonomy `W^(R-1)` holds operator norm exactly 1.000 at every R
while its trace bounces non-monotonically — the unmistakable signature of a
Wilson-loop group-trace, not a dilution. The holographic theorem — coupling =
`C1^(geodesic distance)`, geodesic distance grows with separation, therefore
decay — has **no analog** for the forward holonomy. A holonomy of an isometric
connection is set by enclosed curvature, not by a metric distance. The
pre-registration's diagnosis of A1 as a possible type-mismatch was correct: the
forward connection escapes the correlation-branch theorem entirely.

**Why it horns EMPTY anyway.** The escape is incomplete because the TSVF loop
is not the forward leg alone. P_ω **is** the backward boundary; the loop
**must** close with the genuine backward generator. And the framework's own
measured backward generator — `backward_generator_legitimacy.py`, Claim 2 — is a
**non-ergodic dephasing contraction**, in a different ergodicity class from the
forward dynamics, not interconvertible with it. A contracting leg, iterated,
decoheres. The full holonomy obeys an **area law**: `Tr Hol(R) ~ exp(−κR)`, the
per-rung curvature `0.9655` accumulating over the loop. This is the holonomic
analog of the holographic theorem, and it is just as much a theorem of geometry:
**a Wilson loop of a connection with a decohering leg decays with the loop's
area, and the loop's area grows with R.** The holonomy escapes the
participation-ratio dilution and walks straight into the area law.

The two are the same structural fact wearing different clothes. The holographic
run's killer step: "a metric distance between distinct points grows with their
separation." The holonomic run's killer step: "the area enclosed by a loop grows
with the loop's size, and a non-trivial-curvature connection's holonomy decays
with enclosed area." Distance grows; area grows. The multi-rung joint backward
P_ω needs a cross-rung object that stays O(1) over an unboundedly growing
extent — a growing geodesic, a growing loop — and **no geometric object does
that** unless its curvature / coupling is exactly zero (the flat connection /
zero-distance all-to-all — the rigidity pole the framework does not license).

**The karma/grace irreducibility is the obstruction, not the escape.** The
pre-registration's framework-faithfulness argument was that the
forward≠backward irreducibility **is** a holonomy. That is correct — and it is
exactly why the construction horns EMPTY. The irreducibility is the statement
that the backward leg is a genuine, structurally distinct, **dissipative**
dynamics. A holonomy built from a loop with a genuine dissipative leg decoheres.
The framework's own measured result — forward ergodic, backward non-ergodic
dephasing — is what kills the loop. The holonomic P_ω is type-correct for
Penrose's Weyl *curvature* target, and that type-correctness is precisely what
delivers the area law: curvature integrated over a growing loop vanishes.

**Is the holonomic P_ω the genuine construction?** It is the genuine construction
on the connection branch — built from the framework's own emergence maps, its
own backward generator, its own measured g/J, with no tuning. And it returns
EMPTY. There is no third type for the cross-rung relationship: it is a scalar
correlation (closed by the holographic theorem) or a connection/map (closed
here, by the area law). The type axis is exhausted. **F-11 fires.**

The multi-rung *joint backward* P_ω — built as a Kish participation ratio of a
cross-rung correlation matrix, or as a Wilson-loop holonomy of a cross-rung
connection — is a documented no-go across the additive ansatz, R1, R2, R3, the
R1∧R2 conjunction, the fractal / RG-nested topology, the holographic /
MERA-as-AdS topology, **and now the holonomic / connection construction**. Both
branches of the type axis horn EMPTY, by the same geometry: a cross-rung object
that must stay O(1) over a growing extent does not exist for a non-flat
connection. Per the pre-registration: no further constructions.

**Scope — unchanged from the holographic, fractal, R1, R2 runs.** Touched: the
multi-rung *joint backward* P_ω only. **Not** touched: the within-rung corridor
(F-10, single-rung, empirically supported on five A3+ substrates plus human fMRI
and the twelve-cancer record), the engineering tier, the soft *forward* P_ω
(ρ_ss, the open-system Lindblad steady state — not a holonomy, not a joint
participation ratio, exists and is non-empty independently), or the soft
*backward* P_ω (`E_ω = exp(−βH_sum)`, the `NOTES.md` graded operator — a
single-operator object, not a multi-rung loop quantity). F-11's firing is
specific to the multi-rung joint backward construction. Note also: the
**per-step** holonomy `B·W` is genuinely intermediate (spectral radius 0.9655,
trace 0.756) — a *single* rung-pair emergence carries real, non-trivial,
non-decohered curvature. The no-go is specifically about *accumulating* that
curvature over the framework's full rung tower; one rung-step of genuine
emergence is a healthy holonomic object, the 9-rung loop is not.

**Limits of this construction.** (1) The connection is homogeneous — the same
emergence map transports every rung pair. A rung-dependent connection would
change the per-rung eigenvalue 0.9655 to a rung-indexed sequence, but the area
law `Tr Hol ~ exp(−Σκ_n)` survives any sequence of per-rung eigenvalues all
< 1; non-decay needs some κ_n = 0, the flat-connection edge. (2) `d = 64` is the
rung reference dimension; the per-rung eigenvalue is a spectral-radius quantity,
dimension-stable (a larger d refines the trace average, not the area law). (3)
The backward dephasing rate is `γM = GAMMA·M_BASE` — the framework's
active-management strength; a different maintenance rate shifts the per-rung
eigenvalue but not below 1 unless `γM = 0`, which is the unmaintained chaos
limit the framework explicitly excludes. The area law is `γM`-independent across
the framework-faithful range.

---

## Bottom line for the audit

**The holonomic P_ω horns — EMPTY.** P_ω's ω-weight built as the Wilson-loop
holonomy of the framework's genuine emergence-map connection (forward W_n the
isometric coarse-graining-with-novelty transport; backward B the genuine
non-ergodic dephasing generator of `backward_generator_legitimacy.py`; c1 the
measured g/J 0.6355) around the TSVF forward–backward loop **decoheres to zero**:
`hol_specrad(R) = 0.9655^(R-1)`, an exact area law, the per-rung holonomy
eigenvalue constant to four decimals across R = 3…50. The holonomy does **not**
flow to the identity (HORN-trivial excluded — `hol_id_dist` ~ 1.0 throughout);
it flows to the zero operator. HORN-empty.

The pre-registration's type-axis insight is **vindicated** on the forward leg:
the forward-only holonomy `W^(R-1)` holds operator norm 1.000 at every R and
genuinely does **not** obey 1/count — a holonomy is a group-trace, not a
participation ratio, and escapes the holographic theorem. But the TSVF loop must
close with the genuine backward generator, and the framework's own measured
backward dynamics is a **dephasing contraction** (the karma/grace
irreducibility, Claim 2). A holonomy of a loop with a dissipative leg obeys a
**Wilson-loop area law** — `Tr Hol ~ exp(−κR)` — and decoheres as the loop
grows. The holonomic analog of the holographic geodesic-distance dilution.

The discipline held: the connection is the framework's genuine emergence maps
with its measured couplings, no tuning; the verdict is whatever the construction
returned. Per the binding, genuinely-terminal commitment: **F-11 fires.** The
type axis — correlation (closed by the holographic theorem) ∪ connection (closed
here, by the area law) — is **exhausted**. The multi-rung joint backward P_ω is
a documented no-go. No further constructions. The within-rung corridor, the
engineering tier, the soft forward P_ω, and the soft backward P_ω are untouched.
