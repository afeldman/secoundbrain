"""Base classes and main orchestration for document and media processing.

This module provides the main DocumentProcessor and MediaProcessor classes that
coordinate the various format-specific processors.

Classes:
    DocumentProcessor: Extracts text from various document formats
    MediaProcessor: Handles audio and video file processing
"""

from pathlib import Path
from typing import ClassVar

from fabric_second_brain.processors import (
    csv_processor,
    media,
    office,
    pandoc,
    pdf,
    postscript,
    text,
)


class DocumentProcessor:
    """Extracts text content from various document formats.

    This class provides a unified interface for extracting text from different
    document formats by delegating to format-specific processors.

    Attributes:
        SUPPORTED_EXTENSIONS: Set of supported file extensions
    """

    SUPPORTED_EXTENSIONS: ClassVar[set[str]] = {
        # PDF
        ".pdf",
        # Microsoft Office
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        # OpenOffice
        ".odt",
        ".ods",
        ".odp",
        # Text
        ".txt",
        ".md",
        ".csv",
        # PostScript
        ".ps",
        ".eps",
        # E-books
        ".epub",
        ".mobi",
        ".rtf",
    }

    @staticmethod
    def is_supported(file_path: Path) -> bool:
        """Check if a file format is supported.

        Args:
            file_path: Path to the file to check

        Returns:
            True if the file extension is supported, False otherwise
        """
        return file_path.suffix.lower() in DocumentProcessor.SUPPORTED_EXTENSIONS

    @staticmethod
    def extract_text(file_path: Path) -> str:
        """Extract text content from a document.

        Args:
            file_path: Path to the document file

        Returns:
            Extracted text content

        Raises:
            ValueError: If the file format is not supported
            RuntimeError: If text extraction fails
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = file_path.suffix.lower()

        # Route to appropriate processor
        if ext == ".pdf":
            return pdf.extract_pdf(file_path)
        elif ext in {".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"}:
            return office.extract_office(file_path, ext)
        elif ext in {".odt", ".ods", ".odp"}:
            return office.extract_openoffice(file_path, ext)
        elif ext == ".csv":
            return csv_processor.extract_csv(file_path)
        elif ext in {".ps", ".eps"}:
            return postscript.extract_postscript(file_path)
        elif ext in {".txt", ".md"}:
            return text.extract_text(file_path)
        elif ext in {".epub", ".mobi", ".rtf"}:
            return pandoc.extract_with_pandoc(file_path, ext)
        else:
            raise ValueError(f"Unsupported file format: {ext}")


class MediaProcessor:
    """Handles audio and video file processing.

    This class provides functionality for extracting audio from video files
    and getting media duration information.

    Attributes:
        SUPPORTED_EXTENSIONS: Set of supported media file extensions
    """

    SUPPORTED_EXTENSIONS: ClassVar[set[str]] = {
        # Audio
        ".mp3",
        ".wav",
        ".m4a",
        ".flac",
        ".ogg",
        ".aac",
        # Video
        ".mp4",
        ".avi",
        ".mov",
        ".mkv",
        ".webm",
        ".flv",
    }

    @staticmethod
    def is_supported(file_path: Path) -> bool:
        """Check if a media format is supported.

        Args:
            file_path: Path to the media file to check

        Returns:
            True if the file extension is supported, False otherwise
        """
        return file_path.suffix.lower() in MediaProcessor.SUPPORTED_EXTENSIONS

    @staticmethod
    def extract_audio(video_path: Path, output_path: Path) -> None:
        """Extract audio from a video file using ffmpeg.

        Args:
            video_path: Path to the input video file
            output_path: Path where the extracted audio should be saved

        Raises:
            RuntimeError: If ffmpeg is not available or extraction fails
        """
        return media.extract_audio(video_path, output_path)

    @staticmethod
    def get_duration(media_path: Path) -> float:
        """Get the duration of a media file in seconds.

        Args:
            media_path: Path to the media file

        Returns:
            Duration in seconds

        Raises:
            RuntimeError: If ffprobe is not available or duration detection fails
        """
        return media.get_duration(media_path)
