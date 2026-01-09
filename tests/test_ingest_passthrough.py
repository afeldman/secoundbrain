from secondbrain.translator import translate_markdown

def test_translation_passthrough():
    text = "# Title\n\n```python\nprint('hi')\n```"
    assert translate_markdown(text) == text
