"""Auto-classify notes in the vault using Fabric AI.

This module provides the classify command to automatically categorize
and organize notes using AI models.
"""

from __future__ import annotations

from pathlib import Path

from fabric_second_brain.color import info
from fabric_second_brain.config import SBConfig
from fabric_second_brain.fabric import run_fabric


def cmd_classify(cfg: SBConfig, path: str | None) -> int:
    """Auto-classify notes in the vault using Fabric AI.

    Args:
        cfg: Configuration instance.
        path: Optional override for vault path.

    Returns:
        Return code from Fabric classify command.
    """
    vault = Path(path) if path else cfg.vault_path
    print(info(f"📂 Auto-classifying notes in {vault} (model={cfg.model})"))
    return run_fabric(cfg, ["classify", "--path", str(vault)])
