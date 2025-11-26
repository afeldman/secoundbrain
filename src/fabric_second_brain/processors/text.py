"""Plain text and markdown file processing.

This module handles simple text file formats that can be read directly
without special processing.

Functions:
    extract_text: Read text from plain text or markdown files
"""

from pathlib import Path

from fabric_second_brain.logger import logger


def extract_text(file_path: Path) -> str:
    """Extract text from plain text or markdown files.

    Supports: TXT, MD

    Args:
        file_path: Path to the text file

    Returns:
        File contents as string

    Raises:
        RuntimeError: If file reading fails
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
        logger.debug(f"Read text file: {file_path}")
        return content
    except UnicodeDecodeError:
        # Try with latin-1 encoding as fallback
        with open(file_path, encoding="latin-1") as f:
            content = f.read()
        logger.debug(f"Read text file with latin-1 encoding: {file_path}")
        return content
