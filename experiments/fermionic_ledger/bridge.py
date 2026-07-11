"""
bridge.py — S4, the instrument relation. Reproduces the entanglement-bridge
design (experiments/entanglement_ledger) on FREE-FERMION systems.

QUESTION. Across a free-fermion phase transition (Kitaev topological transition
mu=2t; XY criticality), does the CLASSICAL instrument S = -ln det C of measured
single-site observables track the FERMIONIC-NATIVE ledger functionals?
  fermionic-native (basis-free):
     S_half  = entanglement entropy S_F of the half chain (reduced covariance)
     L_half  = F2 log-det potential -sum ln(1-nu^2) on the half-chain covariance
     I_reg   = F1 multi-information within a contiguous region
  classical instrument (basis-dependent, the point):
     S_cl(theta) = -ln det C, C = corr matrix of single-site axis observables
                   O_i = cos(theta) Z_i + sin(theta) X_i  (Z = occupation basis).
Report Spearman across the sweep; Z (order-parameter/occupation) vs X (conjugate)
is the known blindness control. The topological edge mode (nonlocal parity) is a
predicted blind spot for the LOCAL classical instrument.
"""

import json
import numpy as np
from scipy.stats import spearmanr
import scipy.sparse as sp
from fermionic_core import (
    S_F_from_nu, logdet_potential_from_nu, classical_S_from_corr,
    multi_information_majorana, nu_from_majorana,
)
from systems import (
    annihilation_ops, majorana_covariance, entanglement_entropy,
    H_kitaev, H_xy, ground_state,
)

# single-site Pauli on JW qubit j (basis |0>=unocc,|1>=occ; Z=+1 on |0>)
_Z1 = np.array([[1, 0], [0, -1]], dtype=complex)
_X1 = np.array([[0, 1], [1, 0]], dtype=complex)
_I1 = np.eye(2, dtype=complex)


def site_op(mat, j, N):
    ops = [sp.identity(2, format="csr", dtype=complex)] * N
    ops[j] = sp.csr_matrix(mat)
    out = ops[0]
    for o in ops[1:]:
        out = sp.kron(out, o, format="csr")
    return out


def classical_S_axis(psi, N, theta, drop_tol=1e-9):
    """S = -ln det C of single-site observables O_i = cos th Z_i + sin th X_i."""
    O = [site_op(np.cos(theta) * _Z1 + np.sin(theta) * _X1, i, N) for i in range(N)]
    means = np.array([np.vdot(psi, Oi @ psi).real for Oi in O])
    Opsi = [Oi @ psi for Oi in O]
    M2 = np.array([[np.vdot(Opsi[i], Opsi[j]) for j in range(N)] for i in range(N)]).real
    cov = M2 - np.outer(means, means)
    var = np.diag(cov).copy()
    keep = var > drop_tol
    if keep.sum() < 2:
        return 0.0
    cov = cov[np.ix_(keep, keep)]
    d = np.sqrt(np.diag(cov))
    C = cov / np.outer(d, d)
    return classical_S_from_corr(C)


def sweep(system, params, N=10, n_theta=19, region=None):
    """Return per-parameter fermionic-native and classical quantities."""
    if region is None:
        region = list(range(N // 2))
    a_ops = annihilation_ops(N)
    thetas = np.linspace(0, np.pi / 2, n_theta)
    rows = []
    for p in params:
        if system == "kitaev":
            H = H_kitaev(N, mu=p, t=1.0, Delta=1.0)
        elif system == "xy_field":
            H = H_xy(N, gamma=0.5, hz=p)          # transverse-field-Ising-like
        elif system == "xx_hop":
            H = H_xy(N, gamma=0.0, hz=p)          # XX in a field (Fermi-sea filling)
        else:
            raise ValueError(system)
        _, psi = ground_state(H)
        M = majorana_covariance(psi, a_ops)
        # fermionic-native
        S_half, nuA = entanglement_entropy(M, region)
        L_half = logdet_potential_from_nu(nuA)
        # region multi-information from the region sub-covariance
        idx = []
        for j in region:
            idx += [2 * j, 2 * j + 1]
        MA = M[np.ix_(idx, idx)]
        I_reg, _, _ = multi_information_majorana(MA)
        # classical instrument, per axis
        Scl = np.array([classical_S_axis(psi, N, th) for th in thetas])
        Scl_finite = np.where(np.isfinite(Scl), Scl, np.nan)
        rows.append({
            "p": float(p),
            "S_half": float(S_half),
            "L_half": float(L_half if np.isfinite(L_half) else 1e6),
            "I_reg": float(I_reg),
            "Scl_Z": float(Scl[0]),                        # theta=0 occupation basis
            "Scl_X": float(Scl[-1]),                       # theta=pi/2 conjugate
            "Scl_best": float(np.nanmax(Scl_finite)),
        })
    return rows


def spearman_report(rows):
    def col(k):
        return np.array([r[k] for r in rows], dtype=float)
    out = {}
    S_half, L_half, I_reg = col("S_half"), col("L_half"), col("I_reg")
    for clname in ("Scl_Z", "Scl_X", "Scl_best"):
        cl = col(clname)
        mask = np.isfinite(cl) & np.isfinite(S_half)
        if mask.sum() < 4:
            continue
        out[clname] = {
            "vs_S_half": float(spearmanr(cl[mask], S_half[mask]).statistic),
            "vs_L_half": float(spearmanr(cl[mask], L_half[mask]).statistic),
            "vs_I_reg": float(spearmanr(cl[mask], I_reg[mask]).statistic),
        }
    # cross-check: do the two fermionic functionals agree in rank?
    out["fermionic_internal"] = {
        "S_half_vs_L_half": float(spearmanr(S_half, L_half).statistic),
        "S_half_vs_I_reg": float(spearmanr(S_half, I_reg).statistic),
    }
    return out


if __name__ == "__main__":
    OUT = {}
    N = 10
    print(f"== S4 bridge, N={N} ==")

    # Kitaev topological transition (mu: 0 -> 4, transition at mu=2)
    mus = np.linspace(0.05, 3.95, 22)
    rk = sweep("kitaev", mus, N=N)
    OUT["kitaev"] = {"rows": rk, "spearman": spearman_report(rk)}
    print("\nKitaev (topological transition mu=2):")
    for k, v in OUT["kitaev"]["spearman"].items():
        print(f"  {k}: {v}")

    # XY in transverse field (Ising criticality hz=1)
    hs = np.linspace(0.05, 2.5, 22)
    rxy = sweep("xy_field", hs, N=N)
    OUT["xy_field"] = {"rows": rxy, "spearman": spearman_report(rxy)}
    print("\nXY-field (Ising criticality hz=1):")
    for k, v in OUT["xy_field"]["spearman"].items():
        print(f"  {k}: {v}")

    with open("bridge_results.json", "w") as f:
        json.dump(OUT, f, indent=2, default=float)
    print("\nwrote bridge_results.json")
