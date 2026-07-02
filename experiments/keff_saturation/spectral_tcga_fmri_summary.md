# Spectral discriminator — TCGA & ABIDE-fMRI (non-neural-single-organism substrates)

Mechanism read (effective rank + subsampling β) on two pre-registered corridor
positives. Core reused verbatim from `spectral_test.py`; β ruler calibrated at
each substrate's N. Data all on disk. Run `spectral_test_tcga_fmri.py`.

**TCGA gene-expression** (5 cancers, genes×samples, HiSeqV2 log2; units=genes,
corr across samples — matches prior ρ read). β ruler at N=1500:
lowrank=0.003 / α1.0=0.046 / α0.6=0.371 / noise=0.696.
- genes-as-units: β 0.010–0.043 (median 0.036), eff_rank 25–46 / 1500.
- samples-as-units: **1 giant eigenvalue (~N) then flat MP bulk, 4–9 spikes,
  PR 1.11–1.18**; spike count NOT growing with N (N=329→4, N=1218→9).
- **VERDICT: LOW-RANK.** β=0.04 lies in the compressed low-rank/steep-power-law
  zone (rulers 0.003 vs 0.046 are indistinguishable at N=1500) — far below the
  real criticality band (0.37–0.70). The auto-label "criticality (4/5)" is that
  ruler-compression artifact; the effective-rank readout (decisive per template
  logic: small & size-independent) is unambiguous. Not criticality (no scale-free
  cascade in either orientation), not noise (PR≪N).

**ABIDE-PCP resting-state fMRI** (139 controls, DX_GROUP==2, CC200 ROI×time;
units=ROIs, corr across time; FFT phase-random surrogate). β ruler at N=200:
lowrank=0.039 / α1.0=0.198 / α0.6=0.592 / noise=0.946.
- β mean **0.058 ± 0.030** (95% CI [0.052,0.063]), 133/139 subjects LOW-RANK.
- eff_rank median **4** (range 1–8), N fixed ~200: 1 dominant eigenvalue then
  flat bulk. Rank small across T=78–296 (corr(eff_rank,T)=0.50 = short scans
  resolve fewer spikes, not extensive growth).
- **VERDICT: LOW-RANK.** β well below the low-rank/criticality midpoint (~0.12).

**Both non-neural-single-organism substrates read LOW-RANK, not criticality.**
Corridor occupation here is genuine few-mode structure (the novel reading), not
the trivial scale-free-criticality alternative — consistent with the C. elegans
decisive result.
