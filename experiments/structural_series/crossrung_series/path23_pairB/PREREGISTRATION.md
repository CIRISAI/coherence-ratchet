# Pre-registration — Paths 2-3, Pair B: the canonical timescale g/J at the LLM internal→external rung pair

Committed BEFORE any results, in a SEPARATE commit that PRECEDES the results
commit; git history is the proof. See `../PROTOCOL.md` for the six-pair series
and `../path1_tau/` for Path 1 (the coupling-RATIO measurement at the same pair).

## 0. What this run settles, and why it is at-risk

`StructuralClaims.lean` Claim 6 (amended) is a statement about **g/J**, where
the PROTOCOL fixes the canonical meaning of g and J as **TIMESCALES**:

- `g` — the cross-rung coupling: how strongly rung-n dynamics drive rung n+1.
- `J` — "the rung's intrinsic dynamical rate ... relaxation timescale⁻¹".

Path 1 measured a *coupling RATIO* (mutual-information-based, a single forward
pass over fixed text, no time axis). The PROTOCOL is explicit that the timescale
g/J and the coupling-ratio g/J **may come apart** — the framework "owes either
(a) a demonstration that the relaxation-timescale g/J can be ≳ 3 while the
coupling-strength ratio is ≈ 1 ... or (b) a retraction." The canonical
timescale g/J has been measured at **ZERO rung pairs**. This run is the first
attempt.

Pair A (TCGA) is structurally infeasible for a timescale: cross-sectional data,
no time axis. Pair B (LLM internal→external) is the only runnable attempt — and
it is at-risk. A prior LLM timescale measurement
(`experiments/open_system_pomega/corridor_exit_rate_llm.py`) was **nulled**: a
24-token windowed-k_eff observable over an LLM generation was too noisy /
window-dominated to be a corridor trajectory. The C. elegans corridor-relaxation
run (`../../corridor_dynamics/celegans/`) pre-registered a window-domination
gate and **failed it** (window-dominated null). This run inherits that gate.

**HONEST NULL is a valid, valuable outcome.** If the timescale observable is
window-dominated, the result is: "the canonical timescale g/J is
observable-blocked at the LLM substrate" — which, combined with Pair A's
infeasibility, would mean the canonical Claim 6 quantity is not measurable at
any of the available pairs. That is important and is reported plainly.

## 1. Models and the time axis

- Models: `gpt2`, `EleutherAI/pythia-160m`, `Qwen/Qwen2.5-0.5B` — the same three
  open HuggingFace models used in Path 1 Pair B and Test E1. Real weights only.
  If a model fails to load it is recorded as not-run, not fabricated.
- **The time axis is the generated token sequence.** From each prompt, the
  model generates `N_GEN = 512` tokens autoregressively with
  `output_hidden_states=True`. Token position `t = 0 ... N_GEN-1` is the
  discrete time index. One generated sequence per (model, prompt).
- Decoding: **temperature sampling, T = 1.0** (fixed seed per (model, prompt)).
  Sampling — not greedy — is the pre-registered choice: greedy decoding was a
  named failure cause in `corridor_exit_rate_llm.py` (it produces neither a
  clean corridor nor a clean exit; it collapses to repetition for some
  prompt/model pairs, pinning the observable). Sampling keeps the sequence a
  live trajectory through the corridor, which is what a relaxation rate is
  defined on. No exit event is needed or sought here — Paths 2-3 measure
  *relaxation rates of a stationary-in-corridor trajectory*, not an exit rate.
- Prompts: a FIXED set of 8 diverse prompts (`PROMPTS` in the script, committed
  with this pre-registration). 3 models × 8 prompts = 24 generated sequences;
  each gives one independent (J_internal, J_external, g) triple. The
  across-sequence spread is the reported uncertainty.

## 2. The two within-rung observables (defined HERE, before results)

At each generated token position `t` the forward pass yields:
- `h_t` — the hidden-state vector at a fixed mid-depth layer
  `layer = num_hidden_layers // 2` (the Path 1 / E1 mid-layer choice), the
  LLM-INTERNAL rung.
- `logit_t` — the next-token logit vector, the LLM-EXTERNAL rung.

The framework's within-rung observable is the correlation structure of a rung.
To get a SCALAR time series per rung — the thing a relaxation rate is defined on
— we need a per-token reduction of that structure. The prior failure used a
sliding-window k_eff; that window IS the window-domination risk. We pre-register
**two** internal/external scalar observables, computed and gated independently,
so the result does not hinge on one fragile construction:

### 2.1 Observable family I — windowless per-token projection (primary)
For each rung, a per-token scalar that needs **no sliding window** and so cannot
be window-dominated by construction:
- `s^int_t` = projection of `h_t` onto the top principal component of the
  hidden-state matrix `H = [h_0; ...; h_{N_GEN-1}]` (PC computed once over the
  whole sequence, fixed). This is the dominant internal coordinate — the
  LLM-internal analogue of C. elegans PC1.
- `s^ext_t` = projection of `logit_t` onto the top principal component of the
  logit matrix `L`. The dominant external coordinate.
Both are z-scored over `t`. These observables have NO window, so their
autocorrelation is a genuine property of the generation dynamics, not a window
artifact. Family I is the **primary** observable.

### 2.2 Observable family II — windowed correlation scalar (secondary, gated)
The framework's literal within-rung quantity is a correlation among
constituents, which needs a window. For each rung, on a sliding window of
`W_TOK` token positions:
- `c^int_t` = mean |Pearson| among a fixed seed-256 subsample of hidden units,
  over the window `[t-W_TOK, t]` (the Path 1 `within_rung_W` construction,
  windowed in time).
- `c^ext_t` = mean |Pearson| among the top-256-variance logit coordinates over
  the same window.
Window length `W_TOK = 32` tokens (fixed; matched in spirit to the prior failed
attempt's 24 so the comparison is honest). Family II is **secondary** and is
reported ONLY if it clears the window-domination gate (§4); if it fails the gate
it is reported as a window-dominated null and excluded from the verdict.

## 3. The three measured quantities

For each (model, prompt) sequence, on EACH observable family:

### 3.1 J_internal, J_external — within-rung relaxation rates
The relaxation rate is the rate constant of return after a fluctuation — the
same two pre-committed estimators as the C. elegans run, on the per-token series
`x_t` (= `s^int_t` / `s^ext_t` for family I; `c^int_t` / `c^ext_t` for II):

**(a) Autocorrelation e-folding time `tau_ac`.** ACF of mean-subtracted `x_t`;
fit `ACF(lag) = exp(-lag/tau_ac)` over lag 0 to the first zero-crossing (or
3·tau_ac, whichever first; if no crossing, to lag = N_GEN/4). `tau_ac` is in
units of tokens. Relaxation **rate** `J = 1 / tau_ac` (units 1/token). Also
report the fit-free integrated autocorrelation time `tau_int = 1 + 2·Σ ACF(lag)`
to the first zero-crossing as a cross-check.

**(b) OU mean-reversion `theta`.** Model `x_t` as Ornstein–Uhlenbeck:
`dx = -theta·(x - x̄) dt + σ dW`. Estimate `theta` by lag-1 autoregression:
regress `(x_{t+1} - x_t)` on `(x_t - x̄)`; slope is `-theta` (dt = 1 token), so
`theta = -slope`. For a pure exponentially-correlated process `theta ≈ 1/tau_ac`;
reporting both checks consistency.

`J_internal` = the rate from the internal observable; `J_external` = from the
external observable. Headline `J` uses estimator (a); (b) is the cross-check.
The pair's within-rung scale for the ratio is `J_within = sqrt(J_int · J_ext)`
(geometric mean — the Path 1 pre-registered choice, for the same reason: the two
rungs are different scales and the ratio must not be dominated by whichever rung
relaxes faster).

### 3.2 g — cross-rung coupling (a lagged / causal measure)
`g` is how strongly the INTERNAL dynamics drive the EXTERNAL — a directed,
lagged quantity (the internal hidden state at step t causally feeds the logits;
the framework's cross-rung coupling is this drive). Pre-registered estimator:

**Lagged predictive coupling.** Fit two nested linear models for the external
observable one step ahead:
- restricted: `x^ext_{t+1} ~ x^ext_t` (external's own autoregression).
- full: `x^ext_{t+1} ~ x^ext_t + x^int_t` (adds the internal state at lag 1).
`g_raw` = the reduction in residual variance from adding `x^int_t`:
`g_raw = 1 - Var(resid_full) / Var(resid_restricted)` — the partial R² of the
internal observable predicting the next external value, controlling for external
autocorrelation. This is a Granger-style directed coupling: internal→external
predictive gain beyond what external predicts about itself. `g_raw ∈ [0, 1]`.

**Debiasing.** `g` is positively biased at finite N (an extra regressor always
explains some variance). Debias against a **block-shuffle null**: the internal
series is permuted in contiguous 16-token blocks (preserving internal
autocorrelation, destroying the internal→external timing alignment),
`N_SHUFFLE = 50` times; `g_floor` = mean null partial R². Reported coupling
`g = max(g_raw - g_floor, 0)`. If `g / g_raw < 0.3` the coupling is flagged
noise-dominated for that sequence.

`g` is dimensionless (a variance ratio in [0,1]); `J` is a rate in 1/token. They
are NOT the same units. To form a dimensionless **timescale g/J** the convention
is fixed here, before results: `g` is converted to a rate by interpreting the
one-step partial R² as a per-token coupling rate `g_rate = -ln(1 - g)` (the
continuous-time decay rate whose one-step survival is `1-g`; standard
discrete→continuous rate conversion, fixed, not tuned). Then

```
timescale g/J  =  g_rate / J_within
```

both in 1/token, ratio dimensionless. The conversion `-ln(1-g)` is monotone and
≈ g for small g, so it does not distort the comparison; it is stated explicitly
so the number is reproducible.

### 3.3 coupling-ratio g/J — Path 1's method, re-run on the SAME sequences
So the timescale ratio and the coupling ratio can be DIRECTLY compared at the
same pair, the Path 1 construction is also computed here, on the generated
sequences (Path 1 used a single non-generated forward pass; re-running its
method on the generated token axis makes the two ratios same-data comparable):
`tau_MI` = normalised cross-rung Gaussian MI `I(R_int;R_ext)/min(H_int,H_ext)`
(the `crossrung_lib.cross_rung_tau` estimator, imported, unchanged);
`W_within` = `sqrt(W_int·W_ext)` of the within-rung mean-|Pearson| couplings
(`crossrung_lib.within_rung_W`, unchanged). `coupling-ratio g/J = tau_MI /
W_within`. This reuses Path 1's audited code verbatim.

## 4. The window-domination GATE (pre-committed, mandatory)

Mirrors the C. elegans pre-registration's gate exactly. A relaxation timescale
`tau_ac` measured on a windowed observable is meaningless if it is merely the
autocorrelation the window mechanically imposes.

**GATE:** for a measured `J` (i.e. `tau_ac`) on a given observable family to
ENTER the verdict, the relaxation timescale must exceed the analysis window by a
stated margin:

```
tau_ac  >  MARGIN · W_eff
```

with **MARGIN = 2.0** (fixed). `W_eff` is the effective window:
- Family I (windowless projection): `W_eff = 1` token — there is no sliding
  window, so the gate is `tau_ac > 2` tokens, i.e. the only requirement is that
  the observable has resolvable autocorrelation at all (a tau_ac of 1 token is
  white noise and carries no rate). Family I is expected to clear this trivially
  unless the projection series is pure white noise.
- Family II (windowed correlation scalar): `W_eff = W_TOK = 32` tokens, so the
  gate is `tau_ac > 64` tokens. This is the demanding gate — the one the prior
  attempt and C. elegans failed.

**Second gate condition — surrogate null.** For each sequence, 100
phase-randomised surrogates of the observable (preserves its power spectrum,
destroys genuine dynamics). If the real `tau_ac` lies inside the surrogate
`tau_ac` distribution (within its 5–95% range), the rate is not distinguishable
from windowed/colored noise → that sequence's `J` is a surrogate null.

**Verdict rule for the gate:**
- An observable family PASSES if, across the 24 sequences, the MAJORITY
  (≥ 13/24) clear BOTH gate conditions (`tau_ac > MARGIN·W_eff` AND outside the
  surrogate band) for BOTH rungs.
- If family I passes: the timescale g/J is reported from family I.
- If family I fails but family II passes: reported from family II.
- If BOTH fail: **HONEST WINDOW-DOMINATION NULL** — "the canonical timescale
  g/J is observable-blocked at the LLM substrate." No g/J number is claimed.
- A `g` (cross-rung coupling) is additionally required to be non-noise-dominated
  (`g/g_raw ≥ 0.3`) in the majority of sequences for the timescale g/J to be
  reported; if `g` itself is noise, that is reported as a coupling null.

## 5. The verdict (pre-committed)

IF the gate passes and a timescale g/J is obtained, AND the coupling-ratio g/J
is obtained on the same sequences, the two are compared:

- **AGREE** — the timescale g/J and the coupling-ratio g/J are the same order
  of magnitude (their ratio is within [1/3, 3]). Then Claim 6's two
  operationalisations of "dominance/coupling" coincide at Pair B; the amended
  Claim 6 (g/J ~ O(1)) is supported on the canonical timescale quantity, not
  only on the Path 1 ratio.
- **COME APART** — the two ratios differ by more than 3×. Then Claim 6 needs
  structural re-articulation about WHICH ratio is canonical: the PROTOCOL names
  the timescale as canonical, so a divergence means the Path 1 result does not
  transfer, and the framework owes the re-articulation the PROTOCOL flagged.
- The timescale g/J is ALSO checked against the amended Claim 6 band
  (`CouplingComparable`: g/J ~ O(1), the Path-1 measured 0.47–1.47). A timescale
  g/J inside O(1) corroborates the amended claim; one at a pole (≪1 or ≫1) on a
  pair whose multi-rung corridor is satisfied is a `Falsifier6` witness candidate
  and is reported as such.

## 6. Confounds and controls (specified before the result)

- **Window-induced autocorrelation** — the headline risk; handled by the §4
  gate. Family I is windowless to side-step it; family II is gated hard.
- **Token-position autocorrelation in `g`** — adjacent tokens are not
  independent, so a naive internal→external coupling inherits trivial timing
  alignment. Controlled by the block-shuffle null (§3.2), which preserves
  internal autocorrelation and destroys only the cross-rung alignment.
- **Architectural cross-rung link** — logits are a learned linear readout of the
  final hidden state; Path 1 flagged Pair B as the weaker pair for exactly this.
  The mid-depth layer (not the final layer) is used for the internal observable
  so the internal→external map is not the identity readout; the caveat still
  stands and is restated in the result.
- **Repetition collapse** — if a generated sequence degenerates to a repeating
  loop the observables go constant and `tau_ac` diverges spuriously. Detected:
  any sequence whose last 64 tokens contain < 8 distinct token ids is flagged
  degenerate and excluded from the verdict (reported separately). Sampling at
  T = 1.0 makes this rare but the check is pre-committed.
- **Sequence-length sensitivity** — `tau_ac` estimation needs N_GEN ≫ tau_ac.
  N_GEN = 512 fixed; if a passing family's median tau_ac exceeds N_GEN/8 = 64
  tokens the estimate is flagged length-limited and reported with that caveat.

## 7. Fixed parameters (no tuning)

```
MODELS      = gpt2, EleutherAI/pythia-160m, Qwen/Qwen2.5-0.5B
N_GEN       = 512 tokens generated per sequence
N_PROMPTS   = 8  (fixed list in the script)
DECODING    = temperature sampling, T = 1.0
LAYER       = num_hidden_layers // 2  (mid-depth)
D_SUB       = 256  (hidden-unit / logit-coord subsample, family II + Path-1 ratio)
W_TOK       = 32   (family II sliding window)
MARGIN      = 2.0  (window-domination gate margin)
N_SHUFFLE   = 50   (g block-shuffle null)
N_SURROGATE = 100  (phase-randomised surrogate null for tau_ac)
BLOCK       = 16   (g null block length)
SEED        = 17   (matches the existing pipeline)
```

## 8. Honest prior

The honest prior is that this run is MORE LIKELY than not to hit a null, because
two prior LLM/biological timescale attempts on windowed corridor observables
both failed window-domination. Family I (windowless PC projection) is the
deliberate design response: it removes the sliding window entirely, so its only
failure mode is the projection series being genuine white noise — which would
itself be an informative result (the LLM-internal dominant coordinate has no
relaxation dynamics along the token axis). If family I passes and family II
fails, that is the expected and reportable shape. A clean pass on both, with a
timescale g/J that AGREES with Path 1's coupling ratio, is the strong outcome
and is not the prior expectation. The numbers are reported either way.
