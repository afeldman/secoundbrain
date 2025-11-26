"""Initialize Second Brain vault structure.

This module provides the init command to set up a new Second Brain vault
with proper directory structure and templates.
"""

from __future__ import annotations

from pathlib import Path

from fabric_second_brain.color import info, magenta, success
from fabric_second_brain.config import SBConfig, get_template_dir, save_config


def cmd_init(cfg: SBConfig) -> int:
    """Initialize Second Brain vault structure.

    Prompts for vault path, creates necessary directories, copies templates,
    and creates a README file.

    Args:
        cfg: Configuration instance to update.

    Returns:
        Always returns 0 (success).
    """
    print(info("🧠 Second-Brain Init"))
    print("-----------------------------------")
    print(info(f"Aktueller Vault-Pfad in der Config: {magenta(str(cfg.vault_path))}"))
    new_path = input("Neuer Vault-Pfad (leer lassen für aktuellen Wert): ").strip()

    if new_path:
        vault = Path(new_path).expanduser()
        cfg.vault_path = vault
        save_config(cfg)
        print(success(f"✅ vault_path in der Config aktualisiert: {vault}"))
    else:
        vault = cfg.vault_path.expanduser()
        print(info(f"➡️  Verwende bestehenden Vault-Pfad: {vault}"))

    print(info(f"🚀 Initializing Second Brain at: {vault}"))

    # 1. Vault erstellen
    vault.mkdir(parents=True, exist_ok=True)

    # 2. Standardverzeichnisse
    folders = [
        "Wisdom",
        "Daily",
        "Inbox",
        "Literature",
        "Media",
        "Templates",
    ]

    for f in folders:
        (vault / f).mkdir(parents=True, exist_ok=True)

    # 3. Templates kopieren
    template_src = get_template_dir()
    template_dst = vault / "Templates"

    copied = 0
    for tpl in template_src.iterdir():
        if tpl.is_file() and tpl.suffix == ".md":
            target = template_dst / tpl.name
            if not target.exists():
                target.write_text(tpl.read_text(encoding="utf-8"), encoding="utf-8")
                copied += 1

    # 4. README
    readme = vault / "README.md"
    if not readme.exists():
        readme.write_text(
            (
                "# Second Brain Vault\n\n"
                "Dies ist dein persönliches Second Brain, bereit für "
                "## Struktur\n"
                "- Wisdom/ — extrahiertes Wissen aus Quellen (PDF, YouTube, Webseiten)\n"
                "- Literature/ — Buchnotizen, Paper, Dokumente\n"
                "- Media/ — Audio- und Videodateien, Musik\n"
                "- Inbox/ — Rohnotizen, unfertig\n"
                "- Daily/ — tägliche Logbücher, Journals\n"
                "- Templates/ — Markdown-Templates für Auto-Generierung\n\n"
                "- Templates/ — Markdown-Templates für Auto-Generierung\n\n"
                "Erstellt von **fabric-second-brain**.\n"
            ),
            encoding="utf-8",
        )

    print(success("🎉 Second-Brain Vault initialized!"))
    print(success(f"📁 Path: {vault}"))
    print(success(f"📄 Copied templates: {copied}"))
    return 0
