#!/usr/bin/env python3
"""
DECISIVE saturation test on a COMPLETE vertebrate brain: larval zebrafish
whole-brain light-sheet (ZAPBench, Immer et al. 2025 -- Ahrens/Engert light-sheet
data). 71,721 segmented neurons x 7,879 volumes = ~all neurons of one entire
brain. Unlike a mouse-cortex 2p subsample, "wrong grain" cannot be invoked:
subsampling runs all the way up to the full N.

Reuses the analysis core (corr eigenvalues, participation ratio, MP edge, phase
randomization, subsample PR curve, block-interleaved cross-validation, synthetic
calibration) from spectral_test.py / spectral_test_allen_cv.py. Because N >> T,
everything is done in T-space via the Gram/dual trick:

  * PR of the neuron-correlation matrix (N x N, rank <= T) is computed from the
    T x T Gram matrix -- identical nonzero spectrum, so PR is exact. Grams are
    accumulated over neuron column-chunks so full N=71721 fits in RAM.
  * cross-validated eigenspectrum (block-interleaved, block >> indicator decay)
    is computed via the DUAL: eig of the Ttr x Ttr train Gram gives u_k; the
    held-out CV eigenvalue is ||Gcross u_k||^2 / (lambda_k Tte), with
    Gcross = Xte_c Xtr_c^T (Tte x Ttr). No N x N matrix is ever formed, so the
    noise-removed k_eff and Stringer alpha are measured at the FULL 71721.

Readouts:
  (a) SATURATION CURVE -- PR vs subsample size N' up to full N (the money plot);
      beta = dlog PR / dlog N' on the upper range. beta->0 = saturation
      (low-rank, CONFIRMATION); 0<beta<1 = power-law growth (FALSIFICATION at a
      complete unit); ~1 = extensive/noise.
  (b) CV power-law alpha (lambda_i ~ i^-alpha) vs Stringer mouse V1 ~1.04.
  (c) noise-free k_eff (PR of the CV-positive, surrogate-subtracted spectrum),
      effective rank vs MP edge and vs a phase-randomized surrogate.

Real ZAPBench data only; synthetics ONLY calibrate the estimators. Incremental
flush of the JSON so a restart leaves recoverable partial work.
"""
import json
import os
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = ("/tmp/claude-1000/-home-emoore-coherence-ratchet/"
           "a15f19f3-8fff-4354-9d5c-e860763082eb/scratchpad")
MEMMAP = os.path.join(SCRATCH, "zap_traces.f32.memmap")
OUT = os.path.join(HERE, "spectral_results_zebrafish.json")
SUMMARY = os.path.join(HERE, "spectral_zebrafish_summary.md")
T_FULL, N_FULL = 7879, 71721
BLOCK = 64          # frames; >> GCaMP6f indicator decay (~2-3 frames), so
                    # train/test halves do not share indicator-noise autocorr
N_SURR = 8
CHUNK = 4000        # neuron columns per accumulation chunk
RNG = np.random.default_rng(0)


# ----------------------------------------------------------------------------
# analysis core (Gram / dual formulation)
# ----------------------------------------------------------------------------
def participation_ratio(ev):
    ev = np.clip(np.asarray(ev, float), 0, None)
    s = ev.sum()
    return float(s * s / np.sum(ev * ev)) if s > 0 else 0.0


def mp_edge(N, T, sigma2=1.0):
    q = N / T
    return sigma2 * (1 + np.sqrt(q)) ** 2


def corr_eigs(Zc):
    """Nonzero eigenvalues (desc) of the neuron correlation matrix, from a
    T x n z-scored block Zc. Uses the smaller of (n x n) / (T x T)."""
    Tt, n = Zc.shape
    M = (Zc.T @ Zc) / Tt if n <= Tt else (Zc @ Zc.T) / Tt
    ev = np.linalg.eigvalsh(M)[::-1]
    return np.clip(ev, 0, None)


def phase_randomize_cols(Zc, rng):
    """Phase-randomize each column's time series (destroy cross-neuron structure,
    preserve each neuron's power spectrum / autocorrelation)."""
    F = np.fft.rfft(Zc, axis=0)
    ph = np.exp(1j * rng.uniform(0, 2 * np.pi, F.shape))
    ph[0] = 1.0
    return np.fft.irfft(F * ph, n=Zc.shape[0], axis=0)


# ----------------------------------------------------------------------------
# (a) saturation curve at full N via chunked Gram accumulation
# ----------------------------------------------------------------------------
def full_corr_eigs(Z, cols, chunk=CHUNK):
    """Nonzero correlation eigenvalues over an arbitrary column set `cols`,
    accumulating the T x T Gram in neuron chunks (memory-bounded)."""
    Tt = Z.shape[0]
    G = np.zeros((Tt, Tt))
    for i in range(0, len(cols), chunk):
        Zc = np.asarray(Z[:, cols[i:i + chunk]], np.float64)
        G += Zc @ Zc.T
    G /= Tt
    ev = np.linalg.eigvalsh(G)[::-1]
    return np.clip(ev, 0, None)


def subsample_pr(Z, sizes, rng, ndraw_fn):
    """Mean PR vs subsample size. Small sizes: n x n corr; large: T x T Gram."""
    Ntot = Z.shape[1]
    Tt = Z.shape[0]
    out = []
    for n in sizes:
        nd = ndraw_fn(n)
        prs = []
        for _ in range(nd):
            idx = rng.choice(Ntot, n, replace=False)
            if n <= Tt:
                ev = corr_eigs(np.asarray(Z[:, idx], np.float64))
            else:
                ev = full_corr_eigs(Z, idx)
            prs.append(participation_ratio(ev))
        out.append((int(n), float(np.mean(prs)), float(np.std(prs)), nd))
        print(f"    N'={n:6d}  PR={np.mean(prs):7.3f} +/- {np.std(prs):.3f}"
              f"  ({nd} draws)", flush=True)
    return out


# ----------------------------------------------------------------------------
# (b,c) block-interleaved cross-validated spectrum via the dual, at full N
# ----------------------------------------------------------------------------
def _accumulate_grams(cols_iter, tr, te):
    """Return (Gtr_raw = Xtr_c Xtr_c^T, Gcross_raw = Xte_c Xtr_c^T) accumulated
    over neuron column-chunks. cols_iter yields T x nc float64 blocks (already
    whatever transform, e.g. surrogate). Columns centered within tr and te."""
    Ttr, Tte = tr.sum(), te.sum()
    Gtr = None
    Gcross = None
    for Zc in cols_iter:
        Xtr = Zc[tr]
        Xte = Zc[te]
        Xtr = Xtr - Xtr.mean(0, keepdims=True)
        Xte = Xte - Xte.mean(0, keepdims=True)
        gtr = Xtr @ Xtr.T
        gcr = Xte @ Xtr.T
        if Gtr is None:
            Gtr, Gcross = gtr, gcr
        else:
            Gtr += gtr
            Gcross += gcr
    return Gtr, Gcross


def cv_spectrum_dual(Gtr, Gcross, Tte):
    """CV eigenvalues (descending order of train eigenvalue) from the dual."""
    lam, U = np.linalg.eigh(Gtr)          # ascending
    lam = lam[::-1]
    U = U[:, ::-1]
    M = Gcross @ U                         # Tte x Ttr
    num = np.einsum("ij,ij->j", M, M)     # ||Gcross u_k||^2
    with np.errstate(divide="ignore", invalid="ignore"):
        cv = num / (lam * Tte)
    cv[~np.isfinite(cv)] = 0.0
    cv[lam <= 1e-9 * lam.max()] = 0.0
    return cv                             # length Ttr, train-eigenvalue order


def _col_blocks(Z, chunk=CHUNK, transform=None, rng=None):
    for i in range(0, Z.shape[1], chunk):
        Zc = np.asarray(Z[:, i:i + chunk], np.float64)
        if transform is not None:
            Zc = transform(Zc, rng)
        yield Zc


def cv_readouts_fullN(Z, rng, n_surr=N_SURR):
    T = Z.shape[0]
    blk = (np.arange(T) // BLOCK) % 2
    tr, te = blk == 0, blk == 1
    Tte = int(te.sum())
    print(f"  block-CV: Ttr={int(tr.sum())} Tte={Tte} (block={BLOCK} frames)",
          flush=True)
    Gtr, Gcross = _accumulate_grams(_col_blocks(Z), tr, te)
    cv = cv_spectrum_dual(Gtr, Gcross, Tte)

    Ss = []
    for s in range(n_surr):
        gt, gc = _accumulate_grams(
            _col_blocks(Z, transform=phase_randomize_cols,
                        rng=np.random.default_rng(100 + s)), tr, te)
        Ss.append(cv_spectrum_dual(gt, gc, Tte))
        print(f"    surrogate {s+1}/{n_surr} done", flush=True)
    Ss = np.vstack(Ss)
    surr_mean = Ss.mean(0)
    surr_p95 = np.percentile(Ss, 95, axis=0)
    surr_top = float(Ss.max())

    keep = cv > surr_p95
    n_cv_pos = int(keep.sum())
    sig = np.clip(cv[keep] - surr_mean[keep], 0, None)
    sig = sig[sig > 0]
    noise_free_keff = participation_ratio(sig) if sig.size else 0.0
    n_above_surr = int((cv > surr_top).sum())

    R = max(n_cv_pos, int((cv > surr_p95).sum()))
    alpha, fit_range = float("nan"), None
    if R >= 12:
        drop = 2
        lam = cv[drop:R]
        idx = np.arange(drop + 1, R + 1)
        m = lam > 0
        if m.sum() >= 8:
            alpha = float(-np.polyfit(np.log10(idx[m]), np.log10(lam[m]), 1)[0])
            fit_range = [int(drop + 1), int(R)]
    return dict(n_cv_pos=n_cv_pos, noise_free_keff=noise_free_keff,
                n_above_surr=n_above_surr, surr_top=surr_top,
                alpha=alpha, alpha_fit_range=fit_range,
                cv_top=[float(x) for x in cv[:16]],
                cv_spectrum_head=[float(x) for x in cv[:400]])


# ----------------------------------------------------------------------------
# synthetic calibration (NOT part of the verdict)
# ----------------------------------------------------------------------------
def _ar_noise(N, T, rng, rho=0.6, passes=3):
    x = rng.standard_normal((T, N))
    for _ in range(passes):
        x[1:] = rho * x[:-1] + x[1:]
    return x


def synth_lowrank(N, T, rng, r=3, snr=2.0):
    F = rng.standard_normal((T, r))
    W = rng.standard_normal((r, N))
    return F @ W + snr ** -1 * _ar_noise(N, T, rng) * np.sqrt(r)


def synth_powerlaw(N, T, rng, alpha=1.0):
    lam = np.arange(1, N + 1.0) ** (-alpha)
    lam = lam / lam.sum() * N
    L = rng.standard_normal((T, N)) * np.sqrt(lam)
    Q, _ = np.linalg.qr(rng.standard_normal((N, N)))
    return L @ Q.T


def zscore_cols(X):
    mu = X.mean(0, keepdims=True)
    sd = X.std(0, keepdims=True)
    sd[sd < 1e-9] = 1.0
    return (X - mu) / sd


def calibrate():
    print("=== CALIBRATION (synthetic; not in the verdict) ===", flush=True)
    N, T = 2000, T_FULL
    rng = np.random.default_rng(1)
    cases = [("low-rank r=3", synth_lowrank(N, T, rng)),
             ("power-law a=1.0", synth_powerlaw(N, T, rng, 1.0)),
             ("power-law a=0.6", synth_powerlaw(N, T, rng, 0.6)),
             ("pure AR noise", _ar_noise(N, T, rng))]
    sizes = [50, 100, 200, 400, 800, 1400, 2000]
    for name, X in cases:
        Z = zscore_cols(X)
        curve = subsample_pr(Z, sizes, np.random.default_rng(2),
                             lambda n: 6 if n < 2000 else 1)
        cn = np.array([c[0] for c in curve], float)
        cp = np.array([c[1] for c in curve])
        up = cn >= 400
        beta = np.polyfit(np.log10(cn[up]), np.log10(cp[up]), 1)[0]
        cvr = cv_readouts_fullN(Z, np.random.default_rng(3), n_surr=4)
        print(f"  [{name:15s}] beta={beta:6.3f}  n_cv_pos={cvr['n_cv_pos']:4d}"
              f"  nf_keff={cvr['noise_free_keff']:6.2f}"
              f"  n>surr={cvr['n_above_surr']:4d}  alpha={cvr['alpha']:.3f}",
              flush=True)
    print("  (expect: low-rank beta~0 & nf_keff~3 & n>surr~3; power-law beta"
          " 0.3-0.8 & alpha~a; noise beta~1 & n>surr~0)\n", flush=True)


# ----------------------------------------------------------------------------
def flush(d):
    with open(OUT, "w") as f:
        json.dump(d, f, indent=1)
        f.flush()
        os.fsync(f.fileno())


def main():
    t0 = time.time()
    calibrate()

    print("=== LOADING ZAPBench whole-brain traces ===", flush=True)
    X = np.memmap(MEMMAP, dtype=np.float32, mode="r", shape=(T_FULL, N_FULL))
    Xr = np.asarray(X, np.float32)              # into RAM (2.26 GB)
    good = np.isfinite(Xr).all(0) & (Xr.std(0) > 1e-9)
    Z = zscore_cols(Xr[:, good].astype(np.float64, copy=False)).astype(np.float32)
    del Xr
    T, N = Z.shape
    print(f"  usable neurons N={N} (dropped {int((~good).sum())}), T={T}",
          flush=True)

    res = dict(
        dataset="ZAPBench whole-brain larval zebrafish light-sheet (Immer et "
                "al. 2025; Ahrens/Engert data). gs://zapbench-release/volumes/"
                "20240930/traces (zarr3, float32).",
        unit="one COMPLETE larval-zebrafish brain (~all neurons)",
        n_animals=1, N_neurons=int(N), T_timepoints=int(T),
        stimulus="9 successive visual conditions (gain,dots,flash,taxis,"
                 "turning,position,...); not purely spontaneous",
        method=dict(pr="correlation-eigenvalue PR via T-space Gram (N>>T; exact "
                       "nonzero spectrum)",
                    cv=f"block-interleaved dual-space CV, block={BLOCK} frames, "
                       f"{N_SURR} phase-randomized surrogates",
                    zscore="neurons z-scored over full recording (scale-invariant)"),
        status="running")
    flush(res)

    # (a) saturation curve up to full N -- the money plot
    print("\n=== (a) SATURATION CURVE (PR vs N') up to full N ===", flush=True)
    sizes = [50, 100, 200, 500, 1000, 2000, 4000, 8000, 16000, 32000,
             50000, N]

    def ndraw(n):
        if n >= 32000:
            return 1
        if n >= 8000:
            return 2
        if n >= 2000:
            return 3
        return 6

    curve = subsample_pr(Z, sizes, np.random.default_rng(10), ndraw)
    cn = np.array([c[0] for c in curve], float)
    cp = np.array([c[1] for c in curve])
    up = cn >= 5000
    beta = float(np.polyfit(np.log10(cn[up]), np.log10(cp[up]), 1)[0])
    # also a top-decade beta (>=16000) -- the steepest test of saturation
    up2 = cn >= 16000
    beta_top = float(np.polyfit(np.log10(cn[up2]), np.log10(cp[up2]), 1)[0])
    pr_full = float(cp[-1])
    res.update(saturation_curve=[dict(Np=c[0], PR=c[1], PR_std=c[2], draws=c[3])
                                 for c in curve],
               beta_upper=beta, beta_upper_range=[5000, int(N)],
               beta_topdecade=beta_top, beta_topdecade_range=[16000, int(N)],
               PR_full_N=pr_full)
    print(f"  beta (N'>=5000) = {beta:.4f}; beta (N'>=16000) = {beta_top:.4f};"
          f" PR at full N = {pr_full:.3f}", flush=True)
    flush(res)

    # (b,c) spectrum diagnostics at full N
    print("\n=== (b,c) full-N correlation spectrum + surrogate ===", flush=True)
    ev = full_corr_eigs(Z, np.arange(N))
    edge = mp_edge(N, T)
    eff_rank_mp = int((ev > edge).sum())
    # phase-randomized surrogate spectrum (chunked), strict floor = its max eig
    Gs = np.zeros((T, T))
    for i in range(0, N, CHUNK):
        Zc = phase_randomize_cols(np.asarray(Z[:, i:i + CHUNK], np.float64),
                                  np.random.default_rng(500 + i))
        Gs += Zc @ Zc.T
    Gs /= T
    ev_surr = np.clip(np.linalg.eigvalsh(Gs)[::-1], 0, None)
    surr_top_eig = float(ev_surr.max())
    eff_rank_surr = int((ev > surr_top_eig).sum())
    pr_corr = participation_ratio(ev)
    res.update(corr_PR_full=pr_corr, mp_edge=float(edge),
               eff_rank_mp=eff_rank_mp, surr_top_eig=surr_top_eig,
               eff_rank_surr=eff_rank_surr,
               top_eigs=[float(x) for x in ev[:16]])
    print(f"  corr PR={pr_corr:.2f}  MP edge={edge:.2f}  eff_rank(MP)="
          f"{eff_rank_mp}  eff_rank(>surrogate)={eff_rank_surr}", flush=True)
    flush(res)

    print("\n=== (b,c) cross-validated spectrum at full N ===", flush=True)
    cvr = cv_readouts_fullN(Z, RNG, n_surr=N_SURR)
    res.update(cv=cvr)
    flush(res)

    verdict, note = decide(beta, beta_top, cvr, eff_rank_surr, pr_full)
    res.update(verdict=verdict, verdict_note=note, status="done",
               runtime_s=round(time.time() - t0, 1))
    flush(res)
    write_summary(res)
    print(f"\nVERDICT: {verdict}\n  {note}", flush=True)
    print(f"\nwrote {OUT} and {SUMMARY}  ({res['runtime_s']}s)", flush=True)


def decide(beta, beta_top, cvr, eff_rank_surr, pr_full):
    nfk = cvr["noise_free_keff"]
    alpha = cvr["alpha"]
    ncv = cvr["n_cv_pos"]
    saturates = beta_top < 0.15 and pr_full <= 12
    stringer = np.isfinite(alpha) and 0.9 <= alpha <= 1.2
    if saturates and nfk <= 12 and not stringer:
        return ("CONFIRMATION (low-rank, saturates)",
                f"PR plateaus (beta_topdecade={beta_top:.3f}~0), PR at full N="
                f"{pr_full:.1f} bounded, noise-free k_eff={nfk:.1f} at/under the "
                f"~10 ceiling, no Stringer power law: complete vertebrate brain "
                f"is low-rank -- corridor saturation HOLDS with no grain "
                f"ambiguity.")
    if (not saturates) or stringer or ncv > 50:
        bits = []
        if not saturates:
            bits.append(f"PR keeps climbing (beta_topdecade={beta_top:.3f}, PR "
                        f"full N={pr_full:.1f})")
        if stringer:
            bits.append(f"CV eigenspectrum is a power law alpha={alpha:.3f} "
                        f"(~Stringer 1.04)")
        if ncv > 50:
            bits.append(f"{ncv} noise-free CV dims (k_eff={nfk:.1f} >> 10)")
        return ("FALSIFICATION (high-dimensional / scale-free)",
                "; ".join(bits) + ". On a COMPLETE brain where 'wrong grain' "
                "cannot be invoked, effective dimensionality does NOT saturate "
                "at the ~10 corridor ceiling -- the corridor claim is falsified "
                "for vertebrate whole-brain.")
    return ("MIXED / INCONCLUSIVE",
            f"beta_topdecade={beta_top:.3f}, PR full N={pr_full:.1f}, noise-free "
            f"k_eff={nfk:.1f}, alpha={alpha:.3f}, {ncv} CV dims, "
            f"{eff_rank_surr} eig above surrogate floor -- readouts disagree.")


def write_summary(r):
    cv = r["cv"]
    L = [
        "# ZAPBench whole-brain zebrafish -- k_eff saturation verdict",
        "",
        "DECISIVE saturation test on a COMPLETE vertebrate brain. ZAPBench "
        "(Immer et al. 2025; Ahrens/Engert light-sheet data): "
        f"**{r['N_neurons']} segmented neurons x {r['T_timepoints']} volumes** "
        "= ~all neurons of one entire larval-zebrafish brain, 1 animal. Because "
        "the whole brain is captured, subsampling runs up to the full N and "
        "'wrong grain' cannot be invoked. Stimulus: "
        f"{r['stimulus']}.",
        "",
        "Analysis core reused from spectral_test.py / spectral_test_allen_cv.py; "
        "N>>T so PR and the cross-validated spectrum are computed in T-space via "
        "the Gram/dual trick (exact nonzero spectrum; no N x N matrix formed).",
        "",
        "## (a) Saturation curve (the money plot)",
        "",
        "| N' | PR (mean) | draws |",
        "|----|-----------|-------|",
    ]
    for c in r["saturation_curve"]:
        L.append(f"| {c['Np']} | {c['PR']:.3f} | {c['draws']} |")
    L += [
        "",
        f"- PR at full N = **{r['PR_full_N']:.2f}**.",
        f"- beta = dlogPR/dlogN' on N'>=5000: **{r['beta_upper']:.4f}**; "
        f"top decade (N'>=16000): **{r['beta_topdecade']:.4f}**.",
        f"  (beta->0 = saturation/low-rank; 0.3-0.8 = power-law growth; "
        f"~1 = extensive.)",
        "",
        "## (b,c) Spectrum diagnostics at full N",
        "",
        f"- correlation-matrix PR (full N) = **{r['corr_PR_full']:.2f}**.",
        f"- Marchenko-Pastur edge lambda+ = {r['mp_edge']:.2f}; effective rank "
        f"above MP edge = **{r['eff_rank_mp']}**; above phase-randomized "
        f"surrogate max eig ({r['surr_top_eig']:.2f}) = **{r['eff_rank_surr']}**.",
        f"- top eigenvalues: {', '.join(f'{x:.1f}' for x in r['top_eigs'][:8])}.",
        "",
        "### Cross-validated (noise-removed) spectrum",
        f"- CV-positive intrinsic dims (> 95th-pct surrogate null): "
        f"**{cv['n_cv_pos']}**.",
        f"- noise-free k_eff (PR of surrogate-subtracted CV-positive spectrum): "
        f"**{cv['noise_free_keff']:.2f}**  (framework ceiling ~10).",
        f"- dims above strict surrogate ceiling: **{cv['n_above_surr']}** "
        f"(lower bound).",
        f"- power-law alpha (lambda_i ~ i^-alpha): **{cv['alpha']:.3f}** "
        f"(Stringer mouse V1 ~1.04).",
        "",
        f"## VERDICT: {r['verdict']}",
        "",
        r["verdict_note"],
    ]
    with open(SUMMARY, "w") as f:
        f.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
