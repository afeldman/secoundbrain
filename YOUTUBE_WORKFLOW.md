# YouTube Workflow

Automatischer Workflow zum Extrahieren von YouTube-Videos mit Fabric AI und Speichern in Obsidian.

## Features

- ✅ **Transkript-Extraktion** mit/ohne Timestamps
- 🤖 **Fabric AI Patterns** für intelligente Verarbeitung
- 📊 **Metadaten** (Titel, Kanal, Duration, etc.)
- 📝 **Obsidian-Integration** mit Frontmatter
- 🔄 **Batch-Processing** für mehrere Videos

## Voraussetzungen

```bash
# Fabric AI muss installiert sein
go install github.com/danielmiessler/fabric@latest
fabric --setup

# Python Dependencies
pip install -r requirements.txt
```

## Verwendung

### Einfaches Transkript

```bash
python3 youtube_workflow.py "https://youtube.com/watch?v=..."
```

Dies erstellt eine Notiz in `03_Resources/YouTube/` mit:

- Vollständigem Transkript
- Video-Metadaten
- Automatischem Frontmatter

### Mit Timestamps

```bash
python3 youtube_workflow.py "https://youtube.com/watch?v=..." --timestamps
```

### Mit Fabric Patterns

```bash
# Weisheiten extrahieren
python3 youtube_workflow.py "https://youtube.com/watch?v=..." --pattern extract_wisdom

# Zusammenfassung
python3 youtube_workflow.py "https://youtube.com/watch?v=..." --pattern summarize

# Claims analysieren
python3 youtube_workflow.py "https://youtube.com/watch?v=..." --pattern analyze_claims
```

### Mehrere Videos

```bash
python3 youtube_workflow.py \
  "https://youtube.com/watch?v=video1" \
  "https://youtube.com/watch?v=video2" \
  "https://youtube.com/watch?v=video3" \
  --pattern extract_wisdom
```

### Custom Titel

```bash
python3 youtube_workflow.py "https://youtube.com/watch?v=..." --title "My Custom Note Title"
```

## Fabric Patterns

Zeige alle verfügbaren Patterns:

```bash
python3 youtube_workflow.py --list-patterns
```

### Empfohlene Patterns für YouTube:

| Pattern           | Beschreibung                                           |
| ----------------- | ------------------------------------------------------ |
| `extract_wisdom`  | Extrahiert die wichtigsten Erkenntnisse und Weisheiten |
| `summarize`       | Erstellt eine kompakte Zusammenfassung                 |
| `analyze_claims`  | Analysiert Behauptungen und deren Validität            |
| `extract_article` | Konvertiert in Artikel-Format                          |
| `create_keynote`  | Erstellt Präsentations-Outline                         |
| `extract_ideas`   | Extrahiert Hauptideen und Konzepte                     |
| `create_quiz`     | Generiert Quiz-Fragen aus dem Content                  |
| `rate_content`    | Bewertet die Qualität des Contents                     |

## Task-Shortcuts

```bash
# Patterns anzeigen
task yt-list-patterns

# Video extrahieren
task yt-extract URL="https://youtube.com/watch?v=..."

# Mit extract_wisdom Pattern
task yt-wisdom URL="https://youtube.com/watch?v=..."
```

## Output-Struktur

Notizen werden gespeichert als:

```
03_Resources/YouTube/
└── YYYY-MM-DD-Video_Title.md
```

### Frontmatter

```yaml
---
title: Video Title
url: https://youtube.com/watch?v=...
date: 2025-12-03
tags: [youtube, video]
type: video-note
channel: Channel Name
duration: 12:34
---
```

## Beispiele

### Tech-Talk extrahieren

```bash
python3 youtube_workflow.py \
  "https://youtube.com/watch?v=dQw4w9WgXcQ" \
  --pattern extract_wisdom \
  --title "AI Safety Talk"
```

### Podcast-Episode zusammenfassen

```bash
python3 youtube_workflow.py \
  "https://youtube.com/watch?v=..." \
  --pattern summarize \
  --timestamps
```

### Tutorial-Serie verarbeiten

```bash
# Alle URLs in einer Datei
cat tutorial_urls.txt | xargs python3 youtube_workflow.py --pattern extract_article
```

## Tipps

1. **Beste Patterns**: `extract_wisdom` ist meist die beste Wahl für YouTube-Videos
2. **Timestamps**: Nützlich für lange Videos zum späteren Nachschlagen
3. **Batch-Processing**: Verarbeite mehrere Videos auf einmal für Effizienz
4. **Custom Patterns**: Erstelle eigene Fabric Patterns in `~/.config/fabric/patterns/`

## Troubleshooting

### Fabric nicht gefunden

```bash
# Installiere Fabric
go install github.com/danielmiessler/fabric@latest
fabric --setup
```

### Transkript nicht verfügbar

- Manche Videos haben keine Untertitel/Transkripte
- Private Videos können nicht verarbeitet werden
- Age-restricted Videos benötigen Authentication

### Langsame Verarbeitung

- Fabric nutzt AI-Modelle, die Zeit benötigen
- Bei vielen Videos: Batch-Processing verwenden
- Lokale Modelle (Ollama) sind schneller als Cloud-APIs
