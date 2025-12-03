#!/usr/bin/env python3
"""
Räumt den Vault auf:
- Zeigt alte Ordner im Root an, die in PARA verschoben werden sollten
- Optional: Verschiebt sie automatisch
"""
import os
import sys
import shutil
from pathlib import Path


def get_vault_path():
    """Ermittelt den Vault-Pfad."""
    vault = os.environ.get("OBSIDIAN_VAULT", "~/Obsidian")
    return Path(vault).expanduser().resolve()


def find_old_folders(vault_path: Path):
    """Findet Ordner im Root, die nicht zur PARA-Struktur gehören."""
    
    # PARA-Ordner und System-Ordner
    skip_folders = {
        "01_Projects", "02_Areas", "03_Resources", "04_Archive",
        ".obsidian", ".trash", ".git", ".smart-env"
    }
    
    old_folders = []
    
    for item in vault_path.iterdir():
        if item.is_dir() and item.name not in skip_folders:
            old_folders.append(item)
    
    return sorted(old_folders, key=lambda x: x.name)


def suggest_para_location(folder_name: str) -> str:
    """Schlägt eine PARA-Kategorie basierend auf dem Namen vor."""
    
    name_lower = folder_name.lower()
    
    # Projekt-Keywords
    project_keywords = [
        "project", "app", "tool", "updater", "generator", 
        "validator", "sync", "playground", "template"
    ]
    
    # Resource-Keywords
    resource_keywords = [
        "whitepaper", "dokumente", "dokumentation", "report", 
        "research", "paper", "decision"
    ]
    
    # Area-Keywords
    area_keywords = [
        "infrastructure", "iac", "configuration", "batch", "acc"
    ]
    
    for keyword in project_keywords:
        if keyword in name_lower:
            return "01_Projects"
    
    for keyword in resource_keywords:
        if keyword in name_lower:
            return "03_Resources"
    
    for keyword in area_keywords:
        if keyword in name_lower:
            return "02_Areas"
    
    # Default: Projects (meistens sind es aktive Projekte)
    return "01_Projects"


def show_analysis(vault_path: Path, old_folders: list):
    """Zeigt Analyse der alten Ordner."""
    
    print(f"\n📊 Vault-Analyse: {vault_path}")
    print(f"\n🗂  Gefundene Ordner außerhalb der PARA-Struktur: {len(old_folders)}\n")
    
    if not old_folders:
        print("✅ Alle Ordner sind bereits in der PARA-Struktur!")
        return
    
    suggestions = {}
    for folder in old_folders:
        suggested = suggest_para_location(folder.name)
        if suggested not in suggestions:
            suggestions[suggested] = []
        suggestions[suggested].append(folder)
    
    for para_folder in ["01_Projects", "02_Areas", "03_Resources", "04_Archive"]:
        if para_folder in suggestions:
            folders = suggestions[para_folder]
            print(f"\n📁 {para_folder}/ ({len(folders)} Ordner):")
            for folder in folders:
                # Zähle Dateien
                md_files = list(folder.rglob("*.md"))
                print(f"   → {folder.name:40} ({len(md_files)} .md Dateien)")


def move_folders(vault_path: Path, old_folders: list, dry_run: bool = True):
    """Verschiebt Ordner in die PARA-Struktur."""
    
    print(f"\n{'🔍 DRY RUN - ' if dry_run else '📦 '}Verschiebe Ordner...\n")
    
    moved = 0
    for folder in old_folders:
        suggested = suggest_para_location(folder.name)
        target_dir = vault_path / suggested
        target_path = target_dir / folder.name
        
        if target_path.exists():
            print(f"⚠️  Überspringe {folder.name} - existiert bereits in {suggested}")
            continue
        
        if dry_run:
            print(f"[DRY] {folder.name} → {suggested}/")
        else:
            try:
                shutil.move(str(folder), str(target_path))
                print(f"✅ {folder.name} → {suggested}/")
                moved += 1
            except Exception as e:
                print(f"❌ Fehler bei {folder.name}: {e}")
    
    if dry_run:
        print(f"\n💡 Nutze --move um die Ordner tatsächlich zu verschieben")
    else:
        print(f"\n✅ {moved} Ordner erfolgreich verschoben!")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Vault Cleanup - Alte Ordner analysieren und in PARA verschieben"
    )
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Zeige Analyse der Ordner (default)"
    )
    parser.add_argument(
        "--move",
        action="store_true",
        help="Verschiebe Ordner in PARA-Struktur"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Zeige was verschoben würde, ohne zu verschieben"
    )
    
    args = parser.parse_args()
    
    # Default: analyze
    if not args.move and not args.dry_run:
        args.analyze = True
    
    vault_path = get_vault_path()
    
    if not vault_path.exists():
        print(f"❌ Vault nicht gefunden: {vault_path}")
        sys.exit(1)
    
    old_folders = find_old_folders(vault_path)
    
    if args.analyze or (not args.move and not args.dry_run):
        show_analysis(vault_path, old_folders)
    
    if args.move or args.dry_run:
        if not old_folders:
            print("\n✅ Keine Ordner zum Verschieben gefunden!")
            return
        
        if args.move and not args.dry_run:
            print("\n⚠️  WARNUNG: Dies verschiebt Ordner!")
            response = input("Fortfahren? [y/N]: ")
            if response.lower() != 'y':
                print("Abgebrochen.")
                return
        
        move_folders(vault_path, old_folders, dry_run=args.dry_run or not args.move)


if __name__ == "__main__":
    main()
