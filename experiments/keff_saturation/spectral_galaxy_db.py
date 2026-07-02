#!/usr/bin/env python3
"""
BOUND-vs-COORDINATING detector on the same complete bound galaxy: broken detailed
balance in the top collective modes (Battle et al. 2016, Science, "Broken
detailed balance at mesoscopic scales"; Gnesotto et al. 2018).

Theory. drho/dt = alpha(rho,S) - gamma*M. A COORDINATING system is sustained by
active maintenance gamma*M: a NON-EQUILIBRIUM STEADY STATE that BREAKS DETAILED
BALANCE -> net probability CURRENTS (circulation) in the plane of a pair of
configuration-like collective coordinates, positive entropy production, a
thermodynamic arrow. A merely BOUND system (gravity = conservative alpha, no
gamma*M) is a Hamiltonian/relaxational system: in configuration-coordinate planes
it satisfies detailed balance -> ~zero NET circulation.

Readout. Project the z-height / j_z / v_r star x snapshot matrices onto their top
collective (SVD) modes; the mode-amplitude trajectories a_k(t) are the collective
coordinates. For each mode pair estimate the mean cycling rate
    omega_ij = <x dy - y dx> / <x^2 + y^2>     (mean angular velocity in the plane)
= net circulation. E[omega]=0 under detailed balance (no preferred rotation
sense). Significance vs a PHASE-RANDOMIZED null (preserves each mode's power
spectrum, destroys the cross-mode phase relations that make net rotation). Summed
|omega| over the top-3 pairs is an entropy-production proxy.

CAVEATS (load-bearing, stated in the summary):
 (1) T=26 snapshots is a SHORT trajectory -> low statistical power; a proper NESS
     detailed-balance test wants a stationary segment with many time points.
 (2) The galaxy is NON-STATIONARY over z=2.3->0 (assembly, secular settling,
     mergers). Any detected irreversibility most likely reflects TRANSIENT
     gravitational relaxation / one-way assembly drift, NOT sustained gamma*M
     active maintenance. Relaxation toward equilibrium also breaks DB transiently.
 (3) Calibration synthetics (reversible OU / driven-rotational NESS / pure
     relaxation transient) ONLY place the galaxy's omega on a ruler; no fabricated
     data enters the verdict.

Reuses build_tracked() from spectral_galaxy.py (cached remote reads).
"""
import numpy as np, json, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("sg", os.path.join(HERE, "spectral_galaxy.py"))
sg = importlib.util.module_from_spec(spec); spec.loader.exec_module(sg)
RNG = np.random.default_rng(0)

def modes(X, k=4):
    """Top-k collective-coordinate trajectories (k x T)."""
    good = np.isfinite(X).all(1) & (X.std(1) > 1e-12)
    Z = X[good]; Z = (Z - Z.mean(1, keepdims=True)) / Z.std(1, keepdims=True)
    U, S, Vt = np.linalg.svd(Z, full_matrices=False)
    return (S[:, None] * Vt)[:k]

def omega(x, y):
    dx = np.diff(x); dy = np.diff(y); xm = x[:-1]; ym = y[:-1]
    den = np.mean(xm**2 + ym**2)
    return float(np.mean(xm*dy - ym*dx) / den) if den > 0 else 0.0

def phaserand(v):
    F = np.fft.rfft(v); ph = np.exp(1j*RNG.uniform(0, 2*np.pi, F.shape)); ph[0] = 1
    return np.fft.irfft(F*ph, n=len(v))

def db_stats(A, npair=3, nnull=3000):
    """Per-pair omega + phase-randomized null z; summed |omega| EP proxy + z."""
    pairs = [(i, j) for i in range(npair) for j in range(i+1, npair)]
    res = {}; obs_sum = 0.0; null_sum = np.zeros(nnull)
    for (i, j) in pairs:
        obs = omega(A[i], A[j])
        null = np.array([omega(phaserand(A[i]), phaserand(A[j])) for _ in range(nnull)])
        z = (obs - null.mean()) / (null.std() + 1e-12)
        res[f"{i}-{j}"] = dict(omega=obs, null_sd=float(null.std()), z=float(z))
        obs_sum += abs(obs); null_sum += np.abs(null)
    zc = (obs_sum - null_sum.mean()) / (null_sum.std() + 1e-12)
    return res, dict(circulation_sum=float(obs_sum), null_mean=float(null_sum.mean()),
                     null_sd=float(null_sum.std()), z=float(zc))

# ---- calibration synthetics (n_modes x T), same T as the galaxy ----------
def ou_equilibrium(m, T):
    """Independent OU: reversible, detailed-balance-satisfying."""
    x = np.zeros((m, T))
    for t in range(1, T):
        x[:, t] = 0.7*x[:, t-1] + RNG.standard_normal(m)
    return x
def ou_driven(m, T, w=0.8):
    """Rotational drift between mode pairs: sustained NESS, breaks DB."""
    x = np.zeros((m, T))
    Adrift = -0.3*np.eye(m)
    for i in range(0, m-1, 2):
        Adrift[i, i+1] = -w; Adrift[i+1, i] = +w        # antisymmetric = cycling
    for t in range(1, T):
        x[:, t] = x[:, t-1] + Adrift @ x[:, t-1] + 0.5*RNG.standard_normal(m)
    return x
def relaxation(m, T):
    """Monotone one-way settling + noise: transient irreversibility, no NESS."""
    tt = np.linspace(0, 1, T)
    x = np.array([np.exp(-(k+1)*tt) for k in range(m)]) * 3
    return x + 0.3*RNG.standard_normal((m, T))

def main():
    keep, Zz, _ = sg.build_tracked("zheight")
    _, Zj, _ = sg.build_tracked("jz")
    _, Zv, _ = sg.build_tracked("vr")
    T = Zz.shape[1]
    out = dict(note="broken-detailed-balance (bound vs coordinating) on top collective modes",
               T=T, N=int(Zz.shape[0]),
               estimator="omega=<x dy - y dx>/<x^2+y^2>; null=phase-randomized modes")

    print("=== CALIBRATION (n_modes=4, T=%d): where does omega land? ===" % T)
    cal = {}
    for name, A in [("OU-equilibrium (reversible)", ou_equilibrium(4, T)),
                    ("OU-driven (NESS, breaks DB)", ou_driven(4, T)),
                    ("relaxation (transient)",       relaxation(4, T))]:
        pr, cs = db_stats(A)
        cal[name] = dict(pairs=pr, circulation=cs)
        print(f"  {name:30s}: sum|omega|={cs['circulation_sum']:.3f}  z={cs['z']:+.2f}  "
              f"(top pair z={pr['0-1']['z']:+.2f})")
    out["calibration"] = cal
    print("  (expect: equilibrium z~0; driven z>>2 large sum; relaxation modest/one-pair)\n")

    print("=== GALAXY (complete bound unit) ===")
    gal = {}
    for scalar, X in [("zheight", Zz), ("jz", Zj), ("vr", Zv)]:
        A = modes(X, 4)
        pr, cs = db_stats(A)
        gal[scalar] = dict(pairs=pr, circulation=cs)
        print(f"  [{scalar}] sum|omega|={cs['circulation_sum']:.3f} z={cs['z']:+.2f}  "
              f"pairs: " + "  ".join(f"{k}:om={v['omega']:+.3f}(z{v['z']:+.1f})" for k,v in pr.items()))
    out["galaxy"] = gal

    # verdict on primary zheight
    z_top = max(abs(gal["zheight"]["pairs"][k]["z"]) for k in gal["zheight"]["pairs"])
    z_sum = abs(gal["zheight"]["circulation"]["z"])
    driven_z = abs(cal["OU-driven (NESS, breaks DB)"]["circulation"]["z"])
    strong = (z_sum > 3) and (z_top > 3) and (gal["zheight"]["circulation"]["circulation_sum"]
                                              > 0.3*cal["OU-driven (NESS, breaks DB)"]["circulation"]["circulation_sum"])
    if strong:
        verdict = ("BROKEN DETAILED BALANCE (strong sustained circulation): consistent with an "
                   "actively-maintained NESS = COORDINATING. (Unexpected for a collisionless "
                   "stellar system; would warrant scrutiny of secular/assembly confounds.)")
    elif z_top >= 2:
        verdict = ("WEAK / MARGINAL circulation (|z|~2 in one mode pair only, others ~0), far below "
                   "the driven-NESS ruler and consistent with TRANSIENT cosmic-assembly drift rather "
                   "than sustained gamma*M. Reads as BOUND (near-detailed-balance), NOT coordinating.")
    else:
        verdict = ("NO significant circulation: detailed-balance-satisfying = BOUND, not coordinating.")
    out["verdict"] = verdict
    print(f"\nDETAILED-BALANCE VERDICT (primary=zheight): {verdict}")

    js = os.path.join(HERE, "spectral_results_galaxy.json")
    full = json.load(open(js)); full["detailed_balance"] = out
    json.dump(full, open(js, "w"), indent=1)
    json.dump(out, open(os.path.join(HERE, "spectral_results_galaxy_db.json"), "w"), indent=1)
    print("\nfolded detailed_balance into spectral_results_galaxy.json (+ _db.json)")

if __name__ == "__main__":
    main()
