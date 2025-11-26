"""Logger configuration for Fabric Second Brain.

Provides a configured loguru logger with rotating file logs and
conditional stderr output.
"""

from __future__ import annotations

from pathlib import Path

from loguru import logger
from platformdirs import PlatformDirs

from .config import APP_AUTHOR, APP_NAME


def _init_logger() -> None:
    """Initialize the loguru logger with file rotation and stderr output.

    Configures:
    - File logging with 10MB rotation and 10 file retention
    - Compressed archived logs (zip)
    - Thread/process-safe logging
    - INFO level for file, WARNING level for stderr
    """
    # Basis-Logger resetten (falls uv / Tools mehrfach importieren)
    logger.remove()

    dirs = PlatformDirs(APP_NAME, APP_AUTHOR)
    log_dir = Path(dirs.user_state_dir) / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "second-brain.log"

    # Rotierende Logs:
    logger.add(
        log_file,
        rotation="10 MB",  # rotiert ab 10 MB
        retention=10,  # 10 Logfiles behalten
        compression="zip",  # alte Logs zippen
        enqueue=True,  # thread-/prozesssicher
        backtrace=True,  # schöne Tracebacks
        diagnose=False,  # Diagnose aus (kürzere Traces)
        level="INFO",
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
    )

    # Optional: zusätzlich auf STDERR loggen
    logger.add(
        sink=lambda msg: print(msg, end=""),
        level="WARNING",
    )


# Beim Import initialisieren
_init_logger()


__all__ = ["logger"]
