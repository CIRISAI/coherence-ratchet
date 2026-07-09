#!/usr/bin/env python3
"""
Calibration leg (N5) of the quantum-corridor spec (SPEC.md §4.4).

Pushes every synthetic state class through the IDENTICAL estimator front-end used on
real substrates, at the substrate's (N,T): Sycamore-like N=53 with S in {1e4,1e5,5e5},
and IBM-like N=20. For each (class, N, S):
  - build the outcome correlation matrix C over shots (Operationalization A, §4.2),
  - subsample-PR beta fit (numerics identical to spectral_test.py; ported verbatim
    below with the source named),
  - beta bootstrap CI (resample shots with replacement),
  - PR / k_eff, eff-rank vs phase-randomized surrogate, rho_bar (mean off-diagonal),
  - measured potential S(k,rho_bar) = -ln(1+rho(k-1)) - (k-1)ln(1-rho).

N5 question answered plainly: do the classes SEPARATE (does beta tell low-rank from
power-law from noise) at each (N,S)?

C3 leg: sweep the depolarized-GHZ ramp p, record the (rho_bar, S) trajectory, and
compare measured S against the parameter-free -(k-1)ln(1-rho_bar) curve; report the
deviation band.

Real data: NONE. Classical surrogates only. Fixed RNG seed.
"""
import os, sys, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "keff_saturation"))

# Reuse the validated core unchanged (corr_eig, participation_ratio, mp_edge).
from spectral_test import corr_eig, participation_ratio, mp_edge  # noqa: E402
import synth_shots as ss                                          # noqa: E402

SEED = 20260709
BASE_RNG = np.random.default_rng(SEED)


# --- ported verbatim from spectral_test.py (subsample_pr / phase_randomize), with an
#     explicit RNG so seeding is controlled here; numerics are identical. -------------
def phase_randomize(X, rng):
    F = np.fft.rfft(X, axis=1)
    ph = np.exp(1j * rng.uniform(0, 2 * np.pi, F.shape))
    ph[:, 0] = 1
    return np.fft.irfft(F * ph, n=X.shape[1], axis=1)


def corr_matrix(X):
    """Row-z-scored correlation matrix (identical to corr_eig's C, before eig)."""
    Z = (X - X.mean(1, keepdims=True)) / X.std(1, keepdims=True)
    return (Z @ Z.T) / X.shape[1]


def subsample_pr(C, sizes, rng, ndraw=25):
    """
    Subsample-PR curve. Numerically identical to spectral_test.subsample_pr: because
    the correlation is z-scored PER ROW, the correlation matrix of a row subset equals
    the corresponding sub-block of the full matrix C, so we subsample C directly instead
    of recomputing Z@Z.T per draw (removes the O(n^2 T) cost from the hot loop).
    """
    N = C.shape[0]
    out = []
    for n in sizes:
        if n > N:
            continue
        prs = []
        for _ in range(ndraw):
            idx = rng.choice(N, n, replace=False)
            ev = np.clip(np.linalg.eigvalsh(C[np.ix_(idx, idx)])[::-1], 0, None)
            prs.append(participation_ratio(ev))
        out.append((n, float(np.mean(prs)), float(np.std(prs))))
    return out


def beta_from_curve(curve):
    """Upper-range dlog(PR)/dlog(N') slope -- identical fit logic to spectral_test.main."""
    cn = np.array([c[0] for c in curve], float)
    cp = np.array([c[1] for c in curve], float)
    upper = cn >= max(20, cn.max() // 3)
    if upper.sum() < 3:
        upper = cn >= cn.min()  # fall back to all points for small N
    return float(np.polyfit(np.log10(cn[upper]), np.log10(cp[upper]), 1)[0])


# --- corridor quantities -----------------------------------------------------------
def rho_bar(X):
    """Mean off-diagonal of the outcome correlation matrix (the direct corridor var)."""
    N = X.shape[0]
    Z = (X - X.mean(1, keepdims=True)) / X.std(1, keepdims=True)
    C = (Z @ Z.T) / X.shape[1]
    off = C[~np.eye(N, dtype=bool)]
    return float(off.mean())


def potential_S(k, rho):
    """Measured potential S(k,rho) = -ln(1+rho(k-1)) - (k-1)ln(1-rho)."""
    if rho >= 1.0 - 1e-12:
        return float("inf")
    return float(-np.log(1 + rho * (k - 1)) - (k - 1) * np.log(1 - rho))


def curve_C3(k, rho):
    """Parameter-free rigidity-pole leg: -(k-1)ln(1-rho)."""
    if rho >= 1.0 - 1e-12:
        return float("inf")
    return float(-(k - 1) * np.log(1 - rho))


def sizes_for(N):
    grid = [8, 10, 12, 15, 20, 25, 30, 40, 53, 64, 80, 100]
    s = [g for g in grid if g <= N]
    if N not in s:
        s.append(N)
    return sorted(set(s))


def analyze(shots, rng, ndraw=25):
    """shots: (S, N) +/-1. Returns the full estimator readout dict."""
    X = shots.T.astype(float)                      # (N, S) = UNITS x OBSERVATIONS
    N, T = X.shape
    ev, _, _ = corr_eig(X)
    pr = participation_ratio(ev)
    # eff-rank vs phase-randomized surrogate (destroys cross-qubit structure)
    Xs = phase_randomize(X, rng)
    evs, *_ = corr_eig(Xs)
    eff_rank = int((ev > evs.max()).sum())
    edge = mp_edge(N, T)
    eff_rank_mp = int((ev > edge).sum())
    rb = rho_bar(X)
    sizes = sizes_for(N)
    curve = subsample_pr(corr_matrix(X), sizes, rng, ndraw=ndraw)
    beta = beta_from_curve(curve)
    kish = N / (1 + rb * (N - 1)) if rb > 0 else float(N)
    return dict(N=N, T=T, PR=float(pr), k_eff_pr=float(pr), k_eff_kish=float(kish),
                eff_rank=eff_rank, eff_rank_mp=eff_rank_mp, rho_bar=rb,
                beta=beta, S=potential_S(pr, rb), curve=curve,
                top_eigs=[float(x) for x in ev[:6]])


def beta_bootstrap(shots, rng, B=25, ndraw=8):
    """Beta CI by resampling shots (observations) with replacement. Reduced ndraw for cost."""
    S, N = shots.shape
    betas = []
    for _ in range(B):
        idx = rng.integers(0, S, size=S)
        X = shots[idx].T.astype(float)
        curve = subsample_pr(corr_matrix(X), sizes_for(N), rng, ndraw=ndraw)
        betas.append(beta_from_curve(curve))
    betas = np.array(betas)
    return float(np.percentile(betas, 2.5)), float(np.percentile(betas, 97.5)), float(betas.std())


def classify(beta_lo, beta_hi, rho, eff_rank, N):
    """Map (beta CI, rho_bar) to a corridor verdict, per SPEC §5 branches."""
    beta_mid = 0.5 * (beta_lo + beta_hi)
    # branch: saturation vs power-law vs noise/extensive
    if beta_hi < 0.3:
        branch = "SATURATION"
    elif beta_lo > 0.3 and beta_hi < 0.9:
        branch = "POWER-LAW"
    elif beta_lo > 0.75:
        branch = "NOISE/EXTENSIVE"
    else:
        branch = "AMBIGUOUS"
    # pole from rho_bar
    if rho > 0.85:
        return "RIGIDITY", branch
    if branch == "SATURATION":
        return "CORRIDOR", branch
    if branch == "POWER-LAW":
        return "CRITICAL", branch
    if branch in ("NOISE/EXTENSIVE",) or rho < 0.05:
        return "CHAOS", branch
    return "AMBIGUOUS", branch


# ---------------------------------------------------------------------------------
def make_classes(S, N, rng):
    """The declared calibration classes at scale (S shots, N qubits)."""
    return {
        "product (Z)":       ss.product_shots(S, N, rng),
        "GHZ (Z)":           ss.ghz_z_shots(S, N, rng),
        "GHZ (X, parity)":   ss.ghz_x_shots(S, N, rng),
        "low-rank r=3":      ss.low_rank_shots(S, N, rng, r=3),
        "power-law a=1.0":   ss.powerlaw_shots(S, N, rng, alpha=1.0),
        "power-law a=0.6":   ss.powerlaw_shots(S, N, rng, alpha=0.6),
        "shot-noise":        ss.shot_noise_shots(S, N, rng),
    }


def run_grid():
    cells = [("Sycamore-like", 53, int(1e4)),
             ("Sycamore-like", 53, int(1e5)),
             ("Sycamore-like", 53, int(5e5)),
             ("IBM-like",      20, int(1e5))]
    results = []
    for label, N, S in cells:
        print(f"\n=== {label}: N={N}, S={S:,} ===")
        rng = np.random.default_rng(SEED + N * 7 + S)  # deterministic per cell
        classes = make_classes(S, N, rng)
        for name, shots in classes.items():
            a = analyze(shots, rng)
            blo, bhi, bstd = beta_bootstrap(shots, rng)
            verdict, branch = classify(blo, bhi, a["rho_bar"], a["eff_rank"], N)
            row = dict(cell=label, name=name, N=N, S=S,
                       beta=a["beta"], beta_lo=blo, beta_hi=bhi, beta_std=bstd,
                       PR=a["PR"], k_eff_kish=a["k_eff_kish"], eff_rank=a["eff_rank"],
                       rho_bar=a["rho_bar"], S_potential=a["S"],
                       branch=branch, verdict=verdict, top_eigs=a["top_eigs"])
            results.append(row)
            sfmt = "inf" if not np.isfinite(a["S"]) else f"{a['S']:6.2f}"
            print(f"  {name:18s} beta={a['beta']:+.3f} [{blo:+.3f},{bhi:+.3f}]  "
                  f"PR={a['PR']:6.2f}  effr={a['eff_rank']:2d}  rho={a['rho_bar']:+.3f}  "
                  f"S={sfmt}  -> {verdict}")
    return results


def run_ramp(N=53, S=int(1e5)):
    """C3 leg: depolarized-GHZ maintenance ramp. Sweep p, track S vs -(k-1)ln(1-rho)."""
    print(f"\n=== C3 ramp (depolarized GHZ): N={N}, S={S:,} ===")
    rng = np.random.default_rng(SEED + 999)
    ps = np.array([0.02, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.55, 0.70, 0.85, 1.00])
    traj = []
    for p in ps:
        shots = ss.ghz_depolarized_shots(S, N, rng, float(p))
        a = analyze(shots, rng, ndraw=15)
        k = a["PR"]
        rb = a["rho_bar"]
        S_meas = potential_S(k, rb)
        S_c3 = curve_C3(k, rb)
        dev = (S_meas - S_c3) if np.isfinite(S_meas) else float("nan")
        traj.append(dict(p=float(p), rho_bar=rb, k_eff=float(k), eff_rank=a["eff_rank"],
                         S_measured=S_meas, S_c3=S_c3, deviation=dev))
        sm = "inf" if not np.isfinite(S_meas) else f"{S_meas:7.3f}"
        sc = "inf" if not np.isfinite(S_c3) else f"{S_c3:7.3f}"
        print(f"  p={p:4.2f}  rho={rb:+.4f}  k_eff={k:6.3f}  "
              f"S_meas={sm}  S_C3={sc}  dev={dev:+.4f}")
    return traj


def main():
    grid = run_grid()
    ramp = run_ramp()
    out = dict(seed=SEED, grid=grid, ramp=ramp)
    with open(os.path.join(HERE, "calibration_results.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("\nwrote calibration_results.json")
    try:
        import make_figures  # noqa: F401
        make_figures.build(out, HERE)
        print("wrote figures")
    except Exception as e:  # matplotlib missing or plotting error -> skip PNGs
        print(f"(figures skipped: {e})")


if __name__ == "__main__":
    main()
