"""
Model 1 of the QG-via-P_omega pipeline: cross-rung coupling vs. the dead zone.
==============================================================================

construct_p_omega_general.py found a DEAD ZONE: on a non-SU(2) substrate with
rungs in GENERIC relative position (independent couplings, no cross-rung
correlation), the three rung-corridor subspaces do not intersect for narrow
bands -- P_omega = 0, the multi-rung corridor object is vacuous.

But the framework's rungs are NOT in generic position. Piece 6 asserts
cross-rung coupling tau_{n,n+1}, itself held in a corridor. The first
construction (construct_p_omega.py) already carried cross-rung coupling -- in
the forward Hamiltonian. The general.py toy dropped it from the corridor-
DEFINING operators rho_n. This script puts it back as a tunable knob g.

If "QG is a cross-rung interaction" (the working hypothesis of the QG line),
then the cross-rung coupling tested here IS the candidate QG-coupling, and the
g-window where the multi-rung P_omega is non-empty AND selective is the
tau-corridor the framework would claim geometry lives in.

MODEL
-----
Same M=8-spin, 256-dim, 3-RG-rung nesting and the same anisotropic non-SU(2)
intra-rung correlation operators as general.py (same RNG seed -> the g=0 row
reproduces the dead zone exactly). Added: nearest-neighbour cross-rung
coupling of strength g in the corridor-DEFINING operators --

    rho_n(g) = intra_n  +  g * sum_{m adjacent to n} cross_{n,m}

cross_{n,m} anisotropically correlates rung n's collective variables with
rung m's. Adjacency: rung 0 ~ rung 1 ~ rung 2.

QUESTION
--------
Sweep g and corridor band width. Is there a region -- intermediate g, narrow
band -- where dim(P_omega) is NON-EMPTY and SELECTIVE (not generic)? If yes,
that viable g-window is the candidate tau-corridor and the QG line proceeds to
Model 2. If the dead zone persists for all g, or only closes by going generic,
the QG line is dead here.
"""
import numpy as np
import itertools

np.set_printoptions(precision=4, suppress=True, linewidth=100)

M = 8
dim = 2 ** M
rng = np.random.default_rng(20260520)

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
    """Anisotropic non-SU(2) correlation within one rung's collective vars."""
    a, b, c = coupling
    gx = [collective(g, SX) for g in groups]
    gy = [collective(g, SY) for g in groups]
    gz = [collective(g, SZ) for g in groups]
    op = np.zeros((dim, dim), dtype=complex)
    pairs = list(itertools.combinations(range(len(groups)), 2))
    for (p, q) in pairs:
        op += a * gx[p] @ gx[q] + b * gy[p] @ gy[q] + c * gz[p] @ gz[q]
    return op / max(1, len(pairs))


def cross_correlation(groups_n, groups_m, coupling):
    """Anisotropic correlation BETWEEN rung n's and rung m's collective
    variables -- the cross-rung coupling term."""
    a, b, c = coupling
    gxn = [collective(g, SX) for g in groups_n]
    gxm = [collective(g, SX) for g in groups_m]
    gyn = [collective(g, SY) for g in groups_n]
    gym = [collective(g, SY) for g in groups_m]
    gzn = [collective(g, SZ) for g in groups_n]
    gzm = [collective(g, SZ) for g in groups_m]
    op = np.zeros((dim, dim), dtype=complex)
    cnt = 0
    for p in range(len(groups_n)):
        for q in range(len(groups_m)):
            op += a * gxn[p] @ gxm[q] + b * gyn[p] @ gym[q] + c * gzn[p] @ gzm[q]
            cnt += 1
    return op / max(1, cnt)


rung0 = [[i] for i in range(M)]
rung1 = [[2 * b, 2 * b + 1] for b in range(M // 2)]
rung2 = [list(range(0, M // 2)), list(range(M // 2, M))]
rungs = [rung0, rung1, rung2]

# same RNG draw order as general.py: 3 intra couplings, then 2 cross couplings
intra_coupl = [tuple(rng.uniform(0.4, 1.6, size=3)) for _ in range(3)]
cross_coupl = [tuple(rng.uniform(0.4, 1.6, size=3)) for _ in range(2)]

intra = [intra_correlation(rungs[n], intra_coupl[n]) for n in range(3)]
cross01 = cross_correlation(rungs[0], rungs[1], cross_coupl[0])
cross12 = cross_correlation(rungs[1], rungs[2], cross_coupl[1])
cross01 = (cross01 + cross01.conj().T) / 2
cross12 = (cross12 + cross12.conj().T) / 2
neighbor_cross = {0: [cross01], 1: [cross01, cross12], 2: [cross12]}


def rho_of_g(n, g):
    """Corridor-defining operator for rung n at cross-rung coupling g,
    rescaled so its spectrum lands in [0, 1]."""
    op = intra[n].copy()
    for c in neighbor_cross[n]:
        op = op + g * c
    op = (op + op.conj().T) / 2
    w = np.linalg.eigvalsh(op)
    return (op - w[0] * np.eye(dim)) / (w[-1] - w[0])


def band_projector(op_hat, lo, hi):
    w, V = np.linalg.eigh(op_hat)
    Vb = V[:, (w >= lo) & (w <= hi)]
    return Vb @ Vb.conj().T


def p_omega(projectors):
    """Exact intersection projector -- eigenvalue-1 space of the averaged
    projector (valid for non-commuting P_n)."""
    avg = sum(projectors) / len(projectors)
    w, V = np.linalg.eigh(avg)
    Vsel = V[:, w > 1 - 1e-9]
    return Vsel @ Vsel.conj().T


g_vals = [0.0, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0, 1.5]
w_vals = [0.05, 0.10, 0.15, 0.20, 0.30, 0.40]

print("=" * 78)
print("STEP 1 -- does cross-rung coupling g align the rungs?")
print("=" * 78)
print(f"  mean inter-rung commutator ||[rho_a, rho_b]|| of the rescaled")
print(f"  corridor-defining operators, vs coupling g:")
for g in g_vals:
    rhos = [rho_of_g(n, g) for n in range(3)]
    cs = [np.abs(rhos[a] @ rhos[b] - rhos[b] @ rhos[a]).max()
          for a in range(3) for b in range(a + 1, 3)]
    print(f"    g = {g:>4.2f} : mean commutator {np.mean(cs):.4e}")

print()
print("=" * 78)
print("STEP 2 -- 2D sweep: dim(P_omega) over (coupling g) x (band half-width)")
print("=" * 78)
header = "    g \\ w  " + "".join(f"{w:>9.2f}" for w in w_vals)
print(header)
grid = {}
for g in g_vals:
    rhos = [rho_of_g(n, g) for n in range(3)]
    row = f"   {g:>5.2f}  "
    for w in w_vals:
        Pw = [band_projector(r, 0.5 - w, 0.5 + w) for r in rhos]
        r = int(round(np.trace(p_omega(Pw)).real))
        grid[(g, w)] = r
        row += f"{r:>9d}"
    print(row)
print(f"  (cells are dim(P_omega); divide by {dim} for Hilbert-space fraction)")

print()
print("=" * 78)
print("STEP 3 -- viable cells: non-empty AND selective (0 < fraction < 0.5)")
print("=" * 78)
viable = [(g, w, grid[(g, w)]) for g in g_vals for w in w_vals
          if 0 < grid[(g, w)] < dim * 0.5]
deadzone_g0 = [w for w in w_vals if grid[(0.0, w)] == 0]
print(f"  g = 0 (no cross-rung coupling) dead zone: band half-widths "
      f"{deadzone_g0} give dim(P_omega) = 0  [control -- reproduces general.py]")
if not viable:
    print(f"  NO viable cell anywhere in the sweep. Cross-rung coupling does not")
    print(f"  open a non-empty-and-selective window. The QG line stops here.")
    best = None
else:
    narrow = [v for v in viable if v[1] <= 0.15]
    print(f"  {len(viable)} viable cell(s). Narrow-band (w <= 0.15) viable cells:")
    if narrow:
        for g, w, r in sorted(narrow, key=lambda t: (t[1], t[0])):
            print(f"    g = {g:>4.2f}, band half-width {w:>4.2f} : "
                  f"dim(P_omega) = {r}  ({r/dim:.2%})")
        # the candidate tau-window: g-range that rescues the narrowest band
        wmin = min(w for _, w, _ in narrow)
        gw = sorted(g for g, w, _ in narrow if w == wmin)
        print(f"  => at the narrowest rescued band (w = {wmin}), cross-rung")
        print(f"     coupling g in {gw} opens a non-empty selective P_omega.")
        print(f"     THIS g-RANGE IS THE CANDIDATE tau-CORRIDOR.")
        best = sorted(narrow, key=lambda t: (t[1], t[2]))[0]
    else:
        print(f"    none at w <= 0.15 -- viable cells exist only at wider bands:")
        for g, w, r in sorted(viable, key=lambda t: (t[1], t[0])):
            print(f"    g = {g:>4.2f}, band half-width {w:>4.2f} : "
                  f"dim(P_omega) = {r}  ({r/dim:.2%})")
        best = sorted(viable, key=lambda t: (t[1], t[2]))[0]

print()
print("=" * 78)
print("STEP 4 -- non-circular TSVF demo at the best viable cell")
print("=" * 78)
if best is None:
    print("  no viable cell -- nothing to post-select through.")
else:
    gb, wb, rb = best
    rhos = [rho_of_g(n, gb) for n in range(3)]
    Pb = [band_projector(r, 0.5 - wb, 0.5 + wb) for r in rhos]
    P_post = p_omega(Pb)
    angles = rng.uniform(0, np.pi, size=M)
    psi0 = np.array([1.0], dtype=complex)
    for i in range(M):
        q = np.array([np.cos(angles[i] / 2), np.sin(angles[i] / 2)], dtype=complex)
        psi0 = np.kron(psi0, q)
    psi0 /= np.linalg.norm(psi0)
    H = sum(intra) + gb * (cross01 + cross12)
    H = (H + H.conj().T) / 2
    eH, UH = np.linalg.eigh(H)
    print(f"  best viable cell: g = {gb}, band half-width {wb}, "
          f"dim(P_omega) = {rb} ({rb/dim:.1%})")
    print(f"  generic product state (independent of P_omega); post-selection")
    print(f"  probability ||P_omega|psi(t)>||^2 along evolution under the")
    print(f"  g-coupled Hamiltonian:")
    for t in [0.0, 0.5, 1.0, 2.0, 4.0]:
        psit = UH @ (np.exp(-1j * eH * t) * (UH.conj().T @ psi0))
        print(f"    t = {t:>4.1f} : {np.linalg.norm(P_post @ psit) ** 2:.4f}")

print()
print("=" * 78)
print("RESULT")
print("=" * 78)
if best is None:
    print(f"  Cross-rung coupling does NOT close the dead zone. Across g in")
    print(f"  {g_vals}, no non-empty selective P_omega exists at any band.")
    print(f"  Model 1 returns a no-go: the multi-rung P_omega stays vacuous,")
    print(f"  and the QG-via-P_omega line stops at gate 1.")
else:
    gb, wb, rb = best
    print(f"  g = 0 reproduces the dead zone (control). Cross-rung coupling")
    print(f"  opens viable -- non-empty AND selective -- P_omega cells.")
    print(f"  Best: g = {gb}, band half-width {wb}, dim(P_omega) = {rb} "
          f"({rb/dim:.1%}).")
    print(f"  The g-window that rescues narrow bands is the candidate")
    print(f"  tau-corridor. Model 1 gate PASSED -> proceed to Model 2:")
    print(f"  does this coupling have renormalization-group (UV-to-IR)")
    print(f"  structure, i.e. is it geometry-like?")
