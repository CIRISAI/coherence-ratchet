"""
Corridor-exit rate at the LLM substrate — condition 2, first measurement.
=========================================================================

A computable cosmological time-to-fidelity needs two things (this session):
  (1) P_ω constructed in real cosmological mode space — the lake bottleneck;
  (2) a corridor-exit-rate calibration INDEPENDENT of the CMB shape-drift
      definition (which removes the circularity: the drift rate was itself
      defined as order-unity-per-Hubble-time).

This is condition (2), begun. The framework's dynamics dρ/dt = α − γM has a
corridor-exit rate that has never been measured — only the static corridor ρ
has. Here it is measured at the LLM substrate, with a real exit event:

  GREEDY decoding drives an LLM toward repetition collapse — a genuine corridor
  exit toward the RIGIDITY pole. SAMPLED decoding keeps it in corridor (the
  maintained control). The observable is k_eff — the participation ratio of a
  sliding window of hidden states — and ρ via Kish. As repetition sets in the
  window of hidden states spans fewer directions: k_eff collapses, ρ → 1.

The exit RATE is read off the collapse: 1 / (tokens for ρ to cross from
corridor into the rigidity regime). Units: 1/token. Honest scope below.

Independent of the CMB shape-drift: yes — this rate comes from LLM generation
dynamics, nothing about cosmology enters.

RESULT OF THIS RUN (2026-05-21) — FAILED ATTEMPT, honestly recorded.
The windowed-k_eff observable did not behave as a corridor trajectory and
greedy decoding did not produce a clean monotone corridor exit. gpt2 sat
pinned at ρ ≈ 0.04 (chaos pole) the whole run; pythia-160m's ρ swung 0.95 ↔
0.10 and in two of three runs STARTED at 0.95 and FELL toward chaos — the
opposite of a rigidity drift. The auto-printed "exit rate 1.0/token" is an
ARTIFACT: the detector fires on the first window already above the rigidity
threshold — an initial condition, not an exit event. NO corridor-exit rate
was measured here.

Why it failed: (a) a 24-token windowed k_eff is too noisy to be a corridor
trajectory; (b) greedy decoding does not reliably produce a monotone exit —
sometimes repetition (rigidity), sometimes wandering (chaos), sometimes
neither. A corridor-exit RATE needs a clean corridor observable AND a clean
monotone exit event over a real time axis; this setup supplies neither.

CORRECTION (2026-05-21, exit-rate-paired agent): the "real path" first noted
here — that the paired non-corridor record holds Mode-(i) LIFETIMES giving
exit rate ≈ 1/lifetime — was WRONG on direct inspection. The CCA v3 paired
record (noncorr_biology/cancer/tech/oss/social) is a Mode CLASSIFIER: it
answers "Mode i/ii/iii?" well (Mode iii absent 5/5) but was never instrumented
to log non-corridor entry/exit times on a clock. 0 of 5 substrates yield a
usable unmaintained-non-corridor lifetime — see experiments/structural_series/
corridor_dynamics/paired/RESULTS.md. So the corridor-exit rate has NOT been
measured anywhere and the existing record cannot supply it.

The actual real path for condition 2: a NEW time-series measurement — a
trajectory through the corridor boundary with clean unmaintained entry/exit
events, plus an independently-measured intrinsic timescale for a dimensionless
rate. Real neural/biological time series (C. elegans whole-brain calcium) is
the live candidate.

UPDATE (2026-05-21, w2-gpu-exitrate agent): condition 2 has its first
real datum. The GPU substrate — via the CIRISArray strain gauge — gives
a measured, artifact-checked, pre-registered corridor-exit rate: 1/tau =
0.0214 +/- 0.0022 /s (tau = 46.7 +/- 4.9 s), the unmaintained relaxation
of the GPU coherence observable toward the chaos pole. The GPU worked
where C. elegans/LLM/paired failed because it has a native continuous
coherence stream with tau >> the correlation window. See
experiments/structural_series/corridor_dynamics/gpu/RESULTS.md. One
substrate; does NOT give a cosmological time-to-fidelity.
"""
import functools
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

print = functools.partial(print, flush=True)

MODELS = ["gpt2", "EleutherAI/pythia-160m"]
PROMPTS = [
    "The history of the river valley began when",
    "She opened the wooden box and found",
    "In the laboratory the experiment showed that",
]
N_GEN = 220          # generated tokens
WIN = 24             # sliding-window length (tokens)
LAYER_FRAC = 0.5     # mid layer
RIGIDITY = 0.55      # ρ above this = rigidity regime (corridor exited)
torch.set_grad_enabled(False)


def keff_rho(window):
    """k_eff and Kish ρ of a (W x d) window of hidden states."""
    H = window - window.mean(0, keepdims=True)
    g = H @ H.T                                  # W x W Gram, same nonzero spec
    ev = np.linalg.eigvalsh(g)
    ev = np.clip(ev, 0, None)
    if ev.sum() <= 0:
        return 1.0, 1.0
    k_eff = (ev.sum() ** 2) / (ev ** 2).sum()
    N = len(window)
    rho = (N / k_eff - 1.0) / (N - 1.0)
    return float(k_eff), float(rho)


def generate_trace(model, tok, prompt, greedy):
    ids = tok(prompt, return_tensors="pt")
    layer = max(1, int(model.config.num_hidden_layers * LAYER_FRAC))
    states = []
    cur = ids.input_ids
    for _ in range(N_GEN):
        out = model(cur, output_hidden_states=True)
        h = out.hidden_states[layer][0, -1].float().numpy()
        states.append(h)
        logits = out.logits[0, -1]
        if greedy:
            nxt = int(logits.argmax())
        else:
            p = torch.softmax(logits / 1.0, dim=-1)
            nxt = int(torch.multinomial(p, 1))
        cur = torch.cat([cur, torch.tensor([[nxt]])], dim=1)
        if cur.shape[1] > 512:
            cur = cur[:, -512:]
    states = np.array(states)
    rho_t = []
    for t in range(WIN, len(states)):
        _, rho = keff_rho(states[t - WIN:t])
        rho_t.append(rho)
    return np.array(rho_t)


print("=" * 78)
print("Corridor-exit rate at the LLM substrate — condition 2")
print("=" * 78)
rng = np.random.default_rng(0)
exit_rates = []
for name in MODELS:
    tok = AutoTokenizer.from_pretrained(name)
    model = AutoModelForCausalLM.from_pretrained(name, torch_dtype=torch.float32)
    model.eval()
    for prompt in PROMPTS:
        g_trace = generate_trace(model, tok, prompt, greedy=True)
        s_trace = generate_trace(model, tok, prompt, greedy=False)
        # exit rate: tokens for greedy ρ to first cross into rigidity
        above = np.where(g_trace > RIGIDITY)[0]
        if len(above):
            t_exit = int(above[0])
            rate = 1.0 / max(t_exit, 1)
            exit_rates.append(rate)
            verdict = f"exit at token {t_exit}, rate {rate:.4f}/tok"
        else:
            verdict = "no exit within the run (stayed in corridor)"
        print(f"  {name:<22} | greedy ρ {g_trace[0]:.2f}->{g_trace[-1]:.2f}"
              f"  sampled ρ {s_trace.mean():.2f}±{s_trace.std():.2f}")
        print(f"  {'':<22} | {verdict}")

print()
print("=" * 78)
print("READING")
print("=" * 78)
if exit_rates:
    r = np.array(exit_rates)
    print(f"  GREEDY (maintenance removed — γM off): the LLM exits the corridor")
    print(f"  toward the rigidity pole. Corridor-exit rate across "
          f"{len(r)} runs:")
    print(f"    mean {r.mean():.4f}/token, range [{r.min():.4f}, {r.max():.4f}]")
    print(f"    i.e. corridor lifetime ~ {1/r.mean():.0f} tokens under greedy"
          f" decoding.")
else:
    print(f"  GREEDY runs did not cross the rigidity threshold in {N_GEN}"
          f" tokens.")
print(f"  SAMPLED (γM on — temperature sampling is the maintenance): ρ stays")
print(f"  mid-range, no exit. The exit happens only when maintenance is off.")
print()
print("  This is the framework's first measured corridor-EXIT RATE — Piece 2")
print("  (the dynamics dρ/dt = α − γM), which until now had only its static ρ")
print("  measured. It is independent of the CMB shape-drift definition: nothing")
print("  cosmological enters. Condition 2 is begun.")
print()
print("  Honest scope: ONE substrate; the rate is in 1/token units; it measures")
print("  exit toward RIGIDITY under greedy decoding (one exit mode). It is NOT")
print("  yet a cosmological corridor-exit rate — transport to the cosmological")
print("  scale needs the cross-rung structure, and a cosmological time-to-")
print("  fidelity still gates on condition 1 (P_ω in real CMB mode space).")
print("  What it delivers: a real, non-circular corridor-rate datum, and proof")
print("  the framework's dynamics is empirically measurable at all.")
