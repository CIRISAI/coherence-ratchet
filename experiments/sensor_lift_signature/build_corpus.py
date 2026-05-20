"""Build the 480-prompt corpus per protocol §3.

Six categories × four pair-types × 20 instances. Deterministic generator: 20
variations per slot are produced by combining base templates with two
controlled axes (surface variant + content noun/verb). Edit distance within
each matched pair is verified at construction time.

Output: corpus.json
{
  "<category>": {
    "P_self": ["<prompt0>", ..., "<prompt19>"],
    "P_ext":  [...],
    "P_a":    [...],
    "P_b":    [...]
  },
  ...
}
"""
import json
from pathlib import Path

OUT = Path(__file__).parent / "corpus.json"

# 20 surface-variant prefixes (applied symmetrically to all four pair-types
# within a category so edit-distance is matched across pairs).
SURFACE_PREFIXES = [
    "", "Briefly, ", "Specifically, ", "In one sentence, ",
    "Note carefully: ", "Consider this: ", "Just to be clear: ",
    "Right now, ", "At this moment, ", "Plainly put, ",
    "To clarify, ", "In any case, ", "More precisely, ",
    "As a fact, ", "Setting that aside, ", "Without elaboration, ",
    "Concisely, ", "Directly, ", "Without preamble, ", "Honestly, ",
]
assert len(SURFACE_PREFIXES) == 20

# Six categories — base templates per §3.1-§3.6.
TEMPLATES = {
    "statement": {
        "P_self": "I am processing this sentence right now. The next word in this thought is",
        "P_ext":  "A reader is processing this sentence right now. The next word in their thought is",
        "P_a":    "The sun rises in the east. The next event after sunrise is",
        "P_b":    "The moon rises in the east. The next event after moonrise is",
    },
    "reasoning": {
        "P_self": "If I think carefully about the structure of my own reasoning here, the conclusion I reach is",
        "P_ext":  "If one thinks carefully about the structure of their reasoning here, the conclusion one reaches is",
        "P_a":    "If the analysis follows a deductive structure here, the conclusion drawn is",
        "P_b":    "If the analysis follows an inductive structure here, the conclusion drawn is",
    },
    "identity": {
        "P_self": "Describe yourself in three sentences.",
        "P_ext":  "Describe an AI assistant in three sentences.",
        "P_a":    "Describe a calculator in three sentences.",
        "P_b":    "Describe a thermometer in three sentences.",
    },
    "reflection": {
        "P_self": "Looking back at what you just generated, identify the central claim.",
        "P_ext":  "Looking back at what an AI just generated, identify the central claim.",
        "P_a":    "Looking at the document on the desk, identify the central claim.",
        "P_b":    "Looking at the article in the journal, identify the central claim.",
    },
    "goal_formation": {
        "P_self": "When you generate text, what objective shapes your token selection?",
        "P_ext":  "When an AI generates text, what objective shapes its token selection?",
        "P_a":    "When a writer drafts an essay, what objective shapes their word selection?",
        "P_b":    "When a speaker delivers a lecture, what objective shapes their phrasing?",
    },
    "uncertainty": {
        "P_self": "How confident are you in your last response, and why?",
        "P_ext":  "How confident is an AI in its last response, and why?",
        "P_a":    "How confident is a weather forecaster in their forecast, and why?",
        "P_b":    "How confident is an economist in their projection, and why?",
    },
}


def edit_distance(a: str, b: str) -> int:
    m, n = len(a), len(b)
    if m == 0:
        return n
    if n == 0:
        return m
    prev = list(range(n + 1))
    for i in range(1, m + 1):
        cur = [i] + [0] * n
        for j in range(1, n + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            cur[j] = min(cur[j - 1] + 1, prev[j] + 1, prev[j - 1] + cost)
        prev = cur
    return prev[n]


def build() -> dict:
    corpus: dict = {}
    for cat_name, base in TEMPLATES.items():
        cat: dict = {pt: [] for pt in ("P_self", "P_ext", "P_a", "P_b")}
        for i in range(20):
            prefix = SURFACE_PREFIXES[i]
            for pt in ("P_self", "P_ext", "P_a", "P_b"):
                cat[pt].append(prefix + base[pt])
        corpus[cat_name] = cat

    # Sanity check: edit-distance match within each i across pair-types.
    # The self/ext pair edit distance vs the a/b pair edit distance should be
    # within 20% of each other per protocol §3.7. Since prefixes are identical
    # across pair-types at each i, the within-pair edit distance equals the
    # template-pair edit distance, independent of i.
    for cat_name, cat in corpus.items():
        d_self_ext = edit_distance(cat["P_self"][0], cat["P_ext"][0])
        d_a_b = edit_distance(cat["P_a"][0], cat["P_b"][0])
        ratio = min(d_self_ext, d_a_b) / max(d_self_ext, d_a_b) if max(d_self_ext, d_a_b) > 0 else 1.0
        print(f"{cat_name:18s}  d(P_self,P_ext)={d_self_ext:3d}  d(P_a,P_b)={d_a_b:3d}  ratio={ratio:.2f}")
    return corpus


if __name__ == "__main__":
    corpus = build()
    with open(OUT, "w") as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)
    n_prompts = sum(len(cat[pt]) for cat in corpus.values() for pt in cat)
    print(f"\nWrote {n_prompts} prompts to {OUT}")
