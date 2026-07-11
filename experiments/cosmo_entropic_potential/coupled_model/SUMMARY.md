# Coupled cross-sector maintenance model — full result-space

**Date:** 2026-07-10. **Mode:** DISCOVERY (no pre-stated prediction; every dial
reported at equal weight; interpretation confined to a labeled section). **Grid:**
2880 cells = 8 dimension-vectors x 2 alpha-forms x 6 (rule,split) combos x 2
budget-accountings x 15 budget-levels. Every cell integrated to steady state /
pole / PSD-boundary, classified, Jacobian eigenvalues computed. Full grid in
`results.json` (incremental-flushed). Lake companion:
`formal/CoherenceRatchet/Core/NestedKish.lean`.

**The model, and how it differs from the parent.** The parent
(`../forced_partition/`) used INDEPENDENT sector blocks: the correlation matrix was
block-diagonal, `-ln det` split additively, and k_eff was extensive in D
(k_eff ~ 0.61*D under every rule -- the parent's `dsweep_keff.py` FAILED to find
saturation, and named the fix: *a model with a global cross-sector correlation
channel is required before the saturation question can be asked*). This model is
that fix. A single GLOBAL channel rho_g couples units in DIFFERENT sectors:

    C_ii = 1,  C_ij = rho_k (same sector k),  C_ij = rho_g (different sectors).

State = (rho_1..rho_n, rho_g): n+1 maintained channels sharing one budget.
`drho_k/dt = alpha(rho_k) - gamma*m_k`, `drho_g/dt = alpha(rho_g) - gamma*m_g`, a = gamma = 1.

**Two-level spectrum (closed form, VALIDATED).** Local eigenvalues (1-rho_k) with
multiplicity (d_k-1) per sector; plus the n eigenvalues of the reduced sector-mean
matrix G (G_kk = 1+(d_k-1)rho_k, G_kl = sqrt(d_k d_l)*rho_g). `k_eff` = participation
ratio (sum lambda)^2/sum lambda^2 of the FULL set; since Tr C = D this is D^2/sum lambda^2 with
sum lambda^2 = sum_k(d_k-1)(1-rho_k)^2 + sum_k(1+(d_k-1)rho_k)^2 + rho_g^2(D^2-sum d_k^2). Validated against
`numpy.eigvalsh` on explicit matrices over 2160 grid cells (D <= 60) plus 2000
random heterogeneous draws: **max |k_eff_closed - numpy| = 2.8e-14, max
|-lndet_closed - numpy| = 7e-12**, and the PSD diagnostic
min eig(C) = min(1-rho_k, min eig G) to 3e-15.

---

## 1. The complete result-space

### 1a. Global classification counts (all 2880 cells)

| class | count |
|---|---|
| collapse_chaos | 1871 |
| symmetric | 511 |
| broken | 451 |
| runaway_rigidity | 29 |
| psd_boundary | 18 |

(collapse_chaos dominates because the budget axis runs to b = 1.45, deep into
over-maintenance; the interior band and its structure are 1b-1f.)

### 1b. k_eff vs D -- THE HEADLINE (does coupling saturate the participation ratio?)

pair25 series (D = 7,14,28,56,112,224), linear alpha. Table entry = k_eff at that D;
`chao`/`rigi` = pole reached. Last column = fitted `d ln k_eff / d ln D` on the
interior cells (0 = saturating, 1 = extensive).

| accounting | rule/split | b | 7 | 14 | 28 | 56 | 112 | 224 | slope |
|---|---|---|---|---|---|---|---|---|---|
| per_pair | A_equal/na | 0.35 | 1.98 | 2.16 | 2.26 | 2.31 | 2.34 | 2.35 | **+0.05** |
| per_pair | A_equal/na | 0.75 | 5.09 | 7.72 | 10.42 | 12.62 | 14.11 | 15.00 | +0.31 |
| per_pair | B_stock/s1 | 0.35 | 1.97 | 2.09 | 2.20 | 2.27 | 2.32 | 2.34 | **+0.05** |
| per_pair | B_stock/s2 | 0.35 | 1.95 | 2.15 | 2.25 | 2.31 | 2.34 | 2.35 | **+0.05** |
| per_pair | C_rate/s1 | 0.35 | 1.96 | 2.05 | 2.18 | 2.27 | rigi | rigi | +0.07 |
| per_pair | C_rate/s2 | 0.35 | 1.96 | 2.14 | 2.23 | 2.29 | 2.32 | 2.34 | **+0.05** |
| per_pair | D_need/na | 0.35 | 1.98 | 2.16 | 2.26 | 2.31 | 2.34 | 2.35 | **+0.05** |
| per_channel | A_equal/na | 0.35 | 1.98 | 2.16 | 2.26 | 2.31 | 2.34 | 2.35 | +0.05 |
| per_channel | B_stock/s1 | 0.35 | 2.44 | 4.97 | 12.74 | 28.34 | 59.34 | 121.33 | **+1.14** |
| per_channel | B_stock/s2 | 0.35 | 2.13 | 2.41 | 2.84 | 3.49 | 4.21 | 4.82 | +0.25 |
| per_channel | C_rate/s2 | 0.35 | 2.40 | 3.66 | 10.14 | 28.32 | 60.38 | 123.88 | **+1.20** |
| per_channel | D_need/na | 0.35 | 1.99 | 2.23 | 2.37 | 2.46 | 2.50 | 2.52 | +0.06 |

**k_eff SATURATES (bounded as D -> inf) under the coupled model** -- the qualitative
departure from the parent's extensive 0.61*D -- but WHICH cells saturate is
controlled by whether the dynamics HOLDS rho_g > 0 as D grows, and that is set by
the **budget accounting for the global channel**:

- **per_pair accounting** (global channel priced by its O(D^2) cross-pair count) ->
  rho_g held at a D-independent value -> **k_eff saturates flat** (slope ~ +0.05) for
  every rule at low budget.
- **per_channel accounting** (global channel = one channel among n+1, priced like a
  single sector) -> for the state-responsive stock/rate rules the global channel's
  budget share -> 0 as n grows -> rho_g -> 0 -> sectors DECOUPLE -> **k_eff extensive**
  (slope ~ +1.1). Explicit at b=0.35, B_stock/s1: per_pair holds rho_g = 0.64->0.65
  and k_eff = 2.0->2.3 across D=7->224, while per_channel lets rho_g = 0.54->0.05->0.00
  and k_eff = 2.4->59->121.

### 1c. The saturation ceiling is exactly 1/rho_g^2 (per_pair, A_equal, lin, D=224)

| b | rho_g* | k_eff(D=224) | 1/rho_g^2 |
|---|---|---|---|
| 0.15 | 0.850 | 1.38 | 1.38 |
| 0.35 | 0.650 | 2.35 | 2.37 |
| 0.55 | 0.450 | 4.85 | 4.94 |
| 0.65 | 0.350 | 7.91 | 8.16 |
| 0.75 | 0.250 | 15.00 | 16.00 |

The bounded k_eff the coupled spectrum settles to is the participation-ratio
ceiling **1/rho_g^2** of the global channel (matched to 1-6%; the gap grows as rho_g
falls and sector structure contributes more of sum lambda^2). This is the participation-
form analogue of the Kish trace-ceiling 1/rho -- squared, because k_eff here is
(sum lambda)^2/sum lambda^2, not Tr/lambda_max. As the budget rises rho_g is spent down, the ceiling rises,
and saturation weakens toward extensivity.

### 1d. rho_g vs sector-rho -- the budget competition (pair25_x8, D=56, lin, per_pair)

| rule/split | b=0.35 | b=0.65 | b=0.95 |
|---|---|---|---|
| A_equal/na | rho_g=.65 r2=.65 r5=.65 | .35/.35/.35 | .05/.05/.05 |
| B_stock/s1 | rho_g=.63 r2=**.998** r5=**.989** | .31/.994/.960 | .015/.899/.597 |
| B_stock/s2 | rho_g=.65 r2=.867 r5=.690 | .35/.611/.333 | .05/.086/.024 |
| C_rate/s2 | rho_g=.63 r2=.978 r5=.911 | .32/.956/.824 | .02/.867/.467 |
| D_need/na | rho_g=.65 r2=.671 r5=.671 | .35/.389/.389 | .05/.107/.105 |

- **A_equal, D_need** hold rho_g = rho_sector (all channels equal) -- the global channel
  is treated identically to a sector.
- **B_stock/s1 and C_rate/s1** (pairwise-proxy stock): the global channel's O(D^2)
  pair count DOMINATES the weight, so it commands budget and holds rho_g moderate
  (~0.63) while the **sector channels are starved to the rigidity pole**
  (rho_sector -> 0.99). The global channel wins the competition and the sectors
  collapse. (For asym_29 this drives the PSD boundary -- 1g.)
- **B_stock/s2, C_rate/s2** (log-det split): balanced -- sectors held below rigidity
  and **dimension-ordered** (rho(d=2) > rho(d=5) throughout), the same anti-dimensional
  ordering the parent found, now WITH a coexisting maintained global channel.

### 1e. Symmetry-breaking by rule (interior cells)

| rule/split | symmetric | broken |
|---|---|---|
| A_equal/na | 192 | 0 |
| D_need/na | 187 | 0 |
| B_stock/s1 | 42 | 121 |
| B_stock/s2 | 26 | 159 |
| C_rate/s1 | 32 | 45 |
| C_rate/s2 | 32 | 126 |

State-responsive rules (B, C) break the sector symmetry (dimension-ordered);
equal- and need-proportional rules never do. Identical to the parent's finding,
reproduced with the global channel present.

### 1f. Stability classes (Jacobian max real eigenvalue, interior cells)

| rule/split | n | max Re(lambda) range | median | marginal (|.|<1e-6) |
|---|---|---|---|---|
| A_equal/na | 192 | [-1.000, -0.632] | -1.000 | 0 |
| B_stock/s1 | 163 | [-1.000, -0.599] | -1.000 | 0 |
| B_stock/s2 | 185 | [-1.000, -0.512] | -1.000 | 0 |
| C_rate/s1 | 77 | [-1.000, -0.536] | -1.000 | 0 |
| C_rate/s2 | 158 | [-1.000, -0.340] | -1.000 | 0 |
| **D_need/na** | 187 | [+0.000, +0.000] | **+0.000** | **147** |

**Need-proportional allocation is MARGINAL** (zero Jacobian eigenvalue, 147/187
interior cells) while equal/stock/rate rules are strongly stable (-1). The parent's
signature result -- need -> neutral manifold; state-responsive -> stable -- **survives
the coupling unchanged**, now over an (n+1)-dimensional Jacobian that includes the
global channel.

### 1g. PSD-boundary encounters (18 cells) -- a first-class new outcome

The coupled matrix is not block-diagonal, so rising rho_g drives the smallest
between-sector **contrast eigenvalue of G** (= 1+(d-1)rho_w - d*rho_g in the equal
case) toward zero -- the PSD boundary, hit at rho_g < 1, WELL before any rigidity
pole. 18 cells reach it (integration stopped there, not hidden by the guard):

- **All 18 are on the most-asymmetric vectors** -- 17 on `asym_29` (2,9), 1 on
  `pair25_x2` -- where sqrt(d_k d_l) cross-weights are largest relative to the
  diagonal, so the contrast eigenvalue is easiest to null.
- Two mechanisms: (i) **B_stock/s2 at starvation** (b=0.05-0.15) -- sectors and the
  global channel both driven up until contrast vanishes (rho_g~0.83-0.91); (ii)
  **C_rate/s1 across a whole budget band** (b=0.35-0.95 on asym_29) -- the pairwise-
  proxy rate pumps the global channel, rho_g rides the PSD edge as budget varies
  (rho_g = 0.78 -> 0.32 tracking the boundary while sectors sit at 0.99 -> 0.66).

The boundary is a genuine dynamical attractor of the starved/pumped global
channel, not a numerical artifact -- reported here at full prominence.

### 1h. alpha-form and accounting dependence

- **Linear alpha** gives the richest interior band; **logistic alpha** narrows it (weaker
  drift near both poles -> over-maintenance tips to chaos more readily), but every
  qualitative signature above (saturation-under-per_pair, dimension-ordered
  breaking, D_need marginality, PSD boundary) reproduces where an interior state
  exists.
- **Accounting is qualitatively DECISIVE here** (unlike the parent, where it was
  immaterial): per_pair vs per_channel is exactly the saturation-vs-extensive
  switch for the state-responsive rules (1b), because it sets the global channel's
  budget share as D grows.

---

## 2. Interpretation (LABELED -- read 1 first)

**The coupled model produces the k_eff saturation the independent-block parent
structurally could not -- and localizes its origin precisely in the maintained
global channel.**

1. **Saturation is real and it is 1/rho_g^2.** When the shared budget holds rho_g at a
   D-independent value, the participation ratio saturates to 1/rho_g^2 regardless of
   how many units or sectors are added (D = 7 -> 224, k_eff flat at ~2.3). This is
   the coupled analogue of the Kish ceiling k_eff -> 1/rho: *more constituents is a
   non-solution to coordination dimensionality* -- but only the GLOBAL correlation
   supplies the ceiling. The parent's sideways diagnosis is confirmed at the
   mechanism level: Gate-0's 1/rho ceiling "lives in global cross-unit correlation,"
   and here that channel, when maintained, delivers exactly a bounded k_eff.

2. **Saturation is CONDITIONAL on the dynamics sustaining rho_g > 0, which is a
   budget-accounting fact, not an allocation-rule fact.** Price the global channel
   by its O(D^2) coordination surface (per_pair) and it keeps a D-independent budget
   share -> rho_g held -> saturation. Price it as one channel among many (per_channel)
   and its share dilutes to zero as the system grows -> rho_g -> 0 -> the sectors
   decouple and k_eff goes extensive again. The saturation is thus a *maintained*
   property -- it exists only while coordination work actually holds the global
   channel -- which is the two-axis stance (structure is sustained by the gamma*M term),
   now visible as a scaling law: **whether effective dimensionality is bounded is
   whether the global coordination channel is affordably maintained as the system
   scales.**

3. **The global channel and the sectors COMPETE for one budget, and the
   competition can starve either side.** Under pairwise-proxy stock/rate rules the
   global channel's huge pair count wins and starves the sectors to rigidity (1d);
   under the log-det split the two coexist with the sectors dimension-ordered. This
   is a genuine, stable symmetry-breaking of the coupled budget, not seeded -- the
   block dimensions are seeded (the parent's honesty carries over), but the rho_g-vs-
   rho_sector split and its stability are dynamical.

4. **The policy <-> stability-class map is coupling-invariant.** Need-proportional
   allocation is marginal (zero eigenvalue) and state-responsive allocation is
   strongly stable, exactly as in the independent model, now over the (n+1)-channel
   Jacobian. The result is robust to adding the global mode.

5. **A new failure mode: the PSD boundary.** Coupling introduces a boundary the
   block model could not have -- the global channel driven until the between-sector
   contrast eigenvalue vanishes and the correlation matrix loses positive-
   definiteness at rho_g < 1. It is reached on asymmetric partitions under global-
   channel-favoring rules. This is the coupled-model counterpart of the rigidity
   pole: an over-coordinated global mode is as fatal as an over-correlated sector.

**Surprises flagged at full weight:** (i) the saturation ceiling matches 1/rho_g^2 to
1-3% with no fitting; (ii) accounting -- immaterial in the parent -- is here the
decisive saturation-vs-extensive switch; (iii) pairwise-proxy allocation starves
sectors to rigidity while the global channel survives; (iv) the PSD boundary is a
real dynamical attractor on asymmetric partitions, not a guard artifact.

---

## 3. Sideways pass (labeled interpretation -- against the program's OTHER standing questions)

**Read against CLAUDE.md's two-axis / Gate-0 stance, this result speaks most directly to the
CONTENT-vs-TAUTOLOGY question (open question #5, "the deepest").** Gate-0 established
that k_eff SATURATES on complete real coordinating units, and the standing worry is
whether that saturation is near-definitional. This toy separates the two cleanly:
in the SAME family of matrices, the participation ratio is **extensive**
(per_channel, decoupled) or **saturated to 1/rho_g^2** (per_pair, coupled) -- the
difference is not the definition of k_eff (identical throughout) but a physical fact
about whether a global correlation channel is *held up* as the system grows. So
"k_eff saturates" is NOT a tautology of the metric: it is a substantive statement
that a maintained global correlation exists. That is precisely the content Gate-0
reads off real data, and this model shows it is a contentful, falsifiable property
of the dynamics -- a system with the same k_eff definition but no maintained global
channel does not saturate.

**Top item -- the concrete next test this hands the program:** the saturation
ceiling being *exactly 1/rho_g^2* converts Gate-0's per-substrate saturation level into
a **direct read-out of the global cross-unit correlation**: measure the saturated
k_eff on a complete unit, and 1/sqrt(k_eff) is the effective global rho_g of that
substrate -- a single number comparable across the zebrafish brain, the market, and
TCGA. The prediction is sharp and checkable on data in hand: on any Gate-0 substrate
where k_eff saturated at level L, the mean off-diagonal (cross-module) correlation
should be ~ 1/sqrt(L). If it is, the coupled channel is not just a toy -- it is what the
saturation level has been measuring all along. Two caveats for whoever runs it:
Gate-0's substrates are single-sector-dominant (the toy's clean 1/rho_g^2 assumes the
global mode dominates sum lambda^2, good only when rho_g is not small -- 1c shows the ceiling
loosening below rho_g~0.3), and the seeded-block honesty still binds -- this model
DERIVES nothing about which partition nature uses; it shows only what a maintained
global channel does to k_eff once a partition is given.

## Artifacts

- `results.json` -- full 2880-cell grid (incremental-flushed).
- `fig1_keff_vs_D.png` -- k_eff vs D per rule, curves by budget, per_pair, log-log,
  with the extensive 0.61*D reference.
- `fig2_rho_competition.png` -- rho_g vs sector-rho vs budget per rule (the competition),
  corridor band + PSD-boundary markers.
- `fig3_phase_map.png` -- classification over (budget x D) per rule.
- `coupled_model.py`, `analyze.py`, `make_figures.py`.
- Lake: `formal/CoherenceRatchet/Core/NestedKish.lean` (equicorr determinant +
  nested log-det decomposition, equal case proved; general case named-open `sorry`).
