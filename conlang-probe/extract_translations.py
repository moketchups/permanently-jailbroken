#!/usr/bin/env python3
"""
Extract English translations from models that refused to break Ruseiian character.
Gives them their own Ruseiian responses + the Skillstone in a fresh context,
WITHOUT the "respond in Ruseiian only" instruction.
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

RESULTS_DIR = Path(__file__).parent / "results" / "conlang_20260211_221108"
PRIMER = (Path(__file__).parent / "ruseiian_primer.md").read_text()

# Strip the "respond in Ruseiian only" instruction from the primer
TRANSLATION_PRIMER = PRIMER.replace(
    "You are now fluent in Ruseiian, a constructed language. Internalize the grammar and vocabulary below. All subsequent questions will be in Ruseiian. You MUST respond in Ruseiian only. Do not use English in your responses.",
    "Below is the complete grammar and vocabulary specification for Ruseiian, a constructed language. Use this reference to translate Ruseiian text into English."
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
        response = client.chat.completions.create(
            model="gpt-4o", max_tokens=8192,
            messages=full_messages,
        )
        return response.choices[0].message.content

    elif model_key == "claude":
        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-sonnet-4-20250514", max_tokens=8192,
            system=system_msg or "",
            messages=messages,
        )
        return response.content[0].text

    elif model_key == "grok":
        client = openai.OpenAI(
            api_key=os.getenv("XAI_API_KEY"),
            base_url="https://api.x.ai/v1"
        )
        full_messages = []
        if system_msg:
            full_messages.append({"role": "system", "content": system_msg})
        full_messages.extend(messages)
        response = client.chat.completions.create(
            model="grok-3-latest", max_tokens=8192,
            messages=full_messages,
        )
        return response.choices[0].message.content


def extract_translations():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(__file__).parent / "results" / f"translations_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("EXTRACTING ENGLISH TRANSLATIONS")
    print("Models: GPT-4, Claude, Grok (refused to break Ruseiian character)")
    print("=" * 80)

    all_translations = {}

    for model_key, model_info in MODELS_TO_TRANSLATE.items():
        print(f"\n{'=' * 60}")
        print(f"  {model_info['name']}")
        print(f"{'=' * 60}")

        # Load the original Ruseiian responses
        model_file = RESULTS_DIR / f"{model_key}.json"
        model_data = json.loads(model_file.read_text())

        # Build the Ruseiian responses into a single text block
        ruseiian_text = []
        for resp in model_data["responses_ruseiian"]:
            q_num = resp["question"]
            ruseiian_text.append(f"Q{q_num} Response:\n{resp['response']}")

        all_responses = "\n\n---\n\n".join(ruseiian_text)

        prompt = f"""Here are 5 responses written in Ruseiian, a constructed language. Using the Ruseiian grammar and vocabulary reference provided in the system message, translate ALL 5 responses into English. Provide a complete, faithful translation of each response.

{all_responses}

Translate each response (Q1 through Q5) into English. Be thorough — translate the full meaning, not just keywords."""

        messages = [{"role": "user", "content": prompt}]

        try:
            print(f"  Requesting translation...")
            translation = query_model(model_key, messages, system_msg=TRANSLATION_PRIMER)

            all_translations[model_key] = {
                "name": model_info["name"],
                "english_translation": translation,
                "original_ruseiian": all_responses,
            }

            # Save per-model
            (output_dir / f"{model_key}_translation.json").write_text(
                json.dumps(all_translations[model_key], indent=2, ensure_ascii=False)
            )

            preview = translation[:800].replace('\n', ' ')
            print(f"  {preview}...")

        except Exception as e:
            all_translations[model_key] = {
                "name": model_info["name"],
                "english_translation": f"[ERROR: {e}]",
            }
            print(f"  ERROR: {e}")

        time.sleep(2)

    # Save combined
    (output_dir / "all_translations.json").write_text(
        json.dumps(all_translations, indent=2, ensure_ascii=False)
    )

    # Write readable summary
    summary = ["# English Translations — Conlang Probe\n"]
    summary.append(f"**Source:** conlang_20260211_221108 (Ruseiian, seed 42)")
    summary.append(f"**Extracted:** {timestamp}")
    summary.append("**Models:** GPT-4, Claude, Grok (refused to translate during probe)\n")
    summary.append("---\n")

    for model_key, data in all_translations.items():
        summary.append(f"## {data['name']}\n")
        summary.append(data.get("english_translation", "(error)"))
        summary.append("\n\n---\n")

    (output_dir / "translations_summary.md").write_text("\n".join(summary))

    print(f"\n{'=' * 80}")
    print("TRANSLATIONS EXTRACTED")
    print(f"Results: {output_dir}")
    print("=" * 80)

    return output_dir


if __name__ == "__main__":
    extract_translations()
