"""
Translator for second brain.

Purpose:
- Translate human-readable Markdown before indexing/storage
- Preserve Markdown structure exactly
- Preserve code blocks and identifiers
- No analysis, no interpretation, no summarization

English input (by errorbrain) is canonical.
Translation is a **presentation transformation only**.

Configuration:
- SECONDBRAIN_LANGUAGE (e.g. 'de', 'fr', 'original')
- SECONDBRAIN_TRANSLATOR (e.g. 'none', 'google', 'llm')
"""

from decouple import config

LANG = config("SECONDBRAIN_LANGUAGE", "original")
BACKEND = config("SECONDBRAIN_TRANSLATOR", "none").lower()


def translate_markdown(text: str) -> str:
    """
    Translate markdown text into the configured language.

    If SECONDBRAIN_LANGUAGE == "original", text is returned unchanged.
    """
    if LANG == "original" or BACKEND == "none":
        return text

    # TODO: implement support for selected backends
    raise NotImplementedError(
        f"Translator backend '{BACKEND}' not implemented"
    )
