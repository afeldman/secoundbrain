# ENTRY POINT: external Markdown ingestion

from secondbrain.fabric_adapter import apply_fabric_patterns
from secondbrain.translator import translate_markdown

from pathlib import Path

# Example function for reading markdown

def read_markdown(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# Main ingest function

def ingest_markdown(path: Path):
    content = read_markdown(path)
    content = apply_fabric_patterns(content)
    content = translate_markdown(content)
    # continue with normalization, indexing, storage
    return content
