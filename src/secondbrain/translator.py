
"""
Translator for secondbrain.

Purpose:
- Translate human-readable Markdown
- Preserve Markdown structure and code blocks
- Perform no analysis, no summarization, no interpretation

English input (errorbrain output) is canonical.
Translation is presentation only.
"""

from decouple import config

LANG = config("SECONDBRAIN_LANGUAGE", default="original")
BACKEND = config("SECONDBRAIN_TRANSLATOR", default="none").lower()

def translate_markdown(text: str) -> str:
    if LANG == "original" or BACKEND == "none":
        return text

    # Dummy implementation for demonstration
    if BACKEND in ("google", "llm"):
        return f"[Translated to {LANG} by {BACKEND} (demo)]\n" + text

    raise NotImplementedError(
        f"Translator backend '{BACKEND}' not implemented"
    )

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
