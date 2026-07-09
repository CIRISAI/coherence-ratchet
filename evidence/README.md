# Evidence registry — `lean:` tier (CC 1.0-rc2)

`cc_lean.tsv` maps CIRISConstitution **Part VI** (the coherence mathematics) claims
to **stable theorem anchors** in this repo's Lean lake. It is the `lean:` leg of the
four-artifact evidence set (Constitution → Spec → Impl → **Formal**); it companions
CIRISConstitution#17 and RATCHET#8 (which owns the `bench:` leg).

## Columns

`cc_decimal_id | cc_claim_id | module_theorem | lean_name | status | note`

- **module_theorem** — the file-based pointer `Core.<Module>.<name>`, as used by
  `lean:coherence-ratchet:…`. `RATCHET:…` denotes an anchor in the sibling RATCHET
  lake; `—` means no Lean anchor exists.
- **lean_name** — the *fully-qualified, resolvable* Lean name. This is not always
  the module path: `Core/BaseIdentity.lean` opens `namespace CoherenceRatchet.Core`,
  so its theorems are `CoherenceRatchet.Core.k_eff_…`, not `…Core.BaseIdentity.…`.
  The verifier resolves this column.
- **status** — `mechanized` (resolves, no `sorryAx`) or `open` (not proved in-lake;
  the Constitution MUST tag it `open`, not `lean`).

## Status summary

| CC | claim | status | anchor |
|----|-------|--------|--------|
| 6.2.2 | Kish identity + ceiling k_eff→1/ρ̄ | **mechanized** | `Core.BaseIdentity.k_eff_asymptotic_ceiling` (+ identity/K3/K4) |
| 6.2.1 | collapse bound, remainder `O(r²·k_eff)` | **mechanized** | `Core.CollapseTheorem.remainder_scales_with_k_eff` (closes #4) |
| 6.2.4 | J = F = k_eff·λ_op·σ | **mechanized** | `Core.Coherence.J_eq_F` |
| 6.2.3 | σ exp-decay semigroup | **mechanized** | `Core.Coherence.sigma_decay_semigroup` |
| 6.2.3.1 | σ signal-source Kish discount | **mechanized** | `Core.SignalSourceDiscount.clique_neutralization` (closes #5) |

## Known registry drift (action required upstream)

- **CC 6.2.4** — `claims.tsv` points `CLM-math-JF` at `lean:coherence-ratchet:Core.Corridor`,
  which contains **no** `J=F` theorem. The anchor lives at `Core.Coherence.J_eq_F`.
  The Constitution pointer must be **repointed** (CIRISConstitution#26).
- **CC 6.2.1 / 6.2.3.1** — `claims.tsv` still tags these `open`. Both are now
  mechanized in-lake (`Core.CollapseTheorem`, `Core.SignalSourceDiscount`), so the
  Constitution *understates* what the lake proves. The verifier reports this as
  `WARN stale-open`.

## Verify

```bash
python3 evidence/verify_lean_anchors.py --self-test   # prove the traps fire
python3 evidence/verify_lean_anchors.py               # check every anchor
```

`verify_lean_anchors.py` resolves each `mechanized` anchor **through Lean itself**
(`#print axioms <lean_name>`), which a grep cannot do. It gives three guarantees:

1. **Resolution** — a renamed or deleted theorem is an `unknown identifier` and fails.
2. **No `sorry`** — a theorem depending on `sorryAx` fails. `mechanized` never means
   "stated with `sorry`".
3. **Axiom audit** — the axioms each anchor *actually* rests on are printed, so
   framework primitives (`λ_geo`, `κ`, `corridorBounds`, `α`/`γ`/`M`) are surfaced
   rather than hidden behind the word "mechanized".

It also warns on **stale-open** drift: a row marked `open` whose anchor nonetheless
resolves and is sorry-free.

Because the lake is currently `sorry`-free, `--self-test` synthesises both failure
modes through real Lean (a `sorry`-proved probe theorem and an absent identifier)
and asserts they are caught — a check that cannot go red is worthless. CI runs the
self-test before trusting the real run: `.github/workflows/lean-evidence.yml`.
