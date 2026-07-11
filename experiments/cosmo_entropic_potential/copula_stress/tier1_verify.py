"""
TIER 1 — VERIFY on synthetic Gaussians.

Confirm S_pipeline (-ln det C) = 2 * I where I is computed BOTH as -0.5 ln det C
(analytic) AND via the KSG multi-information estimator on samples. Validate that the
KSG estimator recovers -0.5 ln det C to its sampling error. Sweep dimension m and
correlation strength rho (uniform-rho / Kish matrices) plus a random-correlation case.

Writes results incrementally to results.json under key 'tier1'.
"""
import json, os, time
import numpy as np
from copula_lib import (kish_corr, kish_MI, analytic_gaussian_MI,
                        ksg_multiinformation, gaussian_copula_MI)

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


def random_corr(m, rng, strength=0.5):
    A = rng.standard_normal((m, m)) * strength
    C = A @ A.T + np.eye(m)
    d = np.sqrt(np.diag(C))
    return C / np.outer(d, d)


def sample_mvn(C, N, rng):
    L = np.linalg.cholesky(C)
    return rng.standard_normal((N, C.shape[0])) @ L.T


def main():
    rng = np.random.default_rng(12345)
    results = load_results()
    out = {"description": "KSG vs analytic -0.5 ln det C on synthetic Gaussians",
           "k_knn": 4, "n_repeats": 8, "cases": []}

    m_grid = [2, 3, 5, 8]
    rho_grid = [0.1, 0.3, 0.5, 0.7]
    N_grid = [2000, 8000, 32000]
    k_knn = 4
    n_rep = 8

    t0 = time.time()
    for m in m_grid:
        # uniform-rho (Kish) matrices
        for rho in rho_grid:
            C = kish_corr(m, rho)
            I_true = kish_MI(m, rho)          # = -0.5 ln det C, analytic
            S_true = 2 * I_true               # entropic potential
            # confirm identity numerically vs slogdet on the actual matrix
            I_logdet = analytic_gaussian_MI(C)
            for N in N_grid:
                ksg_vals = []
                gc_vals = []
                for r in range(n_rep):
                    X = sample_mvn(C, N, rng)
                    ksg_vals.append(ksg_multiinformation(X, k=k_knn, rng=rng))
                    gc, _, _ = gaussian_copula_MI(X)
                    gc_vals.append(gc)
                ksg = np.array(ksg_vals); gc = np.array(gc_vals)
                case = dict(family="kish", m=m, rho=rho, N=N,
                            I_analytic=I_true, S_analytic=S_true,
                            I_analytic_slogdet=I_logdet,
                            ksg_mean=float(ksg.mean()), ksg_sd=float(ksg.std(ddof=1)),
                            ksg_bias=float(ksg.mean() - I_true),
                            ksg_sem=float(ksg.std(ddof=1) / np.sqrt(n_rep)),
                            gcopula_mean=float(gc.mean()),
                            gcopula_bias=float(gc.mean() - I_true))
                out["cases"].append(case)
                print(f"kish m={m} rho={rho} N={N:6d}: I={I_true:.4f} "
                      f"KSG={ksg.mean():.4f}±{ksg.std(ddof=1):.4f} "
                      f"(bias {ksg.mean()-I_true:+.4f})  Gcop={gc.mean():.4f}")
        # random-correlation case at largest N
        C = random_corr(m, rng)
        I_true = analytic_gaussian_MI(C)
        N = 32000
        ksg_vals = [ksg_multiinformation(sample_mvn(C, N, rng), k=k_knn, rng=rng)
                    for _ in range(n_rep)]
        ksg = np.array(ksg_vals)
        out["cases"].append(dict(family="random", m=m, rho=None, N=N,
                                 I_analytic=I_true, S_analytic=2 * I_true,
                                 ksg_mean=float(ksg.mean()),
                                 ksg_sd=float(ksg.std(ddof=1)),
                                 ksg_bias=float(ksg.mean() - I_true),
                                 ksg_sem=float(ksg.std(ddof=1) / np.sqrt(n_rep))))
        print(f"random m={m} N={N}: I={I_true:.4f} KSG={ksg.mean():.4f} "
              f"(bias {ksg.mean()-I_true:+.4f})")
        # flush after each m
        results["tier1"] = out
        save_results(results)

    out["walltime_s"] = time.time() - t0
    results["tier1"] = out
    save_results(results)
    print(f"\nTIER 1 done in {out['walltime_s']:.1f}s. cases={len(out['cases'])}")


if __name__ == "__main__":
    main()
