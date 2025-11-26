"""PDF document processing.

This module provides functionality for extracting text from PDF files using
pdftotext (from poppler) with a fallback to pandoc.

Functions:
    extract_pdf: Extract text from a PDF file
"""

import shutil
import subprocess
from pathlib import Path

from fabric_second_brain.logger import logger
from fabric_second_brain.processors import pandoc


def extract_pdf(file_path: Path) -> str:
    """Extract text from a PDF file.

    Tries to use pdftotext first (from poppler), falls back to pandoc if unavailable.

    Args:
        file_path: Path to the PDF file

    Returns:
        Extracted text content

    Raises:
        RuntimeError: If text extraction fails
    """
    # Try pdftotext first (from poppler)
    if shutil.which("pdftotext"):
        try:
            result = subprocess.run(
                ["pdftotext", "-layout", str(file_path), "-"],
                capture_output=True,
                text=True,
                check=True,
            )
            logger.debug(f"Extracted PDF text using pdftotext: {file_path}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.warning(f"pdftotext failed, trying pandoc: {e}")
            return pandoc.extract_with_pandoc(file_path, ".pdf")
    else:
        logger.warning("pdftotext not found, using pandoc")
        return pandoc.extract_with_pandoc(file_path, ".pdf")
