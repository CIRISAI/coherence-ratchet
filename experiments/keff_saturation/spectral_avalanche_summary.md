# Observable-collision test: neuronal avalanches vs. covariance saturation

**Question.** Does neuronal **avalanche criticality** (Beggs & Plenz 2003 — the third
pillar of criticality-in-biology, defined on the **avalanche-size distribution**,
power-law with τ≈3/2) **collide** with our **covariance-saturation** reading (defined
on the **covariance eigenspectrum**, k_eff = participation ratio)? Or are they two
observables passing in the night — a system can be "critical by avalanches" **and**
"low-dimensional by covariance" at the same time? We measure **both on the same data**.

## Dataset

Wagenaar, Pine & Potter (2006), *"An extremely rich repertoire of bursting patterns
during the development of cortical cultures"*, BMC Neuroscience 7:11. Dense dissociated
rat cortical cultures on 60-channel MEAs, 30–45 min spontaneous recordings. Public
archive (Potter lab, Georgia Tech):
`https://potterlab.bme.gatech.edu/development-data/simple-text/daily/spont/dense/`.
Same in-vitro cortical-MEA paradigm as the canonical avalanche work of Beggs & Plenz.
Format: two columns per line = (spike_time_s, channel 0..59). Five mature cultures
(DIV 25–33), 0.18M–1.9M spikes, 56–58 active electrodes. **Real data only.**

## Two observables, same recordings

**(a) THEIR observable — avalanche-size distribution.** Pool all electrodes, bin at
`dt = mean inter-event interval` (the canonical Beggs–Plenz bin). An avalanche = a
maximal run of consecutive non-empty bins flanked by empty bins; size S = spikes in
the run. Fit `P(S) ~ S^-τ` by discrete Clauset MLE with KS-optimal x_min, plus a
per-point log-likelihood ratio vs. an exponential alternative (`llr_z`; >0 and |z|>2
⇒ power-law preferred). Branching parameter σ reported as a secondary check.

**(b) OUR observable — covariance saturation** (reusing `spectral_test.py` core:
`corr_eig`, `participation_ratio`, `mp_edge`, `phase_randomize`, `subsample_pr`).
Channel × time spike-count matrix at 20 ms. k_eff = PR of the correlation
eigenspectrum; effective rank = eigenvalues above a phase-randomized surrogate floor;
PR subsampling exponent β. β≈0 & small rank ⇒ bounded/low-dimensional; 0.3–0.8 ⇒
scale-free growth. Calibrated at N=58, T=1800 (low-rank β=0.08, power-law β=0.4–0.7,
noise β=0.98).

## Results

| culture | τ (size, events) | KS | llr_z vs exp | σ | ‖ | PR (k_eff) | eff.rank | β | covariance verdict |
|---------|-----------------:|----:|-------------:|----:|---|-----------:|---------:|-----:|--------------------|
| 1-1-25  | **1.47** | 0.053 | +26.8 | 0.14 | ‖ | **1.48** | 1 | 0.016 | LOW-RANK / bounded |
| 6-1-25  | **1.77** | 0.116 | +57.4 | 0.33 | ‖ | **1.47** | 2 | 0.010 | LOW-RANK / bounded |
| 2-1-25  | 2.67 | 0.139 | +10.2 | 0.62 | ‖ | 4.98 | 2 | 0.098 | LOW-RANK / bounded |
| 2-2-25  | 3.15 | 0.155 | +16.9 | 0.66 | ‖ | 3.36 | 1 | 0.053 | LOW-RANK / bounded |
| 2-1-33  | 3.59 | 0.324 | +33.6 | 0.54 | ‖ | 2.16 | 2 | −0.003 | LOW-RANK / bounded |

(τ at the canonical `dt = mean IEI`; PR/β at 20 ms. Full bin-sweep in
`spectral_results_avalanche.json`.)

**The avalanche observable (a).** Every culture has a heavy-tailed, power-law-preferred
size distribution (llr_z ≫ 2 vs. exponential everywhere). The *exponent* varies: one
culture (**1-1-25**) is a textbook Beggs–Plenz critical avalanche — **τ = 1.47**, KS =
0.05 — and a second (**6-1-25**) is near-critical (τ = 1.77). The other three are
steeper (τ = 2.7–3.6), i.e. burst-dominated / not cleanly critical, as dissociated
cultures famously are relative to organotypic slices.

**The covariance observable (b).** **LOW-RANK / bounded in all five cultures**, with no
exception: PR (k_eff) = 1.5–5.0, effective rank 1–2 above the surrogate floor, β ≈ 0
(−0.003 to 0.10). The covariance eigenspectrum is a few spikes on a flat noise bulk —
maximally low-dimensional — regardless of where the avalanche exponent lands.

## Verdict: the two observables PASS — they do not collide

The decisive case is culture **1-1-25**: **avalanche-critical (τ = 1.47, the canonical
3/2) *and* maximally covariance-bounded (k_eff = 1.48, effective rank 1) in the same
recording.** Avalanche criticality here co-occurs with the *lowest possible* covariance
dimensionality. Criticality-by-avalanches does **not** imply high covariance rank, and
covariance-boundedness does **not** require a steep (subcritical) avalanche tail: across
the five cultures the avalanche exponent moves over 1.47 → 3.59 while the covariance
verdict never budges from LOW-RANK. **The two measures are statistically independent on
this data — two observables passing in the night.**

- **PASS (avalanche-critical + covariance-bounded, same recording): 1 culture (1-1-25).**
- **COLLIDE (avalanche-critical + covariance NOT bounded): 0 cultures.**
- Covariance bounded in **5/5** regardless of avalanche shape.

**This confirms the prior-art finding:** avalanche criticality (a size-distribution
observable) and our covariance low-dimensionality (an eigenspectrum observable) are
**compatible**, so **neither refutes the other**. A system flagged "critical" by
Beggs–Plenz avalanches is not thereby high-dimensional in covariance, and our
covariance-saturation result at C. elegans / cortex does not contradict the neuronal-
avalanche literature. They measure different things.

## Caveats (grain)

- **Wrong-grain / subsampling.** An MEA samples a ~2 mm patch and only 60 electrodes of
  a whole culture — the same wrong-grain caveat as sampling a cortical patch. Heavy
  electrode subsampling is known to **bias the naive branching parameter σ downward**
  and **steepen apparent τ** (Priesemann/Wilting). That is exactly what we see (σ =
  0.14–0.66 < 1, and inflated τ in the burst-dominated cultures); we therefore key the
  "avalanche-critical" call on the **size-distribution exponent + goodness-of-fit**, not
  on σ. The subsampling artifact affects observable (a); it does not rescue any
  collision, because observable (b) is bounded independent of it.
- **Dissociated ≠ organotypic.** These are dissociated cultures; clean τ≈1.5 criticality
  is more characteristic of Beggs–Plenz organotypic slices. We still recover it in one
  culture and near it in a second, which is sufficient for the collision test.
- The avalanche bin and exponent are bin-sensitive (full sweep at ×1/×2/×4 mean-IEI in
  the JSON); the covariance verdict is bin-robust (bounded at both 20 ms and dt = mean
  IEI in every culture).

## Files

- `spectral_avalanche.py` — analysis (reuses `spectral_test.py` core).
- `spectral_results_avalanche.json` — per-culture avalanche fits (all bins) + covariance readouts + β calibration.
- Raw data downloaded to scratchpad (not committed); source URL above.
