# Result — particle decay concentration at fixed Q-value

Date: 2026-05-21. Run AFTER PREREGISTRATION.md was committed (commit f6e97a7).

## Verdict: NULL — no corridor.

The pre-registered corridor bar (std(rho) < 0.10 under BOTH confound controls,
median in [0.15, 0.45], pole fraction <= 0.20) is NOT cleared. It is not cleared
under either control, let alone both.

## Numbers (PDG 2025, `pdg` v0.2.2, real data)

13 particles with >= 5 clean exclusive Q-resolvable decay channels (baseline,
B2); 9 survive the B1 Q-band cut. (D_s+, B_s0, Lambda_c+, K(S)0, K(L)0, the
narrow Upsilon/Delta states drop on PDG-package name/PDGITEM resolution
failures or too few clean channels — data-access limitation, not faked around.)

| Control | n | rho range | median | std | pole fraction |
|---|---|---|---|---|---|
| Baseline (confound A only — fixed N, no Q control) | 13 | [0.014, 0.992] | 0.166 | 0.372 | 0.69 |
| B1 — Q-band restriction Q/M in [0.05, 0.60] | 9 | [0.016, 0.997] | 0.199 | 0.300 | 0.44 |
| B2 — phase-space normalisation BF / Q^((3n-5)/2) | 13 | [0.008, 0.981] | 0.174 | 0.360 | 0.360 |

The pre-registered bar is std < 0.10. The observed std is 0.30-0.37 — three to
four times the bar. The distribution still runs essentially pole to pole
(0.01 to 0.99). Pole fraction is 0.44-0.85, far above the 0.20 cap.

## Reading

The kinematic phase-space confound was a real confound but was NOT the cause of
E4's broad spread. Controlling it (B1 narrows std from 0.372 to 0.300; B2
barely moves it, 0.372 -> 0.360) leaves the distribution essentially as broad
as E4 found. The broad spread is intrinsic to particle decay-channel
concentration, not a kinematic artefact.

The numbers also show *why*: at fixed Q-value the particles split by physics,
not into a band. The heavy-flavour weak decayers (D0, D+, B+, B0, J/psi,
chi_c0) sit near the chaos pole (rho 0.01-0.06) — their decay strength is
genuinely spread across many comparable channels. The light vector and hyperon
states (rho(770), phi(1020), K+, Sigma+) sit near the rigidity pole (rho
0.75-0.99) — one channel dominates. The tau and charmonium states land in the
middle. This is two-or-three clusters set by decay mechanism (weak vs strong
vs electromagnetic, multi-channel vs single-dominant), not an attractor band.

This is fully consistent with the framework's own position, stated plainly in
the pre-registration: decay channels are NOT a coordinated rung. There is no
maintenance work, no drho/dt, no attractor dynamics — so there is no reason to
expect a corridor, and none is found. The honest prior was null; the result is
null; E4's null replicates under the additional confound control.
