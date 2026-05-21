"""
Does the backward-soft dead zone return at high rung count? — GPU scaling run.
=============================================================================

backward_soft_deadzone.py (3 rungs) found the backward soft operator
E_omega(beta) = exp(-beta * sum_n (rho_n - rho_c)^2) does NOT inherit the
hard-projector dead zone: h_min(Hsum) stayed small. Open question: h_min is a
sum over rungs and grows with rung count R. Does it grow fast enough that the
soft operator becomes exponentially suppressed at high R?

13+ rungs via genuine RG-nesting-on-spins is impossible (the Hilbert space is
2^spins). So the Hilbert space is held at a FIXED dimension D and the NUMBER of
rung-operators is grown. Honest caveat: the rungs are operators on a shared
space with tunable non-commutativity, not genuine RG-coarse-grainings -- a
model, and (for independent rungs) the worst case for h_min growth.

  rho_n = U_n(eps) Lambda U_n(eps)^dag,  U_n(eps) = exp(i eps A_n),
  A_n random Hermitian (spectral radius 1), Lambda fixed spectrum in [0,1].
  eps -> 0  : rungs commute, h_min = 0.   eps large : maximal non-commutativity.

h_min(eps, R) = lambda_min( sum_{n=1}^R (rho_n - rho_c)^2 ), instance-averaged.
soft weight at the framework-referenced beta_pin = 1/(2 w^2):
exp(-beta_pin * h_min). The dead zone returns where that -> 0.

fp32 (complex64) on the GPU; the A_n eigendecompositions are cached across eps.
"""
import numpy as np
import time

try:
    import cupy as xp
    GPU = True
except Exception:
    import numpy as xp
    GPU = False

CC = xp.complex64
RR = xp.float32
D = 2048
RHO_C = 0.5
EPS_VALS = [0.05, 0.15, 0.40, 1.00]
R_CHECK = [1, 3, 5, 9, 13, 17, 25, 40]
R_MAX = R_CHECK[-1]
N_INST = 4

Lam = xp.asarray(np.linspace(0.0, 1.0, D), dtype=RR)
IdD = xp.eye(D, dtype=CC)

print("=" * 80, flush=True)
print("BACKWARD-SOFT DEAD ZONE — rung-count scaling", flush=True)
print("=" * 80, flush=True)
print(f"  backend: {'cupy / RTX 4090' if GPU else 'numpy / CPU'} (complex64); "
      f"D = {D}; instances = {N_INST}; R up to {R_MAX}", flush=True)


def random_herm(seed):
    rng = np.random.default_rng(seed)
    G = rng.standard_normal((D, D)) + 1j * rng.standard_normal((D, D))
    return xp.asarray((G + G.conj().T) / 2, dtype=CC)


def lambda_min(M):
    v = xp.linalg.eigvalsh(M)[0]
    return float(v.get() if GPU else v)


hmin = {e: {R: [] for R in R_CHECK} for e in EPS_VALS}
commutator = {e: [] for e in EPS_VALS}

t0 = time.time()
for inst in range(N_INST):
    # cache the A_n eigendecompositions once (eps-independent)
    cache = []
    for n in range(R_MAX):
        a, Q = xp.linalg.eigh(random_herm((inst, n)))
        a = a / xp.abs(a).max()
        cache.append((a.astype(RR), Q))
    for eps in EPS_VALS:
        Hsum = xp.zeros((D, D), dtype=CC)
        rho_first = []
        for n in range(R_MAX):
            a, Q = cache[n]
            U = (Q * xp.exp(1j * eps * a)) @ Q.conj().T
            rho = (U * Lam) @ U.conj().T
            if n < 2:
                rho_first.append(rho)
            dev = rho - RHO_C * IdD
            Hsum = Hsum + dev @ dev
            if (n + 1) in R_CHECK:
                hmin[eps][n + 1].append(lambda_min(Hsum))
        c = float(xp.abs(rho_first[0] @ rho_first[1]
                         - rho_first[1] @ rho_first[0]).max())
        commutator[eps].append(c)
    print(f"  instance {inst+1}/{N_INST} done  ({time.time()-t0:.0f}s)",
          flush=True)

print(flush=True)
print("=" * 80, flush=True)
print("h_min( sum_{n<=R} (rho_n - rho_c)^2 ) — mean over instances", flush=True)
print("=" * 80, flush=True)
print("  eps \\ R " + "".join(f"{R:>8d}" for R in R_CHECK) + "   ||[r,r]||",
      flush=True)
for eps in EPS_VALS:
    row = f"  {eps:>7.2f} "
    for R in R_CHECK:
        row += f"{np.mean(hmin[eps][R]):>8.4f}"
    row += f"   {np.mean(commutator[eps]):>9.2e}"
    print(row, flush=True)

print(flush=True)
print("=" * 80, flush=True)
print("soft weight  exp(-beta_pin * h_min)  at beta_pin = 1/(2 w^2)", flush=True)
print("=" * 80, flush=True)
for w in [0.15, 0.10]:
    beta_pin = 1.0 / (2.0 * w * w)
    print(f"\n  corridor half-width w = {w}  ->  beta_pin = {beta_pin:.1f}",
          flush=True)
    print("  eps \\ R " + "".join(f"{R:>9d}" for R in R_CHECK), flush=True)
    for eps in EPS_VALS:
        row = f"  {eps:>7.2f} "
        for R in R_CHECK:
            row += f"{np.exp(-beta_pin * np.mean(hmin[eps][R])):>9.2e}"
        print(row, flush=True)

print(flush=True)
print("=" * 80, flush=True)
print("READING", flush=True)
print("=" * 80, flush=True)
for eps in EPS_VALS:
    h13 = np.mean(hmin[eps][13])
    slope = np.mean(hmin[eps][R_MAX]) / R_MAX
    w15 = np.exp(-(1 / (2 * 0.15 ** 2)) * h13)
    w10 = np.exp(-(1 / (2 * 0.10 ** 2)) * h13)
    print(f"  eps={eps:>5.2f} (||[r,r]||~{np.mean(commutator[eps]):.1e}): "
          f"h_min/R ~ {slope:.4f}; R=13: h_min={h13:.4f}, "
          f"soft weight w=0.15:{w15:.2e}  w=0.10:{w10:.2e}", flush=True)
print(flush=True)
print("  The deadzone toy's RG-nested rungs had ||[rho_a,rho_b]|| ~ 8e-3 -- the",
      flush=True)
print("  LOW-eps, near-commuting end. Read the R=13 bet off the eps row whose",
      flush=True)
print("  commutator is closest to that. High-eps (independent) rungs are the",
      flush=True)
print("  worst case.", flush=True)
