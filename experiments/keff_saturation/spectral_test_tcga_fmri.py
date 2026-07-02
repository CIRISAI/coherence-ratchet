#!/usr/bin/env python3
"""
Mechanism-level criticality-vs-low-rank SPECTRAL discriminator on TWO
pre-registered corridor positives that are NOT single-organism neural:

  (A) TCGA cancer gene-expression  (genes x samples)   -- cellular substrate
  (B) ABIDE-PCP resting-state fMRI (ROI x time)         -- human-neural substrate

Both landed IN the corridor via mean-pairwise rho / k_eff (StructuralClaims.lean).
This adds the spectral read (effective rank + subsampling exponent beta) to
decide whether that corridor occupation is:

  LOW-RANK (novel):    few spikes above a flat Marchenko-Pastur bulk; effective
                       rank small & ~size-independent; PR subsampling beta ~ 0.
  CRITICALITY (trivial): power-law spectrum, no clean spike/bulk separation;
                       beta 0.3-0.8.
  NOISE (chaos):       all eigenvalues ~ MP bulk; beta ~ 1; ~0 spikes.

ANALYSIS CORE reused verbatim from spectral_test.py (C. elegans decisive test):
corr_eig, participation_ratio, mp_edge, phase_randomize, subsample_pr, and the
synthetic calibrators. Two additions, documented at their definitions:
  - permute_surrogate(): the correct destroy-cross-unit-structure surrogate for
    TCGA, whose sample axis is UNORDERED (FFT phase-randomization assumes an
    ordered/time axis and is only used for fMRI here).
  - calibrate(N,T) is parametrized so synthetics are calibrated AT EACH
    SUBSTRATE'S N (beta's baseline drifts with N).

No fabricated data. Synthetics ONLY calibrate the rulers.
"""
import numpy as np, pandas as pd, json, os, glob, gzip

HERE = os.path.dirname(os.path.abspath(__file__))
RNG = np.random.default_rng(0)

TCGA_DIR = "/home/emoore/coherence-ratchet/.claude/worktrees/agent-ae618976841275d76/experiments/noncorr_cancer/data"
ABIDE_DIR = "/home/emoore/nilearn_data/ABIDE_pcp/cpac/filt_noglobal"
PHENO = "/home/emoore/nilearn_data/ABIDE_pcp/Phenotypic_V1_0b_preprocessed1.csv"

# ---------------------------------------------------------------- reused core
def corr_eig(X):
    """z-score UNITS (rows), return correlation-matrix eigenvalues (desc), N, T."""
    N, T = X.shape
    Z = (X - X.mean(1, keepdims=True)) / X.std(1, keepdims=True)
    C = (Z @ Z.T) / T
    ev = np.linalg.eigvalsh(C)[::-1]
    return np.clip(ev, 0, None), N, T

def participation_ratio(ev):
    return (ev.sum() ** 2) / (ev ** 2).sum()

def mp_edge(N, T, sigma2=1.0):
    q = N / T
    return sigma2 * (1 + np.sqrt(q)) ** 2

def phase_randomize(X):
    """Ordered-axis (time) surrogate: preserve each row's power spectrum,
    destroy cross-row correlation. Valid for fMRI timeseries only."""
    F = np.fft.rfft(X, axis=1)
    ph = np.exp(1j * RNG.uniform(0, 2*np.pi, F.shape))
    ph[:, 0] = 1
    return np.fft.irfft(F * ph, n=X.shape[1], axis=1)

def permute_surrogate(X):
    """Unordered-axis surrogate: independently permute each row across columns.
    Destroys cross-row correlation, preserves each row's marginal. Correct for
    TCGA (samples are unordered; FFT phase-randomization would be meaningless)."""
    Y = X.copy()
    for i in range(Y.shape[0]):
        Y[i] = Y[i, RNG.permutation(Y.shape[1])]
    return Y

def subsample_pr(X, sizes, ndraw=40):
    N = X.shape[0]
    out = []
    for n in sizes:
        if n > N: continue
        prs = []
        for _ in range(ndraw):
            idx = RNG.choice(N, n, replace=False)
            ev, *_ = corr_eig(X[idx])
            prs.append(participation_ratio(ev))
        out.append((n, float(np.mean(prs)), float(np.std(prs))))
    return out

def fit_beta(curve, floor):
    cn = np.array([c[0] for c in curve]); cp = np.array([c[1] for c in curve])
    up = cn >= floor
    if up.sum() < 3: return float("nan")
    return float(np.polyfit(np.log10(cn[up]), np.log10(cp[up]), 1)[0])

# ---------------------------------------------------------------- synthetics
def synth_lowrank(N, T, r=3, snr=3.0):
    F = RNG.standard_normal((r, T)); W = RNG.standard_normal((N, r))
    return W @ F + snr**-1 * RNG.standard_normal((N, T)) * np.sqrt(r)

def synth_powerlaw(N, T, alpha=1.0):
    lam = (np.arange(1, N+1) ** (-alpha)); lam = lam / lam.sum() * N
    L = np.sqrt(lam)[:, None] * RNG.standard_normal((N, T))
    Q, _ = np.linalg.qr(RNG.standard_normal((N, N)))
    return Q @ L

def synth_noise(N, T):
    return RNG.standard_normal((N, T))

def calibrate(N, T, sizes, ndraw=20):
    """Calibrate beta ruler AT THIS SUBSTRATE'S N (baseline drifts with N)."""
    floor = max(20, sizes[len(sizes)//2])
    cal = {}
    for name, X in [("lowrank_r3", synth_lowrank(N, T)),
                    ("powerlaw_a1.0", synth_powerlaw(N, T, 1.0)),
                    ("powerlaw_a0.6", synth_powerlaw(N, T, 0.6)),
                    ("noise", synth_noise(N, T))]:
        curve = subsample_pr(X, [s for s in sizes if s <= N], ndraw=ndraw)
        cal[name] = round(fit_beta(curve, floor), 3)
    return cal

def verdict(beta, cal):
    """Classify a measured beta against this-N synthetic rulers."""
    if not np.isfinite(beta): return "inconclusive(no-beta)"
    lo, p1, p06, noi = cal["lowrank_r3"], cal["powerlaw_a1.0"], cal["powerlaw_a0.6"], cal["noise"]
    # midpoints between adjacent rulers
    lo_crit = (lo + min(p1, p06)) / 2
    crit_noise = (max(p1, p06) + noi) / 2
    if beta <= lo_crit:   return "LOW-RANK"
    if beta >= crit_noise: return "NOISE"
    return "CRITICALITY"

# ---------------------------------------------------------------- loaders
def load_tcga(path):
    """genes x samples log2 matrix. Returns (X_genes[N=genes,T=samples], gene_names)."""
    df = pd.read_csv(path, sep="\t", index_col=0)
    df = df.apply(pd.to_numeric, errors="coerce")
    df = df.dropna(how="any")
    # drop constant genes
    X = df.values.astype(float)
    good = X.std(1) > 1e-9
    return X[good], df.index[good].tolist()

def load_abide_controls():
    ph = pd.read_csv(PHENO)
    # DX_GROUP==2 -> typically-developing control
    ctrl = set(ph.loc[ph["DX_GROUP"] == 2, "FILE_ID"].astype(str))
    files = sorted(glob.glob(os.path.join(ABIDE_DIR, "*_rois_cc200.1D")))
    out = []
    for f in files:
        fid = os.path.basename(f).replace("_rois_cc200.1D", "")
        if fid in ctrl:
            out.append((fid, f))
    return out

def load_1d(path):
    """returns ROI x time (N=200 x T)."""
    M = np.loadtxt(path, comments="#")   # T x ROI
    X = M.T
    good = np.isfinite(X).all(1) & (X.std(1) > 1e-9)
    return X[good]

# ---------------------------------------------------------------- per-unit read
def spectral_read(X, surrogate, sizes, ndraw=40):
    ev, N, T = corr_eig(X)
    pr = participation_ratio(ev)
    edge = mp_edge(N, T)
    eff_mp = int((ev > edge).sum())
    Xs = surrogate(X); evs, *_ = corr_eig(Xs)
    eff_surr = int((ev > evs.max()).sum())
    surr_mp = int((evs > edge).sum())
    usizes = [s for s in sizes if s <= N]
    curve = subsample_pr(X, usizes, ndraw=ndraw)
    floor = max(20, N // 3)
    beta = fit_beta(curve, floor)
    return dict(N=int(N), T=int(T), PR=float(pr), mp_edge=float(edge),
                eff_rank_mp=eff_mp, eff_rank_surr=eff_surr, surr_rank_mp=surr_mp,
                beta_sub=beta, top_eigs=[float(x) for x in ev[:6]], subsample=curve)

# ---------------------------------------------------------------- substrate A: TCGA
def run_tcga():
    print("\n" + "="*70 + "\n=== SUBSTRATE A: TCGA gene-expression (genes x samples) ===\n" + "="*70)
    print("UNITS choice: genes (rows). Correlation across SAMPLES -- matches the")
    print("prior corridor read (rho = mean|Pearson| over gene-gene pairs across")
    print("samples). Surrogate = per-gene permutation across samples (unordered).")
    files = sorted(glob.glob(os.path.join(TCGA_DIR, "TCGA_*_HiSeqV2.tsv.gz")))
    GENE_CAP = 1500          # random gene panel (fixed seed) -> tractable eigvalsh
    sizes = [50, 100, 200, 300, 500, 800, 1100, 1500]
    per = []; both_orient = []
    cal_N = None
    for f in files:
        name = os.path.basename(f).split("_")[1]
        Xg_full, genes = load_tcga(f)
        Ngenes, Ns = Xg_full.shape
        # ---- orientation G: genes as units (faithful analog) ----
        idx = RNG.choice(Ngenes, min(GENE_CAP, Ngenes), replace=False)
        Xg = Xg_full[idx]
        if cal_N is None:
            cal_N = Xg.shape[0]
            cal = calibrate(cal_N, 2000, sizes)
            print(f"\n  beta ruler (synthetic, N={cal_N}): {cal}\n")
        rg = spectral_read(Xg, permute_surrogate, sizes, ndraw=20)
        rg["cancer"] = name; rg["orientation"] = "genes_as_units"
        rg["n_genes_total"] = int(Ngenes); rg["n_samples"] = int(Ns)
        rg["gene_cap"] = int(GENE_CAP)
        rg["verdict"] = verdict(rg["beta_sub"], cal)
        per.append(rg)
        # ---- orientation S: samples as units (clean MP, q<1) ----
        Xs = Xg_full.T          # samples x genes  (N=samples, T=genes)
        ev, N, T = corr_eig(Xs)
        s_edge = mp_edge(N, T)
        evp, *_ = corr_eig(permute_surrogate(Xs))
        both_orient.append(dict(cancer=name, orientation="samples_as_units",
            N=int(N), T=int(T), PR=float(participation_ratio(ev)),
            mp_edge=float(s_edge), eff_rank_mp=int((ev > s_edge).sum()),
            eff_rank_surr=int((ev > evp.max()).sum()),
            top_eigs=[float(x) for x in ev[:6]]))
        print(f"  {name:5s} genes-as-units N={rg['N']:4d} T={rg['T']:3d} "
              f"PR={rg['PR']:6.2f} eff_rank(surr)={rg['eff_rank_surr']:3d} "
              f"beta={rg['beta_sub']:.3f} -> {rg['verdict']}")
        print(f"        samples-as-units N={N:3d} T={T:5d} eff_rank(MP)="
              f"{both_orient[-1]['eff_rank_mp']:3d} eff_rank(surr)="
              f"{both_orient[-1]['eff_rank_surr']:3d} PR={both_orient[-1]['PR']:.2f}")
    return per, both_orient, cal

# ---------------------------------------------------------------- substrate B: fMRI
def run_fmri():
    print("\n" + "="*70 + "\n=== SUBSTRATE B: ABIDE-PCP resting-state fMRI (ROI x time) ===\n" + "="*70)
    print("UNITS choice: CC200 ROIs (rows), correlation across TIME -- direct")
    print("analog of C. elegans neurons x time. Surrogate = FFT phase-randomize")
    print("(valid: time is ordered). Controls only (DX_GROUP==2).")
    subs = load_abide_controls()
    sizes = [10, 15, 20, 30, 40, 60, 80, 100, 150, 200]
    cal = calibrate(200, 2000, sizes)
    print(f"\n  beta ruler (synthetic, N=200): {cal}\n")
    per = []
    for fid, f in subs:
        X = load_1d(f)
        if X.shape[0] < 50 or X.shape[1] < 40:
            continue
        r = spectral_read(X, phase_randomize, sizes, ndraw=40)
        r["subject"] = fid; r["orientation"] = "roi_as_units"
        r["verdict"] = verdict(r["beta_sub"], cal)
        per.append(r)
    # aggregate
    betas = np.array([r["beta_sub"] for r in per if np.isfinite(r["beta_sub"])])
    effs = np.array([r["eff_rank_surr"] for r in per])
    print(f"  n_subjects used: {len(per)}")
    print(f"  eff_rank(surr): median {np.median(effs):.1f} range {effs.min()}-{effs.max()}")
    print(f"  beta: mean {betas.mean():.3f} +/- {betas.std():.3f} (n={len(betas)})")
    se = betas.std()/np.sqrt(len(betas))
    ci = [betas.mean()-2*se, betas.mean()+2*se]
    print(f"  beta 95% CI ~ [{ci[0]:.3f}, {ci[1]:.3f}]")
    return per, cal, dict(n=len(per), eff_rank_median=float(np.median(effs)),
        eff_rank_range=[int(effs.min()), int(effs.max())],
        beta_mean=float(betas.mean()), beta_std=float(betas.std()),
        beta_ci=[float(ci[0]), float(ci[1])], n_beta=int(len(betas)))

def main():
    tcga_per, tcga_both, tcga_cal = run_tcga()
    fmri_per, fmri_cal, fmri_agg = run_fmri()

    # ---- TCGA aggregate verdict ----
    tbetas = np.array([r["beta_sub"] for r in tcga_per if np.isfinite(r["beta_sub"])])
    teff_g = np.array([r["eff_rank_surr"] for r in tcga_per])          # genes-as-units
    teff_s = np.array([r["eff_rank_surr"] for r in tcga_both])         # samples-as-units
    tverd = [r["verdict"] for r in tcga_per]
    from collections import Counter
    tcga_verdict = Counter(tverd).most_common(1)[0][0]

    fbetas = np.array([r["beta_sub"] for r in fmri_per if np.isfinite(r["beta_sub"])])
    fverd = [verdict(b, fmri_cal) for b in fbetas]
    fmri_verdict = Counter(fverd).most_common(1)[0][0]

    out = dict(
        tcga=dict(
            orientation_primary="genes_as_units",
            calibration=tcga_cal,
            per_cancer=tcga_per,
            samples_orientation=tcga_both,
            n_cancers=len(tcga_per),
            beta_median=float(np.median(tbetas)),
            beta_range=[float(tbetas.min()), float(tbetas.max())],
            eff_rank_genes_median=float(np.median(teff_g)),
            eff_rank_genes_range=[int(teff_g.min()), int(teff_g.max())],
            eff_rank_samples_median=float(np.median(teff_s)),
            eff_rank_samples_range=[int(teff_s.min()), int(teff_s.max())],
            verdict=tcga_verdict, per_cancer_verdicts=tverd),
        fmri=dict(
            orientation="roi_as_units",
            calibration=fmri_cal,
            per_subject=fmri_per,
            aggregate=fmri_agg,
            verdict=fmri_verdict),
    )
    json.dump(out, open(os.path.join(HERE, "spectral_results_tcga_fmri.json"), "w"), indent=1)

    print("\n" + "="*70 + "\n=== VERDICTS ===\n" + "="*70)
    print(f"TCGA (genes-as-units): beta median {np.median(tbetas):.3f} "
          f"range [{tbetas.min():.3f},{tbetas.max():.3f}]; "
          f"eff_rank(genes) median {np.median(teff_g):.0f}; "
          f"eff_rank(samples) median {np.median(teff_s):.0f}")
    print(f"     ruler: {tcga_cal}")
    print(f"     per-cancer: {dict(Counter(tverd))}  -> {tcga_verdict}")
    print(f"fMRI (roi-as-units): beta {fbetas.mean():.3f} +/- {fbetas.std():.3f}; "
          f"eff_rank(surr) median {fmri_agg['eff_rank_median']:.0f}")
    print(f"     ruler: {fmri_cal}")
    print(f"     per-subject: {dict(Counter(fverd))}  -> {fmri_verdict}")
    print("\nwrote spectral_results_tcga_fmri.json")

if __name__ == "__main__":
    main()
