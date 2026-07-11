"""
maintenance.py — S5, the maintenance reading. Free fermionic dissipative
(Lindblad) dynamics on the correlation matrix, instantiating the corridor
dynamics dρ/dt = α − γ·M (Core/Dynamics.lean, Piece 2).

Lindblad on Gaussian states keeps Gaussianity: the one-body correlation matrix
G_ij = <a_i^dag a_j> obeys a CLOSED linear equation. For:
  * Hamiltonian h (Hermitian):            dG/dt |_H   = i[h, G]  (unitary; preserves nu-spectrum)
  * pure dephasing rate gamma (L_i=√γ n_i): dG_ij/dt = -gamma (1-δ_ij) G_ij  (decays coherence)
  * coherence maintenance rate alpha toward pattern P (a driven/feedback reservoir
    injecting the coordinating coherence): dG/dt |_maint = alpha (P - G)_offdiag
These combine. We use the uniform family so the reading ties directly to S1/S2:
G(t) stays in the family with collective order parameter s(t), and the scalar
equation reduces EXACTLY to
        ds/dt = alpha (s_target - s) - gamma s = alpha s_target - (alpha+gamma) s,
the corridor equation. Steady state s* = alpha s_target / (alpha + gamma),
bounded by the EXCLUSION cap s<=1.

Demonstrations:
  (D1) dephasing alone (alpha=0): s(t)=s0 e^{-gamma t} -> 0. Free dissipation
       selects the CHAOS pole (I_F -> 0). Validated against closed form.
  (D2) maintenance on: NESS at finite s* in the interior (corridor). I_F held
       off both poles by the alpha term — the gamma·M work.
  (D3) over-drive (s_target -> 1, alpha>>gamma): s* -> 1, collective mode freezes
       (nu0 -> 1) — the RIGIDITY pole, capped by exclusion (I_F -> ln2, not inf).
"""

import json
import numpy as np
from scipy.integrate import solve_ivp
from fermionic_core import LN2, h_nu, S_F_from_nu
from uniform_family import family_nu, multi_information_family

OUT = {}


def s_ode(t, s, alpha, gamma, s_target):
    return [alpha * (s_target - s[0]) - gamma * s[0]]


def integrate_s(s0, alpha, gamma, s_target, T=20.0, n=400):
    sol = solve_ivp(s_ode, (0, T), [s0], args=(alpha, gamma, s_target),
                    t_eval=np.linspace(0, T, n), rtol=1e-9, atol=1e-12)
    return sol.t, sol.y[0]


def full_matrix_dephasing_check(k=8, s0=0.6, gamma=0.7, T=5.0):
    """Validate the family reduction: integrate the FULL G-matrix ODE under pure
       dephasing and confirm it stays in the family with s(t)=s0 e^{-gamma t}."""
    c0 = s0 / (2 * (k - 1))
    G0 = 0.5 * np.eye(k) + c0 * (np.ones((k, k)) - np.eye(k))
    off = (np.ones((k, k)) - np.eye(k))

    def dG(t, gvec):
        G = gvec.reshape(k, k)
        dGm = -gamma * off * G     # dephasing: off-diagonals decay
        return dGm.reshape(-1)

    sol = solve_ivp(dG, (0, T), G0.reshape(-1),
                    t_eval=np.linspace(0, T, 50), rtol=1e-10, atol=1e-12)
    # recover s(t) from an off-diagonal element: G_ij = c(t) = s(t)/(2(k-1))
    Gt = sol.y[:, -1].reshape(k, k)
    c_t = Gt[0, 1]
    s_num = c_t * 2 * (k - 1)
    s_closed = s0 * np.exp(-gamma * T)
    return {"s_numeric_full_matrix": float(s_num),
            "s_closed_form": float(s_closed),
            "err": float(abs(s_num - s_closed))}


if __name__ == "__main__":
    k = 100
    print("== S5 maintenance: corridor dynamics on the fermionic covariance ==")

    # validate the family reduction against the full-matrix ODE
    chk = full_matrix_dephasing_check()
    OUT["family_reduction_check"] = chk
    print(f"\n[reduction check] full-matrix dephasing s(T)={chk['s_numeric_full_matrix']:.6f} "
          f"vs closed form {chk['s_closed_form']:.6f}  err={chk['err']:.2e}")

    # D1: dephasing alone -> chaos pole
    t, s = integrate_s(s0=0.6, alpha=0.0, gamma=0.5, s_target=0.9)
    IF = np.array([multi_information_family(k, si)[0] for si in s])
    OUT["D1_dephasing_only"] = {"s_final": float(s[-1]), "IF_final": float(IF[-1]),
                                "selects": "chaos pole (I_F -> 0)"}
    print(f"\n[D1] dephasing only (alpha=0,gamma=0.5): s: 0.60 -> {s[-1]:.4f}, "
          f"I_F: {IF[0]:.4f} -> {IF[-1]:.4f}   => CHAOS pole")

    # D2: maintenance on -> NESS in the corridor
    for (alpha, gamma, st) in [(0.5, 0.5, 0.6), (0.8, 0.4, 0.7), (0.3, 0.9, 0.9)]:
        t, s = integrate_s(s0=0.05, alpha=alpha, gamma=gamma, s_target=st)
        sstar = alpha * st / (alpha + gamma)
        IFstar = multi_information_family(k, s[-1])[0]
        rec = {"alpha": alpha, "gamma": gamma, "s_target": st,
               "s_star_numeric": float(s[-1]), "s_star_closed": float(sstar),
               "I_F_star": float(IFstar)}
        OUT.setdefault("D2_maintenance_NESS", []).append(rec)
        print(f"[D2] alpha={alpha} gamma={gamma} s_t={st}: NESS s*={s[-1]:.4f} "
              f"(closed {sstar:.4f}), I_F*={IFstar:.4f}  => corridor interior")

    # D3: over-drive -> rigidity pole (capped by exclusion)
    t, s = integrate_s(s0=0.1, alpha=50.0, gamma=0.1, s_target=0.9999)
    IFr = multi_information_family(k, s[-1])[0]
    cap = k * LN2 - (k - 1) * float(h_nu(1.0 / (k - 1)))
    OUT["D3_overdrive"] = {"s_final": float(s[-1]), "I_F_final": float(IFr),
                           "I_F_exclusion_cap": float(cap),
                           "selects": "rigidity pole (nu0->1), CAPPED at ~ln2"}
    print(f"\n[D3] over-drive (alpha>>gamma, s_t->1): s -> {s[-1]:.5f}, "
          f"I_F -> {IFr:.4f}  (exclusion cap {cap:.4f})  => RIGIDITY pole, capped")

    print("\nSummary: free dissipation (dephasing) selects the CHAOS pole; the "
          "alpha maintenance term holds a NESS in the corridor; over-drive reaches "
          "the RIGIDITY pole but exclusion caps I_F at ~ln2 (no divergence).")

    with open("maintenance_results.json", "w") as f:
        json.dump(OUT, f, indent=2, default=float)
    print("wrote maintenance_results.json")
