#!/usr/bin/env python3
"""
Erstellt Daily Notes im Vault und verlinkt bestehende Inhalte.
"""
import os
from pathlib import Path
from datetime import datetime, timedelta
import frontmatter


def get_vault_path():
    """Ermittelt den Vault-Pfad."""
    vault = os.environ.get("OBSIDIAN_VAULT", "~/Obsidian")
    return Path(vault).expanduser().resolve()


def create_daily_notes_structure(vault_path: Path):
    """Erstellt die Daily Notes Ordnerstruktur."""
    daily_path = vault_path / "Daily"
    daily_path.mkdir(exist_ok=True)
    
    # Unterordner nach Jahren
    current_year = datetime.now().year
    year_path = daily_path / str(current_year)
    year_path.mkdir(exist_ok=True)
    
    return year_path


def get_daily_note_path(vault_path: Path, date: datetime = None) -> Path:
    """Gibt den Pfad für eine Daily Note zurück."""
    if date is None:
        date = datetime.now()
    
    year_path = vault_path / "Daily" / str(date.year)
    year_path.mkdir(parents=True, exist_ok=True)
    
    filename = date.strftime("%Y-%m-%d.md")
    return year_path / filename


def create_daily_note(vault_path: Path, date: datetime = None, content: str = None):
    """Erstellt eine Daily Note."""
    if date is None:
        date = datetime.now()
    
    daily_path = get_daily_note_path(vault_path, date)
    
    if daily_path.exists():
        print(f"✓ Daily Note existiert bereits: {daily_path.name}")
        return daily_path
    
    # Template für Daily Note
    post = frontmatter.Post(content or "")
    post.metadata = {
        "date": date.strftime("%Y-%m-%d"),
        "tags": ["daily"],
        "title": date.strftime("%Y-%m-%d")
    }
    
    # Content
    daily_content = f"""# {date.strftime('%A, %d. %B %Y')}

## 📝 Notes


## ✅ Tasks

- [ ] 

## 🔗 Links


## 💭 Reflections

"""
    
    post.content = daily_content
    
    with open(daily_path, "w", encoding="utf-8") as f:
        f.write(frontmatter.dumps(post))
    
    print(f"✓ Daily Note erstellt: {daily_path.name}")
    return daily_path


def scan_recent_files(vault_path: Path, days: int = 7):
    """Scannt nach kürzlich geänderten Dateien."""
    cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
    
    recent_files = {}
    
    for md_file in vault_path.rglob("*.md"):
        # Überspringe Daily Notes, Index-Dateien, etc.
        if "Daily" in md_file.parts or "Index" in md_file.name:
            continue
        
        mtime = md_file.stat().st_mtime
        if mtime > cutoff_time:
            file_date = datetime.fromtimestamp(mtime).date()
            if file_date not in recent_files:
                recent_files[file_date] = []
            recent_files[file_date].append(md_file)
    
    return recent_files


def add_link_to_daily(daily_path: Path, file_path: Path, section: str = "Links"):
    """Fügt einen Link zur Daily Note hinzu."""
    
    if not daily_path.exists():
        return
    
    post = frontmatter.load(daily_path)
    content = post.content
    
    # Link erstellen
    link = f"- [[{file_path.stem}]]"
    
    # Prüfe ob Link schon existiert
    if link in content:
        return
    
    # Füge Link unter passender Section hinzu
    section_marker = f"## 🔗 {section}"
    
    if section_marker in content:
        lines = content.split('\n')
        new_lines = []
        in_section = False
        added = False
        
        for line in lines:
            new_lines.append(line)
            if line.startswith(section_marker):
                in_section = True
            elif in_section and not added and (line.startswith('##') or not line.strip()):
                if line.strip():  # Nächste Section
                    new_lines.insert(-1, link)
                    new_lines.insert(-1, "")
                else:
                    new_lines.insert(-1, link)
                added = True
                in_section = False
        
        if not added:
            new_lines.append(link)
        
        post.content = '\n'.join(new_lines)
    else:
        # Section existiert nicht, füge sie hinzu
        post.content += f"\n\n{section_marker}\n\n{link}\n"
    
    with open(daily_path, "w", encoding="utf-8") as f:
        f.write(frontmatter.dumps(post))


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Erstellt Daily Notes und organisiert Inhalte"
    )
    parser.add_argument(
        "--create",
        action="store_true",
        help="Erstelle Daily Note für heute"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Anzahl Tage rückwärts für die Daily Notes erstellt werden (default: 7)"
    )
    parser.add_argument(
        "--link-recent",
        action="store_true",
        help="Verlinke kürzlich geänderte Dateien in Daily Notes"
    )
    parser.add_argument(
        "--scan",
        action="store_true",
        help="Zeige kürzlich geänderte Dateien"
    )
    
    args = parser.parse_args()
    
    vault_path = get_vault_path()
    
    if not vault_path.exists():
        print(f"❌ Vault nicht gefunden: {vault_path}")
        return
    
    # Default: heute erstellen
    if not any([args.scan, args.link_recent]):
        args.create = True
    
    if args.create:
        print(f"\n📅 Erstelle Daily Notes für die letzten {args.days} Tage\n")
        
        for i in range(args.days):
            date = datetime.now() - timedelta(days=i)
            create_daily_note(vault_path, date)
        
        print(f"\n✅ Daily Notes erstellt in: {vault_path}/Daily/\n")
    
    if args.scan or args.link_recent:
        print(f"\n🔍 Scanne kürzlich geänderte Dateien (letzte {args.days} Tage)...\n")
        recent_files = scan_recent_files(vault_path, args.days)
        
        if not recent_files:
            print("Keine kürzlich geänderten Dateien gefunden.\n")
            return
        
        for file_date in sorted(recent_files.keys(), reverse=True):
            files = recent_files[file_date]
            date_str = file_date.strftime("%Y-%m-%d (%A)")
            print(f"📅 {date_str}: {len(files)} Dateien")
            
            if args.scan:
                for f in files[:5]:  # Zeige max 5
                    print(f"   - {f.relative_to(vault_path)}")
                if len(files) > 5:
                    print(f"   ... und {len(files) - 5} weitere")
            
            if args.link_recent:
                # Daily Note für diesen Tag erstellen/öffnen
                daily_date = datetime.combine(file_date, datetime.min.time())
                daily_path = create_daily_note(vault_path, daily_date)
                
                # Links hinzufügen
                for f in files:
                    add_link_to_daily(daily_path, f)
                
                print(f"   ✓ {len(files)} Links hinzugefügt zu {daily_path.name}")
            
            print()
        
        if args.link_recent:
            print("✅ Daily Notes aktualisiert!\n")


if __name__ == "__main__":
    main()
