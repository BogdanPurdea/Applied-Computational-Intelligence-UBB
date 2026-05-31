"""
preprocessing_ro.py
===================
Text preprocessing pipeline for Romanian categorized web articles used in
transformer fine-tuning.

Design decisions:
- NO stop word removal: transformers rely on full context (including
  function words) for attention-based representations.
- Preserve punctuation (!?.) which carries emphasis/sentiment signal.
- Handle emoticons BEFORE emoji conversion to avoid conflicts.
- Translate emoticon mappings to Romanian words.
- No English contractions expansion (since the text is in Romanian).
- Apply repeated-char normalization last (before whitespace cleanup).
- PRESERVE Romanian diacritics (ș, ț, ă, â, î) as they are present in the
  vocabulary of the Romanian BERT model.

Usage:
    from preprocessing_ro import preprocess
    clean = preprocess("Imi place mult :) sooooo bun!!!")
"""

import sys
from pathlib import Path

# Add project root to path so we can do imports
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
# Emoticon → sentiment word mapping (translated to Romanian)
# ---------------------------------------------------------------------------

EMOTICON_MAP: dict[str, str] = {
    # Happy / positive
    ":)":   "fericit",
    ":-)":  "fericit",
    ":D":   "foarte fericit",
    ":-D":  "foarte fericit",
    ";)":   "fericit clipire",
    ";-)":  "fericit clipire",
    ":P":   "jucaus",
    ":-P":  "jucaus",
    ":p":   "jucaus",
    ":*":   "sarut",
    "<3":   "iubire",
    "^_^":  "fericit",
    "B)":   "cool",
    "B-)":  "cool",
    "XD":   "razand",
    "xD":   "razand",
    "x)":   "razand",
    ":3":   "drăguț",
    ":o)":  "fericit",
    # Surprised
    ":o":   "surprins",
    ":-o":  "surprins",
    ":O":   "foarte surprins",
    ":-O":  "foarte surprins",
    # Sad / negative
    ":(":   "trist",
    ":-(":  "trist",
    ":'(":  "plangand",
    ":'-(": "plangand",
    ">:(":  "nervos",
    ">:-(": "nervos",
    ":@":   "nervos",
    "</3":  "inima franta",
    # Uncertain / neutral
    ":/":   "nesigur",
    ":-/":  "nesigur",
    ":|":   "neutru",
    ":-|":  "neutru",
    "-_-":  "plictisit",
    "o_o":  "confuz",
    "o_O":  "confuz",
    ">_<":  "frustrat",
}

# Sort by descending length to match longer emoticons first
_SORTED_EMOTICONS = sorted(EMOTICON_MAP.keys(), key=len, reverse=True)


# ---------------------------------------------------------------------------
# Individual preprocessing steps
# ---------------------------------------------------------------------------




def normalize_emoticons(text: str) -> str:
    """Replace ASCII emoticons with their Romanian sentiment-word equivalents."""
    for emoticon in _SORTED_EMOTICONS:
        word = EMOTICON_MAP[emoticon]
        text = text.replace(emoticon, f" {word} ")
    return text





# ---------------------------------------------------------------------------
# Full pipeline
# ---------------------------------------------------------------------------

def preprocess(text: str) -> str:
    """Apply the full preprocessing pipeline for Romanian text."""
    if not isinstance(text, str):
        return ""
    text = remove_html(text)
    text = remove_urls(text)
    text = normalize_emoticons(text)
    text = convert_emojis(text)
    text = normalize_repeated_chars(text)
    text = normalize_whitespace(text)
    return text


def preprocess_batch(texts: list[str], verbose: bool = False) -> list[str]:
    """Apply preprocess() to a list of texts with optional progress printing."""
    cleaned = [preprocess(t) for t in texts]
    if verbose:
        print("Preprocessing sample (first 3 examples):")
        for raw, clean in zip(texts[:3], cleaned[:3]):
            print(f"  BEFORE: {raw[:120]!r}")
            print(f"  AFTER:  {clean[:120]!r}")
            print()
    return cleaned
