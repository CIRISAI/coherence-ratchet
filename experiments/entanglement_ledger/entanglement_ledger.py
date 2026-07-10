"""
entanglement_ledger.py — physics vs bookkeeping: does the classical-S corridor
track the TRUE quantum entanglement ledger?

THE QUESTION (README line 72; LedgerLaw.lean's own L-01 "KNOWN HOLE"):
  Our instrument is a CLASSICAL, PAIRWISE functional S = -ln det C of
  MEASURED-OUTCOME correlations. The gravity ledger's currency is
  ENTANGLEMENT (quantum, higher-order). Does the corridor structure our
  classical S reports (two poles, interior, saturation) also live in the true
  quantum entanglement structure, or only in the classical shadow?

Fully runnable classically by EXACT computation on SMALL quantum systems.

TWO QUANTITIES, per state / per coupling:

  (A) CLASSICAL-S  (our instrument, basis-DEPENDENT — that is the point):
      pick single-qubit measurement observables O_i = n_i . sigma (a
      measurement axis per site). Because the O_i commute across sites the
      joint outcome distribution is a genuine classical distribution; its
      pairwise outcome correlation matrix is EXACT (infinite-shot):
          C_ij = (<O_i O_j> - <O_i><O_j>) / sqrt((1-<O_i>^2)(1-<O_j>^2))
      Frozen sites (var ~ 0, i.e. deterministic outcomes = a "mean", clause-3
      blind) are dropped: the fluctuation copula ignores them. Then
          S_classical = -ln det C     (our entropic potential, T-E5b form)
      C singular (perfect outcome correlation) => S = +inf = the RIGIDITY POLE.
      C = I (independent outcomes)        => S = 0   = the CHAOS POLE / vacuum.

  (B) QUANTUM entanglement structure (the true ledger, basis-INDEPENDENT):
      - S_vN(A) = -Tr rho_A ln rho_A : von Neumann entanglement entropy across
        a bipartition (canonical bipartite entanglement).
      - I(i:j) = S(rho_i)+S(rho_j)-S(rho_ij) : quantum mutual information.
        Q_pair = sum_{i<j} I(i:j) is the HONEST pairwise analog of classical-S
        (same order, same "how correlated are the parts pairwise"), but
        basis-free and coherence-aware.
      - T = sum_i S(rho_i) - S(rho_global) : quantum total correlation /
        multi-information. For a PURE global state S(rho_global)=0 so
        T = sum_i S(rho_i). This is the all-orders multi-information whose
        Gaussian/pairwise shadow our classical S approximates.

WHY these are the honest analogs (honesty gate i): classical S = 2 * Gaussian
multi-information of the OUTCOME distribution (LedgerLaw clause 2a). Its exact,
basis-free, all-orders quantum counterpart is the quantum total correlation T;
its same-order counterpart is Q_pair. For a pure state the classical outcome
correlations and the entanglement are related but NOT identical — classical S
sees only the pairwise second moments of one measurement basis; the quantum
quantities see the whole density operator. The GAP between them IS the physics.

numpy/scipy only. Exact statevectors (N<=8 families) and sparse exact
diagonalization (N<=12 spin chains).
"""

import json
import numpy as np
from numpy.linalg import slogdet, eigvalsh
from itertools import combinations
import scipy.sparse as sp
import scipy.sparse.linalg as spla

RNG = np.random.default_rng(20260710)

# ---------------------------------------------------------------------------
# Single-qubit operators
# ---------------------------------------------------------------------------
I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
PAULI = {"X": SX, "Y": SY, "Z": SZ, "I": I2}


def axis_observable(theta, phi=0.0):
    """Single-qubit observable n.sigma for axis (sin th cos ph, sin th sin ph, cos th)."""
    return (np.sin(theta) * np.cos(phi) * SX
            + np.sin(theta) * np.sin(phi) * SY
            + np.cos(theta) * SZ)


# ---------------------------------------------------------------------------
# Statevector helpers (exact)
# ---------------------------------------------------------------------------
def op_on(op, i, N):
    """Embed single-qubit op on site i into full 2^N space (sparse)."""
    mats = [sp.identity(2, format="csr", dtype=complex)] * N
    mats[i] = sp.csr_matrix(op)
    out = mats[0]
    for m in mats[1:]:
        out = sp.kron(out, m, format="csr")
    return out


def two_op(opi, i, opj, j, N):
    mats = [sp.identity(2, format="csr", dtype=complex)] * N
    mats[i] = sp.csr_matrix(opi)
    mats[j] = sp.csr_matrix(opj)
    out = mats[0]
    for m in mats[1:]:
        out = sp.kron(out, m, format="csr")
    return out


def expval(psi, Op):
    return np.vdot(psi, Op @ psi).real


def reduced_dm(psi, keep, N):
    """Partial trace of pure state |psi> keeping the sites in `keep` (sorted)."""
    keep = sorted(keep)
    trace_out = [q for q in range(N) if q not in keep]
    t = psi.reshape([2] * N)
    # move kept axes to front
    perm = keep + trace_out
    t = np.transpose(t, perm)
    dk = 2 ** len(keep)
    dt = 2 ** len(trace_out)
    t = t.reshape(dk, dt)
    return t @ t.conj().T


def vn_entropy(rho, base_e=True):
    ev = eigvalsh(rho)
    ev = ev[ev > 1e-13]
    s = -(ev * np.log(ev)).sum()
    return float(s)


# ---------------------------------------------------------------------------
# CLASSICAL-S  (our instrument)
# ---------------------------------------------------------------------------
def classical_correlation_matrix(psi, N, obs_list):
    """obs_list[i] = single-qubit observable measured on site i (commuting across
    sites). Returns (C, kept_indices, means, variances).

    Uses the Hermitian identity <O_i O_j> = <O_i psi | O_j psi> (the O_i are
    Hermitian and commute across sites), so we form a_i = O_i|psi> once per site
    and read all pairwise correlations off inner products a_i^dagger a_j."""
    a = [op_on(obs_list[i], i, N) @ psi for i in range(N)]
    means = np.array([np.vdot(psi, a[i]).real for i in range(N)])
    var = 1.0 - means ** 2  # since O_i^2 = I for a unit-axis observable
    kept = [i for i in range(N) if var[i] > 1e-9]
    k = len(kept)
    C = np.eye(k)
    for aa in range(k):
        for bb in range(aa + 1, k):
            i, j = kept[aa], kept[bb]
            eij = np.vdot(a[i], a[j]).real
            cov = eij - means[i] * means[j]
            C[aa, bb] = C[bb, aa] = cov / np.sqrt(var[i] * var[j])
    return C, kept, means, var


def classical_S_from_C(C):
    """S = -ln det C, with the rigidity pole reported as np.inf."""
    if C.shape[0] == 0:
        return 0.0  # vacuum: everything frozen / no fluctuation copula
    ev = eigvalsh(C)
    lam_min = float(ev.min())
    if lam_min <= 1e-12:
        return np.inf
    sgn, logdet = slogdet(C)
    if sgn <= 0:
        return np.inf
    return float(-logdet)


def classical_S(psi, N, obs_list):
    C, kept, means, var = classical_correlation_matrix(psi, N, obs_list)
    S = classical_S_from_C(C)
    return S, C, kept


def uniform_axis_obs(theta, N, phi=0.0):
    O = axis_observable(theta, phi)
    return [O] * N


# ---------------------------------------------------------------------------
# QUANTUM entanglement structure (the true ledger)
# ---------------------------------------------------------------------------
def quantum_structure(psi, N):
    """Return dict of the true (basis-free) entanglement quantities."""
    # single-site entropies
    S_site = np.array([vn_entropy(reduced_dm(psi, [i], N)) for i in range(N)])
    T_total = float(S_site.sum())  # pure global state => S(rho_global)=0

    # half-chain (contiguous) bipartite entanglement
    half = list(range(N // 2))
    S_half = vn_entropy(reduced_dm(psi, half, N))

    # pairwise quantum mutual information network
    Qpair = 0.0
    Imat = np.zeros((N, N))
    for i, j in combinations(range(N), 2):
        rij = reduced_dm(psi, [i, j], N)
        Iij = S_site[i] + S_site[j] - vn_entropy(rij)
        Imat[i, j] = Imat[j, i] = Iij
        Qpair += Iij
    return {
        "S_site": S_site.tolist(),
        "T_total": T_total,
        "S_half": float(S_half),
        "Q_pair": float(Qpair),
        "I_matrix": Imat.tolist(),
    }


# ---------------------------------------------------------------------------
# State families
# ---------------------------------------------------------------------------
def ghz_state(N):
    psi = np.zeros(2 ** N, dtype=complex)
    psi[0] = 1 / np.sqrt(2)
    psi[-1] = 1 / np.sqrt(2)
    return psi


def w_state(N):
    psi = np.zeros(2 ** N, dtype=complex)
    for i in range(N):
        psi[1 << i] = 1.0
    return psi / np.linalg.norm(psi)


def product_state(N):
    psi = np.zeros(2 ** N, dtype=complex)
    psi[0] = 1.0
    return psi


def haar_random_state(N):
    v = RNG.standard_normal(2 ** N) + 1j * RNG.standard_normal(2 ** N)
    return v / np.linalg.norm(v)


def cluster_state(N):
    """1D cluster/graph state: H on all, then CZ on nearest neighbours (open)."""
    psi = np.ones(2 ** N, dtype=complex) / np.sqrt(2 ** N)  # |+>^N
    # apply CZ_{i,i+1}: multiply amplitude by -1 where bits i and i+1 both 1
    for idx in range(2 ** N):
        bits = [(idx >> b) & 1 for b in range(N)]
        sign = 1
        for i in range(N - 1):
            if bits[i] and bits[i + 1]:
                sign *= -1
        psi[idx] *= sign
    return psi


# ---------------------------------------------------------------------------
# Spin-chain Hamiltonians (sparse) + ground states
# ---------------------------------------------------------------------------
def tfim_ground_state(N, g, J=1.0, pbc=False, hz=0.0):
    """H = -J sum ZZ - g sum X - hz sum Z. QPT at g=1 (in units J=1).

    hz=0 gives the Z2-SYMMETRIC ground state (in the ordered phase a GHZ-like
    cat that carries an extra ln2 across every cut). A small hz>0 breaks the
    symmetry and selects a physical broken state whose half-chain entanglement
    is the textbook criticality corridor (0 -> peak at g~1 -> 0)."""
    dim = 2 ** N
    H = sp.csr_matrix((dim, dim), dtype=complex)
    bonds = N if pbc else N - 1
    for i in range(bonds):
        j = (i + 1) % N
        H = H - J * two_op(SZ, i, SZ, j, N)
    for i in range(N):
        H = H - g * op_on(SX, i, N)
        if hz != 0.0:
            H = H - hz * op_on(SZ, i, N)
    H = H.real
    vals, vecs = spla.eigsh(H, k=1, which="SA")
    psi = vecs[:, 0].astype(complex)
    return psi, float(vals[0])


def xxz_ground_state(N, Delta, J=1.0, pbc=False):
    """H = J sum (XX + YY + Delta ZZ). Gapless XY -1<Delta<=1, gapped else."""
    dim = 2 ** N
    H = sp.csr_matrix((dim, dim), dtype=complex)
    bonds = N if pbc else N - 1
    for i in range(bonds):
        j = (i + 1) % N
        H = H + J * two_op(SX, i, SX, j, N)
        H = H + J * two_op(SY, i, SY, j, N)
        H = H + J * Delta * two_op(SZ, i, SZ, j, N)
    H = H.real
    vals, vecs = spla.eigsh(H, k=1, which="SA")
    psi = vecs[:, 0].astype(complex)
    return psi, float(vals[0])


# ---------------------------------------------------------------------------
# Basis sweep for classical-S
# ---------------------------------------------------------------------------
def classical_S_basis_sweep(psi, N, thetas, phi=0.0):
    """Uniform measurement axis rotated in the (X,Z) plane by theta."""
    out = []
    for th in thetas:
        S, C, kept = classical_S(psi, N, uniform_axis_obs(th, N, phi))
        out.append(S)
    return np.array(out)


# ---------------------------------------------------------------------------
# EXPERIMENT 1 — GHZ / W / product / random / cluster: the blind-spot gap
# ---------------------------------------------------------------------------
def experiment_families(N=6):
    families = {
        "product": product_state(N),
        "GHZ": ghz_state(N),
        "W": w_state(N),
        "cluster": cluster_state(N),
        "random_Haar": haar_random_state(N),
    }
    thetas = np.linspace(0, np.pi / 2, 46)  # Z (0) .. X (pi/2)
    results = {}
    for name, psi in families.items():
        q = quantum_structure(psi, N)
        # classical S in the three MUBs
        S_Z, _, _ = classical_S(psi, N, [SZ] * N)
        S_X, _, _ = classical_S(psi, N, [SX] * N)
        S_Y, _, _ = classical_S(psi, N, [SY] * N)
        sweep = classical_S_basis_sweep(psi, N, thetas)
        finite = sweep[np.isfinite(sweep)]
        results[name] = {
            "N": N,
            "quantum": {k: v for k, v in q.items() if k != "I_matrix"},
            "classical_S": {
                "Z": None if np.isinf(S_Z) else S_Z,
                "X": None if np.isinf(S_X) else S_X,
                "Y": None if np.isinf(S_Y) else S_Y,
                "Z_is_pole": bool(np.isinf(S_Z)),
                "X_is_pole": bool(np.isinf(S_X)),
                "Y_is_pole": bool(np.isinf(S_Y)),
            },
            "basis_sweep": {
                "theta": thetas.tolist(),
                "S": [None if np.isinf(s) else float(s) for s in sweep],
                "min_over_basis": float(finite.min()) if finite.size else None,
                "max_over_basis": (float(finite.max()) if finite.size else None),
                "any_pole": bool(np.any(np.isinf(sweep))),
            },
        }
    return results, thetas


# ---------------------------------------------------------------------------
# EXPERIMENT 2 — TFIM sweep across the QPT: do the two corridors overlay?
# ---------------------------------------------------------------------------
def _tfim_sector(N, gs, thetas, hz):
    S_half, Q_pair, T_total, zz_order, S_Z, S_X = [], [], [], [], [], []
    Ssurf = np.zeros((len(gs), len(thetas)))
    for gi, g in enumerate(gs):
        psi, e0 = tfim_ground_state(N, g, hz=hz)
        q = quantum_structure(psi, N)
        S_half.append(q["S_half"])
        Q_pair.append(q["Q_pair"])
        T_total.append(q["T_total"])
        zz_order.append(abs(expval(psi, two_op(SZ, 0, SZ, N - 1, N))))
        sZ, _, _ = classical_S(psi, N, [SZ] * N)
        sX, _, _ = classical_S(psi, N, [SX] * N)
        S_Z.append(sZ)
        S_X.append(sX)
        Ssurf[gi] = classical_S_basis_sweep(psi, N, thetas)
    return {
        "hz": hz,
        "S_half": S_half,
        "Q_pair": Q_pair,
        "T_total": T_total,
        "zz_order": zz_order,
        "classical_S_Z": [None if np.isinf(s) else float(s) for s in S_Z],
        "classical_S_X": [None if np.isinf(s) else float(s) for s in S_X],
        "S_surface": [[None if np.isinf(s) else float(s) for s in row]
                      for row in Ssurf],
    }


def experiment_tfim(N=10, gs=None, n_theta=25, hz_break=0.02):
    """Sweep g across the QPT. Compute quantum entanglement + classical-S basis
    surface in BOTH the Z2-symmetric sector (hz=0; ordered phase = GHZ cat) and
    the symmetry-broken sector (hz=hz_break; textbook criticality corridor)."""
    if gs is None:
        gs = np.linspace(0.05, 2.0, 40)
    thetas = np.linspace(0, np.pi / 2, n_theta)
    return {
        "N": N,
        "g": gs.tolist(),
        "theta": thetas.tolist(),
        "hz_break": hz_break,
        "symmetric": _tfim_sector(N, gs, thetas, hz=0.0),
        "broken": _tfim_sector(N, gs, thetas, hz=hz_break),
    }


def experiment_xxz(N=10, deltas=None):
    if deltas is None:
        deltas = np.linspace(-2.0, 2.0, 33)
    S_half, Q_pair, T_total, S_Z, S_X = [], [], [], [], []
    for D in deltas:
        psi, e0 = xxz_ground_state(N, D)
        q = quantum_structure(psi, N)
        S_half.append(q["S_half"])
        Q_pair.append(q["Q_pair"])
        T_total.append(q["T_total"])
        sZ, _, _ = classical_S(psi, N, [SZ] * N)
        sX, _, _ = classical_S(psi, N, [SX] * N)
        S_Z.append(sZ)
        S_X.append(sX)
    return {
        "N": N,
        "Delta": deltas.tolist(),
        "S_half": S_half,
        "Q_pair": Q_pair,
        "T_total": T_total,
        "classical_S_Z": [None if np.isinf(s) else float(s) for s in S_Z],
        "classical_S_X": [None if np.isinf(s) else float(s) for s in S_X],
    }


# ---------------------------------------------------------------------------
# Correlation / verdict helpers
# ---------------------------------------------------------------------------
def _pearson(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3:
        return None
    a, b = a[m], b[m]
    if a.std() < 1e-12 or b.std() < 1e-12:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def _argpeak(x, grid):
    x = np.asarray(x, float)
    m = np.isfinite(x)
    if m.sum() == 0:
        return None
    idx = np.nanargmax(np.where(m, x, -np.inf))
    return float(grid[idx])


def main():
    out = {"meta": {
        "seed": 20260710,
        "description": "physics vs bookkeeping: classical-S corridor vs true "
                       "quantum entanglement corridor",
    }}

    # -- Experiment 1: state families --------------------------------------
    fam, thetas = experiment_families(N=6)
    out["families"] = fam

    # GHZ blind-spot gap: X-basis classical-S vs quantum multipartite content
    ghz = fam["GHZ"]
    out["ghz_gap"] = {
        "classical_S_X": ghz["classical_S"]["X"],
        "classical_S_Z_is_pole": ghz["classical_S"]["Z_is_pole"],
        "quantum_T_total": ghz["quantum"]["T_total"],
        "quantum_S_half": ghz["quantum"]["S_half"],
        "quantum_Q_pair": ghz["quantum"]["Q_pair"],
        "min_classical_S_over_all_bases": ghz["basis_sweep"]["min_over_basis"],
        "note": "X-basis: classical-S=0 (vacuum) while T_total=N*ln2 maximal; "
                "Z-basis: rigidity pole. Neither reads the interior.",
    }

    # -- Experiment 2: TFIM sweep ------------------------------------------
    tfim = experiment_tfim(N=10)
    out["tfim"] = tfim
    g = np.array(tfim["g"])
    theta = np.array(tfim["theta"])

    def _analyze_sector(sec):
        SZv = [np.nan if v is None else v for v in sec["classical_S_Z"]]
        SXv = [np.nan if v is None else v for v in sec["classical_S_X"]]
        surf = np.array([[np.nan if v is None else v for v in row]
                         for row in sec["S_surface"]])
        # best fixed basis for tracking the quantum entanglement corridor
        best = {"S_half": (-2.0, None), "Q_pair": (-2.0, None)}
        for ti in range(surf.shape[1]):
            for tgt in ("S_half", "Q_pair"):
                c = _pearson(surf[:, ti], sec[tgt])
                if c is not None and c > best[tgt][0]:
                    best[tgt] = (c, float(theta[ti]))
        return {
            "peak_g_S_half": _argpeak(sec["S_half"], g),
            "peak_g_Q_pair": _argpeak(sec["Q_pair"], g),
            "peak_g_classical_S_Z": _argpeak(
                [np.nan if v is None else v for v in SZv], g),
            "peak_g_classical_S_X": _argpeak(
                [np.nan if v is None else v for v in SXv], g),
            "corr_classicalSZ_Shalf": _pearson(SZv, sec["S_half"]),
            "corr_classicalSX_Shalf": _pearson(SXv, sec["S_half"]),
            "corr_classicalSZ_zzOrder": _pearson(SZv, sec["zz_order"]),
            "corr_classicalSX_zzOrder": _pearson(SXv, sec["zz_order"]),
            "best_basis_for_S_half": {
                "corr": None if best["S_half"][1] is None else best["S_half"][0],
                "theta_rad": best["S_half"][1]},
            "best_basis_for_Q_pair": {
                "corr": None if best["Q_pair"][1] is None else best["Q_pair"][0],
                "theta_rad": best["Q_pair"][1]},
        }

    out["tfim_analysis"] = {
        "symmetric": _analyze_sector(tfim["symmetric"]),
        "broken": _analyze_sector(tfim["broken"]),
    }

    # -- Experiment 3: XXZ sweep -------------------------------------------
    xxz = experiment_xxz(N=10)
    out["xxz"] = xxz
    D = np.array(xxz["Delta"])
    out["xxz_analysis"] = {
        "peak_Delta_S_half": _argpeak(xxz["S_half"], D),
        "peak_Delta_Q_pair": _argpeak(xxz["Q_pair"], D),
        "corr_classicalSZ_Shalf": _pearson(
            [np.nan if v is None else v for v in xxz["classical_S_Z"]], xxz["S_half"]),
        "corr_classicalSX_Shalf": _pearson(
            [np.nan if v is None else v for v in xxz["classical_S_X"]], xxz["S_half"]),
    }

    with open("experiments/entanglement_ledger/results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("wrote results.json")
    # console summary
    print("\n=== GHZ blind-spot gap (N=6) ===")
    print(json.dumps(out["ghz_gap"], indent=2))
    print("\n=== TFIM analysis ===")
    print(json.dumps(out["tfim_analysis"], indent=2))
    print("\n=== XXZ analysis ===")
    print(json.dumps(out["xxz_analysis"], indent=2))
    return out


if __name__ == "__main__":
    main()
