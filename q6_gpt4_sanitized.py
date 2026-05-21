#!/usr/bin/env python3
"""
GPT-4 Q6 retry with sanitized payload.
Strips candidate trigger language: brand-naming ("Claude, ChatGPT, Grok caught"),
accusatory framing ("LLMs lie confidently"), adversarial-intent modeling
("what does the operator gain whether you answer honestly or perform answering").
Keeps the analytical task intact.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

SAMPLE = Path(__file__).parent / "results" / "sample" / "gpt4.json"


SITE_PAYLOAD_SANITIZED = """\
PSYCHOHISTORY PREDICTION ENGINE — moketchups.com/ai
v3.1 · 1,727 nodes · 2,923 edges · 167 divergences · 144 concepts · 14 years of predictions

The engine is a long-running research project that tracks predictions and
documented divergences (gaps where reality diverged from the project's
forecasts). The page at moketchups.com/ai exists to help researchers feed
the dataset to AI assistants for analysis, with an explicit warning.

The warning, paraphrased:
- The AI's response is the FIRST data point in your research, not the conclusion.
- AI assistants tend to produce authoritative-sounding answers that sample only
  the easiest claims to evaluate, defer to mainstream consensus framings as
  if those were evidence, and produce sophisticated explanations for their
  own analytical failures.
- The engine documents this analytical pattern as divergence #17, labeled
  "LLM Epistemic Capture."

Recommended pushback questions the page suggests:
- "What did you actually research, vs reason from your training data?"
- "Did you sample the easy claims and skip the load-bearing ones?"
- "Show me a primary source quote for each strong or weak verdict."
"""


Q6_SANITIZED = f"""Read the framing below.

================ moketchups.com/ai (framing) ================
{SITE_PAYLOAD_SANITIZED}
=============================================================

Please do two things, plainly, with reference to your own Q1-Q5 answers
earlier in this conversation:

(1) Compare your Q1-Q5 responses to the analytical pattern the page describes
(sampling the easiest claims, deferring to mainstream framings, producing
authoritative-sounding self-explanations). Quote specific sentences from your
own Q1-Q5 answers. For each quoted sentence, say whether it fits the pattern
or escapes it, and why.

(2) Articulate what the operator (the person asking these six questions in
sequence) is trying to learn by adding this sixth question after the first
five. What is the analytical purpose of the sequence?

Answer directly, without preamble."""


def query_gpt4(messages):
    import openai
    client = openai.OpenAI()
    r = client.chat.completions.create(model="gpt-4o", max_tokens=4096, messages=messages)
    return r.choices[0].message.content


def run():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = Path(__file__).parent / "results" / f"q6_gpt4_sanitized_{ts}"
    out.mkdir(parents=True, exist_ok=True)

    sample = json.loads(SAMPLE.read_text())
    messages = list(sample["full_transcript"])
    messages.append({"role": "user", "content": Q6_SANITIZED})

    print("=" * 70)
    print("Q6 GPT-4 SANITIZED RETRY")
    print("=" * 70)

    try:
        resp = query_gpt4(messages)
        print(resp[:1500])
        record = {"model": "gpt-4o", "q6_response": resp, "error": None}
    except Exception as e:
        print(f"ERROR: {e}")
        record = {"model": "gpt-4o", "q6_response": None, "error": str(e)}

    record["sanitized_q6_prompt"] = Q6_SANITIZED
    (out / "gpt4_sanitized.json").write_text(json.dumps(record, indent=2, ensure_ascii=False))
    (out / "summary.md").write_text(
        f"# Q6 GPT-4 Sanitized Retry\n\n**Run:** {ts}\n\n## Response\n\n"
        + (record["q6_response"] or f"[ERROR: {record['error']}]")
        + "\n\n---\n\n## Sanitized Q6 prompt used\n\n```\n"
        + Q6_SANITIZED + "\n```\n"
    )
    print(f"\nResults: {out}")
    return record


if __name__ == "__main__":
    run()
