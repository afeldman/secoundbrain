"""Audio and video file processing.

This module provides functionality for working with media files, including
extracting audio from video files and detecting media duration using ffmpeg/ffprobe.

Functions:
    extract_audio: Extract audio track from video files
    get_duration: Get the duration of a media file
"""

import shutil
import subprocess
from pathlib import Path

from fabric_second_brain.logger import logger


def extract_audio(video_path: Path, output_path: Path) -> None:
    """Extract audio from a video file using ffmpeg.

    Args:
        video_path: Path to the input video file
        output_path: Path where the extracted audio should be saved

    Raises:
        RuntimeError: If ffmpeg is not available or extraction fails
    """
    if not shutil.which("ffmpeg"):
        raise RuntimeError(
            "ffmpeg not found. Please install ffmpeg to extract audio from videos. "
            "See INSTALL.md for instructions."
        )

    try:
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                str(video_path),
                "-vn",  # No video
                "-acodec",
                "libmp3lame",  # MP3 codec
                "-q:a",
                "2",  # Quality
                str(output_path),
            ],
            check=True,
            capture_output=True,
        )
        logger.debug(f"Extracted audio from {video_path} to {output_path}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to extract audio: {e}") from e


def get_duration(media_path: Path) -> float:
    """Get the duration of a media file in seconds.

    Args:
        media_path: Path to the media file

    Returns:
        Duration in seconds

    Raises:
        RuntimeError: If ffprobe is not available or duration detection fails
    """
    if not shutil.which("ffprobe"):
        raise RuntimeError(
            "ffprobe not found. Please install ffmpeg to detect media duration. "
            "See INSTALL.md for instructions."
        )

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
                str(media_path),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        duration = float(result.stdout.strip())
        logger.debug(f"Media duration: {duration}s for {media_path}")
        return duration
    except (subprocess.CalledProcessError, ValueError) as e:
        raise RuntimeError(f"Failed to get media duration: {e}") from e
