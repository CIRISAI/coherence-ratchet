# PFL3 LAL spectral discriminator — BLOCKED (insufficient dimensionality)

**Substrate:** Drosophila PFL3 (FB→LAL steering neurons), two-photon LAL imaging.
**Genotype:** 57C10-AD-VT037220-DBD. **Recordings:** 18 (_im.h5), 10 flies. **T:** 14100 frames (~1540 s @ ~9.2 Hz).

**What the .h5 files contain:** each `_im.h5` is a pandas HDF (`df/block0_values`, shape 14100×5) with columns
`[t, ps_c1_roi_1_F, ps_c1_roi_2_F, ps_c2_roi_1_F, ps_c2_roi_2_F]` =
time + **Left/Right LAL GCaMP** (2 activity ROIs) + **Left/Right LAL tdTomato** (2 anatomical-reference ROIs).

**Why blocked:** only **N=2 activity units** per recording (bilateral bulk-LAL fluorescence). The spectral test
(Marchenko-Pastur edge, participation ratio, PR subsampling exponent β over N′∈{10…150}) requires a segmented
population; every readout is undefined at N=2. No per-glomerulus segmentation and no raw movie are stored, so a
higher-N matrix cannot be recovered, and hand-segmentation is out of scope.

**Verdict:** INCONCLUSIVE — spectral discriminator not runnable on this dataset. No synthetic units were substituted.

**Note for the EPG/low-rank corroboration question:** PFL3 *cannot* independently corroborate or refute the
EPG low-rank read from these files — the stored representation is already reduced to a 2-D (left−right) steering
readout, which is consistent with (but not an independent test of) the low-dimensional expectation.
