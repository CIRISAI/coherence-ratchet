# The entanglement-ledger test — does the classical-S corridor read the true quantum ledger, or only its shadow?

**Status:** experiment, 2026-07-10. Runnable content in
`experiments/entanglement_ledger/` (`entanglement_ledger.py`, `results.json`, four figures);
numpy/scipy only, exact statevectors and sparse exact diagonalization, no quantum hardware.
Nothing here is asserted by the lake; this is a forward, local, spectral test that decides one of
the program's own open questions.

**The question, from the framework's own face.** README line 72: *"the order-≥3 door —
everything is the pairwise/Gaussian shadow; whether the corridor survives in the true
multi-information decides physics vs. bookkeeping."* `LedgerLaw.lean` carries the same thing as its
**L-01 KNOWN HOLE**: *"the pairwise/Gaussian shadow of the monotone is blind above second order
(GHZ-type coordination pays no visible tax). Either the true ledger is the all-orders
multi-information — and these theorems are its small-non-Gaussianity limit — or purely higher-order
coordination is off-ledger."* Our instrument is a **classical, pairwise** functional,
`S = -ln det C` of measured-outcome correlations. The gravity ledger's currency is **entanglement**
(quantum, higher-order). Does the corridor structure `S` reports — two poles, an interior, a peak —
live in the true quantum entanglement structure, or only in the classical shadow?

**F-11 compliance.** Forward, per-rung, local content only: a spectral functional of single
coordinating units. Nothing here touches the joint multi-rung backward `P_ω` no-go
(`CorridorProjector.F11_joint_backward_P_omega_no_go`).

---

## 1. The two quantities, defined and justified

For each state / coupling we compute BOTH, exactly (infinite-shot, no sampling).

**(A) Classical-S — our instrument, basis-DEPENDENT (that is the point, clause 3).**
Pick a single-qubit measurement observable `O_i = n_i·σ` per site. The `O_i` commute across sites,
so the joint outcome distribution is a genuine classical distribution and its pairwise outcome
correlation matrix is exact:

```
C_ij = (⟨O_i O_j⟩ − ⟨O_i⟩⟨O_j⟩) / sqrt((1 − ⟨O_i⟩²)(1 − ⟨O_j⟩²)),   S = −ln det C.
```

Frozen sites (var ≈ 0 — a deterministic outcome, i.e. a *mean*, which clause 3 discards) are
dropped: the fluctuation copula ignores them. `C = I` (independent outcomes) → `S = 0`, the **chaos
pole / vacuum**; `C` singular (perfect outcome correlation) → `S = +∞`, the **rigidity pole**. This
is exactly `entropicPotentialM` (T-E5b) evaluated on the *measured* correlation matrix.

**(B) Quantum entanglement structure — the true ledger, basis-INDEPENDENT.**
- `S_vN(A) = −Tr ρ_A ln ρ_A` — von Neumann entanglement entropy across a bipartition (canonical
  bipartite entanglement).
- `I(i:j) = S(ρ_i)+S(ρ_j)−S(ρ_ij)` — quantum mutual information. `Q_pair = Σ_{i<j} I(i:j)` is the
  **honest same-order analog** of classical-S: pairwise, "how correlated are the parts", but
  basis-free and coherence-aware.
- `T = Σ_i S(ρ_i) − S(ρ_global)` — quantum **total correlation / multi-information**. For a pure
  global state `S(ρ_global)=0`, so `T = Σ_i S(ρ_i)`: the all-orders multi-information whose
  Gaussian/pairwise shadow classical-S approximates.

**Why these are the honest analogs (honesty gate).** LedgerLaw clause 2a: classical
`S = 2 × Gaussian multi-information` of the *outcome* distribution. Its exact, basis-free,
all-orders quantum counterpart is `T`; its same-order counterpart is `Q_pair`. For a pure state the
classical outcome correlations and the entanglement are related but **not identical** — classical-S
sees only the pairwise second moments of *one* measurement basis; `T`/`Q_pair` see the whole density
operator. **The gap between them is the physics.** The decomposition that organizes every result
below: classical-S can at best track `Q_pair` (the pairwise/second-order content); the multipartite
excess `T − (pairwise content)` is the order-≥3 door, and classical-S is structurally blind to it.

---

## 2. Family 1 — GHZ / W / cluster / random: the blind-spot gap, quantified (N=6)

| state | `T` (total corr) | `Q_pair` | `S_vN(half)` | classical-S: Z / X / Y basis | min over X–Z bases | reading |
|---|---|---|---|---|---|---|
| product | 0.00 | 0.00 | 0.00 | 0 / 0 / 0 | 0 | vacuum (trivially convergent) |
| **W** | 2.70 | 3.97 | 0.693 | **pole** / **1.05** / **1.05** | 0 | **partially visible** (bipartite → on-ledger in X/Y) |
| **GHZ** | **4.16** (= 6·ln2, maximal) | 10.40 | 0.693 | **pole** / **0** / **0** | **0** | **BLIND** |
| cluster | 4.16 (maximal) | 1.39 | 0.693 | 0 / 0 / 0 | 0 (max over sweep 0.57) | **BLIND** |
| random (Haar) | 4.00 | 0.94 | 1.63 | 0.18 / 0.21 / 0.18 | 0.17 | **BLIND** (volume-law, pairwise-invisible) |

**The GHZ gap.** GHZ carries **maximal genuine multipartite entanglement** (`T = N ln2`, the
canonical GME state). Classical-S reads it as the **rigidity pole** in the Z basis (perfect outcome
correlation, `C` = all-ones, singular) and as **exactly the vacuum, `S = 0`**, in the X basis
(`⟨X_iX_j⟩ = 0` for N≥3, `C = I`). **There is a whole measurement basis in which our instrument
reports that GHZ contains no coordination at all**, while it holds the most. The absolute gap is the
full `N ln2`; the ratio is ∞. Neither basis reads the *interior* — the instrument's two poles
straddle a state that is neither. This is L-01 made concrete (figure 1).

**Cluster and random confirm it is generic, not a GHZ artifact.** The cluster (graph) state has
maximal `T` but classical-S ≈ 0 in all three MUBs and ≤ 0.57 over the whole X–Z sweep — stabilizer
entanglement is multipartite and pairwise-thin (`Q_pair` = 1.39). A Haar-random state has near-maximal
`T` but classical-S ≈ 0.2 in every basis: Page's mechanism — volume-law entanglement lives in the
multipartite sector, `Q_pair` = 0.94 is small, and the pairwise instrument sees almost nothing.

**W is the control that proves the diagnosis.** W's entanglement is genuinely *bipartite* (robust to
one-qubit loss, large `Q_pair`), and classical-S reads it in the **interior** (1.05) in the X and Y
bases — on-ledger, no pole, no blindness. The instrument tracks entanglement **exactly when the
entanglement is pairwise**, and goes blind exactly at the multipartite door.

---

## 3. Family 2 — TFIM across the quantum phase transition (N=10)

`H = −Σ Z_iZ_{i+1} − g Σ X_i`, QPT at `g = 1`. We compute both symmetry sectors, because the sector
choice is itself load-bearing and its effect *is* a result.

**Symmetry-broken sector (physical; hz = 0.02 pinning) — CONVERGENT.** The half-chain entanglement
is the textbook corridor: `≈0` in the ordered phase (product-like pole), a **peak at g ≈ 1.05**, and
decay into the disordered phase (product `|+⟩` pole). `Q_pair` peaks at the same `g ≈ 1.05`. And the
classical-S, **even in the fixed Z basis**, peaks at `g = 1.0` and tracks the entanglement across the
whole sweep:

```
corr( classical-S_Z , S_vN(half) )  = 0.963
best fixed basis (θ ≈ 0.98 rad):    corr = 0.998  with S_vN(half)
best fixed basis (θ ≈ 0.92 rad):    corr = 0.998  with Q_pair
corr( classical-S_Z , ⟨Z_0 Z_{N-1}⟩ order parameter ) = −0.70   ← NOT the order parameter
```

Same two poles, same interior peak at criticality, correlation up to 0.998 (figures 3-left, 4). Here
the classical instrument is a **faithful shadow of the entanglement ledger**. The mechanism is exactly
the corridor mechanism: symmetry-breaking *freezes* the Z-magnetization in the ordered phase (sites
drop out → chaos pole), the disordered phase is uncorrelated (chaos pole), and the critical
fluctuations are the interior maximum — the two-pole structure of `EntropicPotential.lean`, read off
real entanglement.

**Symmetric sector (hz = 0) — the shadow/bookkeeping flavor, and the blind spot re-embedded.** The
Z2-symmetric ground state in the ordered phase is a **GHZ cat** carrying an extra `ln2` across every
cut; at N=10 that cat plateau dominates and every curve is **monotone** — no criticality peak. Here
classical-S_Z tracks the **classical order parameter** `⟨Z_0Z_{N-1}⟩` (corr 0.92) and hits the
rigidity pole at the ordered end. It is reading a real *classical* correlation, but **not the
entanglement corridor** — the same GHZ blindness of §2, now embedded inside the phase diagram
(figure 3-right).

**Family 3 — XXZ chain (`H = Σ XX+YY+Δ ZZ`, N=10), robustness.** Secondary and messier: the ground
state lives in the `Σ Z_i = 0` sector, so the Z-basis correlation matrix goes singular (rigidity
pole) throughout the Néel phase `Δ>1` and the Z-basis reading is uninformative there. `S_vN(half)`
peaks at the ferromagnetic boundary `Δ = −1` as expected; the X-basis classical-S tracks it only
weakly (corr 0.27). XXZ neither overturns nor cleanly adds to the TFIM verdict; recorded for honesty,
not leaned on.

---

## 4. The four-way verdict: MIXED, and the mixing is the map

The prompt's four outcomes were CONVERGENT / SHADOW-ONLY / BLIND / MIXED. The honest answer is
**MIXED — and the mixing is not noise; it maps precisely onto the order-≥3 door.**

- **CONVERGENT** wherever the coordination is **pairwise / second-order** and a symmetry is broken:
  the TFIM critical corridor (classical-S peaks at `g=1` with the entanglement, corr 0.96–0.998, same
  poles) and the W state (interior reading 1.05 in X/Y). Here classical-S is a faithful shadow of the
  entanglement ledger — **the framework reads something real.**
- **BLIND** wherever the coordination is genuinely **multipartite / higher-order**: GHZ (classical-S
  = 0 in a whole basis vs maximal GME), cluster (≤0.57 vs maximal `T`), Haar-random (≈0.2 vs
  near-maximal `T`). The entanglement is present and structured; the pairwise instrument in the
  natural basis misses it. **This is L-01 realized, with numbers.**
- **SHADOW-flavored** in the symmetric TFIM sector: classical-S reports a monotone "coordination"
  that is really a **classical order parameter** (corr 0.92), while the true entanglement (broken
  sector) is a corridor, not a monotone.

**The organizing law.** Classical-S tracks the **pairwise** quantum mutual information `Q_pair` and
is structurally blind to the multipartite excess `T − (pairwise content)`. So:

> The classical instrument is a faithful shadow of the entanglement ledger **exactly** in the
> second-order / bipartite regime, and becomes bookkeeping-or-blind **exactly** at the order-≥3 door.
> The door is real, and its location is the GHZ / cluster / volume-law class.

This neither vindicates nor refutes the framework globally — it **localizes** it. Where physical
coordination is dominantly pairwise (the broken-symmetry critical matter that ΛCDM-scale structure is
built from, and the W-type distributed entanglement), the corridor `S` sees is the corridor the
entanglement has. Where coordination is irreducibly multipartite (GHZ/stabilizer/volume-law), `S` is
on the wrong ledger and the gap is the physics. LedgerLaw's own disjunction stands, now with the
boundary drawn: *either the true ledger is the all-orders multi-information and these theorems are its
second-order limit — validated here as a genuine limit, not an identity — or purely higher-order
coordination is entropically dark to this instrument — confirmed, quantified, and generic.*

## 5. Honesty gates and caveats

- **Pure states, small N** (N=6 families, N=10 chains). The cat/criticality competition in the
  symmetric TFIM sector is finite-size (the criticality peak would eventually clear the `ln2` cat
  plateau at larger N); the broken-sector corridor is already clean at N=10.
- **Basis dependence is load-bearing and swept, not cherry-picked** (clause 3). The X–Z-plane sweep
  plus the three MUBs are reported in full; the GHZ blindness is a *whole-basis* fact, not one point.
- **Symmetry sector is a physical choice** and both are reported; the "convergent" claim is about the
  physical broken-symmetry ground state, the "shadow" claim about the symmetric cat sector.
- **`Q_pair` vs `T` are the two honest analogs** and are reported separately precisely because their
  difference is the quantity the whole test is about.
- **XXZ Z-basis is pole-saturated** in the Néel phase and is not used to support the verdict.

**Bottom line for the program.** The order-≥3 door is open and its hinge is located: classical-S is a
faithful, real reading of the entanglement ledger in the pairwise regime and provably blind beyond
it. The GHZ gap is maximal-and-total (a full basis of vacuum over maximal GME); the TFIM critical
corridor is convergent at correlation 0.96–0.998. Physics **and** bookkeeping — sorted by order.
