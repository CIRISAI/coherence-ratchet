"""
TIER 3 — THE REAL TEST: the N-body copula gap.

On the TNG300 halo catalogs (205 Mpc/h) across z = 3 -> 0, build a density field by
CIC gridding, sample sets of m cells under statistical homogeneity (a fixed template
of relative offsets slid over every periodic origin = ng^3 samples of the m-tuple),
rank-transform to the empirical copula, estimate I_true via KSG, and compare to the
Gaussian-copula baseline -0.5 ln det C_rank on the SAME cells.

The GAP = I_true - I_gaussian_copula is the higher-order coordination the pipeline's
2-point log-det misses. We report:
  - gap_analytic  = I_KSG(real) - I_gauss_analytic   (contaminated by KSG bias)
  - gap_matched   = I_KSG(real) - I_KSG(surrogate)   (bias-cancelled; THE estimator)
    where surrogate = MVN with the same rank-correlation C_rank (exact Gaussian copula).

MEASURE: gap vs SCALE (template separation / grid resolution), gap vs REDSHIFT,
and the SIGN of the gap (adds coordination, or inverts like the fermionic Hubbard).

Writes to results.json under 'tier3'. Incremental flush per snapshot.
"""
import json, os, time, glob
import numpy as np
from copula_lib import (cic_grid, template_samples, ksg_multiinformation,
                        gaussian_copula_MI, gaussian_surrogate, normal_scores)

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.json")
DATA = os.path.join(HERE, "..", "large_volume", "data")
BOX = 205.0  # Mpc/h, TNG300


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


def line_template(m, sep):
    """m cells along the x-axis separated by `sep` grid cells."""
    return [(i * sep, 0, 0) for i in range(m)]


def block_template(side):
    """side^3 compact block of adjacent cells (m = side^3)."""
    return [(i, j, k) for i in range(side) for j in range(side) for k in range(side)]


def measure_gap(field, offsets, k_knn, rng, cell_mpc, n_surr=6, n_real=3):
    """Return the gap dict for one template on one field.
    gap_matched = I_KSG(real) - I_KSG(surrogate), with a surrogate NULL of n_surr
    Gaussian-copula draws (same C_rank) giving the null spread -> a z-score. The real
    KSG is re-jittered n_real times for its own (small) variance."""
    X = template_samples(field, offsets)          # (ng^3, m)
    N, m = X.shape
    # rank/normal-score correlation -> Gaussian-copula baseline
    I_gauss, C_rank, n_clip = gaussian_copula_MI(X)
    # true MI via KSG on the empirical copula (a few re-jitters for its variance)
    real_vals = [ksg_multiinformation(X, k=k_knn, rng=rng) for _ in range(n_real)]
    I_ksg_real = float(np.mean(real_vals))
    real_sd = float(np.std(real_vals, ddof=1)) if n_real > 1 else 0.0
    # bias-cancelling surrogate NULL: MVN with same rank correlation (Gaussian copula)
    surr_vals = []
    for _ in range(n_surr):
        Z = gaussian_surrogate(C_rank, N, rng)
        surr_vals.append(ksg_multiinformation(Z, k=k_knn, rng=rng))
    surr_vals = np.array(surr_vals)
    I_ksg_surr = float(surr_vals.mean())
    surr_sd = float(surr_vals.std(ddof=1))
    gap = I_ksg_real - I_ksg_surr
    # significance: gap over combined null spread of the two KSG estimates
    denom = np.sqrt(surr_sd ** 2 + real_sd ** 2) + 1e-12
    off = C_rank[np.triu_indices(m, 1)]
    return dict(
        m=m, N=int(N), cell_mpc=float(cell_mpc), n_clip=int(n_clip),
        mean_offdiag_rankcorr=float(off.mean()),
        max_offdiag_rankcorr=float(off.max()),
        I_gauss_copula=float(I_gauss),
        I_ksg_real=I_ksg_real, I_ksg_real_sd=real_sd,
        I_ksg_surrogate=I_ksg_surr, I_ksg_surrogate_sd=surr_sd,
        gap_analytic=float(I_ksg_real - I_gauss),
        gap_matched=float(gap),
        gap_matched_z=float(gap / denom),
    )


def main():
    rng = np.random.default_rng(2024)
    results = load_results()
    k_knn = 4

    # snapshots spanning z=3 -> 0 (subset for tractability)
    files = {
        "025": None, "033": None, "042": None, "051": None,
        "059": None, "067": None, "076": None, "087": None, "099": None,
    }
    snaps = []
    for s in files:
        f = os.path.join(DATA, f"tng300_groups_{s}.npz")
        if os.path.exists(f):
            snaps.append((s, f))

    out = {
        "description": "N-body copula gap on TNG300 halos: I_true(KSG) vs "
                       "-0.5 ln det C_rank, vs scale and redshift.",
        "box_mpc": BOX, "k_knn": k_knn,
        "weighting": "number (CIC deposit, weight=1 per halo)",
        "note": "gap_matched = I_KSG(real) - I_KSG(surrogate) cancels KSG bias; "
                "sign: + = higher-order copula ADDS coordination, - = INVERTS.",
        "snapshots": [],
    }

    # grid resolutions (scale via cell size) and templates
    ng_list = [16, 32, 48]           # cell sizes: 205/ng ~ 12.8, 6.4, 4.3 Mpc/h
    m_line = 6                        # line template length
    sep_list = [1, 2, 4]             # separations in cells

    t0 = time.time()
    for s, f in snaps:
        d = np.load(f)
        pos = d["pos"]; z = float(d["z"])
        snap_rec = {"snap": s, "z": z, "n_halos": int(pos.shape[0]), "configs": []}
        for ng in ng_list:
            field = cic_grid(pos, BOX, ng, weights=None)  # number field
            cell = BOX / ng
            # line templates at several separations (the primary scale axis)
            for sep in sep_list:
                if (m_line - 1) * sep >= ng:      # template must fit inside box
                    continue
                offs = line_template(m_line, sep)
                rec = measure_gap(field, offs, k_knn, rng, cell)
                rec.update(ng=ng, template="line", sep=sep,
                           separation_mpc=float(sep * cell))
                snap_rec["configs"].append(rec)
            # a compact 2x2x2 block (m=8) at this resolution
            offs = block_template(2)
            rec = measure_gap(field, offs, k_knn, rng, cell)
            rec.update(ng=ng, template="block2", sep=1,
                       separation_mpc=float(cell))
            snap_rec["configs"].append(rec)
        out["snapshots"].append(snap_rec)
        results["tier3"] = out
        save_results(results)
        # progress print
        for c in snap_rec["configs"]:
            print(f"z={z:5.2f} ng={c['ng']:2d} {c['template']:6s} sep={c['sep']} "
                  f"cell={c['cell_mpc']:4.1f} sepMpc={c['separation_mpc']:4.1f} "
                  f"rbar={c['mean_offdiag_rankcorr']:+.3f} "
                  f"Igauss={c['I_gauss_copula']:.4f} "
                  f"gap_m={c['gap_matched']:+.4f} z={c['gap_matched_z']:+.1f} "
                  f"gap_a={c['gap_analytic']:+.4f}")
        print("-" * 80)

    out["walltime_s"] = time.time() - t0
    results["tier3"] = out
    save_results(results)
    print(f"\nTIER 3 done in {out['walltime_s']:.1f}s.")


if __name__ == "__main__":
    main()
