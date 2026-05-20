"""
Model 1'' of the QG-via-P_omega pipeline: the MERA isometry tower.
==================================================================

Models 1 and 1' tested P_omega as an intersection of per-rung corridor
subspaces on ONE shared Hilbert space. Both hit a robust narrow-band dead
zone: three narrow subspaces in generic position in a large space do not
intersect.

This script builds the framework-faithful alternative -- the rungs live on
DIFFERENT Hilbert spaces of decreasing dimension, connected by coarse-
graining isometries (the MERA / RG picture). Rung n+1's correlation operator
is the coarse-graining of rung n's, not an independent operator.

  H_0 (256) --W_0--> H_1 (64) --W_1--> H_2 (16)
  W_0, W_1 are isometries (W^dag W = I); each keeps a block's low-energy
  subspace -- the RG-relevant degrees of freedom.
  rho_0 on H_0 ; rho_1 = W_0^dag rho_0 W_0 ; rho_2 = W_1^dag rho_1 W_1.

P_omega is still an intersection, but of the per-rung corridor projectors
PULLED BACK to H_0:
  Ptil_0 = P_0
  Ptil_1 = W_0 P_1 W_0^dag               (supported in range W_0,    dim 64)
  Ptil_2 = (W_0 W_1) P_2 (W_0 W_1)^dag   (supported in range W_0 W_1, dim 16)
The pulled-back projectors are NOT in generic position -- they are confined
to nested subspaces. dim(P_omega) <= dim(H_2) = 16: the coarsest rung is the
bottleneck.

QUESTION: does the narrow-band dead zone close in the isometry tower? It is
genuinely open -- the corridor of a compressed operator is not the
compression of the fine corridor, so the pulled-back projectors are nested
but not trivially aligned. Could land non-empty-and-selective, empty, or
trivial (P_omega collapsing to P_0).
"""
import numpy as np
import itertools

np.set_printoptions(precision=4, suppress=True, linewidth=100)

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def kron_all(ops):
    out = ops[0]
    for o in ops[1:]:
        out = np.kron(out, o)
    return out


def nsite(op, i, n):
    ops = [I2] * n
    ops[i] = op
    return kron_all(ops)


print("=" * 78)
print("STEP 1 -- build the coarse-graining isometries (keep low-energy subspace)")
print("=" * 78)

# block Hamiltonian on a 4-spin block (16-dim), anisotropic nearest-neighbour
Hblk = np.zeros((16, 16), dtype=complex)
for i in range(3):
    Hblk += (0.9 * nsite(X, i, 4) @ nsite(X, i + 1, 4)
             + 1.3 * nsite(Y, i, 4) @ nsite(Y, i + 1, 4)
             + 0.6 * nsite(Z, i, 4) @ nsite(Z, i + 1, 4))
Hblk = (Hblk + Hblk.conj().T) / 2
wb, Vb = np.linalg.eigh(Hblk)
w0 = Vb[:, :8]                       # C^8 -> C^16 : keep 8 lowest of 16
# layer-1 block "Hamiltonian": the layer-0 Hamiltonian compressed to kept space
Hblk8 = w0.conj().T @ Hblk @ w0      # 8 x 8
w8, V8 = np.linalg.eigh((Hblk8 + Hblk8.conj().T) / 2)
w1 = V8[:, :4]                       # C^4 -> C^8 : keep 4 lowest of 8

W0 = np.kron(w0, w0)                 # H_1 (64) -> H_0 (256)
W1 = np.kron(w1, w1)                 # H_2 (16) -> H_1 (64)
W01 = W0 @ W1                        # H_2 (16) -> H_0 (256)

for name, W, d in [("W0", W0, 64), ("W1", W1, 16), ("W0 W1", W01, 16)]:
    err = np.abs(W.conj().T @ W - np.eye(d)).max()
    print(f"  {name:>6s}: shape {W.shape}, isometry ||W^dag W - I|| = {err:.2e}")

print()
print("=" * 78)
print("STEP 2 -- rho_n by RG coarse-graining: rho_1 = W0^dag rho_0 W0, etc.")
print("=" * 78)
# rho_0: anisotropic correlation among 8 single spins on H_0 (256)
SX = [nsite(X, i, 8) for i in range(8)]
SY = [nsite(Y, i, 8) for i in range(8)]
SZ = [nsite(Z, i, 8) for i in range(8)]
a, b, c = 0.9, 1.3, 0.6
rho0 = np.zeros((256, 256), dtype=complex)
pairs = list(itertools.combinations(range(8), 2))
for (i, j) in pairs:
    rho0 += a * SX[i] @ SX[j] + b * SY[i] @ SY[j] + c * SZ[i] @ SZ[j]
rho0 = (rho0 / len(pairs))
rho0 = (rho0 + rho0.conj().T) / 2
rho1 = W0.conj().T @ rho0 @ W0
rho2 = W1.conj().T @ rho1 @ W1
rho1 = (rho1 + rho1.conj().T) / 2
rho2 = (rho2 + rho2.conj().T) / 2

rhos = [rho0, rho1, rho2]
Ws = [np.eye(256, dtype=complex), W0, W01]   # pullback maps H_n -> H_0
for n, r in enumerate(rhos):
    sp = np.linalg.eigvalsh(r)
    print(f"  rho_{n} on H_{n} (dim {r.shape[0]:>3d}): "
          f"spectrum range [{sp[0]:+.3f}, {sp[-1]:+.3f}], "
          f"{len(set(np.round(sp,4)))} distinct eigenvalues")


def rescale01(op):
    w = np.linalg.eigvalsh(op)
    return (op - w[0] * np.eye(op.shape[0])) / (w[-1] - w[0])


def band_projector(op_hat, lo, hi):
    w, V = np.linalg.eigh(op_hat)
    Vb = V[:, (w >= lo) & (w <= hi)]
    return Vb @ Vb.conj().T


def p_omega(projectors):
    avg = sum(projectors) / len(projectors)
    w, V = np.linalg.eigh(avg)
    Vsel = V[:, w > 1 - 1e-9]
    return Vsel @ Vsel.conj().T


rho_hat = [rescale01(r) for r in rhos]

print()
print("=" * 78)
print("STEP 3 -- band sweep: dim(P_omega) in the pulled-back H_0 space")
print("=" * 78)
print(f"  P_omega = intersection of the three corridor projectors pulled back")
print(f"  to H_0; bounded above by dim(H_2) = 16.")
print(f"  {'half-width':>11} {'band':>14} {'rk P0,P1,P2':>14} "
      f"{'dim P_omega':>12} {'fraction':>10}")
w_vals = [0.05, 0.10, 0.15, 0.20, 0.30, 0.40]
curve = []
for w_half in w_vals:
    lo, hi = 0.5 - w_half, 0.5 + w_half
    P_local = [band_projector(rho_hat[n], lo, hi) for n in range(3)]
    P_tilde = [Ws[n] @ P_local[n] @ Ws[n].conj().T for n in range(3)]
    Pom = p_omega(P_tilde)
    rk = [int(round(np.trace(p).real)) for p in P_local]
    r = int(round(np.trace(Pom).real))
    curve.append((w_half, r))
    print(f"  {w_half:>11.2f} {f'[{lo:.2f},{hi:.2f}]':>14} "
          f"{str(tuple(rk)):>14} {r:>12d} {r/256:>9.2%}")

print()
print("=" * 78)
print("STEP 4 -- is the narrow-band dead zone closed in the isometry tower?")
print("=" * 78)
narrow = [(w, r) for w, r in curve if w <= 0.15]
narrow_nonempty = [w for w, r in narrow if r > 0]
selective = [(w, r) for w, r in curve if 0 < r < 256 * 0.5]
for w, r in narrow:
    print(f"  band half-width {w:>4.2f}: dim(P_omega) = {r}  "
          f"({'NON-EMPTY' if r > 0 else 'empty'})")

print()
print("=" * 78)
print("RESULT")
print("=" * 78)
if narrow_nonempty:
    best = min((v for v in selective if v[0] <= 0.15), key=lambda t: t[0],
               default=None)
    print(f"  The MERA isometry tower CLOSES the narrow-band dead zone:")
    print(f"  band half-widths {narrow_nonempty} give a non-empty P_omega.")
    print(f"  Because the rungs live on nested spaces, the pulled-back corridor")
    print(f"  projectors are confined to nested subspaces and DO intersect.")
    print(f"  dim(P_omega) is bounded by the coarsest rung (dim H_2 = 16) --")
    print(f"  the multi-rung corridor is small but real. Gate 1 PASSED via the")
    print(f"  isometry tower. What unblocks Model 2: characterise whether the")
    print(f"  coarse-graining isometries carry UV-to-IR (RG) structure.")
else:
    print(f"  Even the MERA isometry tower does NOT close the narrow-band dead")
    print(f"  zone: dim(P_omega) = 0 for band half-widths {[w for w,_ in narrow]}.")
    print(f"  The hard-projector multi-rung P_omega is obstructed across all")
    print(f"  three constructions (shared-space, RG-coupled, isometry tower).")
    print(f"  The remaining route is a SOFT P_omega -- a graded operator, not a")
    print(f"  projector. That is the reformulation to take to Model 2.")
