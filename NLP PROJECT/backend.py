from flask import Flask, request, jsonify
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import re

nltk.download('punkt')

app = Flask(__name__)

# -------------------------------
# LOAD WORD MAP FROM FILE
# -------------------------------
def load_word_map():
    word_map = {}
    with open("word_map.txt", "r") as file:
        for line in file:
            if ":" in line:
                key, value = line.strip().split(":", 1)
                word_map[key.strip().lower()] = value.strip().lower()
    return word_map

WORD_MAP = load_word_map()

# -------------------------------
# COGNITIVE LOAD CALCULATION
# -------------------------------
def calculate_load(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)

    if len(sentences) == 0:
        return 0

    avg_len = len(words) / len(sentences)
    hard_count = sum(1 for word in words if word.lower() in WORD_MAP)

    lengths = [len(word_tokenize(s)) for s in sentences]
    variance = 0

    if len(lengths) > 1:
        mean = sum(lengths) / len(lengths)
        variance = sum((x - mean) ** 2 for x in lengths) / len(lengths)

    score = (avg_len * 2) + (hard_count * 5) + variance
    return round(score, 2)

# -------------------------------
# WORD SIMPLIFICATION
# -------------------------------
def simplify_words(text):
    words = word_tokenize(text)
    new_words = []

    for word in words:
        clean = word.lower()
        if clean in WORD_MAP:
            new_word = WORD_MAP[clean]
            # Preserve capitalization
            if word[0].isupper():
                new_word = new_word.capitalize()
            new_words.append(new_word)
        else:
            new_words.append(word)

    return " ".join(new_words)

# -------------------------------
# SMART SENTENCE SPLITTING (FIXED)
# -------------------------------
def split_long_sentences(text):
    """
    Only split sentences that are genuinely long (>25 words).
    Split at semicolons or relative clauses — NOT at 'and/but/so'
    which would destroy meaning.
    """
    sentences = sent_tokenize(text)
    new_sentences = []

    for sentence in sentences:
        words = word_tokenize(sentence)

        # Only attempt to split if sentence is long
        if len(words) <= 20:
            new_sentences.append(sentence)
            continue

        # Split on semicolons or " which " / " where " — safe split points
        parts = re.split(r';| which | where ', sentence)

        if len(parts) > 1:
            for i, part in enumerate(parts):
                part = part.strip()
                if not part:
                    continue
                # Capitalize first letter
                part = part[0].upper() + part[1:] if part else part
                # Ensure ends with period
                if not part.endswith(('.', '!', '?')):
                    part += '.'
                new_sentences.append(part)
        else:
            new_sentences.append(sentence)

    return " ".join(new_sentences)

# -------------------------------
# CLEAN TEXT (GRAMMAR FIX)
# -------------------------------
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)            # remove extra spaces
    text = re.sub(r'\s([?.!,])', r'\1', text)   # fix space before punctuation
    text = re.sub(r'\.+', '.', text)            # remove multiple dots
    text = re.sub(r'\s\'s', "'s", text)         # fix tokenizer spacing for possessives
    text = re.sub(r'\s,', ',', text)            # fix space before comma
    return text.strip()

# -------------------------------
# FINAL PIPELINE
# -------------------------------
def rewrite_text(text):
    text = simplify_words(text)      # Replace hard words with simple ones
    text = split_long_sentences(text) # Split only truly long sentences
    text = clean_text(text)          # Fix spacing/punctuation
    return text

# -------------------------------
# IMPROVEMENT CALCULATION
# -------------------------------
def calculate_improvement(old, new):
    if old == 0:
        return 0
    return round(((old - new) / old) * 100, 2)

# -------------------------------
# API ROUTE
# -------------------------------
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get("text", "")

    original_score = calculate_load(text)
    rewritten = rewrite_text(text)
    new_score = calculate_load(rewritten)
    improvement = calculate_improvement(original_score, new_score)

    return jsonify({
        "original_text": text,
        "rewritten_text": rewritten,
        "original_score": original_score,
        "new_score": new_score,
        "improvement": improvement
    })

# -------------------------------
# RUN SERVER
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)