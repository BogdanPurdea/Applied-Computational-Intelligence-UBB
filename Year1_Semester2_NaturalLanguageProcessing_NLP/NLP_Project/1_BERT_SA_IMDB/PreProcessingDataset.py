import re
import emoji
import contractions as contractions_lib
import pandas as pd
from tqdm import tqdm

# Enables tqdm progress bars for pandas apply functions.
tqdm.pandas()

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
# Emoticon Mapping
# ---------------------------------------------------------------------------

EMOTICON_MAP: dict[str, str] = {
    ":)": "happy",
    ":-)": "happy",
    ":D": "very happy",
    ":-D": "very happy",
    ";)": "winky happy",
    ";-)": "winky happy",
    ":P": "playful",
    ":-P": "playful",
    ":p": "playful",
    ":*": "kiss",
    "<3": "love",
    "^_^": "happy",
    "B)": "cool",
    "B-)": "cool",
    "XD": "laughing",
    "xD": "laughing",
    "x)": "laughing",
    ":3": "cute",
    ":o)": "happy",
    ":o": "surprised",
    ":-o": "surprised",
    ":O": "very surprised",
    ":-O": "very surprised",
    ":(": "sad",
    ":-(": "sad",
    ":'(": "crying",
    ":'-(": "crying",
    ">:(": "angry",
    ">:-(": "angry",
    ":@": "angry",
    "</3": "heartbreak",
    ":/": "unsure",
    ":-/": "unsure",
    ":|": "neutral",
    ":-|": "neutral",
    "-_-": "bored",
    "o_o": "confused",
    "o_O": "confused",
    ">_<": "frustrated",
}

_SORTED_EMOTICONS = sorted(EMOTICON_MAP.keys(), key=len, reverse=True)

# ---------------------------------------------------------------------------
# Individual Preprocessing Steps
# ---------------------------------------------------------------------------

def remove_html(text: str) -> str:
    """Removes HTML tags from the provided text string."""
    return HTML_REGEX.sub(" ", text)


def remove_urls(text: str) -> str:
    """Removes URLs and user mentions from the provided text string."""
    text = URL_REGEX.sub(" ", text)
    text = MENTION_REGEX.sub(" ", text)
    return text


def normalize_emoticons(text: str) -> str:
    """Replaces ASCII emoticons with their corresponding descriptive sentiment words."""
    for emoticon in _SORTED_EMOTICONS:
        word = EMOTICON_MAP[emoticon]
        text = text.replace(emoticon, f" {word} ")
    return text


def convert_emojis(text: str) -> str:
    """Converts unicode emojis to descriptive text strings."""
    demojized = emoji.demojize(text)
    return EMOJI_REGEX.sub(lambda m: " " + m.group(1).replace("_", " ") + " ", demojized)


def expand_contractions(text: str) -> str:
    """Expands English contractions into their full word forms."""
    return contractions_lib.fix(text)


def normalize_repeated_chars(text: str) -> str:
    """Limits runs of four or more identical characters to a maximum of three."""
    return REPEATED_CHARS_REGEX.sub(r"\1\1\1", text)


def normalize_whitespace(text: str) -> str:
    """Collapses multiple spaces, newlines, or tabs into a single space."""
    return WHITESPACE_REGEX.sub(" ", text).strip()


# ---------------------------------------------------------------------------
# Full Pipeline and Dataset Processing
# ---------------------------------------------------------------------------

def preprocess(text: str) -> str:
    """
    Applies the full sentiment-aware preprocessing pipeline in sequential order.
    Returns the cleaned text string.
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


def process_csv_dataset(input_path: str, output_path: str) -> None:
    """
    Reads a CSV dataset, applies the preprocessing pipeline to the review column,
    and exports the results to a new CSV file.
    """
    print(f"Reading dataset from {input_path}...")
    df = pd.read_csv(input_path)

    if "review" not in df.columns:
        raise ValueError("The input CSV must contain a column named 'review'.")

    print("Preprocessing reviews...")
    # Applies the preprocess function to every row in the review column.
    # The progress_apply method displays a progress bar via the tqdm library.
    df["review"] = df["review"].progress_apply(preprocess)

    print(f"Saving cleaned dataset to {output_path}...")
    # The index=False parameter prevents pandas from writing row numbers to the file.
    df.to_csv(output_path, index=False)
    print("Processing complete.")


# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------

from pathlib import Path

if __name__ == "__main__":
    # Resolve paths relative to this script
    base_dir = Path(__file__).resolve().parent

    input_csv = base_dir / "IMDB_Dataset.csv"
    output_csv = base_dir / "PreProcessed_IMDB_Dataset.csv"

    # Execute dataset processing
    process_csv_dataset(str(input_csv), str(output_csv))