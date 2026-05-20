"""
Soft-vs-hard P_omega discriminator: the SHAPE of the cross-rung coupling
distribution in real Drosophila EPG<->FC3 simultaneous recordings.
========================================================================

Context. The soft-vs-hard P_omega debate (team p-omega-debate) concluded the
choice is presently FORMAL, not empirically decided. data-arbiter proposed an
empirical discriminator: in a real two-rung system the cross-rung coupling
distribution should show a SHARP EDGE if the underlying corridor constraint is
a hard projector, or a GRADED (exponential) TAIL if it is soft.

Data. Ishida et al 2025 (Cell), simultaneous dual-color two-photon imaging of
EPG (compass rung, jRGECO1a, EB) and FC3 (FB columnar rung, GCaMP7f) in the
SAME fly. 7 recordings / 4 flies, folder 6 of Zenodo 17555687. Real data,
fetched by the v19_biology autonomous-loop agent.

What v19 already did. v19 measured mean cross-rung |Pearson| (rho_EF ~ 0.18)
and tested its goal-directed-vs-spontaneous state-dependence (FAIL: no shift).
v19 did NOT characterise the DISTRIBUTION SHAPE of the coupling. That is what
this script computes -- the genuinely unrun piece.

The discriminator, framework-faithfully. The framework says within-rung rho
lives in a corridor (rho_lower, rho_upper). A HARD P_omega makes rho_upper a
wall: windowed rho never exceeds it, the upper tail terminates in a cliff. A
SOFT P_omega makes rho_upper a soft threshold: windowed rho can exceed it but
is exponentially suppressed -- a graded tail, no cliff. So: build the
distribution of windowed rho (within-EPG, within-FC3, cross-EF) and ask
whether its upper tail is hard-edged or graded.

HONEST CAVEAT (also printed in output). This is a WEAK proxy. The inferential
chain from "fly EPG-FC3 coupling tail shape" to "the cosmological P_omega is
soft or hard" is long and depends on substrate-generality -- and v19 already
found the framework's cross-rung prediction FAILS at this substrate. This
script characterises the coupling distribution honestly; it does not settle
the soft-vs-hard question. Real data only; no fabrication.
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

DATA = Path("/home/emoore/coherence-ratchet/.claude/worktrees/"
            "agent-a4753b36bf926c6d6/experiments/v19_biology/data/ishida_folder6")
EPG_SUFFIX = "eb_c2"
FC3_SUFFIX = "fb2_c1"
F0_FRAC = 0.05
WIN_SEC = 30.0
HOP_SEC = 15.0


def F_to_dFF(F, f0_frac=F0_FRAC):
    valid = F[~np.isnan(F)]
    if len(valid) < 10:
        return F * np.nan
    s = np.sort(valid)
    n = max(1, int(len(s) * f0_frac))
    F0 = s[:n].mean()
    if F0 <= 1e-9:
        F0 = 1e-9
    return (F - F0) / F0


def mean_abs_corr(X, cross=None):
    """Mean |Pearson| over within-block upper triangle, or over the full
    cross-block if `cross` is given."""
    Xz = (X - X.mean(0, keepdims=True)) / (X.std(0, keepdims=True) + 1e-12)
    if cross is None:
        C = (Xz.T @ Xz) / X.shape[0]
        iu = np.triu_indices(C.shape[0], k=1)
        return float(np.nanmean(np.abs(C[iu])))
    Yz = (cross - cross.mean(0, keepdims=True)) / (cross.std(0, keepdims=True) + 1e-12)
    C = (Xz.T @ Yz) / X.shape[0]
    return float(np.nanmean(np.abs(C)))


def load_recording(im_path):
    im = pd.read_csv(im_path)
    cols = list(im.columns)
    epg = sorted(c for c in cols if c.endswith(EPG_SUFFIX))
    fc3 = sorted(c for c in cols if c.endswith(FC3_SUFFIX))
    if len(epg) < 8 or len(fc3) < 8:
        return None
    Fe, Ff = im[epg].values, im[fc3].values
    dFe = np.column_stack([F_to_dFF(Fe[:, j]) for j in range(Fe.shape[1])])
    dFf = np.column_stack([F_to_dFF(Ff[:, j]) for j in range(Ff.shape[1])])
    keep = ~(np.any(np.isnan(dFe), 1) | np.any(np.isnan(dFf), 1))
    return dFe[keep], dFf[keep]


def windowed(dFe, dFf, dt):
    w = max(20, int(round(WIN_SEC / dt)))
    hop = max(10, int(round(HOP_SEC / dt)))
    out = {"EE": [], "FF": [], "EF": []}
    for s in range(0, len(dFe) - w + 1, hop):
        e, f = dFe[s:s + w], dFf[s:s + w]
        out["EE"].append(mean_abs_corr(e))
        out["FF"].append(mean_abs_corr(f))
        out["EF"].append(mean_abs_corr(e, cross=f))
    return {k: np.array(v) for k, v in out.items()}


def tail_shape(x):
    """Characterise the upper tail of distribution x.
    Returns metrics that separate a graded (exponential) tail from a hard edge.
      - exp_R2  : R^2 of a linear fit to log-survival over the upper tail.
                  ~1 => exponential/graded tail (soft-consistent).
      - gauss_R2: R^2 of log-survival vs (x - mu)^2 (Gaussian tail comparison).
      - cliff   : (max - p99) / (p99 - p50). Small => tail terminates abruptly
                  just past p99 (hard-edge-like); large => tail extends (graded).
    """
    x = np.sort(x[~np.isnan(x)])
    n = len(x)
    p = {q: float(np.percentile(x, q)) for q in (50, 90, 95, 99)}
    xmax = float(x[-1])
    cliff = (xmax - p[99]) / max(p[99] - p[50], 1e-9)
    # upper-tail survival fit, over points above the median
    tail = x[x > p[50]]
    surv = 1.0 - (np.arange(len(tail)) + 0.5) / len(tail)
    ok = surv > 1e-3
    tt, ss = tail[ok], surv[ok]
    logS = np.log(ss)

    def r2(xv, yv):
        b = np.polyfit(xv, yv, 1)
        pred = np.polyval(b, xv)
        ssr = np.sum((yv - pred) ** 2)
        sst = np.sum((yv - yv.mean()) ** 2)
        return float(1 - ssr / sst) if sst > 0 else float("nan"), b

    exp_R2, exp_b = r2(tt, logS)                       # exponential tail
    gauss_R2, _ = r2((tt - x.mean()) ** 2, logS)       # Gaussian tail
    return {"n": n, "p50": p[50], "p90": p[90], "p95": p[95], "p99": p[99],
            "max": xmax, "cliff_ratio": cliff,
            "exp_tail_R2": exp_R2, "gauss_tail_R2": gauss_R2,
            "exp_decay_per_unit_rho": float(-exp_b[0])}


def main():
    rec_dirs = sorted(p.parent for p in DATA.glob("*/*/*_im.csv"))
    print(f"recordings found: {len(rec_dirs)}")
    if not rec_dirs:
        print("NO DATA at expected path -- aborting (no fabrication).")
        sys.exit(1)

    win = {"EE": [], "FF": [], "EF": []}
    pair = {"EE": [], "FF": [], "EF": []}
    for d in rec_dirs:
        im_path = next(d.glob("*_im.csv"))
        beh = pd.read_csv(next(d.glob("*_beh.csv")))
        dt = float(beh["imt"].diff().median())
        loaded = load_recording(im_path)
        if loaded is None:
            print(f"  SKIP {d.name}: too few ROIs")
            continue
        dFe, dFf = loaded
        w = windowed(dFe, dFf, dt)
        for k in win:
            win[k].append(w[k])
        # static pairwise correlations over the whole recording
        Ez = (dFe - dFe.mean(0)) / (dFe.std(0) + 1e-12)
        Fz = (dFf - dFf.mean(0)) / (dFf.std(0) + 1e-12)
        Cee = (Ez.T @ Ez) / len(Ez)
        Cff = (Fz.T @ Fz) / len(Fz)
        Cef = (Ez.T @ Fz) / len(Ez)
        pair["EE"].append(np.abs(Cee[np.triu_indices(Cee.shape[0], 1)]))
        pair["FF"].append(np.abs(Cff[np.triu_indices(Cff.shape[0], 1)]))
        pair["EF"].append(np.abs(Cef).ravel())
        print(f"  {d.name}: dt={dt:.3f}s, {len(dFe)} samples, "
              f"{len(w['EF'])} windows")

    win = {k: np.concatenate(v) for k, v in win.items()}
    pair = {k: np.concatenate(v) for k, v in pair.items()}

    print()
    print("=" * 76)
    print("WINDOWED rho DISTRIBUTION  (30 s windows, 50% overlap, pooled)")
    print("=" * 76)
    labels = {"EE": "within-rung EPG", "FF": "within-rung FC3",
              "EF": "cross-rung EPG<->FC3"}
    shapes = {}
    for k in ("EE", "FF", "EF"):
        t = tail_shape(win[k])
        shapes[k] = t
        frac_above_043 = float(np.mean(win[k] > 0.43))
        print(f"\n  {labels[k]}  (n={t['n']} windows)")
        print(f"    median {t['p50']:.3f} | p90 {t['p90']:.3f} | "
              f"p95 {t['p95']:.3f} | p99 {t['p99']:.3f} | max {t['max']:.3f}")
        print(f"    fraction of windows with rho > 0.43 (GPU-substrate "
              f"corridor upper bound): {frac_above_043:.3f}")
        print(f"    upper-tail shape:")
        print(f"      exponential-tail fit R^2 = {t['exp_tail_R2']:.4f}  "
              f"(near 1 => graded/exponential tail => soft-consistent)")
        print(f"      Gaussian-tail   fit R^2 = {t['gauss_tail_R2']:.4f}")
        print(f"      cliff ratio (max-p99)/(p99-p50) = {t['cliff_ratio']:.3f}  "
              f"(small => abrupt edge; large => extended graded tail)")

    print()
    print("=" * 76)
    print("STATIC PAIRWISE |corr| DISTRIBUTION  (per-ROI-pair, whole recording)")
    print("=" * 76)
    for k in ("EE", "FF", "EF"):
        t = tail_shape(pair[k])
        print(f"  {labels[k]:24s} n={t['n']:5d}  median {t['p50']:.3f}  "
              f"p99 {t['p99']:.3f}  max {t['max']:.3f}  "
              f"exp_R2 {t['exp_tail_R2']:.3f}  cliff {t['cliff_ratio']:.3f}")

    print()
    print("=" * 76)
    print("READING")
    print("=" * 76)
    ef = shapes["EF"]
    soft_like = ef["exp_tail_R2"] > 0.95 and ef["cliff_ratio"] > 0.4
    hard_like = ef["cliff_ratio"] < 0.15
    print(f"  cross-rung EPG<->FC3 windowed rho: exponential-tail R^2 = "
          f"{ef['exp_tail_R2']:.3f}, cliff ratio = {ef['cliff_ratio']:.3f}.")
    if soft_like and not hard_like:
        print("  Descriptive reading: the cross-rung coupling tail is GRADED")
        print("  (extended, well fit by an exponential) -- soft-consistent.")
    elif hard_like and not soft_like:
        print("  Descriptive reading: the cross-rung coupling tail TERMINATES")
        print("  abruptly -- hard-edge-consistent.")
    else:
        print("  Descriptive reading: the tail shape is INTERMEDIATE / not")
        print("  cleanly hard or soft on these metrics.")
    print()
    print("  CAVEAT: this is a weak proxy for the soft-vs-hard P_omega")
    print("  question. The chain from a fly EPG-FC3 coupling tail to the")
    print("  cosmological P_omega is long; v19 already found the framework's")
    print("  cross-rung prediction FAILS at this substrate. This result")
    print("  characterises the coupling distribution; it does not settle the")
    print("  formal soft-vs-hard choice.")


if __name__ == "__main__":
    main()
