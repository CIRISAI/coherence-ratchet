"""
Model 1' of the QG-via-P_omega pipeline: rungs as RG coarse-grainings.
======================================================================

Model 1 (construct_p_omega_coupled.py) tested whether ADDITIVE nearest-
neighbour cross-rung coupling closes the dead zone. Result: it does not at
narrow bands -- for every coupling strength g tested, dim(P_omega) = 0 for
band half-width <= 0.15. Coupling pushed the right direction (it aligned the
rungs, lifted mid-band occupancy) but was too weak in that form to reach the
narrow-corridor regime the framework actually claims.

Diagnosis: additive coupling is the wrong model. The framework's rungs NEST
by coarse-graining (Piece 6; the RG / MERA picture). Rung n+1 is not an
independent operator with a coupling bolted on -- it is a coarse-graining of
rung n. Then the corridor subspaces are related by the RG step, not in
generic position.

This script builds that. All three rungs carry a correlation structure that
is RG-inherited; a flow parameter measures distance from the RG fixed point.
  flow = 0 : all rungs carry the SAME coupling (RG fixed point) -- the
             corridor structure is coarse-grained, not independent.
  flow = 1 : the independent per-rung couplings of general.py -- the dead
             zone.
  coupling_n(flow) = (1 - flow) * base  +  flow * independent_n

QUESTION: at / near the RG fixed point (flow -> 0), is the narrow-band dead
zone closed? If yes, the multi-rung P_omega is viable specifically near an RG
fixed point -- a sharp, framework-faithful result that rhymes with asymptotic-
safety QG (gravity defined by a non-trivial UV fixed point). If the dead zone
survives even at the fixed point, it is robust, and the multi-rung P_omega is
in genuine trouble.
"""
import numpy as np
import itertools

np.set_printoptions(precision=4, suppress=True, linewidth=100)

M = 8
dim = 2 ** M

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def kron_all(ops):
    out = ops[0]
    for o in ops[1:]:
        out = np.kron(out, o)
    return out


def site(op, i):
    ops = [I2] * M
    ops[i] = op
    return kron_all(ops)


SX = [site(X, i) for i in range(M)]
SY = [site(Y, i) for i in range(M)]
SZ = [site(Z, i) for i in range(M)]


def collective(group, P):
    return sum(P[i] for i in group) / len(group)


def intra_correlation(groups, coupling):
    a, b, c = coupling
    gx = [collective(g, SX) for g in groups]
    gy = [collective(g, SY) for g in groups]
    gz = [collective(g, SZ) for g in groups]
    op = np.zeros((dim, dim), dtype=complex)
    pairs = list(itertools.combinations(range(len(groups)), 2))
    for (p, q) in pairs:
        op += a * gx[p] @ gx[q] + b * gy[p] @ gy[q] + c * gz[p] @ gz[q]
    return op / max(1, len(pairs))


def band_projector(op_hat, lo, hi):
    w, V = np.linalg.eigh(op_hat)
    Vb = V[:, (w >= lo) & (w <= hi)]
    return Vb @ Vb.conj().T


def p_omega(projectors):
    avg = sum(projectors) / len(projectors)
    w, V = np.linalg.eigh(avg)
    Vsel = V[:, w > 1 - 1e-9]
    return Vsel @ Vsel.conj().T


rung0 = [[i] for i in range(M)]
rung1 = [[2 * b, 2 * b + 1] for b in range(M // 2)]
rung2 = [list(range(0, M // 2)), list(range(M // 2, M))]
rungs = [rung0, rung1, rung2]

# RG fixed-point coupling (anisotropic, non-SU(2)); shared across all rungs
base = np.array([0.9, 1.3, 0.6])
# the independent per-rung couplings of general.py (same RNG seed / draw order)
rng = np.random.default_rng(20260520)
independent = [rng.uniform(0.4, 1.6, size=3) for _ in range(3)]


def coupling_n(n, flow):
    return tuple((1 - flow) * base + flow * independent[n])


def rho_n(n, flow):
    op = intra_correlation(rungs[n], coupling_n(n, flow))
    op = (op + op.conj().T) / 2
    w = np.linalg.eigvalsh(op)
    return (op - w[0] * np.eye(dim)) / (w[-1] - w[0])


flow_vals = [0.0, 0.1, 0.25, 0.5, 0.75, 1.0]
w_vals = [0.05, 0.10, 0.15, 0.20, 0.30, 0.40]

print("=" * 78)
print("STEP 1 -- rung alignment vs RG flow distance from the fixed point")
print("=" * 78)
print(f"  mean inter-rung commutator ||[rho_a, rho_b]|| of the rescaled")
print(f"  corridor-defining operators (flow = 0 is the RG fixed point):")
for flow in flow_vals:
    rhos = [rho_n(n, flow) for n in range(3)]
    cs = [np.abs(rhos[a] @ rhos[b] - rhos[b] @ rhos[a]).max()
          for a in range(3) for b in range(a + 1, 3)]
    print(f"    flow = {flow:>4.2f} : mean commutator {np.mean(cs):.4e}")

print()
print("=" * 78)
print("STEP 2 -- 2D sweep: dim(P_omega) over (RG flow) x (band half-width)")
print("=" * 78)
print("  flow \\ w  " + "".join(f"{w:>9.2f}" for w in w_vals))
grid = {}
for flow in flow_vals:
    rhos = [rho_n(n, flow) for n in range(3)]
    row = f"   {flow:>5.2f}  "
    for w in w_vals:
        Pw = [band_projector(r, 0.5 - w, 0.5 + w) for r in rhos]
        r = int(round(np.trace(p_omega(Pw)).real))
        grid[(flow, w)] = r
        row += f"{r:>9d}"
    print(row)
print(f"  (cells are dim(P_omega); divide by {dim} for Hilbert-space fraction)")

print()
print("=" * 78)
print("STEP 3 -- is the narrow-band dead zone closed near the fixed point?")
print("=" * 78)
narrow_w = [w for w in w_vals if w <= 0.15]
for flow in flow_vals:
    cells = [(w, grid[(flow, w)]) for w in narrow_w]
    rescued = [w for w, r in cells if r > 0]
    detail = "  ".join(f"w={w}:{r}" for w, r in cells)
    tag = (f"narrow bands rescued: {rescued}" if rescued
           else "narrow-band dead zone INTACT")
    print(f"  flow = {flow:>4.2f} | {detail} | {tag}")

fp_narrow = [grid[(0.0, w)] for w in narrow_w]
fixed_point_closes = any(r > 0 for r in fp_narrow)
# selective => non-empty but well below generic (< 50% of the space)
fp_selective = [w for w in narrow_w if 0 < grid[(0.0, w)] < dim * 0.5]

print()
print("=" * 78)
print("RESULT")
print("=" * 78)
if fixed_point_closes:
    print(f"  At the RG fixed point (flow = 0) the narrow-band dead zone is")
    print(f"  CLOSED: band half-widths {fp_selective} give a non-empty")
    print(f"  selective P_omega. The multi-rung corridor object is viable")
    print(f"  specifically near an RG fixed point -- and degrades as the flow")
    print(f"  carries the rungs away from it. This is the framework-faithful")
    print(f"  result and it rhymes with asymptotic-safety QG. Model 1' gate")
    print(f"  PASSED -> Model 2: does the fixed-point coupling tie UV to IR?")
else:
    print(f"  Even at the RG fixed point (flow = 0, all rungs sharing one")
    print(f"  coarse-grained coupling structure) the narrow-band dead zone")
    print(f"  SURVIVES: dim(P_omega) = 0 for band half-widths {narrow_w}.")
    print(f"  The dead zone is robust to both additive coupling (Model 1) and")
    print(f"  RG coarse-graining (Model 1'). The multi-rung P_omega is in")
    print(f"  genuine trouble at narrow bands -- the QG line cannot proceed")
    print(f"  on a narrow-corridor reading. Honest no-go at gate 1.")
