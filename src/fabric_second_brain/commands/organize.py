"""Organize vault folders using AI.

This module provides the organize command to automatically structure
and organize vault folders using AI models.
"""

from __future__ import annotations

from pathlib import Path

from fabric_second_brain.color import info
from fabric_second_brain.config import SBConfig
from fabric_second_brain.fabric import run_fabric


def cmd_organize(cfg: SBConfig, path: str | None) -> int:
    """Organize vault folders using AI.

    Args:
        cfg: Configuration instance.
        path: Optional override for vault path.

    Returns:
        Return code from Fabric organize command.
    """
    vault = Path(path) if path else cfg.vault_path
    print(info(f"🗂️  Organizing vault {vault} (model={cfg.model}, vendor={cfg.vendor})"))
    return run_fabric(cfg, ["organize", str(vault)])
