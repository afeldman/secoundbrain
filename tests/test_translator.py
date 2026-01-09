import os
import pytest
from fabric_second_brain.translator import translate_markdown

def test_translation_passthrough_no_env_vars():
    """
    Test that translate_markdown returns the input unchanged when no
    translation-related environment variables are set.
    """
    # Ensure env vars are not set
    if "SECONDBRAIN_LANGUAGE" in os.environ:
        del os.environ["SECONDBRAIN_LANGUAGE"]
    if "SECONDBRAIN_TRANSLATOR" in os.environ:
        del os.environ["SECONDBRAIN_TRANSLATOR"]

    text = "# Title\n\n```python\nprint('hi')\n```\n\nSome **bold** text."
    assert translate_markdown(text) == text

def test_translation_passthrough_language_original():
    """
    Test that translate_markdown returns the input unchanged when
    SECONDBRAIN_LANGUAGE is set to 'original'.
    """
    os.environ["SECONDBRAIN_LANGUAGE"] = "original"
    os.environ["SECONDBRAIN_TRANSLATOR"] = "google" # Can be anything as language is original
    text = "# Title\n\n```python\nprint('hi')\n```\n\nSome **bold** text."
    assert translate_markdown(text) == text
    del os.environ["SECONDBRAIN_LANGUAGE"]
    del os.environ["SECONDBRAIN_TRANSLATOR"]

def test_translation_passthrough_translator_none():
    """
    Test that translate_markdown returns the input unchanged when
    SECONDBRAIN_TRANSLATOR is set to 'none'.
    """
    os.environ["SECONDBRAIN_LANGUAGE"] = "de" # Can be anything as translator is none
    os.environ["SECONDBRAIN_TRANSLATOR"] = "none"
    text = "# Title\n\n```python\nprint('hi')\n```\n\nSome **bold** text."
    assert translate_markdown(text) == text
    del os.environ["SECONDBRAIN_LANGUAGE"]
    del os.environ["SECONDBRAIN_TRANSLATOR"]

def test_unimplemented_translator_raises_error():
    """
    Test that translate_markdown raises NotImplementedError for
    unimplemented backends.
    """
    os.environ["SECONDBRAIN_LANGUAGE"] = "de"
    os.environ["SECONDBRAIN_TRANSLATOR"] = "google"
    text = "# Title\n\n```python\nprint('hi')\n```"
    with pytest.raises(NotImplementedError) as excinfo:
        translate_markdown(text)
    assert "Google Translate backend is not yet implemented." in str(excinfo.value)
    del os.environ["SECONDBRAIN_LANGUAGE"]
    del os.environ["SECONDBRAIN_TRANSLATOR"]

    os.environ["SECONDBRAIN_LANGUAGE"] = "fr"
    os.environ["SECONDBRAIN_TRANSLATOR"] = "llm"
    with pytest.raises(NotImplementedError) as excinfo:
        translate_markdown(text)
    assert "LLM backend is not yet implemented." in str(excinfo.value)
    del os.environ["SECONDBRAIN_LANGUAGE"]
    del os.environ["SECONDBRAIN_TRANSLATOR"]
