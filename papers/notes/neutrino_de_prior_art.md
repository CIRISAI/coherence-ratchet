# Neutrino ↔ dark energy: the prior-art map, and two ledger-native kills

**Date 2026-07-10.** Theory/literature pass, run before any neutrino-sector claim is married.
Companion to the flavor result (`experiments/sm_escalator_mixing/SUMMARY.md`: the ledger reads
lepton mixing as Haar-anarchic — the neutrino mass book is written off the Higgs mechanism)
and to the dm-mass kill, whose kill (c) already logged `ρ_Λ^{1/4} ≈ 2.24 meV ≈ m_ν` as PRIOR
ART with zero new ledger content (`experiments/dark_sector_mass/SUMMARY.md`). This note (1)
maps that prior art in both directions with verified citations, (2) does the ledger-native
arithmetic and stakes the kills, (3) positions honestly what — if anything — our version adds.

**Bottom line up front:** the neutrino↔DE link is one of the most heavily backwards-theorized
coincidences in cosmology (20+ years, both directions, no confirmed mechanism). The ledger-native
"per-neutrino ln2 posting" identity is **DEAD** (needs m_ν ≈ 14 eV, ~200× the bound). The
surviving fourth-root match is **circular by construction** — it is the observed ρ_Λ re-expressed
in eV, containing no neutrino physics. Our framework **structurally cannot** supply the missing
mechanism (the dimensional + provenance lines forbid it from writing a mass). What we add beyond
prior art is thin, and I say so.

---

## 1. Verified-citation status (the program has been burned by confabulation — read this first)

| Source | ID | Verification |
|---|---|---|
| Fardon, Nelson, Weiner, *Dark Energy from Mass Varying Neutrinos* (MaVaNs), JCAP 0410:005 (2004) | astro-ph/0309800 | **verified** (title+authors, search) |
| Afshordi, Zaldarriaga, Kohri, *Instability of Dark Energy with Mass-Varying Neutrinos*, PRD 72:065024 (2005) | astro-ph/0506663 | **verified** (title+authors, search) |
| Dvali, Funcke, *Small neutrino masses from gravitational θ-term* (2016) | 1602.03191 | **verified by direct fetch** (authors + meV-transition claim) |
| de Vega, Sanchez, *Dark Energy is the Cosmological Quantum Vacuum Energy of Light Particles — The Axion and the Lightest Neutrino* (2007) | astro-ph/0701212 | **verified by direct fetch** (authors + relation) |
| Amendola, Baldi, Wetterich, *growing neutrino quintessence* (2008); Wetterich (2007) | — | authors/year **verified via search summary**; individual arXiv IDs NOT pinned — do not cite an ID |
| Phenomenological relation `μ_vac ~ m_ν ~ Λ_ew²/M`, M ~ 3×10¹⁶ GeV | — | appears in review literature; **primary source not pinned** — flag, do not lean |
| "Neutrino Condensate as Origin of Dark Energy" (ResearchGate hit, ~2010) | — | **authorship UNVERIFIED** — excluded from claims below |

---

## 2. The ledger-native arithmetic (Task 2 — the sharp new content)

Working numbers (h=0.674, Ω_Λ=0.69): ρ_Λ = **3303 eV/cm³** = 2.54×10⁻¹¹ eV⁴, and
ρ_Λ^{1/4} = **2.244 meV** (reproduces the textbook figure exactly). Script: inline, `Bash`.

### (i) The "ln2 per CνB mode" identity is DEAD

If the balance posts ln2 (the fermionic per-mode rigidity ceiling, `fermionic_ledger`) per
cosmic-neutrino-background mode, then ρ_Λ = ln2 · n_CνB · m_ν. Solving for the required mass with
n_CνB = 336 cm⁻³ (3 flavors × ν+ν̄):

  **m_ν(required) = 3303 / (0.693 × 336) = 14.2 eV** (42.5 eV if one uses 112 cm⁻³ per species).

The cosmological bound is Σm_ν ≲ 0.06–0.12 eV, i.e. ~0.02–0.05 eV per species. The identity
**misses by a factor of ~140–700 (2–2.7 orders of magnitude).**

> **KILL (per-neutrino posting).** The reading "the balance posts ln2 per CνB mode" is dead:
> it requires a neutrino mass two-plus orders above the DR-class cosmological bound. This is
> **distinct from and sharper than** the dm-mass note's route where the mass cancels: here the
> mass does *not* cancel, it is over-determined and wrong. Recorded as a dated debt discharged.
> The dimensional fourth-root (§2ii) is untouched by this — it survives only as dimensional
> analysis, not as a posting identity.

Why it fails, structurally: ln2/mode is a *rigidity* (a dimensionless entropy ceiling); pairing
it with a number density and a mass to make an energy density is a dimensional coincidence that
the ledger's own scale-freedom (dimensional line §1) gives no reason to hold. It doesn't.

### (ii) Is there ANY ledger-native bridge to the meV scale? — No, and the fourth-root is circular

Swept the framework's actual dimensionless objects — ln2/mode, corridor ρ∈(0.1,0.43), k_eff≤10,
dlnS/dlna — for any combination that emits meV without inserting it. Per the provenance line
(`dimensional_line_kB.md` §3), a dimensionful output requires the **one married scale** (retention
unit ~10^11.8 M⊙/h → κ from matching ρ_Λ today). So every route to a dimensionful meV runs
through κ, and:

  ρ_Λ = κ·S  →  ρ_Λ^{1/4} = (κ·S)^{1/4} = **2.244 meV**.

But κ today is fixed *by matching the observed ρ_Λ*. So ρ_Λ^{1/4} is **the observed dark-energy
density, fourth-rooted into eV** — a unit conversion on an input, carrying **zero** neutrino
physics and zero ledger content. The "prediction" that it lands near m_ν is the same number
(nature's ρ_Λ) fed back; it is **circular**.

> **CIRCULARITY VERDICT (fourth-root chain).** As currently anchored (κ ← ρ_Λ match), the
> neutrino "prediction" ρ_Λ^{1/4}≈m_ν is circular: it is the observed DE scale in different units.
> **The only way it becomes non-circular** is if retention-v2 derives κ from independent baryonic
> physics (the retention-scale → κ chain). *Then* ρ_Λ = κ·S is a genuine prediction of the DE
> density, and its fourth root landing at the neutrino scale is a real cross-scale coincidence —
> **but still only a coincidence**, because nothing in the chain references m_ν. There is no
> independent cross-check that closes the loop through the neutrino sector; the retention chain is
> the *only* route to the number, and it terminates at ρ_Λ, not at m_ν.

### (iii) What a non-fluke would require, and whether prior art can supply it *compatibly*

A non-fluke needs a **mechanism** linking the balance's currency (stress-energy / entanglement
coordination) to neutrino mass *generation*. The framework's own commitments forbid it from
containing one:
- **Dimensional line** (§1): S is a copula functional, amplitude-blind by theorem — it cannot
  emit a mass.
- **Provenance line** (§3, clause 2): marginals — masses, mass ratios — are upstream input the
  ledger reads *downstream of*. A mass-generation mechanism is exactly an upstream-datum
  construction the ledger is proved blind to.

So for us the fourth-root match can **never** be more than dimensional analysis. Full stop. The
question is then whether any *verified prior-art* mechanism supplies the bridge in a way
**compatible with our perturbation-sector commitment** (CLAUDE.md: exactly ΛCDM in the
conditioning/perturbation sector — `CMBOrthogonality.lean` — no new dynamics there; DE is a
one-directional functional of the matter coordination history, sign law 1+w = −⅓ dlnS/dlna).

- **MaVaNs / acceleron (FNW 2004):** ρ_DE tracks neutrino density via a light scalar coupled to
  ν. **Incompatible.** It lives *in* the perturbation sector we declare untouched, and it was
  killed there: Afshordi–Zaldarriaga–Kohri (2005) showed a generic adiabatic (hydrodynamic)
  instability — as ν go non-relativistic they condense into "neutrino nuggets" that redshift like
  CDM, so the model either ceases to act as DE or is fine-tuned into indistinguishability from Λ.
  Also its w(z) is set by dln m_ν/dln a (a fifth-force dynamic), **not** by our −⅓ dlnS/dlna sign
  law — the two make different w(z) for different reasons.
- **Growing-neutrino quintessence (Wetterich 2007; Amendola–Baldi–Wetterich 2008):** cosmon–ν
  coupling stops the cosmon when ν go non-relativistic (a "why now" fix), producing nonlinear
  neutrino lumps at supercluster scales, z≈1. **Incompatible** for the same reason — it is a
  distinctive, heavily-constrained perturbation-sector signature; our framework forbids exactly
  that.
- **Dvali–Funcke gravitational-θ-term condensate (2016):** the *closest* compatible-direction
  mechanism — a late-Universe (T~meV) phase transition generates small neutrino masses from a
  gravitational anomaly (η′-analog neutrino bound state), and predicts the *cosmological ν-mass
  bound relaxes* (ν massless until the transition). It runs DE-scale → m_ν, our conjecture's
  direction, and does not obviously require a perturbation-sector fifth force. **But it is a
  specific BSM Lagrangian mechanism that is NOT our framework** — it *writes* the mass from a new
  gravitational term; our ledger is proved unable to write masses. It supplies *an* alternative
  bridge, not *our* bridge. (It also predicts dynamical late-time m_ν, which does leave a
  free-streaming imprint — a phenomenological tension with strict ΛCDM-in-perturbations.)
- **de Vega–Sanchez (2007):** vacuum energy of light particles; notably the lightest neutrino
  gives a *negative* DE contribution there. Numerology-adjacent; no coupling in our sector.

**Compatibility verdict:** every prior-art mechanism that would make the coincidence physical is
either (a) killed/constrained in the perturbation sector our orthogonality theorem forbids us to
touch (MaVaNs, growing-ν), or (b) a distinct BSM mass-generation Lagrangian our framework
structurally cannot host (Dvali–Funcke). None supplies a bridge that is *both* live *and* ours.

---

## 3. Prior-art map, both directions (Task 1)

**(a) DE-scale → m_ν (our conjecture's direction).** Genuinely populated. Dvali–Funcke (2016,
verified) is the flagship: the meV DE/vacuum scale *is* the scale of a late phase transition that
sets m_ν; predicts the cosmological mass bound weakens and Dirac-vs-Majorana decay signatures.
de Vega–Sanchez (2007, verified) tie the DE scale to light-particle (axion~meV, lightest-ν)
vacuum energy. The review-level relation μ_vac ~ m_ν ~ Λ_ew²/M with M~3×10¹⁶ GeV (source not
pinned — flagged) frames the meV DE scale as the seesaw combination. Status: live but unconfirmed;
no DR-class datum has picked one out.

**(b) neutrino sector → DE (the backwards direction).** The classic program. MaVaNs
(Fardon–Nelson–Weiner 2004, verified) — DE from density-dependent m_ν via the acceleron, with a
model-independent w(m_ν) relation and m_ν allowed to exceed the constant-mass cosmological bound.
Damaged by Afshordi–Zaldarriaga–Kohri (2005, verified): generic adiabatic instability → neutrino
nuggets → indistinguishable from Λ unless contrived. Growing-neutrino quintessence
(Wetterich/Amendola–Baldi 2007–08, verified via summary) is the surviving descendant, at the cost
of a distinctive (and now tightly constrained) neutrino-lump signature. Most of these make
ρ_DE ~ m_ν⁴ *explicit*.

**(c) pure-coincidence / numerology.** Widely stated: ρ_DE^{1/4} ~ 2×10⁻³ eV ~ m_ν (normal
hierarchy), and ρ_DE ~ (Δm²)² ~ m_ν⁴. Universally treated as *suggestive but unexplained* — a
coincidence in search of a mechanism, exactly the status kill (c) of the dm-mass sweep assigned it.

**How heavily backwards-theorized:** very. Both directions have been worked for two decades; the
ρ_DE~m_ν⁴ relation is a standard talking point; the forward (DE→m_ν) direction has at least one
serious mechanism (Dvali–Funcke). This is a crowded, well-trodden coincidence, not open ground.

---

## 4. What our version adds beyond prior art — honestly thin

Candidate additions, weighed:

1. **Independent structural selection (the one real, non-numerological contribution).** The ledger
   reads lepton mixing as Haar-anarchic and quark mixing as comonotone — a *parameter-free*
   statement that the neutrino mass book is written by a **different mechanism, off the Higgs**
   (`sm_escalator_mixing`). This is independent of the DE-scale coincidence and does not depend on
   it. It is a *reading*, not a mechanism (provenance line), and it concerns mixing/structure, not
   the *mass scale* — so it does **not** touch the ρ_Λ^{1/4}~m_ν coincidence at all. Its value is
   orthogonal: it says "the second book exists and is anarchic," consistent with the neutrino
   sector being where any DE-scale coincidence would have to live, but it explains none of the meV
   arithmetic.
2. **The derived-κ chain, IF retention-v2 validates.** Would upgrade ρ_Λ^{1/4} from circular to a
   genuine (baryonic-physics-derived) DE-scale prediction — but per §2ii, still a coincidence with
   m_ν, not a link to it. Conditional, and even when granted, adds nothing on the *neutrino* side.
3. **Registered kills.** The two kills above (per-neutrino posting DEAD; fourth-root circular) are
   genuine additions to the coincidence literature's usual hand-waving — but they are *subtractive*
   (they close doors), which is the honest thing to add here.

**On the mass-scale coincidence specifically, our addition is thin — and I say thin.** We cannot
derive m_ν, we cannot host a mechanism that does, and our best "prediction" is a unit conversion on
the observed ρ_Λ. The one substantive, non-thin contribution (the anarchic-book selection) is about
flavor *structure*, not the meV *scale*, and stands on its own registered kill (DUNE/Hyper-K δ)
regardless of anything in this note.

---

## 5. Fluke probability (honest)

For **our framework's purposes**, the probability that ρ_Λ^{1/4}≈m_ν carries real ledger content
(is not a fluke) is **low — I put it ~10–15%**. Reasoning: (i) we have *proved* (dimensional line)
we cannot emit a mass, so for us the match can only ever be dimensional analysis on an input; (ii)
the ln2·n·m posting identity — the one way it could have been ledger-native — is dead by ~200×;
(iii) the coincidence is order-of-magnitude at best (2.24 meV vs solar 8.6 meV vs atmospheric 50
meV — factors of 4–20 depending on which ν scale), between two of the smallest numbers in physics,
and 20 years of mechanism-hunting has produced candidates (MaVaNs, growing-ν, Dvali–Funcke) but no
confirmation. The broader *physical* question — is nature's meV DE scale mechanistically the ν-mass
scale? — remains genuinely open (~30–40% one might call it live, given Dvali–Funcke), but that is a
puzzle **others** may resolve with machinery we forbid ourselves. On our books it stays logged as
prior-art numerology, not support (rule 2), and the per-neutrino-posting door is now closed.

## 6. Kills staked (dated debts, 2026-07-10)

- **K-ν1 (fired):** per-CνB-mode ln2 posting → requires m_ν≈14 eV → DEAD. Discharged.
- **K-ν2 (standing):** the fourth-root match is support only if a mechanism *links* κ/ρ_Λ to
  m_ν-generation. No such mechanism is compatible with our perturbation-sector commitment (§2iii);
  until one is, ρ_Λ^{1/4}≈m_ν stays logged as prior-art coincidence, never cited as support.
- **K-ν3 (standing, inherited):** the anarchic-book selection dies if DUNE/Hyper-K push δ toward
  CP-conserving or θ₁₃ off the Haar bulk (`sm_escalator_mixing` kills) — this is the *only* live
  neutrino-sector claim, and it is about mixing structure, not the meV coincidence.

---

## 7. Sideways pass (orchestrator) — the kills stand; the "thin" verdict over-flattened three conjunctions this note documents but never combines

The two kills are correct and stay fired/standing. What the note's own sections contain, read
*together* rather than serially:

**(a) The composite route is non-circular, and this note assembled both halves without joining
them.** §2ii: if retention-v2 validates, ρ_Λ becomes a *derived* number (baryonic feedback →
unit scale → κ → ρ_Λ) — "genuine prediction of the DE density." §3a: Dvali–Funcke is a verified,
live mechanism running DE-scale → m_ν — a machine that *eats* a meV vacuum scale and *emits*
neutrino masses, whose own free input is "why is the transition scale meV?" Composite:
**our (conditionally) derived scale + their mechanism = a closed chain from galaxy-formation
physics to m_ν**, with each program supplying exactly what the other is missing — they have a
mechanism with an underived scale; we have a (conditionally) derived scale and a proof we can
never have a mechanism. This is NOT our marriage (we cannot host their Lagrangian; rule 2
untouched; K-ν2 unrescinded) — it is a **named-partner consilience at recognition weight**, the
same tier as the anomaly-cancellation echo, and it is not thin.

**(b) "Orthogonal" (§4.1) understates a conjunction.** SM fermion masses span ~14 orders
(meV → 10¹¹ eV). The one fermion whose book the flavor read independently flags as off-Higgs is
also the one sitting within ~an order of the balance scale. Under a null where the anomalous
book could sit anywhere, that is a ~10% joint coincidence — weak, one order of surprise, exactly
"suggestive" tier. Two independent instruments pointing at the same sector is evidence *of the
conjunction*, even when neither explains the other. Logged as suggestive, never as support.

**(c) The composite has a LIVE observational hook this note names and drops.** §3a records that
Dvali–Funcke predicts the cosmological ν-mass bound *relaxes* (neutrinos effectively massless at
early times). The note never connects this to the present data: the current **Σm_ν squeeze** —
cosmological bounds pressing at/below the minimal-NO oscillation floor — is a mild live anomaly
sitting exactly where late-mass-generation predicts relief. And our thawing background
*independently* relaxes the same bound. Three-way convergence at DR3: our w(z) retrodiction, the
squeeze's resolution, and the composite's viability are probed by the same release.

**Disposition unchanged in kind, corrected in weight:** nothing married; K-ν1 fired, K-ν2/K-ν3
standing; the mass-scale claim stays out of the stance. But the file's summary line "what we add
is thin" is amended to: *what we can claim alone is thin; what the conjunction + composite +
squeeze jointly constitute is a registered, kill-carrying, recognition-weight bridge with a
named partner mechanism and a dated test (DR3).* Fluke-probability restated: for-us-alone
~3–5% (proved-circular unless retention validates); composite-route live-ness, conditional on
retention surviving its audit, ~15–20%.

**Condition resolved same night: retention FAILED its audit** (C1/C2 fired — the extremum is
cap-set, not SHM-set; `retention_v2/CHALLENGES.md`). κ stays anchored to the observed ρ_Λ, so
the fourth-root chain stays circular (K-ν2 unrelieved) and the composite route's conditional
band collapses back to the unconditional ~3–5%. What survives of §7 unconditionally: the
conjunction (b) at its ~10% weight, and the Σm_ν-squeeze hook (c), which depends only on the
thawing background, not on retention.

*(Arithmetic and citation verification by the neutrino-de prior-art agent; two citations confirmed
by direct arXiv fetch, remainder flagged per §1. Sideways pass §7 by the orchestrator.)*
