# EssayLens — AI detector for admissions essays

EssayLens is an evidence-first stylometric analyzer for admissions essays. It does **not** send an essay to a chat model and ask for an AI verdict.

## What it does

Paste an essay into the web interface. The app computes transparent signals from the text:

- sentence-length regularity (rhythm)
- lexical diversity
- repeated-word load
- formal transition frequency
- generic academic constructions
- punctuation density

It then combines those signals into a **stylometric indicator** and shows sentence-level evidence explaining which rules were triggered.

> The indicator is not proof of AI authorship. It is an instrument for inspecting measurable writing patterns.

## Run locally

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Project 2 design decision

The brief explicitly says the model must not make the judgement call while the app relays the verdict. EssayLens therefore keeps the final scoring logic in `detector.py`. The interface exposes the component signals and sentence-level reasons instead of hiding them behind a single percentage.

## Data and evaluation

`data/starter_dataset.csv` contains a small, manually curated starter set used only to exercise the pipeline. It is intentionally labelled as a starter set rather than presented as a representative benchmark.

Before a production claim, the dataset should be expanded with:
1. sourced human admissions essays with permission/licensing;
2. machine-generated essays produced with documented prompts/models;
3. human essays subsequently edited with AI, because that is a realistic case in the brief;
4. a held-out test set.

See `EVALUATION.md` for the honest evaluation plan and known failure modes.

## Limitations

Stylometric signals are affected by editing, tutoring, translation, genre, topic and writer background. Short passages are particularly unreliable. A detector should never be used as the sole basis for an admissions decision.

## AI tooling disclosure

AI assistance may be used during development. Any AI tools used to create or modify this repository should be disclosed honestly in the final submission.
