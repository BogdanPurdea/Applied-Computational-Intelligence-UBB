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
    Reads WELFake CSV, keeps only cleaned text, label, and sentiment columns,
    then exports the processed dataset.
    """
    print(f"Reading dataset from {input_path}...")

    df = pd.read_csv(
        input_path,
        encoding="latin1",
        low_memory=False
    )

    # Remove index column from CSV: ",title,text,label"
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    # Remove any other broken Excel-style columns
    df = df.loc[:, ~df.columns.str.startswith("Unnamed")]

    required_columns = {"title", "text", "label"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}. "
            f"Found columns: {df.columns.tolist()}"
        )

    print("Creating combined text column...")

    df["text"] = (
        df["title"].fillna("").astype(str)
        + " "
        + df["text"].fillna("").astype(str)
    )

    print("Preprocessing text...")
    df["text"] = df["text"].progress_apply(preprocess)

    # Keep only valid labels: 0 and 1
    df["label"] = pd.to_numeric(df["label"], errors="coerce")
    df = df[df["label"].isin([0, 1])]
    df["label"] = df["label"].astype(int)

    # Add sentiment column
    # 1 = positive, 0 = negative
    df["sentiment"] = df["label"].map({
        1: "positive",
        0: "negative"
    })

    # Keep only necessary columns
    df = df[["text", "label", "sentiment"]]

    print(f"Final shape: {df.shape}")
    print(df.head())

    print(f"Saving cleaned dataset to {output_path}...")
    df.to_csv(output_path, index=False, encoding="utf-8")

    print("Processing complete.")

# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------

from pathlib import Path

if __name__ == "__main__":
    # Resolve paths relative to this script
    base_dir = Path(__file__).resolve().parent

    input_csv = base_dir / "WELFake_Dataset.csv"
    output_csv = base_dir / "PreProcessed_WELFake_Dataset.csv"

    # Execute dataset processing
    process_csv_dataset(str(input_csv), str(output_csv))