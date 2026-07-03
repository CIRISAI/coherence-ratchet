# Two-pole dynamics test on macaque ECoG anesthesia (clean re-run)

**Claim under test.** The dynamics piece is now the two-pole form `dρ/dt = α − γ·M`.
At `M=0` (maintenance withdrawn) the system leaves the awake operating point toward
the pole selected by `sign(α)`: **RIGIDITY** (ρ→1, k_eff→1) or **CHAOS** (ρ→0,
k_eff→N). The *weak* reading ("anesthesia exits toward some pole") is nearly
unfalsifiable. The **strong, falsifiable prediction** is that the pole is set by the
agent's mechanism:

- **propofol** (GABA-A, slow-wave **synchronization**) → **RIGIDITY** (ρ↑ / k_eff↓)
- **ketamine** (dissociative, high-frequency **desynchronization**) → **CHAOS** (ρ↓ / k_eff↑)

Two agents landing at **two different poles** is the signature with predictive content.

**Bottom line: the strong prediction FAILS.** The pole is not set by the agent's
mechanism. In the broadband measure both agents go to the *same* pole (rigidity);
switching the analysis band flips propofol to the *opposite* pole. Ketamine never
shows its predicted chaos. The maintenance-withdrawal detailed-balance drop holds for
propofol but not ketamine. Only the weak, near-unfalsifiable reading survives.

## Confound fixes vs the earlier arousal test

| Confound in prior test | Fix here |
|---|---|
| WRONG GRAIN: 19 volume-conducted scalp EEG channels | **128-ch subdural ECoG** (neural field, minimal volume conduction) |
| WRONG PERTURBATION: post-anoxic damage (uncontrolled) | **clean graded pharmacology**, two agents, matched awake baseline **on the same electrodes** |
| single perturbation, no predictive fork | **two agents predicted to hit two different poles** — the actual two-pole signature |

## Data (real, open)

NeuroTycho (Yanagawa, Fujii; RIKEN), monkey **Chibi**, 128-ch subdural ECoG array,
left hemisphere, 1 kHz. Two anesthesia sessions, each an awake→anesthetized→recovery
protocol with `Condition.mat` event markers; awake baseline and anesthetized period
are on the **same implant** within each session (matched channels).

- Propofol: `20120730PF_Anesthesia+and+Sleep_Chibi` (1.26 GB)
- Ketamine: `20120719KT_Anesthesia+and+Sleep_Chibi` (1.47 GB)
- Source list: `http://neurotycho.org/anesthesia-and-sleep-task` → task-78 catalog
  (`http://neurotycho.org/data/detail.json`); files under
  `http://neurotycho.brain.riken.jp/download/2014/`.

Awake = `AwakeEyesOpened`+`AwakeEyesClosed`; drug = `Anesthetized`; recovery =
`RecoveryEyesClosed`+`RecoveryEyesOpened`. 12 non-overlapping 20 s windows per state.

## Matched preprocessing

Identical across all states/agents: same 128 channels (all 128 good in every state),
50 Hz notch, band-pass, decimate to 250 Hz, per-channel z-score, **no re-reference**
(common-average reference would inject spurious anticorrelation and bias k_eff). Only
**within-session, matched awake-vs-drug differences** are read; absolute k_eff is
field/reference-confounded. Core reused verbatim: `corr_eig`, `participation_ratio`
(`spectral_test.py`); `irreversibility_from_units(X, k=4)` (`entropy_production.py`).
k_eff = participation ratio of the channel correlation spectrum; ρ_Kish inverted from
k_eff via the base identity; detailed-balance |z| = top-4-mode winding irreversibility.

## Results — broadband (1–100 Hz)  [primary]

| agent | k_eff awake→drug | ρ_Kish awake→drug | pole | predicted | DB |z| awake→drug |
|---|---|---|---|---|---|
| **propofol** | 14.9 → **6.4** (Δ=−8.5, d=−4.9, p=3.7e-5) | 0.062 → **0.153** (d=+5.9) | **RIGIDITY** | RIGIDITY ✓ | 2.79 → 2.19 (**drop**, p=.046) |
| **ketamine** | 14.5 → **5.3** (Δ=−9.3, d=−4.9, p=3.7e-5) | 0.064 → **0.185** (d=+7.6) | **RIGIDITY** | CHAOS ✗ | 3.51 → 3.82 (**rise**, p=.29 ns) |

Both agents move to the **same** pole (k_eff↓, ρ↑). Ketamine, predicted to go to
chaos, goes to rigidity *more strongly* than propofol. Recovery returns toward awake
in both (propofol k_eff 13.2, ketamine 12.7). **No differential = the strong two-pole
prediction is falsified in broadband.**

## Results — gamma band (30–90 Hz)  [where ketamine's desync mechanism lives]

| agent | k_eff awake→drug | ρ_Kish awake→drug | pole | predicted |
|---|---|---|---|---|
| **propofol** | 18.1 → **27.7** (Δ=+9.6, d=+1.5, p=.014) | 0.070 → 0.029 | **CHAOS** | RIGIDITY ✗ |
| **ketamine** | 20.7 → 18.8 (Δ=−1.9, d=−0.3, p=.37 **ns**) | 0.054 → 0.047 | flat / unclear | CHAOS ✗ |

In gamma the picture **flips**: propofol desynchronizes gamma (k_eff↑ → chaos), the
opposite of its broadband rigidity; ketamine barely moves. **The pole an agent exits
to is band-dependent, not agent-determined** — the same agent (propofol) can be made
to land at either pole by choosing the analysis band. That is the opposite of "the
pole is a property of the agent's mechanism."

## Reading

1. **Strong (predictive) two-pole test: FAILS.** The pole does not track the agent's
   mechanism. Broadband: both agents → rigidity (no fork). Gamma: propofol → chaos,
   ketamine → flat (a fork, but with propofol on the *wrong* side and ketamine still
   not at chaos). No band gives the predicted propofol-rigidity / ketamine-chaos split.
2. **Ketamine never reaches chaos.** Predicted chaos in both bands; observed rigidity
   (broadband) or no change (gamma). The one agent chosen to demonstrate the *second*
   pole does not.
3. **Maintenance-withdrawal (DB drop): inconsistent across agents.** Propofol's |z|
   drops under anesthesia in both bands (consistent with less active γ·M). Ketamine's
   is flat (broadband slight rise, gamma flat). So even the pole-agnostic
   "DB drops under anesthesia" signature is not robust.
4. **Weak reading survives, trivially.** Anesthesia does move the system off its awake
   operating point in every condition (large effects), so "exits toward *some* pole"
   is satisfied — but with no predictive content, exactly the near-unfalsifiable
   version the strong test was meant to replace.

**Corridor-bounds wrinkle (reported, not leaned on).** By the GPU-inherited literal
bounds (ρ∈(0.1,0.43)), awake ECoG here sits *below* the corridor floor (ρ≈0.06,
k_eff≈14.5>10 ceiling) and both anesthetics move ρ *up into* the corridor
(0.15–0.19), i.e. toward rigidity but not out the top. Read as direction only; the
CLAUDE.md bounds are un-calibrated for this substrate (per-substrate calibration is
open work), so this is not scored as pass/fail — only the differential-pole prediction is.

## Caveats

- ECoG is a mesoscopic **field**, better than scalp but not single neurons; residual
  shared-field/reference structure inflates absolute correlation (why only matched
  differences are read).
- **One monkey.** Chibi only; George (PF `20120731`/`20120803`, KT `20120724`/
  `20120810`) is the obvious replication and is available at the same source. Not run
  here to keep the download modest; the within-subject falsification is already
  two-band and both-agent.
- Awake vs anesthetized are separate contiguous sub-recordings (same day, same
  implant); acquisition drift across sub-recordings is a residual confound, mitigated
  by the recovery state returning toward awake.
- Band choice is itself a researcher degree of freedom — which is precisely the point:
  the pole assignment is not band-robust.

## Bottom line

**The two-pole dynamics does not survive a clean, right-grain test with predictive
content.** On matched 128-ch macaque ECoG, propofol and ketamine — chosen to fall on
opposite poles — land on the *same* pole (rigidity) in broadband, and the apparent
pole flips with the analysis band rather than with the agent. Ketamine never shows the
predicted chaos. The falsifiable prediction (pole set by mechanism) is rejected; only
the near-unfalsifiable "exits somewhere" reading is left standing.

Outputs: `spectral_results_twopole.json` (broadband),
`spectral_results_twopole_gamma.json` (gamma), `spectral_twopole.py`.
