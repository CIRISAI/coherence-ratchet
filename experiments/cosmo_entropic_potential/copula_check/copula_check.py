#!/usr/bin/env python3
"""
Copula-invariance verification pass  (papers/notes/copula_invariance_remark.md, sec. 3).

The remark's sharpening: multi-information is a functional of the COPULA. It is
exactly invariant under invertible pointwise maps, and strictly decreased by
non-invertible ones (DPI). The Gaussian-committed S = -ln det C_pearson is NOT
copula-invariant: it falls under the lognormal map. That fall is the no-phantom
theorem's signal. If the true multi-information is the right functional, that
fall is a Gaussian-ruler artifact and local growth contributes exactly zero.

This script executes the four checks:

  (a) TRUE-MI INVARIANCE. k in {3,4,5} Gaussians with known C: true multi-
      information I = -1/2 ln det C. Apply the invertible pointwise lognormal map
      x -> exp(sigma x). Estimate I of the transformed field with a Kraskov-
      Stoegbauer-Grassberger (KSG) k-NN estimator, implemented here from scratch
      and VALIDATED FIRST on the Gaussian case where truth is known.
      PASS = transformed-field MI matches Gaussian MI within estimator error.

  (b) RANK-BASED S FLATNESS. Gaussian-rank (van der Waerden / normal-scores)
      correlation vs Pearson correlation of the lognormal field, over the
      sigma-nonlinearity ramp (0.05 -> 1.6, the s_of_a range).
      PREDICTION: S_rank flat at the linear value; S_pearson falls.

  (c) STRICT DECREASE UNDER NON-INVERTIBLE MAPS. Sign-threshold the field to +/-1.
      True MI must STRICTLY decrease (DPI). Quantify against the 2/pi Van Vleck
      arcsine attenuation documented in experiments/quantum_corridor/CALIBRATION.md.

  (d) COSMOLOGICAL IMPLICATION. Re-run the s_of_a.py nonlinear S(a) with C_rank
      instead of C_pearson. PREDICTION: dlnS_rank/dlna = 0, i.e. under the true-MI
      reading local growth contributes EXACTLY nothing to w(z), and the fixed-unit
      branch sharpens from "thawing, w >= -1" to "w = -1 exactly".

This modifies no committed theorem. It tests which FUNCTIONAL the theorems are about.

Usage: python3 copula_check.py
Outputs: results.json, fig1..fig4 png
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy.spatial import cKDTree
from scipy.special import digamma
from scipy.stats import rankdata, norm

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

# Reuse the committed machinery verbatim -- do not re-implement the cosmology.
from s_of_a import (  # noqa: E402
    PowerSpectrum, cubic_lattice, linear_corr_matrix, lognormal_corr_matrix,
    entropy_S, growth_D, dln_dlna, w_from_S,
)

SEED = 20260710
rng_global = np.random.default_rng(SEED)


# ============================================================================
# 0. THE ESTIMATOR:  Kraskov-Stoegbauer-Grassberger (2004), estimator 1,
#    generalized to the multi-information (total correlation) of m 1-D marginals.
#
#    I(X_1,...,X_m) = psi(k) + (m-1) psi(N) - < sum_j psi(n_{x_j} + 1) >
#
#    where eps_i is the distance to the i-th point's k-th nearest neighbour in
#    the JOINT space under the max (Chebyshev) norm, and n_{x_j}(i) counts the
#    points strictly within eps_i of x_j(i) in marginal j.
# ============================================================================
def ksg_multiinformation(X, k=4, standardize=True, jitter=1e-10, rng=None):
    """Multi-information of the columns of X (n, m), each column one scalar variable.

    standardize: divide each column by its std. This is an INVERTIBLE LINEAR map,
        so it preserves MI exactly; it only puts the marginals on a common scale so
        the max-norm neighbour structure is not dominated by one axis. It is NOT a
        rank transform -- the skewness of the lognormal marginals is left intact,
        which is precisely the stressor this test is meant to apply.
    """
    X = np.asarray(X, dtype=float)
    n, m = X.shape
    rng = np.random.default_rng(0) if rng is None else rng

    if standardize:
        X = (X - X.mean(0)) / X.std(0)
    if jitter:
        # break ties (KSG assumes continuous data / distinct distances)
        X = X + jitter * rng.standard_normal(X.shape) * np.maximum(X.std(0), 1e-12)

    tree = cKDTree(X)
    # k+1 because the query point is its own 0-distance neighbour
    dists, _ = tree.query(X, k=k + 1, p=np.inf, workers=-1)
    eps = dists[:, -1]

    acc = np.zeros(n)
    for j in range(m):
        xj = X[:, j:j + 1]
        tj = cKDTree(xj)
        # query_ball_point counts distance <= r and INCLUDES the point itself.
        # We want n_{x_j} + 1 with n_{x_j} counting STRICTLY within eps, excluding
        # self. Shrinking r just below eps gives exactly (n_{x_j} strictly inside)
        # + 1 (self).
        cnt = tj.query_ball_point(xj, r=eps * (1 - 1e-12) - 1e-15, p=np.inf,
                                  return_length=True, workers=-1)
        acc += digamma(np.maximum(cnt, 1))

    return float(digamma(k) + (m - 1) * digamma(n) - acc.mean())


def gauss_mi_true(C):
    """True multi-information of a Gaussian with correlation matrix C: -1/2 ln det C."""
    sign, logdet = np.linalg.slogdet(C)
    assert sign > 0, "C not positive definite"
    return float(-0.5 * logdet)


def equicorr(k, rho):
    C = np.full((k, k), float(rho))
    np.fill_diagonal(C, 1.0)
    return C


def sample_gaussian(C, n, rng):
    L = np.linalg.cholesky(C)
    return rng.standard_normal((n, C.shape[0])) @ L.T


def normal_scores_corr(X):
    """Gaussian-rank (van der Waerden) correlation: rank each margin, push through
    Phi^-1, take Pearson. For any pointwise-monotone image of a Gaussian field this
    estimates the underlying Gaussian (copula) correlation, because ranks are
    invariant under monotone maps."""
    n = X.shape[0]
    U = np.column_stack([rankdata(X[:, j]) / (n + 1.0) for j in range(X.shape[1])])
    Z = norm.ppf(U)
    C = np.corrcoef(Z, rowvar=False)
    np.fill_diagonal(C, 1.0)
    return C


def pearson_corr(X):
    C = np.corrcoef(X, rowvar=False)
    np.fill_diagonal(C, 1.0)
    return C


# ============================================================================
# ESTIMATOR VALIDATION -- do this FIRST, on the case where truth is known.
# ============================================================================
def validate_estimator(n_samples=(20_000, 50_000, 100_000, 200_000), k_knn=4,
                       n_trials=8):
    print("[0] KSG estimator validation on Gaussians (truth = -1/2 ln det C)")
    out = {"k_knn": k_knn, "n_trials": n_trials, "cases": []}
    cases = [(3, 0.3), (3, 0.6), (4, 0.4), (5, 0.5)]
    for (k, rho) in cases:
        C = equicorr(k, rho)
        truth = gauss_mi_true(C)
        for n in n_samples:
            ests = []
            for t in range(n_trials):
                rng = np.random.default_rng(SEED + 1000 * k + 97 * t + n)
                X = sample_gaussian(C, n, rng)
                ests.append(ksg_multiinformation(X, k=k_knn, rng=rng))
            ests = np.array(ests)
            rec = dict(k=k, rho=rho, n=n, truth=truth,
                       mean=float(ests.mean()), std=float(ests.std(ddof=1)),
                       bias=float(ests.mean() - truth),
                       rel_bias=float((ests.mean() - truth) / truth),
                       sem=float(ests.std(ddof=1) / np.sqrt(n_trials)))
            out["cases"].append(rec)
            print(f"    k={k} rho={rho:.1f} n={n:>7d}  truth={truth:.4f} "
                  f"est={ests.mean():.4f}+/-{ests.std(ddof=1):.4f}  "
                  f"bias={rec['bias']:+.4f} ({100*rec['rel_bias']:+.2f}%)")
    return out


# ============================================================================
# (a) TRUE-MI INVARIANCE UNDER THE INVERTIBLE POINTWISE LOGNORMAL MAP
#
# DESIGN NOTE (this matters, and a naive fixed-n test gets it wrong).
# Exact invariance of the TRUE multi-information under a strictly monotone
# pointwise map is a theorem: I depends only on the copula, and x -> exp(sigma x)
# leaves the copula untouched. So any gap between the Gaussian and lognormal
# KSG estimates is NECESSARILY estimator bias. And KSG does have such a bias:
# it grows with the skewness of the marginals (a local-density-gradient effect)
# and, because KSG is consistent, it shrinks to zero as n -> infinity.
#
# A fixed-n 3-sigma test would therefore report "FAIL" for a purely numerical
# reason. The meaningful test is the CONVERGENCE test:
#
#     Ihat(n) = I_inf + b * n^(-p)     fit over an n-ladder,
#
# then ask whether the extrapolated I_inf equals the known truth -1/2 ln det C
# AND is independent of sigma. If the map genuinely changed the MI, I_inf would
# converge to a sigma-dependent value != truth. That is the discriminating fit.
# We report the raw fixed-n table too, so the bias is visible, not hidden.
# ============================================================================
def _fit_extrapolate(ns, mus, sems):
    """Fit Ihat(n) = I_inf + b n^(-p); return (I_inf, stderr, b, p).

    When there is no systematic trend (the Gaussian control), p runs to its lower
    bound and the covariance blows up. That is a DEGENERATE fit, and the caller
    must not read a 'PASS' out of its enormous error bar -- it is handled by the
    direct (tier-1) test instead.
    """
    from scipy.optimize import curve_fit
    ns = np.asarray(ns, float); mus = np.asarray(mus, float)
    sems = np.maximum(np.asarray(sems, float), 1e-6)

    def model(n, I_inf, b, p):
        return I_inf + b * n ** (-p)

    d = np.abs(mus - mus[-1]) + 1e-9
    try:
        p0 = max(0.1, min(0.9, -np.polyfit(np.log(ns[:-1]), np.log(d[:-1]), 1)[0]))
    except Exception:
        p0 = 0.4
    b0 = (mus[0] - mus[-1]) * ns[0] ** p0
    try:
        popt, pcov = curve_fit(model, ns, mus, p0=[mus[-1], b0, p0], sigma=sems,
                               absolute_sigma=True, maxfev=400_000,
                               bounds=([-np.inf, -np.inf, 0.05], [np.inf, np.inf, 1.5]))
        err = float(np.sqrt(np.diag(pcov))[0])
        return float(popt[0]), err, float(popt[1]), float(popt[2])
    except Exception:
        return float(mus[-1]), float("inf"), float("nan"), float("nan")


def check_a_invariance(n_ladder=(25_000, 50_000, 100_000, 200_000, 400_000, 800_000),
                       k_knn=4, n_trials=3):
    """TIERED criterion (see design note above).

    tier 1 (direct):   |Ihat(n_max) - truth| <= tol, tol = max(3*sem, sys_floor).
                       Used where the estimator has already converged.
    tier 2 (extrapolated): only when tier 1 fails, i.e. a real deficit exists.
                       Require (i) the deficit shrinks with n, (ii) the fit is
                       NON-DEGENERATE, (iii) |I_inf - truth| <= max(3*fit_err, sys_floor).
    degenerate fit + tier-1 failure -> INDETERMINATE (estimator-limited), reported
    loudly; never silently a PASS.

    sys_floor is the estimator's own systematic scale, calibrated per cell from the
    untransformed Gaussian control measured at the same n: a claim cannot be held to
    a tolerance finer than the ruler's own bias on the case where truth is known.
    """
    print("\n[a] true-MI invariance under x -> exp(sigma x)  (invertible, pointwise)")
    print("    tier1: direct agreement at n_max. tier2: n->inf extrapolation.")
    print("    truth = -1/2 ln det C. A degenerate fit yields INDETERMINATE, not PASS.")
    out = {"n_ladder": list(n_ladder), "k_knn": k_knn, "n_trials": n_trials,
           "grid": [], "criterion": "tiered direct/extrapolated; see docstring"}
    ks = [3, 4, 5]
    rhos = [0.2, 0.4, 0.6]
    sigmas = [0.5, 1.0, 1.6]
    statuses = []

    for k in ks:
        for rho in rhos:
            C = equicorr(k, rho)
            truth = gauss_mi_true(C)
            channels = {"gauss": None}
            channels.update({f"sigma={s}": s for s in sigmas})
            curves = {name: {"n": [], "mean": [], "std": [], "sem": []}
                      for name in channels}

            for n in n_ladder:
                acc = {name: [] for name in channels}
                for t in range(n_trials):
                    rng = np.random.default_rng(
                        SEED + 7717 * k + 131 * t + int(1000 * rho) + n)
                    X = sample_gaussian(C, n, rng)
                    for name, s in channels.items():
                        # exp(s*X): invertible, strictly monotone, pointwise
                        Z = X if s is None else np.exp(s * X)
                        acc[name].append(ksg_multiinformation(Z, k=k_knn, rng=rng))
                for name in channels:
                    e = np.array(acc[name])
                    curves[name]["n"].append(n)
                    curves[name]["mean"].append(float(e.mean()))
                    curves[name]["std"].append(float(e.std(ddof=1)))
                    curves[name]["sem"].append(float(e.std(ddof=1) / np.sqrt(n_trials)))

            gauss_def = curves["gauss"]["mean"][-1] - truth
            sys_floor_ctrl = 0.02 * abs(truth)
            sys_floor = max(sys_floor_ctrl, 1.5 * abs(gauss_def))

            rec = dict(k=k, rho=rho, truth_MI=truth,
                       gauss_control_deficit=float(gauss_def),
                       gauss_control_rel_bias=float(gauss_def / truth),
                       sys_floor=float(sys_floor), channels={})

            for name in channels:
                cu = curves[name]
                floor = sys_floor_ctrl if name == "gauss" else sys_floor
                sem_max = cu["sem"][-1]
                direct_dev = cu["mean"][-1] - truth
                tol1 = max(3.0 * sem_max, floor)
                tier1 = bool(abs(direct_dev) <= tol1)

                defs = np.abs(np.array(cu["mean"]) - truth)
                shrinking = bool(defs[-1] < defs[0] - 1e-12)

                I_inf, I_err, b, p = _fit_extrapolate(cu["n"], cu["mean"], cu["sem"])
                degenerate = bool((not np.isfinite(I_err))
                                  or I_err > 0.15 * abs(truth)
                                  or (np.isfinite(p) and p <= 0.06))
                tol2 = max(3.0 * I_err, floor) if np.isfinite(I_err) else np.inf
                tier2 = bool((not degenerate) and shrinking
                             and abs(I_inf - truth) <= tol2)

                if tier1:
                    status = "PASS_direct"
                elif tier2:
                    status = "PASS_extrapolated"
                elif shrinking and degenerate:
                    status = "INDETERMINATE_estimator_limited"
                else:
                    status = "FAIL"
                statuses.append(status)

                rec["channels"][name] = dict(
                    n=cu["n"], mean=cu["mean"], std=cu["std"], sem=cu["sem"],
                    deficit_at_min_n=float(cu["mean"][0] - truth),
                    deficit_at_max_n=float(direct_dev),
                    rel_deficit_at_max_n=float(direct_dev / truth),
                    tier1_direct_ok=tier1, tier1_tol=float(tol1),
                    I_inf=I_inf, I_inf_stderr=I_err, fit_b=b, fit_p=p,
                    fit_degenerate=degenerate,
                    dev_I_inf_from_truth=float(I_inf - truth),
                    rel_dev_I_inf=float((I_inf - truth) / truth),
                    deficit_shrinks_with_n=shrinking,
                    status=status)
                print(f"    k={k} rho={rho:.1f} {name:>10s}  truth={truth:.4f}  "
                      f"Ihat(nmax)={cu['mean'][-1]:.4f} ({100*direct_dev/truth:+.1f}%)  "
                      f"I_inf={I_inf:.4f} (p={p:.2f}{',DEGEN' if degenerate else ''})  "
                      f"-> {status}")

            good = [rec["channels"][f"sigma={s}"]["I_inf"] for s in sigmas
                    if not rec["channels"][f"sigma={s}"]["fit_degenerate"]]
            rec["I_inf_spread_across_sigma"] = (
                float(np.max(good) - np.min(good)) if len(good) > 1 else None)
            out["grid"].append(rec)

    n_fail = sum(s == "FAIL" for s in statuses)
    n_indet = sum(s.startswith("INDETERMINATE") for s in statuses)
    out["n_channels"] = len(statuses)
    out["n_fail"] = n_fail
    out["n_indeterminate"] = n_indet
    out["n_pass"] = len(statuses) - n_fail - n_indet
    if n_fail:
        out["verdict"] = "FAIL"
    elif n_indet:
        out["verdict"] = "PASS_WITH_INDETERMINATE"
    else:
        out["verdict"] = "PASS"
    print(f"    -> {out['n_pass']}/{len(statuses)} pass, {n_indet} indeterminate, "
          f"{n_fail} fail   verdict={out['verdict']}")
    return out


# ============================================================================
# (b) RANK-BASED S FLATNESS ACROSS THE SIGMA RAMP
# ============================================================================
def check_b_rank_flatness(n_cell=3, spacing=20.0, n_samples=200_000):
    print("\n[b] rank-based S flatness vs Pearson-S decline over the sigma ramp")
    ps = PowerSpectrum("eh98", "tophat")
    R_cell = spacing * (3.0 / (4.0 * np.pi)) ** (1.0 / 3.0)
    xi = ps.xi_spline(R_cell)
    s2 = ps.sigma2_R(R_cell)
    pos = cubic_lattice(n_cell, spacing)
    c = linear_corr_matrix(pos, xi, s2)        # the LINEAR (copula) correlation
    p = c.shape[0]
    S_linear = entropy_S(c)

    sigmas = np.linspace(0.05, 1.6, 24)

    # --- ANALYTIC branch (exact) -------------------------------------------
    # Pearson correlation of the lognormal image is exactly
    #     C_NL = (exp(sig^2 c) - 1)/(exp(sig^2) - 1)      [Coles & Jones 1991]
    # The copula of a monotone pointwise image of a Gaussian is the Gaussian copula
    # with the SAME correlation c, so the rank correlation is exactly c.
    S_pearson_an = np.array([entropy_S(lognormal_corr_matrix(c, s * s)) for s in sigmas])
    S_rank_an = np.full_like(S_pearson_an, S_linear)

    # --- EMPIRICAL branch (finite samples) ---------------------------------
    rng = np.random.default_rng(SEED + 4242)
    G = sample_gaussian(c, n_samples, rng)     # one Gaussian draw, reused
    S_pearson_emp, S_rank_emp = [], []
    for s in sigmas:
        Y = np.exp(s * G)                      # monotone pointwise map
        S_pearson_emp.append(entropy_S(pearson_corr(Y)))
        S_rank_emp.append(entropy_S(normal_scores_corr(Y)))
    S_pearson_emp = np.array(S_pearson_emp)
    S_rank_emp = np.array(S_rank_emp)

    # Independent draws per sigma -> honest finite-sample scatter on S_rank
    S_rank_indep = []
    for i, s in enumerate(sigmas):
        r = np.random.default_rng(SEED + 9001 + i)
        Gi = sample_gaussian(c, n_samples, r)
        S_rank_indep.append(entropy_S(normal_scores_corr(np.exp(s * Gi))))
    S_rank_indep = np.array(S_rank_indep)

    S_rank_emp_ref = S_rank_emp[0]
    max_dev_rank_an = float(np.max(np.abs(S_rank_an - S_linear)))
    max_dev_rank_emp = float(np.max(np.abs(S_rank_emp - S_rank_emp_ref)))
    max_dev_rank_indep = float(np.max(np.abs(S_rank_indep - S_rank_indep.mean())))
    pearson_decline = float(S_pearson_an[0] - S_pearson_an[-1])
    pearson_rel_decline = float(1.0 - S_pearson_an[-1] / S_pearson_an[0])

    # finite-sample bias of -ln det on p dims from n samples (constant in sigma)
    rank_bias = float(S_rank_emp_ref - S_linear)

    print(f"    p={p} cells, S_linear={S_linear:.6f}, n={n_samples}")
    print(f"    S_pearson: {S_pearson_an[0]:.4f} (sig=0.05) -> {S_pearson_an[-1]:.4f} "
          f"(sig=1.6)   decline={pearson_decline:.4f} ({100*pearson_rel_decline:.1f}%)")
    print(f"    S_rank (analytic)          max|S_rank - S_linear| = {max_dev_rank_an:.3e}")
    print(f"    S_rank (empirical, shared) max dev across ramp    = {max_dev_rank_emp:.3e}")
    print(f"    S_rank (independent draws) max dev about mean     = {max_dev_rank_indep:.3e}")
    print(f"    finite-sample -lndet bias on S_rank (const in sigma) = {rank_bias:+.4f}")

    ratio = max_dev_rank_indep / pearson_decline
    verdict = "PASS" if (max_dev_rank_an < 1e-12 and ratio < 0.05) else "FAIL"
    print(f"    rank wobble / pearson decline = {ratio:.3e}   -> {verdict}")

    return dict(
        n_cells=p, spacing=spacing, R_cell=R_cell, sigma2_R=float(s2),
        n_samples=n_samples, S_linear=float(S_linear),
        sigmas=sigmas.tolist(),
        S_pearson_analytic=S_pearson_an.tolist(),
        S_rank_analytic=S_rank_an.tolist(),
        S_pearson_empirical=S_pearson_emp.tolist(),
        S_rank_empirical=S_rank_emp.tolist(),
        S_rank_independent_draws=S_rank_indep.tolist(),
        max_dev_rank_analytic=max_dev_rank_an,
        max_dev_rank_empirical_shared=max_dev_rank_emp,
        max_dev_rank_independent=max_dev_rank_indep,
        pearson_decline_abs=pearson_decline,
        pearson_decline_rel=pearson_rel_decline,
        rank_wobble_over_pearson_decline=float(ratio),
        rank_finite_sample_logdet_bias=rank_bias,
        pearson_emp_vs_analytic_maxdiff=float(np.max(np.abs(S_pearson_emp - S_pearson_an))),
        verdict=verdict,
        note=("Ranks are invariant under any strictly monotone pointwise map, so for a "
              "SHARED underlying Gaussian draw the normal-scores matrix is literally the "
              "same matrix at every sigma; the empirical wobble reported is exactly 0 by "
              "construction. The 'independent draws' row is the honest finite-sample "
              "scatter."),
    )


# ============================================================================
# (c) STRICT DECREASE UNDER A NON-INVERTIBLE MAP (sign thresholding)
# ============================================================================
def discrete_multiinformation(B):
    """Exact plug-in multi-information of binary columns (values in {-1,+1})."""
    n, m = B.shape
    bits = (B > 0).astype(np.int64)
    code = np.zeros(n, dtype=np.int64)
    for j in range(m):
        code |= bits[:, j] << j
    joint = np.bincount(code, minlength=2**m).astype(float) / n
    H_joint = -np.sum(joint[joint > 0] * np.log(joint[joint > 0]))
    H_marg = 0.0
    for j in range(m):
        pj = np.bincount(bits[:, j], minlength=2).astype(float) / n
        H_marg += -np.sum(pj[pj > 0] * np.log(pj[pj > 0]))
    return float(H_marg - H_joint)


def check_c_threshold_dpi(n=2_000_000):
    print("\n[c] strict decrease under the NON-invertible sign map (DPI) + Van Vleck")
    out = {"n_samples": n, "cases": []}
    strict = True
    for k in [3, 4, 5]:
        for rho in [0.1, 0.2, 0.4, 0.6]:
            C = equicorr(k, rho)
            I_gauss = gauss_mi_true(C)
            rng = np.random.default_rng(SEED + 555 * k + int(1000 * rho))
            X = sample_gaussian(C, n, rng)
            B = np.sign(X)
            I_bin = discrete_multiinformation(B)

            # Van Vleck arcsine law: E[sign(x)sign(y)] = (2/pi) arcsin(rho)
            r_vv = (2.0 / np.pi) * np.arcsin(rho)
            r_emp = float(np.mean(B[:, 0] * B[:, 1]))
            atten = r_vv / rho

            # Gaussian shadow of the thresholded field
            C_pm = (2.0 / np.pi) * np.arcsin(C)
            np.fill_diagonal(C_pm, 1.0)
            S_shadow_ratio = gauss_mi_true(C_pm) / I_gauss

            decreased = bool(I_bin < I_gauss - 1e-9)
            strict &= decreased
            ratio = I_bin / I_gauss
            # leading order small-rho prediction: I ~ (1/2) sum_{i<j} r_ij^2
            # so I_bin / I_gauss -> (2/pi)^2 = 0.4053 as rho -> 0
            rec = dict(k=k, rho=rho, I_gauss=I_gauss, I_binary=I_bin,
                       ratio_Ibin_over_Igauss=float(ratio),
                       strictly_decreased=decreased,
                       vanvleck_r=float(r_vv), empirical_pm_corr=r_emp,
                       vanvleck_atten_factor=float(atten),
                       two_over_pi=float(2.0 / np.pi),
                       two_over_pi_squared=float((2.0 / np.pi) ** 2),
                       gaussian_shadow_MI_ratio=float(S_shadow_ratio))
            out["cases"].append(rec)
            print(f"    k={k} rho={rho:.1f}  I_gauss={I_gauss:.5f}  I_bin={I_bin:.5f}  "
                  f"ratio={ratio:.4f}  atten={atten:.4f} (2/pi={2/np.pi:.4f})  "
                  f"{'DECREASE' if decreased else 'NO-DECREASE'}")

    # small-rho limit check of the (2/pi)^2 prediction
    small = [c for c in out["cases"] if c["rho"] == 0.1]
    out["small_rho_ratio_mean"] = float(np.mean([c["ratio_Ibin_over_Igauss"] for c in small]))
    out["small_rho_predicted_(2/pi)^2"] = float((2.0 / np.pi) ** 2)
    out["verdict"] = "PASS" if strict else "FAIL"
    print(f"    small-rho (0.1) mean I_bin/I_gauss = {out['small_rho_ratio_mean']:.4f}  "
          f"vs (2/pi)^2 = {(2/np.pi)**2:.4f}")
    return out


# ============================================================================
# (d) THE COSMOLOGICAL IMPLICATION:  S_rank(a) instead of S_pearson(a)
# ============================================================================
def check_d_cosmology(n_cell=3, spacing=20.0, n_samples=100_000, n_seeds=6):
    print("\n[d] S(a) with C_rank instead of C_pearson -> dlnS_rank/dlna")
    ps = PowerSpectrum("eh98", "tophat")
    R_cell = spacing * (3.0 / (4.0 * np.pi)) ** (1.0 / 3.0)
    xi = ps.xi_spline(R_cell)
    s2 = ps.sigma2_R(R_cell)
    pos = cubic_lattice(n_cell, spacing)
    c = linear_corr_matrix(pos, xi, s2)
    S_linear = entropy_S(c)

    a_grid = np.linspace(0.30, 1.0, 60)
    D = growth_D(a_grid)

    # --- Pearson branch: the committed no-phantom computation (analytic, exact) ---
    S_pearson = np.array([entropy_S(lognormal_corr_matrix(c, s2 * d * d)) for d in D])
    dls_pearson = dln_dlna(a_grid, S_pearson)
    w_pearson = w_from_S(a_grid, S_pearson)

    # --- Rank branch: analytic. The lognormal map at every a is strictly monotone in
    #     the underlying Gaussian, and the NORMALIZED linear correlation c is itself
    #     a-independent (D(a) cancels). So the copula is the SAME Gaussian copula at
    #     every a: C_rank(a) = c, S_rank(a) = -ln det c = const, dlnS_rank/dlna = 0.
    S_rank_an = np.full_like(S_pearson, S_linear)
    dls_rank_an = dln_dlna(a_grid, S_rank_an)

    # --- Rank branch: finite samples, INDEPENDENT draw at each a (honest error bars) ---
    a_sub = np.linspace(0.30, 1.0, 12)
    D_sub = growth_D(a_sub)
    dls_rank_emp = []
    S_rank_curves = []
    for sd in range(n_seeds):
        S_r = []
        for i, a in enumerate(a_sub):
            r = np.random.default_rng(SEED + 31337 * sd + 17 * i)
            G = sample_gaussian(c, n_samples, r)
            sig = np.sqrt(s2) * D_sub[i]
            delta = np.exp(sig * G - 0.5 * sig**2) - 1.0   # the s_of_a lognormal field
            S_r.append(entropy_S(normal_scores_corr(delta)))
        S_r = np.array(S_r)
        S_rank_curves.append(S_r.tolist())
        dls_rank_emp.append(dln_dlna(a_sub, S_r))
    dls_rank_emp = np.array(dls_rank_emp)          # (n_seeds, len(a_sub))

    # today's value
    d_rank_today = dls_rank_emp[:, -1]
    d_rank_mean = float(d_rank_today.mean())
    d_rank_sem = float(d_rank_today.std(ddof=1) / np.sqrt(n_seeds))
    d_rank_sd = float(d_rank_today.std(ddof=1))
    d_pearson_today = float(dls_pearson[-1])

    # whole-curve summary
    d_rank_all_mean = float(dls_rank_emp.mean())
    d_rank_all_sd = float(dls_rank_emp.std(ddof=1))

    nsig_from_zero = abs(d_rank_mean) / d_rank_sem if d_rank_sem > 0 else np.inf
    nsig_pearson = abs(d_pearson_today) / d_rank_sem if d_rank_sem > 0 else np.inf

    w_rank_today = -1.0 - d_rank_mean / 3.0
    w_rank_err = d_rank_sem / 3.0

    consistent_with_zero = bool(nsig_from_zero < 3.0)
    verdict = "PASS" if consistent_with_zero else "FAIL"

    print(f"    S_linear = {S_linear:.6f}")
    print(f"    PEARSON  dlnS/dlna|_0 = {d_pearson_today:+.5f}  -> w_0 = "
          f"{w_pearson[-1]:+.5f}  (thawing, w > -1)")
    print(f"    RANK (analytic)   dlnS/dlna|_0 = {dls_rank_an[-1]:+.3e}  (identically 0)")
    print(f"    RANK (empirical)  dlnS/dlna|_0 = {d_rank_mean:+.5f} +/- {d_rank_sem:.5f} "
          f"(sem, {n_seeds} seeds)  -> {nsig_from_zero:.2f} sigma from 0")
    print(f"    -> w_rank(a=1) = {w_rank_today:+.5f} +/- {w_rank_err:.5f}")
    print(f"    Pearson signal is {nsig_pearson:.1f} sigma in the same units -> "
          f"the two functionals are cleanly discriminated")
    print(f"    verdict: {verdict}")

    return dict(
        n_cells=int(c.shape[0]), spacing=spacing, R_cell=R_cell, sigma2_R=float(s2),
        S_linear=float(S_linear), n_samples=n_samples, n_seeds=n_seeds,
        a_grid=a_grid.tolist(), a_sub=a_sub.tolist(),
        S_pearson=S_pearson.tolist(),
        dlnS_dlna_pearson=dls_pearson.tolist(),
        w_pearson=w_pearson.tolist(),
        dlnS_dlna_pearson_today=d_pearson_today,
        w_pearson_today=float(w_pearson[-1]),
        S_rank_analytic=S_rank_an.tolist(),
        dlnS_dlna_rank_analytic_today=float(dls_rank_an[-1]),
        S_rank_empirical_curves=S_rank_curves,
        dlnS_dlna_rank_empirical=dls_rank_emp.tolist(),
        dlnS_dlna_rank_today_mean=d_rank_mean,
        dlnS_dlna_rank_today_sd=d_rank_sd,
        dlnS_dlna_rank_today_sem=d_rank_sem,
        dlnS_dlna_rank_allcurve_mean=d_rank_all_mean,
        dlnS_dlna_rank_allcurve_sd=d_rank_all_sd,
        n_sigma_rank_from_zero=float(nsig_from_zero),
        n_sigma_pearson_in_rank_units=float(nsig_pearson),
        w_rank_today=float(w_rank_today), w_rank_today_err=float(w_rank_err),
        consistent_with_w_minus_one=consistent_with_zero,
        verdict=verdict,
    )


# ============================================================================
# figures
# ============================================================================
def make_figures(res):
    # fig1: estimator validation
    v = res["estimator_validation"]["cases"]
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
    keys = sorted({(c["k"], c["rho"]) for c in v})
    for (k, rho) in keys:
        sub = [c for c in v if c["k"] == k and c["rho"] == rho]
        ns = [c["n"] for c in sub]
        rb = [100 * c["rel_bias"] for c in sub]
        sd = [100 * c["std"] / c["truth"] for c in sub]
        ax[0].semilogx(ns, rb, "o-", label=f"k={k}, $\\rho$={rho}")
        ax[1].loglog(ns, sd, "s-", label=f"k={k}, $\\rho$={rho}")
    ax[0].axhline(0, color="k", lw=0.7)
    ax[0].set_xlabel("$n$ samples"); ax[0].set_ylabel("relative bias [%]")
    ax[0].set_title("KSG bias vs truth $-\\frac{1}{2}\\ln\\det C$"); ax[0].legend(fontsize=7)
    ax[1].set_xlabel("$n$ samples"); ax[1].set_ylabel("relative std [%]")
    ax[1].set_title("KSG dispersion"); ax[1].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(HERE / "fig1_estimator_validation.png", dpi=140)
    plt.close(fig)

    # fig2: (a) invariance -- left: the n-ladder convergence for one hard case;
    #                        right: extrapolated intercept vs truth across the grid
    g = res["a_true_mi_invariance"]["grid"]
    names = ["gauss", "sigma=0.5", "sigma=1.0", "sigma=1.6"]
    cols = {"gauss": "k", "sigma=0.5": "crimson", "sigma=1.0": "steelblue",
            "sigma=1.6": "seagreen"}
    hard = max(g, key=lambda r: (r["k"], r["rho"]))
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.0))
    for nm in names:
        ch = hard["channels"][nm]
        ns = np.array(ch["n"], float)
        ax[0].errorbar(ns, np.array(ch["mean"]) - hard["truth_MI"],
                       yerr=ch["sem"], fmt="o-", ms=4, capsize=2,
                       color=cols[nm], label=nm)
        nn = np.logspace(np.log10(ns[0]), np.log10(4e7), 100)
        if np.isfinite(ch["fit_p"]):
            ax[0].plot(nn, ch["I_inf"] + ch["fit_b"] * nn ** (-ch["fit_p"])
                       - hard["truth_MI"], "--", lw=0.8, color=cols[nm], alpha=0.6)
    ax[0].axhline(0, color="k", lw=0.9, ls=":")
    ax[0].set_xscale("log")
    ax[0].set_xlabel("$n$ samples")
    ax[0].set_ylabel("$\\hat I - I_{\\rm true}$  [nats]")
    ax[0].set_title(f"(a) KSG bias vanishes as $n\\to\\infty$  "
                    f"(k={hard['k']}, $\\rho$={hard['rho']})")
    ax[0].legend(fontsize=7)

    for i, rec in enumerate(g):
        for j, nm in enumerate(names):
            ch = rec["channels"][nm]
            off = 0.16 * (j - 1.5)
            budget = max(ch["I_inf_stderr"], ch["sem"][-1])
            ax[1].errorbar(i + off, ch["I_inf"] - rec["truth_MI"], yerr=budget,
                           fmt="o", ms=4, capsize=2, color=cols[nm],
                           label=nm if i == 0 else None)
    ax[1].axhline(0, color="k", lw=0.9, ls=":")
    ax[1].set_xticks(range(len(g)))
    ax[1].set_xticklabels([f"k={r['k']}\n$\\rho$={r['rho']}" for r in g], fontsize=6.5)
    ax[1].set_ylabel("$I_\\infty - I_{\\rm true}$  [nats]")
    ax[1].set_title("Extrapolated intercept recovers truth, $\\sigma$-independently")
    ax[1].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(HERE / "fig2_mi_invariance.png", dpi=140)
    plt.close(fig)

    # fig3: (b) rank flatness
    b = res["b_rank_flatness"]
    s = np.array(b["sigmas"])
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
    ax[0].plot(s, b["S_pearson_analytic"], "-", color="crimson",
               label="$S_{\\rm Pearson}$ (Gaussian ruler)")
    ax[0].plot(s, b["S_rank_analytic"], "-", color="steelblue",
               label="$S_{\\rm rank}$ (copula)")
    ax[0].plot(s, b["S_rank_independent_draws"], ".", color="steelblue", ms=4,
               alpha=0.6, label="$S_{\\rm rank}$ indep. draws")
    ax[0].axhline(b["S_linear"], color="k", ls=":", lw=0.8, label="$S_{\\rm linear}$")
    ax[0].set_xlabel("$\\sigma$ (nonlinearity)"); ax[0].set_ylabel("$S$")
    ax[0].set_title("(b) Pearson-$S$ falls, rank-$S$ is flat"); ax[0].legend(fontsize=7)
    ax[1].semilogy(s, np.abs(np.array(b["S_pearson_analytic"]) - b["S_pearson_analytic"][0]) + 1e-18,
                   "-", color="crimson", label="$|\\Delta S_{\\rm Pearson}|$")
    ax[1].semilogy(s, np.abs(np.array(b["S_rank_analytic"]) - b["S_linear"]) + 1e-18,
                   "-", color="steelblue", label="$|\\Delta S_{\\rm rank}|$ analytic")
    ax[1].semilogy(s, np.abs(np.array(b["S_rank_independent_draws"])
                             - np.mean(b["S_rank_independent_draws"])) + 1e-18,
                   ".", color="steelblue", alpha=0.6, ms=4, label="indep. draws scatter")
    ax[1].set_xlabel("$\\sigma$"); ax[1].set_ylabel("$|\\Delta S|$")
    ax[1].set_title("The discriminator"); ax[1].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(HERE / "fig3_rank_flatness.png", dpi=140)
    plt.close(fig)

    # fig4: (d) cosmology
    d = res["d_cosmology"]
    a = np.array(d["a_grid"]); a_sub = np.array(d["a_sub"])
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.9))
    Sp = np.array(d["S_pearson"])
    ax[0].plot(a, Sp / Sp[0], "-", color="crimson", label="$S_{\\rm Pearson}(a)$")
    ax[0].plot(a, np.ones_like(a), "-", color="steelblue", label="$S_{\\rm rank}(a)$ (flat)")
    for cur in d["S_rank_empirical_curves"]:
        cur = np.array(cur)
        ax[0].plot(a_sub, cur / cur[0], ".", color="steelblue", ms=3, alpha=0.45)
    ax[0].set_xlabel("$a$"); ax[0].set_ylabel("$S(a)/S(a_{\\min})$")
    ax[0].set_title("(d) Local growth moves the Gaussian ruler, not the copula")
    ax[0].legend(fontsize=7)

    ax[1].plot(a, d["dlnS_dlna_pearson"], "-", color="crimson", label="Pearson")
    de = np.array(d["dlnS_dlna_rank_empirical"])
    ax[1].errorbar(a_sub, de.mean(0), yerr=de.std(0, ddof=1) / np.sqrt(de.shape[0]),
                   fmt="o", ms=3, capsize=2, color="steelblue",
                   label="rank (empirical $\\pm$ sem)")
    ax[1].axhline(0, color="k", lw=0.8, ls=":")
    ax[1].axhspan(-0.5, -0.3, color="green", alpha=0.10, label="DESI requires today")
    ax[1].set_xlabel("$a$"); ax[1].set_ylabel("$d\\ln S/d\\ln a$")
    ax[1].set_title("$1+w = -\\frac{1}{3} d\\ln S/d\\ln a$"); ax[1].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(HERE / "fig4_cosmology_rank.png", dpi=140)
    plt.close(fig)


def main():
    res = {"seed": SEED,
           "what": "copula-invariance verification pass (copula_invariance_remark.md sec.3)",
           "modifies": "interpretation only; no committed theorem is touched"}

    res["estimator_validation"] = validate_estimator()
    res["a_true_mi_invariance"] = check_a_invariance()
    res["b_rank_flatness"] = check_b_rank_flatness()
    res["c_threshold_dpi"] = check_c_threshold_dpi()
    res["d_cosmology"] = check_d_cosmology()

    res["verdicts"] = {
        "a_true_mi_invariance": res["a_true_mi_invariance"]["verdict"],
        "b_rank_flatness": res["b_rank_flatness"]["verdict"],
        "c_threshold_dpi": res["c_threshold_dpi"]["verdict"],
        "d_cosmology": res["d_cosmology"]["verdict"],
    }

    make_figures(res)

    def sanitize(o):
        if isinstance(o, dict):
            return {k: sanitize(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [sanitize(v) for v in o]
        if isinstance(o, (np.floating, np.integer)):
            o = o.item()
        if isinstance(o, float) and not np.isfinite(o):
            return None
        return o

    with open(HERE / "results.json", "w") as f:
        json.dump(sanitize(res), f, indent=2)

    print("\n" + "=" * 72)
    for k, v in res["verdicts"].items():
        print(f"  {k:28s} {v}")
    print("=" * 72)
    print("wrote results.json + fig1..fig4")
    return res


if __name__ == "__main__":
    main()
