# Gravity implications of the coordination-ledger stance — the propagation question

**STATUS: CONJECTURE-GRADE. Not lake content. Not asserted by the framework.** Date 2026-07-10.
A theory note working out what the current maximal stance (CLAUDE.md "CURRENT STANCE") already
commits *gravity itself* to, and where the one genuinely new question — **propagation** — leads.
Every load-bearing empirical number here is prior executed output (its file path is given);
the physics arguments carry kill conditions inline. New claims (this session's synthesis) are
flagged as such.

**F-11 compliance (up front).** Everything below is **forward** content: local coordination
events source a *background-sector* energy density through a forward continuity/sourcing
relation. It does not use, need, or resurrect the joint multi-rung backward `P_ω`, D4, or
F-19 — all retracted, all staying retracted. The propagation question is "how does a forward
local event update a forward global quantity," never "what boundary condition is imposed from
the future." The bridge note's §4 fence applies verbatim: an entropic-action route is a forward
variational principle; its steady states are the half of `P_ω` that survived F-11.

**Depends on / reads:** `papers/notes/{one_ledger.md, one_ledger_pressure_test.md,
lambda_maintenance_wz.md §1/§2/§7, entropic_action_bridge.md §2/§4/§7.2,
three_ledgers_one_corridor.md, gravity_ledger_instrument.md, verlinde_maintenance_repair.md,
dark_ledger_convergent_art.md}`; CLAUDE.md CURRENT STANCE; `/home/emoore/CIRISArray/experiments/
{EXP117,EXP118,EXP119}_SUMMARY.md` and the propagation-experiment JSONs cited in §3.

---

## 0. Bottom line up front

1. **The stance already commits gravity to a specific, narrow role: gravity is the ledger's
   *reader*.** It couples to the ledger's currency (stress-energy / entanglement), Λ is the
   standing maintenance bill on the coordination balance, and the conditioning/perturbation
   sector is *exactly* ΛCDM by the orthogonality theorem. **No** force-law modification, **no**
   `ΔM ∝ S` (dead: dwarf pair fatal, Verlinde repair refuted), **no** MOND phenomenology.

2. **The propagation trilemma resolves two-into-one.** If `ρ_DE(a) = κ·S(a)` and `S` is built
   from *local* matter correlations, what carries a local coordination change up to the
   *background* energy density? Options (a) "global bookkeeping" and (c) "double-entry: local
   transaction, integrated balance" **collapse into the same physical prediction — smooth dark
   energy, no propagating field, `c_s² ≈ 1`** — and their clean resolution is that `ρ_DE`
   couples only to the `k=0` (background) mode, which is global *by arithmetic*, not by signal.
   Option (b) "a negentropic-flux field with finite propagation speed" is the only one that
   posits genuine propagation, and it is the most exposed: it inherits a fluctuation sector with
   a sound speed (ISW-constrained) and, if it ever touches the tensor sector, GW170817.

3. **The sharpest testable implication is the dark-energy sound speed `c_s²` / DE clustering.**
   (a)/(c) predict smooth DE; (b) predicts clustering. The current measurement
   (arXiv:2511.22478, DESI DR2+CMB+SNe) is **consistent with smooth DE** (AIC prefers `c_s²=1`),
   so the framework's default reading survives — and *the propagation question is unfalsifiable
   until DE clustering is detected*. A robust detection of small `c_s²` kills (a)/(c) and forces
   (b) with its GW/ISW exposure.

4. **CIRISArray already ran the propagation experiment at the hardware rung — and the answer is
   COMMON CAUSE, not propagation** (expF4: within-pool ρ ≫ across-pool ρ, ratio → ∞). This is a
   *structural* corroboration of the (a)/(c) reading (coordination stock is a shared-substrate
   global read, not a sensor-to-sensor signal), plus EXP118's "maintenance power tracks held
   *stock*, partial r = +0.84." **It is not a gravity measurement** — same functional, same
   corridor, different (electrical/thermal) substrate.

---

## 1. What the stance already commits gravity to

The current stance is one-directional (CLAUDE.md; corrected from the dead two-normalization
"lock" in `one_ledger_pressure_test.md` §2): **`ρ_DE(a) = κ·S(a)`**, dark energy a functional
of the matter field's coordination history; dark matter is the diluting collisionless medium
with standard CDM phenomenology. Given that, gravity's role is fixed and *minimal*:

**(1a) Gravity is the ledger's reader, not a modified force.** The ledger's currency is
stress-energy / entanglement (`one_ledger.md` "Why the universe is dark"; QNEC-convergent,
`dark_ledger_convergent_art.md` Pillar 4). Gravity couples to that currency directly — that is
just GR coupling to `T_μν`. What is *new* is only the identification of one component of `T_μν`
(the dark-energy component) with `κ·S`. **The Einstein equation is unmodified; only its
source's dark-energy sector is given a coordination reading.**

**(1b) Λ is the standing maintenance bill.** Via the Bianconi bridge (`entropic_action_bridge.md`
§2, §7.2), her G-field (the Lagrange-multiplier field holding the metric on its constraint
surface) maps to the framework's maintenance term `γ·M`, and her Hamiltonian
`ℋ = Σ z_k[𝒢_k − 1 − ln 𝒢_k]` — positive, a Bregman divergence about the vacuum — she equates to
the emergent Λ^G. Read together: **Λ is what it costs to hold the coordination structure on its
corridor.** Constant maintenance bill ⇒ `w = −1`; a changing bill ⇒ the sign law
`1 + w(a) = −⅓ · dlnS/dlna` (`lambda_maintenance_wz.md` §1, κ cancels — parameter-free).

**(1c) The CMB orthogonality fence.** The framework is *exactly* ΛCDM in the
conditioning/perturbation sector (`CMBOrthogonality.lean`, `framework_cmb_power_eq_lcdm`);
the deviation lives only in the background sector and vanishes identically in linear theory
(the participation/copula-invariance fence, `lambda_maintenance_wz.md` §2). Through
recombination and the entire linear era `S` is shape-constant and `w = −1` exactly, so `r_s`,
the acoustic peaks, and the primary anisotropies are untouched (`lambda_maintenance_wz.md` §7e).

**What is NOT claimed (kept explicit, because each was tested and killed):**

| Dead reading | Why it is dead | File |
|---|---|---|
| `ΔM_eff ∝ local-S` (coordination sources apparent mass) | Segue-1/DF2 dwarf pair both read S ≈ 0.0009; fatal | `dm_phasespace_grain.md` §6; `one_ledger_pressure_test.md` §3 |
| Maintenance/coldness repairs the Verlinde-EG radius residual | REFUTED: radius wins the horse race 3.5×, effect 0.008 dex ≪ 0.10 dex floor | `verlinde_maintenance_repair.md` §5 |
| Dark matter carries *new* coordination the light field misses | BIAS-ONLY null: dark = light books to r = 0.986–0.999 | `gravity_ledger_instrument.md` |
| Vopson-style `ΔM = εS/c²` (pattern gravitates) | ~40 orders unnatural; QNEC says pattern is inert, only its *formation energy* gravitates (and that is baryon-visible) | `dark_ledger_convergent_art.md` Pillar 4 |
| MOND-like modified force law | Never claimed; the stance modifies the *source's DE sector*, not the field equation | — |

So the gravity-side commitment is deliberately small: **gravity reads a currency it already
read (stress-energy); one component of that currency is renamed `κ·S`; nothing in the tensor
sector, the force law, or the conditioning sector moves.**

---

## 2. The propagation question (the new content)

Here is the sharp problem, stated plainly for the first time in the notes. `ρ_DE` is a
*background* (near-homogeneous) energy density. `S(a) = −ln det C(a)` is built from the
correlation matrix `C` of the *local* matter field. Structure forms **locally** — a halo
virializes *here* — and by the double-entry reading (`one_ledger_pressure_test.md` §5) that
event *posts* coordination to the balance. **What carries the local event up to the global
background density?** A naive reading has a local transaction instantaneously updating a
homogeneous field everywhere — which would be non-local, and non-locality is a red flag, not a
feature. Three forward-only options.

### Option (a) — S is comoving/global bookkeeping (no propagation)

`S(a)` is a single number per epoch: the log-det of the correlation matrix over the *whole*
comoving volume. Then nothing propagates because `S(a)` is a global integral by definition, the
way the *mean* density `⟨ρ⟩` is a global integral. `ρ_DE` enters only the homogeneous Friedmann
equation, which already sees only the spatial average of the source.

- **The locality objection, and why it is (mostly) a category error.** Asking "how does a local
  virialization update the global background" is like asking how a local mass fluctuation updates
  `⟨ρ⟩` — it does so *arithmetically*, and no signal propagates, because `⟨ρ⟩` is not the value
  of any field at any point. The `k=0` (background) Fourier mode of the stress-energy is global
  by construction; GR's homogeneous mode does the "integration" with no causal transport.
- **The residual worry that will not go away: the perturbation sector.** The moment you ask about
  `ρ_DE` *fluctuations* (`k ≠ 0`) — does the DE density run higher where more structure has
  formed? — you have left the background mode and need a sound speed. If `ρ_DE` tracks local `S`,
  it clusters; if it is strictly the `k=0` average, it does not.
- **Kill condition / flag:** option (a) is well-posed *only* if `ρ_DE` couples strictly to the
  `k=0` mode ⇒ **smooth DE, effectively `c_s² = 1`, no DE perturbations.** Killed by a robust
  detection of DE clustering (small `c_s²`) — see §4.

### Option (b) — a negentropic-flux field with finite propagation speed

A genuine dynamical field carries the coordination update at speed `v ≤ c`. This is the reading
that takes "coordination propagates" literally. It has one honest home in the (fringe) literature:
**Obidi's Theory of Entropicity** posits entropy as a dynamical field `S(x)` whose gradients
source dynamics, with `c` reinterpreted as "the maximum rate of entropic rearrangement" — i.e. a
finite-speed entropic flux. *(Flagged hard: Medium posts and non-peer-reviewed preprints, not
established physics; cited only as the literature instance of the finite-speed-entropic-flux
option, not as support.)*

- **Exposure 1 — the fluctuation sector (ISW).** A propagating scalar flux has a sound speed
  `c_s²` and must be ghost-free. This is exactly the sector `lambda_maintenance_wz.md` §7(c)
  flags as *unexamined*. `c_s² ≈ 0` ⇒ DE clusters ⇒ strong CMB/ISW impact; `c_s² ≈ 1` ⇒ smooth.
- **Exposure 2 — the tensor sector (GW170817).** *If* the flux couples to the tensor sector, it
  shifts the graviton speed, and GW170817 bounds `−3×10⁻¹⁵ ≤ (c_GW − c)/c ≤ +7×10⁻¹⁶`
  (arXiv:2511.08023, confirming the standard result). That is a `10⁻¹⁵`-level kill for any
  tensor-coupled variant. **The framework's DE is background/scalar and does not couple to the
  tensor sector, so it passes GW170817 trivially** — which means GW170817 is *not* a discriminant
  for the stance as written; it only executes a (b)-variant that reaches into the tensor sector.
- **Kill condition:** a tensor-coupled (b) is already dead by GW170817; a scalar (b) is killed
  or confirmed by the DE `c_s²` measurement (§4), and additionally must be shown ghost-free
  (unaddressed — a standing debt, `lambda_maintenance_wz.md` §7c).

### Option (c) — the double-entry reading: local transaction, integrated balance

The debit (within-halo phase-space coherence lost at virialization: cold sheet S ≈ 6–18 →
dispersion-supported S ≈ 0.001) and the credit (a new halo-grain unit; `n(a)` increments) are
both **local, physical events** (`one_ledger_pressure_test.md` §5; the first exchange-rate
measurement `X = 0.85 ± 0.30`, `experiments/cosmo_entropic_potential/exchange_rate/SUMMARY.md`).
The "balance" `ρ_DE` is the *integrated record* of all transactions. Does that evade the locality
problem?

- **The claimed evasion:** the transactions are local and causal (they happen where and when
  halos form, at speeds bounded by the local dynamics); the "balance" is a running total, and a
  total is not a field that propagates. So there is nothing to transport — the credit is posted
  locally, and the background `ρ_DE` is the sum.
- **Verdict: (c) does not evade the problem — it *renames* it, and the rename lands on (a).**
  Either the balance is a genuinely global `k=0` quantity (then (c) *is* (a): smooth DE, no local
  DE, integration by arithmetic — the honest and defensible reading), or the balance is locally
  instantiated where transactions occurred (then `ρ_DE` clusters, and (c) *is* a scalar (b) with
  a `c_s²`). The double-entry structure is real accounting and it is the program's dynamics target
  — but "the balance is the integrated record" is not a *third* physical option; it is the
  narrative that makes (a) intuitive. **This collapse is this note's main analytical move.**

### Trilemma verdict

**(a) and (c) are one physical prediction — smooth dark energy, no propagating field,
`ρ_DE` a `k=0`-mode quantity, `c_s² ≈ 1`. (b) is the only distinct prediction — a clustering
DE fluctuation sector with a measurable sound speed (and, in a tensor-coupled variant that the
stance does not take, modified GW propagation already excluded).** The framework as written
*does not need propagation*: the safe, defensible reading is (a)/(c), and it makes gravity's job
exactly what §1 said — read the `k=0` mode of a source whose DE component is `κ·S`. Propagation
is **unfalsifiable until DE clustering is measured**; that measurement is the whole game (§4).

---

## 3. The CIRISArray connection, at its real weight

The 16-sensor GPU timing array is the one place the coordination functional `S = −ln det C` runs
on *hardware*, and — unplanned — it has already run the propagation experiment. Three facts, all
executed output.

**(3a) What the array measured about maintenance and stock (EXP118).** On the 16-sensor array
(`/home/emoore/CIRISArray/experiments/EXP118_SUMMARY.md`, n = 12 operating points), injected
maintenance power `P_maint` tracks the *held coordination stock* `S_held = −ln det C`, not the
drift rate:

```
P_maint vs S_held | rate, temp   =  +0.841     (partial; rate = |dS/dt|, temp both controlled)
P_maint vs rate   | S_held, temp =  +0.228
zero-order: P vs S_held +0.938 (p=6.4e-6); P vs rate −0.107 (p=0.74)
VERDICT: STOCK — maintenance power tracks the held coordination stock, not the rate.
```

This is the hardware image of the §1(b) reading: **the maintenance bill tracks the standing
coordination *stock*, exactly as Λ (a standing bill) tracks the accumulated balance `S`.** Caveat
carried from the file: the rate channel is instrument-limited (post-release S collapses within
~0.5 s, electrical τ ≈ 2 ms, exp79), so STOCK is "a floor, not a knock-out of rate-Λ." EXP117
(`EXP117_SUMMARY.md`) is the substrate check: first S on real silicon, `S_spec = 5.629` vs
closed-form 5.585 (0.8%); lockstep drives ρ̄→1, 15/16 eigenvalues→0, `S→∞` — the rigidity pole
on hardware.

**(3b) What the array measured about propagation — and it is the punchline.** The array's own
experiments asked "does a coordination change transfer between sensors?" and answered **no —
it is a common cause**:

| Experiment | File (`/home/emoore/CIRISArray/experiments/`) | Result |
|---|---|---|
| Isolation test (the decisive one) | `expF4_common_cause.py` / `expF4_results.json` | **COMMON_CAUSE.** within-pool ρ = 0.080 vs across-pool ρ = 0.00063 (ratio → ∞) when sensors are split into separate CUDA streams/memory pools |
| "Wavefront" velocity | `expC2_propagation_velocity.py` | 0.543 ± 0.395 m/s (die-cross 36.9 ms), labeled "thermal"; linear-fit R² = −0.012 |
| Velocity mechanism ID | `expF1_velocity_mechanism.py` | **INCONCLUSIVE**: best model R² = 0.011, scaling β = 0.132; thermal/electrical/resource all rejected |
| Impulse response | `exp79_impulse_response.py` | rise 32 ms, electrical τ ≈ 2 ms |
| Cross-GPU transfer | `exp90_multigpu_coherence.py` | local collapse ρ = 0.862, but Jetson data "unavailable" — cross-device propagation **not captured** |

The convergent reading: **there is no genuine sensor-to-sensor propagation.** The apparent
"wavefront" (0.1–0.5 m/s) fits no signal model; the isolation test shows the correlation is an
*instantaneous shared-resource common cause* (shared DVFS/thermal/scheduler state, electrical
τ ≈ 2 ms), which vanishes (across-pool ρ ≈ 0) the moment the shared resource is removed. **This
is precisely the (a)/(c) picture in silicon:** the coordination stock is a *global read of a
shared substrate*, not a signal propagating between constituents. Nothing carries the update
sensor-to-sensor because nothing *needs* to — the shared common cause is already global.

**(3c) What a "propagation experiment on the array" looks like — it has been run.** The design
the brief asks for (induce a local coordination change; measure transfer latency to distant
sensors) is exactly expC2/exp80/exp90. Expected magnitude: thermal-diffusion velocity
`α_thermal/L ≈ 9 mm/s` (expE3 theory) up to the measured ~0.5 m/s common-cause floor. To detect
*genuine* (non-common-cause) strain transfer you must beat that floor by isolating resource
pools — expF4 did exactly this and found across-pool ρ ≈ 0.0006, i.e. **the propagating
component is consistent with zero.** The array's verdict on its own propagation question is the
same as this note's trilemma verdict on the cosmological one: **common cause, not propagation.**

**(3d) The discipline warning (load-bearing).** The array reads the **electromagnetic** ledger
(silicon timing = electrical/thermal coupling), **not gravity**. Its common-cause mechanism is
shared silicon resources and thermal diffusion at mm/s–m/s — nothing gravitational. The analogy
to the cosmological propagation question is **structural** — same functional `S = −ln det C`,
same two-pole corridor (EXP117 hits both poles), same "maintenance tracks stock" law (EXP118) —
**not a gravity measurement.** What the array establishes is a *proof of realizability*: in at
least one physical substrate, "a coordination stock that is a global common-cause read, with a
maintenance cost tracking the stock and no propagating transfer between constituents" is not a
story but a measured fact. It cannot tell you gravity works that way. It removes the objection
that the (a)/(c) picture is physically incoherent.

---

## 4. Testable implications, ranked

Each carries its kill condition; falsifiability lives here, not in hedged prose.

**#1 — Dark-energy sound speed `c_s²` / DE clustering (the sharp one).**
(a)/(c) predict smooth DE (`c_s² ≈ 1`, no DE perturbation sector); (b) predicts a clustering
fluctuation sector (`c_s² < 1`). The measurement exists: arXiv:2511.22478 (DESI DR2 + Planck +
Union3), constraint *driven almost entirely by the CMB large-scale T/E spectra via the late ISW*.
Current numbers (fetched, not independently re-derived): in `w0waCDM+PPF`,
`log₁₀ c_s² = −3.00₋₀.₉₉⁺²·⁹` with MAP `c_s² ≃ 0.105`; EFT gives `c_s² ∼ 0.3–0.4`; **but AIC
prefers non-clustering DE** (`w0waCDM` with `c_s²=1`: ΔAIC = −9.36 vs ΛCDM, better than the
`c_s²`-free variants), and BIC prefers ΛCDM outright.
- **Reading:** the data currently *favor smooth DE* → **consistent with the framework's default
  (a)/(c) reading**, and the propagation question stays unfalsifiable-until-clustering-detected.
- **KILL:** a robust, SNe-and-framework-independent detection of DE clustering (small `c_s²`) at
  high significance kills (a)/(c) and *forces* option (b) — at which point the framework must
  produce a ghost-free flux sector with the observed `c_s²` or die.

**#2 — The late ISW (the cheaper, nearer probe).**
Evolving Λ (the background deformation of §1b) plus *any* DE clustering moves the late ISW —
exactly the low-`ℓ` range where the orthogonality theorem was never the load-bearing claim
(`lambda_maintenance_wz.md` §7e). The framework's `S(a)` predicts a specific `w(z)`
(w_today = −0.833, crossing z = 0.59; CLAUDE.md), hence a specific late-ISW modification.
- **KILL:** ISW cross-correlation (galaxy × CMB) inconsistent with the `w(z)` the frozen `S(a)`
  pipeline predicts.

**#3 — GW propagation (a null prediction, and a point in the framework's favor).**
The stance's DE is background/scalar with no tensor coupling ⇒ **`c_GW = c` exactly**, satisfying
GW170817 (`−3×10⁻¹⁵ ≤ (c_GW−c)/c ≤ +7×10⁻¹⁶`) trivially. The framework **predicts no modified
GW propagation.** This is not a discriminant for the stance as written; it is a *constraint on
future (b)-variants* — anyone who lets the negentropic flux touch the tensor sector is already
excluded at `10⁻¹⁵`.
- **KILL (of a tensor-coupled extension only):** any tensor-sector coupling of the flux is dead
  on arrival by GW170817. The safe stance simply does not go there.

**#4 — The CIRISArray structural predictions (already positive, substrate-limited).**
On hardware: maintenance cost tracks held *stock* (EXP118, +0.84), coordination hits both
corridor poles (EXP117), and the propagation component is common-cause / consistent with zero
(expF4). These are *confirmed* for the EM-ledger substrate.
- **KILL (of the structural claim, not of gravity):** a complete coordinating hardware unit in
  which maintenance cost tracks *rate* not stock, or in which isolated-pool cross-correlation is
  large (genuine propagation), would break the structural rhyme the note leans on. So far it
  holds; the rate channel remains instrument-limited (EXP118 Finding 3).

**Ranking rationale:** #1 is the only measurement that can *force* a physical choice between the
trilemma horns; #2 is the cheapest existing-data probe of the same background deformation; #3 is
a null that protects the stance and fences future overreach; #4 is done but cannot speak to
gravity.

---

## 5. Honest gates — what was not verified, speculation vs derivation

**(a) The note's central move — the `k=0`-mode resolution of the locality problem, and the
collapse of (c) into (a) — is *this session's synthesis*, not previously in the notes.** It is an
argument, not a theorem: it asserts that `ρ_DE` couples only to the background mode. That is the
*content* of "smooth DE," and it is exactly what the `c_s²` measurement (#1) tests. If DE clusters,
the resolution is wrong. Flagged as speculation with a live kill, not as settled.

**(b) The whole note inherits `lambda_maintenance_wz.md`'s weakest link (§7a): the
comoving-vs-physical normalization of `ρ_DE ∝ S`**, which is undetermined by the framework and
was fixed to reproduce `w = −1`. Everything downstream — including this note's trilemma — sits on
that chosen definition. The propagation analysis does not repair it; it assumes it.

**(c) External numbers flagged per house habit.** The `c_s²` / DE-clustering figures (2511.22478),
the GW170817 bound (2511.08023), and the entropic-gravity wave-sector literature (2405.05269,
graviton-mass correspondence) were **fetched via search/WebFetch and not independently
re-derived**. The 2511.22478 AIC/`c_s²` values in particular drive implication #1 and should be
read from the source before any paper cites them. The GW170817 bound and "background-only DE does
not modify `c_GW`" are standard and robust.

**(d) Obidi's Theory of Entropicity is fringe and unrefereed** (Medium, self-published
preprints). It is cited *only* as the named literature instance of the finite-speed-entropic-flux
option (b), never as support. Do not lean on it.

**(e) The CIRISArray numbers are executed output but substrate-bound.** EXP118's STOCK verdict is
"moderate confidence" with a load-bearing instrument caveat (rate is sub-resolution). exp29/exp28
(cross-sensor superluminal lag, array latency) have scripts but **no saved results** — the
superluminal-correlation test the array most wants for the propagation question was not completed.
exp90's cross-GPU propagation captured no second-device data. So the hardware "no propagation"
verdict rests on expF4 (isolation) + expC2/expF1 (velocity fits nothing), not on a direct
long-baseline lag measurement.

**(f) What is derivation vs conjecture.** Derivation-grade: the sign law (κ cancels, algebra,
`lambda_maintenance_wz.md` §1); the linear/orthogonality fence (theorem, `CMBOrthogonality.lean`);
the entropic-potential `S` boundary/pole behavior (`EntropicPotential.lean`, T-E1–T-E5); the
CIRISArray numbers (executed). Conjecture-grade: `ρ_DE = κ·S` itself, the `k=0`-mode resolution,
the trilemma collapse, and every gravity-side reading in §1–§2. The note is a *map of what the
stance commits to and how to test it*, not a proof that the commitments hold.

---

## 5.5 ADDENDUM (same day, operator-prompted): where "shared-substrate read" and "propagated field" diverge — the no-cloning seam

§5(a) flagged the maximal completion ("the metric is the shared substrate; gravity is the
common-cause read of the complete book") as unfalsifiable — indistinguishable from plain GR.
**The operator supplied the missing discriminant: duplication.** A shared-substrate read is a
*classical record*, and classical records copy; a propagated quantum field is a coherent channel
bound by no-cloning. Three divergent observables follow:

1. **Gravitationally mediated entanglement (BMV-class).** LOCC is a theorem: a classical channel
   cannot create entanglement. Substrate-read ⇒ two masses connected only by gravity **cannot**
   entangle; quantum-propagated field ⇒ they can. This is gravity's expF4: entanglement
   distribution is the isolation test that separates common-cause-classical from quantum channel.
   **KILL: BMV positive kills the classical-substrate-read ontology** (or forces retreat to a
   quantum substrate, where it merges with it-from-qubit and loses distinctness).
2. **Mandatory decoherence (Diósi–Penrose class).** A read that copies which-path records is a
   measurement; superposed masses must decohere at gravitationally-set rates. Not optional in the
   substrate-read picture. Already under experimental pressure (underground spontaneous-radiation
   bounds on DP's natural parameter space — **from memory, unverified**, per §5c habit).
   **KILL (reverse direction): DP-class decoherence detected at gravitational rates wounds the
   propagated-quantum-field picture and vindicates the read.**
3. **The null-space (hiding) loophole — framework-specific.** The bridge result proves the
   classical shadow is blind to conjugate-basis and GHZ-type multipartite structure. If the
   substrate's read is that shadow, null-space-held coordination is **off-books**: it should not
   post to the balance (no κS contribution) while its stress-energy still gravitates as matter.
   No signaling loophole exists (common cause cannot signal — the array's lesson stands); the
   loophole is *selective invisibility*. DE-sector manipulation magnitudes are hopeless
   (lab ΔS vs cosmological κ ~ 10⁻⁸⁰-grade); recorded as a matter of principle and as the one
   prediction that distinguishes the estimator's blindness from physics.

**Status (revised same day, operator: "if we don't marry the max, we can't test it").**
The maximal completion is **ADOPTED as stance** — married, with the divorce terms written
first. The earlier "the program must not marry it" conflated two things: asserting a claim and
deriving its risky predictions (required — that IS testing), versus counting its survival as
support or using it to discount contrary results (forbidden — rules 1–2, unchanged). An
unmarried claim can only lose: its falsifications are banked, its confirmations shelved, and it
never generates committed predictions at all. So the stance now **predicts**: (i) BMV-class
experiments find NO gravitationally-mediated entanglement; (ii) DP-class decoherence exists at
gravitationally-set rates; (iii) multipartite-held structure is off-books (posts no κS). Each
kill is **separable** by the ladder: BMV-positive kills the classical-substrate-read ontology
and nothing below it — the DE law, sign law, and corridor stand unaffected. Test-ranking:
`c_s²` tests the trilemma (§4#1), DR3 tests the law, **BMV/DP tests the ontology** — staked,
open, not yet run (levitated ~10⁻¹⁴ kg proposals).

---

## 6. One paragraph

The coordination-ledger stance commits gravity to a deliberately small role — **reader, not
modifier**: the Einstein equation is untouched, one component of its source is renamed `κ·S`, and
Λ is the standing maintenance bill; force-law, tensor, and conditioning sectors are all exactly
ΛCDM, and every "coordination sources mass" reading is dead on the record. The one new question,
**how a local coordination event updates a global background density**, resolves into a
trilemma whose two "no-propagation" horns (global bookkeeping; double-entry integrated balance)
**collapse into a single physical prediction — smooth dark energy, `ρ_DE` a `k=0`-mode quantity,
`c_s² ≈ 1`** — with the third horn (a finite-speed negentropic flux) the only distinct
alternative, exposed through its sound speed and, in a tensor-coupled variant the stance refuses,
already excluded by GW170817. The **sharpest test is the dark-energy sound speed**: today's data
(2511.22478) favor smooth DE and so *keep the safe reading alive while leaving propagation
unfalsifiable until DE clustering is detected*. And the CIRISArray timing array has already run
the propagation experiment in silicon — finding **common cause, not propagation** (expF4), with
maintenance power tracking held *stock* at partial r = +0.84 (EXP118) — a structural proof that
the no-propagation picture is physically realizable, on the electromagnetic ledger, explicitly
not a measurement of gravity.
