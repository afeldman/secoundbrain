"""PostScript file processing.

This module handles text extraction from PostScript and EPS files using
ps2txt (from ghostscript) with a fallback to pandoc.

Functions:
    extract_postscript: Extract text from PostScript files
"""

import shutil
import subprocess
from pathlib import Path

from fabric_second_brain.logger import logger
from fabric_second_brain.processors import pandoc


def extract_postscript(file_path: Path) -> str:
    """Extract text from PostScript files.

    Tries to use ps2txt first (from ghostscript), falls back to pandoc if unavailable.

    Supports: PS, EPS

    Args:
        file_path: Path to the PostScript file

    Returns:
        Extracted text content

    Raises:
        RuntimeError: If text extraction fails
    """
    # Try ps2txt first (from ghostscript)
    if shutil.which("ps2txt"):
        try:
            result = subprocess.run(
                ["ps2txt", str(file_path)], capture_output=True, text=True, check=True
            )
            logger.debug(f"Extracted PS text using ps2txt: {file_path}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.warning(f"ps2txt failed, trying pandoc: {e}")
            return pandoc.extract_with_pandoc(file_path, file_path.suffix)
    else:
        logger.warning("ps2txt not found, using pandoc")
        return pandoc.extract_with_pandoc(file_path, file_path.suffix)
