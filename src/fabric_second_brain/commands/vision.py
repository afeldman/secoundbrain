"""Vision analysis on images using AI.

This module provides the vision command to analyze images using
AI vision models.
"""

from __future__ import annotations

from fabric_second_brain.color import info
from fabric_second_brain.config import SBConfig
from fabric_second_brain.fabric import run_fabric


def cmd_vision(cfg: SBConfig, image: str) -> int:
    """Perform vision analysis on an image.

    Args:
        cfg: Configuration instance.
        image: Path to image file.

    Returns:
        Return code from Fabric vision command.
    """
    print(info(f"🖼️  Vision analysis for {image} (model={cfg.model}, vendor={cfg.vendor})"))
    return run_fabric(cfg, ["vision", "analyze", image])
