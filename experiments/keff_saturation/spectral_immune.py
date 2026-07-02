#!/usr/bin/env python3
"""
ADVERSARIAL breadth test on the criticality camp's flagship BIOLOGICAL system:
the adaptive-immune (antibody) repertoire.

Mora, Walczak, Bialek & Callan and collaborators argue immune-repertoire
statistics are CRITICAL: the CLONE-SIZE distribution is Zipf/power-law, and
maximum-entropy models sit near a critical point. We test the SAME system with
our criticality-vs-low-rank discriminator and report BOTH observables, because
they are NOT the same measurement:

  (a) CLONE-SIZE / abundance distribution  -- the criticality camp's observable.
      Is it power-law (Zipf), or lognormal? Fit discrete power-law (Clauset-
      Shalizi-Newman MLE + KS xmin) and Vuong LR test vs lognormal, per repertoire.

  (b) COVARIANCE-SPECTRUM saturation       -- OUR observable.
      Feature = V-J germline-gene-usage fraction; observation = sample (run).
      Build feature x sample matrix, correlate features across the population,
      ask: does effective dimensionality SATURATE under subsampling (low-rank,
      beta~0, few spikes over the Marchenko-Pastur/surrogate floor) or grow as a
      power of N (criticality, 0<beta<1)?

DATA: Observed Antibody Space (OAS), Briney et al. 2019, "Commonality despite
exceptional diversity in the baseline human antibody repertoire" (Nature) --
9 healthy human donors, heavy-chain (IgH) bulk repertoires. 170 of the 296
Heavy_Bulk data units, streamed directly from
  https://opig.stats.ox.ac.uk/webapps/ngsdb/unpaired/Briney_2019/csv/
AIRR columns used: v_call, j_call, cdr3_aa, Redundancy (duplicate-read count =
abundance proxy). Real data only; synthetics calibrate the discriminator only.

Honest unit caveat (stated in the summary): one person's repertoire is a
POPULATION OF CLONES under shared antigenic selection -- a shared driver is
present, but "coordination" is indirect (clones do not signal each other). And
observable (b) here is POPULATION-level gene-usage covariance across samples, not
one repertoire's own clonal dynamics; the latter (longitudinal clone tracking) is
the faithful single-unit test and is low-T. Both limits are reported plainly.
"""
import numpy as np, pandas as pd, gzip, glob, os, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spectral_test import (corr_eig, participation_ratio, mp_edge,
                           phase_randomize, subsample_pr,
                           synth_lowrank, synth_powerlaw, synth_noise)

HERE = os.path.dirname(os.path.abspath(__file__))
BULKDIR = "/tmp/claude-1000/-home-emoore-coherence-ratchet/a15f19f3-8fff-4354-9d5c-e860763082eb/scratchpad/briney_bulk"
RNG = np.random.default_rng(0)


# ---------------------------------------------------------------- parsing
def gene(call):
    """IGHV3-23*01 (or 'IGHV3-23*01,IGHV3-23*04') -> IGHV3-23."""
    if not isinstance(call, str) or not call:
        return None
    return call.split(",")[0].split("*")[0].strip()


def parse_unit(path):
    """Return (subject, vj_counts dict, clone_sizes np.array, redundancy np.array)."""
    with gzip.open(path, "rt") as fh:
        meta = fh.readline()
    try:
        import json as _j
        m = _j.loads(meta.strip().strip('"').replace('""', '"'))
        subject = m.get("Subject", os.path.basename(path))
    except Exception:
        subject = os.path.basename(path)
    df = pd.read_csv(path, skiprows=1,
                     usecols=["v_call", "j_call", "cdr3_aa", "Redundancy"],
                     dtype=str, on_bad_lines="skip", engine="c")
    df = df.dropna(subset=["v_call", "j_call"])
    vg = df["v_call"].map(gene)
    jg = df["j_call"].map(gene)
    red = pd.to_numeric(df["Redundancy"], errors="coerce").fillna(1.0).clip(lower=1.0)
    ok = vg.notna() & jg.notna()
    vg, jg, red = vg[ok], jg[ok], red[ok]
    cdr = df["cdr3_aa"].where(df["cdr3_aa"].notna(), "").astype(str)[ok]
    # (a) V-J usage counts (unique-sequence-weighted composition vector)
    vj = (vg + "|" + jg)
    vj_counts = vj.value_counts().to_dict()
    # (b) clonotype sizes: group identical (V,J,CDR3aa), size = summed reads
    key = vg.values + "\t" + jg.values + "\t" + cdr.values
    tmp = pd.DataFrame({"key": key, "r": red.values})
    clone_sizes = tmp.groupby("key")["r"].sum().values.astype(float)
    return subject, vj_counts, clone_sizes, red.values.astype(float)


# ------------------------------------------------- power-law (clone-size)
def _discrete_pl_alpha(x, xmin):
    x = x[x >= xmin]
    n = len(x)
    if n < 20:
        return np.nan, n
    # continuous MLE (good for xmin>=~5); Clauset eq. 3.1
    alpha = 1.0 + n / np.sum(np.log(x / (xmin - 0.5)))
    return alpha, n


def _pl_cdf_ks(x, xmin, alpha):
    x = np.sort(x[x >= xmin])
    n = len(x)
    if n < 20:
        return np.inf
    emp = np.arange(1, n + 1) / n
    # continuous power-law CDF
    theo = 1.0 - (x / xmin) ** (1.0 - alpha)
    return np.max(np.abs(emp - theo))


def fit_powerlaw(x):
    """CSN-style: pick xmin minimizing KS, MLE alpha. Return dict."""
    x = np.asarray(x, float)
    x = x[x >= 1]
    if len(x) < 50:
        return dict(alpha=np.nan, xmin=np.nan, ks=np.nan, n_tail=0, ntot=len(x))
    cand = np.unique(np.floor(np.quantile(x[x >= 1], np.linspace(0, 0.9, 25)))).astype(int)
    cand = cand[cand >= 1]
    best = None
    for xm in cand:
        a, n = _discrete_pl_alpha(x, xm)
        if not np.isfinite(a) or a <= 1:
            continue
        ks = _pl_cdf_ks(x, xm, a)
        if best is None or ks < best[2]:
            best = (a, xm, ks, n)
    if best is None:
        return dict(alpha=np.nan, xmin=np.nan, ks=np.nan, n_tail=0, ntot=len(x))
    a, xm, ks, n = best
    return dict(alpha=float(a), xmin=int(xm), ks=float(ks), n_tail=int(n), ntot=int(len(x)))


def vuong_pl_vs_lognormal(x, xmin):
    """Vuong LR test: >0 favors power-law, <0 favors lognormal. Returns (R, p)."""
    from scipy import stats
    x = np.asarray(x, float)
    x = x[x >= xmin]
    n = len(x)
    if n < 30:
        return np.nan, np.nan
    a, _ = _discrete_pl_alpha(x, xmin)
    if not np.isfinite(a):
        return np.nan, np.nan
    # per-point log-likelihood, power-law (continuous, x>=xmin)
    ll_pl = np.log((a - 1) / xmin) - a * np.log(x / xmin)
    # lognormal MLE on x>=xmin (truncated approx via full-fit; standard CSN comparison)
    lx = np.log(x)
    mu, sig = lx.mean(), lx.std(ddof=0)
    if sig <= 0:
        return np.nan, np.nan
    ll_ln = -np.log(x * sig * np.sqrt(2 * np.pi)) - (lx - mu) ** 2 / (2 * sig ** 2)
    d = ll_pl - ll_ln
    R = d.sum()
    sd = d.std(ddof=0)
    if sd <= 0:
        return np.nan, np.nan
    z = R / (np.sqrt(n) * sd)
    p = 2 * stats.norm.sf(abs(z))
    return float(z), float(p)   # z>0 favors power-law


def pl_spectrum_alpha(ev, kmax=None):
    """power-law exponent of the ranked eigenvalue spectrum lambda_k ~ k^-alpha."""
    ev = np.sort(ev)[::-1]
    ev = ev[ev > 1e-9]
    k = np.arange(1, len(ev) + 1)
    hi = min(kmax or len(ev), len(ev))
    lo = 1
    m = (k >= lo) & (k <= hi)
    if m.sum() < 4:
        return np.nan
    return -np.polyfit(np.log10(k[m]), np.log10(ev[m]), 1)[0]


# ------------------------------------------------------------ calibration
def calibrate():
    print("=== CALIBRATION (synthetic; discriminator only) ===")
    N, T = 200, 800
    for name, X in [("low-rank r=3", synth_lowrank(N, T)),
                    ("power-law a=1.0", synth_powerlaw(N, T, 1.0)),
                    ("power-law a=0.6", synth_powerlaw(N, T, 0.6)),
                    ("pure noise", synth_noise(N, T))]:
        ev, n, t = corr_eig(X)
        pr = participation_ratio(ev)
        Xs = phase_randomize(X); evs, *_ = corr_eig(Xs)
        eff = int((ev > evs.max()).sum())
        sizes = [10, 20, 40, 60, 100, 140, 200]
        curve = subsample_pr(X, sizes, ndraw=20)
        cn = np.array([c[0] for c in curve]); cp = np.array([c[1] for c in curve])
        up = cn >= 40
        beta = np.polyfit(np.log10(cn[up]), np.log10(cp[up]), 1)[0]
        print(f"  {name:16s}: PR={pr:6.2f}  eff_rank={eff:3d}  beta_sub={beta:6.3f}")
    print("  (low-rank beta~0 few spikes; power-law beta 0.3-0.8; noise beta~1)\n")


# ------------------------------------------------------------------- main
def main():
    calibrate()
    files = sorted(glob.glob(os.path.join(BULKDIR, "*.csv.gz")))
    print(f"parsing {len(files)} OAS/Briney_2019 Heavy_Bulk units ...")
    samples = []           # per-sample dict
    all_clone = []         # per-sample clone-size fit rows
    vj_vocab = {}
    for i, f in enumerate(files):
        try:
            subj, vjc, clones, red = parse_unit(f)
        except Exception as e:
            print(f"  skip {os.path.basename(f)}: {e}"); continue
        tot = sum(vjc.values())
        if tot < 500:
            continue
        samples.append(dict(file=os.path.basename(f), subject=subj, ntot=tot, vj=vjc))
        for k in vjc:
            vj_vocab[k] = vj_vocab.get(k, 0) + 1
        # clone-size fit (criticality observable) on the clonotype-aggregated sizes
        pf = fit_powerlaw(clones)
        if np.isfinite(pf["alpha"]):
            z, p = vuong_pl_vs_lognormal(clones, pf["xmin"])
        else:
            z, p = np.nan, np.nan
        all_clone.append(dict(file=os.path.basename(f), subject=subj,
                              nclones=int(len(clones)), max_size=float(clones.max()),
                              **pf, vuong_z=z, vuong_p=p))
        if (i + 1) % 25 == 0:
            print(f"  {i+1}/{len(files)} parsed")
            sys.stdout.flush()

    print(f"\nusable samples: {len(samples)}")
    subs = sorted({s['subject'] for s in samples})
    print(f"distinct donors: {len(subs)}  -> {subs}")

    # ---- feature x sample matrix: V-J usage fraction, features seen in >=60% of samples
    S = len(samples)
    feats = sorted([k for k, c in vj_vocab.items() if c >= 0.6 * S])
    fidx = {k: i for i, k in enumerate(feats)}
    M = np.zeros((len(feats), S))
    for j, s in enumerate(samples):
        tot = s['ntot']
        for k, c in s['vj'].items():
            if k in fidx:
                M[fidx[k], j] = c / tot
    print(f"feature x sample matrix: N={M.shape[0]} V-J features, T={M.shape[1]} samples")

    # ---- OUR discriminator on the covariance spectrum
    ev, N, T = corr_eig(M)
    pr = participation_ratio(ev)
    edge = mp_edge(N, T)
    eff_rank_mp = int((ev > edge).sum())
    # time-series surrogate (weakly motivated here: samples are UNORDERED individuals)
    Xs = phase_randomize(M); evs, *_ = corr_eig(Xs)
    surr_top = float(evs.max())
    eff_rank_surr = int((ev > surr_top).sum())
    surr_rank_mp = int((evs > edge).sum())
    # PROPER cross-sectional null: permute each feature independently across samples
    # (destroys cross-feature correlation, preserves each feature's marginal). Count
    # data eigenvalues clearing the 99th percentile of the permuted top eigenvalue.
    perm_tops = []
    for _ in range(200):
        Mp = np.array([row[RNG.permutation(T)] for row in M])
        ep, *_ = corr_eig(Mp)
        perm_tops.append(ep.max())
    perm_thresh = float(np.quantile(perm_tops, 0.99))
    eff_rank_perm = int((ev > perm_thresh).sum())
    sizes = [s for s in [10, 15, 20, 30, 40, 60, 80, 100, 120, 150, N] if s <= N]
    sizes = sorted(set(sizes))
    curve = subsample_pr(M, sizes, ndraw=40)
    cn = np.array([c[0] for c in curve]); cp = np.array([c[1] for c in curve])
    upper = cn >= max(20, cn.max() // 3)
    beta = float(np.polyfit(np.log10(cn[upper]), np.log10(cp[upper]), 1)[0]) if upper.sum() >= 3 else np.nan
    alpha_spec = pl_spectrum_alpha(ev, kmax=min(N, 40))

    print("\n=== OBSERVABLE (b): COVARIANCE SATURATION (our discriminator) ===")
    print(f"  PR / k_eff              = {pr:.2f}   (ceiling N={N})")
    print(f"  eff_rank (MP edge {edge:.2f}) = {eff_rank_mp}")
    print(f"  eff_rank (perm null 99pct {perm_thresh:.2f}) = {eff_rank_perm}   [proper cross-sectional null]")
    print(f"  eff_rank (time-surrogate) = {eff_rank_surr}   (weak null: samples unordered)")
    print(f"  subsample beta          = {beta:.3f}")
    print(f"  spectrum power-law alpha= {alpha_spec:.3f}")
    print(f"  subsample curve (N', PR):")
    for n_, p_, sd_ in curve:
        print(f"     N'={n_:4d}  PR={p_:6.2f} +/- {sd_:.2f}")

    # ---- clone-size (criticality observable) summary
    ca = pd.DataFrame(all_clone)
    good = ca[np.isfinite(ca["alpha"])]
    alpha_med = float(good["alpha"].median())
    alpha_iqr = [float(good["alpha"].quantile(.25)), float(good["alpha"].quantile(.75))]
    # power-law favored over lognormal where vuong_z>0; significantly where p<0.1 & z>0
    vz = good["vuong_z"].values; vp = good["vuong_p"].values
    frac_pl_favored = float(np.mean(vz > 0))
    frac_pl_sig = float(np.mean((vz > 0) & (vp < 0.1)))
    frac_ln_sig = float(np.mean((vz < 0) & (vp < 0.1)))

    print("\n=== OBSERVABLE (a): CLONE-SIZE DISTRIBUTION (criticality camp's observable) ===")
    print(f"  per-repertoire power-law exponent alpha: median {alpha_med:.2f}  IQR {alpha_iqr}")
    print(f"  Vuong power-law vs lognormal (z>0 favors power-law):")
    print(f"     frac repertoires favoring power-law (z>0):      {frac_pl_favored:.2f}")
    print(f"     frac significantly power-law (z>0, p<0.1):      {frac_pl_sig:.2f}")
    print(f"     frac significantly lognormal (z<0, p<0.1):      {frac_ln_sig:.2f}")

    # ---- verdicts
    sat = (beta < 0.15) and (eff_rank_perm <= 4)
    cov_verdict = ("LOW-RANK / SATURATING" if sat else
                   ("POWER-LAW / CRITICALITY-like" if beta > 0.3 else "INTERMEDIATE"))
    clone_verdict = ("heavy-tailed, power-law NOT ruled out (Zipf-consistent)"
                     if frac_ln_sig < 0.5 else "lognormal-favored (not clean power-law)")

    out = dict(
        dataset="OAS / Briney_2019 (9 healthy human donors, IgH bulk repertoires)",
        source_url="https://opig.stats.ox.ac.uk/webapps/ngsdb/unpaired/Briney_2019/csv/",
        n_units=len(files), n_samples=S, n_donors=len(subs), donors=subs,
        covariance=dict(N=int(N), T=int(T), PR_keff=pr, mp_edge=float(edge),
                        eff_rank_mp=eff_rank_mp, eff_rank_perm=eff_rank_perm,
                        perm_thresh=perm_thresh, eff_rank_surr=eff_rank_surr,
                        surr_rank_mp=surr_rank_mp, beta_sub=beta,
                        spectrum_alpha=alpha_spec,
                        top_eigs=[float(x) for x in ev[:8]],
                        subsample=[(int(a), float(b), float(c)) for a, b, c in curve],
                        verdict=cov_verdict),
        clone_size=dict(alpha_median=alpha_med, alpha_iqr=alpha_iqr,
                        frac_pl_favored=frac_pl_favored, frac_pl_sig=frac_pl_sig,
                        frac_ln_sig=frac_ln_sig, verdict=clone_verdict,
                        per_sample=all_clone),
    )
    json.dump(out, open(os.path.join(HERE, "spectral_results_immune.json"), "w"), indent=1)
    print("\n=== VERDICTS ===")
    print(f"  covariance (our observable): {cov_verdict}  (beta={beta:.3f}, eff_rank_perm={eff_rank_perm}, k_eff={pr:.1f}/{N})")
    print(f"  clone-size (their observable): {clone_verdict}  (median alpha={alpha_med:.2f})")
    print("\nwrote spectral_results_immune.json")


if __name__ == "__main__":
    main()
