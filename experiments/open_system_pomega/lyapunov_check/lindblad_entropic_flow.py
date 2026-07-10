"""
Is the forward open-system P_omega (Lindblad steady state) gradient flow on the
entropic potential S(k, rho) = -ln det C ?

The model mirrors experiments/open_system_pomega/construct_pomega_lindblad.py
exactly (6 spins / 3 rungs, dim 64; intra-rung Heisenberg + cross-rung ZZ;
per-rung collective decay = the "alpha" channel; per-spin bit-flip at rate
gamma_M = the maintenance channel). That script only solved for the steady state
rho_ss. Here we integrate the TRAJECTORY rho(t) -> rho_ss and watch the entropic
potential along it.

TWO DIFFERENT ENTROPIES -- the load-bearing distinction
-------------------------------------------------------
The Lean object (T-E5, Core/EntropicPotential.lean) is

    S(k, rho) = -ln det C = -sum_i ln lambda_i(C)

with C the k x k CORRELATION MATRIX (unit diagonal) of k coordinating units;
and S = 2 * I where I is the GAUSSIAN multi-information of those units.

The Lindblad object is a DENSITY MATRIX on a 64-dim Hilbert space. It is a
different object. -Tr ln(density matrix) is neither -ln det C nor the von
Neumann entropy. So we compute, separately and explicitly:

  (A) THE T-E5 OBJECT.  The six spin observables Z_i mutually COMMUTE, so any
      state rho induces a genuine joint probability distribution over
      {+1,-1}^6 -- the diagonal of rho in the computational basis. Its Pearson
      correlation matrix

          C_ij = cov(Z_i, Z_j) / sqrt(var Z_i * var Z_j)

      is a bona fide classical correlation matrix: exactly the object an
      experimenter builds from projective Z readouts, and exactly what the
      bridge note's prediction candidate says to measure ("the eigenvalue
      spectrum of the correlation matrix across the coordinating degrees of
      freedom"). We take the k=6 SPINS as the sensors / coordinating units;
      we also report the k=3 rung-level reduction using the collective rung
      observable (Z_a + Z_b)/2.
          S_det := -ln det C.
      This is the potential of T-E1..T-E5, on the nose.

      NOTE (raw moment vs correlation). construct_pomega_lindblad.py reports
      rho_n := |<Z_a Z_b>|, the RAW second moment. That is not the correlation
      coefficient the Kish / entropic algebra takes as its rho: if the spins are
      polarised (<Z_i> != 0) then <Z_a Z_b> = C_ab*sqrt(var_a var_b) +
      <Z_a><Z_b>, and the second term can dominate. We report both.

  (B) THE QUANTUM RELATIVE-ENTROPY OBJECTS.  The correct quantum analogue of a
      multi-information is the quantum TOTAL CORRELATION
          T(rho) = sum_i S_vN(rho_i) - S_vN(rho) = D(rho || rho_1 (x) ... (x) rho_6)
      a relative entropy against the product of marginals (>= 0, = 0 iff
      product). And the functional guaranteed to be a Lyapunov function of any
      Lindblad flow with a stationary rho_ss is Spohn's
          D(rho(t) || rho_ss),
      monotone non-increasing by data processing under the CPTP semigroup. Both
      are computed; the Spohn monotonicity doubles as an integrator check.

  We also compute the DISCRETE multi-information I_disc of the same +-1 readouts,
  to quantify how far the Gaussian reading S = 2*I is from the truth here.

ALPHA-CHANNEL DIAGNOSTIC
------------------------
The framework's Piece 2 is drho/dt = alpha - gamma*M: alpha is by definition the
rate at which correlation is WRITTEN INTO the substrate. A collective-decay
channel does not do that -- it polarises. We therefore also run a properly
specified alpha channel: pairwise ALIGNMENT ("consensus"/copying) jumps

    A_ab = |uu><ud| + |uu><du|      (anti-aligned -> up-up)
    B_ab = |dd><ud| + |dd><du|      (anti-aligned -> down-down)

symmetric under a<->b and under global flip, so they create positive Z
correlation with no net polarisation. This isolates whether a NO verdict is a
property of S or a property of the channel the original script chose.

numpy/scipy only. Fixed seed. Writes results.json + PNGs next to this file.
"""
import json
import os

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.integrate import solve_ivp

SEED = 20260710
np.random.seed(SEED)
HERE = os.path.dirname(os.path.abspath(__file__))

NSPIN = 6
DIM = 2 ** NSPIN
RUNGS = [(0, 1), (2, 3), (4, 5)]
GAMMA_ALPHA = (0.6, 1.0, 1.5)     # per-rung rigidity-drift rates (original script)
J_HEIS, G_ZZ = 1.0, 0.5

EPS_VAR = 1e-9      # variance floor: below this a spin is fully polarised
EPS_EIG = 1e-12     # eigenvalue floor for -ln det C
EPS_P = 1e-14       # probability floor for entropies

# ---------------------------------------------------------------- operators
sI = sp.identity(2, format="csr", dtype=complex)
sX = sp.csr_matrix(np.array([[0, 1], [1, 0]], dtype=complex))
sY = sp.csr_matrix(np.array([[0, -1j], [1j, 0]], dtype=complex))
sZ = sp.csr_matrix(np.array([[1, 0], [0, -1]], dtype=complex))
sSM = sp.csr_matrix(np.array([[0, 0], [1, 0]], dtype=complex))   # |1><0|, lowers |0>


def _site(op, i):
    out = sp.identity(1, format="csr", dtype=complex)
    for j in range(NSPIN):
        out = sp.kron(out, op if j == i else sI, format="csr")
    return out


SX = [_site(sX, i) for i in range(NSPIN)]
SY = [_site(sY, i) for i in range(NSPIN)]
SZ = [_site(sZ, i) for i in range(NSPIN)]
SM = [_site(sSM, i) for i in range(NSPIN)]
SP = [m.getH().tocsr() for m in SM]
PU = [(sp.identity(DIM, format="csr", dtype=complex) + SZ[i]) * 0.5 for i in range(NSPIN)]
PD = [(sp.identity(DIM, format="csr", dtype=complex) - SZ[i]) * 0.5 for i in range(NSPIN)]
sId = sp.identity(DIM, format="csr", dtype=complex)

ZDIAG = np.array([np.real(SZ[i].diagonal()) for i in range(NSPIN)])   # (6, 64), +-1


def diss(L):
    """Row-major-vec Lindblad dissipator. vec_r(A X B) = (A (x) B^T) vec_r(X)."""
    L = sp.csr_matrix(L)
    LdL = (L.getH() @ L).tocsr()
    return (sp.kron(L, L.conj(), format="csr")
            - 0.5 * sp.kron(LdL, sId, format="csr")
            - 0.5 * sp.kron(sId, LdL.T, format="csr"))


def hamiltonian(g=G_ZZ, J=J_HEIS):
    H = sp.csr_matrix((DIM, DIM), dtype=complex)
    for (a, b) in RUNGS:
        H = H + J * (SX[a] @ SX[b] + SY[a] @ SY[b] + SZ[a] @ SZ[b])
    for n in range(len(RUNGS) - 1):
        H = H + g * (SZ[RUNGS[n][1]] @ SZ[RUNGS[n + 1][0]])
    return ((H + H.getH()) * 0.5).tocsr()


def commutator_super(H):
    return -1j * (sp.kron(H, sId, format="csr") - sp.kron(sId, H.T, format="csr"))


def align_jumps(a, b, rate):
    """Consensus/copying jumps on pair (a,b): drive anti-aligned -> aligned,
    symmetric in up/down so no net polarisation is induced."""
    A = (PU[a] @ SP[b] + SP[a] @ PU[b])
    B = (SM[a] @ PD[b] + PD[a] @ SM[b])
    return [np.sqrt(rate) * A, np.sqrt(rate) * B]


def build_pieces(g=G_ZZ, alpha_scale=1.0, alpha_channel="decay", J=J_HEIS):
    """Return (L0, Lbf) with full Liouvillian = L0 + gamma_M * Lbf."""
    L0 = commutator_super(hamiltonian(g=g, J=J))
    if alpha_channel == "decay":                     # the original script's alpha
        for rate, (a, b) in zip(GAMMA_ALPHA, RUNGS):
            L0 = L0 + diss(np.sqrt(alpha_scale * rate) * (SM[a] + SM[b]))
    elif alpha_channel == "align":                   # correlation-writing alpha
        for rate, (a, b) in zip(GAMMA_ALPHA, RUNGS):
            for Jop in align_jumps(a, b, alpha_scale * rate):
                L0 = L0 + diss(Jop)
        for n in range(len(RUNGS) - 1):              # cross-rung links, rate g
            if g > 0:
                for Jop in align_jumps(RUNGS[n][1], RUNGS[n + 1][0], alpha_scale * g):
                    L0 = L0 + diss(Jop)
    elif alpha_channel == "align_all":               # exchange-symmetric (uniform rho)
        for i in range(NSPIN):
            for j in range(i + 1, NSPIN):
                for Jop in align_jumps(i, j, alpha_scale):
                    L0 = L0 + diss(Jop)
    else:
        raise ValueError(alpha_channel)
    Lbf = sp.csr_matrix((DIM * DIM, DIM * DIM), dtype=complex)
    for i in range(NSPIN):
        Lbf = Lbf + diss(SX[i])
    return L0.tocsr(), Lbf.tocsr()


def steady_state(L0, Lbf, gamma_M):
    """Trace-replacement linear solve (same trick as construct_pomega_lindblad.py)."""
    M = (L0 + gamma_M * Lbf).tolil()
    M[0, :] = np.eye(DIM, dtype=complex).reshape(-1)
    M = M.tocsc()
    b = np.zeros(DIM * DIM, dtype=complex)
    b[0] = 1.0
    rho = spla.spsolve(M, b).reshape(DIM, DIM)
    rho = (rho + rho.conj().T) / 2
    return rho / np.trace(rho).real


# ---------------------------------------------------- (A) the T-E5 object
def z_observables(groups=None):
    if groups is None:
        return ZDIAG
    return np.array([ZDIAG[a] + ZDIAG[b] for (a, b) in groups]) / 2.0


def z_correlation_matrix(rho, groups=None):
    """Pearson correlation matrix of the (mutually commuting) Z readouts."""
    p = np.clip(np.real(np.diag(rho)), 0.0, None)
    p = p / p.sum()
    obs = z_observables(groups)
    m = obs @ p                                       # <O_i>
    cov = (obs * p) @ obs.T - np.outer(m, m)
    var = np.diag(cov).copy()
    floored = int(np.sum(var < EPS_VAR))
    d = 1.0 / np.sqrt(np.maximum(var, EPS_VAR))
    C = cov * np.outer(d, d)
    np.fill_diagonal(C, 1.0)
    return (C + C.T) / 2, floored


def s_det(C):
    """S = -ln det C = -sum ln lambda_i, with an eigenvalue floor."""
    ev = np.linalg.eigvalsh(C)
    n_floored = int(np.sum(ev < EPS_EIG))
    return float(-np.sum(np.log(np.maximum(ev, EPS_EIG)))), ev, n_floored


def rho_bar(C):
    iu = np.triu_indices(C.shape[0], 1)
    return float(np.mean(C[iu]))


def k_eff_participation(C):
    ev = np.maximum(np.linalg.eigvalsh(C), 0.0)
    return float(ev.sum() ** 2 / np.sum(ev ** 2))


def k_eff_kish(k, r):
    return k / (1.0 + r * (k - 1.0))


def S_closed(k, r):
    """Uniform-rho closed form (T-E1). Domain of the theorems is 0 <= r < 1."""
    if not (-1.0 / (k - 1) < r < 1.0):
        return np.nan
    return float(-np.log(1 + r * (k - 1)) - (k - 1) * np.log(1 - r))


def dS_drho_closed(k, r):
    """dS/drho = (k-1)[1/(1-r) - 1/(1+r(k-1))]   (T-E2)."""
    if not (-1.0 / (k - 1) < r < 1.0):
        return np.nan
    return (k - 1.0) * (1.0 / (1.0 - r) - 1.0 / (1.0 + r * (k - 1.0)))


def raw_zz(rho):
    return [abs(float(np.real(np.trace(rho @ (SZ[a] @ SZ[b]).toarray())))) for a, b in RUNGS]


def mean_z(rho):
    return ZDIAG @ np.clip(np.real(np.diag(rho)), 0, None)


# ------------------------------------------ (B) quantum relative entropies
def vn_entropy(rho):
    ev = np.linalg.eigvalsh(rho)
    ev = ev[ev > EPS_P]
    return float(-np.sum(ev * np.log(ev)))


def marginal_z(rho, i):
    t = rho.reshape([2] * (2 * NSPIN))
    order = ([i, NSPIN + i]
             + [j for j in range(NSPIN) if j != i]
             + [NSPIN + j for j in range(NSPIN) if j != i])
    t = np.transpose(t, order).reshape(2, 2, 2 ** (NSPIN - 1), 2 ** (NSPIN - 1))
    return np.trace(t, axis1=2, axis2=3)


def total_correlation(rho):
    """T(rho) = sum_i S(rho_i) - S(rho) = D(rho || (x)_i rho_i) in [0, k ln 2]."""
    return float(sum(vn_entropy(marginal_z(rho, i)) for i in range(NSPIN))
                 - vn_entropy(rho))


def discrete_multi_information(rho):
    """I of the actual +-1 readout distribution (NOT the Gaussian surrogate)."""
    p = np.clip(np.real(np.diag(rho)), 0, None)
    p = p / p.sum()
    H = -np.sum(p[p > EPS_P] * np.log(p[p > EPS_P]))
    Hi = 0.0
    for i in range(NSPIN):
        pu = p[ZDIAG[i] > 0].sum()
        pi = np.array([pu, 1 - pu])
        Hi += -np.sum(pi[pi > EPS_P] * np.log(pi[pi > EPS_P]))
    return float(Hi - H)


def rel_entropy(rho, sigma):
    """D(rho||sigma) = Tr rho ln rho - Tr rho ln sigma. sigma assumed full rank."""
    pr, Ur = np.linalg.eigh(rho)
    qs, Us = np.linalg.eigh(sigma)
    pr = np.clip(pr, 0.0, None)
    keep = qs > EPS_P
    term1 = np.sum(pr[pr > EPS_P] * np.log(pr[pr > EPS_P]))
    ov = np.abs(Ur.conj().T @ Us[:, keep]) ** 2
    term2 = float(pr @ (ov @ np.log(qs[keep])))
    return float(term1 - term2)


# ---------------------------------------------------------- initial states
def ic_maxmix():
    return np.eye(DIM, dtype=complex) / DIM


def ic_plus():
    v = np.ones(DIM, dtype=complex) / np.sqrt(DIM)      # |+>^6: pure, C = I, S = 0
    return np.outer(v, v.conj())


def ic_ghz_soft(eps=0.05):
    v = np.zeros(DIM, dtype=complex)
    v[0] = v[DIM - 1] = 1 / np.sqrt(2)
    return (1 - eps) * np.outer(v, v.conj()) + eps * np.eye(DIM, dtype=complex) / DIM


# ---------------------------------------------------------------- trajectory
def time_grid(T=40.0):
    return np.unique(np.concatenate([
        np.linspace(0.0, 1.0, 201),
        np.linspace(1.0, 5.0, 161),
        np.linspace(5.0, T, 201),
    ]))


def integrate(Lsp, rho0, ts):
    n = DIM * DIM
    y0 = rho0.reshape(-1)
    y0r = np.concatenate([y0.real, y0.imag])

    def rhs(_t, y):
        v = y[:n] + 1j * y[n:]
        w = Lsp @ v
        return np.concatenate([w.real, w.imag])

    sol = solve_ivp(rhs, (ts[0], ts[-1]), y0r, t_eval=ts,
                    method="RK45", rtol=1e-9, atol=1e-11, max_step=0.05)
    assert sol.success, sol.message
    out = []
    for j in range(len(ts)):
        r = (sol.y[:n, j] + 1j * sol.y[n:, j]).reshape(DIM, DIM)
        out.append((r + r.conj().T) / 2)
    return out


def trace_traj(rhos, rho_ss, k=6, groups=None):
    keys = ["S_det", "rho_bar", "k_eff_pr", "k_eff_kish", "S_closed",
            "dS_drho_closed", "S_vN", "T_corr", "I_disc", "D_ss", "purity",
            "lam_min", "n_floored_eig", "n_floored_var", "trace_err", "herm_err"]
    rec = {kk: [] for kk in keys}
    for r in rhos:
        C, nfv = z_correlation_matrix(r, groups)
        S, ev, nfe = s_det(C)
        rb = rho_bar(C)
        rec["S_det"].append(S)
        rec["rho_bar"].append(rb)
        rec["k_eff_pr"].append(k_eff_participation(C))
        rec["k_eff_kish"].append(k_eff_kish(k, rb))
        rec["S_closed"].append(S_closed(k, rb))
        rec["dS_drho_closed"].append(dS_drho_closed(k, rb))
        rec["S_vN"].append(vn_entropy(r))
        rec["T_corr"].append(total_correlation(r))
        rec["I_disc"].append(discrete_multi_information(r))
        rec["D_ss"].append(rel_entropy(r, rho_ss))
        rec["purity"].append(float(np.trace(r @ r).real))
        rec["lam_min"].append(float(ev.min()))
        rec["n_floored_eig"].append(nfe)
        rec["n_floored_var"].append(nfv)
        rec["trace_err"].append(abs(float(np.trace(r).real) - 1.0))
        rec["herm_err"].append(float(np.abs(r - r.conj().T).max()))
    return {kk: np.array(v) for kk, v in rec.items()}


def r2(y, yhat):
    m = np.isfinite(y) & np.isfinite(yhat)
    y, yhat = y[m], yhat[m]
    ss_tot = np.sum((y - y.mean()) ** 2)
    return float(1 - np.sum((y - yhat) ** 2) / ss_tot) if ss_tot > 0 else np.nan


def summarize_state(rho, tag):
    C, nfv = z_correlation_matrix(rho)
    S, ev, nfe = s_det(C)
    C3, _ = z_correlation_matrix(rho, RUNGS)
    S3, ev3, _ = s_det(C3)
    rb = rho_bar(C)
    return {
        "tag": tag,
        "S_det_k6": S, "rho_bar_k6": rb,
        "S_closed_from_rhobar_k6": S_closed(6, rb),
        "k_eff_pr_k6": k_eff_participation(C),
        "k_eff_kish_k6": k_eff_kish(6, rb),
        "min_eig_C_k6": float(ev.min()),
        "intra_rung_C": [float(C[a, b]) for a, b in RUNGS],
        "S_det_k3_rungs": S3, "rho_bar_k3_rungs": rho_bar(C3),
        "raw_abs_ZZ_per_rung": raw_zz(rho),
        "mean_Z_per_spin": mean_z(rho).tolist(),
        "min_var_Z": float(np.min(1 - mean_z(rho) ** 2)),
        "S_vN": vn_entropy(rho),
        "T_corr_quantum": total_correlation(rho),
        "I_disc": discrete_multi_information(rho),
        "two_I_disc": 2 * discrete_multi_information(rho),
        "purity": float(np.trace(rho @ rho).real),
        "floored_eigs": nfe, "floored_vars": nfv,
    }


# ================================================================== main
def main():
    res = {"seed": SEED, "dim": DIM, "nspin": NSPIN, "k_ln2_bound": NSPIN * np.log(2),
           "eps_eig": EPS_EIG, "eps_var": EPS_VAR,
           "gamma_alpha": list(GAMMA_ALPHA), "J": J_HEIS, "g_default": G_ZZ}

    GM, G = 0.5, 0.5
    print(f"[1] baseline model (alpha = per-rung collective decay), gamma_M={GM}, g={G}")
    L0, Lbf = build_pieces(g=G, alpha_channel="decay")
    Lsp = (L0 + GM * Lbf).tocsr()
    rss = steady_state(L0, Lbf, GM)
    ss = summarize_state(rss, "rho_ss(decay, gM=0.5)")
    res["steady_state_baseline"] = ss
    print(f"    S_det={ss['S_det_k6']:.4f}  rho_bar={ss['rho_bar_k6']:+.4f}  "
          f"intra-rung C={np.round(ss['intra_rung_C'],3)}  "
          f"raw|<ZZ>|={np.round(ss['raw_abs_ZZ_per_rung'],3)}")
    print(f"    T_quantum={ss['T_corr_quantum']:.4f}  2*I_disc={ss['two_I_disc']:.4f}  "
          f"S_det={ss['S_det_k6']:.4f}   (k ln2 = {NSPIN*np.log(2):.4f})")

    S_ss = ss["S_det_k6"]
    ts = time_grid()
    ics = {"maxmix": ic_maxmix(),
           "plus_product": ic_plus(),
           "ghz_soft": ic_ghz_soft()}
    traj, tres = {}, {}
    for name, r0 in ics.items():
        print(f"    integrating IC: {name}")
        rhos = integrate(Lsp, r0, ts)
        rec = trace_traj(rhos, rss)
        dS = np.gradient(rec["S_det"], ts)
        drb = np.gradient(rec["rho_bar"], ts)
        dD = np.gradient(rec["D_ss"], ts)
        dT = np.gradient(rec["T_corr"], ts)
        pred = rec["dS_drho_closed"] * drb

        act = np.abs(dS) > 1e-6 * max(np.abs(dS).max(), 1e-30)
        frac_pos = float(np.mean(dS[act] > 0)) if act.any() else np.nan
        frac_neg = float(np.mean(dS[act] < 0)) if act.any() else np.nan
        toward = np.sign(dS[act]) == np.sign(S_ss - rec["S_det"][act])
        frac_toward = float(np.mean(toward)) if act.any() else np.nan

        actD = np.abs(dD) > 1e-9 * max(np.abs(dD).max(), 1e-30)
        frac_D_nonpos = float(np.mean(dD[actD] <= 0)) if actD.any() else np.nan

        mm = np.abs(dS) > 1e-3 * np.abs(dS).max()
        chain_r2 = r2(dS[mm], pred[mm])
        chain_resid = float(np.median(np.abs(dS[mm] - pred[mm]) / (np.abs(dS[mm]) + 1e-30)))

        traj[name] = dict(ts=ts, rec=rec, dS=dS, pred=pred)
        tres[name] = {
            "S_0": float(rec["S_det"][0]), "S_final": float(rec["S_det"][-1]),
            "S_ss": S_ss,
            "rho_bar_0": float(rec["rho_bar"][0]),
            "rho_bar_final": float(rec["rho_bar"][-1]),
            "frac_steps_dS_pos": frac_pos, "frac_steps_dS_neg": frac_neg,
            "frac_steps_S_moves_toward_S_ss": frac_toward,
            "S_overshoot_beyond_S_ss": float(np.max(np.abs(rec["S_det"] - S_ss))
                                             - abs(rec["S_det"][0] - S_ss)),
            "frac_steps_dD_ss_nonpositive": frac_D_nonpos,
            "D_ss_0": float(rec["D_ss"][0]), "D_ss_final": float(rec["D_ss"][-1]),
            "chainrule_R2": chain_r2, "chainrule_median_rel_resid": chain_resid,
            "dS_final_over_dS_max": float(abs(dS[-1]) / max(abs(dS).max(), 1e-30)),
            "T_corr_0": float(rec["T_corr"][0]), "T_corr_final": float(rec["T_corr"][-1]),
            "frac_steps_dT_pos": float(np.mean(dT[np.abs(dT) > 1e-9] > 0))
            if np.any(np.abs(dT) > 1e-9) else np.nan,
            "max_trace_err": float(rec["trace_err"].max()),
            "max_herm_err": float(rec["herm_err"].max()),
            "total_floored_eigs": int(rec["n_floored_eig"].sum()),
            "total_floored_vars": int(rec["n_floored_var"].sum()),
            "min_C_eig_over_traj": float(rec["lam_min"].min()),
        }
        print(f"      S: {rec['S_det'][0]:.4f} -> {rec['S_det'][-1]:.4f} (S_ss={S_ss:.4f}) | "
              f"dS>0 {frac_pos:.0%} / dS<0 {frac_neg:.0%} | toward S_ss {frac_toward:.0%} | "
              f"chain R2={chain_r2:.4f} | dD<=0 {frac_D_nonpos:.1%}")
    res["trajectories_baseline"] = tres

    res["stationarity"] = {
        "S_ss": S_ss, "finite": bool(np.isfinite(S_ss)),
        "min_eig_C_ss": ss["min_eig_C_k6"], "rho_bar_ss": ss["rho_bar_k6"],
        "dist_to_chaos_pole_in_S": S_ss,
        "interior_strict": bool(S_ss > 1e-6),
        "rho_bar_in_corridor_0p1_0p43": bool(0.10 < ss["rho_bar_k6"] < 0.43),
        "raw_ZZ_in_corridor": [bool(0.10 < x < 0.43) for x in ss["raw_abs_ZZ_per_rung"]],
    }

    # ------------------------------------------- (3) parameter grid, decay alpha
    print("\n[2] parameter grid (alpha = decay): gamma_M x g x alpha_scale")
    grid = []
    for g in [0.0, 0.5, 1.0]:
        for a_s in [0.5, 1.0, 2.0]:
            L0g, Lbfg = build_pieces(g=g, alpha_scale=a_s, alpha_channel="decay")
            for gm in [0.02, 0.05, 0.1, 0.2, 0.35, 0.5, 1.0, 2.0, 5.0]:
                r = steady_state(L0g, Lbfg, gm)
                s = summarize_state(r, f"decay g={g} a={a_s} gM={gm}")
                s.update(gamma_M=gm, g=g, alpha_scale=a_s, alpha_channel="decay")
                grid.append(s)
            print(f"    g={g:.1f} a={a_s:.1f}: S range "
                  f"[{min(x['S_det_k6'] for x in grid[-9:]):.4f}, "
                  f"{max(x['S_det_k6'] for x in grid[-9:]):.4f}]  "
                  f"rho_bar range [{min(x['rho_bar_k6'] for x in grid[-9:]):+.4f}, "
                  f"{max(x['rho_bar_k6'] for x in grid[-9:]):+.4f}]")
    res["grid_decay"] = grid

    mono = {}
    for g in [0.0, 0.5, 1.0]:
        for a_s in [0.5, 1.0, 2.0]:
            rows = [r for r in grid if r["g"] == g and r["alpha_scale"] == a_s]
            Sv = np.array([r["S_det_k6"] for r in rows])
            mono[f"g={g},a={a_s}"] = {
                "S_monotone_decreasing_in_gamma_M": bool(np.all(np.diff(Sv) < 0)),
                "frac_decreasing_steps": float(np.mean(np.diff(Sv) < 0)),
                "argmax_gamma_M": float(rows[int(np.argmax(Sv))]["gamma_M"]),
                "S_max": float(Sv.max()), "S_at_smallest_gamma_M": float(Sv[0]),
                "all_rho_bar_negative": bool(all(r["rho_bar_k6"] < 0 for r in rows)),
            }
    res["maintenance_monotonicity_decay"] = mono

    # -------------------------------- alpha as ALIGNMENT (correlation-writing)
    print("\n[3] alpha = pairwise ALIGNMENT (consensus). Does S then behave as a "
          "two-pole potential?")
    grid_a = []
    for chan, g in [("align", 0.5), ("align_all", 0.0)]:
        L0a, Lbfa = build_pieces(g=g, alpha_scale=1.0, alpha_channel=chan)
        print(f"    channel={chan}")
        print(f"      {'gamma_M':>8} {'S_det':>10} {'S_closed':>10} {'rho_bar':>9} "
              f"{'k_eff_pr':>9} {'k_eff_kish':>10} {'minEigC':>10} {'T_q':>8}")
        for gm in [0.01, 0.02, 0.05, 0.1, 0.2, 0.35, 0.5, 1.0, 2.0, 5.0]:
            r = steady_state(L0a, Lbfa, gm)
            s = summarize_state(r, f"{chan} gM={gm}")
            s.update(gamma_M=gm, g=g, alpha_scale=1.0, alpha_channel=chan)
            grid_a.append(s)
            print(f"      {gm:>8.2f} {s['S_det_k6']:>10.4f} "
                  f"{s['S_closed_from_rhobar_k6']:>10.4f} {s['rho_bar_k6']:>+9.4f} "
                  f"{s['k_eff_pr_k6']:>9.3f} {s['k_eff_kish_k6']:>10.3f} "
                  f"{s['min_eig_C_k6']:>10.2e} {s['T_corr_quantum']:>8.4f}")
    res["grid_align"] = grid_a

    for chan in ["align", "align_all"]:
        rows = [r for r in grid_a if r["alpha_channel"] == chan]
        Sv = np.array([r["S_det_k6"] for r in rows])
        rb = np.array([r["rho_bar_k6"] for r in rows])
        res.setdefault("maintenance_monotonicity_align", {})[chan] = {
            "S_monotone_decreasing_in_gamma_M": bool(np.all(np.diff(Sv) < 0)),
            "frac_decreasing_steps": float(np.mean(np.diff(Sv) < 0)),
            "S_at_smallest_gamma_M": float(Sv[0]), "S_at_largest_gamma_M": float(Sv[-1]),
            "rho_bar_at_smallest_gamma_M": float(rb[0]),
            "rho_bar_at_largest_gamma_M": float(rb[-1]),
            "all_rho_bar_positive": bool(np.all(rb > 0)),
            "gamma_M_with_rho_bar_in_corridor": [
                float(r["gamma_M"]) for r in rows if 0.10 < r["rho_bar_k6"] < 0.43],
            "max_rel_gap_S_det_vs_S_closed": float(np.nanmax(np.abs(
                np.array([r["S_det_k6"] for r in rows])
                - np.array([r["S_closed_from_rhobar_k6"] for r in rows]))
                / (np.array([r["S_det_k6"] for r in rows]) + 1e-12))),
        }

    # trajectories on the exchange-symmetric alignment model: the clean chain-rule test
    print("\n[4] trajectories on align_all (exchange-symmetric => C exactly uniform)")
    L0s, Lbfs = build_pieces(g=0.0, alpha_scale=1.0, alpha_channel="align_all")
    GM2 = 0.2
    Lsp2 = (L0s + GM2 * Lbfs).tocsr()
    rss2 = steady_state(L0s, Lbfs, GM2)
    ss2 = summarize_state(rss2, f"rho_ss(align_all, gM={GM2})")
    res["steady_state_align_all"] = ss2
    S_ss2 = ss2["S_det_k6"]
    print(f"    S_ss={S_ss2:.4f} rho_bar={ss2['rho_bar_k6']:+.4f} "
          f"k_eff_pr={ss2['k_eff_pr_k6']:.3f}")
    tres2 = {}
    for name, r0 in ics.items():
        rhos = integrate(Lsp2, r0, ts)
        rec = trace_traj(rhos, rss2)
        dS = np.gradient(rec["S_det"], ts)
        drb = np.gradient(rec["rho_bar"], ts)
        dD = np.gradient(rec["D_ss"], ts)
        pred = rec["dS_drho_closed"] * drb
        act = np.abs(dS) > 1e-6 * max(np.abs(dS).max(), 1e-30)
        mm = np.abs(dS) > 1e-3 * np.abs(dS).max()
        actD = np.abs(dD) > 1e-9 * max(np.abs(dD).max(), 1e-30)
        traj[f"align_all:{name}"] = dict(ts=ts, rec=rec, dS=dS, pred=pred)
        tres2[name] = {
            "S_0": float(rec["S_det"][0]), "S_final": float(rec["S_det"][-1]),
            "S_ss": S_ss2,
            "frac_steps_dS_pos": float(np.mean(dS[act] > 0)),
            "frac_steps_dS_neg": float(np.mean(dS[act] < 0)),
            "frac_steps_S_moves_toward_S_ss": float(np.mean(
                np.sign(dS[act]) == np.sign(S_ss2 - rec["S_det"][act]))),
            "frac_steps_dD_ss_nonpositive": float(np.mean(dD[actD] <= 0)),
            "chainrule_R2": r2(dS[mm], pred[mm]),
            "chainrule_median_rel_resid": float(np.median(
                np.abs(dS[mm] - pred[mm]) / (np.abs(dS[mm]) + 1e-30))),
            "max_S_closed_minus_S_det": float(np.nanmax(np.abs(
                rec["S_closed"] - rec["S_det"]))),
            "dS_final_over_dS_max": float(abs(dS[-1]) / max(abs(dS).max(), 1e-30)),
            "min_C_eig_over_traj": float(rec["lam_min"].min()),
            "total_floored_eigs": int(rec["n_floored_eig"].sum()),
        }
        print(f"      {name:<14} S: {rec['S_det'][0]:8.4f} -> {rec['S_det'][-1]:.4f} | "
              f"dS>0 {tres2[name]['frac_steps_dS_pos']:.0%} | toward S_ss "
              f"{tres2[name]['frac_steps_S_moves_toward_S_ss']:.0%} | chain R2="
              f"{tres2[name]['chainrule_R2']:.5f} | |S_closed-S_det|max="
              f"{tres2[name]['max_S_closed_minus_S_det']:.2e}")
    res["trajectories_align_all"] = tres2

    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(res, f, indent=2, default=float)
    print(f"\nwrote {os.path.join(HERE,'results.json')}")

    make_plots(traj, grid, grid_a, S_ss, S_ss2)


def make_plots(traj, grid, grid_a, S_ss, S_ss2):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:                                    # noqa: BLE001
        print(f"plotting skipped: {e}")
        return
    cols = {"maxmix": "tab:blue", "plus_product": "tab:green", "ghz_soft": "tab:red"}

    fig, ax = plt.subplots(2, 3, figsize=(16, 8))
    for nm in cols:
        d = traj[nm]
        ax[0, 0].plot(d["ts"], d["rec"]["S_det"], color=cols[nm], label=nm)
        ax[0, 1].plot(d["ts"], d["dS"], color=cols[nm])
        ax[0, 2].plot(d["ts"], d["rec"]["D_ss"], color=cols[nm])
        d2 = traj[f"align_all:{nm}"]
        ax[1, 0].plot(d2["ts"], d2["rec"]["S_det"], color=cols[nm], label=nm)
        ax[1, 1].plot(d2["ts"], d2["dS"], color=cols[nm])
        m = np.abs(d2["dS"]) > 1e-3 * np.abs(d2["dS"]).max()
        ax[1, 2].scatter(d2["pred"][m], d2["dS"][m], s=6, alpha=.5, color=cols[nm])
    ax[0, 0].axhline(S_ss, ls="--", c="k", lw=1, label="S(rho_ss)")
    ax[0, 0].set(title="BASELINE (alpha=decay): S along the flow", xlabel="t",
                 ylabel="S = -ln det C")
    ax[0, 0].legend(fontsize=7)
    ax[0, 1].axhline(0, ls="--", c="k", lw=1)
    ax[0, 1].set(title="dS/dt is NOT single-signed", xlabel="t", ylabel="dS/dt")
    ax[0, 2].set(title="D(rho||rho_ss): the true (Spohn) Lyapunov fn", xlabel="t",
                 yscale="log")
    ax[1, 0].axhline(S_ss2, ls="--", c="k", lw=1, label="S(rho_ss)")
    ax[1, 0].set(title="ALIGNMENT alpha: S along the flow", xlabel="t",
                 ylabel="S = -ln det C")
    ax[1, 0].legend(fontsize=7)
    ax[1, 1].axhline(0, ls="--", c="k", lw=1)
    ax[1, 1].set(title="dS/dt (alignment)", xlabel="t", ylabel="dS/dt")
    lim = ax[1, 2].get_xlim()
    ax[1, 2].plot(lim, lim, "k--", lw=1)
    ax[1, 2].set(title="chain rule: (dS/drho)(drho/dt) vs dS/dt",
                 xlabel="uniform-rho prediction", ylabel="actual dS/dt")
    for a in ax[:, :2].ravel():
        a.set_xscale("symlog", linthresh=1.0)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "trajectories.png"), dpi=140)

    fig2, ax2 = plt.subplots(1, 3, figsize=(15, 4.2))
    base = [r for r in grid if r["g"] == 0.5 and r["alpha_scale"] == 1.0]
    for lbl, rows, c in [("alpha=decay (original)", base, "tab:red"),
                         ("alpha=align (rung+chain)",
                          [r for r in grid_a if r["alpha_channel"] == "align"], "tab:blue"),
                         ("alpha=align_all (uniform)",
                          [r for r in grid_a if r["alpha_channel"] == "align_all"], "tab:green")]:
        gm = [r["gamma_M"] for r in rows]
        ax2[0].plot(gm, [max(r["S_det_k6"], 1e-6) for r in rows], "o-", c=c, label=lbl)
        ax2[1].plot(gm, [r["rho_bar_k6"] for r in rows], "o-", c=c, label=lbl)
        ax2[2].plot(gm, [r["k_eff_pr_k6"] for r in rows], "o-", c=c, label=lbl)
    ax2[0].set(xscale="log", yscale="log", xlabel="gamma_M (maintenance)",
               ylabel="S(rho_ss)", title="S vs maintenance")
    ax2[1].axhline(0.43, ls="--", c="r", lw=1)
    ax2[1].axhline(0.10, ls="--", c="r", lw=1)
    ax2[1].axhline(0.0, ls=":", c="k", lw=1)
    ax2[1].set(xscale="log", xlabel="gamma_M", ylabel="rho_bar(rho_ss)",
               title="corridor band 0.1-0.43 (dashed)")
    ax2[2].set(xscale="log", xlabel="gamma_M", ylabel="k_eff (participation)",
               title="effective diversity of rho_ss")
    for a in ax2:
        a.legend(fontsize=7)
    fig2.tight_layout()
    fig2.savefig(os.path.join(HERE, "maintenance_sweep.png"), dpi=140)
    print("wrote trajectories.png, maintenance_sweep.png")


if __name__ == "__main__":
    main()
