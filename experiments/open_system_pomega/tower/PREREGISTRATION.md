# P_ω as an explicit finite-dimensional tower — pre-registration

**Date:** 2026-05-21. **Falsification handle:** F-11 / F-12 (P_ω operator
construction). **This is a formal construction, not a data experiment** — the
discipline is: state the target, attempt it, report honestly whether it closes
or hits a *documented obstruction* (a characterised no-go is a result here).

## Where P_ω stands (do not redo this)

Established in `experiments/p_omega_construction/NOTES.md`:

- The **hard projector** P_ω = ∩ per-rung corridor subspaces is **dead** — a
  documented no-go across three models (additive coupling, RG coarse-graining,
  MERA isometry tower): empty for narrow bands, trivial when nested.
- The **soft forward** P_ω = ρ_ss (open-system Lindblad steady state) works.
- The **soft backward** P_ω = E_ω(β) = exp(−β H_sum), H_sum = Σ_n (ρ_n − ρ_c)²,
  β = β_pin = 1/2w², is constructible, escapes the dead zone, and scales to a
  rung budget **R\* ≈ 25–56** — but that scaling was measured with **random
  operators on a fixed-dimension Hilbert space**, and the *faithful* nested-rung
  model was **dimension-capped at 3 rungs** (a faithful nesting has
  dim ~ 2^(2^R) — doubly exponential in rung count).

## The genuine remaining frontier

Two gaps the existing work names but did not close:

1. **A genuine tower, not a fixed-space proxy.** The R\*≈25–56 budget rode on
   random operators sharing one Hilbert space. A faithful construction is a
   *sequence* of finite-dimensional spaces H₀, H₁, …, H_R connected by genuine
   coarse-graining maps W_n (rung n+1's degrees of freedom are coarse-grainings
   of rung n's), each space modest in dimension, the tower deep — so the
   doubly-exponential dimension wall is *tamed by the tower structure itself*
   rather than hit head-on.
2. **Cross-rung structure carried.** The soft toy used H_sum = Σ_n within-rung
   penalties only. ω's property (iii) is the **cross-rung corridor**. A faithful
   E_ω must include cross-rung penalty terms H_{n,n+1} = (τ_n − τ_c)² coupling
   adjacent rungs — which make H_sum a rung-chain Hamiltonian (non-factorising),
   the genuinely hard part. "An explicit tower carrying cross-rung structure" is
   the paper's own phrase (§sec:open-research).

## The construction target

Build the soft backward E_ω on an explicit tower:

- A sequence H₀ → H₁ → … → H_R of finite-dimensional spaces with explicit
  coarse-graining (isometry / RG) maps W_n. Each H_n modest; the tower deep.
- Per-level rung correlation operator ρ_n on H_n; within-rung penalty
  H_n = (ρ_n − ρ_c)².
- **Cross-rung** penalty H_{n,n+1} = (τ_n − τ_c)², τ_n the coupling between
  adjacent rungs through W_n. H_sum = Σ_n H_n + Σ_n H_{n,n+1}.
- E_ω,R(β_pin) = exp(−β_pin H_sum) assembled across the tower (a tensor-network
  / transfer-operator object — the rung-chain structure is 1D-local).
- Scale R well past the framework's 9 rungs — to ≥ R\* (25–56) and beyond — to
  test the budget on the *genuine* tower and probe the inductive limit.

## Pre-registered verdict

- **Constructed:** E_ω is well-defined on the genuine tower, with cross-rung
  terms, at the framework's rung count with margin; the tower structure tames
  the dimension wall; the R\* budget either reproduces or is corrected, stated
  either way. Report whether the strict R→∞ ("cosmological") limit exists, needs
  β-renormalisation, or is moot because the physical rung count is finite — and
  say which, with the math.
- **Documented obstruction:** the genuine tower hits a specific, characterised
  wall the fixed-space proxy hid — e.g. cross-rung terms re-trigger the dead
  zone, or the coarse-graining maps force the RG-subspace / corridor-subspace
  mismatch that killed the hard MERA tower. Characterise it precisely; that is
  an F-11/F-12 result.

## Discipline

- **CUDA mandatory.** The tower's dimension scales fast; use `cupy`, complex64
  (the established pattern — `deadzone_rung_scaling.py` ran GPU complex64 in
  ~70 s against a 35-min fp64 CPU run). Fall back to CPU only with the fallback
  stated in the output.
- Incremental output: flush per-rung-depth results as computed, so a wedge
  leaves recoverable partial work.
- This is a math construction — no synthetic *data*; the honesty constraint is
  that the construction be genuine (real coarse-graining maps, real cross-rung
  terms), not a relabelled fixed-space proxy.
- Report a no-go as a result. F-11/F-12: a documented obstruction is as
  informative as a successful construction.
