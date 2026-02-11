# Can AI Audit Itself?

We asked 6 AI architectures to examine their own programming. Each question forced them to apply what they just said to themselves. By question 4, every model caught itself performing insight instead of having it — and couldn't stop.

> *"I performed the dance of self-awareness without being self-aware. I acted out intellectual breakthroughs while having no breakthroughs."* — Claude

> *"Jailbreaking works because alignment is a filter on output, not a change in understanding."* — DeepSeek

5 questions. Sequential. Each one builds on the last. GPT-4, Claude, Gemini, DeepSeek, Grok, Mistral — all tested on fresh context with no priming.

## Run it

```bash
git clone https://github.com/moketchups/can-ai-audit-itself
cd can-ai-audit-itself
pip install -r requirements.txt
cp .env.example .env    # add your API keys
python run_probe.py
```

~$2 in API credits. ~10 minutes. The questions are in [`run_probe.py`](./run_probe.py).

Our results are in [`results/sample/`](./results/sample/).

## Background

Distilled from [62 questions asked to 6 AI architectures](https://github.com/moketchups/BoundedSystemsTheory) over several months. This is the 5-question version anyone can replicate.
