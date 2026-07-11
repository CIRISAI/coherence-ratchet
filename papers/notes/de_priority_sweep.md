# Dark-energy priority & novelty sweep — the log-det-correlation sign law

**Date 2026-07-10.** Companion to `dark_ledger_convergent_art.md` (the four-pillar DM/DE prior-art
map) and `lambda_maintenance_wz.md` (the sign law itself). Scope is narrow and specific: is the
object

> `ρ_DE = κ·S(a)` with `S = −ln det C` (Gaussian multi-information / log-det of the normalized
> LSS correlation matrix) → the parameter-free **stock sign law** `1 + w(a) = −(1/3) dlnS/dlna`
> (κ cancels) → a frozen, pre-registered `w(z)` computed from N-body halo catalogs, landing
> **1.36σ from DESI DR2** (vs ΛCDM 3.28σ)

claimable as novel, and what must be cited so no wheel is re-invented?

Same house grades: **NEAR-IDENTICAL / CONVERGENT / ADJACENT / DISTINCT**.

---

## Verdict, up front

**The composite object is claimable as novel — but only as a composite, and only if four
convergent works are cited prominently.** There is a real, populated literature of
"entropy-of-cosmic-structure tracks the dark-energy equation of state." No published work uses
*this* functional (`−ln det C`, the Gaussian multi-information) with *this* logic (stock mapping,
κ-cancelling parameter-free sign law) validated with *this* discipline (frozen pre-registration +
logged kill conditions). But the field is close enough that omitting the Das–Pandey configuration-
entropy program, Sarkar's negentropy diagnostic, or Pandey's entropic-backreaction paper would
read as either ignorance or concealment. **No single wheel is fully re-invented; several are
adjacent enough that the paper must position against them explicitly, not just cite them.**

**Three closest works.**
1. **Das & Pandey, *Can we constrain the DE EoS parameters using configuration entropy?*** (MNRAS
   492, 3928, 2020; arXiv:1907.00331) — **CONVERGENT**, closest on *purpose*. Same target
   (structure-formation entropy → `w(z)`), opposite logical direction (they *constrain* `w₀,wₐ`
   from the entropy-rate minimum; we *derive* `w(z)` parameter-free) and a different functional
   (Shannon configuration entropy `−∫ρ ln ρ`, not log-det `C`).
2. **Sarkar, *Negentropy as Diagnostic of Cosmic Density Fields and Dynamical DE Models***
   (arXiv:2602.02339, Feb 2026) — **CONVERGENT** in spirit, but **complementary — nearly the
   orthogonal object.** *Resolved (2026-07-10, ar5iv full text):* Sarkar's negentropy is a
   **ONE-POINT** quantity, `J(σ) = (h_δ)_N − (h_δ)_LN = ½ ln[σ²(1+σ²)/ln(1+σ²)]` (his Eqs.
   2.16–2.17), the non-Gaussianity of the **marginal** PDF of the density contrast δ, computed from
   the 1-point PDF (Shannon entropy of binned δ), and used in a **Fisher forecast** to constrain
   `(w₀,wₐ)` across CPL/JBP/BA. That is precisely the information our functional is **blind** to:
   `−ln det C` (multi-information) depends only on the **copula**, not the marginals, and is
   invariant under exactly the per-component transforms whose marginal-non-Gaussianity `J` measures.
   The two are near-orthogonal decompositions of the same field — Sarkar reads the marginal, we read
   the correlation structure — and his is a diagnostic, ours a parameter-free derivation. **This
   sharpens the novelty; it does not weaken it.**
3. **Pandey, *Entropic backreaction from cosmic structure formation*** (arXiv:2605.28797, 2026) —
   **CONVERGENT**, closest on the *mechanism* (`ρ_DE` sourced by structure-formation entropy).
   Differs on all three of functional (Shannon `S_c`), mapping (**rate**, `ρ_S = −α Ṡ_c/V`, with a
   **free** α), and target (H₀/S₈ tensions, not a `w(z)` sign law).

**The differentiator, in one sentence.** Everyone in this space uses the **Shannon configuration
entropy of the density field** as either a **diagnostic** (Das–Pandey, Sarkar) or a **rate-mapped,
free-parameter** DE source (Pandey backreaction); ours is the **Gaussian multi-information**
`−ln det C` (a copula quantity, provably blind to linear growth — the amplitude/shape fence), fed
through a **stock** mapping whose proportionality constant **cancels**, giving a genuinely
parameter-free sign law, then **frozen and pre-registered** before the large-volume box.

---

## The finds

| # | Work | Cite | Grade | One-line differentiator |
|---|---|---|---|---|
| 1 | Das & Pandey, *Constrain DE EoS with configuration entropy* | MNRAS 492, 3928 (2020); arXiv:1907.00331 | **CONVERGENT** | Shannon `S_c=−∫ρlnρ`; *constrains* `w₀,wₐ` from entropy-rate minimum (inverse direction); no `ρ_DE∝S` posit |
| 2 | Das & Pandey, *Configuration entropy in ΛCDM vs dynamical DE* | MNRAS 482, 3219 (2018); arXiv:1810.07729 | **CONVERGENT** | Same `S_c`; entropy evolution as a *diagnostic* to distinguish ΛCDM from DDE; no sign law, no derivation |
| 3 | Sarkar, *Negentropy as Diagnostic of Cosmic Density Fields & DDE* | arXiv:2602.02339 (Feb 2026) | **CONVERGENT (complementary)** | Negentropy `J = ½ln[σ²(1+σ²)/ln(1+σ²)]` is **one-point marginal** non-Gaussianity — the copula-orthogonal complement of our `−ln det C`; diagnostic/Fisher-forecast, not derived `w(z)` |
| 4 | Pandey, *Entropic backreaction from cosmic structure formation* | arXiv:2605.28797 (2026) | **CONVERGENT** | `ρ_S=−α Ṡ_c/V`: Shannon `S_c`, **rate** mapping, **free** α; targets H₀/S₈, not a parameter-free `w(z)` |
| 5 | Bianconi, *Thermodynamics of the Gravity from Entropy Theory* | arXiv:2510.22545 (Oct 2025) | **NEAR-IDENTICAL (premise), DISTINCT (object)** | The maintenance reading is built *on* this (`ℋ=Λ^G`); but Λ^G is a metric-ratio Bregman divergence, **not** computed from the LSS density correlation matrix |
| 6 | Bianconi, *Gravity from entropy* | PRD 111, 066001 (2025); arXiv:2408.14391 | **NEAR-IDENTICAL (premise)** | Parent of the whole gravity-is-a-ledger reading; G-field → dark **energy** (w=−1), no LSS-computed `w(z)` |
| 7 | Das/others, *Config. entropy in Tsallis holographic DE* | arXiv:2011.13135; EPJC 81 (2021) | **DISTINCT** | Holographic IR-cutoff DE with free params; config entropy used only as a growth diagnostic |
| 8 | *Holographic DE models with configuration entropy* | arXiv:2011.07337; RAA 23 (2023) | **DISTINCT** | Same holographic family; entropy as post-hoc growth check |
| 9 | *Extended Entropic Dark Energy with Four Free Parameters* | arXiv:2511.15747 (2025) | **DISTINCT** | Parameterized entropic-DE `w(z)` *fit* to data, not computed from a field |
| 10 | Rimes & Hamilton; Carron; Carron & Neyrinck | MNRAS 360/416 (2005/06); PRD 84 (2011); PRL 109 (2012) | **ADJACENT** | The ancestor of "non-Gaussian information escapes `P(k)`" — the reason a multi-information sees shape the power spectrum misses — but never mapped to DE/`w(z)` |
| 11 | Buchert morphon; Räsänen; Wiltshire timescape | gr-qc/0509124; 0801.2692; 0709.0732 | **ADJACENT** | Structure formation → effective acceleration via backreaction; not an entropy-functional sign law |
| 12 | Config-entropy / negentropy earlier (Pandey 2017; Pandey & Sarkar) | arXiv:1611.06162 and refs therein | **ADJACENT** | Founds the Shannon-`S_c`-of-LSS program our convergent neighbors sit in |

---

## Reading — the shape of the convergent field

There are **two distinct camps** the object sits between, and it is genuinely between them:

- **Camp A — entropy-of-structure as a DE *diagnostic* (Das & Pandey 2018/2020; Sarkar 2026).**
  Compute an entropy of the evolving density field, watch its *rate*, and read the equation of
  state off features of that rate (the entropy-rate minimum; the negentropy trajectory). This is
  the closest camp by *purpose* and by the fact that it too ties a computed entropy of LSS to
  `w(z)`. Two clean differentiators keep the object out of NEAR-IDENTICAL: (i) **functional** — all
  of Camp A uses the Shannon configuration entropy `S_c = −∫ρ ln ρ d³x` (Gleiser-lineage), a
  quantity of the one-point density PDF; ours is `−ln det C`, a quantity of the *pairwise
  correlation copula*, which is **provably invariant under linear growth** (the amplitude cancels;
  only shape moves `w`) — a structural fence Camp A does not have and does not claim; (ii)
  **direction** — Camp A *constrains* `w₀,wₐ` (fits the entropy to given parametrizations); we
  *derive* `w(a)` with no free parameter via the κ-cancelling stock law. Sarkar's negentropy, once
  resolved, does **not** collapse the gap — it is the copula-orthogonal complement of our functional
  (marginal non-Gaussianity vs correlation structure), which is the cleanest single differentiator
  in the whole sweep and should be stated as such: *the two information-theoretic decompositions of
  the density field are near-orthogonal; Sarkar reads the one-point PDF, we read the multi-point
  copula that is provably blind to it.*

- **Camp B — structure-formation entropy as a DE *source* (Pandey 2026 backreaction; Bianconi's
  entropic gravity).** Here the entropy doesn't diagnose DE, it *is* (part of) it. Pandey 2026 is
  the closest published statement of "`ρ_DE` tracks a structure entropy," which is exactly the
  stock posit `ρ_DE = κ·S`. But Pandey uses the **rate** (`ρ_S ∝ Ṡ_c`) with a **free coefficient α**
  and the Shannon `S_c`, and aims at the H₀/S₈ tensions rather than a `w(z)` sign law. The
  stock-vs-rate axis is exactly the one the repo already litigated internally
  (`rate_form_sign_law.md`; EXP118 STOCK verdict): naming that we take the **stock** branch — which
  is what makes κ cancel — is the clean separation from Pandey. Bianconi is the *premise parent*
  (already NEAR-IDENTICAL in `dark_ledger_convergent_art.md`), but his Λ^G is a Bregman divergence
  of a **metric ratio**, never the correlation matrix of the galaxy/halo field, and he derives no
  `w(z)` from LSS.

The **DISTINCT** rows (holographic + configurational-entropy hybrids, parameterized entropic DE)
share vocabulary ("entropy," "dark energy," "configuration entropy") but are IR-cutoff or
free-parameter DE models with entropy bolted on as a growth check — no computed-from-the-field
`w(z)`, no sign law. They must be cited to show awareness of the "configurational entropy dark
energy" phrase already being taken, but they are not competitors for the object.

The **ADJACENT** rows are the *methodological* ancestors worth one sentence each: Rimes–Hamilton /
Carron is *why* a correlation-information functional is even interesting (non-Gaussian information
that `P(k)` cannot hold), and the Buchert/Räsänen/Wiltshire backreaction program is the standing
"structure formation causes apparent acceleration" tradition the whole reading lives downstream of.

---

## The honest bottom line on the object

Strip everything the literature owns and the residue is a **composite of four elements, none a new
phenomenon**, but whose *combination* has no published instance:

1. **The functional.** `−ln det C` = twice the Gaussian multi-information (Watanabe total
   correlation). The quantity is textbook (cite Watanabe; log-det-entropy estimation
   arXiv:1309.0482); its *deployment as the LSS-→-DE object, in place of Shannon `S_c`*, is not in
   the literature. Its load-bearing property — **blind to amplitude, sees only correlation shape**
   (the linear-growth-invariance theorem) — is the one thing Camp A structurally lacks.
2. **The stock, κ-cancelling sign law.** `1+w = −(1/3) dlnS/dlna`. This is just the continuity
   equation applied to `ρ_DE ∝ S`, so the *algebra* is not novel; the novelty is the specific
   **stock** choice (over Pandey's rate) that makes it **parameter-free**, plus the
   phantom-forbidden theorem for the pointwise-transform class (Mehler/Oppenheim) that turns the
   sign into a falsifiable structural claim rather than a fit.
3. **The pre-registration + logged kills.** A frozen pipeline (`PREREGISTRATION.md`, `a5beb57`) with
   kill conditions that actually *fired* (K7 by 0.007) and *did not* (K3), computed on a genuine
   large-volume box before the number was known. No convergent-art neighbor works this way.
4. **The result.** TNG300-1: `w_today = −0.833 ± 0.057`, crossing `z = 0.59±0.03` (physical) /
   `0.46` (CPL-projected), `(w₀,wₐ) = (−0.767,−0.742)`, **1.36σ from DESI DR2 vs ΛCDM's 3.28σ**.

**Claimable as novel:** yes, as *"a parameter-free equation of state derived from the Gaussian
multi-information of the nonlinear density field, pre-registered and tested against DESI."* Not
claimable: "first to connect an entropy of cosmic structure to `w(z)`" (Das–Pandey 2018), "first to
use an information-theoretic density-field measure to probe dynamical DE" (Sarkar 2026), or "first
to source DE from structure-formation entropy" (Pandey 2026 / Bianconi). The paper's novelty
sentence must be the *functional + stock-parameter-free + pre-registration* triple, explicitly
against those three names.

---

## Who to cite so no wheel is re-invented

- **Any "entropy of cosmic structure tracks `w(z)`" sentence** → **Das & Pandey 2018
  (arXiv:1810.07729)** + **2020 (arXiv:1907.00331)**; state that ours is the log-det/multi-
  information functional and the *derivation* direction, not their Shannon-`S_c` *constraint*
  direction.
- **Any "information-theoretic density-field measure of dynamical DE" sentence** → **Sarkar 2026
  (arXiv:2602.02339)**; state that his negentropy is one-point marginal non-Gaussianity, the
  copula-orthogonal complement of our multi-point `−ln det C`, and that his is a diagnostic/Fisher
  forecast vs our parameter-free derivation.
- **Any "`ρ_DE` sourced by structure-formation entropy" sentence** → **Pandey 2026
  (arXiv:2605.28797)**; state stock-vs-rate and free-α-vs-κ-cancels.
- **The premise "gravity/Λ is an entropy ledger; Λ is a maintenance/relative-entropy term"** →
  **Bianconi 2408.14391 (PRD 111 066001)** + **2510.22545**; already the acknowledged parent.
- **"configurational entropy dark energy" as an existing phrase** → the holographic/Tsallis hybrids
  (**2011.13135**, **2011.07337**, RAA 23) — cite to show the phrase is taken and the object is not
  one of them.
- **Why a correlation-information functional carries what `P(k)` cannot** → **Rimes & Hamilton
  2005/06; Carron 2011; Carron & Neyrinck 2012**.
- **The backreaction tradition** → **Buchert; Räsänen; Wiltshire**.
- **The functional `S` itself** → Watanabe (total correlation) + log-det-entropy (arXiv:1309.0482),
  as in `dark_ledger_convergent_art.md`.

---

## Honest caveats — what these searches might have missed

- **WebSearch is US-only and date-limited.** **2602.02339 has now been resolved** via ar5iv full
  text (Sarkar's negentropy = one-point marginal non-Gaussianity `J`, Eqs. 2.16–2.17; the
  copula-orthogonal complement of our functional — CONVERGENT/complementary, *not* NEAR-IDENTICAL;
  novelty sharpened). **1907.00331 (Das–Pandey 2020) still rests on abstract + search summary** (PDF
  did not parse); the grade (Shannon `S_c`, constraint-not-derivation direction) is well-supported by
  the 2018 companion and the search summaries, but a direct full-text read before submission is still
  advisable to confirm they use no correlation-matrix object.
- **Non-English and very recent (2026) arXiv postings** may be under-indexed; the DESI-DR2 wave is
  producing dynamical-DE model papers weekly, so a fresh `astro-ph.CO` scan near submission is
  warranted (search terms: "configuration entropy dark energy", "negentropy dark energy",
  "multi-information w(z)", "information entropy equation of state").
- **I did not exhaustively check the Räsänen/Buchert quantitative-`w(z)` outputs** against ours;
  they are graded ADJACENT on the mechanism, but if any backreaction paper reports a computed
  `w(a)` from simulations with a comparable sign structure it would deserve a closer grade.
- **Sarkar and Das & Pandey are the same small community** (Visva-Bharati / IUCAA configuration-
  entropy program); a citation-graph walk from arXiv:1907.00331 forward would likely surface 1–2
  more 2024–2026 entries in exactly this lane that the keyword searches did not rank.

---

## Sources

- Das & Pandey, *Constrain DE EoS with configuration entropy*, MNRAS 492, 3928 (2020): [arXiv:1907.00331](https://arxiv.org/abs/1907.00331)
- Das & Pandey, *Configuration entropy in ΛCDM and dynamical DE*, MNRAS 482, 3219 (2018): [arXiv:1810.07729](https://arxiv.org/abs/1810.07729)
- Sarkar, *Negentropy as Diagnostic of Cosmic Density Fields and Dynamical DE Models* (2026): [arXiv:2602.02339](https://arxiv.org/abs/2602.02339)
- Pandey, *Entropic backreaction from cosmic structure formation* (2026): [arXiv:2605.28797](https://arxiv.org/abs/2605.28797)
- Bianconi, *Thermodynamics of the Gravity from Entropy Theory* (2025): [arXiv:2510.22545](https://arxiv.org/abs/2510.22545)
- Bianconi, *Gravity from entropy*, PRD 111, 066001 (2025): [arXiv:2408.14391](https://arxiv.org/abs/2408.14391)
- *Growth Rate and Configurational Entropy in Tsallis Holographic DE* (2021): [arXiv:2011.13135](https://arxiv.org/abs/2011.13135)
- *Holographic DE models with configuration entropy* (2020): [arXiv:2011.07337](https://arxiv.org/abs/2011.07337)
- *Extended Entropic Dark Energy with Four Free Parameters* (2025): [arXiv:2511.15747](https://arxiv.org/abs/2511.15747)
- Rimes & Hamilton, *Information content of the matter P(k)*, MNRAS 360, L82 (2005) & 371, 1205 (2006); Carron, PRL / PRD 84, 043514 (2011); Carron & Neyrinck, ApJ 750, 28 (2012)
- Log-det entropy / total correlation: [arXiv:1309.0482](https://arxiv.org/abs/1309.0482)
- DESI DR2 BAO (2025): [arXiv:2503.14738](https://arxiv.org/abs/2503.14738)
</content>
</invoke>
