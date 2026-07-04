# Evidence registry — `lean:` tier (CC 1.0-rc2)

`cc_lean.tsv` maps CIRISConstitution **Part VI** (the coherence mathematics) claims
to **stable theorem anchors** in this repo's Lean lake. It is the `lean:` leg of the
four-artifact evidence set (Constitution → Spec → Impl → **Formal**); it companions
CIRISConstitution#17 and RATCHET#8 (which owns the `bench:` leg).

## Columns

`cc_decimal_id | cc_claim_id | module_theorem | status | note`

- **module_theorem** — a `Core.<Module>.<name>` anchor, resolvable as
  `lean:coherence-ratchet:Core.<Module>.<name>` at a pinned commit. `RATCHET:…`
  denotes an anchor that lives in the sibling RATCHET lake; `—` means no Lean
  anchor exists.
- **status** — `mechanized` (a real theorem/def, no `sorry`) or `open` (not proved
  in-lake; the Constitution MUST tag it `open`, not `lean`).

## Status summary

| CC | claim | status | anchor |
|----|-------|--------|--------|
| 6.2.2 | Kish identity + ceiling k_eff→1/ρ̄ | **mechanized** | `Core.BaseIdentity.k_eff_asymptotic_ceiling` (+ identity/K3/K4) |
| 6.2.1 | collapse theorem + preconditions | **open** | decay+remainder in RATCHET / `#4`; corridor structure + collapse direction mechanized here |
| 6.2.4 | J = F = k_eff·λ_op·σ | **mechanized** | `Core.Coherence.J_eq_F` |
| 6.2.3 | σ exp-decay semigroup | **mechanized** | `Core.Coherence.sigma_decay_semigroup` |
| 6.2.3.1 | σ signal-source discount | **open** | unpatched gap `#5`; no anchor |

## Known registry drift (action required upstream)

- **CC 6.2.4** — `claims.tsv` points `CLM-math-JF` at `lean:coherence-ratchet:Core.Corridor`,
  which contains **no** `J=F` theorem. The anchor now lives at `Core.Coherence.J_eq_F`
  (commit added the module). The Constitution pointer must be **repointed** to
  `Core.Coherence` (tracked in the CIRISConstitution repoint issue).

## Verify

`./verify_lean_anchors.sh` checks that every `mechanized` in-lake anchor resolves to
a real declaration in the lake at the current commit. Run in CI to keep the
Constitution from overclaiming a proof the lake no longer has.
