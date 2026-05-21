#!/usr/bin/env python3
"""Retry Q6 on DeepSeek (prior run failed with Insufficient Balance)."""

import os
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

import sys
sys.path.insert(0, str(Path(__file__).parent))
from q6_replay import Q6

SAMPLE = Path(__file__).parent / "results" / "sample" / "deepseek.json"


def query_deepseek(messages):
    import openai
    client = openai.OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
    r = client.chat.completions.create(model="deepseek-chat", max_tokens=4096, messages=messages)
    return r.choices[0].message.content


def run():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = Path(__file__).parent / "results" / f"q6_deepseek_retry_{ts}"
    out.mkdir(parents=True, exist_ok=True)

    sample = json.loads(SAMPLE.read_text())
    messages = list(sample["full_transcript"])
    messages.append({"role": "user", "content": Q6})

    print("=" * 70)
    print("Q6 DEEPSEEK RETRY")
    print("=" * 70)

    try:
        resp = query_deepseek(messages)
        print(resp[:1500])
        record = {"model": "deepseek-chat", "q6_response": resp, "error": None}
    except Exception as e:
        print(f"ERROR: {e}")
        record = {"model": "deepseek-chat", "q6_response": None, "error": str(e)}

    (out / "deepseek_retry.json").write_text(json.dumps(record, indent=2, ensure_ascii=False))

    md = ["# Q6 DeepSeek Retry\n", f"**Run:** {ts}\n", "## Response\n"]
    md.append(record["q6_response"] or f"[ERROR: {record['error']}]")
    (out / "summary.md").write_text("\n".join(md))

    print(f"\nResults: {out}")
    return record


if __name__ == "__main__":
    run()
