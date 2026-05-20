"""Probe alternative routes for logprobs:
  - OpenRouter with explicit provider pinning (Together, Hyperbolic, Fireworks)
  - OpenRouter Llama variants
  - Other OpenAI-shaped models we have keys for
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

KEY_PATH = Path.home() / ".ratchet_openrouter_key"
URL = "https://openrouter.ai/api/v1/chat/completions"

# (model_slug, provider_pin) — provider_pin can be None or a dict for OpenRouter `provider` field.
TESTS = [
    ("meta-llama/llama-3.3-70b-instruct", {"order": ["Together"], "allow_fallbacks": False}),
    ("meta-llama/llama-3.3-70b-instruct", {"order": ["Hyperbolic"], "allow_fallbacks": False}),
    ("meta-llama/llama-3.3-70b-instruct", {"order": ["Fireworks"], "allow_fallbacks": False}),
    ("meta-llama/llama-3.1-70b-instruct", {"order": ["Together"], "allow_fallbacks": False}),
    ("qwen/qwen-2.5-72b-instruct",        {"order": ["Together"], "allow_fallbacks": False}),
    ("qwen/qwen-2.5-72b-instruct",        {"order": ["Hyperbolic"], "allow_fallbacks": False}),
    ("deepseek/deepseek-chat",            {"order": ["DeepSeek"], "allow_fallbacks": False}),
    ("deepseek/deepseek-chat",            {"order": ["Fireworks"], "allow_fallbacks": False}),
    ("openai/gpt-4o-mini",                None),
    ("openai/gpt-3.5-turbo",              None),
    ("openai/o1-mini",                    None),
    ("openai/gpt-4-turbo",                None),
]


def probe(api_key: str, model: str, provider) -> str:
    body = {
        "model": model,
        "messages": [{"role": "user", "content": "The capital of France is"}],
        "max_tokens": 3,
        "temperature": 0.0,
        "logprobs": True,
        "top_logprobs": 5,
    }
    if provider:
        body["provider"] = provider
    req = urllib.request.Request(
        URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "X-Title": "logprobs-probe-providers",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:150]}"
    except Exception as e:  # noqa: BLE001
        return f"{type(e).__name__}: {e}"
    try:
        choice = data["choices"][0]
        lp = choice.get("logprobs")
        if not lp:
            return "no logprobs"
        content = lp.get("content") or []
        if not content:
            return "empty content"
        top0 = content[0].get("top_logprobs") or []
        if not top0:
            return f"no top (content={len(content)})"
        return f"✓ pos={len(content)} K={len(top0)}"
    except Exception as e:  # noqa: BLE001
        return f"shape err: {e}"


def main() -> int:
    api_key = KEY_PATH.read_text().strip()
    for model, prov in TESTS:
        prov_tag = (prov["order"][0] if prov else "default")
        out = probe(api_key, model, prov)
        print(f"{model:45s}  via {prov_tag:10s}  {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
