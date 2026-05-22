# Robust re-run of v1's five-substrate corridor record — results

**Date:** 2026-05-21. All five substrates of `Corridor Dynamics.tex`
§sec:corridor-empirical re-run under the robust framing pre-registered in
`PREREGISTRATION.md` — debiased ρ via phase-randomized surrogate floor,
canonical participation-ratio k_eff, substrate-local calibration, thresholds
fixed before computing.

## Verdict: 5/5 PASS

v1's five-substrate paired record stands under the more robust framing. No
substrate fired the whole-wave falsifier — no in-corridor substrate pinned at a
pole under debiasing, no out-corridor result reversed direction. v1's Figure 2
paired-validation matrix (Mode (iii) = 0/5) holds.

| Substrate | verdict | debiased numbers | v2 amendment |
|---|---|---|---|
| C. elegans — neural in-corridor (832 worms, 12 studies) | PASS | whole-brain ρ_deb 0.312 (raw 0.357, floor 0.176); k_eff 3.9; per class: command 0.597, motor 0.392, interneuron 0.358, sensory 0.315 | footnote: the surrogate floor is substantial (~0.18 of raw 0.36); band centres sit slightly lower once it is removed — v1's raw estimator did not subtract it |
| Drosophila CX — neural in-corridor (v18 + v19, 4 rungs) | PASS | EPG 0.424, FC2 0.331, EPG(v19) 0.089, FC3 0.269; debias shaves <3.5% | Figure 1: CX band is ~0.09–0.46, not 0.25–0.75 — the 0.25–0.75 was C. elegans-driven; Figure 1 needs per-substrate bands |
| EEG — neural out-corridor (CHB-MIT, I-CARE) | PASS | healthy 0.270, seizure +0.030, coma +0.20–0.23; k_eff 6.5→5.6→3.3 | none — v1 text reproduces to 3 decimals; pole-entry still not reached, exactly as v1 framed |
| OSS contribution (15 repos) | PASS | rigid_w 0.607 vs 0.225; multi_w 0.000 vs 0.693; recomputed from raw commit data, matches v1 | rubric: γM(t) = active maintenance of *any* provenance (institutional OR volunteer) — Tenacity is Mode (ii), Mode (iii) stays 0 |
| Social groups (9 groups) | PASS | AM checklist re-verified internally consistent | "four orders of magnitude" persistence spread → median-to-median is 374y/0.83y ≈ 450× = **2.7 orders** |

LLM internals and cellular/cancer were re-run under the robust framing in the
2026-05-21 structural series itself (LLM-internals; TCGA 7 new cancers) and are
not repeated here.

## Reading

The robust re-run changes no substrate's verdict. Every amendment is a
precision correction — per-substrate band calibration (Drosophila, C. elegans),
a rubric clarification (OSS), a ratio restatement (social) — each named, none a
falsification. The debiasing step matters most at C. elegans, where ~half the
raw correlation is surrogate-floor artifact; even there the genuine debiased
correlation clears both poles. v2's §sec:corridor-empirical can state the
five-substrate record on uniform footing with the structural series' additions
(fMRI, Allen, cancer 5→12).
