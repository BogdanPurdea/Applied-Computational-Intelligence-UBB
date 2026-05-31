"""
preprocessing_base.py
=====================
Core text preprocessing components and regular expressions shared across languages.
"""

from __future__ import annotations

import re
import emoji

# ---------------------------------------------------------------------------
# Compiled Regular Expressions for Performance
# ---------------------------------------------------------------------------

HTML_REGEX = re.compile(r"<[^>]+>")
URL_REGEX = re.compile(r"https?://\S+|www\.\S+")
MENTION_REGEX = re.compile(r"@\w+")
EMOJI_REGEX = re.compile(r":([a-z0-9_]+):")
REPEATED_CHARS_REGEX = re.compile(r"(.)\1{3,}")
WHITESPACE_REGEX = re.compile(r"\s+")

# ---------------------------------------------------------------------------
# Core Cleaning Functions
# ---------------------------------------------------------------------------

def remove_html(text: str) -> str:
    """Remove HTML tags (e.g., <br />, <b>, <i>)."""
    return HTML_REGEX.sub(" ", text)

def remove_urls(text: str) -> str:
    """Remove URLs and Twitter-style @mentions."""
    text = URL_REGEX.sub(" ", text)
    text = MENTION_REGEX.sub(" ", text)
    return text

def convert_emojis(text: str) -> str:
    """Convert unicode emojis to readable text descriptions.

    E.g. 😊 -> 'smiling face with smiling eyes'
    """
    demojized = emoji.demojize(text)  # e.g. ":smiling_face:"
    return EMOJI_REGEX.sub(lambda m: " " + m.group(1).replace("_", " ") + " ", demojized)

def normalize_repeated_chars(text: str) -> str:
    """Cap runs of 4+ identical characters to 3.

    E.g. "sooooo" -> "sooo"
    """
    return REPEATED_CHARS_REGEX.sub(r"\1\1\1", text)

def normalize_whitespace(text: str) -> str:
    """Collapse multiple spaces, newlines, and tabs into a single space."""
    return WHITESPACE_REGEX.sub(" ", text).strip()
