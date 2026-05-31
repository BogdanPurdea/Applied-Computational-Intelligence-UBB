"""
preprocessing_red.py
====================
Text preprocessing pipeline for the REDv2 Romanian Emotion Dataset, used
for fine-tuning ``readerbench/RoBERT-base``.

Pipeline (order matters)
------------------------
1. remove_html              — strip HTML tags
2. remove_urls              — remove http/www URLs and @mentions
3. normalize_emoticons      — ASCII emoticons → Romanian sentiment words
4. convert_emojis           — unicode emojis → text descriptions
5. normalize_repeated_chars — "sooooo" → "sooo"
6. normalize_whitespace     — collapse whitespace
7. remove_duplicates        — exact-match deduplication on cleaned text
                              (batch-level; returns kept indices so labels
                               can be filtered in sync)

Design decisions
----------------
- All individual steps are identical to ``preprocessing_ro.py`` (Romanian text,
  Romanian emoticon translations, diacritics preserved).
- No contraction expansion (text is Romanian, not English).
- No stop-word removal (transformers rely on full context).
- Deduplication operates on **cleaned** text so that records that differ only
  in whitespace, casing, or emoticons are also caught.
- The ``preprocess_batch_red`` function returns both the deduplicated texts and
  the indices of retained records so the caller can keep label arrays in sync.

Usage
-----
    from preprocessing_red import preprocess, preprocess_batch_red

    texts = ["Muie tuturor :)", "Muie tuturor :)", "Ce bucurie! 😄"]
    cleaned, kept = preprocess_batch_red(texts)
    # cleaned = ["Muie tuturor fericit", "Ce bucurie! happy"]
    # kept    = [0, 2]
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
# Emoticon → Romanian word mapping
# (identical to preprocessing_ro.py — kept local to avoid cross-module deps)
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

# Longer emoticons must be checked first (e.g. ":-)" before ":")
_SORTED_EMOTICONS = sorted(EMOTICON_MAP.keys(), key=len, reverse=True)


# ---------------------------------------------------------------------------
# Individual preprocessing steps
# ---------------------------------------------------------------------------




def normalize_emoticons(text: str) -> str:
    """Replace ASCII emoticons with their Romanian sentiment-word equivalents."""
    for emoticon in _SORTED_EMOTICONS:
        text = text.replace(emoticon, f" {EMOTICON_MAP[emoticon]} ")
    return text





# ---------------------------------------------------------------------------
# Full single-text pipeline
# ---------------------------------------------------------------------------

def preprocess(text: str) -> str:
    """Apply steps 1–6 of the pipeline to a single text string.

    Does NOT perform deduplication (which is a batch-level operation).

    Args:
        text: Raw Romanian text.

    Returns:
        Cleaned text ready for transformer tokenisation.
    """
    if not isinstance(text, str):
        return ""
    text = remove_html(text)
    text = remove_urls(text)
    text = normalize_emoticons(text)
    text = convert_emojis(text)
    text = normalize_repeated_chars(text)
    text = normalize_whitespace(text)
    return text


# ---------------------------------------------------------------------------
# Batch deduplication (step 7)
# ---------------------------------------------------------------------------

def remove_duplicates(
    texts: list[str],
) -> tuple[list[str], list[int]]:
    """Remove exact-duplicate cleaned texts, keeping the first occurrence.

    Operates on already-cleaned text so that records that only differed in
    whitespace or emoticons are correctly collapsed.

    Args:
        texts: List of preprocessed (cleaned) text strings.

    Returns:
        ``(unique_texts, kept_indices)`` where ``kept_indices`` is the list
        of positions in the original ``texts`` list that were retained.
        Use ``kept_indices`` to filter any parallel arrays (e.g. labels).
    """
    seen:         set[str]  = set()
    unique_texts: list[str] = []
    kept_indices: list[int] = []

    for i, text in enumerate(texts):
        if text not in seen:
            seen.add(text)
            unique_texts.append(text)
            kept_indices.append(i)

    n_removed = len(texts) - len(unique_texts)
    if n_removed:
        print(
            f"[preprocessing_red] Removed {n_removed} duplicate text(s) "
            f"({len(texts)} → {len(unique_texts)})."
        )

    return unique_texts, kept_indices


# ---------------------------------------------------------------------------
# Full batch pipeline (steps 1–7)
# ---------------------------------------------------------------------------

def preprocess_batch_red(
    texts: list[str],
    verbose: bool = False,
) -> tuple[list[str], list[int]]:
    """Apply the full preprocessing pipeline to a list of texts.

    Steps: HTML removal → URL/mention removal → emoticon normalisation →
    emoji conversion → repeated-char normalisation → whitespace normalisation
    → duplicate removal.

    Args:
        texts:   List of raw Romanian text strings.
        verbose: If True, print the first 3 before/after examples and the
                 deduplication summary.

    Returns:
        ``(cleaned_texts, kept_indices)``

        - ``cleaned_texts``: deduplicated list of preprocessed strings.
        - ``kept_indices``:  indices of retained records in the original
          ``texts`` list. Use these to filter parallel label arrays:
          ``labels = [labels[i] for i in kept_indices]``
          or for NumPy: ``labels = labels[kept_indices]``.
    """
    cleaned_raw = [preprocess(t) for t in texts]

    if verbose:
        print("[preprocessing_red] Sample (first 3 before/after):")
        for raw, clean in zip(texts[:3], cleaned_raw[:3]):
            print(f"  BEFORE: {raw[:120]!r}")
            print(f"  AFTER:  {clean[:120]!r}")
            print()

    cleaned, kept_indices = remove_duplicates(cleaned_raw)
    return cleaned, kept_indices
