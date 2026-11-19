%%writefile /content/backend/rag/chunking/text_cleaner.py

import re
import unicodedata


def clean_text(text: str) -> str:

    if not text:
        return ""

    # Normalize Unicode characters
    text = unicodedata.normalize("NFKC", text)

    # Remove null characters
    text = text.replace("\x00", "")

    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove excessive horizontal whitespace
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove whitespace around lines
    text = "\n".join(
        line.strip()
        for line in text.splitlines()
    )

    return text.strip()
