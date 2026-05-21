"""
pp_angular — the tt-bar spin-density matrix as a corridor shape observable.
============================================================================

Third particle-physics shape-observable test (after E4 decay branching
fractions and pp_cp CP-violation structure). See PREREGISTRATION.md, committed
BEFORE this script produced any result.

The shape observable: the tt-bar two-particle spin state is a 4x4 density
matrix R (one qubit per top, helicity basis {r,k,n}). Its four eigenvalues sum
to 1 and are non-negative -- a probability distribution on the 4-simplex. The
participation ratio of that eigenvalue spectrum is the matrix shape observable.

  k_eff = 1/sum(lambda_i^2),  rho = (N/k_eff - 1)/(N-1),  N = 4.

rho -> 1: one eigenvalue dominates (near-pure state, rigidity).
rho -> 0: four equal eigenvalues, R prop. I (maximally mixed, chaos).
corridor: a bounded interior band -- pre-registered A3+ ref [0.17, 0.35].

Data: CMS 2024, HEPData 153301, "full matrix inclusive from m(tt)" (Fig 17).
15 measured spin-density-matrix coefficients with stat+syst errors. Real data.
Honest prior: NULL. The tt-bar spin state is NOT a coordinated rung (single-
shot, ~1e-25 s, no maintenance dynamics gamma*M(t)) -- PREREGISTRATION sec 0.
"""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "cms_fullmatrix_inclusive_mtt.json")
RNG = np.random.default_rng(20260521)
N_MC = 20000

# Pauli matrices, index order I, X(=r), Y(=k... see basis note), Z(=n).
# We label the three spin axes r, k, n and use one Pauli per axis. The basis
# choice does not affect eigenvalues of R (basis-independent), so any fixed
# assignment sigma_r, sigma_k, sigma_n to {X,Y,Z} gives identical lambda.
sx = np.array([[0, 1], [1, 0]], complex)
sy = np.array([[0, -1j], [1j, 0]], complex)
sz = np.array([[1, 0], [0, -1]], complex)
I2 = np.eye(2, dtype=complex)
SIG = {"r": sx, "k": sy, "n": sz}            # fixed axis -> Pauli assignment


def kron(a, b):
    return np.kron(a, b)


def load_coeffs():
    """Return {name: (value, sigma)} for the 15 measured coefficients,
    sigma = quadrature sum of stat and syst (errors treated independent --
    a stated approximation, full covariance not in the table)."""
    with open(DATA) as f:
        doc = json.load(f)
    out = {}
    pred = {}
    for entry in doc["values"]:
        # x label like "$C_{rr}$ for inclusive measurement"
        raw = entry["x"][0]["value"]
        name = raw.split(" for ")[0].strip("$").replace("\\", "")
        meas = None
        sig_terms = []
        powheg = None
        for y in entry["y"]:
            g = y.get("group")
            if g == 0:                        # measured
                meas = float(y["value"])
                for e in y.get("errors", []):
                    lab = e.get("label", "")
                    if lab in ("stat", "syst"):
                        sig_terms.append(float(e["symerror"]))
            elif g == 1:                      # Powheg+P8 SM prediction
                powheg = float(y["value"])
        sigma = float(np.sqrt(np.sum(np.square(sig_terms))))
        out[name] = (meas, sigma)
        pred[name] = powheg
    return out, pred


def build_R(c):
    """Assemble the 4x4 spin-density matrix from a coefficient dict c.
    Keys: P_{r,n,k}, bar{P}_{r,n,k}, C_{rr,nn,kk}, C_{nr,rk,nk}^{+/-}."""
    axes = ["r", "k", "n"]
    R = kron(I2, I2).astype(complex)
    # net polarisations: top (B+) and antitop (B-)
    for ax in axes:
        bp = c[f"P_{{{ax}}}"]
        bm = c[f"bar{{P}}_{{{ax}}}"]
        R += bp * kron(SIG[ax], I2)
        R += bm * kron(I2, SIG[ax])
    # spin-correlation matrix C_ij
    C = {}
    for ax in axes:
        C[(ax, ax)] = c[f"C_{{{ax}{ax}}}"]
    # off-diagonal pairs from symmetric/antisymmetric combos
    for (i, j) in [("n", "r"), ("r", "k"), ("n", "k")]:
        cp = c[f"C_{{{i}{j}}}^{{+}}"]
        cm = c[f"C_{{{i}{j}}}^{{-}}"]
        C[(i, j)] = 0.5 * (cp + cm)
        C[(j, i)] = 0.5 * (cp - cm)
    for (i, j), val in C.items():
        R += val * kron(SIG[i], SIG[j])
    R = R / 4.0
    R = 0.5 * (R + R.conj().T)               # symmetrise (Hermitian)
    return R, C


def rho_from_eigs(lam):
    """Kish rho of an eigenvalue spectrum (clipped non-negative, renormalised)."""
    lam = np.clip(np.asarray(lam, float), 0.0, None)
    s = lam.sum()
    if s <= 0:
        return np.nan, np.nan
    p = lam / s
    N = len(p)
    k_eff = 1.0 / np.sum(p ** 2)
    rho = (N / k_eff - 1.0) / (N - 1.0)
    return k_eff, rho


def main():
    coeffs, pred = load_coeffs()
    print("=" * 78)
    print("pp_angular — tt-bar spin-density matrix corridor test")
    print("CMS 2024, HEPData 153301, full matrix inclusive from m(tt)")
    print("=" * 78)

    cval = {k: v[0] for k, v in coeffs.items()}
    R0, C0 = build_R(cval)
    lam0 = np.sort(np.linalg.eigvalsh(R0))[::-1]
    keff0, rho0 = rho_from_eigs(lam0)

    print("\n[central value]")
    print(f"  Tr R              = {np.trace(R0).real:.6f}  (must be 1)")
    print(f"  eigenvalues       = "
          + ", ".join(f"{x:.5f}" for x in lam0))
    print(f"  min eigenvalue    = {lam0.min():.5f}")
    print(f"  k_eff (of 4)      = {keff0:.4f}")
    print(f"  rho               = {rho0:.4f}")
    trC = C0[("r", "r")] + C0[("k", "k")] + C0[("n", "n")]
    print(f"  tr[C]             = {trC:.4f}   (-tr[C]-1 = {-trC-1:.4f}; "
          f"table 'c' = {cval.get('c', float('nan')):.4f})")

    # physicality: how negative, relative to MC error spread (computed below)
    neg = lam0[lam0 < 0]
    if len(neg):
        print(f"  NOTE: {len(neg)} eigenvalue(s) negative at central value "
              f"(min {neg.min():.5f}) -- physical-positivity check vs MC below")

    # ---- MC error propagation ----
    rhos, keffs, minlam = [], [], []
    for _ in range(N_MC):
        cdraw = {k: RNG.normal(v[0], v[1]) if v[1] > 0 else v[0]
                 for k, v in coeffs.items()}
        Rm, _ = build_R(cdraw)
        lam = np.sort(np.linalg.eigvalsh(Rm))[::-1]
        minlam.append(lam.min())
        ke, rh = rho_from_eigs(lam)
        keffs.append(ke)
        rhos.append(rh)
    rhos = np.array(rhos)
    keffs = np.array(keffs)
    minlam = np.array(minlam)
    p16, p50, p84 = np.percentile(rhos, [16, 50, 84])
    width = p84 - p16

    print(f"\n[MC error propagation, {N_MC} draws, stat+syst in quadrature]")
    print(f"  rho   median {p50:.4f}   16-84 [{p16:.4f}, {p84:.4f}]   "
          f"width {width:.4f}")
    print(f"  k_eff median {np.median(keffs):.4f}   "
          f"16-84 [{np.percentile(keffs,16):.4f}, "
          f"{np.percentile(keffs,84):.4f}]")
    print(f"  min eigenvalue: median {np.median(minlam):.5f}   "
          f"16-84 [{np.percentile(minlam,16):.5f}, "
          f"{np.percentile(minlam,84):.5f}]")
    frac_neg = float(np.mean(minlam < 0))
    print(f"  fraction of draws with a negative eigenvalue: {frac_neg:.3f}")

    # ---- SM-prediction cross-check ----
    if all(pred.get(k) is not None for k in coeffs):
        Rp, _ = build_R(pred)
        lamp = np.sort(np.linalg.eigvalsh(Rp))[::-1]
        keffp, rhop = rho_from_eigs(lamp)
        print(f"\n[SM Powheg+P8 prediction]  eigs = "
              + ", ".join(f"{x:.5f}" for x in lamp))
        print(f"  rho_SM = {rhop:.4f}   (vs measured rho {rho0:.4f}; "
              f"diff {abs(rhop-rho0):.4f})")
    else:
        rhop = None
        print("\n[SM prediction] not all coefficients have a Powheg+P8 value")

    # ---- naive 15-vector contrast (NOT the matrix shape observable) ----
    vec = np.array([abs(v[0]) for v in coeffs.values()])
    pv = vec ** 2 / np.sum(vec ** 2)
    Nv = len(pv)
    kv = 1.0 / np.sum(pv ** 2)
    rv = (Nv / kv - 1.0) / (Nv - 1.0)
    print(f"\n[contrast] naive |coeff|^2 of 15-vector (NOT a matrix shape): "
          f"rho = {rv:.4f}")

    # ---- verdict against the pre-registered bar ----
    print("\n" + "=" * 78)
    print("VERDICT (against PREREGISTRATION.md section 3)")
    print("=" * 78)
    CORR_LO, CORR_HI = 0.17, 0.35
    in_band = (p16 >= CORR_LO) and (p84 <= CORR_HI)
    pole_rig = p50 > 0.55
    pole_chaos = p50 < 0.12
    too_wide = width > 0.18
    sm_same = (rhop is not None) and (abs(rhop - rho0) < (p84 - p16))
    big_neg = np.median(minlam) < -0.02

    if big_neg:
        print("  CONSTRUCTION FAILURE: assembled R has a large negative")
        print(f"  eigenvalue (median min {np.median(minlam):.4f}); not a")
        print("  physical density matrix. No verdict forced.")
    elif pole_rig:
        print(f"  NULL -- pole pile-up (rigidity): rho median {p50:.3f} > 0.55.")
        print("  R is a near-pure two-qubit state.")
    elif pole_chaos:
        print(f"  NULL -- pole pile-up (chaos): rho median {p50:.3f} < 0.12.")
        print("  R is near maximally mixed.")
    elif in_band and not too_wide:
        print(f"  rho 16-84 interval [{p16:.3f},{p84:.3f}] lies inside the A3+")
        print(f"  reference corridor [0.17, 0.35].")
        if sm_same:
            print("  BUT rho_SM equals rho_measured within error: the observable")
            print("  carries nothing the SM Lagrangian did not already fix.")
            print("  Reported as NULL -- uninformative (PREREG sec 3).")
        else:
            print("  Numerically inside the corridor band. PER PREREG sec 0 & 4")
            print("  this is a COINCIDENCE of the descriptive statistic, NOT")
            print("  framework support: the tt-bar spin state is not a")
            print("  coordinated rung (single-shot, ~1e-25 s, no gamma*M(t)).")
    else:
        print(f"  NULL -- rho median {p50:.3f}, 16-84 [{p16:.3f},{p84:.3f}]")
        print(f"  is OUTSIDE the A3+ corridor band [0.17, 0.35].")
        print("  A value, but not a corridor occupancy.")
    print()
    print("  Prior was NULL; the tt-bar spin-density matrix is not a")
    print("  coordinated rung in the framework's sense (PREREG sec 0).")


if __name__ == "__main__":
    main()
