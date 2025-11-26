"""Fabric AI integration module.

This module provides a clean interface to Fabric AI, separating
the Fabric-specific logic from the CLI implementation.

Functions:
    run_fabric: Execute Fabric AI commands with direct argument list
    run_fabric_capture: Execute Fabric and capture output
    check_fabric_available: Check if Fabric is installed
"""

import subprocess
from pathlib import Path

from fabric_second_brain.color import error
from fabric_second_brain.config import SBConfig
from fabric_second_brain.logger import logger


def check_fabric_available(cfg: SBConfig) -> bool:
    """Check if Fabric AI is available.

    Args:
        cfg: Application configuration

    Returns:
        True if Fabric is available, False otherwise
    """
    try:
        subprocess.run(
            [cfg.fabric_cmd, "--version"],
            capture_output=True,
            check=True,
            timeout=5,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False


def run_fabric(cfg: SBConfig, args: list[str]) -> int:
    """Execute Fabric command with arguments.

    This is a simpler version that directly calls Fabric with the given
    arguments and does not capture output.

    Args:
        cfg: Configuration instance containing fabric_cmd.
        args: List of arguments to pass to Fabric.

    Returns:
        Return code from Fabric command.
    """
    cmd = [cfg.fabric_cmd, *args]
    try:
        return subprocess.call(cmd)
    except FileNotFoundError:
        print(
            error(
                f"❌ '{cfg.fabric_cmd}' not found in PATH – "
                "bitte in der Config (fabric_cmd) anpassen"
            )
        )
        return 1


def run_fabric_capture(cfg: SBConfig, args: list[str]) -> tuple[int, str, str]:
    """Execute Fabric command and capture output.

    Args:
        cfg: Configuration instance containing fabric_cmd.
        args: List of arguments to pass to Fabric.

    Returns:
        Tuple of (return_code, stdout, stderr).
    """
    cmd = [cfg.fabric_cmd, *args]
    try:
        proc = subprocess.run(
            cmd,
            text=True,
            capture_output=True,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except FileNotFoundError:
        msg = f"❌ '{cfg.fabric_cmd}' not found in PATH – bitte in der Config (fabric_cmd) anpassen"
        print(error(msg))
        return 1, "", msg


def run_fabric_advanced(
    cfg: SBConfig,
    pattern: str,
    input_data: str | None = None,
    input_file: Path | None = None,
    model: str | None = None,
    vendor: str | None = None,
    youtube_url: str | None = None,
    pdf_file: Path | None = None,
) -> tuple[int, str, str]:
    """Execute a Fabric AI command with advanced options.

    Args:
        cfg: Application configuration
        pattern: Fabric pattern to use (e.g., 'summarize', 'extract_wisdom')
        input_data: Text input to process
        input_file: File to process
        model: Override model from config
        vendor: Override vendor from config
        youtube_url: YouTube URL to process
        pdf_file: PDF file to process

    Returns:
        Tuple of (return_code, stdout, stderr)

    Raises:
        ValueError: If no input source is provided
    """
    if not any([input_data, input_file, youtube_url, pdf_file]):
        raise ValueError("At least one input source must be provided")

    # Build command
    cmd = [cfg.fabric_cmd, "--pattern", pattern]

    # Add model/vendor overrides
    if model:
        cmd.extend(["--model", model])
    elif cfg.model:
        cmd.extend(["--model", cfg.model])

    if vendor:
        cmd.extend(["--vendor", vendor])
    elif cfg.vendor:
        cmd.extend(["--vendor", cfg.vendor])

    # Add input source
    if youtube_url:
        cmd.extend(["--youtube", youtube_url])
    elif pdf_file:
        cmd.extend(["--pdf", str(pdf_file)])
    elif input_file:
        cmd.extend([str(input_file)])

    logger.debug(f"Running Fabric command: {' '.join(cmd)}")

    try:
        if input_data:
            # Pipe stdin
            result = subprocess.run(
                cmd,
                input=input_data,
                text=True,
                capture_output=True,
                timeout=300,  # 5 minutes timeout
            )
        else:
            # No stdin
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
            )

        return result.returncode, result.stdout, result.stderr

    except subprocess.TimeoutExpired:
        error_msg = "Fabric command timed out after 5 minutes"
        logger.error(error_msg)
        return 1, "", error_msg
    except Exception as e:
        error_msg = f"Failed to run Fabric: {e}"
        logger.error(error_msg)
        return 1, "", error_msg
