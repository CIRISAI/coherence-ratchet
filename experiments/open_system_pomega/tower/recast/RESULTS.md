# P_ω tower — recast: cross-rung corridor as a map-constraint — results

**Date:** 2026-05-22. **Falsification handle:** F-11 / F-12 (P_ω operator
construction). **Pre-registration:** `PREREGISTRATION.md` (this directory).
**Build script:** `build_tower_recast.py`. **Raw results:**
`results_tower_recast.json`. **Prior construction under test:**
`../build_tower_pomega.py`, `../RESULTS.md`.

---

## VERDICT: TRIVIAL

The pre-registration's third horn. The frustration the prior construction
documented **does dissolve** under the relational map-constraint form — the
per-rung floor does **not** grow ≈0.19/rung; it is effectively zero. But it
dissolves the **trivial** way: each connecting map W_n independently satisfies
its own cross-rung corridor with no joint constraint binding the tower
together. The cross-rung corridor, recast as a constraint on the maps, does
**no joint work**. Per the pre-registration this is reported as TRIVIAL,
**not** as a DISCOVERY — DISCOVERY required the floor to dissolve *and* the
multi-rung object to stay non-trivial; the second condition fails.

This is a two-sided result: the misread hypothesis is **half right**. The
prior obstruction's specific mechanism — adjacent additive operator penalties
frustrating over a shared rung — *is* an artifact of the additive-operator
modeling choice, and the relational form removes it. But removing it does not
yield a working multi-rung P_ω; it yields a tower that decouples into
independent single-bond constraints. The recast trades an obstruction for a
triviality. It is not the genuine framework structure that rescues the
multi-rung object.

---

## What was built

A genuine tower with the cross-rung corridor recast onto the connecting maps,
exactly as the pre-registration specifies:

- **Rungs carry distributions.** Rung n carries a probability distribution
  p_n on a d=3 macrostate alphabet (the rung's macrostate occupation).
- **Maps are coarse-graining channels.** W_n : rung n → rung n+1 is a
  column-stochastic matrix — a genuine classical coarse-graining channel. The
  emergence relation *is* the channel. Rung n+1's distribution is the genuine
  push-forward p_{n+1} = W_n p_n; the composition W_{n+1}∘W_n is carried by
  construction.
- **τ(W_n) is the framework's own definition.** Not a hand-tuned penalty: the
  genuine normalized mutual information

      τ(W_n) = I(R_n; R_{n+1}) / min(H(R_n), H(R_{n+1}))

  with the joint J[y,x] = W_n[y,x]·p_n[x] and I = Σ J log(J / (p_in⊗p_out)).
  The sanity check confirms it spans the framework's axis exactly: a
  permutation channel (n+1 relabels n) gives τ = 1.000 (rigidity pole); the
  fully-mixing channel (n+1 independent of n) gives τ = 0.000 (chaos pole).
- **Within-rung penalty unchanged** — the soft H_n = (ρ_n − ρ_c)², with
  ρ_n = 1 − H(p_n)/H_max the within-rung correlation scalar, ρ_c = 0.5.
- **Joint object** H_total = Σ_n (ρ_n − ρ_c)² + Σ_n (τ(W_n) − τ_c)², τ_c = 0.5.
  h_min(R) = min over {p_0, W_0…W_{R−2}}.

CUDA throughout: cupy/float64, all τ, push-forwards and per-map searches
GPU-batched (pools of 60k channels + 12 rounds of local refinement). Results
flushed per depth. Runtime ~52 s.

**Why the greedy chain solve is the correct solver — and why that is itself
the finding.** τ(W_n) depends only on (W_n, p_n); p_n depends only on
W_0…W_{n−1}. The tower is a **directed feed-forward chain**, not a frustrated
loop. So h_min is found by sweeping the maps in order — at each rung, with the
input fixed, pick W_n locally. There is no backward coupling: W_n cannot make
an upstream rung worse. Independent re-solves agree to ~1e-7. *That the chain
is feed-forward is the structural content of the recast* — and it is also
exactly why the result is TRIVIAL rather than a discovery.

---

## What the construction showed

### 1. The per-rung frustration floor is gone (≈0.19/rung → ≈0)

| R   | prior run (additive operator) h_min/R | recast (map-constraint) h_min/R |
|-----|----------------------------------------|----------------------------------|
| 9   | ~0.19 (plateau)                        | 6.5 × 10⁻⁸                       |
| 13  | ~0.17–0.19                             | 5.6 × 10⁻⁸                       |
| 20  | ~0.19                                  | 4.1 × 10⁻⁸                       |
| 56  | ~0.19                                  | 6.7 × 10⁻⁸                       |
| 120 | (analytic: linear, slope 0.19)         | 6.7 × 10⁻⁸                       |

h_min(R) does **not** grow ≈0.19/rung. The per-rung energy density over the
deep tail is e_inf ≈ 7 × 10⁻⁸ — flat, no accumulation. (An initial coarse-pool
run left an O(1e-3) residual; a separate check confirmed that residual is
random-search error, not a floor — local refinement drives it to ~1e-7, and
the final run carries that refinement. The genuine floor is zero.)

### 2. The shared-rung frustration is gone

The prior run's decisive test, in relational form:

- **One isolated** cross-constraint: min penalty 1.3 × 10⁻¹⁰ (prior: ~2 × 10⁻⁶
  — both satisfiable).
- **Two adjacent** cross-constraints sharing a rung: min penalty 2.2 × 10⁻⁹.
  Prior run: **0.096** — irreducible, the two could not be jointly satisfied.

In the relational form the two adjacent constraints reach τ(W_0) = 0.5000,
τ(W_1) = 0.5000 simultaneously. The shared-rung competition the prior run
identified — adjacent quantum operators (τ_n − τ_c)² fighting over the
H_{n+1} tensor factor — **has no analogue here**, because W_0 and W_1 are
distinct maps and the middle rung's distribution is simply whatever W_0
produces, then freely re-coarse-grained by W_1. The pre-registration's
hypothesis is confirmed *on this point*: the frustration was an artifact of
modeling τ as an additive operator competing for a shared quantum rung.

### 3. But the dissolution is TRIVIAL — the corridor does no joint work

The decisive DISCOVERY-vs-TRIVIAL test (STAGE C). For 600 random rung input
distributions, search whether a **single** channel can put τ(W) in the
corridor (0.1, 0.43) **and** deliver an output distribution in the corridor:

- **0 / 600** inputs had no locally-satisfying map. Every rung is
  independently solvable, *whatever distribution arrives at it*.
- The joint optimum h_min(R) equals the sum of independent per-map optima
  (the "gap" in the JSON is just the ~1e-6 search residual).
- The τ values at the joint optimum have spread ~1e-4 — every map sits at the
  same τ, each pinned independently to τ_c.

A direct calculation makes the mechanism explicit. A column-stochastic channel
W_n has (d−1)·d = 6 free parameters; τ(W_n) is 1 scalar constraint and "push
ρ into corridor" is d−1 = 2 more. There is enormous slack. Sampling channels
that fix a chosen distribution p* (so ρ_{n+1} = ρ_c automatically), τ ranges
continuously over [0.02, 0.50] — so each W_n can independently hit both its
cross corridor and a corridor output, *for any input*, with a fixed-point
distribution p* carried trivially down the whole tower. The tower decouples
into R−1 independent single-bond problems.

This is the pre-registration's named TRIVIAL horn verbatim: "the frustration
dissolves only because each W_n independently satisfies its corridor with no
joint constraint." It does.

---

## Honest assessment — is the recast the genuine framework structure?

**The recast is not a self-sealing rescue, and the verdict is not DISCOVERY.**
The honest reading:

1. **The relational form is a defensible reading of the framework.** The
   framework genuinely defines τ_(n,n+1) as a normalized mutual information,
   and in a tower that MI is genuinely a property of the coarse-graining map.
   Modeling the cross-rung corridor as a constraint on W_n rather than as an
   independent additive operator is *not* a tuned-to-vanish choice — τ(W_n)
   was computed as the literal framework definition, and the construction did
   not get to pick its value (the sanity poles confirm τ is the real MI). So
   the test was run fairly.

2. **The prior obstruction's mechanism was partly an artifact.** The specific
   ≈0.19/rung frustration floor came from adjacent *operators* sharing a
   quantum tensor factor. That shared factor does not exist when the cross-rung
   relation is carried by distinct maps. The misread hypothesis is right that
   the additive-operator form imposed structure the relational definition does
   not.

3. **But removing the artifact does not produce a working multi-rung P_ω.**
   It produces a tower that is not a *joint* object at all. The whole point of
   P_ω — and of the asymptotic-conditioning theorem and the Penrose-past
   argument that post-select through it — is that "corridor at every rung
   simultaneously" is a non-trivial joint constraint that concentrates measure
   on a special subset of configurations. A feed-forward chain where each map
   independently satisfies its corridor concentrates measure on *nothing*: any
   tower can be made to satisfy it bond by bond. The selectivity that D1 needs
   is gone.

4. **This is the same empty/trivial squeeze, relocated.** The P_ω history
   (`../../p_omega_construction/NOTES.md`) documents the squeeze: the hard
   projector is *empty* (narrow per-rung corridors don't intersect) or
   *trivial* (nest the rungs and it collapses to the finest-rung projector).
   The additive-operator soft tower hit the *empty* side (dead zone /
   frustration). The relational map-constraint tower hits the **trivial**
   side: non-empty by construction, but doing no joint work. The recast moves
   the construction from one horn to the other; it does not escape the
   squeeze.

**Two caveats on scope, stated plainly.**

- The penalty centre is τ_c = 0.5, matched to the prior run, but the
  framework's actual cross-rung corridor is the band (0.10, 0.43). At the
  optimum every τ sits at 0.5 — *outside* that band (`tau-in-band 0/119` in
  the depth scan). This does **not** change the verdict: STAGE C's
  decisive does-it-do-work test used the genuine band (0.10, 0.43) and still
  found every rung independently satisfiable (0/600 failures). The triviality
  is a property of the feed-forward structure, not of where the corridor
  centre sits.
- The construction is classical (stochastic channels on a d=3 alphabet),
  where the prior run was quantum (operators on a tensor product). That is the
  honest cost of the recast: a normalized mutual information realized by a
  *map* is most naturally a classical channel object. A quantum-channel
  version (CPTP maps, quantum MI) is the obvious next construction — but the
  triviality here is driven by the feed-forward / no-shared-rung structure,
  which a quantum tower of distinct CPTP maps would share. The squeeze is not
  expected to depend on classical-vs-quantum.

---

## Scope — what this touches and what it does not

**Touched.** The *multi-rung* P_ω carrying cross-rung structure. The prior
run's documented obstruction (additive-operator frustration, ≈0.19/rung) is
shown to be modeling-specific — but the relational alternative does not yield
a non-trivial joint object. The multi-rung P_ω remains caught in the
empty/trivial squeeze; this construction lands it on the trivial horn.

**Not touched.** The within-rung corridor (F-10, single-rung, empirically
supported across five substrates). The engineering tier. The soft *forward*
P_ω (ρ_ss, the open-system steady state). The Kish identity and the
corridor-as-attractor empirical content. As in the prior run, this is a
squeeze on the multi-rung *joint backward* object specifically.

**Bottom line for F-11 / F-12.** The hard-projector form is dead (documented,
three models). The additive-operator soft tower is dead-zoned (the prior run).
The relational map-constraint tower is non-empty but trivial (this run). The
multi-rung P_ω has now been obstructed or trivialized on every construction
tried. F-11's trigger is a documented no-go *without an alternative
TSVF-compatible operator emerging*: a *trivial* operator that does no joint
work is not the selective alternative the asymptotic-conditioning theorem
needs. This run does not by itself fire F-11, but it removes the relational
map-tower from the list of live rescues — and it sharpens what a genuine
rescue would have to do: produce a multi-rung object that is non-empty,
selective, and **jointly** constrained, which neither the additive-operator
form nor the relational map form delivers.
