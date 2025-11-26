"""Summarize files using AI.

This module provides the summary command to generate AI-powered
summaries of documents and files.
"""

from __future__ import annotations

from fabric_second_brain.color import info
from fabric_second_brain.config import SBConfig
from fabric_second_brain.fabric import run_fabric


def cmd_summary(cfg: SBConfig, file: str) -> int:
    """Summarize a file using AI.

    Args:
        cfg: Configuration instance.
        file: Path to file to summarize.

    Returns:
        Return code from Fabric summarize command.
    """
    print(info(f"📝 Summarizing {file} (model={cfg.model}, vendor={cfg.vendor})"))
    return run_fabric(cfg, ["summarize", file])
