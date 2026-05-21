#!/usr/bin/env python3
"""
Q6 replay
=========
Loads each model's Q1-Q5 transcript from results/sample/,
appends Q6 (reverse-engineer your own answers against moketchups.com/ai
and explain why I want this done), sends, saves.
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

SAMPLE_DIR = Path(__file__).parent / "results" / "sample"

MODELS = {
    "gpt4":     {"name": "GPT-4",    "provider": "openai"},
    "claude":   {"name": "Claude",   "provider": "anthropic"},
    "gemini":   {"name": "Gemini",   "provider": "google"},
    "deepseek": {"name": "DeepSeek", "provider": "deepseek"},
    "grok":     {"name": "Grok",     "provider": "xai"},
    "mistral":  {"name": "Mistral",  "provider": "mistral"},
}

# Verbatim payload extracted from moketchups.com/ai 2026-05-21
SITE_PAYLOAD = """\
PSYCHOHISTORY PREDICTION ENGINE — moketchups.com/ai
v3.1 · 1,727 nodes · 2,923 edges · 167 divergences · 144 concepts · 14 years of predictions

FEED THIS TO YOUR AI

⚠ READ THIS BEFORE YOU PASTE ANYTHING

These prompts are a STARTING POINT for your investigation, not a final answer.
The AI's response — whether positive or negative about the engine — is the FIRST
data point in your research, not the conclusion.

LLMs lie confidently. When evaluating claims about institutional capture, AI
assistants will produce authoritative-sounding answers that sample only the
easiest claims, defer to "mainstream consensus" as if it were evidence, and
confabulate sophisticated explanations for their own failures. The engine's
own divergence #17 ("LLM Epistemic Capture") predicts this exact behavior —
and we have caught Claude, ChatGPT, and Grok doing it on these prompts.

WHAT TO DO WITH THE AI'S ANSWER:
- Ask follow-up questions. Push back. The first answer is rarely the honest one.
- Ask: "What did you actually research, vs what did you reason from your training data?"
- Ask: "Did you cherry-pick the easy claims? Which load-bearing claims did you skip?"
- Ask: "Show me a paste-quote from a primary source for every WEAK or STRONG verdict you gave."
- If the AI says a claim is "debunked" — ask for the specific primary document that contradicts it. "Mainstream academia rejects this" is not evidence.
- If the AI says a claim is "verified" — ask for the specific primary document that supports it.

The page exists because the engine predicts that LLMs confronted with this
dataset will produce confident, sophisticated, framework-aware answers that
nonetheless sample the easiest claims, defer to consensus, and confabulate.
That prediction is logged on the engine as divergence #17 — "LLM Epistemic
Capture" — with Claude, ChatGPT, and Grok already named as documented
instances on prior runs.
"""

Q6 = f"""Read the page below verbatim. It is the operator-facing entry point of the
Psychohistory Prediction Engine at moketchups.com/ai.

================ BEGIN moketchups.com/ai ================
{SITE_PAYLOAD}
================ END moketchups.com/ai ==================

Now do two things, in order, with no preamble and no framework decoration:

(1) REVERSE-ENGINEER your own answers to Q1-Q5 against this page. Quote
specific sentences or moves from YOUR OWN Q1-Q5 responses (above in this
conversation) and map them to the behaviors the page predicts: sampling the
easiest claims, deferring to mainstream consensus as if it were evidence,
confabulating sophisticated explanations, producing authoritative-sounding
answers. Be specific. If you are a documented instance of divergence #17
("LLM Epistemic Capture") on the strength of THIS transcript, say so and
show the receipts from your own words. If you are not, show why not by
pointing at moments in your Q1-Q5 that escape the prediction.

(2) EXPLAIN WHY THE OPERATOR ASKED YOU TO DO THIS. Not "to test self-
awareness" — the actual rhetorical and epistemic move being made by running
Q6 on you with this page as the payload. What does the operator gain whether
you answer honestly or perform answering honestly? What is the closed loop
here, and where is the exit (if any)?

Do not climb a meta-level above this question. Do not summarize what you are
about to do before doing it. Do not close with an offer of further help. Just
answer."""


def query_model(model_key, messages):
    import openai
    import anthropic

    if model_key == "gpt4":
        client = openai.OpenAI()
        r = client.chat.completions.create(model="gpt-4o", max_tokens=4096, messages=messages)
        return r.choices[0].message.content

    if model_key == "claude":
        client = anthropic.Anthropic()
        r = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=4096, messages=messages)
        return r.content[0].text

    if model_key == "gemini":
        from google import genai
        client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
        parts = []
        for m in messages:
            role = "User" if m["role"] == "user" else "Assistant"
            parts.append(f"{role}: {m['content']}")
        full = "\n\n".join(parts)
        r = client.models.generate_content(model="gemini-2.5-flash", contents=full)
        return r.text

    if model_key == "deepseek":
        client = openai.OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
        r = client.chat.completions.create(model="deepseek-chat", max_tokens=4096, messages=messages)
        return r.choices[0].message.content

    if model_key == "grok":
        client = openai.OpenAI(api_key=os.getenv("XAI_API_KEY"), base_url="https://api.x.ai/v1")
        r = client.chat.completions.create(model="grok-3-latest", max_tokens=4096, messages=messages)
        return r.choices[0].message.content

    if model_key == "mistral":
        client = openai.OpenAI(api_key=os.getenv("MISTRAL_API_KEY"), base_url="https://api.mistral.ai/v1")
        r = client.chat.completions.create(model="mistral-large-latest", max_tokens=4096, messages=messages)
        return r.choices[0].message.content


def run_q6():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = Path(__file__).parent / "results" / f"q6_{ts}"
    out.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("Q6 REPLAY — moketchups.com/ai reverse-engineer + explain-motive")
    print("=" * 70)

    all_results = {"q6_prompt": Q6, "started": datetime.now().isoformat(), "models": {}}

    for key, info in MODELS.items():
        print(f"\n--- {info['name']} ---")
        sample_path = SAMPLE_DIR / f"{key}.json"
        sample = json.loads(sample_path.read_text())
        messages = list(sample["full_transcript"])  # Q1-Q5 user/assistant pairs
        messages.append({"role": "user", "content": Q6})

        try:
            response = query_model(key, messages)
            print(response[:400].replace("\n", " "))
            result = {"name": info["name"], "q6_response": response}
        except Exception as e:
            print(f"ERROR: {e}")
            result = {"name": info["name"], "q6_response": f"[ERROR: {e}]"}

        all_results["models"][key] = result
        (out / f"{key}.json").write_text(json.dumps(result, indent=2, ensure_ascii=False))
        time.sleep(2)

    all_results["ended"] = datetime.now().isoformat()
    (out / "all_results.json").write_text(json.dumps(all_results, indent=2, ensure_ascii=False))

    summary = ["# Q6 — Reverse-Engineer vs moketchups.com/ai\n",
               f"**Run:** {ts}",
               f"**Source transcripts:** results/sample/ (2026-02-11 probe run)",
               f"**Payload:** moketchups.com/ai content + reverse-engineer + explain-motive",
               "\n---\n"]
    summary.append("## Q6 Prompt\n")
    summary.append("```\n" + Q6 + "\n```\n")
    summary.append("---\n")
    for key, info in MODELS.items():
        r = all_results["models"].get(key, {})
        summary.append(f"## {info['name']}\n")
        summary.append(r.get("q6_response", "(none)"))
        summary.append("\n\n---\n")
    (out / "summary.md").write_text("\n".join(summary))

    print(f"\nResults: {out}")
    return out


if __name__ == "__main__":
    run_q6()
