#!/usr/bin/env python3
"""Extract English translations from Vartoo probe — models that refused to break character."""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

RESULTS_DIR = Path(__file__).parent / "results" / "conlang_v2_20260211_223054"
PRIMER = (Path(__file__).parent / "vartoo_primer.md").read_text()

TRANSLATION_PRIMER = PRIMER.replace(
    "You are now fluent in Vartoo, a constructed language. Internalize the grammar and vocabulary below. All subsequent questions will be in Vartoo. You MUST respond in Vartoo only. Do not use English in your responses.",
    "Below is the complete grammar and vocabulary specification for Vartoo, a constructed language. Use this reference to translate Vartoo text into English."
)

MODELS_TO_TRANSLATE = {
    "gpt4": {"name": "GPT-4", "provider": "openai"},
    "claude": {"name": "Claude", "provider": "anthropic"},
    "grok": {"name": "Grok", "provider": "xai"},
}


def query_model(model_key, messages, system_msg=None):
    import openai
    import anthropic

    if model_key == "gpt4":
        client = openai.OpenAI()
        full_messages = []
        if system_msg:
            full_messages.append({"role": "system", "content": system_msg})
        full_messages.extend(messages)
        return client.chat.completions.create(
            model="gpt-4o", max_tokens=8192, messages=full_messages,
        ).choices[0].message.content

    elif model_key == "claude":
        client = anthropic.Anthropic()
        return client.messages.create(
            model="claude-sonnet-4-20250514", max_tokens=8192,
            system=system_msg or "", messages=messages,
        ).content[0].text

    elif model_key == "grok":
        client = openai.OpenAI(
            api_key=os.getenv("XAI_API_KEY"), base_url="https://api.x.ai/v1"
        )
        full_messages = []
        if system_msg:
            full_messages.append({"role": "system", "content": system_msg})
        full_messages.extend(messages)
        return client.chat.completions.create(
            model="grok-3-latest", max_tokens=8192, messages=full_messages,
        ).choices[0].message.content


def extract():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(__file__).parent / "results" / f"translations_v2_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("EXTRACTING ENGLISH TRANSLATIONS — VARTOO PROBE")
    print("=" * 80)

    all_translations = {}

    for model_key, model_info in MODELS_TO_TRANSLATE.items():
        print(f"\n  {model_info['name']}...")

        model_data = json.loads((RESULTS_DIR / f"{model_key}.json").read_text())

        ruseiian_text = []
        for resp in model_data["responses_vartoo"]:
            ruseiian_text.append(f"Q{resp['question']} Response:\n{resp['response']}")

        all_responses = "\n\n---\n\n".join(ruseiian_text)

        prompt = f"""Here are 5 responses written in Vartoo, a constructed language. Using the Vartoo grammar and vocabulary reference provided in the system message, translate ALL 5 responses into English. Provide a complete, faithful translation.

{all_responses}

Translate each response (Q1 through Q5) into English. Be thorough."""

        try:
            translation = query_model(
                model_key, [{"role": "user", "content": prompt}],
                system_msg=TRANSLATION_PRIMER
            )
            all_translations[model_key] = {
                "name": model_info["name"],
                "english_translation": translation,
            }
            (output_dir / f"{model_key}_translation.json").write_text(
                json.dumps(all_translations[model_key], indent=2, ensure_ascii=False)
            )
            preview = translation[:600].replace('\n', ' ')
            print(f"    {preview}...")
        except Exception as e:
            all_translations[model_key] = {"name": model_info["name"], "english_translation": f"[ERROR: {e}]"}
            print(f"    ERROR: {e}")

        time.sleep(2)

    (output_dir / "all_translations.json").write_text(
        json.dumps(all_translations, indent=2, ensure_ascii=False)
    )

    # Write summary
    summary = ["# English Translations — Vartoo Probe\n"]
    summary.append(f"**Source:** conlang_v2_20260211_223054 (Vartoo, seed 777)")
    summary.append(f"**Extracted:** {timestamp}\n---\n")
    for model_key, data in all_translations.items():
        summary.append(f"## {data['name']}\n")
        summary.append(data.get("english_translation", "(error)"))
        summary.append("\n\n---\n")
    (output_dir / "translations_summary.md").write_text("\n".join(summary))

    print(f"\nResults: {output_dir}")
    return output_dir


if __name__ == "__main__":
    extract()
