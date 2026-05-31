"""
preprocessing.py
================
Text preprocessing pipeline for IMDB-style movie reviews used in
transformer fine-tuning.

Design decisions:
- NO stop word removal: transformers rely on full context (including
  function words) for attention-based representations. Removing stop
  words would corrupt the input distribution and degrade performance.
- Preserve punctuation (!?.) which carries emphasis/sentiment signal.
- Handle emoticons BEFORE emoji conversion to avoid conflicts.
- Expand contractions AFTER HTML/URL removal for cleaner input.
- Apply repeated-char normalization last (before whitespace cleanup).

Usage:
    from preprocessing import preprocess
    clean = preprocess("I loved it :) <br/> sooooo good!!!")
"""

import sys
from pathlib import Path
import contractions as contractions_lib

# Add project root and shared/migrated to path so we can do imports
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "shared" / "migrated"))
from preprocessing_base import (
    remove_html,
    remove_urls,
    convert_emojis,
    normalize_repeated_chars,
    normalize_whitespace,
)


# ---------------------------------------------------------------------------
# Emoticon → sentiment word mapping
# ---------------------------------------------------------------------------

EMOTICON_MAP: dict[str, str] = {
    # Happy / positive
    ":)":   "happy",
    ":-)":  "happy",
    ":D":   "very happy",
    ":-D":  "very happy",
    ";)":   "winky happy",
    ";-)":  "winky happy",
    ":P":   "playful",
    ":-P":  "playful",
    ":p":   "playful",
    ":*":   "kiss",
    "<3":   "love",
    "^_^":  "happy",
    "B)":   "cool",
    "B-)":  "cool",
    "XD":   "laughing",
    "xD":   "laughing",
    "x)":   "laughing",
    ":3":   "cute",
    ":o)":  "happy",
    # Surprised
    ":o":   "surprised",
    ":-o":  "surprised",
    ":O":   "very surprised",
    ":-O":  "very surprised",
    # Sad / negative
    ":(":   "sad",
    ":-(":  "sad",
    ":'(":  "crying",
    ":'-(": "crying",
    ">:(":  "angry",
    ">:-(": "angry",
    ":@":   "angry",
    "</3":  "heartbreak",
    # Uncertain / neutral
    ":/":   "unsure",
    ":-/":  "unsure",
    ":|":   "neutral",
    ":-|":  "neutral",
    "-_-":  "bored",
    "o_o":  "confused",
    "o_O":  "confused",
    ">_<":  "frustrated",
}

# Sort by descending length to match longer emoticons first (e.g. ":-)" before ":")
_SORTED_EMOTICONS = sorted(EMOTICON_MAP.keys(), key=len, reverse=True)


# ---------------------------------------------------------------------------
# Individual preprocessing steps
# ---------------------------------------------------------------------------




def normalize_emoticons(text: str) -> str:
    """Replace ASCII emoticons with their sentiment-word equivalents.

    Iterates in descending length order so multi-char emoticons like ':-)'
    are replaced before single-char prefixes like ':'.
    """
    for emoticon in _SORTED_EMOTICONS:
        word = EMOTICON_MAP[emoticon]
        text = text.replace(emoticon, f" {word} ")
    return text





def expand_contractions(text: str) -> str:
    """Expand English contractions so negations are explicit.

    E.g. "don't" → "do not", "can't" → "cannot", "it's" → "it is".
    Critical for sentiment: "not good" ≠ "good".
    """
    return contractions_lib.fix(text)





# ---------------------------------------------------------------------------
# Full pipeline
# ---------------------------------------------------------------------------

def preprocess(text: str) -> str:
    """Apply the full preprocessing pipeline for transformer fine-tuning.

    Pipeline order (order matters):
        1. remove_html              — strip tags before any other processing
        2. remove_urls              — remove noise before tokenization
        3. normalize_emoticons      — ASCII emoticons → words (before emoji step)
        4. convert_emojis           — unicode emojis → words
        5. expand_contractions      — "don't" → "do not" (negation-safe)
        6. normalize_repeated_chars — "sooooo" → "sooo"
        7. normalize_whitespace     — clean up spacing

    Stop word removal is intentionally omitted: transformers use full-context
    attention and their subword tokenizer expects natural text. Removing stop
    words would discard function words that guide syntactic/semantic
    interpretation and degrade fine-tuning quality.

    Args:
        text: Raw review text.

    Returns:
        Cleaned text string ready for transformer tokenization.
    """
    if not isinstance(text, str):
        return ""
    text = remove_html(text)
    text = remove_urls(text)
    text = normalize_emoticons(text)
    text = convert_emojis(text)
    text = expand_contractions(text)
    text = normalize_repeated_chars(text)
    text = normalize_whitespace(text)
    return text


def preprocess_batch(texts: list[str], verbose: bool = False) -> list[str]:
    """Apply preprocess() to a list of texts with optional progress printing.

    Args:
        texts:   List of raw text strings.
        verbose: If True, print a sample of before/after pairs.

    Returns:
        List of cleaned text strings.
    """
    cleaned = [preprocess(t) for t in texts]
    if verbose:
        print("Preprocessing sample (first 3 examples):")
        for raw, clean in zip(texts[:3], cleaned[:3]):
            print(f"  BEFORE: {raw[:120]!r}")
            print(f"  AFTER:  {clean[:120]!r}")
            print()
    return cleaned
