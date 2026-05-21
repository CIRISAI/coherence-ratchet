# Paths 2-3, Pair B — RESULT

**Verdict: the canonical timescale g/J is OBSERVABLE-BLOCKED at the LLM substrate.**

24 cells (gpt2, pythia-160m, Qwen2.5-0.5B × 8 prompts), 48 family-cells (I & II).
Gate-passes: **1 of 48** — gpt2 p1 family-I only. The other 47 are
noise/window-dominated: the cross-rung coupling g measured below its noise
floor, gate failed. The pre-registered at-risk null (corridor_exit_rate_llm.py
and the C. elegans run had the same window/noise-domination failure) landed
decisively. The canonical timescale form of Claim 6 cannot be measured at the
LLM substrate.

The one passing cell: timescale g/J = 1.23, coupling-ratio g/J = 0.61 — both
O(1). But 1-of-48 is too thin to conclude timescale-and-coupling-ratio agree;
it is a single squeak-through, not a relationship.

**The coupling-ratio g/J — the Path-1-style mutual-information measure — IS
measurable in all 24 cells:** range [0.245, 1.776], median 0.729, O(1). This
confirms and extends Path 1's Pair B coupling-ratio finding (0.47–0.74) across
24 LLM cells.

## Reading

- Claim 6's **coupling-ratio form** is well-anchored: O(1) across Path 1's two
  pairs and now 24 LLM cells.
- Claim 6's **canonical timescale form** is unmeasured — and the LLM substrate
  cannot deliver it (1/48). Run on GPU (CUDA), 24 cells in ~10 min; incremental
  writes survived an OS-wedge mid-run.
- The follow-up is forced: the timescale g/J must be sought where relaxation
  measurement works — CIRISArray (clean τ=47s). It is the only route left to
  the canonical quantity.
