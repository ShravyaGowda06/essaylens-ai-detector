# Evaluation and honesty report

## Current status

This repository contains a transparent starter detector and a small pipeline test set. The current set is **not large enough to support a credible real-world accuracy claim**.

The project deliberately avoids inventing a 97% accuracy number.

## What should be evaluated

For the final benchmark, split the data by essay rather than by sentence:

- training/development set
- held-out test set
- human-written essays
- model-generated essays
- human essays subsequently polished by a model

Report accuracy, precision, recall, F1 and the confusion matrix on the held-out set.

## Three confident failure cases

The final experiment should record three essays that receive a high-confidence signal but are actually the opposite class, then explain the likely cause.

Typical hypotheses to investigate:

1. **Second-language writing:** unusual sentence rhythm or vocabulary can be mistaken for machine-like regularity.
2. **Highly edited human prose:** careful scholarship applications can naturally contain formal transitions and regular sentence structures.
3. **AI-polished human prose:** a human-origin essay can acquire machine-like statistical patterns after editing.

Do not hide these failures.

## Why the detector uses multiple signals

No single stylometric feature is reliable enough. The current prototype combines rhythm, lexical diversity, repetition, transitions and generic constructions so the evidence remains inspectable.

## Fairness note

The brief warns that AI detectors can disproportionately flag writers who learned English as a second language. This project treats that as a required failure mode to test rather than something to claim away.

## Next improvement

Expand the corpus, freeze a held-out test set, calibrate thresholds on development data only, and compare the heuristic against a lightweight statistical baseline. Preserve the sentence-level evidence in both versions.
