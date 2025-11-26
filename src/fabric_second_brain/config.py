"""Configuration management for Fabric Second Brain.

Handles loading, saving, and managing application configuration using TOML format.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import tomlkit
from platformdirs import PlatformDirs

APP_NAME = "fabric_second_brain"
APP_AUTHOR = "Anton Feldmann"


@dataclass
class SBConfig:
    """Configuration dataclass for Second Brain settings.

    Attributes:
        model: Name of the AI model to use.
        vault_path: Path to the Obsidian vault directory.
        vendor: AI vendor/provider (e.g., 'lmstudio', 'ollama').
        fabric_cmd: Command to invoke Fabric CLI.
    """

    model: str = "smollm3-3b-mlx"
    vault_path: Path = Path.home() / "Obsidian"
    vendor: str = "lmstudio"  # oder "ollama" etc.
    fabric_cmd: str = "fabric"  # z.B. "fabric", "fabric-ai"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SBConfig:
        """Create SBConfig instance from dictionary.

        Args:
            data: Dictionary containing configuration values.

        Returns:
            New SBConfig instance with values from dictionary.
        """
        return cls(
            model=data.get("model", cls.model),
            vault_path=Path(data.get("vault_path", str(cls().vault_path))).expanduser(),
            vendor=data.get("vendor", cls.vendor),
            fabric_cmd=data.get("fabric_cmd", cls.fabric_cmd),
        )

    def to_toml_document(self) -> tomlkit.TOMLDocument:
        """Convert configuration to TOML document.

        Returns:
            TOMLDocument containing all configuration values.
        """
        doc = tomlkit.document()
        doc.add(tomlkit.key("model"), self.model)  # type: ignore[arg-type]
        doc.add(tomlkit.key("vault_path"), str(self.vault_path))  # type: ignore[arg-type]
        doc.add(tomlkit.key("vendor"), self.vendor)  # type: ignore[arg-type]
        doc.add(tomlkit.key("fabric_cmd"), self.fabric_cmd)  # type: ignore[arg-type]
        return doc


def get_config_path() -> Path:
    """Get the path to the configuration file.

    Creates the configuration directory if it doesn't exist.

    Returns:
        Path to the config.toml file in the user's config directory.
    """
    dirs = PlatformDirs(APP_NAME, APP_AUTHOR)
    config_dir = Path(dirs.user_config_dir)
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.toml"


def load_config() -> SBConfig:
    """Load configuration from file or create default.

    If the configuration file doesn't exist, creates a new one with
    default values.

    Returns:
        Loaded or newly created SBConfig instance.
    """
    path = get_config_path()
    if not path.exists():
        cfg = SBConfig()
        save_config(cfg)
        return cfg

    text = path.read_text(encoding="utf-8")
    data = tomlkit.parse(text)
    return SBConfig.from_dict(dict(data))


def get_template_dir() -> Path:
    """Get the directory for Markdown templates.

    Creates the templates directory if it doesn't exist.
    Example path: ~/.config/fabric_second_brain/markdown_templates

    Returns:
        Path to the markdown templates directory.
    """
    dirs = PlatformDirs(APP_NAME, APP_AUTHOR)
    config_dir = Path(dirs.user_config_dir)
    templates_dir = config_dir / "markdown_templates"
    templates_dir.mkdir(parents=True, exist_ok=True)
    return templates_dir


def save_config(cfg: SBConfig) -> None:
    """Save configuration to file.

    Args:
        cfg: Configuration instance to save.
    """
    path = get_config_path()
    doc = cfg.to_toml_document()
    path.write_text(tomlkit.dumps(doc), encoding="utf-8")
