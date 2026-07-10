# Physics vs bookkeeping: does the classical-S corridor track the true quantum entanglement corridor?

**Verdict: MIXED — and the mixing is structured, which is the result.** In the physically
natural (order-parameter) basis the classical instrument is a **faithful shadow** of the
entanglement ledger; in the conjugate basis it is blind, exactly as clause 3 requires. This
is **not bookkeeping** (a shadow-only outcome), and it is not pure blindness. Summary written
by the orchestrator from executed `results.json`; the load-bearing tracking correlations were
recomputed independently before this was written.

## The decisive test — tracking across a quantum phase transition

Transverse-field Ising chain, exact diagonalization, swept across its critical point (g=1).
At each coupling, compute BOTH our classical `S = −ln det C` (outcome-correlation, per basis)
and the true quantum structure: bipartite entanglement entropy `S_half`, pairwise quantum
mutual information `Q_pair`. Spearman correlation of the classical corridor with the quantum
corridor across the sweep (n=40 couplings), recomputed by the orchestrator:

| sector | classical basis | vs entanglement entropy `S_half` | vs quantum MI `Q_pair` |
|---|---|---|---|
| symmetric | **Z (order-parameter)** | **+0.97** | **+1.00** |
| symmetric | X (conjugate) | −0.97 | −1.00 |
| broken | **Z (order-parameter)** | **+0.98** | **+0.99** |
| broken | X (conjugate) | +0.61 | +0.58 |

**In the order-parameter basis the classical instrument tracks the true entanglement structure
at Spearman +0.97 to +1.00** — not just the pairwise quantum MI (which one might expect to
match a pairwise classical quantity), but the *bipartite entanglement entropy* `S_half`, a
genuinely global/higher-order quantity, at +0.97/+0.98. The entanglement corridor is real and
independently present (the quantum system has the two-pole/critical structure on its own), and
our classical shadow reads it faithfully when pointed at the right observable.

**In the conjugate basis it anti-tracks or decorrelates** (−1.00 in the symmetric sector) —
the clause-3 amplitude/basis blindness, quantified.

## The GHZ calibration — the blind spot, made exact

| GHZ (N=6) | value |
|---|---|
| true bipartite entanglement `S_half` | 0.693 (maximal for the cut) |
| true total correlation `T_total` | 4.16; pairwise quantum MI `Q_pair` = 10.4 |
| classical `S`, X and Y basis | **0.0** (totally blind) |
| classical `S`, Z basis | a *pole* (reads rigidity) |
| basis sweep, max over basis | 31.8 (a pole exists in some basis) |

GHZ is the extreme: genuine multipartite entanglement is maximal while classical `S` reads
exactly zero in the conjugate bases. The gap is total. This is the documented order-≥3 blind
spot with a number on it, and it is why the instrument is basis-dependent: some coordination
lives entirely off the pairwise-outcome ledger in the natural basis.

## What this settles

- **NOT bookkeeping.** A shadow-only outcome would be a classical corridor with no
  entanglement counterpart. The opposite is observed: the entanglement corridor is real and
  the classical one tracks it at ρ≈1.0 in the right basis. Our framework, when correctly
  pointed, is a *faithful classical shadow of the entanglement ledger* — the ledger whose
  currency is what gravity actually reads.
- **The failures are exactly the theorem's.** Where classical `S` misses the entanglement, it
  misses it in the conjugate basis (clause 3) and on genuinely multipartite states (GHZ, the
  order-≥3 door). The blindness is not random noise; it is the proved null space, confirmed.
- **The instrument needs the right basis/grain** — the framework's own Gate-0 discipline
  (fix the grain before the spectrum) is not a nicety here; it is the difference between
  Spearman +1.0 and −1.0.

## Honest limits

- Small N (6–12 qubits), exact-diagonalization finite size; the phase transition is sharp in
  a clean model and messier in real systems.
- `Q_pair` (pairwise quantum MI) tracking a pairwise classical quantity is partly expected;
  the non-trivial result is `S_half` (global bipartite entanglement) tracking at +0.97/+0.98.
- "The right basis" is knowable here because we know the order parameter. For a system whose
  order parameter is unknown, the instrument requires a basis sweep — which is exactly what
  the framework already prescribes, and exactly where it can fail silently if the grain is
  chosen wrong.
- This validates that the classical instrument *can* read the entanglement ledger; it does
  not run on quantum hardware. Randomized-measurement / classical-shadows estimation
  (Huang–Kueng–Preskill) is the hardware version and the natural next step.

## Bottom line

The single most important open question of the program — is the corridor physics or
bookkeeping — comes back: **physics, conditionally.** The corridor exists in the true quantum
entanglement, and the classical instrument reads it faithfully (Spearman ~1.0 across a phase
transition, including the global entanglement entropy) *in the order-parameter basis*, failing
exactly and only where the amplitude-blindness theorem says it must. The framework is a
faithful, basis-dependent shadow of the entanglement ledger — not an elaborate re-description
of classical statistics.

Artifacts: `entanglement_ledger.py`, `results.json`, figures.
