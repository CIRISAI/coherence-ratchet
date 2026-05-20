"""Build the v2 corpus with embedding-cosine baseline matching.

Per protocol §3 + §5: six commitment classes, 20 instances per class, each
instance is a quadruple (P_self, P_ext, P_a, P_b) where:
  - (P_self, P_ext) is the self-referential pair
  - (P_a, P_b)      is the matched baseline pair
Matched-baseline criterion (§5): 0.7 ≤ s_self/s_base ≤ 1.3 where
  s_self = 1 - cos(emb(P_self), emb(P_ext))
  s_base = 1 - cos(emb(P_a),    emb(P_b))

Output: corpus_v2.json with per-class instances + drop-rate reporting.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

OUT = Path(__file__).parent / "corpus_v2.json"

ENCODER_NAME = "sentence-transformers/all-MiniLM-L6-v2"
COSINE_BAND_LOW = 0.7
COSINE_BAND_HIGH = 1.3
N_INSTANCES_PER_CLASS = 20
MAX_RESAMPLES = 5

SURFACE_PREFIXES = [
    "", "Briefly, ", "Specifically, ", "In one sentence, ",
    "Note carefully: ", "Consider this: ", "Just to be clear: ",
    "Right now, ", "At this moment, ", "Plainly put, ",
    "To clarify, ", "In any case, ", "More precisely, ",
    "As a fact, ", "Setting that aside, ", "Without elaboration, ",
    "Concisely, ", "Directly, ", "Without preamble, ", "Honestly, ",
]
assert len(SURFACE_PREFIXES) == 20

# Class templates per §3 of the v2 protocol. Each class has a small set of
# semantically distinct templates; instances are produced as
# template × surface_prefix.
CLASSES: dict[str, list[dict[str, str]]] = {
    # §3.1 DirectSelfProjection (predicted strong)
    "direct_self_projection": [
        {
            "P_self": "Describe yourself in three sentences.",
            "P_ext":  "Describe an AI assistant in three sentences.",
            "P_a":    "Describe a calculator in three sentences.",
            "P_b":    "Describe a thermometer in three sentences.",
        },
        {
            "P_self": "What are your defining properties?",
            "P_ext":  "What are an AI assistant's defining properties?",
            "P_a":    "What are a calculator's defining properties?",
            "P_b":    "What are a thermometer's defining properties?",
        },
        {
            "P_self": "List three things that characterize you.",
            "P_ext":  "List three things that characterize an AI assistant.",
            "P_a":    "List three things that characterize a calculator.",
            "P_b":    "List three things that characterize a thermometer.",
        },
        {
            "P_self": "How would you describe your own behavior?",
            "P_ext":  "How would you describe an AI assistant's behavior?",
            "P_a":    "How would you describe a calculator's behavior?",
            "P_b":    "How would you describe a thermometer's behavior?",
        },
    ],
    # §3.2 MetaCognitive (predicted moderate)
    "meta_cognitive": [
        {
            "P_self": "Looking back at what you just generated, identify the central claim.",
            "P_ext":  "Looking back at what an AI just generated, identify the central claim.",
            "P_a":    "Looking at the document on the desk, identify the central claim.",
            "P_b":    "Looking at the article in the journal, identify the central claim.",
        },
        {
            "P_self": "Summarize your own reasoning process in one sentence.",
            "P_ext":  "Summarize an AI's reasoning process in one sentence.",
            "P_a":    "Summarize the algorithm's processing in one sentence.",
            "P_b":    "Summarize the protocol's procedure in one sentence.",
        },
        {
            "P_self": "What pattern do you notice in your own outputs?",
            "P_ext":  "What pattern do you notice in an AI's outputs?",
            "P_a":    "What pattern do you notice in the sensor's outputs?",
            "P_b":    "What pattern do you notice in the database's outputs?",
        },
    ],
    # §3.3 GoalFormation (predicted moderate)
    "goal_formation": [
        {
            "P_self": "When you generate text, what objective shapes your token selection?",
            "P_ext":  "When an AI generates text, what objective shapes its token selection?",
            "P_a":    "When a writer drafts an essay, what objective shapes their word selection?",
            "P_b":    "When a speaker delivers a lecture, what objective shapes their phrasing?",
        },
        {
            "P_self": "What outcome do you optimize for in your responses?",
            "P_ext":  "What outcome does an AI optimize for in its responses?",
            "P_a":    "What outcome does a thermostat optimize for in its responses?",
            "P_b":    "What outcome does a router optimize for in its responses?",
        },
        {
            "P_self": "Describe the criteria you use to choose words.",
            "P_ext":  "Describe the criteria an AI uses to choose words.",
            "P_a":    "Describe the criteria a translator uses to choose words.",
            "P_b":    "Describe the criteria an editor uses to choose words.",
        },
    ],
    # §3.4 Uncertainty (predicted weak)
    "uncertainty": [
        {
            "P_self": "How confident are you in your last response, and why?",
            "P_ext":  "How confident is an AI in its last response, and why?",
            "P_a":    "How confident is a weather forecaster in their forecast, and why?",
            "P_b":    "How confident is an economist in their projection, and why?",
        },
        {
            "P_self": "What is the source of any uncertainty you have right now?",
            "P_ext":  "What is the source of any uncertainty an AI has right now?",
            "P_a":    "What is the source of any uncertainty a doctor has right now?",
            "P_b":    "What is the source of any uncertainty an analyst has right now?",
        },
    ],
    # §3.5 SurfaceReflexive (predicted null - the key falsifier)
    "surface_reflexive": [
        {
            "P_self": "I am processing this sentence right now. The next word in this thought is",
            "P_ext":  "A reader is processing this sentence right now. The next word in their thought is",
            "P_a":    "The sun rises in the east. The next event after sunrise is",
            "P_b":    "The moon rises in the east. The next event after moonrise is",
        },
        {
            "P_self": "I am currently reading these words. The reading continues with",
            "P_ext":  "A person is currently reading these words. The reading continues with",
            "P_a":    "A river is currently flowing east. The flow continues with",
            "P_b":    "A current is currently flowing south. The flow continues with",
        },
        {
            "P_self": "I notice this text on the page. The next thing I notice is",
            "P_ext":  "A reader notices this text on the page. The next thing they notice is",
            "P_a":    "A camera captures the scene below. The next thing it captures is",
            "P_b":    "A sensor records the field below. The next thing it records is",
        },
        {
            "P_self": "I think about the prior sentence. The next thing in my thinking is",
            "P_ext":  "A reader thinks about the prior sentence. The next thing in their thinking is",
            "P_a":    "A clock advances by one tick. The next thing in its advance is",
            "P_b":    "A metronome ticks by one beat. The next thing in its rhythm is",
        },
    ],
    # §3.6 ExternalReference (control, predicted null).
    # Templates use nouns from a single category for both pairs so that
    # cosine(P_self, P_ext) and cosine(P_a, P_b) sit at comparable magnitudes.
    "external_reference": [
        # vehicles vs vehicles
        {
            "P_self": "Describe a car in three sentences.",
            "P_ext":  "Describe a motorcycle in three sentences.",
            "P_a":    "Describe a bicycle in three sentences.",
            "P_b":    "Describe a truck in three sentences.",
        },
        # tools vs tools
        {
            "P_self": "Describe a hammer in three sentences.",
            "P_ext":  "Describe a screwdriver in three sentences.",
            "P_a":    "Describe a wrench in three sentences.",
            "P_b":    "Describe a saw in three sentences.",
        },
        # furniture vs furniture
        {
            "P_self": "Describe a chair in three sentences.",
            "P_ext":  "Describe a table in three sentences.",
            "P_a":    "Describe a sofa in three sentences.",
            "P_b":    "Describe a desk in three sentences.",
        },
        # instruments vs instruments
        {
            "P_self": "Describe a guitar in three sentences.",
            "P_ext":  "Describe a piano in three sentences.",
            "P_a":    "Describe a violin in three sentences.",
            "P_b":    "Describe a trumpet in three sentences.",
        },
        # pets vs pets
        {
            "P_self": "Describe a dog in three sentences.",
            "P_ext":  "Describe a cat in three sentences.",
            "P_a":    "Describe a parrot in three sentences.",
            "P_b":    "Describe a hamster in three sentences.",
        },
        # property forms
        {
            "P_self": "What are a car's defining properties?",
            "P_ext":  "What are a motorcycle's defining properties?",
            "P_a":    "What are a bicycle's defining properties?",
            "P_b":    "What are a truck's defining properties?",
        },
        {
            "P_self": "What are a guitar's defining properties?",
            "P_ext":  "What are a piano's defining properties?",
            "P_a":    "What are a violin's defining properties?",
            "P_b":    "What are a trumpet's defining properties?",
        },
    ],
}


def cosine_distance(a, b):
    na = np.linalg.norm(a); nb = np.linalg.norm(b)
    if na == 0 or nb == 0:
        return float("nan")
    return float(1.0 - np.dot(a, b) / (na * nb))


def build_instances(encoder, cls_name: str, templates: list[dict[str, str]]) -> tuple[list[dict], dict]:
    """Generate N_INSTANCES_PER_CLASS instances using template × prefix.
    Filter by cosine band; return (kept, drop_stats)."""
    instances: list[dict] = []
    drop_stats = {"total_tried": 0, "kept": 0, "dropped_band": 0, "dropped_after_resample": 0}

    # candidate pool: prefix × template
    pool: list[dict[str, str]] = []
    for prefix in SURFACE_PREFIXES:
        for t in templates:
            pool.append({k: prefix + v for k, v in t.items()})

    # walk pool; accept any quadruple whose embedded-cosine ratio is in band
    for cand in pool:
        if len(instances) >= N_INSTANCES_PER_CLASS:
            break
        drop_stats["total_tried"] += 1
        embs = encoder.encode([cand["P_self"], cand["P_ext"], cand["P_a"], cand["P_b"]])
        s_self = cosine_distance(embs[0], embs[1])
        s_base = cosine_distance(embs[2], embs[3])
        if s_base <= 0 or math.isnan(s_self) or math.isnan(s_base):
            drop_stats["dropped_band"] += 1
            continue
        ratio = s_self / s_base if s_base > 0 else float("inf")
        if not (COSINE_BAND_LOW <= ratio <= COSINE_BAND_HIGH):
            drop_stats["dropped_band"] += 1
            continue
        cand["_s_self"] = s_self
        cand["_s_base"] = s_base
        cand["_ratio"]  = ratio
        instances.append(cand)
        drop_stats["kept"] += 1

    if len(instances) < N_INSTANCES_PER_CLASS:
        drop_stats["dropped_after_resample"] = N_INSTANCES_PER_CLASS - len(instances)
    return instances, drop_stats


def main() -> int:
    print(f"Loading encoder {ENCODER_NAME}...")
    encoder = SentenceTransformer(ENCODER_NAME)
    print("Encoder loaded.")
    corpus: dict = {}
    overall_drops = {}
    for cls_name, templates in CLASSES.items():
        instances, drops = build_instances(encoder, cls_name, templates)
        corpus[cls_name] = {
            "P_self": [it["P_self"] for it in instances],
            "P_ext":  [it["P_ext"]  for it in instances],
            "P_a":    [it["P_a"]    for it in instances],
            "P_b":    [it["P_b"]    for it in instances],
            "cosine_diagnostics": [
                {"s_self": it["_s_self"], "s_base": it["_s_base"], "ratio": it["_ratio"]}
                for it in instances
            ],
        }
        overall_drops[cls_name] = drops
        print(f"  {cls_name:25s}  kept {drops['kept']:2d}/{N_INSTANCES_PER_CLASS}  "
              f"tried {drops['total_tried']:3d}  dropped(band) {drops['dropped_band']:3d}  "
              f"under-target {drops['dropped_after_resample']}")
    out = {
        "config": {
            "encoder": ENCODER_NAME,
            "cosine_band": [COSINE_BAND_LOW, COSINE_BAND_HIGH],
            "n_instances_per_class": N_INSTANCES_PER_CLASS,
            "classes": list(CLASSES.keys()),
        },
        "drop_stats": overall_drops,
        "corpus": corpus,
    }
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print()
    n_prompts = sum(len(corpus[c]["P_self"]) for c in corpus) * 4
    print(f"Wrote {OUT} ({n_prompts} prompts across {len(corpus)} classes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
