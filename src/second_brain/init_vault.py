#!/usr/bin/env python3
"""
Initialisiert die PARA-Struktur im Obsidian Vault.
"""
import os
import sys
from pathlib import Path


def create_para_structure(vault_path: Path, dry_run: bool = False):
    """Erstellt die PARA-Ordnerstruktur."""
    
    folders = [
        "01_Projects",
        "02_Areas", 
        "03_Resources",
        "04_Archive",
    ]
    
    print(f"📁 Vault: {vault_path}")
    print(f"{'🔍 DRY RUN - ' if dry_run else ''}Erstelle PARA-Struktur...\n")
    
    for folder in folders:
        folder_path = vault_path / folder
        
        if folder_path.exists():
            print(f"✓ {folder} existiert bereits")
        else:
            if not dry_run:
                folder_path.mkdir(parents=True, exist_ok=True)
            print(f"{'[DRY] ' if dry_run else '✓ '}{folder} erstellt")
    
    # .gitkeep Dateien erstellen (damit leere Ordner in Git bleiben)
    if not dry_run:
        for folder in folders:
            gitkeep = vault_path / folder / ".gitkeep"
            if not gitkeep.exists():
                gitkeep.touch()
    
    print("\n✅ PARA-Struktur initialisiert!")
    print("\nNächste Schritte:")
    print("  1. Verschiebe Projekt-Ordner nach 01_Projects/")
    print("  2. Organisiere bestehende Notizen mit: ./bootstrap-secondbrain.sh")
    print("  3. Oder manuell mit: python3 organize.py move --rules rules/categorize.yaml")


def show_migration_info(vault_path: Path):
    """Zeigt Info über bestehende Inhalte."""
    
    # Zähle existierende Ordner und Files
    dirs = [d for d in vault_path.iterdir() 
            if d.is_dir() and not d.name.startswith('.')]
    
    md_files = list(vault_path.glob("*.md"))
    
    print("\n📊 Bestehende Inhalte:")
    print(f"   Ordner: {len(dirs)}")
    print(f"   Markdown-Dateien (root): {len(md_files)}")
    
    if dirs:
        print("\n📂 Ordner (werden nicht automatisch verschoben):")
        for d in sorted(dirs)[:10]:  # Zeige max. 10
            print(f"   - {d.name}")
        if len(dirs) > 10:
            print(f"   ... und {len(dirs) - 10} weitere")
    
    if md_files:
        print("\n📝 Markdown-Dateien im Root:")
        for f in sorted(md_files)[:5]:
            print(f"   - {f.name}")
        if len(md_files) > 5:
            print(f"   ... und {len(md_files) - 5} weitere")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Initialisiert PARA-Struktur im Obsidian Vault"
    )
    parser.add_argument(
        "--vault",
        type=str,
        help="Pfad zum Vault (default: $OBSIDIAN_VAULT oder ~/Obsidian)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Zeige nur was gemacht würde, ohne Änderungen"
    )
    parser.add_argument(
        "--info",
        action="store_true", 
        help="Zeige Info über bestehende Inhalte"
    )
    
    args = parser.parse_args()
    
    # Vault-Pfad ermitteln
    vault_path = args.vault or os.environ.get("OBSIDIAN_VAULT", "~/Obsidian")
    vault_path = Path(vault_path).expanduser().resolve()
    
    if not vault_path.exists():
        print(f"❌ Vault nicht gefunden: {vault_path}")
        print("\nBitte erstelle den Vault oder setze OBSIDIAN_VAULT:")
        print("  export OBSIDIAN_VAULT=/pfad/zu/deinem/vault")
        sys.exit(1)
    
    if args.info:
        show_migration_info(vault_path)
    else:
        create_para_structure(vault_path, dry_run=args.dry_run)
        
        if not args.dry_run:
            print("\n💡 Tipp: Nutze --info um bestehende Inhalte anzuzeigen")


if __name__ == "__main__":
    main()
