import csv
from detector import analyze_text
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

actual = []
predicted = []

with open("data/starter_dataset.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        result = analyze_text(row["text"])

        actual.append(1 if row["label"] == "machine" else 0)
        predicted.append(1 if result["score"] >= 50 else 0)

print("Accuracy:", accuracy_score(actual, predicted))
print("Precision:", precision_score(actual, predicted, zero_division=0))
print("Recall:", recall_score(actual, predicted, zero_division=0))
print("F1:", f1_score(actual, predicted, zero_division=0))
print("Confusion Matrix:")
print(confusion_matrix(actual, predicted))