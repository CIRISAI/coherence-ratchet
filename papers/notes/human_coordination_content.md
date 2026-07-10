# How much dark matter does a human produce? — coordination content, the map to mass, and why the honest answer is ~zero

**STATUS: L5+ SPECULATION, conditional on an UNPROVEN thesis.** Every claim below rides on the
"dark ledger" reframing (dark matter = the gap between gravity's demand and the visible-coordination
account), which is itself conjecture-to-speculation grade and, in its naive form, already **dead**
(`dm_coherence_priorart.md`: killed on magnitude by ~40 orders; `dm_phasespace_grain.md`: direction
revived only as a merger-geometry-bound, CDM-circular shadow). This note treats the operator's
question — *how much dark matter does a human/humanity produce?* — as a **stress-test / possible
reductio** of the thesis, not as a number to manufacture. The result (~zero) is reported as itself
the finding.

**Date 2026-07-10. Companion to** `formal/CoherenceRatchet/LedgerLaw.lean` (the law + the three
blindnesses), `dm_coherence_priorart.md` (the ε problem and the magnitude death),
`dm_phasespace_grain.md` (grain discipline). Executed arithmetic:
`experiments/dm_coherence/human/human_dm_estimate.py` (deterministic; every number below is script
output).

**Three layers, kept strictly separate.** Layer 1 is honest information theory (coordination content
in nats) and stands **regardless of the gravity thesis**. Layer 2 maps nats to mass and shows both
candidate maps give ~0 for a human. Layer 3 is what that ~0 does to the thesis. Do not let them bleed.

---

## Layer 1 — coordination CONTENT S (nats). Real, computable, no gravity.

S is the relative entropy of a system's fluctuation structure from independence (multi-information;
in the Gaussian/pairwise shadow the ledger commits to, `S = −ln det C`, a proved theorem —
`LedgerLaw` clauses 1–2). It is a **pure information quantity**: no length, mass, or energy scale.
This layer asks only: how many nats of coordination does a human, and humanity, hold?

**The governing discipline is the repo's own k_eff-saturation result.** Effective dimensionality is
**bounded** — low-rank saturation on *complete* units, decisive even at the whole larval-zebrafish
brain (β≈0; `experiments/keff_saturation/NEW_DIRECTIONS.md`). Coordination content is set by
**effective (bounded) modes and maintenance, NOT raw part count.** So a brain's S is fixed by the
tens-to-hundreds of coherent modes its dynamics actually occupy — a neural manifold of
O(10–100) dimensions — **not** by its 8.6×10¹⁰ neurons, and emphatically not by its ~10²⁷ atoms.
Counting a nat per part is the exact error clause 3 forbids (the same "one nat per baryon" mistake
that inflated the galactic estimate to 10⁶⁸ nats before it was retired in `dm_coherence_priorart.md`).

### Single human — S by grain (grain stated; ranges)

| Grain | S (nats) | Note |
|---|---|---|
| **Brain, effective neural manifold** — k_eff ~ 10–100 coherent modes, ρ ~ 0.3–0.5 **(most defensible)** | **~10¹ – 10³** | The saturating grain. ~65 nats at k_eff=100, ρ=0.5. |
| Brain, resolution cells of the neural state — ~10⁶ cells at ρ~0.9 | ~10⁶ | Fine but defensible upper end of "held structure." |
| Lifetime information **throughput** envelope — ~10⁹ bit/s × ~2.5×10⁹ s | ~10¹⁸ | **FLUX, not held S.** Information *touched*, not coordination *held*. Upper envelope only — overcounts badly. |
| Molecular microstate count — ~10²⁷ atoms | ~10²⁷ | **REJECT.** Counts substrate/amplitude, not coordination shape (clause-3-illegitimate). |

**Human headline: S ~ 10¹–10³ nats** on the saturating grain (effective coherent modes), rising to
~10⁶–10⁹ only if you resolve the neural state finely, with a soft ~10¹⁸-nat ceiling if you (wrongly)
count lifetime throughput as held coordination. The defensible number is **tiny** — tens to
thousands of nats — precisely because k_eff saturates. This is the honest and slightly surprising
Layer-1 result: *the coordination content of a human is far below its neuron count.*

### Humanity — S by grain

| Grain | S (nats) | Note |
|---|---|---|
| **Effective institutional / linguistic modes** — k ~ 10³–10⁴ coordinating units (nation-states, major institutions, languages), ρ ~ 0.3 | **~10⁴ – 10⁸** | Civilization also saturates: the effective number of independent coordination poles is small. |
| 8×10⁹ humans × per-human effective S (~10²) | ~10¹² | If humans coordinate as effective units. |
| Stored-data envelope — ~10²³ bits (world data, 2026) | ≤ ~10²³ | **ENVELOPE.** Most stored data is redundant/compressible/independent — *not* coordination content. A ceiling, not S. |

**Humanity headline: S ~ 10⁴–10⁸ nats** of genuine coordination (effective modes), with a
stored-data ceiling of ≤~10²³ nats of which only a fraction is coordination. **Crucially, every nat
of it — brains, institutions, the internet, encrypted archives — is carried on baryonic substrate.**
Hold that fact; it is the whole story in Layer 2(ii).

*This layer is honest information theory and stands on its own. Nothing above touches gravity.*

---

## Layer 2 — the map to mass, and why it almost certainly fails.

Two candidate maps from S (nats) to ΔM (dark mass), both speculative.

### (i) The DEAD naive map: ΔM = εS/c²

One posits an energy-per-nat ε and reads coordination as gravitating mass-energy. The magnitude
sweep (script output), across every ε from the physically motivated Landauer floor to Planck:

| | ε = k_BT @ body (4.3×10⁻²¹ J/nat) | ε = m_e c² (8×10⁻¹⁴) | ε = Planck (2×10⁹) |
|---|---|---|---|
| **Human**, S = 10³ nats | **4.8×10⁻³⁵ kg** (10⁻⁵ eₘₐₛₛ) | 9×10⁻²⁸ kg | 2×10⁻⁵ kg |
| **Human**, S = 10¹⁸ (throughput) | 4.8×10⁻²⁰ kg | 9×10⁻¹³ kg | 2×10¹⁰ kg |
| **Humanity**, S = 10⁸ | 4.8×10⁻³⁰ kg | 9×10⁻²³ kg | 2 kg |
| **Humanity**, S = 10²³ (stored) | 4.8×10⁻¹⁵ kg | 9×10⁻⁸ kg | 2×10¹⁵ kg |

At the **physically motivated** ε (Landauer at body temperature — the actual thermodynamic cost of
maintaining a bit of order at 310 K), a human "produces" **~10⁻³⁵ to 10⁻²⁰ kg** of dark matter:
between ~10⁻⁵ electron masses and a fraction of a virus. A meaningless, unobservable number,
~10⁻³⁷ to 10⁻²² of the human's own mass.

Inverting: to make a human "produce" even its own 70 kg again in dark matter requires
ε ≈ 6×10¹⁵ J/nat at the defensible S (≈ **10³⁶ × Landauer, 10⁶ × Planck**) — flatly absurd. Only if
you inflate S to the throughput envelope (10¹⁸ nats, itself an overcount) does the required ε fall to
~6 J/nat, which is *sub*-Planckian but still **~10²¹ × the thermodynamic floor** — absurd on the only
yardstick (Landauer) that has physical meaning for the cost of holding a bit.

This is the **same reductio** that killed the galactic reading: there, S = coordination forced
ε ≈ 10³⁷–10⁴⁷ × Planck (`dm_coherence_priorart.md` §2). At human scale the identical squeeze plays
out. **Map (i) is DEAD**: it gives either ~0 (at natural ε) or an absurd ε (for any macroscopic ΔM).

### (ii) The GAP map: ΔM = G_demanded − G_visible — a human produces EXACTLY zero

The live reframing does not multiply S by an ε. It says dark matter is the **gap** between the
gravitational field a system demands (its G) and the field its *visible* (baryonic) census accounts
for. Now apply it to a human.

**A human is made of ordinary baryons whose gravity is fully accounted for by their rest mass.** The
field a human sources is set by the stress-energy tensor T_μν of those baryons. Every correlated
neural signal, every maintained bit of order, is **already energy inside those baryons** — kinetic,
binding, electromagnetic-field energy — and every joule of it is **already in the measured ~70 kg**
(rest mass includes all of it). There is no gravitational demand beyond what the visible baryonic
rest mass supplies:

```
   G_demanded(human)  =  G_visible(human)      ⇒     GAP  =  0.
```

**Under the gap reading, a human produces exactly ZERO dark matter.** Not because its coordination is
small — Layer 1 shows it is real, tens to thousands of nats — but because that coordination is
**carried by baryons already on the visible ledger and already fully counted in their rest-mass
gravity.** The same holds for humanity: institutions, the economy, the internet, encrypted archives,
even sealed quantum states all sit on baryonic hardware whose stress-energy is fully censused.
GAP ≈ 0.

**The mechanism, stated precisely (and it is clause 3).** Correlating vs. de-correlating the same
neurons changes the **copula** (S rises) but not the **total stress-energy** (the energy is the same
whether the parts fire together or independently). An entangled/coordinated state and a product state
of the *same energy* gravitate identically. S is a functional of shape (amplitude-blind, clause 3, a
proved theorem); gravity couples to stress-energy, which **is** the amplitude. So the pattern that
adds S carries no extra T_μν → no extra gravity → **no gap**. Coordination-as-pattern is
gravitationally inert by the very theorem that makes S a clean coordination detector.

**What WOULD produce a gap?** Only stress-energy the visible baryon census misses — i.e. coordination
whose **carrier is off the visible ledger** (order-≥3 correlations among dark-sector particles; a
dark-sector condensate). But even there, what gravitates is the *carrier's* stress-energy, not the
coordination; the coordination is epiphenomenal to the gravity. **Is any human activity such a
carrier?** Almost certainly not. Even a quantum computer's entanglement — genuine order-≥3
coordination, invisible to pairwise S (the LedgerLaw "known hole") — is carried by baryonic qubits on
the visible ledger and adds no stress-energy beyond them. Encryption, the internet, sealed states: all
baryonic. **No sense survives in which human activity creates non-baryon-carried coordination.**

**Layer-2 verdict: a human produces ~0 dark matter under both maps.** Map (i): ~0 at natural ε, absurd
ε for anything more. Map (ii): *exactly* 0, for a principled reason — human coordination is
baryon-carried, hence already on the visible ledger. **The ~0 is the answer, and map (ii)'s ~0 is the
sharp, informative one.**

---

## Layer 3 — what the exercise reveals: CARRIER vs. PATTERN.

The two maps giving ~0 for the cleanest possible case — a system of maximally rich coordination
(a human, a civilization) built entirely on fully-visible carriers — is not a null result. It is a
**sharp constraint on what the dark-ledger thesis can mean.**

**"Hidden coordination" cannot mean "any coordination invisible to a particular instrument."** If it
did, a human — dense with coordination invisible to a naive baryon-mass census — would produce dark
matter. It produces none. So the thesis's "hidden coordination" must mean something narrower:
**coordination whose CARRIER is off the visible (baryonic) ledger.** The human calculation forces this
distinction, and the distinction has teeth:

- **If hidden coordination requires a hidden CARRIER** → the thesis is **particle dark matter with
  extra steps.** What gravitates is the dark carrier's stress-energy; the "coordination" story adds
  nothing gravitational and is observationally redundant with CDM. This is exactly the circularity
  the Bullet-Cluster notes kept hitting — "dark mass sits with the collisionless component" *is* the
  definition of CDM (`reversal_adversarial_audit.md` Attack 4; `dm_phasespace_grain.md` §4).

- **If pattern-level hidden coordination could gravitate on its own** (order-≥3 correlations among
  *visible* baryons, carrying no extra stress-energy) → this is the **only** version in which humans
  could produce dark matter. But clause 3 forbids it: **S is amplitude/pattern-blind while gravity
  sees stress-energy, which is the amplitude.** Pattern alone carries no stress-energy; no
  stress-energy, no gravity. Pure-pattern coordination is gravitationally inert. Humans produce zero.

**The cleanest statement of what the thesis can and cannot mean:**

> **Stress-energy is amplitude; S is pattern; the two are ORTHOGONAL by clause 3
> (`copula_blindness`, a proved theorem). Gravity couples to stress-energy, not to pattern. Therefore
> coordination-as-pattern cannot gravitate on its own — only coordination whose carrier contributes
> stress-energy gravitates, and that stress-energy is on the visible ledger whenever the carrier is
> baryonic. "Hidden coordination" gravitates only if it has a hidden carrier — at which point it is
> particle dark matter, and "coordination" is a re-description, not a mechanism.**

S sees exactly what gravity cannot (pure shape) and gravity sees exactly what S cannot (stress-energy
magnitude). The dark-ledger thesis's hope was that these coincide — that hidden coordination *is*
dark mass. The human calculation shows, via a proved theorem, that they are **orthogonal.** A human is
the ideal probe of this because it is the extreme case: maximal coordination richness, zero
gravitational gap. The gap is zero *because* the richness is all pattern on visible carriers.

---

## Bottom line

**How much dark matter does a human produce? ~Zero — and that answer is the interesting finding.**

- **Layer 1 (real, no gravity):** coordination content S ≈ **10¹–10³ nats** for a human (effective
  neural modes; up to ~10⁶–10⁹ on a fine grain), and ≈ **10⁴–10⁸ nats** for humanity (effective
  institutional modes; ≤~10²³ as a stored-data ceiling). Bounded far below part count, because k_eff
  saturates. All of it baryon-carried.

- **Layer 2 (the map to mass):** the naive map ΔM = εS/c² gives **~10⁻³⁵–10⁻²⁰ kg** for a human at
  physically motivated ε — meaningless — and needs an ε ~20–40 orders past any physical scale to give
  anything macroscopic (the galactic reductio, repeated). The gap map gives **exactly 0**, for the
  principled reason that human coordination is baryon-carried and baryon stress-energy is fully on the
  visible ledger.

- **Layer 3 (what it teaches):** the forced ~0 sharpens the thesis to a single fork. "Hidden
  coordination" gravitates **only** if its carrier is off the visible ledger — which makes the thesis
  particle dark matter in disguise — because pure pattern (S) is orthogonal to stress-energy (gravity)
  by clause 3. There is no third option in which a human's rich, visible-baryon-carried coordination
  produces dark mass. The exercise is thus a clean **reductio of the pattern-gravitates reading** and a
  **sharpening (into near-redundancy with CDM) of the hidden-carrier reading.** Either way, humans and
  humanity produce ~zero dark matter, and *why* is the cleanest available statement of what the dark
  ledger can and cannot claim: it is a ledger of carriers, not of patterns.
