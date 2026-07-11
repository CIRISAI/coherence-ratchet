# Functional falsification — is the log-det copula functional specific, or is the DESI fit family-generic?

**Date 2026-07-10.** Pre-committed design: `DECISIONS.md` (both outcomes and their meanings
stated before any fit). Every alternative functional computed on the SAME TNG300-1 halo
catalogs, mapped through the SAME stock rule ρ_DE ∝ F(a) (comoving), fit with the SAME official
DESI DR2 likelihood + θ* anchor and the same two fitted parameters (Ω_m, scale) as the
framework row. Data: `results.json`.

## Verdict: PARTIAL SPECIFICITY — and the specific thing selected is the amplitude-blindness theorem

**Between families, the discrimination is decisive.** Every amplitude-carrying functional
fails, in the direction and for the reason the framework's copula-blindness theorem predicts
(amplitude growth drags F(a) monotone-up → phantom, no interior peak, bad fit):

| functional (with θ* anchor) | w_today | interior peak | χ² | AIC | verdict |
|---|---|---|---|---|---|
| **framework: extensive log-det S** (frozen) | −0.833 | z = 0.59 | **8.86** | **12.86** | best AIC |
| S/k intensive (decomposition row) | −0.936 | z = 0.79 | 8.66 | 12.66 | statistically tied |
| F4: k(a) unit count alone | −0.898 | z = 0.55 | 9.87 | 13.87 | quadrant, mid |
| F1: Shannon config entropy (mass-wtd) | −0.974 | z = 2.32 | 9.83 | 13.83 | quadrant, mid |
| F1: Shannon config entropy (count) | −0.997 | z = 0.79 | 10.22 | 14.22 | ≈ ΛCDM |
| **ΛCDM** | −1 | — | 10.32 | 14.32 | anchor |
| F2: marginal negentropy (count / mass) | −1.08 / −1.30 | none | 13.3 / 29.1 | 17.3 / 33.1 | **FAILS** |
| F3: variance σ² (count / mass) | −1.11 / −1.77 | none | 15.0 / 95.4 | 19.0 / 99.4 | **FAILS** |
| F5: PEDE (external zero-param model) | −1.145 | none | 26.2 | 30.2 | **FAILS** |
| CPL (2 extra fitted params) | fitted | — | 6.90 | 14.90 | fitted ceiling |

- **Sarkar-class marginal negentropy fails** (the priority-sweep's closest-on-functional
  neighbor) — its one-point information is exactly what the copula functional is blind to, and
  the data reward the blindness.
- **The pure-amplitude control (σ²) fails worst** — the amplitude-blindness theorem
  (`participation_scale_invariant` / copula invariance) is not just proved, it is what the DR2
  likelihood empirically selects for.
- **PEDE — the literature's zero-parameter competitor — fails badly on DR2** (χ² 26.2 vs
  ΛCDM 10.3): the "other models with the same claim" question has a number, and the answer is
  that the known zero-parameter alternative is excluded where ours is preferred.
- **Das–Pandey-class Shannon configuration entropy** lands mid-pack: count-weighted ≈ ΛCDM;
  mass-weighted beats ΛCDM but trails the framework, with a physically strange early peak
  (z = 2.3) that DR2 distances barely notice.

**Within the family, DR2 distances cannot discriminate.** Extensive log-det (8.86), intensive
S/k (8.66), and even the bare unit count k(a) (9.87) all land in the DESI quadrant; Δχ² ≲ 1 at
identical parameter count is noise. Honest deflation, stated plainly: much of the fit is
carried by the halo-formation epoch structure itself, and the log-det adds ~Δχ² = 1 beyond pure
counting. "Club of one" deflates to **"club of one family, whose membership card is
amplitude-blindness"** — the copula/count class is specifically favored over everything the
adjacent literature actually proposes, but the specific convention (extensive vs intensive vs
count) is not separable by present distance data.

## Consequences

1. **For the letter:** the defensible uniqueness claim is the FAMILY claim, with the theorem as
   the differentiator: *amplitude-blind structure functionals fit DR2; amplitude-carrying ones
   fail; the known zero-parameter competitor fails.* The frozen extensive convention stays (per
   the preregistration) but must not be oversold as uniquely selected by χ².
2. **The within-family discriminator is the crossing epoch** — the variants' interior peaks
   differ (0.55 / 0.59 / 0.79 / 2.3) where their distance-χ² do not. DR3's crossing posterior
   is therefore not only the law's test but the convention's.
3. **The S/k wrinkle, on record:** the intensive variant — the one T-E3's discipline prefers
   and the one the P4 fence used as the controlled measure — fits DR2 distances as well as the
   frozen extensive choice (8.66 vs 8.86, indistinguishable). This cuts both ways: it removes
   any suspicion that the extensive convention was χ²-selected, and it means the
   convention-level claim is weaker than the family-level claim. Both statements go in the
   paper.

## Caveats

Halo-field operationalizations of full-field functionals (Das–Pandey/Sarkar defined on the
matter field; here computed on the same halo catalogs our functional used — apples-to-apples
internally, but not a literal reproduction of their pipelines); grid-scale sensitivity checked
at 2 vs 4 Mpc/h (verdicts stable); single box; no SNe likelihood; θ* anchor approximation
inherited from `../desi_likelihood_v2/`.

*(Summary written by the orchestrating session from the agent's completed results.json after
the agent idled; all numbers are the agent's executed output.)*
