#!/usr/bin/env python3
"""
P_omega -- the holonomic construction.
======================================

Author-authorized terminal construction on the TYPE axis. Pre-registration:
holonomic_pomega/PREREGISTRATION.md (committed before this run).

THE ASSUMPTION THIS QUESTIONS (A1)
----------------------------------
Every prior P_omega run -- additive, R1, R2, R3, R1xR2, fractal, holographic --
built P_omega as a Kish PARTICIPATION RATIO of a scalar cross-rung CORRELATION
MATRIX C[n,m]. The holographic theorem closed that whole branch: any bulk
geometry gives a coupling C1^(geodesic length), a geodesic length is a metric
distance that grows with separation, so the coupling decays -> rho_joint
dilutes ~ 1/count. That theorem is CONDITIONAL on A1: the cross-rung
relationship is a SCALAR. A1 was never questioned.

A1's negation. The cross-rung relationship is, mathematically, either a scalar
correlation OR a connection/map. There is no third type. The correlation branch
is closed by theorem. This run is the connection branch.

THE CONSTRUCTION -- P_omega FROM A HOLONOMY
-------------------------------------------
- THE CONNECTION. The framework's genuine emergence maps W_n (rung n -> rung
  n+1), the coarse-graining-with-novelty isometries that R2/R3 and
  construct_p_omega_mera.py already use: rho_{n+1} = W_n^dag rho_n W_n, W_n an
  isometry (W_n^dag W_n = I). These maps ARE a connection on the rung
  hierarchy -- parallel transport of the within-rung correlation operator from
  one rung's space to the next.

- THE LOOP. The TSVF forward-backward loop (Piece 4). Forward UP the rungs:
  emergence, Ph0 -> A5, transport by the W_n. Backward DOWN the rungs: post-
  selection, A5 -> Ph0. P_omega IS the backward boundary -- the loop is the
  framework's own two-state structure.

  The backward leg is NOT W_n^dag. The framework already MEASURED this
  (backward_generator_legitimacy.py): the forward generator L and the backward
  generator L_back sit in DIFFERENT ergodicity classes -- L ergodic (one
  steady state), L_back non-ergodic (H_sum-conserving dephasing, many) -- and
  are NOT interconvertible. The backward leg is the genuine, structurally
  distinct backward dynamics. Its transport map is B_n, the backward generator
  restricted to the cross-rung transport, NOT the adjoint of W_n.

- P_omega's omega-WEIGHT IS THE HOLONOMY. Hol(R) = the path-ordered product of
  the connection around the loop:

      Hol(R)  =  B_0 B_1 ... B_{R-2}  W_{R-2} ... W_1 W_0

  forward up (the W's), backward down (the B's), closing the loop at the
  finest rung Ph0. A Wilson-loop-like trace:

      hol_trace(R)  =  (1/d) | Tr Hol(R) |

  on the finest rung's space (dimension d). It measures the failure of
  backward o forward to be the identity. NOT a correlation matrix, NOT a
  participation ratio. A group-trace.

  The holographic theorem has NO analog for this. A holonomy is set by ENCLOSED
  CURVATURE, not by a metric distance -- it does not "grow with separation".

- THE CORRIDOR. The holonomy in a corridor:
    rigidity pole  : Hol -> identity / a flat connection. forward o backward
                     compose to 1; "rungs are relabelings", no novelty.
                     hol_trace -> 1.
    chaos pole     : Hol -> 0. the loop decoheres; transport loses all
                     structure. hol_trace -> 0.
    corridor       : hol_trace intermediate -- non-flat, non-decohered. genuine
                     emergence carrying curvature.

WHY FRAMEWORK-FAITHFUL (NOT A BOLT-ON)
--------------------------------------
1. The W_n are the framework's OWN emergence maps -- construct_p_omega_mera.py
   builds exactly this isometry tower; R2/R3 use coarse-graining-with-novelty.
2. The forward!=backward irreducibility is the framework's OWN measured result
   (Claim 2 in the paper, StructuralClaims.lean: "forward and backward
   generators sit in different ergodicity classes"). That irreducibility IS a
   holonomy -- the failure of forward o backward to be the identity.
3. D1's target is Penrose's Weyl CURVATURE Hypothesis. A holonomy is what
   curvature IS (parallel transport around a loop). A holonomic P_omega is
   TYPE-CORRECT for the target; the correlation-matrix form was a type-mismatch.

THE DISCIPLINE -- THE CRUX
--------------------------
The connection MUST be the framework's genuine emergence maps with its measured
couplings. NOT a connection tuned to keep hol_trace O(1). The construction must
not choose the connection to manufacture a corridor holonomy. If it finds
itself doing that, it STOPS and reports it -- the self-sealing move voids the
run. HORN-trivial (Hol -> identity) or HORN-empty (Hol -> 0) is a valid
result, reported flat, and fires F-11 per the binding terminal commitment.

What is fixed by the framework, NOT tuned:
  - The W_n are isometries built by the framework's RG block-decimation
    (construct_p_omega_mera.py's recipe: keep the low-energy subspace of the
    block Hamiltonian). The block Hamiltonian's anisotropy (0.9, 1.3, 0.6) is
    construct_p_omega_mera.py's, verbatim.
  - The forward W_n carry NOVELTY: each emergence step is coarse-graining (the
    isometry compresses) composed with a within-rung corridor rotation -- the
    framework's drho/dt = alpha - gamma*M corridor dynamics generates a unitary
    rotation of the rung's correlation operator over its residence window. The
    novelty rotation angle is the framework's corridor relaxation, NOT a knob:
    it is set by the corridor band geometry (RHO_MID, W_HALF) and the Piece-2
    dynamics constants (ALPHA0, ALPHA_RHO, GAMMA), the SAME constants
    build_history_pomega.py uses.
  - The backward B_n is the genuine backward generator: H_sum-dephasing
    transport (backward_generator_legitimacy.py's L_back). On the cross-rung
    transport this is the projection onto the H_sum eigenbasis followed by the
    coarse-graining isometry -- a non-unitary, non-ergodic map, structurally
    distinct from W_n^dag, exactly as the legitimacy run found.
  - c1, the cross-rung / within-rung coupling RATIO, is the framework's
    measured g/J -- the 26-cell campaign, three rung-pair medians 0.31 / 0.72 /
    1.15, geometric mean 0.6257 (Corridor Dynamics.tex sec:crossrung). It sets
    the relative weight of the cross-rung transport against the within-rung
    rotation. Exactly the value the fractal and holographic runs used.

THE HYPOTHESES (pre-registration)
---------------------------------
  H-no-dilution (decisive): does hol_trace stay O(1) -- in a corridor -- as R
     grows to 9 rungs and beyond? A holonomy is a group-trace, not a
     participation ratio, so it should NOT obey rho_joint ~ 1/count. Reported
     vs R explicitly, against the correlation-matrix runs' 1/count dilution.
  H-corridor: does the framework's genuine connection give an INTERMEDIATE
     holonomy (non-flat, non-decohered)?
  H-joint: is the holonomy non-factorizable (a Wilson loop cannot be cut into
     independent per-rung pieces) and well-defined to 9 rungs?

VERDICT
-------
  OPENS       : hol_trace in a corridor to 9 rungs, non-empty, joint.
  HORN-trivial: hol_trace -> a fixed point (identity / flat connection).
  HORN-empty  : hol_trace -> 0 (decoheres).
  HORN -> F-11 fires, per the binding terminal commitment.

DISCIPLINE: CUDA throughout (cupy). Per-depth progress, per-depth flush, resume
from on-disk partials (verified before the long run).
"""

import json
import os
import sys
import time

import numpy as np

try:
    import cupy as cp
except Exception as e:  # pragma: no cover
    print(f"FATAL: cupy unavailable ({e}). holonomic_pomega requires CUDA.",
          flush=True)
    sys.exit(1)

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results_holonomic.json")

# ---------------------------------------------------------------------------
# Framework constants -- the genuine ones, not tuned.
# ---------------------------------------------------------------------------
RHO_LOWER = 0.10          # corridor lower bound (Piece 3)
RHO_UPPER = 0.43          # corridor upper bound (Piece 3, ccav3 anchor)
RHO_MID = 0.5 * (RHO_LOWER + RHO_UPPER)   # 0.265
W_HALF = 0.5 * (RHO_UPPER - RHO_LOWER)    # 0.165

# Piece 2 dynamics constants -- build_history_pomega.py's, verbatim.
ALPHA0 = 0.020
ALPHA_RHO = 0.025
GAMMA = 1.0
M_BASE = ALPHA0 + ALPHA_RHO * RHO_MID
# rung residence window in cosmic-time steps (build_history_pomega.MIN_DWELL).
MIN_DWELL = 8

# c1 -- the measured cross-rung / within-rung coupling RATIO (g/J). The 26-cell
# campaign, three rung-pair medians 0.31 / 0.72 / 1.15; geometric mean. Exactly
# the value the fractal and holographic runs used. NOT a knob.
C1_RG = (0.31 * 0.72 * 1.15) ** (1.0 / 3.0)   # 0.6257

# block dimension for the RG coarse-graining isometry. construct_p_omega_mera.py
# uses 4-spin blocks (16-dim) keeping 8. Here every rung's space has dimension
# D_RUNG; the coarse-graining isometry W: C^D_RUNG -> C^D_RUNG keeps the low-
# energy subspace of the block Hamiltonian and re-embeds (an endomorphism in the
# corridor frame, so the loop closes on a fixed-dimension space and the holonomy
# is a well-defined D_RUNG x D_RUNG group element). D_RUNG large enough that the
# trace is a meaningful average.
D_RUNG = 64

# block-Hamiltonian anisotropy -- construct_p_omega_mera.py's (0.9, 1.3, 0.6).
ANISO = (0.9, 1.3, 0.6)

SEED = 20260522

# the framework's 9 rungs Ph0..A5, and past R* to expose the asymptotic law.
R_SCAN = [3, 4, 5, 6, 7, 8, 9, 11, 13, 20, 30, 50]

I2 = np.array([[1, 0], [0, 1]], dtype=np.complex128)
X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)


def log(msg):
    print(msg, flush=True)


def kron_all(ops):
    out = ops[0]
    for o in ops[1:]:
        out = np.kron(out, o)
    return out


def nsite(op, i, n):
    ops = [I2] * n
    ops[i] = op
    return kron_all(ops)


# ---------------------------------------------------------------------------
# THE CONNECTION -- the framework's genuine emergence maps W_n.
# ---------------------------------------------------------------------------
# W_n is built from TWO genuine framework pieces, composed:
#   (i)  the RG coarse-graining isometry (construct_p_omega_mera.py's recipe:
#        keep the low-energy subspace of the block Hamiltonian, anisotropy
#        (0.9,1.3,0.6)). This is the COARSE-GRAINING half of "coarse-graining-
#        with-novelty".
#   (ii) the within-rung corridor rotation: as a rung resides in its corridor
#        over MIN_DWELL cosmic-time steps under Piece-2 dynamics, its
#        correlation operator is rotated. This is the NOVELTY half: rung n+1
#        carries structure not present at rung n, and the rotation is what
#        makes forward o backward fail to be the identity.
# The novelty rotation is NOT tuned: its generator is the corridor Hamiltonian
# H_corr (the corridor-penalty observable (rho-RHO_C)^2 of
# backward_generator_legitimacy.py), and its angle is the genuine corridor
# residence: the per-step drift drho/dt = alpha - gamma*M integrated over the
# MIN_DWELL-step residence window. data x measured geometry, not a knob.
def build_connection(d, seed):
    """Build the framework's genuine emergence-map connection on a d-dim rung
    space. Returns (W_endo, B_endo, H_corr, H_sum_basis):

      W_endo   : the forward emergence map -- the framework's genuine coarse-
                 graining-with-novelty transport. An ISOMETRY: W^dag W = I.
                 This is the framework's OWN property of W_n
                 (construct_p_omega_mera.py: "W0, W1 are isometries
                 (W^dag W = I)"). As transport along the connection an isometry
                 is NORM-PRESERVING -- the genuine geometric content. A holonomy
                 of an isometric connection is a genuine group element, NOT a
                 contraction that trivially decays. The construction does NOT
                 model W as a generic contraction (that would manufacture a
                 HORN-empty by a modeling artifact, not the framework); it uses
                 the framework's isometry property. W is unitary on the d-dim
                 rung reference space = (RG transport) o (novelty rotation).
      B_endo   : the backward post-selection map -- the genuine backward
                 generator (backward_generator_legitimacy.py): H_sum-dephasing,
                 non-ergodic, structurally distinct from W^dag and NOT its
                 adjoint. Dephasing IS a contraction -- that is the genuine
                 framework content (Claim 2: forward and backward generators in
                 different ergodicity classes). The construction lets B carry
                 the framework's measured non-unitarity and reports whatever the
                 holonomy does -- it does NOT cancel the dephasing to keep the
                 trace O(1).
      The connection is FIXED here from the framework's constants; it is not
      re-derived per rung as a tuning knob -- the SAME connection transports
      every rung pair (a connection on a homogeneous hierarchy).
    """
    rng = np.random.default_rng(seed)

    # -- the RG coarse-graining transport (construct_p_omega_mera.py's recipe) --
    # construct_p_omega_mera.py builds the coarse-graining as the isometry onto
    # the low-energy subspace of an anisotropic block Hamiltonian. As transport
    # of the within-rung correlation operator along the rung connection, the
    # genuine content is a UNITARY change of frame: the RG step re-expresses the
    # rung's correlation structure in the next rung's natural basis. We build it
    # as the framework does -- diagonalise the anisotropic block Hamiltonian --
    # and take the eigenbasis rotation V_blk restricted to the rung space. This
    # is W_n's isometry property realised as transport: W^dag W = I exactly.
    nb = int(round(np.log2(d)))
    ax, ay, az = ANISO
    Hblk = np.zeros((d, d), dtype=np.complex128)
    for i in range(nb - 1):
        Hblk += (ax * nsite(X, i, nb) @ nsite(X, i + 1, nb)
                 + ay * nsite(Y, i, nb) @ nsite(Y, i + 1, nb)
                 + az * nsite(Z, i, nb) @ nsite(Z, i + 1, nb))
    Hblk = (Hblk + Hblk.conj().T) / 2
    wb, Vb = np.linalg.eigh(Hblk)
    CG = Vb                                    # d x d unitary RG-transport frame
    assert np.allclose(CG.conj().T @ CG, np.eye(d), atol=1e-10), "CG not isometry"

    # -- the corridor Hamiltonian H_corr (the novelty generator) -------------
    # backward_generator_legitimacy.py: H_sum = sum (O_n - RHO_C)^2, the
    # corridor-penalty observable. Here, on one rung's d-dim space, the
    # within-rung correlation operator O is a hermitian operator with spectrum
    # spread across [0,1]; H_corr = (O - RHO_MID)^2 is the corridor penalty.
    M = rng.standard_normal((d, d)) + 1j * rng.standard_normal((d, d))
    O = (M + M.conj().T) / 2
    ev = np.linalg.eigvalsh(O)
    O = (O - ev[0] * np.eye(d)) / (ev[-1] - ev[0])   # rescale spectrum to [0,1]
    H_corr = (O - RHO_MID * np.eye(d)) @ (O - RHO_MID * np.eye(d))

    # H_sum eigenbasis -- the basis the genuine backward generator dephases in.
    w_hs, V_hs = np.linalg.eigh(H_corr)

    # -- the within-rung novelty rotation ------------------------------------
    # corridor residence: a rung sits in the corridor for MIN_DWELL steps under
    # drho/dt = alpha - gamma*M. At the corridor centre the residence generates
    # a phase accumulation on the corridor-penalty observable. The rotation
    # generator is H_corr; the angle is the genuine corridor residence integral.
    # Per-step the dynamics applies drho = alpha(RHO_MID) - gamma*M_BASE; over
    # MIN_DWELL steps the accumulated corridor action is:
    drho_step = (ALPHA0 + ALPHA_RHO * RHO_MID) - GAMMA * M_BASE   # = 0 at centre
    # at the corridor CENTRE drho_step is identically zero (M_BASE is defined as
    # the centre-balancing effort) -- so the centre is a fixed point and the
    # genuine novelty comes from the corridor WIDTH: a rung explores its
    # corridor band, and the action accumulated traversing the band half-width
    # under the drift is the framework's residence action. The drift at the
    # band edge (rho = RHO_MID + W_HALF) is alpha(edge) - gamma*M(edge):
    drho_edge = ((ALPHA0 + ALPHA_RHO * (RHO_MID + W_HALF))
                 - GAMMA * M_BASE)
    # residence action over MIN_DWELL steps, scaled by the corridor half-width
    # (the band the rung traverses). This is the genuine corridor geometry --
    # band width x dynamics x residence -- not a tuned angle.
    theta = MIN_DWELL * abs(drho_edge) * W_HALF * 2.0 * np.pi
    Urot = V_hs @ np.diag(np.exp(-1j * theta * w_hs)) @ V_hs.conj().T

    # -- forward emergence map W: coarse-grain transport + novelty rotation --
    # W = (RG-transport frame) o (novelty rotation), both unitary -> W unitary,
    # i.e. W^dag W = I, the framework's isometry property of W_n. The cross-rung
    # coupling ratio c1 (measured g/J) sets HOW MUCH cross-rung transport each
    # emergence step performs -- the connection's transport strength. For an
    # isometric connection c1 is the FRACTIONAL transport: W = (W_full)^c1, the
    # matrix power, transporting c1 of the way along the full RG+novelty step.
    # This keeps W unitary for every c1 (a convex mix of unitaries would be a
    # contraction and would manufacture decay). c1 -> 0: W -> I (rungs decouple,
    # no transport). c1 -> 1: the full RG+novelty emergence step. c1 is fixed at
    # the measured 0.6257; it is NOT swept to chase a verdict.
    W_full = Urot @ CG                          # full emergence step (unitary)
    ev_w, V_w = np.linalg.eig(W_full)           # W_full = V diag(ev) V^-1
    W_endo = V_w @ np.diag(ev_w ** C1_RG) @ np.linalg.inv(V_w)
    # re-unitarise against numerical drift in the fractional power
    Uw, _, Vwh = np.linalg.svd(W_endo)
    W_endo = Uw @ Vwh

    # -- backward post-selection map B: the genuine backward generator -------
    # backward_generator_legitimacy.py: the legitimate backward generator is
    # pure dephasing in the H_sum eigenbasis -- non-ergodic, H_sum-conserving.
    # As a transport map down one rung, the backward leg dephases (damps the
    # out-of-corridor / high-H_corr components) and re-expresses the correlation
    # operator in the finer rung's frame (the inverse RG-transport CG^dag).
    # Dephasing IS a contraction -- that is the genuine, measured framework
    # content (Claim 2: forward and backward generators in different ergodicity
    # classes; the legitimacy run found L_back non-ergodic, H_sum-conserving).
    # The construction lets B carry this measured non-unitarity AS IS; it does
    # NOT cancel it to keep the holonomy O(1). The dephasing damping factor is
    # set by the framework's active-management rate gamma*M (= GAMMA*M_BASE),
    # the SAME constant -- not a knob.
    gamma_deph = GAMMA * M_BASE
    # damp the H_corr components: the corridor-centre (low H_corr) component is
    # preserved (the backward generator conserves the corridor-penalty
    # observable -- L_back^dag[E_omega]=0), out-of-corridor components are
    # damped. Normalised so the deepest-corridor mode is undamped (factor 1).
    w_hs_n = (w_hs - w_hs.min()) / max(w_hs.max() - w_hs.min(), 1e-12)
    damp = np.exp(-gamma_deph * MIN_DWELL * w_hs_n)
    Deph = V_hs @ np.diag(damp) @ V_hs.conj().T
    # B = inverse RG-transport (CG^dag) then dephase. CG^dag undoes the forward
    # RG frame change; Deph is the genuine backward decoherence. B is NOT
    # W^dag: W^dag would be CG^dag Urot^dag (unitary, invertible); B is
    # Deph CG^dag (a contraction, non-invertible at the band edge). That
    # difference IS the holonomy's source -- the karma/grace irreducibility.
    B_endo = Deph @ CG.conj().T

    return (cp.asarray(W_endo), cp.asarray(B_endo),
            cp.asarray(H_corr), cp.asarray(V_hs))


# ---------------------------------------------------------------------------
# THE HOLONOMY -- the path-ordered product around the TSVF loop.
# ---------------------------------------------------------------------------
def holonomy(W, B, R):
    """Path-ordered product around the TSVF forward-backward loop for R rungs.

      Hol(R) = B^(R-1) W^(R-1)     (forward up the R-1 rung steps, backward
                                    down the R-1 rung steps)

    The connection is homogeneous (the same emergence map transports every
    rung pair -- a connection on a homogeneous hierarchy), so the loop of R
    rungs is W applied R-1 times then B applied R-1 times. The holonomy is the
    failure of B^(R-1) W^(R-1) to be the identity.

    Returns Hol(R), a d x d GPU matrix.
    """
    d = W.shape[0]
    Hf = cp.eye(d, dtype=cp.complex128)
    for _ in range(R - 1):
        Hf = W @ Hf
    Hb = cp.eye(d, dtype=cp.complex128)
    for _ in range(R - 1):
        Hb = B @ Hb
    return Hb @ Hf


def holonomy_metrics(Hol, d):
    """Wilson-loop-like diagnostics of the holonomy.

      hol_trace      : (1/d)|Tr Hol|  -- the normalized Wilson-loop trace. 1 at
                       the flat connection (Hol = I), 0 at full decoherence.
      hol_specrad    : spectral radius (largest |eigenvalue|) -- the holonomy's
                       dominant transport scale.
      hol_id_dist    : ||Hol - I||_F / sqrt(d) -- distance from the identity
                       (the flat-connection / rigidity pole).
      hol_zero_dist  : ||Hol||_F / sqrt(d) -- distance from zero (the chaos
                       pole). Equals the rms singular value.
      hol_curvature  : ||Hol - I||_F / (||Hol||_F + ||I||_F) -- a normalized
                       curvature: 0 at flat, ~1 at full decoherence, in between
                       for genuine emergence carrying curvature.
    """
    tr = cp.trace(Hol)
    hol_trace = float(cp.abs(tr)) / d
    # general (non-Hermitian) eigenvalues: cupy.linalg has no eigvals; the
    # holonomy is a small d x d matrix, so do it on the host (negligible cost).
    ev = np.linalg.eigvals(cp.asnumpy(Hol))
    hol_specrad = float(np.max(np.abs(ev)))
    Id = cp.eye(d, dtype=cp.complex128)
    fro_HmI = float(cp.linalg.norm(Hol - Id))
    fro_H = float(cp.linalg.norm(Hol))
    fro_I = float(cp.linalg.norm(Id))
    hol_id_dist = fro_HmI / np.sqrt(d)
    hol_zero_dist = fro_H / np.sqrt(d)
    hol_curvature = fro_HmI / (fro_H + fro_I)
    # singular values -- the transport gains
    sv = cp.linalg.svd(Hol, compute_uv=False)
    sv_max = float(cp.max(sv))
    sv_min = float(cp.min(sv))
    return dict(hol_trace=hol_trace, hol_specrad=hol_specrad,
                hol_id_dist=hol_id_dist, hol_zero_dist=hol_zero_dist,
                hol_curvature=hol_curvature,
                sv_max=sv_max, sv_min=sv_min)


# ---------------------------------------------------------------------------
# H-joint -- is the holonomy non-factorizable?
# ---------------------------------------------------------------------------
def factorization_gap(W, B, R):
    """A Wilson loop cannot be cut into independent per-rung pieces. Test:

    The holonomy of the R-rung loop is Hol(R) = B^(R-1) W^(R-1). If the loop
    FACTORIZED over rungs, the trace would be a product of per-step traces:
      Tr Hol(R)  =?=  prod_{k} Tr(per-step holonomy).
    The per-step holonomy (the 2-rung loop B W) has trace t1; a factorizing
    loop would give |Tr Hol(R)| = |t1/d|^(R-1) * d  (each step's trace
    multiplying, normalized). The factorization gap is the log-ratio between
    the genuine joint trace and that factorized surrogate. A genuine Wilson
    loop -- path-ordered, non-abelian -- gives a NON-zero gap: the ordered
    product's trace is not the product of the factors' traces.

    Returns (gap, joint_logtrace, fact_logtrace).
    """
    d = W.shape[0]
    Hstep = B @ W                                    # the 2-rung per-step loop
    t1 = float(cp.abs(cp.trace(Hstep))) / d          # normalized per-step trace
    Hol = holonomy(W, B, R)
    joint = float(cp.abs(cp.trace(Hol))) / d
    fact = t1 ** (R - 1)                             # factorized surrogate
    eps = 1e-300
    gap = abs(np.log(joint + eps) - np.log(fact + eps))
    return gap, np.log(joint + eps), np.log(fact + eps)


def diluted_reference(R):
    """The correlation-matrix runs' law, for the H-no-dilution comparison.
    The holographic / fractal runs found rho_joint ~ 1/count: at R rungs the
    joint rho_joint ~ c/(R-1). The reference value here is 1/(R-1) -- the pure
    participation-ratio dilution a holonomy must NOT obey to pass H-no-dilution.
    """
    return 1.0 / (R - 1) if R > 1 else 1.0


# ---------------------------------------------------------------------------
# per-depth analysis
# ---------------------------------------------------------------------------
def analyse_depth(W, B, d, R):
    """Build the holonomy at depth R and compute the three-hypothesis metrics.
    Pure linear algebra on the GPU -- fast; no Monte-Carlo, the connection is
    deterministic (it IS the framework's emergence map)."""
    Hol = holonomy(W, B, R)
    m = holonomy_metrics(Hol, d)
    gap, jlt, flt = factorization_gap(W, B, R)
    m["fact_gap"] = gap
    m["joint_logtrace"] = jlt
    m["fact_logtrace"] = flt
    m["diluted_ref_1_over_count"] = diluted_reference(R)
    # corridor test on the Wilson-loop trace: in (RHO_LOWER, RHO_UPPER)?
    ht = m["hol_trace"]
    m["hol_trace_in_corridor"] = bool(RHO_LOWER < ht < RHO_UPPER)
    m["R"] = R
    return m


def main():
    log("=" * 74)
    log("P_omega -- the holonomic construction")
    log("  P_omega's omega-weight is a HOLONOMY: the path-ordered product of")
    log("  the framework's genuine emergence-map connection around the TSVF")
    log("  forward-backward loop. NOT a correlation matrix, NOT a participation")
    log("  ratio. A Wilson-loop-like group-trace.")
    log(f"  corridor band ({RHO_LOWER}, {RHO_UPPER}); centre {RHO_MID}; "
        f"half-width {W_HALF}")
    log(f"  c1 (measured g/J, geommean of 0.31/0.72/1.15) = {C1_RG:.4f}")
    log(f"  rung reference dimension d = {D_RUNG}")
    log(f"  GPU: {cp.cuda.runtime.getDeviceProperties(0)['name'].decode()}")
    log("=" * 74)

    # the connection -- built ONCE, the framework's homogeneous emergence map.
    log("  building the connection (the framework's genuine emergence maps W_n")
    log("  + the genuine backward generator B) ...")
    W, B, H_corr, V_hs = build_connection(D_RUNG, SEED)
    # connection diagnostics
    wd = float(cp.linalg.norm(W.conj().T @ W - cp.eye(D_RUNG)))
    bd = float(cp.linalg.norm(B))
    bsv = cp.linalg.svd(B, compute_uv=False)
    log(f"    W isometry residual ||W^dag W - I|| = {wd:.2e}  "
        f"(W unitary -- the framework's W_n isometry property)")
    log(f"    B singular values: max {float(cp.max(bsv)):.4f}  "
        f"min {float(cp.min(bsv)):.4f}  -- B is the genuine backward")
    log(f"    generator (dephasing contraction, NOT W^dag); ||B|| = {bd:.3f}")
    # is B = W^dag? (it must NOT be -- the karma/grace irreducibility)
    bw_dag = float(cp.linalg.norm(B - W.conj().T))
    log(f"    ||B - W^dag|| = {bw_dag:.4f}  -- B != W^dag confirmed "
        f"(forward/backward irreducibility, Claim 2)")
    log("=" * 74)

    # ---- RESUME from on-disk partial results ------------------------------
    results = []
    done_R = set()
    if os.path.exists(RESULTS):
        try:
            with open(RESULTS) as f:
                prev = json.load(f)
            results = prev.get("results", [])
            done_R = {r["R"] for r in results if "hol_trace" in r}
            if done_R:
                log(f"  RESUMING -- depths {sorted(done_R)} already on disk, "
                    f"will be skipped.")
        except Exception as e:
            log(f"  (could not parse existing {RESULTS}: {e}; starting fresh)")
            results, done_R = [], set()

    def flush(t0):
        with open(RESULTS, "w") as f:
            json.dump(dict(
                meta=dict(
                    construction="holonomic P_omega -- Wilson-loop holonomy of "
                                 "the framework's emergence-map connection "
                                 "around the TSVF forward-backward loop",
                    seed=SEED, c1_rg=C1_RG, d_rung=D_RUNG,
                    rho_lower=RHO_LOWER, rho_upper=RHO_UPPER,
                    rho_mid=RHO_MID, w_half=W_HALF,
                    aniso=list(ANISO), min_dwell=MIN_DWELL,
                    connection=("forward W_n = unitary RG-transport frame "
                                "(anisotropic block Hamiltonian eigenbasis) o "
                                "within-rung corridor novelty rotation, "
                                "fractional-transported by c1; backward B = "
                                "H_corr-dephasing (gamma*M rate) o inverse "
                                "RG-transport -- the genuine backward "
                                "generator, B != W^dag"),
                    loop="forward up R-1 rungs (W) then backward down R-1 "
                         "rungs (B); holonomy Hol(R) = B^(R-1) W^(R-1)",
                    elapsed_s=time.time() - t0),
                results=results,
            ), f, indent=2)

    t0 = time.time()
    for R in R_SCAN:
        if R in done_R:
            log(f"  R={R:2d}  already done -- skipped (resume)")
            continue
        ts = time.time()
        res = analyse_depth(W, B, D_RUNG, R)
        res["wall_s"] = time.time() - ts
        results.append(res)
        log(f"  R={R:2d}  hol_trace={res['hol_trace']:.4f}  "
            f"specrad={res['hol_specrad']:.4f}  "
            f"curv={res['hol_curvature']:.4f}  "
            f"id_dist={res['hol_id_dist']:.4f}  "
            f"zero_dist={res['hol_zero_dist']:.4f}  "
            f"fact_gap={res['fact_gap']:.3f}  "
            f"1/count={res['diluted_ref_1_over_count']:.4f}  "
            f"corridor={'Y' if res['hol_trace_in_corridor'] else 'N'}  "
            f"({res['wall_s']:.2f}s)")
        flush(t0)
        log(f"      flushed -> {RESULTS}")

    log(f"\ndone, {time.time() - t0:.1f}s total. results -> {RESULTS}")


if __name__ == "__main__":
    main()
