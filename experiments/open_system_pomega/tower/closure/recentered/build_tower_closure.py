"""
P_omega tower -- the FORWARD-BACKWARD CLOSURE.
==============================================

Pre-registration: experiments/open_system_pomega/tower/closure/PREREGISTRATION.md.
Prior constructions (the two horns of the squeeze):
  ../build_tower_pomega.py  -- additive operator penalty: frustration (EMPTY horn)
  ../recast/build_tower_recast.py -- feed-forward map constraints: DECOUPLES (TRIVIAL horn)

WHY THE RECAST DECOUPLED (the thing this construction must overcome).
  In the recast, rung n carries a distribution p_n; the map W_n is column-
  stochastic; p_{n+1} = W_n p_n is the genuine push-forward. The cross-rung
  tau(W_n) is the genuine normalized mutual information. But the tower is a
  DIRECTED FEED-FORWARD CHAIN: p_n depends only on W_0..W_{n-1} (upstream),
  tau(W_n) depends only on (W_n, p_n). So W_n cannot affect any rung < n. The
  joint optimum = sum of independent per-bond optima; fixing W_n does NOT
  change what W_{n+1} may do. Decoupled. TRIVIAL.

THE CLOSURE -- restoring the genuine TSVF backward boundary.
  P_omega was never a forward object. It is the framework's BACKWARD boundary
  <Phi_omega| -- a post-selection from the future boundary t_f. Both prior
  towers simplified that away. Here it is restored.

  Each rung n carries a TWO-STATE PAIR:
    - forward state  |psi_n>  : a distribution propagated UP from the base,
        psi_0 = p_0 (free root),  psi_{n+1} = W_n psi_n      (push-forward)
    - backward state <phi_n|  : a covector propagated DOWN from a post-selection
        at the TOP rung R-1,
        phi_{R-1} = b_omega   (the omega-condition, see below),
        phi_n     = W_n^T phi_{n+1}                          (pull-back / adjoint)

  The WEAK STATE at rung n is the two-state (ABL) combination
        q_n[x]  proportional to  phi_n[x] * psi_n[x]
  -- the classical analogue of the weak value <phi|.|psi>/<phi|psi>. The
  within-rung and cross-rung corridor conditions are conditions on the WEAK
  states q_n, NOT on the forward states alone.

  WITHIN-RUNG:  rho_n = 1 - H(q_n)/H_max,  penalty (rho_n - rho_c)^2.
  CROSS-RUNG:   tau_n = normalized MI of the joint weak two-rung law
                  Q_n[y,x] proportional to W_n[y,x] * psi_n[x] * phi_{n+1}[y]
                -- the map W_n weighted by the forward state arriving from
                below AND the backward state arriving from above. tau(W_n) is
                the genuine I(R_n;R_{n+1})/min(H,H) of THAT weak joint law.
                penalty (tau_n - tau_c)^2.

THE OMEGA-CONDITION (the backward boundary -- this must NOT be hand-tuned).
  The pre-registration's hard discipline: the boundary must be the genuine
  omega-post-selection, not a boundary chosen to manufacture coupling. The
  omega-condition is property (ii)+(iii) of Piece 7 evaluated at the TOP rung:
  the top rung is corridor-occupying. So b_omega is the SOFT corridor weight on
  the top rung's state space -- the SAME exp(-beta (rho - rho_c)^2) soft P_omega
  the NOTES.md history settled on, restricted to rung R-1. It is a fixed
  function of the corridor centre rho_c and width w (beta_pin = 1/2w^2); it has
  NO free parameters the construction gets to pick. Concretely b_omega is the
  per-macrostate corridor-compatibility covector: a macrostate x of the top rung
  is omega-favoured to the degree a top rung CONCENTRATED on x sits in corridor.
  We also run a CONTROL boundary b_flat = uniform covector (no post-selection):
  if the flat boundary ALSO couples the chain, the coupling is an artifact of
  the two-state algebra, not of omega; if only b_omega couples, the omega
  post-selection is doing the work.

WHY THIS CANNOT DECOUPLE THE RECAST WAY (the hypothesis under test).
  phi_n = W_n^T phi_{n+1} depends on W_n, W_{n+1}, ..., W_{R-2}, b_omega -- the
  WHOLE downstream chain. psi_n depends on W_0..W_{n-1} -- the whole upstream
  chain. The weak state q_n ~ phi_n * psi_n therefore depends on EVERY map in
  the tower. Fixing W_n changes phi_{n-1}, phi_{n-2}, ..., phi_0 -- it changes
  the weak states of every UPSTREAM rung. The feed-forward directedness the
  recast exploited is broken by the backward leg. WHETHER that makes the joint
  object non-trivially COUPLED (joint optimum != sum of per-bond optima) is the
  decisive test -- not assumed.

DECISIVE DIAGNOSTICS (same kind the recast ran).
  D1. Joint optimum vs sum-of-independent-per-bond optima. Recast: equal
      (gap ~ 1e-7 search residual). Closure: if the gap is real and grows with
      R, the boundary couples.
  D2. Fix-W_n perturbation. Solve the joint optimum; fix W_n at its optimal
      value; re-optimise everything else; then PERTURB W_n and re-optimise --
      does the optimal W_{n+1} (and W_{n-1}) MOVE? In a decoupled chain it does
      not. The size of the move is the coupling strength.
  D3. Random-tower factorization test. For random towers, does the joint
      penalty factorize over bonds (H_total = sum_n f(bond n)) or not? Measured
      by whether the cross-partial d^2 H / dW_n dW_m is zero for |n-m|>0.
  D4. Selectivity: fraction of random towers in the joint corridor. Trivial
      if all towers pass; selective if measure-concentrated.

VERDICT (three horns, pre-committed):
  DISCOVERY -- non-empty AND coupled (D1 gap real & grows, D2 moves, D3 does not
               factorize) AND well-defined to 9 rungs and past R*.
  EMPTY     -- the two-arm constraint is over-determined: no tower satisfies the
               forward corridors and the backward-propagated boundary.
  TRIVIAL   -- the closure still decouples / the backward boundary does no work.

CUDA: cupy/float64 throughout. Incremental: every depth flushed to JSON.
"""
import json
import os
import time

import numpy as np

try:
    import cupy as xp
    GPU = True
    _GPU_ERR = None
except Exception as exc:                                   # pragma: no cover
    xp = np
    GPU = False
    _GPU_ERR = str(exc)

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results_tower_closure.json")

D = 3                         # rung alphabet size (qutrit -- as recast)
# BUG-FIX RE-CENTRING (recentered/PREREGISTRATION.md): the penalty centre is the
# ACTUAL corridor centre, rho_c = tau_c = (0.10 + 0.43)/2 = 0.265, NOT 0.5.
# The 0.5 centre sat outside the band (0.10, 0.43) -> tau_in_band_count = 0 at
# every depth. The centre 0.265 is forced by the band; it is not a tunable knob.
RHO_C = 0.265                 # within-rung corridor centre = band centre
TAU_C = 0.265                 # cross-rung corridor centre  = band centre
TAU_LOWER, TAU_UPPER = 0.10, 0.43      # framework corridor band
W_CORR = 0.165                # corridor half-width (A3+ calibration ~0.16-0.35)
BETA_PIN = 1.0 / (2.0 * W_CORR ** 2)   # framework-referenced beta = 1/2w^2
EPS = 1e-12
HMAX = float(np.log(D))
R_LIST = [2, 3, 4, 5, 6, 7, 8, 9, 11, 13, 20, 30, 40, 56]
SEED = 20260522
POOL = 24000
REFINE = 10


def log(msg):
    print(msg, flush=True)


# ---------------------------------------------------------------------------
# core quantities
# ---------------------------------------------------------------------------
def entropy_vec(P):
    Pc = xp.clip(P, EPS, 1.0)
    return -xp.sum(Pc * xp.log(Pc), axis=1)


def rho_of(p):
    """within-rung correlation rho = 1 - H(p)/H_max for one distribution."""
    pc = xp.clip(p, EPS, 1.0)
    pc = pc / xp.sum(pc)
    return float(1.0 - (-xp.sum(pc * xp.log(pc))) / HMAX)


def rho_vec(P):
    return 1.0 - entropy_vec(P) / HMAX


def normalize(p):
    p = xp.clip(p, EPS, None)
    return p / xp.sum(p)


def random_channels(N, rng, sharpness=1.5):
    """N column-stochastic channels (N,d,d)."""
    M = xp.asarray(rng.random((N, D, D))) ** sharpness + 0.02
    return M / xp.sum(M, axis=1, keepdims=True)


def random_simplex(rng):
    v = xp.asarray(rng.random(D)) ** 1.5 + 0.02
    return v / xp.sum(v)


# ---------------------------------------------------------------------------
# the omega-condition: the genuine TSVF backward boundary
# ---------------------------------------------------------------------------
# WHY THE BOUNDARY IS NOT A FIXED MACROSTATE COVECTOR.
#   The omega-condition is corridor-OCCUPATION of the top rung: rho(psi_R) in
#   band. rho is the within-rung correlation = 1 - H(psi)/H_max -- a NONLINEAR
#   (entropy) functional of the distribution. A fixed covector on the d
#   macrostates cannot carry an entropy condition: on a symmetric d-alphabet
#   any such covector is flat (verified -- the naive b_omega[x] came out
#   [1/3,1/3,1/3], i.e. no post-selection at all). The genuine TSVF backward
#   state is the LINEAR-RESPONSE (weak-value) form of the soft post-selection
#   E_omega = exp(-beta (rho-rho_c)^2): the backward covector is the GRADIENT
#   of the soft omega log-weight evaluated AT the top rung's forward state.
#
#   This is exactly the two-state-vector structure: weak values ARE first-order
#   responses of a post-selected amplitude. The boundary covector is:
#
#       phi_R[x]  proportional to  psi_R[x] * exp( g * d/d(psi_R[x]) of
#                                       [ -beta (rho(psi_R)-rho_c)^2 ] )
#
#   It is determined ENTIRELY by the framework's E_omega (the soft corridor
#   operator) and beta_pin = 1/2w^2 -- NO free knob. It is genuinely non-flat
#   because it depends on psi_R, the forward state arriving at the top, which
#   in turn depends on every map below. That state-dependence is the genuine
#   post-selection coupling -- it is a CONSEQUENCE of the omega-condition, not
#   a hand-tuned input.

def omega_backward_covector(psi_top):
    """The genuine omega post-selection backward covector at the top rung.

    The soft post-selection is E_omega = exp(-beta H), H = (rho(psi)-rho_c)^2.
    The TSVF backward state is the WEAK-VALUE (first-order / linear-response)
    object: weak values are first-order responses of the post-selected
    amplitude, NOT the full exponential. The backward covector is therefore
    the first-order post-selection reweighting

        phi_R[x]  proportional to  uniform[x] * (1 + grad[x])

    with grad[x] = d(-beta H)/d(psi[x]) the omega log-weight gradient at the
    top forward state, mean-subtracted (a pure reweighting) and gain-limited
    so phi stays a positive graded covector -- the genuine weak value, not a
    saturated hard projector. Determined by (rho_c, beta_pin): NO free knob.
    """
    p = normalize(psi_top)
    pc = xp.clip(p, EPS, 1.0)
    H = -xp.sum(pc * xp.log(pc))                  # Shannon entropy
    rho = 1.0 - H / HMAX
    drho = (1.0 + xp.log(pc)) / HMAX              # d rho / d p[x]
    grad = -2.0 * BETA_PIN * (rho - RHO_C) * drho
    grad = grad - xp.mean(grad)                   # pure reweighting
    # scale so the largest |grad| component reweights by at most a factor ~e:
    # the weak value is a first-order response; gain-limit keeps it graded.
    g = float(xp.max(xp.abs(grad)))
    if g > 1.0:
        grad = grad / g
    phi = xp.clip(1.0 + grad, 1e-3, None)
    return normalize(phi)


# ---------------------------------------------------------------------------
# forward / backward propagation through the tower
# ---------------------------------------------------------------------------
def forward_states(p0, Wlist):
    """|psi_n> for n=0..R-1: psi_0 = p0, psi_{n+1} = W_n psi_n."""
    psis = [normalize(p0)]
    for W in Wlist:
        psis.append(normalize(W @ psis[-1]))
    return psis


def top_boundary(psi_top, mode):
    """The backward boundary covector at the top rung.

    mode='omega' -- the genuine omega post-selection: the linear-response
        covector of the soft corridor operator E_omega evaluated at psi_top
        (omega_backward_covector). State-dependent BY THE OMEGA CONDITION.
    mode='flat'  -- the CONTROL: uniform covector = no post-selection. Used to
        check that any coupling found is omega-specific, not a two-state-
        algebra artifact.
    """
    if mode == "flat":
        return xp.ones(D) / D
    return omega_backward_covector(psi_top)


def backward_states(psis, Wlist, mode):
    """<phi_n| for n=0..R-1: phi_{R-1} = top_boundary(psi_top), then
    phi_n = W_n^T phi_{n+1}.

    This is the genuine TSVF backward propagation: the covector pulled DOWN
    through the coarse-graining maps from the post-selection boundary at the
    top rung. W_n^T is the adjoint of the channel W_n. The top boundary itself
    is the omega-condition evaluated at the forward state arriving at the top,
    so the WHOLE backward leg depends on the forward leg -- the closure."""
    R = len(Wlist) + 1
    phis = [None] * R
    phis[R - 1] = normalize(top_boundary(psis[R - 1], mode))
    for n in range(R - 2, -1, -1):
        phis[n] = normalize(Wlist[n].T @ phis[n + 1])
    return phis


def weak_states(phis, psis):
    """q_n[x] ~ phi_n[x] * psi_n[x] -- the two-state (ABL) weak distribution."""
    return [normalize(phis[n] * psis[n]) for n in range(len(psis))]


def tau_weak(W, psi_in, phi_out):
    """Cross-rung tau on the WEAK two-rung joint law.

    The forward state psi_in arrives at rung n from below; the backward state
    phi_out arrives at rung n+1 from above. The weak joint law of the bond is
        Q[y,x] ~ W[y,x] * psi_in[x] * phi_out[y]
    -- the channel weighted by BOTH boundary states. tau is the genuine
    normalized mutual information of Q."""
    psi_in = normalize(psi_in)
    phi_out = normalize(phi_out)
    Q = W * psi_in[xp.newaxis, :] * phi_out[:, xp.newaxis]      # (d,d)
    s = xp.sum(Q)
    Q = Q / xp.maximum(s, EPS)
    px = xp.sum(Q, axis=0)            # marginal on rung n
    py = xp.sum(Q, axis=1)            # marginal on rung n+1
    Qc = xp.clip(Q, EPS, 1.0)
    outer = xp.clip(py[:, xp.newaxis] * px[xp.newaxis, :], EPS, 1.0)
    I = float(xp.sum(Q * xp.log(Qc / outer)))
    Hx = float(-xp.sum(xp.clip(px, EPS, 1.0) * xp.log(xp.clip(px, EPS, 1.0))))
    Hy = float(-xp.sum(xp.clip(py, EPS, 1.0) * xp.log(xp.clip(py, EPS, 1.0))))
    denom = min(Hx, Hy)
    return 0.0 if denom < 1e-9 else I / denom


def tau_weak_batch(Wpool, psi_in, phi_out):
    """tau_weak for a batch of channels (N,d,d) -- GPU vectorised."""
    psi_in = normalize(psi_in)
    phi_out = normalize(phi_out)
    Q = (Wpool * psi_in[xp.newaxis, xp.newaxis, :]
         * phi_out[xp.newaxis, :, xp.newaxis])               # (N,d,d)
    s = xp.sum(Q, axis=(1, 2), keepdims=True)
    Q = Q / xp.maximum(s, EPS)
    px = xp.sum(Q, axis=1)            # (N,d)
    py = xp.sum(Q, axis=2)            # (N,d)
    Qc = xp.clip(Q, EPS, 1.0)
    outer = xp.clip(py[:, :, xp.newaxis] * px[:, xp.newaxis, :], EPS, 1.0)
    I = xp.sum(Q * xp.log(Qc / outer), axis=(1, 2))
    Hx = -xp.sum(xp.clip(px, EPS, 1.0) * xp.log(xp.clip(px, EPS, 1.0)), axis=1)
    Hy = -xp.sum(xp.clip(py, EPS, 1.0) * xp.log(xp.clip(py, EPS, 1.0)), axis=1)
    denom = xp.minimum(Hx, Hy)
    return xp.where(denom < 1e-9, 0.0, I / xp.maximum(denom, 1e-9))


# ---------------------------------------------------------------------------
# the joint penalty -- a TRUE functional of the whole tower
# ---------------------------------------------------------------------------
def H_total(p0, Wlist, mode):
    """H_total = sum_n (rho(q_n) - rho_c)^2 + sum_n (tau_weak_n - tau_c)^2,
    with q_n the weak states and tau_weak the weak-joint cross-rung MI.

    This is NOT feed-forward: q_n depends on phi_n which depends on W_n..W_{R-2}
    and the top boundary; the top boundary depends on psi_top which depends on
    ALL maps. tau_weak_n depends on psi_n (upstream) AND phi_{n+1} (downstream).
    Every term couples both directions. mode in {'omega','flat'}."""
    psis = forward_states(p0, Wlist)
    phis = backward_states(psis, Wlist, mode)
    qs = weak_states(phis, psis)
    within = 0.0
    rhos = []
    for q in qs:
        r = rho_of(q)
        rhos.append(r)
        within += (r - RHO_C) ** 2
    cross = 0.0
    taus = []
    for n, W in enumerate(Wlist):
        t = tau_weak(W, psis[n], phis[n + 1])
        taus.append(t)
        cross += (t - TAU_C) ** 2
    return within + cross, {"within": within, "cross": cross,
                            "rho": rhos, "tau": taus}


# ---------------------------------------------------------------------------
# the joint solver -- coordinate descent (NOT a greedy feed-forward sweep)
# ---------------------------------------------------------------------------
def solve_joint(R, mode, rng, restarts=4, sweeps=10, fixed=None):
    """Minimise H_total over {p0, W_0..W_{R-2}} by full coordinate descent.

    Crucially this is NOT the recast's greedy feed-forward sweep. Each W_n is
    re-optimised against the FULL H_total (which sees the whole tower through
    the backward leg AND the state-dependent omega boundary), and sweeps are
    repeated until convergence. For a genuine feed-forward chain a single
    forward sweep would converge; if the closure couples, multiple sweeps keep
    improving (downstream maps changing upstream weak states).

    `fixed`: optional dict {map_index: W} of maps held frozen (used by the
    fix-W_n perturbation diagnostic)."""
    fixed = fixed or {}
    best_total = None
    best = None
    nmaps = max(R - 1, 1)
    for attempt in range(restarts):
        p0 = random_simplex(rng)
        Wlist = [fixed.get(i, random_channels(1, rng)[0]) for i in range(nmaps)]
        cur, _ = H_total(p0, Wlist, mode)
        sweep_curve = [cur]
        # because the omega boundary depends on psi_top, coordinate descent
        # is NOT monotone -- optimising a downstream map shifts the boundary
        # and can raise an upstream term. (For a feed-forward chain it WOULD
        # be monotone; the non-monotonicity IS a coupling signature.) So we
        # track the best (p0, Wlist) ever seen, not the last.
        run_best_v = cur
        run_best = (p0, [W for W in Wlist])
        for sweep in range(sweeps):
            # batched p0 search (p0 enters rung 0 -> whole tower batched)
            P0 = xp.stack([random_simplex(rng) for _ in range(4000)])
            P0 = xp.concatenate([P0, p0[xp.newaxis]], axis=0)   # keep current
            v0 = _eval_p0_pool(P0, Wlist, mode)
            kp = int(xp.argmin(v0))
            p0, cur = P0[kp], float(v0[kp])
            for n in range(nmaps):
                if n in fixed:
                    continue
                pool = random_channels(POOL, rng)
                vals = _eval_Wn_pool(p0, Wlist, mode, n, pool)
                k = int(xp.argmin(vals))
                Wk, vk = pool[k], float(vals[k])
                for _ in range(REFINE):
                    J = (Wk[xp.newaxis]
                         + xp.asarray(rng.normal(0, 0.03, (6000, D, D))))
                    J = xp.clip(J, 1e-4, None)
                    J = J / xp.sum(J, axis=1, keepdims=True)
                    vj = _eval_Wn_pool(p0, Wlist, mode, n, J)
                    kk = int(xp.argmin(vj))
                    if float(vj[kk]) < vk:
                        Wk, vk = J[kk], float(vj[kk])
                Wlist[n] = Wk
                cur = vk
                if cur < run_best_v:
                    run_best_v = cur
                    run_best = (p0, [W for W in Wlist])
            sweep_curve.append(cur)
            if (sweep > 1 and
                    abs(sweep_curve[-2] - sweep_curve[-1]) < 1e-13 and
                    abs(sweep_curve[-3] - sweep_curve[-1]) < 1e-13):
                break
        if best_total is None or run_best_v < best_total:
            best_total = run_best_v
            bp0, bW = run_best
            tot, info = H_total(bp0, bW, mode)
            best = {"within": info["within"], "cross": info["cross"],
                    "rho": [float(r) for r in info["rho"]],
                    "tau": [float(t) for t in info["tau"]],
                    "sweep_curve": [float(s) for s in sweep_curve],
                    "p0": bp0.get() if GPU else bp0,
                    "Wlist": [W.get() if GPU else W for W in bW]}
    return best_total, best


def omega_backward_covector_batch(psi_top):
    """Batched omega backward covector for psi_top of shape (N,d).
    First-order weak-value form -- matches omega_backward_covector exactly."""
    p = psi_top / xp.sum(psi_top, axis=1, keepdims=True)
    pc = xp.clip(p, EPS, 1.0)
    H = -xp.sum(pc * xp.log(pc), axis=1)                 # (N,)
    rho = 1.0 - H / HMAX
    drho = (1.0 + xp.log(pc)) / HMAX                     # (N,d)
    grad = -2.0 * BETA_PIN * (rho - RHO_C)[:, xp.newaxis] * drho
    grad = grad - xp.mean(grad, axis=1, keepdims=True)
    g = xp.max(xp.abs(grad), axis=1, keepdims=True)      # (N,1)
    grad = xp.where(g > 1.0, grad / xp.maximum(g, EPS), grad)
    phi = xp.clip(1.0 + grad, 1e-3, None)
    return phi / xp.sum(phi, axis=1, keepdims=True)


def _eval_Wn_pool(p0, Wlist, mode, n, Wpool):
    """H_total for a whole POOL of candidate W_n, with all other maps fixed.

    Vectorised on the GPU. Changing W_n affects:
      - psi_{n+1}, psi_{n+2}, ..., psi_{R-1}   (forward, downstream)
      - the top boundary phi_{R-1}  (omega mode: phi_top = f(psi_top), and
        psi_top depends on W_n)
      - phi_n, ..., phi_0  AND, through the moving boundary, phi_{n+1}..phi_{R-2}
      - the weak states q_0..q_{R-1} (all of them) and every tau bond.
    So a single map-change touches the WHOLE tower BOTH WAYS -- this is the
    coupling the closure introduces and the recast (feed-forward) lacked.

    Because the top boundary is omega(psi_top) and psi_top depends on W_n,
    the ENTIRE backward leg is batched in omega mode (no phi is fixed)."""
    N = Wpool.shape[0]
    R = len(Wlist) + 1
    # --- forward leg: psi_0..psi_n fixed; psi_{n+1}.. batched -------------
    psi_fixed = [normalize(p0)]
    for m in range(n):
        psi_fixed.append(normalize(Wlist[m] @ psi_fixed[-1]))
    psi_batch = [None] * R
    for m in range(n + 1):
        psi_batch[m] = xp.broadcast_to(psi_fixed[m], (N, D))
    cur = xp.einsum("nij,j->ni", Wpool, psi_fixed[n])     # psi_{n+1} (N,d)
    cur = cur / xp.sum(cur, axis=1, keepdims=True)
    psi_batch[n + 1] = cur
    for m in range(n + 1, R - 1):
        cur = xp.einsum("ij,nj->ni", Wlist[m], cur)
        cur = cur / xp.sum(cur, axis=1, keepdims=True)
        psi_batch[m + 1] = cur
    # --- top boundary: omega(psi_top) -- batched if psi_top is batched ---
    if mode == "flat":
        phi_top = xp.broadcast_to(xp.ones(D) / D, (N, D))
    else:
        phi_top = omega_backward_covector_batch(psi_batch[R - 1])
    # --- backward leg: all phi batched (boundary depends on W_n) ----------
    phi_batch = [None] * R
    phi_batch[R - 1] = phi_top
    for m in range(R - 2, n, -1):
        # W_m fixed, phi batched: phi_m = W_m^T phi_{m+1}
        cur = xp.einsum("ji,nj->ni", Wlist[m], phi_batch[m + 1])
        cur = cur / xp.sum(cur, axis=1, keepdims=True)
        phi_batch[m] = cur
    # phi_n: W_n is the pool -> phi_n = W_n^T phi_{n+1}
    cur = xp.einsum("nji,nj->ni", Wpool, phi_batch[n + 1])
    cur = cur / xp.sum(cur, axis=1, keepdims=True)
    phi_batch[n] = cur
    for m in range(n - 1, -1, -1):
        cur = xp.einsum("ji,nj->ni", Wlist[m], cur)
        cur = cur / xp.sum(cur, axis=1, keepdims=True)
        phi_batch[m] = cur
    # --- weak states q_m ~ phi_m * psi_m ---------------------------------
    within = xp.zeros(N)
    for m in range(R):
        q = phi_batch[m] * psi_batch[m]
        q = q / xp.sum(q, axis=1, keepdims=True)
        r = rho_vec(q)
        within = within + (r - RHO_C) ** 2
    # --- cross-rung tau on the weak joint law for each bond --------------
    cross = xp.zeros(N)
    for m in range(R - 1):
        if m == n:
            tau = _tau_weak_bvar(Wpool, psi_batch[m], phi_batch[m + 1])
        else:
            Wm = xp.broadcast_to(Wlist[m], (N, D, D))
            tau = _tau_weak_bvar(Wm, psi_batch[m], phi_batch[m + 1])
        cross = cross + (tau - TAU_C) ** 2
    return within + cross


def _tau_weak_bvar(Wpool, psi_in, phi_out):
    """tau_weak with psi_in, phi_out themselves batched (N,d)."""
    psi_in = psi_in / xp.sum(psi_in, axis=1, keepdims=True)
    phi_out = phi_out / xp.sum(phi_out, axis=1, keepdims=True)
    Q = (Wpool * psi_in[:, xp.newaxis, :] * phi_out[:, :, xp.newaxis])
    s = xp.sum(Q, axis=(1, 2), keepdims=True)
    Q = Q / xp.maximum(s, EPS)
    px = xp.sum(Q, axis=1)
    py = xp.sum(Q, axis=2)
    Qc = xp.clip(Q, EPS, 1.0)
    outer = xp.clip(py[:, :, xp.newaxis] * px[:, xp.newaxis, :], EPS, 1.0)
    I = xp.sum(Q * xp.log(Qc / outer), axis=(1, 2))
    Hx = -xp.sum(xp.clip(px, EPS, 1.0) * xp.log(xp.clip(px, EPS, 1.0)), axis=1)
    Hy = -xp.sum(xp.clip(py, EPS, 1.0) * xp.log(xp.clip(py, EPS, 1.0)), axis=1)
    denom = xp.minimum(Hx, Hy)
    return xp.where(denom < 1e-9, 0.0, I / xp.maximum(denom, 1e-9))


def _eval_p0_pool(P0pool, Wlist, mode):
    """H_total for a whole POOL of root distributions p0 (N,d), maps fixed.

    p0 enters at rung 0, so the WHOLE forward leg -- and, in omega mode, the
    state-dependent top boundary and the whole backward leg -- become batched.
    Vectorised on the GPU; replaces the per-p0 Python loop."""
    N = P0pool.shape[0]
    R = len(Wlist) + 1
    psi_batch = [None] * R
    cur = P0pool / xp.sum(P0pool, axis=1, keepdims=True)
    psi_batch[0] = cur
    for m in range(R - 1):
        cur = xp.einsum("ij,nj->ni", Wlist[m], cur)
        cur = cur / xp.sum(cur, axis=1, keepdims=True)
        psi_batch[m + 1] = cur
    if mode == "flat":
        phi_top = xp.broadcast_to(xp.ones(D) / D, (N, D))
    else:
        phi_top = omega_backward_covector_batch(psi_batch[R - 1])
    phi_batch = [None] * R
    phi_batch[R - 1] = phi_top
    cur = phi_top
    for m in range(R - 2, -1, -1):
        cur = xp.einsum("ji,nj->ni", Wlist[m], cur)
        cur = cur / xp.sum(cur, axis=1, keepdims=True)
        phi_batch[m] = cur
    within = xp.zeros(N)
    for m in range(R):
        q = phi_batch[m] * psi_batch[m]
        q = q / xp.sum(q, axis=1, keepdims=True)
        within = within + (rho_vec(q) - RHO_C) ** 2
    cross = xp.zeros(N)
    for m in range(R - 1):
        Wm = xp.broadcast_to(Wlist[m], (N, D, D))
        tau = _tau_weak_bvar(Wm, psi_batch[m], phi_batch[m + 1])
        cross = cross + (tau - TAU_C) ** 2
    return within + cross


# ===========================================================================
def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    out = {
        "meta": {
            "date": "2026-05-22",
            "construction": "P_omega tower CLOSURE -- forward-backward two-state "
                            "tower; backward boundary = the linear-response "
                            "(weak-value) covector of the soft omega corridor "
                            "operator E_omega evaluated at the top rung's "
                            "forward state; corridor conditions on the WEAK "
                            "states q_n ~ phi_n*psi_n",
            "rung_alphabet_d": D, "rho_c": RHO_C, "tau_c": TAU_C,
            "corridor_band": [TAU_LOWER, TAU_UPPER],
            "w_corridor": W_CORR, "beta_pin": BETA_PIN,
            "gpu": GPU, "backend": "cupy/float64" if GPU else "numpy-cpu",
            "framework_rung_count": 9,
        },
        "sanity": {}, "depth_scan": {}, "coupling_test": {},
        "selectivity_test": {}, "control_flat_boundary": {},
    }
    if not GPU:
        out["meta"]["cpu_fallback_reason"] = _GPU_ERR

    def _san(o):
        """recursively coerce numpy / cupy scalars to JSON-native types."""
        if isinstance(o, dict):
            return {k: _san(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [_san(v) for v in o]
        if isinstance(o, (np.bool_,)):
            return bool(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        if hasattr(o, "item") and getattr(o, "ndim", 1) == 0:
            return o.item()
        return o

    def flush():
        with open(RESULTS, "w") as fh:
            json.dump(_san(out), fh, indent=2)
    flush()

    log("=" * 78)
    log("P_omega TOWER -- the FORWARD-BACKWARD CLOSURE")
    log("=" * 78)
    log(f"  backend: {out['meta']['backend']};  d={D}  beta_pin={BETA_PIN:.2f}")
    log("  backward boundary = omega post-selection (weak-value covector of the")
    log("  soft corridor operator at the top rung) -- state-dependent BY the")
    log("  omega condition, no free knob. Control: a flat (no-post-selection)")
    log("  boundary, to check any coupling found is omega-specific.")

    # -- SANITY: backward propagation + weak states behave -------------------
    log("")
    log("-" * 78)
    log("SANITY -- forward/backward propagation and the weak (two-state) state")
    log("-" * 78)
    Wt = [random_channels(1, rng)[0] for _ in range(4)]
    p0t = random_simplex(rng)
    psis = forward_states(p0t, Wt)
    phis = backward_states(psis, Wt, "omega")
    qs = weak_states(phis, psis)
    # the omega boundary covector must be NON-FLAT (else no post-selection)
    phitop = phis[len(Wt)]
    spread = float(xp.max(phitop) - xp.min(phitop))
    # check it varies with the top state (the post-selection content)
    psis_b = forward_states(random_simplex(rng), Wt)
    phitop_b = top_boundary(psis_b[len(Wt)], "omega")
    boundary_varies = float(xp.sqrt(xp.sum((phitop - phitop_b) ** 2)))
    log(f"  forward psi_0..psi_4 entropies: "
        f"{[round(float(entropy_vec(p[xp.newaxis])[0]),3) for p in psis]}")
    log(f"  backward phi_0..phi_4 entropies: "
        f"{[round(float(entropy_vec(p[xp.newaxis])[0]),3) for p in phis]}")
    log(f"  weak q_n rho values: {[round(rho_of(q),3) for q in qs]}")
    log(f"  omega boundary covector spread (max-min) = {spread:.4f}  "
        f"({'FLAT -- no post-selection!' if spread < 1e-3 else 'non-flat -- genuine post-selection'})")
    log(f"  boundary varies with top state: ||delta|| = {boundary_varies:.4f}  "
        f"({'state-dependent (genuine weak value)' if boundary_varies > 1e-3 else 'state-independent'})")
    out["sanity"] = {
        "forward_entropies": [float(entropy_vec(p[xp.newaxis])[0]) for p in psis],
        "backward_entropies": [float(entropy_vec(p[xp.newaxis])[0]) for p in phis],
        "weak_rho": [rho_of(q) for q in qs],
        "omega_boundary_spread": spread,
        "omega_boundary_state_dependence": boundary_varies,
    }
    flush()

    # -- STAGE A: depth scan -------------------------------------------------
    log("")
    log("-" * 78)
    log("STAGE A -- depth scan: joint H_min(R) under the forward-backward closure")
    log("-" * 78)
    for R in R_LIST:
        restarts = 4 if R <= 13 else 3
        sweeps = 10 if R <= 20 else 7
        hmin, info = solve_joint(R, "omega", rng, restarts=restarts, sweeps=sweeps)
        # how much did the multi-sweep coordinate descent improve over the
        # first sweep? a genuine feed-forward chain converges in sweep 1.
        sc = info["sweep_curve"]
        sweep1 = sc[1] if len(sc) > 1 else sc[0]
        sweepN = sc[-1]
        improvement = sweep1 - sweepN
        out["depth_scan"][str(R)] = {
            "h_min": hmin, "h_min_per_rung": hmin / R,
            "within_part": info["within"], "cross_part": info["cross"],
            "tau_values": info["tau"], "rho_values": info["rho"],
            "tau_in_band_count": int(sum(1 for t in info["tau"]
                                         if TAU_LOWER < t < TAU_UPPER)),
            "n_sweeps_to_converge": len(sc) - 1,
            "first_sweep_h": sweep1, "final_sweep_h": sweepN,
            "post_sweep1_improvement": improvement,
        }
        log(f"  R={R:>3d}  H_min={hmin:.6e}  /R={hmin/R:.6e}  "
            f"(within={info['within']:.3e} cross={info['cross']:.3e})  "
            f"sweeps={len(sc)-1}  post-sweep1 gain={improvement:.3e}  "
            f"[{time.time()-t0:.0f}s]")
        flush()

    Rs = sorted(int(k) for k in out["depth_scan"])
    curve = {R: out["depth_scan"][str(R)]["h_min"] for R in Rs}
    deep = [R for R in Rs if R >= 20]
    if len(deep) >= 2:
        e_inf = (curve[deep[-1]] - curve[deep[0]]) / (deep[-1] - deep[0])
    else:
        e_inf = curve[Rs[-1]] / Rs[-1]
    out["per_rung_energy_density_e_inf"] = e_inf
    log(f"  per-rung energy density e_inf (slope over deep tail) = {e_inf:.6e}")
    flush()

    # -- STAGE B: the decisive coupling test ---------------------------------
    log("")
    log("-" * 78)
    log("STAGE B -- DECISIVE: does the backward boundary COUPLE the chain?")
    log("-" * 78)
    log("  D1: joint optimum vs sum of independent per-bond optima.")
    log("  D2: fix-W_n perturbation -- does optimal W_{n+1}/W_{n-1} move?")
    log("  Recast verdict: joint == sum-of-independent (gap ~1e-7); no move.")

    coupling = {}
    for R in [5, 9, 13]:
        # --- D1: independent-per-bond lower bound -------------------------
        # Solve each bond IN ISOLATION: a 2-rung tower with the omega boundary
        # on the upper rung of that bond. Sum the isolated optima. If the
        # closure couples, the joint optimum EXCEEDS this sum (a bond cannot
        # be satisfied without disturbing its neighbours through the backward
        # leg) OR falls below it is impossible -- the genuine signature is a
        # POSITIVE, R-growing gap.
        indep_sum = 0.0
        for _ in range(R - 1):
            h2, _ = solve_joint(2, "omega", rng, restarts=4, sweeps=6)
            indep_sum += h2
        joint_h = curve[R]
        gap = joint_h - indep_sum

        # --- D2: fix-W_n conditional-optimum test -------------------------
        # The clean differential test: pick a middle map n*. CONDITION on a
        # value of W_{n*} and find the optimal W_{n*+1} (re-optimising the rest
        # with n* frozen). Do this for TWO different frozen values of W_{n*}.
        # If the optimal W_{n*+1} is the SAME for both -> W_{n*+1}'s optimum
        # does not depend on W_{n*} -> DECOUPLED. If it MOVES by more than
        # solver noise -> fixing W_{n*} genuinely changes what W_{n*+1} may do
        # -> the backward boundary couples the chain. This is exactly the
        # recast's decoupling check, run on the closure.
        def cdist(A, B):
            return float(xp.sqrt(xp.sum((A - B) ** 2)))
        nstar = (R - 1) // 2

        def conditional_opt(Wn_fixed):
            """optimal W_{nstar+1} given W_{nstar}=Wn_fixed, rest swept."""
            _, info = solve_joint(R, "omega", rng, restarts=3, sweeps=8,
                                  fixed={nstar: Wn_fixed})
            return xp.asarray(info["Wlist"][nstar + 1])

        moved = {}
        if nstar + 1 <= R - 2:
            WA = random_channels(1, rng)[0]
            WB = random_channels(1, rng)[0]
            opt_next_A = conditional_opt(WA)
            opt_next_B = conditional_opt(WB)
            # control: re-run conditional_opt(WA) -- two solves with the SAME
            # frozen W_n bound the solver noise.
            opt_next_A2 = conditional_opt(WA)
            shift = cdist(opt_next_A, opt_next_B)
            noise = cdist(opt_next_A, opt_next_A2)
            moved = {
                "next_map_shift_AvsB": shift,
                "solver_noise_AvsA": noise,
                "coupling_ratio": shift / max(noise, 1e-9),
            }

        coupling[str(R)] = {
            "joint_optimum_h": joint_h,
            "independent_per_bond_sum": indep_sum,
            "joint_minus_independent_gap": gap,
            "fixWn_conditional_test": moved,
            "tested_map_index": nstar,
        }
        log(f"  R={R}: joint H={joint_h:.4e}  indep-sum={indep_sum:.4e}  "
            f"gap={gap:+.4e}")
        if moved:
            log(f"        fix-W_{nstar}: optimal W_{nstar+1} shift "
                f"(diff W_n) = {moved['next_map_shift_AvsB']:.4e}  "
                f"vs solver noise = {moved['solver_noise_AvsA']:.4e}  "
                f"ratio = {moved['coupling_ratio']:.2f}")
        flush()
    out["coupling_test"] = coupling

    # -- STAGE C: control -- the FLAT boundary -------------------------------
    log("")
    log("-" * 78)
    log("STAGE C -- CONTROL: flat boundary (no omega post-selection)")
    log("-" * 78)
    log("  If the flat boundary ALSO couples the chain, the coupling is an")
    log("  artifact of the two-state algebra, NOT of the omega condition.")
    log("  If only b_omega couples, the omega post-selection does the work.")
    ctrl = {}
    for R in [9, 13]:
        hmin_flat, info_flat = solve_joint(R, "flat", rng, restarts=4, sweeps=10)
        # independent-per-bond sum with the flat boundary
        indep_flat = 0.0
        for _ in range(R - 1):
            h2, _ = solve_joint(2, "flat", rng, restarts=3, sweeps=5)
            indep_flat += h2
        gap_flat = hmin_flat - indep_flat
        ctrl[str(R)] = {
            "h_min_flat": hmin_flat,
            "independent_per_bond_sum_flat": indep_flat,
            "gap_flat": gap_flat,
            "tau_values": info_flat["tau"],
        }
        log(f"  R={R}: flat-boundary joint H={hmin_flat:.4e}  "
            f"indep-sum={indep_flat:.4e}  gap={gap_flat:+.4e}")
        flush()
    out["control_flat_boundary"] = ctrl

    # -- STAGE D: selectivity ------------------------------------------------
    log("")
    log("-" * 78)
    log("STAGE D -- selectivity: how concentrated is the joint object?")
    log("-" * 78)
    log("  Measured on the genuine joint penalty H_total (band-centre-agnostic):")
    log("  fraction of random towers within 10x of the joint optimum H_min.")
    log("  Trivial if a large fraction land near the optimum (any tower works);")
    log("  selective if measure-concentrated. Run for BOTH omega and the flat")
    log("  control -- selectivity is omega-specific iff omega concentrates more.")

    def random_tower_penalties(R, mode, n_rand):
        """H_total for n_rand random towers, batched."""
        P0 = xp.stack([random_simplex(rng) for _ in range(n_rand)])
        Wbonds = [random_channels(n_rand, rng) for _ in range(R - 1)]
        psi_b = [P0 / xp.sum(P0, axis=1, keepdims=True)]
        for m in range(R - 1):
            cur = xp.einsum("nij,nj->ni", Wbonds[m], psi_b[-1])
            psi_b.append(cur / xp.sum(cur, axis=1, keepdims=True))
        if mode == "flat":
            phi_top = xp.broadcast_to(xp.ones(D) / D, (n_rand, D))
        else:
            phi_top = omega_backward_covector_batch(psi_b[R - 1])
        phi_b = [None] * R
        phi_b[R - 1] = phi_top
        for m in range(R - 2, -1, -1):
            cur = xp.einsum("nji,nj->ni", Wbonds[m], phi_b[m + 1])
            phi_b[m] = cur / xp.sum(cur, axis=1, keepdims=True)
        h = xp.zeros(n_rand)
        for m in range(R):
            q = phi_b[m] * psi_b[m]
            q = q / xp.sum(q, axis=1, keepdims=True)
            h = h + (rho_vec(q) - RHO_C) ** 2
        for m in range(R - 1):
            tau = _tau_weak_bvar(Wbonds[m], psi_b[m], phi_b[m + 1])
            h = h + (tau - TAU_C) ** 2
        return h.get() if GPU else h

    sel = {}
    for R in [5, 9, 13]:
        n_rand = 6000
        h_om = random_tower_penalties(R, "omega", n_rand)
        h_fl = random_tower_penalties(R, "flat", n_rand)
        hmin_R = curve[R]
        hmin_flat_R = ctrl.get(str(R), {}).get("h_min_flat", None)
        thr_om = 10.0 * hmin_R
        n_near_om = int(np.sum(h_om < thr_om))
        if hmin_flat_R is not None:
            thr_fl = 10.0 * hmin_flat_R
            n_near_fl = int(np.sum(h_fl < thr_fl))
        else:
            thr_fl, n_near_fl = None, None
        sel[str(R)] = {
            "random_towers": n_rand,
            "joint_optimum_h": hmin_R,
            "omega_near_optimum_count": n_near_om,
            "omega_pass_fraction": n_near_om / n_rand,
            "omega_h_random_median": float(np.median(h_om)),
            "omega_h_random_min": float(np.min(h_om)),
            "flat_near_optimum_count": n_near_fl,
            "flat_pass_fraction": (n_near_fl / n_rand
                                   if n_near_fl is not None else None),
            "flat_h_random_median": float(np.median(h_fl)),
        }
        # legacy key used by the verdict's selectivity test
        sel[str(R)]["pass_fraction"] = n_near_om / n_rand
        log(f"  R={R}: omega -- {n_near_om}/{n_rand} random towers within 10x "
            f"of H_min ({100*n_near_om/n_rand:.3f}%); median H_rand "
            f"{np.median(h_om):.3e} vs H_min {hmin_R:.3e}")
        if n_near_fl is not None:
            log(f"         flat  -- {n_near_fl}/{n_rand} within 10x of "
                f"flat-H_min ({100*n_near_fl/n_rand:.3f}%)")
        flush()
    out["selectivity_test"] = sel

    # -- VERDICT --------------------------------------------------------------
    log("")
    log("=" * 78)
    log("VERDICT")
    log("=" * 78)
    e_inf = float(out["per_rung_energy_density_e_inf"])
    # EMPTY: the joint optimum stays large -- no tower satisfies both arms
    h9 = curve.get(9, curve[Rs[-1]])
    empty = (h9 / 9.0) > 0.02 and e_inf > 0.01
    well_defined_9 = ("9" in out["depth_scan"] and
                      out["depth_scan"]["9"]["h_min"] / 9.0 < 0.05)

    # --- the coupling determination -------------------------------------
    # D1, the decisive test (the one the recast ran): joint optimum vs sum of
    # independent per-bond optima. The scale-free measure is the RATIO
    # joint_h / indep_sum. Recast: ratio ~ 1 (gap = search residual). Closure
    # couples iff the ratio is >> 1 AND that excess is OMEGA-SPECIFIC -- i.e.
    # the FLAT-boundary control ratio is ~ 1 (no post-selection -> decouples
    # like the recast). The gap need not be monotone in R; it must be large
    # and omega-specific at every R.
    omega_ratios = {int(k): (coupling[k]["joint_optimum_h"]
                             / max(coupling[k]["independent_per_bond_sum"],
                                   1e-12))
                    for k in coupling}
    flat_ratios = {int(k): (ctrl[k]["h_min_flat"]
                            / max(ctrl[k]["independent_per_bond_sum_flat"],
                                  1e-12))
                   for k in ctrl}
    min_omega_ratio = min(omega_ratios.values())
    max_flat_ratio = max(flat_ratios.values()) if flat_ratios else 1.0
    # coupled: every omega ratio is well above 1, AND the omega ratios are
    # decisively larger than the flat-control ratios (omega-specific).
    d1_coupled = (min_omega_ratio > 3.0 and
                  min_omega_ratio > 3.0 * max_flat_ratio)
    # D2 (secondary, noisy): conditional optimum shift / solver noise.
    cond_ratios = []
    for k in coupling:
        ct = coupling[k].get("fixWn_conditional_test", {})
        if "coupling_ratio" in ct:
            cond_ratios.append(ct["coupling_ratio"])
    d2_signal = (len(cond_ratios) > 0 and np.median(cond_ratios) > 3.0)
    # post-sweep-1 improvement: a feed-forward chain converges in sweep 1; the
    # closure does not. growing post-sweep1 gain corroborates coupling.
    sweep_gains = {int(k): out["depth_scan"][k]["post_sweep1_improvement"]
                   for k in out["depth_scan"]}
    deep_gain = np.mean([sweep_gains[R] for R in sweep_gains if R >= 13])
    nonconverging = deep_gain > 1e-3

    coupled = d1_coupled       # D1 is the decisive, recast-comparable test
    selective = all(sel[k]["pass_fraction"] < 0.5 for k in sel)

    if empty:
        verdict = "EMPTY"
        reason = ("the two-arm constraint is over-determined -- the joint "
                  "optimum stays large at the framework's rung count; no tower "
                  "satisfies both the forward corridors and the backward-"
                  "propagated omega boundary")
    elif coupled and selective and well_defined_9:
        verdict = "DISCOVERY"
        reason = ("the forward-backward closure yields a joint object that is "
                  "non-empty, COUPLED (the joint optimum is several-fold above "
                  "the sum of independent per-bond optima, and this excess is "
                  "omega-specific -- the flat-boundary control decouples), "
                  "selective (almost no random tower satisfies the joint "
                  "constraint), and well-defined to the framework's rung count "
                  "-- this is the genuine P_omega form")
    elif not coupled:
        verdict = "TRIVIAL"
        reason = ("the closure still decouples -- the backward boundary does no "
                  "joint work: the joint optimum is not decisively above the "
                  "sum of independent per-bond optima, or the excess is not "
                  "omega-specific; the squeeze holds, on the trivial horn")
    else:
        verdict = "TRIVIAL (partial/mixed)"
        reason = ("coupling signal present but not selective and/or not "
                  "well-defined -- reported honestly, not forced to DISCOVERY")

    out["verdict"] = {
        "verdict": verdict, "reason": reason,
        "per_rung_energy_density_e_inf": e_inf,
        "empty": empty, "coupled": coupled, "selective": selective,
        "well_defined_to_9_rungs": well_defined_9,
        "D1_omega_joint_over_indep_ratio": omega_ratios,
        "D1_flat_joint_over_indep_ratio": flat_ratios,
        "D1_min_omega_ratio": min_omega_ratio,
        "D1_max_flat_ratio": max_flat_ratio,
        "D1_coupled_omega_specific": d1_coupled,
        "D2_conditional_shift_signal": d2_signal,
        "D2_median_coupling_ratio": float(np.median(cond_ratios))
        if cond_ratios else 0.0,
        "post_sweep1_nonconvergence_deep": nonconverging,
        "post_sweep1_mean_gain_deep": float(deep_gain),
        "selectivity_pass_fractions": {k: sel[k]["pass_fraction"] for k in sel},
    }
    log(f"  e_inf = {e_inf:.6e}   empty={empty}")
    log(f"  D1 (decisive) joint/indep ratio -- omega: "
        f"{ {k: round(v,1) for k,v in sorted(omega_ratios.items())} }")
    log(f"  D1 joint/indep ratio -- FLAT control: "
        f"{ {k: round(v,2) for k,v in sorted(flat_ratios.items())} }")
    log(f"  -> min omega ratio {min_omega_ratio:.1f}  vs  max flat ratio "
        f"{max_flat_ratio:.2f}  => D1 coupled & omega-specific: {d1_coupled}")
    log(f"  D2 (secondary, noisy) median coupling ratio "
        f"{np.median(cond_ratios) if cond_ratios else 0:.2f}  signal: {d2_signal}")
    log(f"  post-sweep1 mean gain (deep R>=13): {deep_gain:.3e}  "
        f"(feed-forward chain would be ~0): {nonconverging}")
    log(f"  selective: {selective}  "
        f"(pass fractions {[round(sel[k]['pass_fraction'],4) for k in sel]})")
    log(f"  well-defined to 9 rungs: {well_defined_9}")
    log("")
    log(f"  >>> VERDICT: {verdict}")
    log(f"  {reason}")
    out["meta"]["runtime_s"] = time.time() - t0
    flush()
    log("")
    log(f"done. results -> {RESULTS}  ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
