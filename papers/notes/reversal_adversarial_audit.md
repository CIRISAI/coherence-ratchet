# Adversarial audit: the Bullet Cluster REVERSAL (`bullet_cluster_correction.md`)

**Date: 2026-07-10. Assignment: destroy the reversal.** Target claim: the shocked ICM
thermalizes → Maxwellian → independence → LOW S; the collisionless galaxies keep coherent bulk
motion (~4500 km/s) → "perfectly correlated" → HIGH S; therefore the ledger (S = −ln det C)
points at the lensing mass (with the galaxies) and beats MOND (which "tracks the gas").

**Bottom line up front: the reversal is (c) ITSELF WRONG.** Four of five attack lines LAND, one
of them a clean kill. The reversal rests on a category error the framework's own definition of C
forbids, and its rival-beating claim misrepresents MOND. The orchestrator was closer to right in
the *original* "DEAD" note than in the retraction — though the original was right for a partly
wrong reason too. What the ledger actually predicts for the Bullet Cluster is at the end.

Computation: `experiments/dm_coherence/mean_removal_toy.py` (seed 20260710; every number below
is executed output).

---

## ATTACK 1 — THE MEAN-VS-FLUCTUATION OBJECTION — **LANDS. This is the kill.**

**S = −ln det C acts on a CORRELATION matrix. A correlation matrix is mean-removed and
variance-normalized by construction** (clause 2b commits to it: `entropicPotentialM (kishMatrix
k ρ)`, ρ = *correlation*, C unit-diagonal). **A coherent bulk velocity shared by every galaxy is
a MEAN, not a correlation among fluctuations.** Removing the mean deletes it.

Explicit toy (units = galaxies, variables = 3 velocity components; galaxy velocity = shared bulk
V + isotropic dispersion σ = 300 km/s):

| V_bulk (km/s) | S = −ln det C (mean-removed) |
|---|---|
| 0 | 0.0002 |
| 4500 | 0.0012 |
| 1 000 000 | 0.0011 |

**S is flat in V_bulk and pinned at ≈ 0.** The coherent bulk motion is completely invisible to
S. Only a *raw second moment about the origin* (NOT mean-removed — not the object the ledger uses)
registers the bulk. Side-by-side, same grain:

```
S_gas  (Maxwellian, no bulk)          =  0.0017
S_gal  (dispersion + 4500 km/s bulk)  =  0.0009      -> IDENTICAL (both ~0)
```

The claimed ordering S_gal ≫ S_gas **does not exist**. It was asserted from a physical picture
("coherent = correlated") that the correlation matrix erases in its first step.

**Two consequences, both fatal to the reversal as written:**

1. **A *mean blindness* joins clause-3 amplitude blindness, and the whole reading never
   confronted it.** S is blind to (a) uniform amplitude [proved: clause 3] AND (b) any shared
   additive offset [mean removal, definitional]. Coherent bulk flow lives entirely in (b).

2. **The "coherent = high S" intuition gets the cold limit backwards.** High S (approach to the
   rigidity pole) requires large off-diagonal correlation *among fluctuations*. A cold, ordered
   stream has *small* dispersion; as σ_disp → 0 the per-unit variance → 0 and the correlation
   matrix becomes ill-defined (you cannot standardize a zero-variance column), not S → ∞.
   Coherent-but-cold bulk motion pushes toward S undefined/0, the opposite of the claim.

**The reversal's central premise is false for the functional the framework actually uses.** Kill.

---

## ATTACK 2 — THE GRAIN PROBLEM — **LANDS.**

The reading never fixes what the coordinating UNITS are, nor what quantity is correlated across
them — a Gate-0 violation (grain before spectrum). The S-ordering is entirely an artifact of
that unfixed choice:

| Grain | What C is | S_gas vs S_gal |
|---|---|---|
| galaxies as samples × 3 velocity components | 3×3, bulk = mean → removed | **S_gas ≈ S_gal ≈ 0** (Attack 1) |
| galaxies as units × shared *fluctuating* common-mode | N×N | S large *only if* bulk is re-read as a fluctuating signal |
| fluid/galaxy positions × spatial two-point copula | grid correlation | **turbulent gas WINS** (Attack 3) |

Toy for the common-mode grain (8 galaxy-units, shared fluctuating driver f(t) + noise):

```
strong shared driver: mean rho = 0.488   S = 3.200
weak   shared driver: mean rho = -0.002  S = 0.009
```

So one *can* manufacture a high-S for coherent motion — but only by (i) reinterpreting the
constant 4500 km/s bulk as a *fluctuating* shared mode (which a single snapshot's bulk velocity
is not), and (ii) then the SAME grain applied to the turbulent ICM gives the gas an *even larger*
S (Attack 3), because turbulence supplies a genuine shared fluctuating field where a rigid bulk
translation supplies none. **No single defensible grain reproduces the claimed ordering.** Every
grain either nulls it (S_gas ≈ S_gal) or reverses it (S_gas > S_gal).

---

## ATTACK 3 — THERMAL ≠ UNCORRELATED — **LANDS, and it inverts the inversion.**

"Thermalized → Maxwellian → independence" conflates the **one-point marginal** (Maxwellian
velocity distribution *at a point*) with the **two-point copula between fluid elements** — and S
reads only the latter. A shocked, turbulent, magnetized ICM is *highly* spatially correlated.

Toy (12 fluid probes, spatially correlated velocity field, exponential correlation length L;
one-point marginal held Gaussian/Maxwellian, excess kurtosis ≈ 0):

| correlation length L | mean \|off-diag ρ\| | S | marginal excess kurtosis |
|---|---|---|---|
| 0.01 (independent) | 0.010 | 0.010 | −0.004 |
| 2.0 | 0.228 | 5.108 | −0.009 |
| 8.0 | 0.618 | 16.647 | −0.054 |

**Same Maxwellian marginal, S ranging from 0 to 16.6** purely by spatial correlation length. The
observations put the ICM at the *long*-correlation end:

- **XRISM/Resolve Perseus (2026, arXiv:2510.12782):** velocity structure function favours an
  energy **injection scale ≥ a few hundred kpc**; a coherent **dipole of ±200–300 km/s** across
  the field; "a single, large-scale kinematic driver." That is a strongly spatially *correlated*
  velocity field.
- **Hitomi Perseus (2016/2018):** low turbulent Mach number, driving scale below ~100 kpc but
  smooth bulk gradients — again coherent, not white.

Post-shock, turbulence is *injected*, raising the two-point correlation, not lowering it. **So
the copula S sees the ICM as the HIGH-S component**, the exact reverse of the reversal's premise.
Thermalization maximizes the *one-point* entropy at fixed energy; it says nothing about — and
merger turbulence actively *raises* — the two-point coordination S measures.

---

## ATTACK 4 — CIRCULARITY — **LANDS.**

Strip Attacks 1 and 3 and the reading's residual content is: "the lensing mass sits with the
collisionless component." That is the definition of CDM (dark matter *is* collisionless). The
correction note concedes this in its own §72 ("also what CDM says"), and `gravity_dark_matter_
reading.md` §8.2 already labeled the only surviving Bullet-Cluster candidate (c) as "just CDM
wearing a copula." The reversal adds no independent, ledger-specific content at the Bullet
Cluster: it neither predicts the *amount* of dark mass (ε unfixed) nor its collisionless behavior
from S (S is silent on collisionality). It is a post-hoc alignment with CDM's answer, not a
derivation from the ledger.

---

## ATTACK 5 — THE RIVAL-BEATING CLAIM — **LANDS (the table row is a strawman).**

The correction's table says MOND "tracks baryonic **mass density** → gas (≈90%) → predicts mass
with the gas → **fails**." **This is false, and has been known false since 2006.**

- **Angus, Famaey & Zhao 2006 (astro-ph/0606216):** in MOND the phantom "missing mass" is
  centered on the **low-acceleration regions, which are where the galaxies are, not the X-ray
  gas.** MOND *reproduces* the potential–gas offset. It does **not** mislocate the lensing peak.
- **arXiv:2604.10811 (2026), "A consistent MOND modelling of the Bullet Cluster":** MOND lensing
  depends on **volume density**, not total mass; near-point-like galaxies (~7% of baryons)
  produce a **larger** phantom surface-density signal than the diffuse Mpc-scale gas. QUMOND
  peaks **on the galaxies, as observed.**

MOND's actual Bullet-Cluster failure is a **residual missing-mass factor ~2** in the core
(Angus+ 2006/2007; Sanders 2006), patched with ~2 eV neutrinos — a **magnitude** problem, NOT a
**mislocation**. So the reversal claims to "beat MOND" at precisely the thing MOND already does
correctly (peak location), while ignoring the residual-mass problem the ledger *also* inherits
(and, per `gravity_dark_matter_reading.md` §8.2b, inherits *worse*, via the Σ_b⁻¹ law). **The
discriminating table is a strawman; the ledger does not beat MOND here.**

---

## The mean-removal verdict (asked for explicitly)

**S does NOT distinguish "coherent bulk flow" from "thermal" — that distinction is invisible to a
normalized correlation matrix.** A shared bulk velocity is a mean; C removes means before it does
anything else. After mean removal the galaxies' residual (their velocity *dispersion*) is
approximately isotropic and uncorrelated across components → C ≈ I → S ≈ 0, identical to the
thermalized gas. The reversal's engine — "coherent motion = perfect correlation = high S" — mines
a signal that C deletes in step one. To rescue high-S for the galaxies you must switch grains
(Attack 2), and every grain that does so hands the turbulent gas an *equal or larger* S
(Attack 3). **The reversal is baseless as constructed.**

---

## VERDICT: (c) the reversal is itself wrong

Not "unsupported-but-not-refuted." **Refuted.** It inverts a sign it should not have touched,
using a "coherence" intuition that the correlation-matrix functional is definitionally blind to,
and it wins its MOND comparison only by misdescribing MOND.

Note the symmetry of the failure: the **original** §8.2(a) ("shock COMPRESSES and CORRELATES →
S rises → dark mass at the shock") was *also* wrong in its stated mechanism — it read compression
(a density/amplitude change) as a rise in S, which clause 3 forbids. **But its *conclusion* —
that S tracks the correlated gas, and the Bullet Cluster is therefore a problem — is closer to
what S actually does than the retraction is**, because the *post-shock ICM turbulence* genuinely
does raise the two-point correlation (Attack 3). The orchestrator has now been wrong twice: once
in the mechanism of the original kill, once in the entire direction of the retraction.

### What the ledger actually predicts for the Bullet Cluster (if anything)

Reading S honestly — copula-only (clause 3) AND mean-blind (definition of C):

1. **On the velocity-component grain: S_gas ≈ S_galaxies ≈ 0.** The ledger is *silent* — it puts
   no mass anywhere. No prediction, not a match with the galaxies.

2. **On any spatial two-point grain (density or velocity field on a comoving grid): S tracks the
   MORE spatially correlated component, which post-shock is the turbulent ICM gas.** The ledger
   points, if anywhere, **at the gas** — i.e. it *fails* the Bullet Cluster in the classic
   MOND/Verlinde way, exactly as `gravity_dark_matter_reading.md` §8.2 first concluded (verdict
   DEAD), and for the corrected reason (spatial correlation, not compression).

3. **The grain is unfixed, so the sign is not even determined** until Gate-0 is honored. That
   itself is the finding: the reversal smuggled a grain choice (whatever made galaxies look
   correlated) without declaring it.

Either way, **the ledger does not robustly point at the collisionless galaxies.** The Bullet
Cluster remains a problem for the strong form of the reading, not a victory. The correction note
should be retracted back to (at least) the "unsupported" state, and its MOND-beating table row
removed as factually wrong.

### What survives of the correction note

- The **narrow** point that "shock compression is a density change S cannot see" (clause 3) is
  **correct** and worth keeping — it refutes the *original mechanism*. But it does not license the
  opposite conclusion; it just removes one wrong argument, leaving the (turbulence-driven,
  Attack 3) spatial correlation to point back at the gas.
- The magnitude, dwarf-spheroidal, DF2/DF4, and circularity caveats (correction §"What is NOT
  rescued") are untouched by this audit and still stand.
- The proposed **SPARC test split by kinematic coherence** is not supported by the mechanism it
  claims (S does not read kinematic coherence of a bulk mean); it would need reformulation in
  terms of the *two-point copula of the baryonic field*, at which point it collapses back into the
  Σ_b⁻¹ exponent problem already shown fatal in §8.1.

---

## Sources

- Angus, Famaey & Zhao 2006, "Can MOND take a bullet?" — [astro-ph/0606216](https://arxiv.org/abs/astro-ph/0606216) (MOND phantom mass on low-acceleration regions = galaxies; residual missing mass ~factor 2; 2 eV neutrino patch).
- "A consistent MOND modelling of the Bullet Cluster" 2026 — [arXiv:2604.10811](https://arxiv.org/html/2604.10811v1) (QUMOND lensing peaks on galaxies via volume-density / point-like argument).
- XRISM/Resolve Perseus kinematics 2026 — [arXiv:2510.12782](https://arxiv.org/pdf/2510.12782) (injection scale ≥ few hundred kpc; coherent ±200–300 km/s dipole; single large-scale driver).
- Hitomi Perseus turbulence — [arXiv:2005.01883](https://arxiv.org/pdf/2005.01883) (mild, coherent gas motions; sub-100 kpc driving; smooth bulk gradient 150 km/s / 60 kpc).
- ICM velocity structure functions (method) — [MNRAS 524, 2945](https://academic.oup.com/mnras/article/524/2/2945/7221340).
