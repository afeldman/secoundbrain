"""Universal document converter using pandoc.

This module provides a fallback text extraction method using pandoc,
which supports a wide variety of document formats.

Functions:
    extract_with_pandoc: Extract text using pandoc as a universal converter
"""

import shutil
import subprocess
from pathlib import Path

from fabric_second_brain.logger import logger


def extract_with_pandoc(file_path: Path, ext: str) -> str:
    """Extract text using pandoc as a universal converter.

    Pandoc supports many formats including: DOCX, ODT, EPUB, RTF, and many more.

    Args:
        file_path: Path to the document
        ext: File extension (used for logging)

    Returns:
        Extracted text content

    Raises:
        RuntimeError: If pandoc is not available or extraction fails
    """
    if not shutil.which("pandoc"):
        raise RuntimeError(
            f"pandoc not found. Please install pandoc to process {ext} files. "
            "See INSTALL.md for instructions."
        )

    try:
        result = subprocess.run(
            ["pandoc", "-t", "plain", str(file_path)],
            capture_output=True,
            text=True,
            check=True,
        )
        logger.debug(f"Extracted {ext} text using pandoc: {file_path}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to extract text with pandoc: {e}") from e
