"""Configuration management commands.

This module provides commands to view and modify the Second Brain
configuration settings.
"""

from __future__ import annotations

from pathlib import Path

from fabric_second_brain.color import info, success
from fabric_second_brain.config import SBConfig, save_config


def cmd_config_show(cfg: SBConfig) -> int:
    """Display current configuration.

    Args:
        cfg: Configuration instance to display.

    Returns:
        Always returns 0 (success).
    """
    print(success("Current Second Brain configuration:\n"))
    print(f"{info('model:       ')} {cfg.model}")
    print(f"{info('vault_path:  ')} {cfg.vault_path}")
    print(f"{info('vendor:      ')} {cfg.vendor}")
    print(f"{info('fabric_cmd:  ')} {cfg.fabric_cmd}")
    return 0


def cmd_config_set_model(cfg: SBConfig, model: str) -> int:
    """Set the default AI model in configuration.

    Args:
        cfg: Configuration instance to update.
        model: Model name to set.

    Returns:
        Always returns 0 (success).
    """
    cfg.model = model
    save_config(cfg)
    print(success(f"✅ model set to: {model}"))
    return 0


def cmd_config_set_vault(cfg: SBConfig, vault: str) -> int:
    """Set the Obsidian vault path in configuration.

    Args:
        cfg: Configuration instance to update.
        vault: Path to Obsidian vault.

    Returns:
        Always returns 0 (success).
    """
    cfg.vault_path = Path(vault).expanduser()
    save_config(cfg)
    print(success(f"✅ vault_path set to: {cfg.vault_path}"))
    return 0


def cmd_config_set_fabric(cfg: SBConfig, fabric_cmd: str) -> int:
    """Set the Fabric command in configuration.

    Args:
        cfg: Configuration instance to update.
        fabric_cmd: Fabric command name or path.

    Returns:
        Always returns 0 (success).
    """
    cfg.fabric_cmd = fabric_cmd
    save_config(cfg)
    print(success(f"✅ fabric_cmd set to: {fabric_cmd}"))
    return 0
