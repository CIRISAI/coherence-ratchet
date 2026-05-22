# Debate synthesis — how to update the paper

Adjudication of `strong_reading.md` against `conservative_reading.md`.

> **Correction (2026-05-21, after reading `Corridor Dynamics.tex` directly).**
> An earlier version of this synthesis was built on a compaction summary's
> account of the paper and got three things wrong: it treated the structural
> series as a re-run that downgraded v1's five-substrate record (it did not —
> see v2 framing); it recommended retitling off "Five-Substrate Validation"
> (the record stands); and it under-credited the paper, which already carries
> the orthogonality theorem at full strength (§open-research) and the
> structural series + Claim 2 amendment (§f-handles). The v2-framing section
> and items 0–2 below are corrected. The conservative ledger's "2 positives"
> is legitimate as the scope of *what the session paid for*, but it undercounts
> the *paper's* evidence base, which is v1's five substrates plus the session's
> additions.

## The debate converged

The two sides were briefed as opponents. They are not. Set their concrete
recommendations side by side and they call for the **same edits**:

| change | strong side | conservative side |
|---|---|---|
| §corridor-empirical revised | "new pre-registered structural-series subsection" | "replace the prior-data matrix; add LLM-weak + Allen rows; downgrade 5/5 PASS" |
| a cross-rung empirical section | "new cross-rung empirical section (the paper has none)" | "rewrite cross-rung to the amended n=2 Claim 6" |
| GPU corridor-exit rate added | "first measurement of dρ/dt" | "with its single-substrate scope on its face" |
| particle-physics nulls go in | "honest scope-drawing" | "retract from speculative-extension to tested null" |
| orthogonality theorem foregrounded | "stated at full strength" | (not denied; the theorem stands in its account) |

The "strong" and "conservative" readings are one paper update seen from two
ends: **state the real results at full strength, and draw every scope line.**
Those are different sentences — a result given cleanly and its scope line given
cleanly do not compete for the same space. The paper's own declared style is
declarative-and-falsification-pinned; doing both is that style.

## The one genuine adjudication call

The strong side wants "the framework is a strict extension of ΛCDM" as a
headline. The conservative side calls the orthogonality theorem "a fence, not a
reach" — its content is that the framework *cannot* move bulk CMB power.

**Verdict: headline it — and the fence is the content.** The orthogonality
theorem is the session's one proved cosmological result and it genuinely
answers the cosmology reviewer. State it as a headline. But the headline is
"strict extension — adds nothing false to bulk physics," not "rival cosmology
that reaches further." What it earns is precisely the fence: the framework is
safe against every bulk-CMB and Standard-Model measurement *because it provably
changes none of them*, and its distinctive content is confined to the shape
sector — which is itself calibration-gated and, in the timescale form, measured
at no substrate. The strong side gets the headline; the conservative side's
gloss is the headline's meaning.

## v2 framing — this is a Zenodo version, not a draft edit

v1 is public: *Corridor Dynamics in Coordinated Systems* — Zenodo v1 DOI
`10.5281/zenodo.20300774`, published 2026-05-20, concept DOI
`10.5281/zenodo.20300773` (resolves to latest). v1 stays citable; v2 gets a new
version DOI on upload. Zenodo carries no version-comment field, so the
change-note lives *inside the v2 PDF* — a dated "Changes in v2" section.

**v1's five-substrate record stands.** §sec:corridor-empirical validates the
corridor at five substrates (C. elegans, Drosophila, four LLM architectures,
four OSS projects, five cancers) with a paired in-corridor / out-corridor
matrix — Figure 2, Mode (iii) = 0/5. The 2026-05-21 structural series did not
re-run those five and downgrade them. It is a second wave: it added human fMRI
and Allen mouse cortex (new substrates), extended the cancer substrate from 5
to 12 cancers (201/201 reproducing the prior 176/176), and re-measured LLM
internals on smaller models with a debiased within-layer observable. The
substrate base is broader after the session, not narrower. The title's
"Five-Substrate Empirical Validation" is intact — now an undercount if v2 adds
substrates, not an overclaim.

**The proper v2 §corridor-empirical is a uniform-footing upgrade.** v1's five
were measured 2026-05-15..19, before the structural series, against the nominal
GPU-anchored (0.10, 0.43) band the paper itself flags as not transferring. v2
should re-run the original five under the structural series' more robust
framing (debiased ρ, substrate-local corridor calibration, canonical
observable) so the flagship matrix is not a mix of pre- and
post-structural-series methods — then add the new substrates. Caveat: two of
the five — OSS (single-author-dominance proxy) and social groups (qualitative
AM checklist) — are not ρ-correlation substrates; "robust framing" for them
means pre-registration and proxy-stated-as-proxy, not the debiased-ρ upgrade,
and needs its own definition before a re-run.

## Recommended paper update — section by section

0. **"Changes in v2" section — no retitle.** The title's "Five-Substrate
   Empirical Validation" stands; the record is intact and the session only
   broadened it. Add a dated change-note section listing the genuine v1→v2
   deltas, each against its experiment: structural spine five→six claims;
   §corridor-empirical re-run on robust footing and extended; cross-rung
   empirical tier added; GPU corridor-exit rate added; particle-physics shape
   sector moved from "open research direction" to "tested null."

1. **Orthogonality theorem — already in v1; consider lifting.** v1
   §sec:open-research already states the theorem at full strength ("strict
   extension of ΛCDM," the proved Lean lemmas named) and §f-handles records it.
   The only optional v2 change is lifting the headline to the abstract. No new
   content owed here — the summary's "the paper is behind on this" was wrong.

2. **§corridor-empirical — the five re-run (5/5 PASS), now extend.** The
   robust re-run is done — `experiments/structural_series/robust_rerun/`,
   all five substrates re-measured under debiased ρ + canonical k_eff +
   substrate-local calibration, every one PASS, no whole-wave falsifier fired.
   v2 states the five-substrate matrix on that uniform footing and folds in
   four named precision amendments: (a) Figure 1 carries per-substrate bands —
   the 0.25–0.75 neural band was C. elegans-driven, Drosophila CX is ~0.09–0.46;
   (b) a C. elegans footnote that band centres sit lower once the substantial
   (~0.18) surrogate floor is debiased out; (c) the OSS rubric stated precisely
   — γM(t) is active maintenance of any provenance; (d) the social persistence
   spread restated median-to-median (2.7 orders, not "four"). Then add the new
   rows: human fMRI confirmed, Allen mouse cortex (chaos-pole datum, owed k_eff
   re-test), cancer extended 5→12. State Claim 4 as recurrence-of-tightness,
   and the band centre as substrate-local and pipeline-dependent (TCGA
   0.27→0.34 on a GDC pipeline change). The five-substrate paired matrix
   (Figure 2, Mode (iii) = 0/5) is re-run and holds — not downgraded.

3. **New cross-rung empirical section** (the paper has none). Path 1 + w3 — the
   coupling ratio O(1) across 26 measurements, **n = 2 distinct rung pairs**
   stated on its face. Claim 6 amended (g/J ≳ 3 retracted → O(1)). The Simon
   head-to-head, Simon 1962 as the named opponent. The canonical timescale g/J
   measured at no substrate — in the same paragraph, not a footnote.

4. **§P_ω / open-research.** Flag that the cross-rung corridor is written in the
   timescale observable (τ_(n,n+1)) while the session measured a coupling
   ratio — an unmeasured-observable gap. Soften "This IS Penrose's WCH,
   structurally derived" — the paper elsewhere correctly calls the Penrose
   argument structural-not-derived; that one sentence overclaims.

5. **§engineering / dynamics.** Add the GPU corridor-exit rate — the first
   measured value of dρ/dt — with its single-substrate, n = 1 scope on its
   face.

6. **§lake + §f-handles.** Record `CMBOrthogonality.lean` as a Tier-A
   derivation (one claim moves Tier D → Tier A). Update the structural-spine to
   six claims. Note the live amendment record — Claim 2 by E2, Claim 6 by
   Path 1 — as the falsification apparatus working.

7. **§not-claim + §open-work.** The four particle-physics nulls as honest
   scope-drawing: the framework's particle tier is composition with the
   Standard Model, not prediction. New not-claim / open-work items: the cross-
   rung n = 2, the dynamics n = 1, the owed Allen k_eff re-test, the
   timescale-g/J gap.

## Net

The session bought a **narrower, better-defended** paper than the draft
occupies — and a genuinely stronger one at its core (a proved theorem, two
clean pre-registered substrate confirmations, a live falsification apparatus).
The update is not a retreat and not a reach: it states six real results at full
strength and draws the scope line on every one. Both debate sides recommend it.
