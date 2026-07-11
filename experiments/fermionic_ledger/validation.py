"""
validation.py — OUT-OF-SEARCH validation. These systems were untouched while the
functional (F1 fermionic multi-information, with the exclusion deformation) was
being fixed on Kitaev/XY/uniform-family. A "found" claim must survive here.

Validation set:
  (V1) SSH chain (dimerized hopping, number-conserving) — two-pole + bridge across
       the topological transition v<->w. Uses the exact free-fermion correlation
       matrix (single-particle diagonalization; scales to large N).
  (V2) 2D free-fermion lattice patch — does the ledger structure survive in 2D?
  (V3) Hubbard chain via EXACT diagonalization (non-Gaussian ground state): apply
       the Gaussian functional to the TRUE covariance. Compare S_F(covariance) to
       the true von Neumann entropy S_vN and I_F(Gaussian) to true multi-info.
       Does the two-pole structure survive on a genuinely correlated (non-Gaussian)
       state, and how large is the non-Gaussian gap?

Free-fermion correlation-matrix method is validated against the ED covariance of
systems.py before use.
"""

import json
import numpy as np
from numpy.linalg import eigh, eigvalsh
from scipy.stats import spearmanr
from fermionic_core import (
    H_bin, LN2, S_F_from_nu, logdet_potential_from_nu, classical_S_from_corr,
)
from systems import (
    annihilation_ops, majorana_covariance, entanglement_entropy,
    H_xy, H_hubbard, ground_state,
)

OUT = {}


# ---------------------------------------------------------------------------
# free-fermion (number-conserving) correlation matrix from a hopping matrix
# ---------------------------------------------------------------------------
def G_from_hopping(hmat, filling=0.5):
    """Ground-state correlation matrix G_ij=<a_i^dag a_j> for H=sum h_ij a_i^dag a_j.
       Fill lowest Nf orbitals (Nf = round(filling*N))."""
    hmat = (hmat + hmat.conj().T) / 2.0
    w, U = eigh(hmat)
    N = hmat.shape[0]
    Nf = int(round(filling * N))
    occ = U[:, :Nf]                      # lowest Nf orbitals
    G = occ @ occ.conj().T
    return (G + G.conj().T) / 2.0


def entropy_from_G_region(G, region):
    """Entanglement entropy of a region from number-conserving G."""
    GA = G[np.ix_(region, region)]
    g = np.clip(eigvalsh((GA + GA.conj().T) / 2).real, 0, 1)
    return float(np.sum(H_bin(g))), g


def multi_information_from_G_region(G, region):
    """I_F within a region: sum_i H_bin(G_ii) - S_F(region)."""
    diag = np.real(np.diag(G))[region]
    marg = float(np.sum(H_bin(diag)))
    joint, _ = entropy_from_G_region(G, region)
    return marg - joint


def classical_S_number(G, region):
    """Classical instrument on LOCAL number observables n_i (string-free).
       Cov(n_i,n_j) = -|G_ij|^2 (i!=j, Wick), Var(n_i)=G_ii(1-G_ii)."""
    idx = np.array(region)
    Gr = G[np.ix_(idx, idx)]
    d = np.real(np.diag(Gr))
    var = d * (1 - d)
    keep = var > 1e-9
    if keep.sum() < 2:
        return 0.0
    Gr = Gr[np.ix_(keep, keep)]
    d = d[keep]
    var = var[keep]
    cov = -np.abs(Gr) ** 2
    np.fill_diagonal(cov, var)
    dd = np.sqrt(var)
    C = cov / np.outer(dd, dd)
    return classical_S_from_corr(C)


# ---------------------------------------------------------------------------
# V0: validate free-fermion route against ED covariance (XX chain)
# ---------------------------------------------------------------------------
def v0_validate_freefermion():
    N = 8
    # ED route
    a_ops = annihilation_ops(N)
    _, psi = ground_state(H_xy(N, gamma=0.0, hz=0.3))
    M = majorana_covariance(psi, a_ops)
    S_ed, _ = entanglement_entropy(M, list(range(N // 2)))
    # free-fermion route: XX hopping matrix, field hz shifts filling
    h = np.zeros((N, N))
    for j in range(N - 1):
        h[j, j + 1] = h[j + 1, j] = -1.0
    for j in range(N):
        h[j, j] = -0.3
    G = G_from_hopping(h, filling=None if False else 0.5)
    S_ff, _ = entropy_from_G_region(G, list(range(N // 2)))
    return {"S_ED": float(S_ed), "S_freefermion": float(S_ff),
            "err": float(abs(S_ed - S_ff))}


# ---------------------------------------------------------------------------
# V1: SSH chain
# ---------------------------------------------------------------------------
def ssh_hopping(Ncells, v, w):
    N = 2 * Ncells
    h = np.zeros((N, N))
    for j in range(N - 1):
        hop = v if (j % 2 == 0) else w
        h[j, j + 1] = h[j + 1, j] = -hop
    return h


def v1_ssh(Ncells=40):
    N = 2 * Ncells
    region = list(range(N // 2))
    ratios = np.linspace(0.2, 3.0, 24)   # w/v across transition at w=v
    S_half, I_reg, L_half, Scl = [], [], [], []
    for r in ratios:
        v, w = 1.0, r
        G = G_from_hopping(ssh_hopping(Ncells, v, w), filling=0.5)
        sh, gA = entropy_from_G_region(G, region)
        S_half.append(sh)
        I_reg.append(multi_information_from_G_region(G, region))
        L_half.append(min(logdet_potential_from_nu(np.abs(2 * gA - 1)), 1e6))
        Scl.append(classical_S_number(G, region))
    S_half, I_reg, Scl = map(np.array, (S_half, I_reg, Scl))
    return {
        "ratios": ratios.tolist(),
        "S_half": S_half.tolist(), "I_reg": I_reg.tolist(),
        "L_half": L_half, "Scl_number": Scl.tolist(),
        "I_F_bounded_max": float(np.max(I_reg)),
        "spearman_Scl_vs_Ihalf": float(spearmanr(Scl, I_reg).statistic),
        "spearman_Scl_vs_Shalf": float(spearmanr(Scl, S_half).statistic),
        "spearman_Shalf_vs_Ireg": float(spearmanr(S_half, I_reg).statistic),
    }


# ---------------------------------------------------------------------------
# V2: 2D free-fermion patch
# ---------------------------------------------------------------------------
def square_hopping(Lx, Ly, t=1.0, mu=0.0):
    N = Lx * Ly
    h = np.zeros((N, N))
    idx = lambda x, y: x * Ly + y
    for x in range(Lx):
        for y in range(Ly):
            i = idx(x, y)
            h[i, i] = -mu
            if x + 1 < Lx:
                j = idx(x + 1, y); h[i, j] = h[j, i] = -t
            if y + 1 < Ly:
                j = idx(x, y + 1); h[i, j] = h[j, i] = -t
    return h, idx


def v2_2d(Lx=6, Ly=6):
    mus = np.linspace(-3.5, 3.5, 21)   # sweep filling through the 2D band
    S_A, I_A, Scl = [], [], []
    h0, idx = square_hopping(Lx, Ly)
    # region A = a Lx/2 x Ly block (a contiguous patch)
    regionA = [idx(x, y) for x in range(Lx // 2) for y in range(Ly)]
    for mu in mus:
        h, _ = square_hopping(Lx, Ly, mu=mu)
        # fill all negative-energy orbitals (grand-canonical ground state)
        w, U = eigh(h)
        occ = U[:, w < 0]
        G = occ @ occ.conj().T
        G = (G + G.conj().T) / 2
        sA, gA = entropy_from_G_region(G, regionA)
        S_A.append(sA)
        I_A.append(multi_information_from_G_region(G, regionA))
        Scl.append(classical_S_number(G, regionA))
    S_A, I_A, Scl = map(np.array, (S_A, I_A, Scl))
    mask = np.isfinite(Scl) & np.isfinite(I_A)
    return {
        "mus": mus.tolist(), "S_A": S_A.tolist(), "I_A": I_A.tolist(),
        "Scl_number": Scl.tolist(),
        "I_F_bounded_max": float(np.max(I_A)),
        "spearman_Scl_vs_I_A": float(spearmanr(Scl[mask], I_A[mask]).statistic),
        "spearman_S_A_vs_I_A": float(spearmanr(S_A, I_A).statistic),
    }


# ---------------------------------------------------------------------------
# V3: Hubbard ED — the Gaussian functional on a NON-Gaussian state
# ---------------------------------------------------------------------------
def hubbard_covariance(psi, a_ops):
    """Full one-body correlation matrix G (with all modes) and F pairing (=0 for
       number-conserving Hubbard ground state at fixed particle number)."""
    N = len(a_ops)
    ad = [x.conj().T for x in a_ops]
    G = np.array([[np.vdot(psi, (ad[i] @ a_ops[j]) @ psi) for j in range(N)]
                  for i in range(N)])
    return (G + G.conj().T) / 2.0


def reduced_vn_entropy(psi, keep_modes, Nmodes):
    """True von Neumann entropy of a subset of fermionic modes (exact partial
       trace over the complementary modes). keep_modes given as mode indices;
       modes are qubits under JW so this is a qubit partial trace."""
    psi = psi.reshape([2] * Nmodes)
    keep = sorted(keep_modes)
    tr = [m for m in range(Nmodes) if m not in keep]
    perm = keep + tr
    psi2 = np.transpose(psi, perm).reshape(2 ** len(keep), 2 ** len(tr))
    rho = psi2 @ psi2.conj().T
    ev = np.clip(eigvalsh(rho).real, 1e-15, 1)
    return float(-np.sum(ev * np.log(ev)))


def v3_hubbard(Nsites=4):
    Nmodes = 2 * Nsites
    a_ops = annihilation_ops(Nmodes)
    region = list(range(Nmodes // 2))     # half the modes
    Us = np.linspace(0.0, 8.0, 17)
    rows = []
    for U in Us:
        H, _ = H_hubbard(Nsites, tt=1.0, U=U)
        _, psi = ground_state(H)
        G = hubbard_covariance(psi, a_ops)
        # Gaussian functional on the TRUE covariance
        S_F_gauss, gA = entropy_from_G_region(G, region)
        I_gauss = multi_information_from_G_region(G, region)
        # true (non-Gaussian) entropy of the same region
        S_vN_true = reduced_vn_entropy(psi, region, Nmodes)
        # true multi-information: sum_i S(mode i) - S(region)
        marg_true = sum(reduced_vn_entropy(psi, [m], Nmodes) for m in region)
        I_true = marg_true - S_vN_true
        rows.append({
            "U": float(U),
            "S_F_gaussian": float(S_F_gauss), "S_vN_true": float(S_vN_true),
            "I_gaussian": float(I_gauss), "I_true": float(I_true),
            "nongaussian_gap_S": float(S_F_gauss - S_vN_true),
        })
    Ig = np.array([r["I_gaussian"] for r in rows])
    It = np.array([r["I_true"] for r in rows])
    Sg = np.array([r["S_F_gaussian"] for r in rows])
    St = np.array([r["S_vN_true"] for r in rows])
    return {
        "rows": rows,
        "spearman_I_gauss_vs_I_true": float(spearmanr(Ig, It).statistic),
        "spearman_S_gauss_vs_S_true": float(spearmanr(Sg, St).statistic),
        "max_nongaussian_gap_S": float(np.max(Sg - St)),
        "I_gauss_bounded_max": float(np.max(Ig)),
        "note": "S_F(covariance) >= S_vN_true always (max-entropy Gaussian bound)",
    }


if __name__ == "__main__":
    print("== V0: free-fermion route vs ED covariance ==")
    OUT["V0_freefermion_check"] = v0_validate_freefermion()
    print(f"  S_ED={OUT['V0_freefermion_check']['S_ED']:.4f} "
          f"S_freefermion={OUT['V0_freefermion_check']['S_freefermion']:.4f} "
          f"err={OUT['V0_freefermion_check']['err']:.2e}")

    print("\n== V1: SSH chain (Ncells=40) ==")
    OUT["V1_ssh"] = v1_ssh()
    v1 = OUT["V1_ssh"]
    print(f"  I_F max (bounded)={v1['I_F_bounded_max']:.4f}  "
          f"Spearman Scl~I_reg={v1['spearman_Scl_vs_Ihalf']:.3f}  "
          f"Scl~S_half={v1['spearman_Scl_vs_Shalf']:.3f}  "
          f"S_half~I_reg={v1['spearman_Shalf_vs_Ireg']:.3f}")

    print("\n== V2: 2D free-fermion patch (6x6) ==")
    OUT["V2_2d"] = v2_2d()
    v2 = OUT["V2_2d"]
    print(f"  I_F max (bounded)={v2['I_F_bounded_max']:.4f}  "
          f"Spearman Scl~I_A={v2['spearman_Scl_vs_I_A']:.3f}  "
          f"S_A~I_A={v2['spearman_S_A_vs_I_A']:.3f}")

    print("\n== V3: Hubbard ED (Nsites=4, NON-Gaussian) ==")
    OUT["V3_hubbard"] = v3_hubbard()
    v3 = OUT["V3_hubbard"]
    print(f"  Spearman I_gauss~I_true={v3['spearman_I_gauss_vs_I_true']:.3f}  "
          f"S_gauss~S_true={v3['spearman_S_gauss_vs_S_true']:.3f}")
    print(f"  max non-Gaussian gap (S_F - S_vN)={v3['max_nongaussian_gap_S']:.4f}  "
          f"I_gauss bounded max={v3['I_gauss_bounded_max']:.4f}")

    with open("validation_results.json", "w") as f:
        json.dump(OUT, f, indent=2, default=float)
    print("\nwrote validation_results.json")
