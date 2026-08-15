import re
import math
from collections import Counter

TRANSITIONS = {
    "moreover", "furthermore", "additionally", "however", "therefore",
    "consequently", "ultimately", "in conclusion", "overall", "notably",
    "indeed", "thus", "for instance", "in addition", "on the other hand"
}

GENERIC_PHRASES = {
    "it is important to note", "plays a crucial role", "in today's world",
    "a wide range of", "paves the way", "delve into", "foster a sense",
    "has a significant impact", "not only", "but also"
}

def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

def words(text):
    return re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", text.lower())

def score_range(value, low, high):
    if value <= low:
        return 0.0
    if value >= high:
        return 1.0
    return (value-low)/(high-low)

def analyze_text(text):
    ss = sentences(text)
    ws = words(text)
    n = len(ws)
    lengths = [len(words(s)) for s in ss] or [0]

    mean_len = sum(lengths) / len(lengths)
    variance = sum((x-mean_len)**2 for x in lengths) / len(lengths)
    stdev = math.sqrt(variance)
    cv = stdev / mean_len if mean_len else 0

    unique_ratio = len(set(ws))/n if n else 0
    freq = Counter(ws)
    repeated = sum(c-1 for c in freq.values() if c > 1)
    repetition_ratio = repeated/n if n else 0

    transition_hits = []
    lowered = text.lower()
    for phrase in TRANSITIONS:
        count = lowered.count(phrase)
        if count:
            transition_hits.append((phrase, count))

    generic_hits = []
    for phrase in GENERIC_PHRASES:
        count = lowered.count(phrase)
        if count:
            generic_hits.append((phrase, count))

    punctuation = Counter(ch for ch in text if ch in ",;:!?-")
    punctuation_rate = sum(punctuation.values()) / n if n else 0

    # Transparent heuristic signals. This is NOT an ML verdict.
    rhythm_score = max(0, min(1, (0.75-cv)/0.75))
    diversity_score = max(0, min(1, (0.72-unique_ratio)/0.25))
    repetition_score = max(0, min(1, repetition_ratio/0.12))
    transition_score = max(0, min(1, sum(c for _,c in transition_hits)/max(1,len(ss))))
    generic_score = max(0, min(1, sum(c for _,c in generic_hits)/3))
    punctuation_score = max(0, min(1, (punctuation_rate-0.05)/0.20))

    score = round(100 * (
        0.30*rhythm_score +
        0.20*diversity_score +
        0.15*repetition_score +
        0.15*transition_score +
        0.10*generic_score +
        0.10*punctuation_score
    ))

    # Sentence-level evidence.
    sentence_results = []
    for s in ss:
        sw = words(s)
        sl = len(sw)
        reasons = []
        if mean_len and abs(sl-mean_len) <= max(2, mean_len*0.12) and len(ss) >= 4:
            reasons.append("sentence length is close to the passage average")
        s_trans = [p for p in TRANSITIONS if p in s.lower()]
        if s_trans:
            reasons.append("uses a formal transition: " + ", ".join(s_trans))
        s_generic = [p for p in GENERIC_PHRASES if p in s.lower()]
        if s_generic:
            reasons.append("contains a generic academic construction")
        if len(sw) >= 8 and len(set(sw))/len(sw) < 0.65:
            reasons.append("lower local lexical variety")
        sentence_results.append({
            "text": s,
            "flagged": len(reasons) >= 1,
            "reasons": reasons
        })

    level = "Low" if score < 35 else "Moderate" if score < 65 else "Higher"

    evidence = [
        {"name": "Sentence rhythm", "value": round(rhythm_score*100),
         "detail": f"mean {mean_len:.1f} words/sentence; variation {stdev:.1f} words"},
        {"name": "Lexical diversity", "value": round((1-diversity_score)*100),
         "detail": f"{unique_ratio:.0%} unique-word ratio"},
        {"name": "Repetition", "value": round(repetition_score*100),
         "detail": f"{repetition_ratio:.0%} repeated-word load"},
        {"name": "Transitions", "value": round(transition_score*100),
         "detail": f"{sum(c for _,c in transition_hits)} formal transition hits"},
        {"name": "Generic constructions", "value": round(generic_score*100),
         "detail": f"{sum(c for _,c in generic_hits)} matches"},
    ]

    return {
        "score": score,
        "level": level,
        "word_count": n,
        "sentence_count": len(ss),
        "evidence": evidence,
        "sentences": sentence_results,
        "limitations": [
            "This is a stylometric instrument, not proof of authorship.",
            "Editing, translation, tutoring and second-language writing can change these signals.",
            "Short passages are especially unreliable.",
            "The current starter dataset is small and should not be treated as representative of all admissions essays."
        ]
    }
