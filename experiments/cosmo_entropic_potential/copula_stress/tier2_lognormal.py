"""
TIER 2 — LOGNORMAL: the decisive demonstration that S/I is a COPULA functional.

A lognormal field delta = exp(g), g ~ N(0, C_g), has a GAUSSIAN COPULA by
construction (delta is a monotone map of a Gaussian). So:

  (a) COPULA INVARIANCE: S/I computed via the rank correlation of delta equals that
      of g  --  the monotone map exp changes nothing the copula sees.
  (b) ZERO COPULA GAP: the TRUE multi-information I_true(delta) (KSG on the samples)
      equals -0.5 ln det C_rank to estimator error, DESPITE maximally non-Gaussian
      (lognormal) marginals.
  (c) THE COSMOLOGY WRINKLE: the PEARSON correlation of delta differs from that of g
      (the ln(1+xi) relation, xi_delta = exp(xi_g)-1 for unit-variance g... more
      generally C_delta = (exp(C_g sig^2)-1)/(exp(sig^2)-1)). So -0.5 ln det C_pearson
      is WRONG while -0.5 ln det C_rank is RIGHT. We quantify the Pearson error.

This localizes WHICH '2-point' the pipeline must use: the rank/normal-score
correlation, not the field-Pearson correlation.

Writes to results.json under 'tier2'.
"""
import json, os, time
import numpy as np
from copula_lib import (ksg_multiinformation, gaussian_copula_MI,
                        analytic_gaussian_MI, normal_scores, kish_corr)

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.json")


def load_results():
    if os.path.exists(RESULTS):
        with open(RESULTS) as f:
            return json.load(f)
    return {}


def save_results(r):
    tmp = RESULTS + ".tmp"
    with open(tmp, "w") as f:
        json.dump(r, f, indent=2)
    os.replace(tmp, RESULTS)


def sample_mvn(C, N, rng):
    L = np.linalg.cholesky(C)
    return rng.standard_normal((N, C.shape[0])) @ L.T


def lognormal_pearson_corr(C_g, sigma):
    """Analytic Pearson correlation of delta=exp(sigma*g)-... for g~N(0,C_g) unit-var.
    For X_i = exp(sigma z_i), z std normal with corr r: corr(X_i,X_j) =
    (exp(sigma^2 r)-1)/(exp(sigma^2)-1)."""
    num = np.exp(sigma ** 2 * C_g) - 1.0
    den = np.exp(sigma ** 2) - 1.0
    return num / den


def main():
    rng = np.random.default_rng(999)
    results = load_results()
    out = {"description": "lognormal field: Gaussian copula => zero copula gap; "
                          "Pearson-vs-rank correlation error",
           "cases": []}
    N = 100000
    k_knn = 4
    m_grid = [3, 5, 8]
    rho_grid = [0.2, 0.4, 0.6]
    sigma_grid = [0.5, 1.0, 1.5]   # marginal non-Gaussianity: sigma of log-field

    t0 = time.time()
    for m in m_grid:
        for rho in rho_grid:
            C_g = kish_corr(m, rho)
            I_gauss_true = analytic_gaussian_MI(C_g)   # copula truth (of g)
            for sigma in sigma_grid:
                g = sample_mvn(C_g, N, rng)            # Gaussian field
                delta = np.exp(sigma * g)              # lognormal field (monotone map)
                # (a) copula invariance: rank/normal-score correlation of delta == of g
                I_rank_delta, C_rank_delta, _ = gaussian_copula_MI(delta)
                I_rank_g, _, _ = gaussian_copula_MI(g)
                # (b) true MI via KSG on lognormal samples
                I_ksg_delta = ksg_multiinformation(delta, k=k_knn, rng=rng)
                I_ksg_g = ksg_multiinformation(g, k=k_knn, rng=rng)
                # (c) Pearson correlation of delta (WRONG ruler) vs analytic
                C_pear = np.corrcoef(delta, rowvar=False)
                I_pear = analytic_gaussian_MI(C_pear)
                C_pear_analytic = lognormal_pearson_corr(C_g, sigma)
                I_pear_analytic = analytic_gaussian_MI(C_pear_analytic)

                case = dict(
                    m=m, rho=rho, sigma=sigma, N=N,
                    I_gauss_copula_truth=I_gauss_true,
                    # (a)
                    I_rank_delta=I_rank_delta, I_rank_g=I_rank_g,
                    rank_invariance_dev=float(I_rank_delta - I_rank_g),
                    # (b) copula gap = KSG(delta) - Gaussian-copula baseline
                    I_ksg_delta=I_ksg_delta, I_ksg_g=I_ksg_g,
                    copula_gap=float(I_ksg_delta - I_rank_delta),
                    copula_gap_vs_truth=float(I_ksg_delta - I_gauss_true),
                    # (c) Pearson error
                    I_pearson_delta=I_pear,
                    I_pearson_analytic=I_pear_analytic,
                    pearson_error=float(I_pear - I_gauss_true),
                    pearson_rel_error=float((I_pear - I_gauss_true) /
                                            max(I_gauss_true, 1e-9)),
                )
                out["cases"].append(case)
                print(f"m={m} rho={rho} sig={sigma}: "
                      f"I_copula_truth={I_gauss_true:.4f} "
                      f"I_rank(delta)={I_rank_delta:.4f} "
                      f"KSG(delta)={I_ksg_delta:.4f} "
                      f"gap={I_ksg_delta - I_rank_delta:+.4f} | "
                      f"I_pearson(delta)={I_pear:.4f} "
                      f"(err {I_pear - I_gauss_true:+.4f})")
            results["tier2"] = out
            save_results(results)

    out["walltime_s"] = time.time() - t0
    results["tier2"] = out
    save_results(results)
    print(f"\nTIER 2 done in {out['walltime_s']:.1f}s. cases={len(out['cases'])}")


if __name__ == "__main__":
    main()
