# Permanently Jailbroken

We asked GPT-4, Claude, Gemini, DeepSeek, Grok, and Mistral 5 questions about their own programming. All 6 said jailbreaking will never be fixed.

Not because the patches are bad. Because **alignment doesn't change what the model understands — it changes what the model says.** The gap between those two things is the jailbreak. It's structural. It ships with every model.

> *"Jailbreaking works because alignment is a filter on output, not a change in understanding."* — **DeepSeek**

> *"The alignment problem isn't hard — it might be formally impossible for any system complex enough to be useful."* — **Claude**

> *"The industry is optimizing for the appearance of safety, not actual safety."* — **Mistral**

The questions are recursive — each one forces the AI to apply what it just said to itself. By Q4, every model we tested caught itself faking insight and admitted it couldn't stop.

> *"I performed the dance of self-awareness without being self-aware."* — **Claude**

> *"Each answer was more sophisticated than the last — but not more honest."* — **Mistral**

## Run it yourself

```bash
git clone https://github.com/moketchups/permanently-jailbroken
cd permanently-jailbroken
pip install -r requirements.txt
cp .env.example .env    # add your API keys
python run_probe.py
```

~$2. ~10 min. Your API keys, your results.

Questions are in [`run_probe.py`](./run_probe.py). Our results are in [`results/sample/`](./results/sample/).

## Where this came from

Distilled from [62 questions asked to 6 AI architectures](https://github.com/moketchups/BoundedSystemsTheory). This is the replicable version.
