"""CSV file processing.

This module handles CSV file parsing and converts tabular data into
a readable text format with pipe-separated columns.

Functions:
    extract_csv: Extract and format text from CSV files
"""

import csv
from pathlib import Path

from fabric_second_brain.logger import logger


def extract_csv(file_path: Path) -> str:
    """Extract text from CSV files.

    Converts CSV data into pipe-separated text format for better readability.

    Args:
        file_path: Path to the CSV file

    Returns:
        Formatted text representation of the CSV data

    Raises:
        RuntimeError: If CSV reading fails
    """
    try:
        with open(file_path, encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            rows = list(reader)

        if not rows:
            return ""

        # Convert to pipe-separated text
        lines = [" | ".join(row) for row in rows]
        logger.debug(f"Extracted CSV with {len(lines)} rows: {file_path}")
        return "\n".join(lines)
    except UnicodeDecodeError:
        # Try with latin-1 encoding as fallback
        with open(file_path, encoding="latin-1", newline="") as f:
            reader = csv.reader(f)
            rows = list(reader)

        if not rows:
            return ""

        lines = [" | ".join(row) for row in rows]
        logger.debug(f"Extracted CSV with latin-1 encoding: {file_path}")
        return "\n".join(lines)
