# bench_suite — pre-registered DECISIONS (FROZEN before any bet-relevant run)

**Date 2026-07-11.** Registered bets 7 (third-law ceiling) and 8 (second-law
equality) from `papers/registrations_2026-07/MANIFEST.md`, and proposed bet 10
(interventional rent-cut) from `papers/notes/materials_mechanism_bet.md §3`. This
file fixes the apparatus and every PASS/KILL threshold. Calibration runs
(`calibrate.py`, `_probe_*.py`) preceded this freeze and produced only instrument
constants (no bet-relevant numbers); their results are quoted where they set a
threshold.

Governing kill wordings that this file must quantify WITHOUT contradicting
(sealed 2026-07-11, zenodo 10.5281/zenodo.21316928):
- Bet 7: "maintenance capacity collapses ∝(1−ρ) under bounded actuation (capacity,
  never realized-σ)"; KILL = "High σ at ρ ≫ 0.43 under bounded actuation; or the
  collapse curve inverts".
- Bet 8: "a single κ_bench satisfies ⟨e^(−W/κ)⟩ = 1 on the maintained corridor";
  KILL = "No single κ within error".

---

## Apparatus (frozen)

Substrate: an ensemble of `R` replicas of a `k`-oscillator **equicorrelation
Ornstein–Uhlenbeck array**, integrated on the RTX 4090 (cupy, Euler–Maruyama),
the object the corridor_ceiling theory is stated on:
`dx = −B x dt + √(2D) dW`, stationary covariance pinned to the Kish object
`C(ρ,k) = (1−ρ)I + ρ·11ᵀ`, `D = I`.

**Noise bath = REAL GPU TIMING JITTER (load-bearing, pre-committed).** Every white-
noise increment `dW` is drawn from `JitterSource` (apparatus.py): the launch+sync
timing of a tiny GPU kernel (CIRISArray validated TRNG path), low 6 timing bits
→ 24-bit uniforms → Box–Muller normals. **PRNG noise is never used to drive the
dynamics.** Calibration validated the bath as white and Gaussian: mean +0.002,
std 0.999, skew −0.006, kurtosis −0.005, lag-1 autocorr +0.001, KS p=0.86
(`calibration.json`). The physicality of the bath is the point of the experiment.

Maintenance / rent (the `γM` axis, formal core piece 2):
- Passive substrate (maintenance OFF): `B = λ₀ I`, `λ₀ = 1.0` — `k` independent
  oscillators on independent real jitter; passive fixed point `ρ = 0`.
- Maintenance ON: drift `B = (D + Q) C(ρ*)⁻¹` holds stationary covariance
  `C(ρ*)` with antisymmetric circulation `Q` (broken detailed balance → σ>0 → the
  rent). The added force beyond bare relaxation is `u = −(B − λ₀ I) x`.
- **RENT (N1 actuation power)** = `⟨‖u‖²⟩ = Tr[(B−λ₀I) C (B−λ₀I)ᵀ]`; the
  irreversible circulation actuation is `‖Q C⁻¹‖²_F ≡ P` (the N1 budget).
- σ̂ (housekeeping-heat rate) measured by the corridor_ceiling estimator
  (Stratonovich midpoint `σ = ⟨F∘dx⟩/dt`, `F = −D⁻¹B x_mid`), validated in
  calibration to 0.3% vs the analytic `Tr[QᵀD⁻¹QC⁻¹]`.

Constants (frozen): `dt = 0.01`, `λ₀ = 1.0`, `k = 8`, `D = I`, N1 budget
`P = 1.0`. ρ̂ = mean off-diagonal Pearson correlation across the k oscillators over
the ensemble; `k_eff = k/(1+ρ̂(k−1))` (formal core piece 1).

### Caveat C1 — what this substrate is and is not (report with all verdicts)
The bench inherits its **physical noise bath** (real GPU jitter) from CIRISArray,
but the array itself is the abstract equicorrelation OU of the corridor theory —
**not** the 46 s Lorenz CIRISArray oscillator. Its own relaxation time is
`1/λ₀ = 1.0` (≈100 steps); burn-ins below respect several of these. The 46 s
thermalization is a property of the Lorenz substrate, not of this OU. Any claim
that is *guaranteed by the linear/software structure* rather than *measured on the
bath* is flagged per-bet below (Caveat C2/C3).

---

## BET 10 — interventional rent-cut (run FIRST)  [ρ* = 0.30]

Protocol per repeat (≥5 fresh real-jitter realizations):
1. **Passive characterization** (maintenance off): measure `λ₀` from the single-
   oscillator equilibrium lag-autocorrelation (AR fit, zero-mean, lags 1–12);
   **γ̂ = 2·λ₀** with bootstrap CI. Discrete truth = `−ln((1−λ₀dt)²)/dt = 2.01`.
2. **Hold** at ρ*=0.30 with dissipative maintenance (`Q` at budget P): record
   steady-state ρ̂, k_eff, **rent** `⟨‖u‖²⟩`, σ̂ over ≥1000 steps.
3. **REGISTER (in results.json/log, before the cut)** the predicted decay curve
   `ρ(t) = 0 + (ρ*−0)·exp(−γ̂·(t−t₀))`, band = γ̂ ± 2·(bootstrap SE), fp = 0
   (passive fixed point).
4. **Cut** maintenance at t₀ (`B → λ₀ I`); record ρ(t) for 150 steps; fit decay
   rate `γ_cut` by windowed log-linear fit on ρ(t) ∈ [0.15,0.85]·ρ* with
   bootstrap CI (method validated in `_probe_decay.py`: recovers 2.01 ± ~0.05).
   R = 2048 for the decay phase (finite-ensemble ρ̂ floor ≈ 0.022).
5. **Restore** maintenance; record recovery to ρ* and hysteresis
   (∫|ρ_recover − ρ_decay| or the recovery half-time vs decay half-time).

**PASS** = γ_cut CI overlaps the registered γ̂ band, for ≥4/5 repeats, AND rent>0
and σ̂>0 while held (maintained non-equilibrium confirmed), AND rent→0 after cut.
**KILL** = γ_cut inconsistent with γ̂ beyond band in ≥2 repeats (a maintained
residue / non-Markovian bath), **or no decay** (ρ persists rent-free — strongest
kill).

**Caveat C2 (pre-stated, the tautology check the brief demands).** On a *linear*
OU substrate the cut installs the passive generator `λ₀I`, so decay to fp at 2λ₀
is *structurally guaranteed*; "rent-free persistence" is impossible for a stable
linear bath. Therefore the strongest kill limb (no decay) is **a priori off the
table on this apparatus** and a decay-rate match is **not** by itself evidence of
"rent." What bet 10 genuinely measures here: (i) the decay rate is governed by the
**noise bath's own decorrelation** (γ_cut matches the *independently* measured
passive λ₀ — confirming the maintained, circulating state carries **no hidden slow
mode** and real jitter is Markovian), and (ii) maintenance genuinely **costs**
continuous dissipation (rent>0, σ̂>0). To make (ii) load-bearing we also run a
**conservative-maintenance control** (symmetric coupling, Q=0): it holds ρ* with
σ̂≈0 and its correlation *also* decays at 2λ₀ when cut — proving the decay test is
necessary but **not sufficient**; only the σ̂/rent certificate distinguishes a
rented corridor from a free (conservative) one. This distinction is the reported
result, not a bare decay curve.

---

## BET 7 — third-law ceiling (capacity collapse)  [ρ* sweep]

Sweep ρ* ∈ {0.10, 0.20, 0.30, 0.43, 0.50, 0.60, 0.70, 0.80, 0.90} at **fixed N1
actuation budget P = 1.0**. At each ρ*: build the N1-optimal circulation `Q(ρ*,P)`
(apparatus.optimal_Q_N1 — the max-σ pair at budget P; this IS the maintainable
capacity, not an incidental realized σ), set `B=(I+Q)C⁻¹`, integrate with real
jitter (R=256, burn-in 800, measure 2000 steps), **measure σ̂** (capacity). Also
record whether the drift is integrable/holdable (no divergence; ρ̂ tracks ρ*).

Fit `σ̂ = A·(1−ρ)^β` (log–log regression over the sweep); report β with jackknife
CI. Predicted β = 1 (analytic N1: for k≥3 the collapsed-collapsed pair gives
σ_max = P(1−ρ)).

**PASS** = σ̂ **monotone collapsing** with ρ* (σ̂(0.90) < σ̂(0.10)) AND fitted β ∈
[0.6, 1.4]. **KILL** = σ̂ flat or **increasing** toward the pole (β ≤ 0), i.e.
high maintainable σ at ρ ≫ 0.43 — the sealed kill wording.
**AMBIGUOUS** = monotone collapse but β outside [0.6,1.4] (mechanism survives,
exponent off).

**Caveat C3.** Under the pre-committed N1 normalization the collapse exponent is
analytically 1, so a clean pass **confirms the estimator + real-noise substrate
reproduce the predicted capacity collapse** rather than discovering it; the
genuine measurement risk is near the pole (stiff `C⁻¹`, eigenvalue 1/(1−ρ)), where
finite-dt Euler could bias σ̂ high or diverge — a bench inversion there would be a
real (if apparatus-level) kill signal. The N3 (bare-stirring) reading inverts by
construction and is **not** the pre-committed normalization (corridor_ceiling
SUMMARY); we report σ̂/σ_analytic as the faithfulness check.

---

## BET 8 — second-law equality (single-κ fluctuation theorem)  [ρ* = 0.30 and 0.60]

At each ρ*: maintained NESS with circulation Q at budget P (broken DB, σ̂>0).
Collect per-segment total entropy production over segments of length L=50 steps:
`ΔS_tot = W_hk/κ + Δs_sys`, `W_hk = Σ_seg F∘dx` (housekeeping heat over the
segment), `Δs_sys = ½(x_endᵀC⁻¹x_end − x_startᵀC⁻¹x_start)` (Gaussian boundary
term). R = 2048, burn-in 800, 12 segments/replica → 24 576 work samples per ρ*.

Estimator (pre-committed): `κ_bench` solves `⟨exp(−(W_hk/κ + Δs_sys))⟩ = 1` by
Brent root-find on κ ∈ [0.2, 5]; bootstrap 1000× over segments for the CI. Because
D=I sets the bath scale, the model value is κ = 1.

Test at BOTH ρ*: **a single κ must hold across both** (that is the test).
**PASS** = κ_bench CIs at ρ*=0.30 and ρ*=0.60 **overlap** (a single state-
independent bath κ) AND at that common κ `⟨exp(−ΔS_tot)⟩` is within the bootstrap
95% CI of 1, at both ρ*. **KILL** = κ_bench CIs disjoint across the two ρ*, or no
κ ∈ [0.2,5] brings `⟨exp(−ΔS_tot)⟩` to 1 within CI — "no single κ within error".

**Caveat C4.** For *ideal* Gaussian white noise + exact dynamics the integral FT
`⟨exp(−ΔS_tot)⟩=1` is an analytic identity (κ = bath temp), so the pass is
*guaranteed for an ideal bath*. The entire genuine content on this bench is
whether **real GPU jitter + finite-dt discretization** preserve it and yield **one
state-independent κ**: a jitter bath with hidden correlation or non-Gaussianity,
or a mis-set effective temperature, breaks the single-κ FT. Bet 8 here is a test
of the jitter's thermodynamic ideality, and is reported as such.

---

## Addendum 2026-07-12 — Bet 8 estimator correction (pre-first-valid-run)
The original Bet 8 spec above tested `ΔS_tot = W_hk/κ + Δs_sys` with the stochastic
system-entropy boundary term. That estimator is **mathematically ill-conditioned**:
for a Gaussian NESS `xᵀC⁻¹x ~ χ²_k` and `E[exp(+½χ²_k)]` **diverges**, so the
`⟨exp(−ΔS_tot)⟩` sample mean has infinite variance and never converges (the first
run failed with no root, exactly this pathology — not an FT failure). The **sealed
MANIFEST wording** is `⟨e^(−W/κ)⟩ = 1` with `W` the maintenance work; the correct,
well-conditioned observable is therefore the **housekeeping-heat integral FT**
(Speck–Seifert 2005): `⟨exp(−W_hk/κ)⟩ = 1`, `W_hk = Σ_seg F∘dx`, **no boundary
term**. Analytic bath value κ=1 (D=I; g(1/κ)=⟨exp(−W_hk/κ)⟩ is convex with
g(0)=g(1)=1, so κ=1 is the nontrivial root). This honors the sealed wording exactly;
all PASS/KILL thresholds (single state-independent κ across both ρ*; FT=1 within CI)
are unchanged. A convergence diagnostic (top-term fraction of the exp-average) is
recorded per ρ*.

## Discipline
Real jitter only (no PRNG in the dynamics); incremental flush to results.json per
sub-run; all outcomes including kills reported at full weight; every verdict
carries its Caveat (C2/C3/C4) stating what is measured vs structurally guaranteed.
Seeds: real jitter is physically fresh each run; "repeat" = new physical
realization. Fixed integer seed 20260711 used ONLY for bootstrap resampling.
