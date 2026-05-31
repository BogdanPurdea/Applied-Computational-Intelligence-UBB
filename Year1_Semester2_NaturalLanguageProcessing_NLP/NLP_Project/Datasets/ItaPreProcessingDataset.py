import re
import emoji
import contractions as contractions_lib
import pandas as pd
from tqdm import tqdm

# Abilita le barre di avanzamento di tqdm per le funzioni apply di pandas.
tqdm.pandas()

# ---------------------------------------------------------------------------
# Espressioni Regolari Compilate per Prestazioni Ottimali
# ---------------------------------------------------------------------------

HTML_REGEX = re.compile(r"<[^>]+>")
URL_REGEX = re.compile(r"https?://\S+|www\.\S+")
MENTION_REGEX = re.compile(r"@\w+")
EMOJI_REGEX = re.compile(r":([a-z0-9_]+):")
REPEATED_CHARS_REGEX = re.compile(r"(.)\1{3,}")
WHITESPACE_REGEX = re.compile(r"\s+")

# ---------------------------------------------------------------------------
# Mappatura delle Emoticon
# ---------------------------------------------------------------------------

EMOTICON_MAP: dict[str, str] = {
    ":)": "felice",
    ":-)": "felice",
    ":D": "molto felice",
    ":-D": "molto felice",
    ";)": "occhiolino",
    ";-)": "occhiolino",
    ":P": "scherzoso",
    ":-P": "scherzoso",
    ":p": "scherzoso",
    ":*": "bacio",
    "<3": "amore",
    "^_^": "felice",
    "B)": "fantastico",
    "B-)": "fantastico",
    "XD": "risata",
    "xD": "risata",
    "x)": "risata",
    ":3": "carino",
    ":o)": "felice",
    ":o": "sorpreso",
    ":-o": "sorpreso",
    ":O": "molto sorpreso",
    ":-O": "molto sorpreso",
    ":(": "triste",
    ":-(": "triste",
    ":'(": "pianto",
    ":'-(": "pianto",
    ">:(": "arrabbiato",
    ">:-(": "arrabbiato",
    ":@": "arrabbiato",
    "</3": "cuore infranto",
    ":/": "incerto",
    ":-/": "incerto",
    ":|": "neutrale",
    ":-|": "neutrale",
    "-_-": "annoiato",
    "o_o": "confuso",
    "o_O": "confuso",
    ">_<": "frustrato",
}

_SORTED_EMOTICONS = sorted(EMOTICON_MAP.keys(), key=len, reverse=True)

# ---------------------------------------------------------------------------
# Passaggi Singoli di Pre-elaborazione
# ---------------------------------------------------------------------------

def remove_html(text: str) -> str:
    """Rimuove i tag HTML dalla stringa di testo fornita."""
    return HTML_REGEX.sub(" ", text)


def remove_urls(text: str) -> str:
    """Rimuove gli URL e le menzioni utente dalla stringa di testo fornita."""
    text = URL_REGEX.sub(" ", text)
    text = MENTION_REGEX.sub(" ", text)
    return text


def normalize_emoticons(text: str) -> str:
    """Sostituisce le emoticon ASCII con le parole descrittive del sentimento corrispondente."""
    for emoticon in _SORTED_EMOTICONS:
        word = EMOTICON_MAP[emoticon]
        text = text.replace(emoticon, f" {word} ")
    return text


def convert_emojis(text: str) -> str:
    """Converte le emoji unicode in stringhe di testo descrittive."""
    # Il parametro language='it' traduce la descrizione della libreria emoji in italiano.
    demojized = emoji.demojize(text, language="it")
    return EMOJI_REGEX.sub(lambda m: " " + m.group(1).replace("_", " ") + " ", demojized)


def expand_contractions(text: str) -> str:
    """Espande le contrazioni della lingua inglese nelle loro forme verbali complete."""
    return contractions_lib.fix(text)


def normalize_repeated_chars(text: str) -> str:
    """Limita le sequenze di quattro o più caratteri identici a un massimo di tre."""
    return REPEATED_CHARS_REGEX.sub(r"\1\1\1", text)


def normalize_whitespace(text: str) -> str:
    """Comprime spazi multipli, ritorni a capo o tabulazioni in un singolo spazio vuoto."""
    return WHITESPACE_REGEX.sub(" ", text).strip()


# ---------------------------------------------------------------------------
# Pipeline Completa ed Elaborazione del Dataset
# ---------------------------------------------------------------------------

def preprocess(text: str) -> str:
    """
    Applica la pipeline completa di pre-elaborazione in ordine sequenziale.
    Restituisce la stringa di testo pulita.
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
    Legge un dataset CSV, applica la pipeline di pre-elaborazione alla colonna di testo
    ed esporta i risultati in un nuovo file CSV.
    """
    print(f"Lettura del dataset da {input_path} in corso...")
    df = pd.read_csv(input_path)

    if "text" not in df.columns:
        raise ValueError("Il file CSV di input deve contenere una colonna denominata 'text'.")

    print("Pre-elaborazione del testo in corso...")
    # Applica la funzione preprocess a ogni riga nella colonna di testo.
    # Il metodo progress_apply visualizza una barra di avanzamento tramite la libreria tqdm.
    df["text"] = df["text"].progress_apply(preprocess)

    print(f"Salvataggio del dataset pulito in {output_path} in corso...")
    # Il parametro index=False impedisce a pandas di scrivere i numeri di riga sequenziali nel file.
    df.to_csv(output_path, index=False)
    print("Elaborazione completata.")


# ---------------------------------------------------------------------------
# Esecuzione
# ---------------------------------------------------------------------------

from pathlib import Path

if __name__ == "__main__":
    # Risolve i percorsi dei file in relazione alla cartella di questo script.
    base_dir = Path(__file__).resolve().parent

    input_csv = base_dir / "FEEL-IT_Dataset.csv"
    output_csv = base_dir / "PreProcessed_FEEL-IT_Dataset.csv"

    # Esegue l'elaborazione del dataset.
    process_csv_dataset(str(input_csv), str(output_csv))