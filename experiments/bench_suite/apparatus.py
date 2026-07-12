#!/usr/bin/env python3
"""
bench_suite apparatus — the shared substrate for registered bets 7, 8, 10.

SUBSTRATE (pre-committed in DECISIONS.md):
  An ensemble of R replicas of a k-oscillator equicorrelation Ornstein-Uhlenbeck
  array, integrated on the RTX 4090 (cupy). The array's WHITE-NOISE BATH is REAL
  GPU TIMING JITTER (the CIRISArray validated TRNG path: launch+sync of a tiny
  kernel, low 6 timing bits -> uniforms -> Box-Muller normals). PRNG noise is
  never used to drive the dynamics. The coupling / maintenance drift is
  software-defined (uniform-rho equicorrelation, the Kish object), matching the
  corridor_ceiling OU theory (sigma = Tr[Q^T D^{-1} Q C^{-1}], verified there).

  Passive substrate (maintenance OFF):  dx_i = -lambda0 x_i dt + sqrt(2D) dW_i
     -> k independent oscillators driven by independent real jitter; the passive
        fixed point is rho = 0 (decorrelated). lambda0 is the bench's bare
        relaxation rate; the correlation-decay rate of the passive array is 2*lambda0.
  Maintenance ON: an ADDED drift  u = -(B - lambda0 I) x  (the force the machine
     applies beyond bare relaxation) holds the stationary covariance at the
     equicorrelation target C(rho*) = (1-rho*) I + rho* 11^T, optionally with an
     antisymmetric circulation Q (broken detailed balance -> the rent).
  RENT (N1 budget) = actuation power = ||B - lambda0 I||_F^2  (force^2 the machine
     applies); housekeeping-heat rate sigma measured from the trajectory.

  The noise bath is the load-bearing physical object; the OU array is the
  software substrate the corridor theory is stated on. This is NOT the 46 s
  Lorenz CIRISArray substrate — see DECISIONS.md caveat C1.

Reuses the VALIDATED entropy-production estimator form from
experiments/corridor_ceiling/sigma_max.py (Stratonovich midpoint housekeeping
heat  sigma = <F o dx>/dt,  F = -D^{-1} B x_mid).
"""
import time, math, json, hashlib
import numpy as np
import cupy as cp

# ----------------------------------------------------------------------------
# real GPU-timing-jitter bath  (CIRISArray src/strain_gauge.py TimingKernel path)
# ----------------------------------------------------------------------------
_JMOD = cp.RawModule(code=r'''
extern "C" __global__ void tk(float* d, int n, int it){
  int i = blockIdx.x*blockDim.x+threadIdx.x; if(i>=n) return;
  float x=d[i]; for(int k=0;k<it;k++){ x=x*0.99f+0.01f; } d[i]=x;
}''')
_JK = _JMOD.get_function('tk')
_JD = cp.random.randn(64, dtype=cp.float32)
_LOWBITS = 6                     # validated: low 6 timing bits = 100% Shannon entropy
_BITS_PER_UNIFORM = 24           # 4 chunks of 6 bits -> 24-bit uniform


class JitterSource:
    """Streams N(0,1) normals whose ENTROPY is real GPU kernel timing jitter."""

    def __init__(self):
        self.n_timings = 0
        self.n_normals = 0
        self._buf = np.empty(0, dtype=np.float64)   # spare normals from Box-Muller pairs

    def _raw_timings(self, m):
        out = np.empty(m, dtype=np.int64)
        pc = time.perf_counter_ns
        for i in range(m):
            s = pc()
            _JK((1,), (64,), (_JD, cp.int32(64), cp.int32(10)))
            cp.cuda.Stream.null.synchronize()
            out[i] = pc() - s
        self.n_timings += m
        return out

    def normals(self, n):
        """Return n real-jitter N(0,1) samples (float64)."""
        need = n - self._buf.size
        if need > 0:
            # each normal-pair needs 2 uniforms = 2*4 = 8 timing samples of 6 bits
            npairs = (need + 1) // 2 + 4                       # small margin
            timings = self._raw_timings(npairs * 8)
            chunks = (timings & ((1 << _LOWBITS) - 1)).astype(np.uint64)   # 6-bit chunks
            chunks = chunks[: (chunks.size // 4) * 4].reshape(-1, 4)
            u = (chunks[:, 0] | (chunks[:, 1] << 6) | (chunks[:, 2] << 12) |
                 (chunks[:, 3] << 18)).astype(np.float64)
            u = (u + 0.5) / (1 << _BITS_PER_UNIFORM)                       # (0,1) open
            m = u.size // 2
            u1 = u[:2 * m:2]; u2 = u[1:2 * m:2]
            rad = np.sqrt(-2.0 * np.log(u1))
            new = np.empty(2 * m, dtype=np.float64)
            new[0::2] = rad * np.cos(2 * np.pi * u2)
            new[1::2] = rad * np.sin(2 * np.pi * u2)
            self._buf = np.concatenate([self._buf, new])
        out = self._buf[:n].copy()
        self._buf = self._buf[n:].copy()
        self.n_normals += n
        return out

    def normal_block(self, shape):
        n = int(np.prod(shape))
        return self.normals(n).reshape(shape)


def validate_normals(z):
    """Whiteness + normality diagnostics for a jitter-normal trace (calibration)."""
    from scipy import stats
    z = np.asarray(z, dtype=np.float64)
    ac = [float(np.corrcoef(z[:-L], z[L:])[0, 1]) for L in (1, 2, 3, 5, 10)]
    ks = stats.kstest((z - z.mean()) / z.std(), 'norm')
    return dict(n=int(z.size), mean=float(z.mean()), std=float(z.std()),
                skew=float(stats.skew(z)), kurtosis=float(stats.kurtosis(z)),
                autocorr_lags_1_2_3_5_10=ac,
                ks_stat=float(ks.statistic), ks_p=float(ks.pvalue),
                sha256=hashlib.sha256(z.tobytes()).hexdigest()[:16])


# ----------------------------------------------------------------------------
# equicorrelation OU objects  (matches corridor_ceiling / Kish theory)
# ----------------------------------------------------------------------------
def C_kish(rho, k):
    return (1.0 - rho) * np.eye(k) + rho * np.ones((k, k))


def keff_from_rho(rho, k):
    return k / (1.0 + rho * (k - 1.0))            # formal core piece 1


def rho_from_keff(keff, k):
    return (k / keff - 1.0) / (k - 1.0)


def optimal_Q_N1(rho, k, P):
    """N1-optimal antisymmetric circulation at actuation budget ||Q C^{-1}||_F^2 <= P.
    Uses the best single pair from sigma_max.py: for k>=3 the collapsed-collapsed
    pair (eff = 1-rho) dominates; else the uniform-collapsed pair. Returns Q (k,k)
    in the ORIGINAL basis and the analytic sigma_max it realizes."""
    l1 = 1.0 + rho * (k - 1.0)
    l2 = 1.0 - rho
    C = C_kish(rho, k)
    w, V = np.linalg.eigh(C)                       # ascending
    order = np.argsort(-w); w = w[order]; V = V[:, order]   # uniform mode first
    # candidate pairs (index into sorted eigenbasis): (uniform=0, collapsed=1) and (1,2)
    cands = []
    # eff = yield/cost for ||QC^{-1}||_F^2 budget; pair (i,j): put all q into that pair
    # cost ||Q C^{-1}||_F^2 = q^2 (1/li^2 + 1/lj^2); yield sigma = q^2 (1/li+1/lj)
    cands.append((0, 1, (1/w[0] + 1/w[1]) / (1/w[0]**2 + 1/w[1]**2)))
    if k >= 3:
        cands.append((1, 2, (1/w[1] + 1/w[2]) / (1/w[1]**2 + 1/w[2]**2)))
    i, j, eff = max(cands, key=lambda c: c[2])
    sigma_max = P * eff
    # q from budget: q^2 (1/wi^2 + 1/wj^2) = P
    q = math.sqrt(P / (1/w[i]**2 + 1/w[j]**2))
    E = np.zeros((k, k)); E[i, j] = q; E[j, i] = -q
    Q = V @ E @ V.T
    return Q, float(sigma_max)


def build_drift(rho, k, Q=None):
    """Maintenance drift B with stationary covariance C(rho) and (optional)
    circulation Q, under fixed unit noise D = I:  B = (D + Q) C^{-1}."""
    C = C_kish(rho, k)
    Cinv = np.linalg.inv(C)
    D = np.eye(k)
    if Q is None:
        Q = np.zeros((k, k))
    return (D + Q) @ Cinv, C, D, Q


# ----------------------------------------------------------------------------
# GPU ensemble integrator (Euler-Maruyama) driven by REAL jitter normals
# ----------------------------------------------------------------------------
def integrate(B, D, X0, jitter, n_steps, dt, R, k,
              record_rho=False, accum_heat=False, seg_len=None, C_for_dss=None):
    """Integrate dX = -X B^T dt + sqrt(2 dt) D^{1/2} Z, Z = real jitter normals.
    Returns dict; all noise comes from `jitter.normal_block`. State on GPU.

    accum_heat: accumulate Stratonovich housekeeping heat  F o dx, F=-D^{-1} B x_mid.
    seg_len: if set, also record per-segment work W_hk and boundary term ds_sys
             (needs C_for_dss = C(rho*)) for the fluctuation-theorem test."""
    Bt = cp.asarray(B.T, dtype=cp.float64)
    Dinv = cp.asarray(np.linalg.inv(D), dtype=cp.float64)
    sq = math.sqrt(2.0 * dt)
    X = cp.asarray(X0, dtype=cp.float64)
    heat = cp.zeros(R, dtype=cp.float64) if accum_heat else None
    rho_t = [] if record_rho else None
    seg_W, seg_dss = [], []
    if seg_len is not None:
        Cinv_g = cp.asarray(np.linalg.inv(C_for_dss), dtype=cp.float64)
        seg_heat = cp.zeros(R, dtype=cp.float64)
        x_seg_start = X.copy()

    for t in range(n_steps):
        Z = cp.asarray(jitter.normal_block((R, k)))
        drift = X @ Bt
        Xn = X - drift * dt + sq * (Z @ cp.asarray(np.linalg.cholesky(D).T))
        if accum_heat or seg_len is not None:
            Xmid = 0.5 * (X + Xn)
            F = -(Xmid @ Bt) @ Dinv                 # (R,k) thermodynamic force
            dq = cp.sum(F * (Xn - X), axis=1)       # (R,) heat this step
            if accum_heat:
                heat += dq
            if seg_len is not None:
                seg_heat += dq
        X = Xn
        if record_rho:
            rho_t.append(_ensemble_rho(X, R, k))
        if seg_len is not None and (t + 1) % seg_len == 0:
            # boundary term ds_sys = 0.5 (x_end^T Cinv x_end - x_start^T Cinv x_start)
            def quad(xg):
                return cp.sum((xg @ Cinv_g) * xg, axis=1)
            dss = 0.5 * (quad(X) - quad(x_seg_start))
            seg_W.append(cp.asnumpy(seg_heat).copy())
            seg_dss.append(cp.asnumpy(dss).copy())
            seg_heat = cp.zeros(R, dtype=cp.float64)
            x_seg_start = X.copy()
    out = dict(X=cp.asnumpy(X))
    if accum_heat:
        out['sigma_hat'] = float(cp.asnumpy(heat).mean() / (n_steps * dt))
        out['sigma_hat_per_replica'] = cp.asnumpy(heat) / (n_steps * dt)
    if record_rho:
        out['rho_t'] = np.array(rho_t)
    if seg_len is not None:
        out['seg_W'] = np.concatenate(seg_W) if seg_W else np.array([])
        out['seg_dss'] = np.concatenate(seg_dss) if seg_dss else np.array([])
    return out


def _ensemble_rho(Xg, R, k):
    """Mean off-diagonal Pearson correlation across the k oscillators, over the
    ensemble of R replicas (each replica = one realization; correlation estimated
    across replicas at this instant)."""
    Xc = Xg - Xg.mean(axis=0, keepdims=True)       # center over replicas
    cov = (Xc.T @ Xc) / (R - 1)                    # (k,k)
    d = cp.sqrt(cp.diag(cov))
    corr = cov / cp.outer(d, d)
    k_ = corr.shape[0]
    off = (cp.sum(corr) - cp.trace(corr)) / (k_ * (k_ - 1))
    return float(off)


def steady_state_sample(C, R, k, jitter):
    """Draw an initial ensemble at the target NESS covariance C, using real jitter
    normals passed through the Cholesky factor (physical initial condition)."""
    L = np.linalg.cholesky(C)
    Z = jitter.normal_block((R, k))
    return Z @ L.T
