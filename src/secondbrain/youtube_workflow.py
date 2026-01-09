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


def run_fabric_command(args: list, input_text: str = None, raise_on_error: bool = False) -> str:
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
        error_msg = e.stderr.strip() if e.stderr else str(e)
        print(f"❌ Fabric Fehler: {error_msg}")
        if raise_on_error:
            raise
        return None
    except FileNotFoundError:
        print("❌ Fabric ist nicht installiert. Bitte installiere es mit: go install github.com/danielmiessler/fabric@latest")
        sys.exit(1)


def get_youtube_transcript(url: str, with_timestamps: bool = False) -> str:
    """Holt das Transkript von YouTube mit Fabric."""
    print(f"📥 Lade Transkript von YouTube...")
    
    # Fabric nutzt -y flag für YouTube URL, gibt direkt das Transkript zurück
    args = ["-y", url]
    
    transcript = run_fabric_command(args, raise_on_error=False)
    if not transcript:
        print("⚠️  Warnung: Transkript konnte nicht geladen werden")
        return ""
    return transcript


def get_youtube_metadata(url: str) -> dict:
    """Holt Metadaten von YouTube - extrahiert sie aus dem Transkript."""
    # Fabric liefert keine separaten Metadaten
    # Wir können nur die Video-ID extrahieren
    video_id = extract_youtube_id(url)
    return {
        "video_id": video_id,
        "url": url
    }


def apply_fabric_pattern(content: str, pattern: str) -> str:
    """Wendet ein Fabric Pattern auf den Content an."""
    print(f"🤖 Wende Pattern '{pattern}' an...")
    
    result = run_fabric_command(["--pattern", pattern], input_text=content)
    return result if result else ""


def create_structured_summary(transcript: str) -> dict:
    """Erstellt eine strukturierte Zusammenfassung mit einem Custom AI-Pattern."""
    print("\n📊 Erstelle strukturierte Zusammenfassung mit AI...")
    
    # Truncate transcript wenn zu lang (API Limits)
    max_chars = 4000  # Konservativer Wert für API Limits
    truncated = False
    if len(transcript) > max_chars:
        print(f"  ⚠️  Transkript zu lang ({len(transcript)} Zeichen), kürze auf {max_chars} Zeichen...")
        transcript = transcript[:max_chars] + "\n\n[... Rest des Transkripts gekürzt ...]"
        truncated = True
    
    # Nutze das Custom Pattern für Video-Zusammenfassungen
    print("  → Applying extract_video_summary pattern...")
    result = apply_fabric_pattern(transcript, 'extract_video_summary')
    
    if not result:
        print("  ⚠️  AI-Verarbeitung fehlgeschlagen, verwende Fallback")
        return {
            'summary': '',
            'tags': [],
            'content': '',
            'truncated': truncated
        }
    
    # Parse das Ergebnis
    summary = {
        'content': result,
        'tags': [],
        'summary': '',
        'truncated': truncated
    }
    
    # Extrahiere Tags aus dem Ergebnis
    if '🏷️ TAGS' in result or '## TAGS' in result:
        lines = result.split('\n')
        for i, line in enumerate(lines):
            if 'TAGS' in line and i + 1 < len(lines):
                # Nächste Zeile enthält die Tags
                tags_line = lines[i + 1].strip()
                tags = [t.strip() for t in tags_line.split(',')]
                summary['tags'] = [t.lower().replace(' ', '-') for t in tags if t][:8]
                break
    
    print(f"  ✅ AI-Zusammenfassung erstellt ({len(result)} Zeichen)")
    return summary


def create_youtube_note(vault_path: Path, url: str, transcript: str, 
                       metadata: dict, pattern: str = None, title: str = None,
                       use_ai_structure: bool = False):
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
    
    # AI-strukturierte Verarbeitung
    ai_summary = None
    if use_ai_structure and transcript:
        ai_summary = create_structured_summary(transcript)
    
    # Content verarbeiten
    processed_content = transcript
    
    if pattern and not use_ai_structure:
        processed_content = apply_fabric_pattern(transcript, pattern)
    
    # Frontmatter erstellen
    post = frontmatter.Post("")
    base_tags = ["youtube", "video"]
    
    # AI-generierte Tags hinzufügen
    if ai_summary and ai_summary.get('tags'):
        base_tags.extend(ai_summary['tags'])
    
    post.metadata = {
        "title": title,
        "url": url,
        "date": date_stamp,
        "tags": base_tags,
        "type": "video-note",
        "ai_processed": use_ai_structure
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
    
    # AI-Zusammenfassung hinzufügen
    if ai_summary and ai_summary.get('content'):
        content += "\n## 🤖 AI Zusammenfassung\n\n"
        if ai_summary.get('truncated'):
            content += "> ⚠️ *Hinweis: Aufgrund der Länge wurde nur der Anfang des Transkripts für die AI-Analyse verwendet.*\n\n"
        content += ai_summary['content'] + "\n\n"
        content += "---\n\n"
    
    content += "\n## 📝 Vollständiges Transkript\n\n"
    content += processed_content if not use_ai_structure else transcript
    
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
        "--ai-summary",
        action="store_true",
        help="Erstelle strukturierte AI-Zusammenfassung (Summary + Wisdom + Auto-Tags)"
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
            
            # Auch bei leerem Transkript fortfahren (Notiz ohne Content)
            # Metadaten holen
            metadata = get_youtube_metadata(url)
            
            # Notiz erstellen
            create_youtube_note(
                vault_path,
                url,
                transcript,
                metadata,
                pattern=args.pattern,
                title=args.title if len(args.urls) == 1 else None,
                use_ai_structure=args.ai_summary
            )
            
        except Exception as e:
            print(f"❌ Fehler bei Video {i}: {e}")
            continue
    
    print(f"\n{'='*60}")
    print("✅ Workflow abgeschlossen!")
    print(f"\n💡 Tipp: Nutze --pattern extract_wisdom für beste Ergebnisse")


if __name__ == "__main__":
    main()
