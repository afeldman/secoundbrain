"""Document and media processing submodule.

This submodule provides processors for extracting text and metadata from various
document and media formats. Each format family has its own processor module for
better organization and maintainability.

Modules:
    pdf: PDF document processing
    office: Microsoft Office format processing (DOCX, XLSX, PPTX)
    text: Plain text and markdown processing
    csv: CSV file processing
    postscript: PostScript file processing
    pandoc: Universal document converter using pandoc
    media: Audio and video file processing
    base: Base classes and utilities

Public API:
    DocumentProcessor: Main class for document text extraction
    MediaProcessor: Main class for media file processing
"""

from fabric_second_brain.processors.base import DocumentProcessor, MediaProcessor

__all__ = ["DocumentProcessor", "MediaProcessor"]
