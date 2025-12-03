#!/usr/bin/env python3
"""
YouTube zu Obsidian Workflow mit Fabric AI.
Extrahiert Transkripte, Kommentare und Metadaten und erstellt Notizen.
"""
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import frontmatter
import json


def get_vault_path():
    """Ermittelt den Vault-Pfad."""
    vault = os.environ.get("OBSIDIAN_VAULT", "~/Obsidian")
    return Path(vault).expanduser().resolve()


def extract_youtube_id(url: str) -> str:
    """Extrahiert die YouTube Video-ID aus der URL."""
    import re
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/)([^&\n?#]+)',
        r'youtube\.com/embed/([^&\n?#]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def run_fabric_command(args: list, input_text: str = None) -> str:
    """Führt einen Fabric-Befehl aus."""
    cmd = ["fabric"] + args
    
    try:
        if input_text:
            result = subprocess.run(
                cmd,
                input=input_text,
                capture_output=True,
                text=True,
                check=True
            )
        else:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Fabric Fehler: {e.stderr}")
        return None
    except FileNotFoundError:
        print("❌ Fabric ist nicht installiert. Bitte installiere es mit: go install github.com/danielmiessler/fabric@latest")
        sys.exit(1)


def get_youtube_transcript(url: str, with_timestamps: bool = False) -> str:
    """Holt das Transkript von YouTube mit Fabric."""
    print(f"📥 Lade Transkript von YouTube...")
    
    args = ["-y", url]
    if with_timestamps:
        args.append("--transcript-with-timestamps")
    else:
        args.append("--transcript")
    
    transcript = run_fabric_command(args)
    return transcript


def get_youtube_metadata(url: str) -> dict:
    """Holt Metadaten von YouTube mit Fabric."""
    print(f"📊 Lade Metadaten...")
    
    output = run_fabric_command(["-y", url, "--metadata"])
    
    if output:
        # Parse als JSON falls möglich
        try:
            return json.loads(output)
        except:
            # Fallback: einfaches Text-Parsing
            return {"raw": output}
    return {}


def apply_fabric_pattern(content: str, pattern: str) -> str:
    """Wendet ein Fabric Pattern auf den Content an."""
    print(f"🤖 Wende Pattern '{pattern}' an...")
    
    result = run_fabric_command(["--pattern", pattern], input_text=content)
    return result if result else ""


def create_youtube_note(vault_path: Path, url: str, transcript: str, 
                       metadata: dict, pattern: str = None, title: str = None):
    """Erstellt eine Obsidian-Notiz für ein YouTube-Video."""
    
    # Ordner für YouTube-Notizen
    youtube_dir = vault_path / "03_Resources" / "YouTube"
    youtube_dir.mkdir(parents=True, exist_ok=True)
    
    # Titel bestimmen
    if not title:
        video_id = extract_youtube_id(url) or "unknown"
        title = metadata.get("title", f"YouTube_{video_id}")
    
    # Dateiname
    date_stamp = datetime.now().strftime("%Y-%m-%d")
    safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in title)
    filename = f"{date_stamp}-{safe_title}.md"
    filepath = youtube_dir / filename
    
    # Content verarbeiten
    processed_content = transcript
    
    if pattern:
        processed_content = apply_fabric_pattern(transcript, pattern)
    
    # Frontmatter erstellen
    post = frontmatter.Post("")
    post.metadata = {
        "title": title,
        "url": url,
        "date": date_stamp,
        "tags": ["youtube", "video"],
        "type": "video-note"
    }
    
    # Metadaten hinzufügen
    if metadata:
        if "channel" in metadata:
            post.metadata["channel"] = metadata["channel"]
        if "duration" in metadata:
            post.metadata["duration"] = metadata["duration"]
        if "views" in metadata:
            post.metadata["views"] = metadata["views"]
    
    # Content zusammensetzen
    content = f"""# {title}

## 📺 Video Info

- **URL**: {url}
- **Date**: {date_stamp}
"""
    
    if metadata:
        if "channel" in metadata:
            content += f"- **Channel**: {metadata.get('channel', 'N/A')}\n"
        if "duration" in metadata:
            content += f"- **Duration**: {metadata.get('duration', 'N/A')}\n"
    
    content += "\n## 📝 Notes\n\n"
    content += processed_content
    
    content += "\n\n## 🔗 Related\n\n"
    
    post.content = content
    
    # Speichern
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter.dumps(post))
    
    print(f"\n✅ Notiz erstellt: {filepath.relative_to(vault_path)}")
    return filepath


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="YouTube zu Obsidian mit Fabric AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  # Einfaches Transkript
  %(prog)s "https://youtube.com/watch?v=..."
  
  # Mit Timestamps
  %(prog)s "https://youtube.com/watch?v=..." --timestamps
  
  # Mit Fabric Pattern (extract_wisdom, summarize, etc.)
  %(prog)s "https://youtube.com/watch?v=..." --pattern extract_wisdom
  
  # Custom Titel
  %(prog)s "https://youtube.com/watch?v=..." --title "My Video Notes"
  
  # Mehrere Videos
  %(prog)s url1 url2 url3 --pattern summarize
        """
    )
    
    parser.add_argument(
        "urls",
        nargs="*",
        help="YouTube Video URL(s)"
    )
    parser.add_argument(
        "-t", "--timestamps",
        action="store_true",
        help="Transkript mit Timestamps"
    )
    parser.add_argument(
        "-p", "--pattern",
        help="Fabric Pattern anwenden (z.B. extract_wisdom, summarize, analyze_claims)"
    )
    parser.add_argument(
        "--title",
        help="Custom Titel für die Notiz"
    )
    parser.add_argument(
        "--list-patterns",
        action="store_true",
        help="Zeige verfügbare Fabric Patterns"
    )
    
    args = parser.parse_args()
    
    # Liste Patterns
    if args.list_patterns:
        print("🎨 Verfügbare Fabric Patterns:\n")
        patterns = run_fabric_command(["--listpatterns"])
        if patterns:
            print(patterns)
        else:
            print("Keine Patterns gefunden. Führe 'fabric --setup' aus.")
        return
    
    vault_path = get_vault_path()
    
    if not vault_path.exists():
        print(f"❌ Vault nicht gefunden: {vault_path}")
        print("Setze OBSIDIAN_VAULT Umgebungsvariable.")
        sys.exit(1)
    
    print(f"\n🎬 YouTube zu Obsidian Workflow")
    print(f"📁 Vault: {vault_path}\n")
    
    for i, url in enumerate(args.urls, 1):
        print(f"\n{'='*60}")
        print(f"Video {i}/{len(args.urls)}: {url}")
        print('='*60)
        
        # Video-ID prüfen
        video_id = extract_youtube_id(url)
        if not video_id:
            print(f"⚠️  Überspringe: Keine gültige YouTube URL")
            continue
        
        try:
            # Transkript holen
            transcript = get_youtube_transcript(url, args.timestamps)
            if not transcript:
                print("⚠️  Konnte Transkript nicht laden")
                continue
            
            # Metadaten holen
            metadata = get_youtube_metadata(url)
            
            # Notiz erstellen
            create_youtube_note(
                vault_path,
                url,
                transcript,
                metadata,
                pattern=args.pattern,
                title=args.title if len(args.urls) == 1 else None
            )
            
        except Exception as e:
            print(f"❌ Fehler bei Video {i}: {e}")
            continue
    
    print(f"\n{'='*60}")
    print("✅ Workflow abgeschlossen!")
    print(f"\n💡 Tipp: Nutze --pattern extract_wisdom für beste Ergebnisse")


if __name__ == "__main__":
    main()
