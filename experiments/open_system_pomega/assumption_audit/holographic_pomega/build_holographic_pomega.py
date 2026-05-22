#!/usr/bin/env python3
"""
P_omega — the holographic construction.
=======================================

Author-authorized terminal construction on the topology axis. Pre-registration:
holographic_pomega/PREREGISTRATION.md (committed before this run). This is the
BINARY COMPLEMENT of the fractal run: the fractal run tested every scale-
DECAYING cross-rung coupling (chain, RG-flow Toeplitz c1^|n-m|, ultrametric
binary tree c1^treedist) and all diluted -- rho_joint ~ R^-1.1, k_eff extensive,
joint corridor empty past R~5. It pinned the escape: the only topology that
breaks the dilution is NON-decaying -- per-rung off-diagonal mass growing with
R. It dismissed that as "non-framework all-to-all". This construction tests
whether the genuine holographic / MERA-as-AdS geometry IS that non-decaying
topology, or whether holding the framework's constraints forces it back to
dilution (EMPTY) or to rigidity (also EMPTY).

THE DISCIPLINE -- THE CRUX
--------------------------
A non-decaying all-to-all matrix trivially does not dilute. Imposing one and
reporting OPENS is the self-sealing move and is FORBIDDEN -- it voids the run.
So the cross-rung coupling here is NOT written down as a non-decaying matrix.
It is DERIVED, tensor by tensor, from the genuine MERA tensor network -- the
framework's own holographic structure (construct_p_omega_mera.py builds the
MERA isometry tower; Swingle: MERA is a discrete slice of an AdS geometry).

The genuine holographic structure, stated precisely
----------------------------------------------------
A MERA is a layered tensor network. Layer d is a scale; the framework's rungs
Ph0..A5 are the scales. The defining holographic fact of a MERA is the CAUSAL
CONE: a bulk tensor at depth d sits in the past causal cone of a contiguous
block of boundary sites, and -- reading the network from the boundary inward --
each rung (scale) n has a causal cone that REACHES INTO THE BULK and OVERLAPS
the causal cones of other rungs.

Two rungs n and m do NOT couple by a single boundary-to-boundary path (that
path, going up the bulk and back down, has length ~|n-m| and gives the
geometric decay c1^|n-m| -- exactly the fractal run's rgflow Toeplitz, which
diluted). They couple through the bulk vertices their causal cones SHARE. The
holographic cross-rung coupling between rung n and rung m is therefore

    C_holo[n,m]  =  (overlap of the bulk causal cones of rung n and rung m)
                    weighted by the bulk correlation each shared vertex carries.

This is the genuine MERA structure -- it is NOT imposed, it is the causal-cone
overlap of the actual network. Whether it decays with |n-m| or not is NOT a
choice: it is a property of the AdS bulk geometry, which the construction
builds explicitly and measures.

The bulk geometry and why the cone overlap does not vanish
-----------------------------------------------------------
The MERA bulk is a hyperbolic (AdS) tiling. A rung at scale n is a boundary
region; its causal cone is the set of bulk tensors causally connected to it.
In a binary MERA the cone of a scale-n region of width w contains O(w) tensors
at scale 0, O(w/2) at scale 1, ..., reaching up to depth ~log w. Crucially the
COARSEST (deepest-bulk) tensors are in the cone of EVERY rung -- the bulk
"center" of AdS is shared by the whole boundary. So the cone-overlap of rung n
and rung m is dominated by the shared deep-bulk vertices, and the count of
shared vertices does NOT go to zero with |n-m|: it saturates at the deep-bulk
core. That is the holographic non-locality, and it is bulk-geometric, derived,
not imposed.

The construction builds the actual MERA tensor network for an R-scale tower,
extracts each rung's causal cone by walking the network, and forms C_holo[n,m]
as the genuine cone-overlap correlation. Then it carries that C_holo into the
R1xR2 joint Kish functional, exactly as the fractal run carried its template.

THE TWO-SIDED TEST (pre-registration)
-------------------------------------
(a) tau in corridor. tau_(n,n+1) -- the cross-rung MUTUAL INFORMATION,
    I(R_n;R_{n+1})/min(H_n,H_{n+1}) (Piece 6) -- must sit IN the cross-rung
    corridor (tau_lower,tau_upper) = (0.10,0.43) (RungHierarchy.lean: the
    cross-rung corridor uses the same bounds as the within-rung corridor) at
    EVERY scale-step. A holographic structure that achieves non-decay only by
    driving tau->1 (pure containment = the rigidity pole) FAILS.
(b) rho_joint non-diluting. With (a) held, does rho_joint stay bounded off the
    chaos pole to the framework's 9 rungs and beyond?

HYPOTHESES
----------
  H-holo (decisive): the genuine holographic structure threads BOTH (a) tau in
     corridor at every scale AND (b) rho_joint non-diluting.
  H1 (segment-shuffle): the non-additive functional does not factorize.
  H3 (joint work): non-empty, selective, well-defined to 9 rungs.

VERDICT
-------
  OPENS  : H-holo AND H1 AND H3.
  EMPTY  : tau-in-corridor forces decay back in -> rho_joint dilutes; OR
           non-decay is bought only by tau->1 (rigidity).
  TRIVIAL: the functional factorizes; OR no-dilution was achieved only by a
           tautologically-imposed all-to-all matrix (self-sealing -- voids it).

DISCIPLINE
----------
CUDA throughout (cupy). Per-depth progress printed, results flushed per depth,
resume from on-disk partials (verified before the long run). The holographic
structure is DERIVED from the genuine MERA tensor network, NOT imposed. EMPTY
or TRIVIAL fires F-11 per the binding terminal commitment -- reported flat.
"""

import json
import os
import sys
import time

import numpy as np

try:
    import cupy as cp
except Exception as e:  # pragma: no cover
    print(f"FATAL: cupy unavailable ({e}). holographic_pomega requires CUDA.",
          flush=True)
    sys.exit(1)

# R2's sequential-emergence simulator, reused unchanged -- the SAME module the
# R1xR2 conjunction and the fractal run reused.
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "R1xR2_conjunction"))
import build_history_pomega as B

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results_holographic.json")

RHO_LOWER = B.RHO_LOWER          # 0.10  (Piece 3)
RHO_UPPER = B.RHO_UPPER          # 0.43  (Piece 3)
RHO_MID = B.RHO_MID              # 0.265 corridor centre
W_HALF = B.W_HALF                # 0.165 corridor half-width
SEED = B.SEED

# the cross-rung corridor -- RungHierarchy.lean: tau corridor membership is
#   rho_lower < tau_cross < rho_upper
# i.e. the SAME bounds as the within-rung corridor. Not a separate calibration.
TAU_LOWER = RHO_LOWER            # 0.10
TAU_UPPER = RHO_UPPER            # 0.43

# the framework's 9 rungs Ph0..A5, and past R* to expose the asymptotic law.
R_SCAN = [3, 4, 5, 6, 7, 8, 9, 11, 13, 20]
N_BY_R = {3: 400_000, 4: 400_000, 5: 600_000, 6: 800_000, 7: 1_000_000,
          8: 1_400_000, 9: 2_000_000, 11: 4_000_000, 13: 8_000_000,
          20: 20_000_000}
CHUNK = 40_000

# C1_RG -- the per-scale-step holographic correlation contraction. NOT a free
# knob: it is the framework's MEASURED adjacent cross-rung / within-rung
# coupling ratio. The 26-cell g/J campaign (Corridor Dynamics.tex
# sec:crossrung) found O(1), three rung-pair medians 0.31 / 0.72 / 1.15. The
# geometric mean is the framework-faithful single number. Held FIXED -- exactly
# the value the fractal run used, so the only change from the fractal run is
# the topology, nothing else. (The trajectory's own cross-rung correlation,
# soft(rvia), additionally multiplies every entry -- data x measured geometry.)
C1_RG = (0.31 * 0.72 * 1.15) ** (1.0 / 3.0)   # = 0.6257 -- measured, fixed.


def log(msg):
    print(msg, flush=True)


def soft(r, beta):
    """Graded corridor-band membership weight in [0,1] -- the within-rung
    corridor cap as a soft TSVF post-selection factor (R1xR2's `soft`)."""
    return cp.exp(-beta * (cp.nan_to_num(r, nan=2.0) - RHO_MID) ** 2)


# ===========================================================================
# THE GENUINE MERA-AS-AdS HOLOGRAPHIC TOPOLOGY -- derived, not imposed.
# ===========================================================================
#
# A binary MERA over an R-scale tower. The boundary has L = 2^(R-1) sites; the
# bulk is the binary coarse-graining tree -- depth d has 2^(R-1-d) tensors,
# d = 0 (finest boundary) .. R-1 (coarsest, the single deep-bulk core tensor).
# A "rung" n is the set of bulk tensors AT scale d=n. (This is exactly
# construct_p_omega_mera.py's tower H_0 -> H_1 -> ... read as a binary tree.)
#
# THE CAUSAL CONE. In a MERA the causal cone of a bulk tensor v at depth d is
# the set of bulk tensors causally connected to v on the way to the boundary.
# Reading it the other way: a bulk tensor v at depth d is IN THE CAUSAL CONE of
# every boundary site that v coarse-grains, i.e. v is shared by 2^d boundary
# sites. Equivalently the rung at scale n and the rung at scale m share a bulk
# tensor whenever a depth-d tensor lies in the past cone of both -- and the
# deep-bulk tensors (large d), each coarse-graining a large boundary block, lie
# in the past cone of an exponentially-large boundary region, hence in the cone
# of EVERY rung. The AdS "center" is shared by the whole boundary.
#
# THE DERIVED CROSS-RUNG COUPLING. C_holo[n,m] is the genuine causal-cone
# overlap of rung n and rung m, bulk-geometrically weighted. We build it
# directly from the network:
#
#   - Walk the binary tree. For each depth d (0..R-1) the tree has 2^(R-1-d)
#     bulk tensors. Each tensor v at depth d is in the causal cone of the
#     contiguous boundary block of 2^d sites it coarse-grains.
#   - Rung n's "footprint" in the bulk is the set of tensors at depth n.
#   - The HOLOGRAPHIC correlation that rung n and rung m exchange is mediated
#     by the bulk tensors whose causal cones contain BOTH a rung-n tensor and a
#     rung-m tensor. The deepest such shared tensor is the lowest common bulk
#     ancestor; the correlation it carries is set by the BULK geodesic, i.e.
#     the proper distance through the hyperbolic bulk between rung n's footprint
#     and rung m's footprint.
#
#   In AdS, the bulk proper distance between two boundary regions is the length
#   of the connecting GEODESIC. For two scales n,m the connecting geodesic dips
#   to the depth of their common bulk ancestor and the geodesic length is
#       L_geo(n,m) = (n - d_anc) + (m - d_anc)
#   where d_anc is the depth of the deepest bulk tensor shared by both rungs'
#   cones. The holographic correlation along a geodesic of length L is the
#   bulk two-point function ~ C1_RG^L (each bulk step contracts by the measured
#   per-step factor C1_RG -- the same RG factor the fractal run used).
#
#   THE DECISIVE DIFFERENCE FROM THE FRACTAL RUN. The fractal run set the
#   coupling = c1^(scale-distance) with scale-distance the BOUNDARY-to-boundary
#   path, which always has length |n-m| (rgflow) or treedist (ultrametric) and
#   always grows with separation -> geometric decay -> dilution. The holographic
#   coupling is c1^(BULK geodesic length to the SHARED ancestor). The shared
#   ancestor is NOT at the boundary: deep-bulk tensors are in EVERY rung's cone,
#   so for the deep-bulk-mediated channel d_anc is large and L_geo is SMALL even
#   for distant rungs. This is the holographic non-locality: the AdS bulk
#   center couples all rungs at O(1) strength regardless of boundary separation.
#
#   We do NOT impose "C_holo[n,m] = const". We COMPUTE, for the genuine binary-
#   MERA bulk, the full set of shared bulk ancestors of rungs n and m and SUM
#   the geodesic-weighted contributions over all of them. Whether the sum
#   decays with |n-m| or not falls out of the bulk geometry. It is then run
#   through the two-sided test: tau (mutual information per scale-step) must
#   stay in (0.10,0.43), and rho_joint must be measured against the fractal
#   baseline. If C_holo turns out non-decaying ONLY because it has collapsed to
#   an all-to-all O(1) matrix, the tau test catches it (tau -> tau_upper) and
#   the verdict is EMPTY, not OPENS.


def mera_causal_cone_overlap(R):
    """Build the genuine binary-MERA bulk and return the holographic cross-rung
    coupling template C_holo[n,m] in [0,1] -- the causal-cone-overlap geodesic-
    weighted correlation between rung n (scale n) and rung m (scale m),
    DERIVED from the actual tensor network, not imposed.

    The binary MERA over R scales: boundary L = 2^(R-1) sites; depth d has
    2^(R-1-d) bulk tensors; tensor j at depth d coarse-grains boundary block
    [j*2^d, (j+1)*2^d). Rung n's footprint = the 2^(R-1-n) tensors at depth n.

    The holographic coupling rung n <-> rung m:
      For every ORDERED pair of bulk tensors (v_n at depth n, v_m at depth m),
      their LOWEST COMMON ANCESTOR in the binary tree is a bulk tensor at some
      depth d_anc >= max(n,m). That ancestor is the deepest bulk vertex in the
      causal cone of BOTH v_n and v_m -- the holographic channel connecting them.
      The connecting bulk geodesic dips from depth n up to d_anc and back to
      depth m: geodesic length L = (d_anc - n) + (d_anc - m). The bulk two-point
      function along it is C1_RG^L. C_holo[n,m] is the MEAN over all such tensor
      pairs of C1_RG^L -- the genuine cone-overlap correlation, normalised to a
      per-pair coupling so it is comparable to the boundary template.

    Returns an (R,R) GPU float64 array, zero diagonal.

    DERIVED, NOT IMPOSED: the only inputs are the binary-tree connectivity (the
    framework's MERA tower) and C1_RG (the measured per-step contraction). The
    decay-or-not of C_holo with |n-m| is a computed property of the AdS bulk.
    """
    # Boundary site count. Cap the explicit per-site walk: for large R the
    # block structure is exact and self-similar, so we walk it analytically.
    # For a binary tree, a tensor at depth d_anc is the LCA of a depth-n tensor
    # and a depth-m tensor iff the two tensors descend from different children
    # of the ancestor (or, for the deepest, the ancestor itself sits above
    # both footprints). The COUNT of (v_n, v_m) pairs whose LCA is at depth
    # d_anc, and the geodesic length, are both pure functions of (n,m,d_anc).
    #
    # Number of depth-n tensors under one depth-d_anc tensor: 2^(d_anc - n).
    # Number of depth-m tensors under it: 2^(d_anc - m). Pairs whose LCA is
    # EXACTLY this ancestor (not a deeper descendant ancestor): those where the
    # two tensors lie under DIFFERENT children of the ancestor -- for the LCA
    # to be the ancestor itself and not one of its two children. Standard
    # binary-tree LCA combinatorics:
    #   pairs with LCA at depth a, for footprints at depths n,m (a > n, a > m):
    #     N_a = 2 * 2^(a-1-n) * 2^(a-1-m)   (the factor 2 = two child orderings,
    #           each footprint tensor under a different child)
    #   pairs with LCA exactly at depth a = n (only when n == m == a not needed;
    #           handled by the a > n,m branch and the a == max branch below).
    # The geodesic length for an ancestor at depth a is L = (a-n)+(a-m).
    # C_holo[n,m] = (sum over a of N_a * C1_RG^L) / (sum over a of N_a)
    #             = the genuine cone-overlap-averaged bulk two-point function.
    #
    # The top of the tree is depth R-1 (the single deep-bulk core tensor): it
    # is the LCA of any pair not sharing a shallower ancestor, and it is in the
    # cone of EVERY rung -- this is the AdS-center channel.
    C = np.zeros((R, R), dtype=np.float64)
    for n in range(R):
        for m in range(R):
            if n == m:
                continue
            lo, hi = min(n, m), max(n, m)
            # ancestors live at depths a in [hi, R-1]: an ancestor must be at
            # or below the deeper of the two footprints (a depth-a tensor can
            # only be an ancestor of a depth-n tensor if a >= n).
            num = 0.0
            den = 0.0
            for a in range(hi, R):
                # count of (v_n, v_m) tensor pairs whose lowest common ancestor
                # sits exactly at depth a.
                if a == hi:
                    # the ancestor is at the depth of the deeper footprint:
                    # the deeper-footprint tensor IS the ancestor; the shallower
                    # one is any of its 2^(a-lo) depth-lo descendants. count of
                    # depth-a tensors = 2^(R-1-a).
                    cnt = (2.0 ** (R - 1 - a)) * (2.0 ** (a - lo))
                else:
                    # ancestor strictly deeper than both footprints: the two
                    # tensors sit under different children of the depth-a
                    # ancestor. depth-a tensors: 2^(R-1-a). under one child
                    # (depth a-1 subtree): 2^(a-1-lo) depth-lo tensors and
                    # 2^(a-1-hi) depth-hi tensors. two child-orderings.
                    cnt = ((2.0 ** (R - 1 - a))
                           * 2.0
                           * (2.0 ** (a - 1 - lo))
                           * (2.0 ** (a - 1 - hi)))
                L_geo = (a - n) + (a - m)
                w = C1_RG ** L_geo
                num += cnt * w
                den += cnt
            C[n, m] = num / den if den > 0 else 0.0
    return cp.asarray(C)


def coupling_matrix_template(R, topology):
    """Cross-rung coupling-decay template T[n,m] in [0,1].

    'chain'      : T[n,m] = 1 if |n-m|==1 else 0       (R1xR2 baseline)
    'rgflow'     : T[n,m] = C1_RG^|n-m|                (fractal-run baseline,
                   the steepest-comparable decaying topology)
    'holographic': T[n,m] = the genuine MERA causal-cone-overlap coupling,
                   derived from the AdS bulk geometry by
                   mera_causal_cone_overlap.

    chain and rgflow are recomputed here as the in-run DECAYING baselines so
    H-holo is read directly against them. Returned as a GPU float64 (R,R)."""
    if topology == "chain":
        T = np.zeros((R, R))
        for n in range(R - 1):
            T[n, n + 1] = T[n + 1, n] = 1.0
        return cp.asarray(T)
    if topology == "rgflow":
        idx = np.arange(R)
        k = np.abs(idx[:, None] - idx[None, :]).astype(np.float64)
        T = C1_RG ** k
        np.fill_diagonal(T, 0.0)
        return cp.asarray(T)
    if topology == "holographic":
        return mera_causal_cone_overlap(R)
    raise ValueError(topology)


# ===========================================================================
# THE JOINT FUNCTIONAL -- R1xR2's joint Kish functional, verbatim. The ONLY
# change from the fractal run is which template coupling_matrix_template
# returns. The functional below is byte-for-byte the fractal run's.
# ===========================================================================
def joint_rho_history(rtf, rvia, beta, T_template):
    """The holographic omega-weight. R1's joint Kish participation ratio carried
    on R2's history frame, with the within-rung corridor cap re-injected -- all
    exactly as R1xR2 / the fractal run. The ONE change is that the cross-rung
    coupling template is the holographic causal-cone-overlap matrix.

    Inputs (GPU arrays, all-emerged histories only):
      rtf        : (K, R)    rung rho at t_f
      rvia       : (K, R-1)  rho of rung n at the step rung n+1 emerged
      beta       : corridor-referenced sharpness 1/2w^2
      T_template : (R, R)    the cross-rung coupling template (GPU)

    Returns (log_w, rho_joint, k_eff_joint) -- all (K,) GPU arrays.
    """
    K, R = rtf.shape
    CMAX = float(RHO_UPPER)

    w = soft(rtf, beta)                                  # (K, R)
    sw = cp.sqrt(cp.clip(w, 1e-12, 1.0))                 # (K, R) = diag(D)

    C = cp.zeros((K, R, R), dtype=cp.float64)
    diag_idx = cp.arange(R)
    C[:, diag_idx, diag_idx] = 1.0

    if R > 1:
        cross_bond = soft(rvia, beta)                    # (K, R-1) in [0,1]
        logb = cp.log(cp.clip(cross_bond, 1e-12, 1.0))   # (K, R-1)
        prefix = cp.zeros((K, R), dtype=cp.float64)
        prefix[:, 1:] = cp.cumsum(logb, axis=1)
        n_i = cp.arange(R)
        span_bonds = cp.abs(n_i[:, None] - n_i[None, :])           # (R,R)
        span_bonds_safe = cp.clip(span_bonds, 1, None)
        span_logsum = -cp.abs(prefix[:, None, :] - prefix[:, :, None])
        geom = cp.exp(span_logsum / span_bonds_safe[None, :, :])   # (K,R,R)
        cross_full = CMAX * geom * T_template[None, :, :]          # (K,R,R)
        offdiag = (span_bonds > 0)
        C = cp.where(offdiag[None, :, :], cross_full, C)

    Cw = C * sw[:, :, None] * sw[:, None, :]             # (K, R, R) = D C D

    trCw = cp.einsum('knn->k', Cw)                       # Tr C_w
    trCw2 = cp.einsum('knm,kmn->k', Cw, Cw)              # Tr(C_w^2)
    k_eff_joint = (trCw * trCw) / cp.clip(trCw2, 1e-300, None)
    if R > 1:
        rho_joint = (R / k_eff_joint - 1.0) / (R - 1.0)
    else:
        rho_joint = cp.zeros(K)

    sharp = 40.0
    rise = 1.0 / (1.0 + cp.exp(-sharp * (rho_joint - RHO_LOWER)))
    fall = 1.0 / (1.0 + cp.exp(-sharp * (RHO_UPPER - rho_joint)))
    e_omega = rise * fall
    log_w = cp.log(cp.clip(e_omega, 1e-300, None))
    return log_w, rho_joint, k_eff_joint


# ===========================================================================
# TAU -- the cross-rung MUTUAL INFORMATION (Piece 6), the two-sided test (a).
# ===========================================================================
def tau_per_scale(rtf, rvia, beta, T_template, R):
    """tau_(n,n+1) for every adjacent rung pair -- the test-(a) coordinate.

    Piece 6 / RungHierarchy.lean: tau_(n,n+1) = I(R_n;R_{n+1}) / min(H_n,H_{n+1}),
    the normalised cross-rung mutual information. The corridor for tau is
    (TAU_LOWER, TAU_UPPER) = (0.10, 0.43).

    The construction's rungs are correlation observables, not raw signals; the
    operative joint object is the corridor-weighted rung-correlation matrix C_w.
    For an adjacent pair (n,n+1) the cross-rung mutual information is read off
    the 2x2 sub-block of the *population* corridor-weighted correlation matrix,
    Gaussian-MI form:
        I = -1/2 log(1 - r^2),   H_n = -1/2 log(1 - <within-rung structure>)...
    -- but the framework-faithful, estimator-free reading is the normalised
    mutual information of two unit-variance Gaussians with correlation r:
        I(r)          = -1/2 log(1 - r^2)
        H of a unit-variance Gaussian is a constant; min(H_n,H_{n+1}) cancels
        the absolute scale, leaving tau a normalised function of the cross-rung
        correlation r and the within-rung correlations.
    We use the operational definition consistent with the path1_tau campaign
    (crossrung_lib.cross_rung_tau): tau is the cross-rung Gaussian mutual
    information normalised by the smaller marginal entropy, computed here from
    the ensemble correlation structure the construction actually produces.

    Concretely, per adjacent pair (n,n+1), over the post-selected ensemble:
      r_cross   = mean off-diagonal coupling C_w[n,n+1] (the cross-rung
                  correlation the holographic template carries)
      r_within  = a within-rung correlation scale = mean diagonal weight,
                  i.e. the corridor weight w_n (the rung's internal coherence).
    tau is then the normalised mutual information
        tau = I(r_cross) / min( I_n^self , I_{n+1}^self )-referenced scale,
    operationalised as the Gaussian-MI ratio
        tau_(n,n+1) = I(r_cross) / ( I(r_cross) + H_min_ref )
    with H_min_ref the marginal-entropy reference. To stay estimator-free and
    Piece-6-faithful we report tau as the *normalised* coupling: the fraction
    of the smaller rung's information that is shared. For unit-variance
    Gaussians this is
        tau_(n,n+1) = I(r_cross) / H_unit ,  H_unit = 1/2 log(2 pi e),
    clamped to [0,1] -- a monotone, parameter-free map from the cross-rung
    correlation to the Piece-6 normalised mutual information.

    Returns tau_mean (R-1,) and tau_min/tau_max scalars over the ensemble,
    plus the population-level tau computed from the mean C_w.
    """
    K, _ = rtf.shape
    w = soft(rtf, beta)                                  # (K,R)
    sw = cp.sqrt(cp.clip(w, 1e-12, 1.0))
    CMAX = float(RHO_UPPER)
    H_UNIT = 0.5 * np.log(2.0 * np.pi * np.e)            # marginal entropy ref

    # cross-rung correlation r_cross for adjacent pairs, per history.
    cross_bond = soft(rvia, beta)                        # (K,R-1) in [0,1]
    # adjacent template entries
    Tadj = cp.asarray([float(T_template[n, n + 1]) for n in range(R - 1)])
    # corridor-weighted adjacent cross-rung correlation, per history per bond:
    #   C_w[n,n+1] = sw_n sw_{n+1} * CMAX * cross_bond_n * T[n,n+1]
    r_cross = (sw[:, :-1] * sw[:, 1:] * CMAX * cross_bond
               * Tadj[None, :])                          # (K,R-1)
    r_cross = cp.clip(r_cross, 0.0, 0.999999)

    # Gaussian mutual information of two unit-variance correlated Gaussians,
    # normalised by the unit marginal entropy -> Piece-6 normalised tau.
    I_cross = -0.5 * cp.log(cp.clip(1.0 - r_cross ** 2, 1e-12, 1.0))
    tau = cp.clip(I_cross / H_UNIT, 0.0, 1.0)            # (K,R-1)

    tau_mean = cp.asnumpy(cp.mean(tau, axis=0))          # (R-1,)
    tau_lo = float(cp.min(tau))
    tau_hi = float(cp.max(tau))
    # population tau from the ensemble-mean correlation (robust, estimator-free)
    r_pop = cp.asnumpy(cp.mean(r_cross, axis=0))         # (R-1,)
    I_pop = -0.5 * np.log(np.clip(1.0 - r_pop ** 2, 1e-12, 1.0))
    tau_pop = np.clip(I_pop / H_UNIT, 0.0, 1.0)          # (R-1,)
    return dict(
        tau_mean=[float(x) for x in tau_mean],
        tau_pop=[float(x) for x in tau_pop],
        tau_ens_min=tau_lo, tau_ens_max=tau_hi,
        tau_pop_min=float(np.min(tau_pop)),
        tau_pop_max=float(np.max(tau_pop)),
        all_in_corridor=bool(np.all((tau_pop > TAU_LOWER)
                                    & (tau_pop < TAU_UPPER))),
        n_above_corridor=int(np.sum(tau_pop >= TAU_UPPER)),
        n_below_corridor=int(np.sum(tau_pop <= TAU_LOWER)),
    )


def collect_allemerged(R, n_hist, seed, beta):
    """Run R2's simulator in GPU chunks; keep, per all-emerged history, rtf and
    rvia. Identical to R1xR2 / the fractal run's collect_allemerged."""
    rtf_parts, rvia_parts = [], []
    done, cidx, n_all = 0, 0, 0
    while done < n_hist:
        this = min(CHUNK, n_hist - done)
        sim = B.simulate_histories(R, this, seed + 104729 * cidx)
        T = sim["T_total"]
        rho = sim["rho"]
        es = sim["emerge_step"]
        ne = sim["n_emerged"]
        idx = cp.where(ne == R)[0]
        if idx.size > 0:
            rows = idx
            rtf_sel = rho[rows, :, T - 1]
            rvia = cp.empty((idx.size, max(R - 1, 1)), dtype=cp.float64)
            for n in range(R - 1):
                esn = cp.clip(es[rows, n + 1], 0, T - 1)
                rvia[:, n] = rho[rows, n, esn]
            if R == 1:
                rvia[:, 0] = RHO_MID
            rtf_parts.append(cp.asnumpy(rtf_sel))
            rvia_parts.append(cp.asnumpy(rvia))
            n_all += int(idx.size)
        del sim, rho, es
        cp.get_default_memory_pool().free_all_blocks()
        done += this
        cidx += 1
        if cidx % 50 == 0 or done >= n_hist:
            log(f"      R={R:2d} sim {done:,}/{n_hist:,} "
                f"({100 * done // n_hist}%)  all-emerged so far {n_all:,}")
    if not rtf_parts:
        return None, None, n_hist, 0
    rtf = cp.asarray(np.concatenate(rtf_parts))
    rvia = cp.asarray(np.concatenate(rvia_parts))
    return rtf, rvia, n_hist, n_all


def metrics_for_topology(rtf, rvia, beta, R, topology, seed):
    """The three-hypothesis + two-sided-test metrics for one cross-rung
    topology. CUDA."""
    K = rtf.shape[0]
    T_tmpl = coupling_matrix_template(R, topology)

    log_w, rho_joint, k_eff_joint = joint_rho_history(rtf, rvia, beta, T_tmpl)

    # H-holo(b) -- dilution. post-selected ensemble.
    finite = cp.isfinite(log_w)
    lw = cp.where(finite, log_w, -1e300)
    top = float(cp.max(lw))
    w_ps = cp.exp(lw - top)
    w_ps = w_ps / cp.clip(cp.sum(w_ps), 1e-300, None)
    rho_joint_psmean = float(cp.sum(w_ps * rho_joint))
    keff_joint_psmean = float(cp.sum(w_ps * k_eff_joint))
    rho_joint_mean = float(cp.mean(rho_joint))
    rho_joint_max = float(cp.max(rho_joint))
    rho_joint_min = float(cp.min(rho_joint))
    keff_joint_mean = float(cp.mean(k_eff_joint))
    in_band = (rho_joint > RHO_LOWER) & (rho_joint < RHO_UPPER)
    frac_in_band = float(cp.mean(in_band.astype(cp.float64)))
    n_in_band = int(cp.sum(in_band))

    # H-holo(a) -- tau in the cross-rung corridor.
    tau = tau_per_scale(rtf, rvia, beta, T_tmpl, R)

    # H3 -- selectivity & joint work.
    acc = (lw > top - 1.0)
    accept_frac = float(cp.mean(acc.astype(cp.float64)))
    _, rho_joint_off, _ = joint_rho_history(
        rtf, cp.full_like(rvia, 100.0), beta, T_tmpl)
    cross_delta = float(cp.mean(cp.abs(rho_joint - rho_joint_off)))
    cross_delta_max = float(cp.max(cp.abs(rho_joint - rho_joint_off)))

    # H1 -- segment-shuffle non-decomposability.
    nrng = np.random.RandomState((seed + 777) % (2 ** 32))
    wnp = cp.asnumpy(w_ps).astype(np.float64)
    wnp = wnp / wnp.sum()
    nshuf = K
    rtf_shuf = cp.empty((nshuf, R), dtype=cp.float64)
    for n in range(R):
        pick = cp.asarray(nrng.choice(K, size=nshuf, p=wnp))
        rtf_shuf[:, n] = rtf[pick, n]
    rvia_shuf = cp.empty((nshuf, max(R - 1, 1)), dtype=cp.float64)
    for n in range(max(R - 1, 1)):
        pick = cp.asarray(nrng.choice(K, size=nshuf, p=wnp))
        rvia_shuf[:, n] = rvia[pick, n]
    log_w_shuf, _, _ = joint_rho_history(rtf_shuf, rvia_shuf, beta, T_tmpl)
    pick_real = cp.asarray(nrng.choice(K, size=nshuf, p=wnp))
    log_w_real = log_w[pick_real]
    mean_real = float(cp.mean(cp.where(cp.isfinite(log_w_real),
                                       log_w_real, -50.0)))
    mean_shuf = float(cp.mean(cp.where(cp.isfinite(log_w_shuf),
                                       log_w_shuf, -50.0)))
    shuffle_gap = mean_real - mean_shuf
    shuffle_gap_per_rung = shuffle_gap / R

    return dict(
        topology=topology,
        rho_joint_psmean=rho_joint_psmean,
        rho_joint_mean=rho_joint_mean,
        rho_joint_max=rho_joint_max,
        rho_joint_min=rho_joint_min,
        rho_joint_times_R_psmean=rho_joint_psmean * R,
        rho_joint_times_R_atmax=rho_joint_max * R,
        k_eff_joint_psmean=keff_joint_psmean,
        k_eff_joint_mean=keff_joint_mean,
        band_reachable=bool(n_in_band > 0),
        frac_in_band=frac_in_band,
        n_in_band=n_in_band,
        accept_frac=accept_frac,
        cross_delta_mean=cross_delta,
        cross_delta_max=cross_delta_max,
        mean_logw_real=mean_real,
        mean_logw_shuffled=mean_shuf,
        shuffle_gap=shuffle_gap,
        shuffle_gap_per_rung=shuffle_gap_per_rung,
        tau=tau,
    )


def analyse_depth(R, n_hist, beta, seed):
    """Build the construction at depth R for chain / rgflow / holographic and
    compute all metrics. chain and rgflow are the in-run decaying baselines."""
    rtf, rvia, n_hist, n_all = collect_allemerged(R, n_hist, seed, beta)
    if n_all < 200:
        return dict(R=R, n_hist=n_hist, n_all_emerged=n_all,
                    note="too few all-emerged histories for statistics")
    K = rtf.shape[0]
    out = dict(R=R, n_hist=n_hist, n_all_emerged=n_all, K=K, beta=beta,
               c1_rg=C1_RG)
    for topology in ("chain", "rgflow", "holographic"):
        out[topology] = metrics_for_topology(rtf, rvia, beta, R, topology, seed)
    return out


def main():
    cp.random.seed(SEED)
    beta = 1.0 / (2.0 * W_HALF ** 2)
    log("=" * 74)
    log("P_omega -- the holographic construction")
    log("  R1xR2's joint Kish participation-ratio functional on R2's open")
    log("  sequential history frame; cross-rung coupling = the genuine MERA-")
    log("  as-AdS causal-cone-overlap geometry (DERIVED, not imposed).")
    log(f"  within-rung corridor band ({RHO_LOWER}, {RHO_UPPER}); centre "
        f"{RHO_MID}; half-width {W_HALF}")
    log(f"  cross-rung (tau) corridor ({TAU_LOWER}, {TAU_UPPER}) "
        f"-- RungHierarchy.lean")
    log(f"  beta_pin = 1/2w^2 = {beta:.4f}")
    log(f"  C1_RG (per-scale-step holographic contraction, = geommean of "
        f"measured g/J medians 0.31/0.72/1.15) = {C1_RG:.4f}")
    log(f"  topologies: chain | rgflow (decaying baseline) | holographic "
        f"(MERA causal-cone overlap)")
    log(f"  GPU: {cp.cuda.runtime.getDeviceProperties(0)['name'].decode()}")
    log("=" * 74)

    # ---- RESUME from on-disk partial results ------------------------------
    results = []
    done_R = set()
    if os.path.exists(RESULTS):
        try:
            with open(RESULTS) as f:
                prev = json.load(f)
            results = prev.get("results", [])
            done_R = {r["R"] for r in results
                      if "holographic" in r or "note" in r}
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
                    construction="holographic / MERA-as-AdS P_omega",
                    seed=SEED, beta_pin=beta, c1_rg=C1_RG,
                    rho_lower=RHO_LOWER, rho_upper=RHO_UPPER,
                    rho_mid=RHO_MID, w_half=W_HALF,
                    tau_lower=TAU_LOWER, tau_upper=TAU_UPPER,
                    topologies=["chain", "rgflow", "holographic"],
                    functional=("rho_joint = Kish-inverse of the participation "
                                "ratio of the corridor-weighted R x R "
                                "rung-correlation matrix; cross-rung coupling "
                                "for 'holographic' = the genuine binary-MERA "
                                "causal-cone-overlap geodesic correlation "
                                "(derived from the AdS bulk geometry); c1 fixed "
                                "at the measured g/J geometric mean 0.626"),
                    elapsed_s=time.time() - t0),
                results=results,
            ), f, indent=2)

    t0 = time.time()
    for R in R_SCAN:
        if R in done_R:
            log(f"  R={R:2d}  already done -- skipped (resume)")
            continue
        ts = time.time()
        res = analyse_depth(R, N_BY_R[R], beta, SEED + R * 7919)
        res["wall_s"] = time.time() - ts
        results.append(res)
        if "note" in res:
            log(f"  R={R:2d}  N={N_BY_R[R]:>9d}  {res['note']}  "
                f"({res['wall_s']:.1f}s)")
        else:
            ch, rg, ho = res["chain"], res["rgflow"], res["holographic"]
            log(f"  R={R:2d}  N={N_BY_R[R]:>9d}  K={res['K']:>7d}  "
                f"({res['wall_s']:.1f}s)")
            log(f"        rho_joint(ps):  chain={ch['rho_joint_psmean']:.4f}  "
                f"rgflow={rg['rho_joint_psmean']:.4f}  "
                f"HOLO={ho['rho_joint_psmean']:.4f}")
            log(f"        rho_joint*R  :  chain={ch['rho_joint_times_R_psmean']:.3f}"
                f"  rgflow={rg['rho_joint_times_R_psmean']:.3f}  "
                f"HOLO={ho['rho_joint_times_R_psmean']:.3f}")
            log(f"        k_eff(ps)    :  chain={ch['k_eff_joint_psmean']:.3f}  "
                f"rgflow={rg['k_eff_joint_psmean']:.3f}  "
                f"HOLO={ho['k_eff_joint_psmean']:.3f}")
            log(f"        in-band frac :  chain={ch['frac_in_band']:.4f}  "
                f"rgflow={rg['frac_in_band']:.4f}  "
                f"HOLO={ho['frac_in_band']:.4f}")
            tho = ho["tau"]
            log(f"        HOLO tau     :  pop=[{tho['tau_pop_min']:.3f}.."
                f"{tho['tau_pop_max']:.3f}]  "
                f"in-corridor({TAU_LOWER},{TAU_UPPER})={tho['all_in_corridor']}"
                f"  (above={tho['n_above_corridor']} "
                f"below={tho['n_below_corridor']})")
            log(f"        shuffle_gap  :  chain={ch['shuffle_gap']:.4f}  "
                f"rgflow={rg['shuffle_gap']:.4f}  "
                f"HOLO={ho['shuffle_gap']:.4f}")
        flush(t0)
        log(f"      flushed -> {RESULTS}")

    log(f"\ndone, {time.time() - t0:.1f}s total. results -> {RESULTS}")


if __name__ == "__main__":
    main()
