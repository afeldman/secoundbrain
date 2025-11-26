"""Document and media file processor for extracting content.

Supports various document formats (PDF, DOCX, XLSX, CSV, etc.) and
extracts text content for AI processing.
"""

from __future__ import annotations

import csv
import subprocess
from pathlib import Path
from typing import ClassVar

from .logger import logger


class DocumentProcessor:
    """Process various document formats and extract text content."""

    SUPPORTED_EXTENSIONS: ClassVar[set[str]] = {
        # Documents
        ".pdf",
        ".doc",
        ".docx",
        ".odt",
        ".rtf",
        ".txt",
        ".md",
        # Spreadsheets
        ".xls",
        ".xlsx",
        ".ods",
        ".csv",
        # Presentations
        ".ppt",
        ".pptx",
        ".odp",
        # PostScript
        ".ps",
        ".eps",
        # E-books
        ".epub",
        ".mobi",
    }

    def __init__(self) -> None:
        """Initialize the document processor."""
        self._check_dependencies()

    def _check_dependencies(self) -> None:
        """Check for optional external tools."""
        # Optional tools für bessere Konvertierung
        self.has_pandoc = self._check_command("pandoc")
        self.has_pdftotext = self._check_command("pdftotext")
        self.has_ps2txt = self._check_command("ps2txt")

        if not self.has_pandoc:
            logger.warning(
                "pandoc not found - limited document format support. "
                "Install with: brew install pandoc"
            )

    def _check_command(self, cmd: str) -> bool:
        """Check if a command exists in PATH."""
        try:
            subprocess.run(
                [cmd, "--version"],
                capture_output=True,
                check=False,
                timeout=2,
            )
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def is_supported(self, file_path: Path) -> bool:
        """Check if file format is supported.

        Args:
            file_path: Path to the file.

        Returns:
            True if format is supported.
        """
        return file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS

    def extract_text(self, file_path: Path) -> str:
        """Extract text from document.

        Args:
            file_path: Path to the document file.

        Returns:
            Extracted text content.

        Raises:
            ValueError: If file format is not supported.
            FileNotFoundError: If file does not exist.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if not self.is_supported(file_path):
            raise ValueError(
                f"Unsupported file format: {file_path.suffix}. "
                f"Supported: {', '.join(sorted(self.SUPPORTED_EXTENSIONS))}"
            )

        ext = file_path.suffix.lower()

        # Plain text files
        if ext in {".txt", ".md"}:
            return self._read_text_file(file_path)

        # CSV files
        if ext == ".csv":
            return self._extract_csv(file_path)

        # PDF files
        if ext == ".pdf":
            return self._extract_pdf(file_path)

        # PostScript files
        if ext in {".ps", ".eps"}:
            return self._extract_postscript(file_path)

        # Use pandoc for all other formats
        if self.has_pandoc:
            return self._extract_with_pandoc(file_path)

        raise ValueError(
            f"Cannot process {ext} - pandoc not available. Install with: brew install pandoc"
        )

    def _read_text_file(self, file_path: Path) -> str:
        """Read plain text file."""
        try:
            return file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Fallback to latin-1
            return file_path.read_text(encoding="latin-1")

    def _extract_csv(self, file_path: Path) -> str:
        """Extract text from CSV file."""
        lines = []
        try:
            with file_path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                for row in reader:
                    lines.append(" | ".join(row))
            return "\n".join(lines)
        except Exception as e:
            logger.warning(f"CSV parsing error: {e}")
            # Fallback to plain text
            return self._read_text_file(file_path)

    def _extract_pdf(self, file_path: Path) -> str:
        """Extract text from PDF."""
        # Try pdftotext first (better quality)
        if self.has_pdftotext:
            try:
                result = subprocess.run(
                    ["pdftotext", "-layout", str(file_path), "-"],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=30,
                )
                return result.stdout
            except subprocess.SubprocessError as e:
                logger.warning(f"pdftotext failed: {e}, trying pandoc")

        # Fallback to pandoc
        if self.has_pandoc:
            return self._extract_with_pandoc(file_path)

        raise ValueError(
            "PDF processing requires pdftotext or pandoc. Install with: brew install poppler pandoc"
        )

    def _extract_postscript(self, file_path: Path) -> str:
        """Extract text from PostScript files."""
        if self.has_ps2txt:
            try:
                result = subprocess.run(
                    ["ps2txt", str(file_path)],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=30,
                )
                return result.stdout
            except subprocess.SubprocessError as e:
                logger.warning(f"ps2txt failed: {e}")

        raise ValueError(
            "PostScript processing requires ps2txt (ghostscript). "
            "Install with: brew install ghostscript"
        )

    def _extract_with_pandoc(self, file_path: Path) -> str:
        """Extract text using pandoc."""
        try:
            result = subprocess.run(
                ["pandoc", str(file_path), "-t", "plain", "--wrap=none"],
                capture_output=True,
                text=True,
                check=True,
                timeout=60,
            )
            return result.stdout
        except subprocess.SubprocessError as e:
            raise ValueError(f"Pandoc conversion failed: {e}") from e


class MediaProcessor:
    """Process media files (audio, video) for transcription."""

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

    def __init__(self) -> None:
        """Initialize the media processor."""
        self._check_dependencies()

    def _check_dependencies(self) -> None:
        """Check for external tools."""
        self.has_ffmpeg = self._check_command("ffmpeg")

        if not self.has_ffmpeg:
            logger.warning(
                "ffmpeg not found - audio/video processing unavailable. "
                "Install with: brew install ffmpeg"
            )

    def _check_command(self, cmd: str) -> bool:
        """Check if a command exists in PATH."""
        try:
            subprocess.run(
                [cmd, "-version"],
                capture_output=True,
                check=False,
                timeout=2,
            )
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def is_supported(self, file_path: Path) -> bool:
        """Check if media format is supported.

        Args:
            file_path: Path to the file.

        Returns:
            True if format is supported.
        """
        return file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS

    def extract_audio(self, file_path: Path, output_path: Path | None = None) -> Path:
        """Extract audio from media file.

        Args:
            file_path: Path to media file.
            output_path: Optional output path for audio file.

        Returns:
            Path to extracted audio file (WAV format).

        Raises:
            ValueError: If ffmpeg is not available.
            FileNotFoundError: If file does not exist.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if not self.has_ffmpeg:
            raise ValueError("Audio extraction requires ffmpeg. Install with: brew install ffmpeg")

        if output_path is None:
            output_path = file_path.with_suffix(".wav")

        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    str(file_path),
                    "-ar",
                    "16000",  # 16kHz sample rate
                    "-ac",
                    "1",  # mono
                    "-y",  # overwrite
                    str(output_path),
                ],
                capture_output=True,
                check=True,
                timeout=300,  # 5 minutes max
            )
            logger.info(f"Audio extracted to: {output_path}")
            return output_path
        except subprocess.SubprocessError as e:
            raise ValueError(f"Audio extraction failed: {e}") from e

    def get_duration(self, file_path: Path) -> float:
        """Get duration of media file in seconds.

        Args:
            file_path: Path to media file.

        Returns:
            Duration in seconds.
        """
        if not self.has_ffmpeg:
            return 0.0

        try:
            result = subprocess.run(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "default=noprint_wrappers=1:nokey=1",
                    str(file_path),
                ],
                capture_output=True,
                text=True,
                check=True,
                timeout=10,
            )
            return float(result.stdout.strip())
        except (subprocess.SubprocessError, ValueError):
            return 0.0
