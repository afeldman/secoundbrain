"""Microsoft Office and OpenOffice document processing.

This module handles text extraction from Microsoft Office formats (DOCX, XLSX, PPTX)
and OpenOffice formats (ODT, ODS, ODP) using pandoc.

Functions:
    extract_office: Extract text from Microsoft Office documents
    extract_openoffice: Extract text from OpenOffice documents
"""

from pathlib import Path

from fabric_second_brain.processors import pandoc


def extract_office(file_path: Path, ext: str) -> str:
    """Extract text from Microsoft Office documents.

    Supports: DOC, DOCX, XLS, XLSX, PPT, PPTX

    Args:
        file_path: Path to the Office document
        ext: File extension (e.g., '.docx')

    Returns:
        Extracted text content

    Raises:
        RuntimeError: If pandoc is not available or extraction fails
    """
    return pandoc.extract_with_pandoc(file_path, ext)


def extract_openoffice(file_path: Path, ext: str) -> str:
    """Extract text from OpenOffice documents.

    Supports: ODT, ODS, ODP

    Args:
        file_path: Path to the OpenOffice document
        ext: File extension (e.g., '.odt')

    Returns:
        Extracted text content

    Raises:
        RuntimeError: If pandoc is not available or extraction fails
    """
    return pandoc.extract_with_pandoc(file_path, ext)
