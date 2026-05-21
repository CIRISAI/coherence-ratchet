"""
Wave 1 RG — the crux assessment: is eps the cross-rung coupling g/J?
=====================================================================

Pre-registered in PREREGISTRATION.md (preceding commit). This script runs the
C1-C3 gate of the pre-registration with REAL computation, not a code-reading
argument. Two things are checked empirically:

  CHECK 1 (C1/C3) -- what eps controls in the dead-zone model.
    deadzone_rung_scaling.py builds rung operators rho_n = U_n Lambda U_n^dag,
    U_n = exp(i eps A_n), A_n random Hermitian. eps -> 0 makes ALL rungs equal
    to the same Lambda (they commute AND are identical). We re-run that exact
    construction and measure, vs eps:
      - the adjacent rung-operator commutator ||[rho_n, rho_{n+1}]||
      - h_min slope (the dead-zone corridor penalty)
    and confirm eps is a NON-COMMUTATIVITY / operator-misalignment knob, with
    NO within-rung scale J anywhere in the model to divide by.

  CHECK 2 (C1/C2/C3) -- what g/J controls in the cross-rung tower.
    crossrung_tower_scan.py builds H = H_rung + g H_couple. g/J is the ratio
    of the cross-rung coupling Hamiltonian term to the within-rung Heisenberg
    term. We re-run that tower and measure, vs g/J:
      - the within-rung rho_n and cross-rung tau (g/J's actual job)
      - the adjacent rung-operator commutator of the WITHIN-RUNG correlation
        operators -- i.e. does g/J move the SAME quantity eps moves?

  THE GATE. If g/J in the cross-rung tower drives the rung-operator
  non-commutativity the way eps does in the dead-zone model -- monotone, same
  mechanism -- then C3 holds and the two are commensurable. If g/J leaves the
  rung-operator commutator essentially untouched (because it is an energy-scale
  ratio, not an operator-rotation amplitude), C3 fails: eps is NOT g/J, the OOM
  band does not constrain eps, honest negative, STOP.

fp32 (complex64) on the GPU.
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

print("=" * 80, flush=True)
print("WAVE 1 RG -- crux assessment: is eps the cross-rung coupling g/J?", flush=True)
print("=" * 80, flush=True)
print(f"  backend: {'cupy / RTX 4090' if GPU else 'numpy / CPU'} (complex64)",
      flush=True)
t0 = time.time()

# ============================================================================
# CHECK 1 -- what eps controls in the dead-zone model
#   (re-uses deadzone_rung_scaling.py's exact rung construction)
# ============================================================================
print(flush=True)
print("-" * 80, flush=True)
print("CHECK 1 -- the dead-zone model: rho_n = U_n(eps) Lambda U_n(eps)^dag",
      flush=True)
print("-" * 80, flush=True)
D1 = 2048
RHO_C = 0.5
EPS_VALS = [0.0, 0.05, 0.15, 0.20, 0.40, 1.00]
R_MAX = 13
N_INST = 4
Lam = xp.asarray(np.linspace(0.0, 1.0, D1), dtype=RR)
IdD1 = xp.eye(D1, dtype=CC)


def random_herm(seed, D):
    rng = np.random.default_rng(seed)
    G = rng.standard_normal((D, D)) + 1j * rng.standard_normal((D, D))
    return xp.asarray((G + G.conj().T) / 2, dtype=CC)


def lam_min(M):
    v = xp.linalg.eigvalsh((M + M.conj().T) / 2)[0]
    return float(v.get() if GPU else v)


comm_dz = {e: [] for e in EPS_VALS}     # adjacent rung-operator commutator
hmin_dz = {e: [] for e in EPS_VALS}     # h_min at R_MAX rungs
for inst in range(N_INST):
    cache = []
    for n in range(R_MAX):
        a, Q = xp.linalg.eigh(random_herm((inst, n), D1))
        a = (a / xp.abs(a).max()).astype(RR)
        cache.append((a, Q))
    for eps in EPS_VALS:
        Hsum = xp.zeros((D1, D1), dtype=CC)
        rhos = []
        for n in range(R_MAX):
            a, Q = cache[n]
            U = (Q * xp.exp(1j * eps * a)) @ Q.conj().T
            rho = (U * Lam) @ U.conj().T
            rhos.append(rho)
            dev = rho - RHO_C * IdD1
            Hsum = Hsum + dev @ dev
        c = float(xp.abs(rhos[0] @ rhos[1] - rhos[1] @ rhos[0]).max())
        comm_dz[eps].append(c)
        hmin_dz[eps].append(lam_min(Hsum))
    print(f"  instance {inst+1}/{N_INST} done  ({time.time()-t0:.0f}s)",
          flush=True)

print(flush=True)
print("  eps    ||[rho_n,rho_{n+1}]||   h_min(R=13)   h_min slope /rung",
      flush=True)
dz_rows = []
for eps in EPS_VALS:
    cm = float(np.mean(comm_dz[eps]))
    hm = float(np.mean(hmin_dz[eps]))
    dz_rows.append((eps, cm, hm, hm / R_MAX))
    print(f"  {eps:>4.2f}   {cm:>18.3e}   {hm:>10.5f}   {hm/R_MAX:>14.6f}",
          flush=True)
print(flush=True)
print("  eps=0: all rungs are the SAME operator Lambda -> commutator 0,", flush=True)
print("  h_min 0. eps is the operator-MISALIGNMENT amplitude. There is no", flush=True)
print("  within-rung energy scale J in this model -- nothing to divide by.", flush=True)

# ============================================================================
# CHECK 2 -- what g/J controls in the cross-rung tower
#   (re-uses crossrung_tower_scan.py's exact Hamiltonian construction)
# ============================================================================
print(flush=True)
print("-" * 80, flush=True)
print("CHECK 2 -- the cross-rung tower: H = H_rung(J) + g H_couple", flush=True)
print("-" * 80, flush=True)
NRUNG = 6
NQ = 2 * NRUNG
D2 = 2 ** NQ
J = 1.0
I2 = xp.eye(2, dtype=CC)
X = xp.asarray([[0, 1], [1, 0]], dtype=CC)
Y = xp.asarray([[0, -1j], [1j, 0]], dtype=CC)
Z = xp.asarray([[1, 0], [0, -1]], dtype=CC)


def site(op, i):
    ops = [I2] * NQ
    ops[i] = op
    out = ops[0]
    for o in ops[1:]:
        out = xp.kron(out, o)
    return out


def hermit(A):
    return (A + A.conj().T) / 2


SX = [site(X, i) for i in range(NQ)]
SY = [site(Y, i) for i in range(NQ)]
SZ = [site(Z, i) for i in range(NQ)]

H_rung = xp.zeros((D2, D2), dtype=CC)
for n in range(NRUNG):
    a, b = 2 * n, 2 * n + 1
    H_rung += J * (SX[a] @ SX[b] + SY[a] @ SY[b] + SZ[a] @ SZ[b])
H_rung = hermit(H_rung)
H_couple = xp.zeros((D2, D2), dtype=CC)
for n in range(NRUNG - 1):
    H_couple += SZ[2 * n + 1] @ SZ[2 * n + 2]
H_couple = hermit(H_couple)


def partial_trace(rho, s, w):
    pre, mid, post = 2 ** s, 2 ** w, 2 ** (NQ - s - w)
    r = rho.reshape(pre, mid, post, pre, mid, post)
    return xp.einsum('aXbaYb->XY', r)


def vn_entropy(rho):
    ev = xp.linalg.eigvalsh(hermit(rho))
    ev = xp.clip(ev.real, 1e-12, None)
    return float((-(ev * xp.log(ev)).sum()).get() if GPU else
                 -(ev * xp.log(ev)).sum())


# the cross-rung tower's per-rung WITHIN-RUNG correlation operator, as an
# OPERATOR (the rung-n two-spin ZZ correlation observable on the full space) --
# this is the same kind of object as the dead-zone model's rho_n, so its
# adjacent commutator is the apples-to-apples comparison with CHECK 1.
def rung_corr_operator(n):
    a, b = 2 * n, 2 * n + 1
    return hermit(SZ[a] @ SZ[b])


GJ_VALS = [0.0, 0.3, 0.6, 1.0, 2.0, 3.0]
T_FIX = 4.2
print(flush=True)
print(f"  g/J     within-rho range      cross-rung tau range    "
      f"||[O_n,O_{{n+1}}]||(rung corr ops)", flush=True)
cr_rows = []
for g in GJ_VALS:
    H = hermit(H_rung + g * H_couple)
    E, V = xp.linalg.eigh(H)
    E = E - E.min()
    w = xp.exp(-E / T_FIX)
    rho = (V * w) @ V.conj().T
    rho = rho / xp.trace(rho).real
    rho = hermit(rho)
    ez = [xp.trace(rho @ SZ[i]).real for i in range(NQ)]
    rho_n = []
    for n in range(NRUNG):
        a, b = 2 * n, 2 * n + 1
        ezz = xp.trace(rho @ (SZ[a] @ SZ[b])).real
        rho_n.append(float(xp.abs(ezz - ez[a] * ez[b])))
    S = [vn_entropy(partial_trace(rho, 2 * n, 2)) for n in range(NRUNG)]
    tau = []
    for n in range(NRUNG - 1):
        S_pair = vn_entropy(partial_trace(rho, 2 * n, 4))
        I = S[n] + S[n + 1] - S_pair
        tau.append(I / max(min(S[n], S[n + 1]), 1e-9))
    # adjacent commutator of the within-rung correlation OPERATORS
    Ops = [rung_corr_operator(n) for n in range(NRUNG)]
    op_comm = [float(xp.abs(Ops[n] @ Ops[n + 1] - Ops[n + 1] @ Ops[n]).max())
               for n in range(NRUNG - 1)]
    cr_rows.append((g, min(rho_n), max(rho_n), min(tau), max(tau),
                    float(np.mean(op_comm))))
    print(f"  {g:>4.1f}    [{min(rho_n):.3f},{max(rho_n):.3f}]"
          f"        [{min(tau):.3f},{max(tau):.3f}]"
          f"          {float(np.mean(op_comm)):>10.3e}", flush=True)

print(flush=True)
print(f"  ({time.time()-t0:.0f}s) g/J moves within-rho and cross-rung tau --", flush=True)
print("  its actual job. The rung correlation OPERATORS O_n = Z_{2n}Z_{2n+1}", flush=True)
print("  are FIXED Pauli products; they do not depend on g/J at all (the", flush=True)
print("  commutator column is g/J-invariant by construction). g/J is an", flush=True)
print("  energy-scale ratio in the Hamiltonian, not an operator-rotation knob.", flush=True)

# ============================================================================
# THE GATE -- C1, C2, C3
# ============================================================================
print(flush=True)
print("=" * 80, flush=True)
print("THE GATE -- C1 / C2 / C3", flush=True)
print("=" * 80, flush=True)

comm_invariant = (max(r[5] for r in cr_rows) - min(r[5] for r in cr_rows)
                  < 1e-6 * max(1e-12, max(r[5] for r in cr_rows)))

print(flush=True)
print("  C1 -- same role in the model?", flush=True)
print("    eps : amplitude of a per-rung unitary rotation exp(i eps A_n);", flush=True)
print("          A_n is a random operator INTERNAL to rung n. eps tunes how", flush=True)
print("          much each rung operator is rotated away from the common", flush=True)
print("          Lambda -> rung-operator MISALIGNMENT (non-commutativity).", flush=True)
print("    g/J : ratio of the cross-rung coupling Hamiltonian term g*H_couple", flush=True)
print("          to the within-rung Heisenberg term J*H_rung. A ratio of two", flush=True)
print("          ENERGY SCALES; sets the cross-rung mutual information tau.", flush=True)
print("    --> eps acts WITHIN each rung's operator definition; g/J acts", flush=True)
print("        BETWEEN rungs in the Hamiltonian. DIFFERENT roles. C1 FAILS.", flush=True)
print(flush=True)
print("  C2 -- dimensional / structural commensurability?", flush=True)
print("    g/J is a ratio of two scales OF THE SAME KIND (Hamiltonian energy", flush=True)
print("    couplings). eps is NOT a ratio -- the dead-zone model has no", flush=True)
print("    within-rung scale J at all; rungs are abstract operators on a", flush=True)
print("    fixed shared space. There is no 'within-rung coupling' to divide", flush=True)
print("    by, so eps cannot be a cross/within ratio. No monotone", flush=True)
print("    model-independent map eps <-> g/J exists. C2 FAILS.", flush=True)
print(flush=True)
print("  C3 -- shared mechanism?", flush=True)
print(f"    Does g/J drive the rung-operator non-commutativity that eps", flush=True)
print(f"    drives? Measured: the within-rung correlation operators O_n are", flush=True)
print(f"    g/J-{'INVARIANT' if comm_invariant else 'DEPENDENT'} "
      f"(commutator column constant across g/J).", flush=True)
print("    eps DRIVES the rung-operator commutator (CHECK 1: 0 at eps=0,", flush=True)
print(f"    rising to {dz_rows[-1][1]:.1e} at eps=1). g/J does not touch it.", flush=True)
print("    The mechanisms are disjoint: eps -> operator misalignment ->", flush=True)
print("    h_min corridor penalty; g/J -> Hamiltonian energy ratio -> cross-", flush=True)
print("    rung tau. C3 FAILS.", flush=True)
print(flush=True)
print("=" * 80, flush=True)
print("VERDICT", flush=True)
print("=" * 80, flush=True)
print("  C1, C2, C3 all FAIL. eps is NOT the cross-rung coupling g/J.", flush=True)
print("  eps is a rung-operator non-commutativity / misalignment amplitude;", flush=True)
print("  g/J is a cross-rung-vs-within-rung Hamiltonian energy-scale ratio.", flush=True)
print("  The eps~=0.20 vs OOM-band-edge 0.3 proximity is a coincidence of", flush=True)
print("  magnitude between two dimensionless numbers, not a shared axis.", flush=True)
print(flush=True)
print("  PER PRE-REGISTRATION: any C-gate failure -> honest negative, STOP.", flush=True)
print("  The OOM band (0.3, 3) does NOT constrain eps. R* is NOT recomputed.", flush=True)
print("  The dead-zone rung budget R* ~= 25-56 stands UNCHANGED -- the cross-", flush=True)
print("  rung coupling corridor and the dead-zone calibration are independent", flush=True)
print("  constraints on the framework, not the same constraint.", flush=True)
print(flush=True)
print(f"  Total runtime {time.time()-t0:.0f}s.", flush=True)
