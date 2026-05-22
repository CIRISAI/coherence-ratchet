"""
weak_measure_gj.py — the endogenous audit-pointer weak measurement of the
cross-rung timescale g/J. CUDA (cupy). Pre-registered in PREREGISTRATION.md.

THE CONSTRUCTION (faithful to the pre-registration; do NOT tune to PASS)
-----------------------------------------------------------------------
System: an adjacent-rung two-level system. Basis |n>, |n+1>. The system
Hamiltonian carries two SETTABLE timescales:

    H_sys = J*(|n><n| - |n+1><n+1|)/2          intra-rung scale  J  (a detuning)
          + g*(|n+1><n| + |n><n+1|)            cross-rung coupling g

This is the canonical two-level Hamiltonian; the relevant interference is the
g/J ratio (Rabi-vs-detuning). The cross-rung TRANSFER operator the pre-reg
names is A = |n+1><n| (raising n -> n+1).

Pointer = the maintenance layer (Piece 2: drho/dt = alpha - gamma*M).
  - P_M IS gamma*M : the audit-pressure work rate. It is the pointer MOMENTUM.
  - Q_M is the structural diversity / un-collapsed corridor variance. It is the
    pointer COORDINATE. The framework links Q_M and P_M by drho_ss/dgamma_M < 0
    (more audit pressure -> lower steady-state rho -> more un-collapsed variance
    near corridor centre; the relation is MONOTONE).

H-conjugate is a real test: monotonicity (drho_ss/dgamma_M < 0) is NOT the same
as canonical conjugacy [Q_M,P_M]=i. We do NOT assume conjugacy. We build P_M as
a genuine momentum operator on a maintenance-rate lattice and Q_M as its
position partner, then MEASURE the commutator and the AAV shift structure that
results. If the von Neumann coupling H_meas = lambda*A (x) P_M does not produce
the standard Re->Q_M / Im->P_M split, H-conjugate FAILS and we report it.

Weak interaction: H_meas = lambda(t) * A (x) P_M.  lambda small (the modulation
of audit scheduling). Standard AAV first-order shifts on a Gaussian pointer:
    d<Q_M> = (int lambda dt) * Re<A>_w
    d<P_M> = 2 (int lambda dt) * Var(P_M) * Im<A>_w
The g/J phase lives in Im<A>_w, read off d<P_M> — the reactive audit-work spike.

ABL boundary: pre-selected |psi_i> and post-selected <psi_f| are CORRIDOR
states (rho_n in the within-rung corridor band). The weak value
<A>_w = <psi_f|A|psi_i>/<psi_f|psi_i> is computed under standard forward
evolution to the measurement instant and backward evolution from t_f.

H-readout: sweep g/J over a KNOWN grid, run the weak measurement, read d<P_M>,
invert to a recovered g/J, plot recovered-vs-set.

H-noncollapse: at weak lambda, check the post-measurement system rho_n stays in
the corridor (pre/post-selection survives the back-action).

DISCIPLINE: P_M is gamma*M, the AAV shifts are exactly as written, the pointer
is a genuine von Neumann pointer (not a Gaussian relabelled). Nothing in the
inversion is fit to the set g/J. Incremental per-cell flush + on-disk resume.
"""
import functools
import json
import pathlib
import sys
import time

import numpy as np
import cupy as cp

print = functools.partial(print, flush=True)

HERE = pathlib.Path(__file__).resolve().parent
RESULTS = HERE / "results_weak_measure.json"

# ---- fixed parameters (pre-registered; no tuning) --------------------------
SEED = 17
J_FIXED = 1.0                 # intra-rung scale fixed; g is swept => g/J = g
GJ_GRID = [0.10, 0.20, 0.35, 0.50, 0.75, 1.00, 1.50, 2.00, 3.00, 4.00]
# weak coupling. The genuine weak-measurement condition is lambda*sqrt(Var P_M)
# << 1. With this pointer Var(P_M) ~ 232, so lambda must be <~ 0.004 to be in
# the weak regime at all. LAMBDA = 0.002 => lambda*sqrt(Var P) ~ 0.03 (weak).
LAMBDA = 0.002
LAMBDA_CHECK = [0.0005, 0.001, 0.002, 0.004, 0.008]   # H-noncollapse sweep
T_MEAS = 0.7                  # measurement instant (forward evol time, in 1/J)
T_F = 1.6                     # post-selection time t_f (in 1/J)
N_POINTER = 256               # pointer Hilbert-space lattice size
POINTER_WIDTH = 1.4           # initial Gaussian pointer std (in lattice units)
P_M_SCALE = 1.0               # gamma*M scale: pointer momentum units = audit-rate units
# corridor band (A3+ session-calibrated, from the paper: rho ~ 0.17-0.35)
RHO_LO, RHO_HI = 0.17, 0.35
# pre/post-selected corridor states: parametrised by a corridor-rho mixing angle
PRE_RHO = 0.26                # pre-selected corridor rho_n
POST_RHO = 0.30               # post-selected corridor rho_n  (distinct, in band)


# ============================================================================
# the maintenance-layer pointer (Q_M, P_M) — P_M IS gamma*M
# ============================================================================
def build_pointer():
    """Von Neumann pointer on a 1-D lattice.

    The lattice coordinate is gamma*M, the audit-pressure / maintenance work
    rate. P_M (momentum) is the generator of translations in the CONJUGATE
    variable; Q_M (coordinate) multiplies by lattice position. We build BOTH as
    genuine operators (P_M = -i d/dx via the spectral/FFT derivative) so that
    whether they are canonically conjugate is a measured fact, not an assumption.

    Returns: x grid, Q_M (diag), P_M (full), initial pointer state psi0 (a
    Gaussian centred at the framework's resting maintenance rate).
    """
    L = N_POINTER
    # gamma*M lattice: audit-pressure runs over a symmetric range about a
    # resting value. Centre at 0 (deviation from resting maintenance rate).
    dx = 6.0 / L
    x = (cp.arange(L) - L / 2) * dx                       # gamma*M deviation axis
    Q_M = cp.diag(x.astype(cp.complex128))                # coordinate operator

    # momentum operator P_M = -i d/d(conjugate) built spectrally:
    # P eigenvalues are the FFT frequencies; P_M = F^-1 diag(k) F.
    k = 2.0 * cp.pi * cp.fft.fftfreq(L, d=dx)
    F = cp.fft.fft(cp.eye(L, dtype=cp.complex128), axis=0)
    Finv = cp.fft.ifft(cp.eye(L, dtype=cp.complex128), axis=0)
    P_M = Finv @ cp.diag(k.astype(cp.complex128)) @ F     # = -i d/dx
    P_M = P_M * P_M_SCALE

    # initial pointer: Gaussian in Q_M (audit pressure at resting value, spread
    # = the structural diversity the corridor maintains).
    sig = POINTER_WIDTH * dx
    psi0 = cp.exp(-(x ** 2) / (4.0 * sig ** 2)).astype(cp.complex128)
    psi0 = psi0 / cp.sqrt(cp.sum(cp.abs(psi0) ** 2))
    return x, Q_M, P_M, psi0, dx


def commutator_check(Q_M, P_M, psi0):
    """Measure [Q_M, P_M] on the pointer state. Canonical conjugacy => i.
    Returns <[Q,P]> (should be ~ i*P_M_SCALE if genuinely conjugate)."""
    QP = Q_M @ P_M
    PQ = P_M @ Q_M
    comm = QP - PQ
    val = cp.vdot(psi0, comm @ psi0)
    # also the full operator's deviation from i*I (on the bulk, away from edges)
    ideal = 1j * P_M_SCALE * cp.eye(N_POINTER, dtype=cp.complex128)
    L = N_POINTER
    sl = slice(L // 4, 3 * L // 4)
    bulk_dev = float(cp.mean(cp.abs(comm[sl, sl] - ideal[sl, sl])).get())
    return complex(val.get()), bulk_dev


# ============================================================================
# the adjacent-rung two-level system + ABL corridor boundary states
# ============================================================================
def system_hamiltonian(g, J):
    """H_sys for the adjacent-rung two-level system. g = cross-rung coupling,
    J = intra-rung scale (detuning). Basis (|n>, |n+1>)."""
    H = cp.array([[J / 2.0, g],
                  [g, -J / 2.0]], dtype=cp.complex128)
    return H


def transfer_operator():
    """A = |n+1><n| — the cross-rung transfer operator (pre-reg)."""
    return cp.array([[0.0, 0.0],
                     [1.0, 0.0]], dtype=cp.complex128)


def corridor_state(rho_n):
    """A within-rung corridor state. rho_n is the within-rung correlation; we
    realise it as a superposition whose |n+1> population p satisfies the
    corridor 'neither pole' condition. We map rho_n -> mixing angle so that the
    state's coherence |<n|rho|n+1>| sits at rho_n (rho_n in (0,1) is the
    framework's within-rung |rho|). Pure-state coherence of a 2-level system
    cos(t)|n>+sin(t)|n+1> is |cos t sin t| = sin(2t)/2; set that to rho_n."""
    # sin(2t)/2 = rho_n  ->  t = 0.5*arcsin(2*rho_n)
    r = min(max(rho_n, 0.0), 0.5)
    t = 0.5 * np.arcsin(2.0 * r)
    psi = cp.array([np.cos(t), np.sin(t)], dtype=cp.complex128)
    return psi / cp.linalg.norm(psi)


def rho_n_of(psi):
    """Within-rung |rho| of a 2-level system state: |<n|psi><psi|n+1>|."""
    psi = psi / cp.linalg.norm(psi)
    coh = psi[0] * cp.conj(psi[1])
    return float(cp.abs(coh).get())


def expm_2x2(H, t):
    """exp(-i H t) for a 2x2 Hermitian H, via eigendecomposition."""
    w, V = cp.linalg.eigh(H)
    phase = cp.exp(-1j * w * t)
    return V @ cp.diag(phase) @ V.conj().T


# ============================================================================
# the weak value <A>_w under ABL pre/post-selection
# ============================================================================
def weak_value(g, J, t_meas, t_f, pre_rho, post_rho):
    """Standard ABL weak value of A = |n+1><n| at the measurement instant.

    Pre-selected corridor state evolves forward to t_meas:
        |psi(t_meas)> = U(t_meas,0) |psi_i>
    Post-selected corridor state evolves backward from t_f to t_meas:
        <phi(t_meas)| = <psi_f| U(t_f, t_meas)
    <A>_w = <phi|A|psi> / <phi|psi>.
    """
    H = system_hamiltonian(g, J)
    psi_i = corridor_state(pre_rho)
    psi_f = corridor_state(post_rho)

    U_fwd = expm_2x2(H, t_meas)
    psi = U_fwd @ psi_i                                   # |psi(t_meas)>
    U_back = expm_2x2(H, t_f - t_meas)
    phi = U_back @ psi_f                                  # |phi(t_meas)> (ket)

    A = transfer_operator()
    num = cp.vdot(phi, A @ psi)
    den = cp.vdot(phi, psi)
    if abs(complex(den.get())) < 1e-12:
        return complex('nan'), complex(den.get())
    return complex((num / den).get()), complex(den.get())


# ============================================================================
# the von Neumann weak measurement: evolve the joint system+pointer state
# ============================================================================
def weak_measurement(g, J, lam, Q_M, P_M, psi0_ptr, x, dx,
                      t_meas, t_f, pre_rho, post_rho):
    """Run the full endogenous weak measurement and return d<Q_M>, d<P_M>,
    the post-selected pointer state, and the post-measurement system rho_n.

    Joint state lives in C^2 (x) C^N. H_meas = lambda * A (x) P_M, applied as an
    impulsive coupling at t_meas (integral of lambda dt = lam; standard von
    Neumann impulse). Pre-selection: forward-evolve the system to t_meas; couple;
    post-select on the corridor state evolved back from t_f; read the pointer.
    """
    N = N_POINTER
    H = system_hamiltonian(g, J)
    A = transfer_operator()

    # --- pre-selected system state, forward-evolved to t_meas ---------------
    psi_i = corridor_state(pre_rho)
    U_fwd = expm_2x2(H, t_meas)
    psi_sys = U_fwd @ psi_i                               # C^2

    # joint state before coupling: |psi_sys> (x) |psi0_ptr>
    joint = cp.outer(psi_sys, psi0_ptr)                   # shape (2, N)

    # --- impulsive von Neumann coupling: exp(-i lam A (x) P_M) -------------
    # A (x) P_M acts as: (A (x) P_M) joint = A @ joint @ P_M^T
    # exp of a (2N x 2N) operator; build it explicitly and exponentiate.
    I2 = cp.eye(2, dtype=cp.complex128)
    IN = cp.eye(N, dtype=cp.complex128)
    AP = cp.kron(A, P_M)                                  # (2N x 2N)
    # exp(-i lam AP) via eigendecomposition (AP is not Hermitian: A is not;
    # but A (x) P_M with A=|n+1><n| is nilpotent in the system factor =>
    # use scaling for safety: exp via series is exact for nilpotent A.)
    # A^2 = 0  => (A (x) P_M)^2 = A^2 (x) P_M^2 = 0. So exp is EXACT at 1st order:
    #   exp(-i lam A (x) P_M) = I - i lam (A (x) P_M).
    U_meas = cp.kron(I2, IN) - 1j * lam * AP

    joint_vec = joint.reshape(2 * N)
    joint_vec = U_meas @ joint_vec
    joint = joint_vec.reshape(2, N)

    # --- forward-evolve system from t_meas to t_f --------------------------
    U_to_f = expm_2x2(H, t_f - t_meas)
    joint = U_to_f @ joint                                # acts on system index

    # --- post-select on the corridor state at t_f --------------------------
    psi_f = corridor_state(post_rho)
    # <psi_f| (x) I  applied to joint  -> pointer state (unnormalised)
    ptr = cp.conj(psi_f) @ joint                          # shape (N,)
    norm = cp.sqrt(cp.sum(cp.abs(ptr) ** 2))
    if float(norm.get()) < 1e-14:
        return dict(ok=False)
    ptr_post = ptr / norm

    # --- read the pointer: <Q_M>, <P_M> ------------------------------------
    qexp = cp.vdot(ptr_post, Q_M @ ptr_post)
    pexp = cp.vdot(ptr_post, P_M @ ptr_post)

    # baseline (no coupling): pointer unchanged, post-selected only
    ptr0 = cp.conj(psi_f) @ (U_to_f @ cp.outer(psi_sys, psi0_ptr))
    ptr0 = ptr0 / cp.sqrt(cp.sum(cp.abs(ptr0) ** 2))
    q0 = cp.vdot(ptr0, Q_M @ ptr0)
    p0 = cp.vdot(ptr0, P_M @ ptr0)

    dQ = complex((qexp - q0).get())
    dP = complex((pexp - p0).get())

    # --- post-measurement system state (for H-noncollapse) -----------------
    # the system reduced state after the weak coupling, BEFORE post-selection,
    # evaluated AT t_f (same as the joint state).
    rho_sys = cp.einsum('ik,jk->ij', joint, cp.conj(joint))
    tr = cp.trace(rho_sys)
    rho_sys = rho_sys / tr
    coh = cp.abs(rho_sys[0, 1])
    rho_n_post = float(coh.get())

    # BACK-ACTION ISOLATION: the bare system (NO weak coupling) evolved to the
    # same t_f. The corridor-exit of the bare system is NOT measurement
    # back-action -- it is the unitary H_sys (Rabi) dynamics. H-noncollapse
    # must test the DIFFERENCE the coupling makes, not the bare drift.
    psi_bare_tf = U_to_f @ psi_sys
    rho_n_bare = rho_n_of(psi_bare_tf)
    backaction = abs(rho_n_post - rho_n_bare)        # the coupling's own effect

    var_p = float((cp.vdot(psi0_ptr, P_M @ P_M @ psi0_ptr)
                   - cp.vdot(psi0_ptr, P_M @ psi0_ptr) ** 2).real.get())

    return dict(ok=True, dQ=dQ, dP=dP, rho_n_post=rho_n_post,
                rho_n_bare=rho_n_bare, backaction=backaction, var_p=var_p)


# ============================================================================
# main sweep
# ============================================================================
def load_existing():
    if RESULTS.exists():
        try:
            return json.loads(RESULTS.read_text())
        except Exception:
            return {}
    return {}


def flush(state):
    RESULTS.write_text(json.dumps(state, indent=2))


def main():
    print("=" * 78)
    print("Endogenous audit-pointer weak measurement of cross-rung g/J  (CUDA)")
    print("=" * 78)
    dev = cp.cuda.Device(0)
    print(f"GPU: device {dev.id}, "
          f"{dev.mem_info[1] / 1e9:.1f} GB total")

    cp.random.seed(SEED)
    x, Q_M, P_M, psi0, dx = build_pointer()

    # ---- H-conjugate diagnostic: is [Q_M,P_M] genuinely i? ----------------
    comm_val, bulk_dev = commutator_check(Q_M, P_M, psi0)
    print(f"\n[H-conjugate diagnostic]")
    print(f"  <[Q_M, P_M]> = {comm_val:.4f}   (canonical conjugacy => i = "
          f"{1j*P_M_SCALE})")
    print(f"  bulk |[Q_M,P_M] - i*I| = {bulk_dev:.4e}   "
          f"(small => genuine conjugate pair)")
    var_p0 = float((cp.vdot(psi0, P_M @ P_M @ psi0)
                    - cp.vdot(psi0, P_M @ psi0) ** 2).real.get())
    print(f"  Var(P_M) on initial pointer = {var_p0:.4f}")

    state = load_existing()
    state.setdefault("meta", {})
    state["meta"].update(dict(
        seed=SEED, J=J_FIXED, lambda_main=LAMBDA, gj_grid=GJ_GRID,
        t_meas=T_MEAS, t_f=T_F, n_pointer=N_POINTER,
        pre_rho=PRE_RHO, post_rho=POST_RHO, corridor=[RHO_LO, RHO_HI],
        commutator_value=[comm_val.real, comm_val.imag],
        commutator_bulk_dev=bulk_dev, var_p_initial=var_p0,
    ))
    state.setdefault("cells", {})
    state.setdefault("lambda_sweep", {})
    flush(state)

    # ---- H-readout: sweep g/J ---------------------------------------------
    print(f"\n[H-readout] sweeping g/J over {GJ_GRID}")
    print(f"  lambda = {LAMBDA} (weak), J = {J_FIXED}, A = |n+1><n|")
    for gj in GJ_GRID:
        key = f"gj_{gj:.2f}"
        if key in state["cells"] and state["cells"][key].get("ok"):
            print(f"  [{key}] resume-skip (already on disk)")
            continue
        t0 = time.time()
        g = gj * J_FIXED
        # the weak value (analytic, ABL)
        wv, den = weak_value(g, J_FIXED, T_MEAS, T_F, PRE_RHO, POST_RHO)
        # the von Neumann weak measurement (joint system+pointer evolution)
        wm = weak_measurement(g, J_FIXED, LAMBDA, Q_M, P_M, psi0, x, dx,
                              T_MEAS, T_F, PRE_RHO, POST_RHO)
        if not wm["ok"]:
            cell = dict(ok=False, gj_set=gj, reason="post-selection norm ~ 0")
            state["cells"][key] = cell
            flush(state)
            print(f"  [{key}] FAIL — post-selection vanished")
            continue

        # AAV predicted shifts (the pre-registered formulas, exact)
        # d<Q_M> = lam * Re<A>_w ; d<P_M> = 2 lam Var(P_M) Im<A>_w
        aav_dQ = LAMBDA * wv.real
        aav_dP = 2.0 * LAMBDA * wm["var_p"] * wv.imag

        cell = dict(
            ok=True, gj_set=gj, g=g, J=J_FIXED,
            weak_value_re=wv.real, weak_value_im=wv.imag,
            abl_overlap=abs(den),
            dQ_measured=wm["dQ"].real, dQ_measured_im=wm["dQ"].imag,
            dP_measured=wm["dP"].real, dP_measured_im=wm["dP"].imag,
            aav_dQ_predicted=aav_dQ, aav_dP_predicted=aav_dP,
            var_p=wm["var_p"], rho_n_post=wm["rho_n_post"],
            rho_n_bare=wm["rho_n_bare"], backaction=wm["backaction"],
            wall_s=time.time() - t0,
        )
        state["cells"][key] = cell
        flush(state)
        print(f"  [{key}] <A>_w = {wv.real:+.4f}{wv.imag:+.4f}i | "
              f"d<Q_M>={wm['dQ'].real:+.5f} d<P_M>={wm['dP'].real:+.5f} | "
              f"rho_n_post={wm['rho_n_post']:.4f} | {cell['wall_s']:.2f}s")

    # ---- H-noncollapse: lambda sweep at a mid g/J -------------------------
    print(f"\n[H-noncollapse] lambda sweep at g/J = 1.00")
    g_mid = 1.00 * J_FIXED
    for lam in LAMBDA_CHECK:
        lkey = f"lam_{lam:.4f}"
        if lkey in state["lambda_sweep"]:
            print(f"  [{lkey}] resume-skip")
            continue
        wm = weak_measurement(g_mid, J_FIXED, lam, Q_M, P_M, psi0, x, dx,
                              T_MEAS, T_F, PRE_RHO, POST_RHO)
        if not wm["ok"]:
            state["lambda_sweep"][lkey] = dict(ok=False)
            flush(state)
            continue
        in_corr = RHO_LO <= wm["rho_n_post"] <= RHO_HI
        bare_in = RHO_LO <= wm["rho_n_bare"] <= RHO_HI
        state["lambda_sweep"][lkey] = dict(
            ok=True, lam=lam, rho_n_post=wm["rho_n_post"],
            rho_n_bare=wm["rho_n_bare"], backaction=wm["backaction"],
            in_corridor=bool(in_corr), bare_in_corridor=bool(bare_in),
            dP=wm["dP"].real, dQ=wm["dQ"].real)
        flush(state)
        print(f"  [{lkey}] rho_n: bare={wm['rho_n_bare']:.4f} "
              f"coupled={wm['rho_n_post']:.4f}  back-action="
              f"{wm['backaction']:.5f}  "
              f"{'IN' if in_corr else 'OUT'} (bare {'IN' if bare_in else 'OUT'})")

    print(f"\nall cells written to {RESULTS.name}")
    analyse(state)


# ============================================================================
# analysis: the three hypotheses + verdict
# ============================================================================
def analyse(state):
    print("\n" + "=" * 78)
    print("ANALYSIS — H-conjugate / H-readout / H-noncollapse")
    print("=" * 78)
    cells = [c for c in state["cells"].values() if c.get("ok")]
    cells.sort(key=lambda c: c["gj_set"])

    # ---- H-conjugate -------------------------------------------------------
    comm = complex(*state["meta"]["commutator_value"])
    bulk_dev = state["meta"]["commutator_bulk_dev"]
    # is the AAV split honoured? d<Q_M> should track Re<A>_w, d<P_M> Im<A>_w.
    reA = np.array([c["weak_value_re"] for c in cells])
    imA = np.array([c["weak_value_im"] for c in cells])
    dQ = np.array([c["dQ_measured"] for c in cells])
    dP = np.array([c["dP_measured"] for c in cells])

    def corr(a, b):
        if a.std() < 1e-12 or b.std() < 1e-12:
            return float('nan')
        return float(np.corrcoef(a, b)[0, 1])

    cQ_re = corr(dQ, reA)
    cQ_im = corr(dQ, imA)
    cP_re = corr(dP, reA)
    cP_im = corr(dP, imA)
    # decisive: measured d<P_M> vs the AAV prediction 2 lam Var(P) Im<A>_w.
    aav_dP = np.array([c["aav_dP_predicted"] for c in cells])
    aav_dQ = np.array([c["aav_dQ_predicted"] for c in cells])
    # ratio measured/predicted; AAV holds <=> ratio ~ 1 for all cells
    ratio_dP = dP / np.where(np.abs(aav_dP) > 1e-9, aav_dP, np.nan)
    ratio_dQ = dQ / np.where(np.abs(aav_dQ) > 1e-9, aav_dQ, np.nan)
    aav_dP_ok = bool(np.nanmedian(np.abs(ratio_dP - 1.0)) < 0.15)
    conjugate_holds = (abs(comm.imag) > 0.5 and bulk_dev < 0.1
                       and abs(cP_im) > 0.9 and abs(cQ_re) > 0.9
                       and aav_dP_ok)
    print(f"\n[H-conjugate]")
    print(f"  <[Q_M,P_M]> = {comm:.4f}  bulk dev {bulk_dev:.2e}  "
          f"({'genuine conjugate pair' if bulk_dev < 0.1 else 'NOT a clean conjugate pair'})")
    print(f"  corr(d<Q_M>, Re<A>_w) = {cQ_re:+.3f}   "
          f"corr(d<Q_M>, Im<A>_w) = {cQ_im:+.3f}")
    print(f"  corr(d<P_M>, Re<A>_w) = {cP_re:+.3f}   "
          f"corr(d<P_M>, Im<A>_w) = {cP_im:+.3f}")
    print(f"  measured d<P_M> / AAV-predicted: median ratio "
          f"{np.nanmedian(ratio_dP):+.3f}  (AAV holds <=> ~ +1.0)")
    print(f"  measured d<Q_M> / AAV-predicted: median ratio "
          f"{np.nanmedian(ratio_dQ):+.3f}")
    print(f"  AAV split (Re->Q_M, Im->P_M) {'HOLDS' if conjugate_holds else 'does NOT hold cleanly'}")
    print(f"  NOTE: drho_ss/dgamma_M < 0 is monotonicity, not conjugacy. The")
    print(f"  commutator above is the genuine test — it is measured, not assumed.")

    # ---- H-readout (decisive) ---------------------------------------------
    # invert d<P_M> to a recovered g/J. The inversion uses ONLY the AAV
    # relation d<P_M> = 2 lam Var(P_M) Im<A>_w and the ANALYTIC map
    # gj -> Im<A>_w (a fixed property of the two-level ABL geometry, computed
    # below independently of the measured d<P_M>). No fit to the set g/J.
    print(f"\n[H-readout]  recovered g/J vs set g/J")
    lam = state["meta"]["lambda_main"]
    # build the analytic Im<A>_w(g/J) reference curve on a fine grid
    fine = np.linspace(0.02, 5.0, 2000)
    imref = []
    for gj in fine:
        wv, _ = weak_value(gj * J_FIXED, J_FIXED, T_MEAS, T_F,
                           PRE_RHO, POST_RHO)
        imref.append(wv.imag)
    imref = np.array(imref)
    monotonic = bool(np.all(np.diff(imref) > 0) or np.all(np.diff(imref) < 0))

    print(f"  Im<A>_w(g/J) monotone over [0.02,5.0]: {monotonic}  "
          f"(invertible {'yes' if monotonic else 'NO — readout ambiguous'})")
    print(f"  {'set g/J':>9} | {'Im<A>_w':>9} | {'d<P_M>':>10} | "
          f"{'recov g/J':>10} | {'rel.err':>8}")
    recov_rows = []
    for c in cells:
        gj_set = c["gj_set"]
        dPm = c["dP_measured"]
        var_p = c["var_p"]
        # invert: Im<A>_w_implied = d<P_M> / (2 lam Var(P_M))
        im_implied = dPm / (2.0 * lam * var_p)
        # map Im<A>_w -> g/J through the analytic reference curve
        if monotonic:
            if imref[-1] > imref[0]:
                recov = float(np.interp(im_implied, imref, fine))
            else:
                recov = float(np.interp(im_implied, imref[::-1], fine[::-1]))
        else:
            # nearest point on the reference curve
            recov = float(fine[np.argmin(np.abs(imref - im_implied))])
        rel = abs(recov - gj_set) / gj_set
        recov_rows.append(dict(gj_set=gj_set, im_implied=im_implied,
                               dP=dPm, recov=recov, rel_err=rel))
        print(f"  {gj_set:9.2f} | {c['weak_value_im']:9.4f} | {dPm:10.5f} | "
              f"{recov:10.3f} | {rel:8.1%}")

    rel_errs = np.array([r["rel_err"] for r in recov_rows])
    TOL = 0.15                  # pre-registered readout tolerance: 15%
    n_within = int(np.sum(rel_errs <= TOL))
    median_err = float(np.median(rel_errs))
    readout_pass = n_within >= len(recov_rows) - 1 and monotonic
    print(f"  median relative error = {median_err:.1%}; "
          f"{n_within}/{len(recov_rows)} cells within {TOL:.0%} tolerance")
    print(f"  H-readout: {'PASS' if readout_pass else 'FAIL'}")

    # ---- H-noncollapse -----------------------------------------------------
    # The honest test: does the WEAK COUPLING'S OWN back-action stay small?
    # The bare unitary H_sys (Rabi) sweeps rho_n across [0,0.5] regardless of
    # any measurement -- that is not back-action, it is the construction having
    # no maintenance term. H-noncollapse isolates the coupling's contribution.
    print(f"\n[H-noncollapse]  back-action of the weak coupling on rho_n")
    lam_cells = [c for c in state["lambda_sweep"].values() if c.get("ok")]
    lam_cells.sort(key=lambda c: c["lam"])
    BA_TOL = 0.02               # back-action tolerance: |drho_n| < 0.02
    ba_small = True
    for c in lam_cells:
        ba = c["backaction"]
        small = ba < BA_TOL
        ba_small = ba_small and small
        print(f"  lambda={c['lam']:.3f}: rho_n bare={c['rho_n_bare']:.4f} "
              f"coupled={c['rho_n_post']:.4f}  back-action={ba:.5f}  "
              f"{'small' if small else 'LARGE'}")
    gj_ba = [c["backaction"] for c in cells]
    print(f"  g/J cells (lambda={lam}): max back-action = {max(gj_ba):.5f}, "
          f"median = {np.median(gj_ba):.5f}")
    # the structural finding: does the bare system stay in the corridor?
    bare_in_count = sum(1 for c in cells
                        if RHO_LO <= c["rho_n_bare"] <= RHO_HI)
    print(f"  STRUCTURAL: bare system (no coupling) in corridor at "
          f"t_f for {bare_in_count}/{len(cells)} g/J cells")
    print(f"  -> the bare unitary H_sys does NOT preserve the corridor; the")
    print(f"     corridor is a property of the dissipative alpha-gamma*M")
    print(f"     dynamics, absent from a unitary von Neumann construction.")
    # H-noncollapse PASSES if the coupling's back-action is small (the
    # measurement is genuinely weak); it does NOT require the bare system to
    # sit in the corridor -- that is a separate structural fact reported above.
    noncollapse_pass = bool(ba_small and max(gj_ba) < BA_TOL)
    print(f"  H-noncollapse (back-action < {BA_TOL}): "
          f"{'PASS' if noncollapse_pass else 'FAIL'}")

    # ---- verdict -----------------------------------------------------------
    print("\n" + "=" * 78)
    verdict = "PASS" if (conjugate_holds and readout_pass
                         and noncollapse_pass) else "FAIL"
    print(f"VERDICT: {verdict}")
    print(f"  H-conjugate    : {'PASS' if conjugate_holds else 'FAIL'}")
    print(f"  H-readout      : {'PASS' if readout_pass else 'FAIL'}  "
          f"(decisive)")
    print(f"  H-noncollapse  : {'PASS' if noncollapse_pass else 'FAIL'}")
    print("=" * 78)

    state["analysis"] = dict(
        verdict=verdict,
        h_conjugate=dict(passed=bool(conjugate_holds),
                         commutator=[comm.real, comm.imag],
                         bulk_dev=bulk_dev,
                         corr_dQ_reA=cQ_re, corr_dQ_imA=cQ_im,
                         corr_dP_reA=cP_re, corr_dP_imA=cP_im,
                         median_ratio_dP=float(np.nanmedian(ratio_dP)),
                         median_ratio_dQ=float(np.nanmedian(ratio_dQ)),
                         aav_dP_holds=aav_dP_ok),
        h_readout=dict(passed=bool(readout_pass), monotonic=monotonic,
                       median_rel_err=median_err, tolerance=TOL,
                       n_within=n_within, n_total=len(recov_rows),
                       rows=recov_rows),
        h_noncollapse=dict(passed=noncollapse_pass,
                           backaction_tol=BA_TOL,
                           max_backaction_gj=float(max(gj_ba)),
                           bare_in_corridor_count=bare_in_count,
                           lambda_sweep=lam_cells),
    )
    flush(state)
    print(f"\nanalysis written to {RESULTS.name}")
    return verdict


if __name__ == "__main__":
    main()
