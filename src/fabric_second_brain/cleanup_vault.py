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


def show_overview(vault_path: Path, old_folders: list):
    """Show an overview of folders outside the PARA structure.

    Args:
        vault_path (Path): Path to the vault root.
        old_folders (list): List of Path objects for folders outside PARA.
    """
    print(f"\n📊 Vault Structure Overview: {vault_path}")
    print(f"\n🗂  Folders outside PARA: {len(old_folders)}\n")
    if not old_folders:
        print("✅ All folders are already in the PARA structure!")
        return
    suggestions = {}
    for folder in old_folders:
        suggested = suggest_para_location(folder.name)
        suggestions.setdefault(suggested, []).append(folder)
    for para_folder in ["01_Projects", "02_Areas", "03_Resources", "04_Archive"]:
        if para_folder in suggestions:
            folders = suggestions[para_folder]
            print(f"\n📁 {para_folder}/ ({len(folders)} folders):")
            for folder in folders:
                md_files = list(folder.rglob("*.md"))
                print(f"   → {folder.name:40} ({len(md_files)} .md files)")


def move_folders(vault_path: Path, old_folders: list, dry_run: bool = True):
    """Move folders into the PARA structure.

    Args:
        vault_path (Path): Path to the vault root.
        old_folders (list): List of Path objects for folders outside PARA.
        dry_run (bool): If True, only show what would be moved.
    """
    print(f"\n{'🔍 DRY RUN - ' if dry_run else '📦 '}Moving folders...\n")
    moved = 0
    for folder in old_folders:
        suggested = suggest_para_location(folder.name)
        target_dir = vault_path / suggested
        target_path = target_dir / folder.name
        if target_path.exists():
            print(f"⚠️  Skipping {folder.name} - already exists in {suggested}")
            continue
        if dry_run:
            print(f"[DRY] {folder.name} → {suggested}/")
        else:
            try:
                shutil.move(str(folder), str(target_path))
                print(f"✅ {folder.name} → {suggested}/")
                moved += 1
            except Exception as e:
                print(f"❌ Error moving {folder.name}: {e}")
    if dry_run:
        print(f"\n💡 Use --move to actually move the folders")
    else:
        print(f"\n✅ {moved} folders moved successfully!")


def main():
    """Command-line interface for vault cleanup.

    Example:
        $ python cleanup_vault.py --overview
        $ python cleanup_vault.py --move
    """
    import argparse
    parser = argparse.ArgumentParser(
        description="Vault Cleanup - Overview and move folders into PARA structure"
    )
    parser.add_argument(
        "--overview",
        action="store_true",
        help="Show overview of folders (default)"
    )
    parser.add_argument(
        "--move",
        action="store_true",
        help="Move folders into PARA structure"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be moved, without moving"
    )
    args = parser.parse_args()
    vault_path = get_vault_path()
    if not vault_path.exists():
        print(f"❌ Vault not found: {vault_path}")
        sys.exit(1)
    old_folders = find_old_folders(vault_path)
    if args.overview or (not args.move and not args.dry_run):
        show_overview(vault_path, old_folders)
    if args.move or args.dry_run:
        if not old_folders:
            print("\n✅ No folders to move found!")
            return
        if args.move and not args.dry_run:
            print("\n⚠️  WARNING: This will move folders!")
            response = input("Continue? [y/N]: ")
            if response.lower() != 'y':
                print("Aborted.")
                return
        move_folders(vault_path, old_folders, dry_run=args.dry_run or not args.move)


if __name__ == "__main__":
    main()
