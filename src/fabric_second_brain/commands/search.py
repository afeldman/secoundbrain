"""Semantic search in the vault.

This module provides the search command to perform semantic searches
across notes using AI models.
"""

from __future__ import annotations

from fabric_second_brain.color import info, magenta
from fabric_second_brain.config import SBConfig
from fabric_second_brain.fabric import run_fabric


def cmd_search(cfg: SBConfig, query: str) -> int:
    """Perform semantic search in the vault.

    Args:
        cfg: Configuration instance.
        query: Search query string.

    Returns:
        Return code from Fabric search command.
    """
    print(
        info("🔍 Semantic search: ")
        + magenta(query)
        + info(f" (model={cfg.model}, vendor={cfg.vendor})")
    )
    return run_fabric(cfg, ["search", query])
