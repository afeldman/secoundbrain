# Fabric Second Brain

Automatisierte Second Brain Organisation mit Fabric AI + Obsidian

## Quick Start

```bash
# Installation mit uv (empfohlen)
uv sync

# Oder mit Task
task install

# Umgebungsvariable setzen
export OBSIDIAN_VAULT="$HOME/lynq"

# PARA-Struktur im Vault erstellen
uv run init-vault

# Vollständige Vault-Organisation ausführen
./bootstrap-secondbrain.sh
```

## Workflow

Das System führt folgende Schritte automatisch aus:

1. **YAML Normalisierung** - Frontmatter standardisieren
2. **Inhaltsanalyse** - Summaries, Keywords, Tags generieren (via Fabric)
3. **Auto-Kategorisierung** - Notizen automatisch kategorisieren
4. **Projekt-Extraktion** - Projekt-relevante Notizen taggen
5. **Personen-Extraktion** - Personen aus Texten extrahieren
6. **Datei-Umbenennung** - Konsistente Dateinamen
7. **Ordner-Organisation** - PARA-Struktur (Projects/Areas/Resources/Archive)
8. **Tag-Bereinigung** - Tags normalisieren und deduplizieren
9. **MOC-Generierung** - Maps of Content erstellen
10. **Cluster-Maps** - Semantische Themen-Cluster visualisieren

## Verfügbare Commands

Alle Scripts sind als CLI-Tools über `uv run` verfügbar:

```bash
# Vault Management
uv run init-vault              # PARA-Struktur erstellen
uv run init-vault --info       # Vault-Analyse
uv run cleanup-vault --analyze # Alte Ordner analysieren

# Daily Notes
uv run create-dailies --create --days 7  # Woche erstellen
uv run create-dailies --link-recent      # Auto-Linking

# YouTube Workflow
uv run youtube "URL" --ai-summary        # Mit AI-Zusammenfassung
uv run youtube "URL" --pattern extract_wisdom

# Organisation
uv run organize rename --rules rules/rename.yml
uv run organize move --rules rules/categorize.yml
uv run organize tags --rules rules/tags.yml

# Generatoren
uv run moc-builder          # Maps of Content
uv run cluster-map          # Cluster-Visualisierung
uv run project-extractor    # Projekt-Extraktion
uv run people-extractor     # Personen-Extraktion
```

## Task Shortcuts

```bash
# Installation
task setup              # Komplette Installation (uv + Fabric)

# Vault Setup
task init-vault        # PARA-Struktur erstellen
task cleanup-move      # Alte Ordner migrieren

# Daily Notes
task daily-create      # Heute
task daily-week        # Letzte Woche
task daily-link        # Auto-Linking

# YouTube
task yt-summary URL="https://youtube.com/..."   # AI-Summary
task yt-wisdom URL="https://youtube.com/..."    # Extract Wisdom
task yt-list-patterns                            # Alle Patterns

# Organisation
task organize          # Bootstrap-Workflow
task build-moc         # MOCs generieren
task build-clusters    # Cluster-Maps
```

## Features

- 🧠 **Fabric AI Integration** - KI-gestützte Inhaltsanalyse und Zusammenfassungen
- 📝 **Auto-Organisation** - Dateien automatisch umbenennen, kategorisieren und verschieben
- 🏗️ **PARA-Struktur** - Projects, Areas, Resources, Archive Organisation
- 🔖 **Tag-Management** - Automatische Tag-Extraktion, Normalisierung und Bereinigung
- 🗺️ **Maps of Content** - Automatische Index-Generierung für Kategorien
- 🔗 **Semantic Clustering** - Thematische Cluster-Visualisierung
- 👥 **Entity-Extraktion** - Personen und Projekte automatisch erkennen
- 📋 **Frontmatter-Normalisierung** - YAML-Metadaten standardisieren
- ⚙️ **LM Studio / Ollama Support** - Lokale LLM-Modelle unterstützt

## Konfiguration

### Rules (YAML)

Passe die Regeln in `rules/` an deine Bedürfnisse an:

- **`categorize.yml`** - Kategorien und Ordner-Zuordnung
- **`rename.yml`** - Regex-Patterns für Dateinamen
- **`tags.yml`** - Tag-Bereinigungsregeln

### Templates

Vorlagen für neue Notizen in `templates/`:

- `journal.md` - Tägliche Journal-Einträge
- `person.md` - Personen-Profile
- `project.md` - Projekt-Übersichten
- `research.md` - Forschungsnotizen
- `resource.md` - Ressourcen und Referenzen

## Requirements

- Python ≥3.11
- Fabric AI CLI (siehe unten)
- Obsidian Vault

### Installation

```bash
# Virtual Environment (empfohlen auf macOS)
python3 -m venv .venv
source .venv/bin/activate

# Python-Dependencies
pip install -r requirements.txt

# Fabric AI installieren
# siehe: https://github.com/danielmiessler/fabric
go install github.com/danielmiessler/fabric@latest
fabric --setup
```

**Hinweis für macOS**: Python ist externally-managed, daher ist ein Virtual Environment erforderlich.

## Ordnerstruktur

Das Projekt organisiert deinen Vault nach der PARA-Methode:

```text
~/Obsidian/
├── 01_Projects/        # Aktive Projekte mit Deadlines
├── 02_Areas/           # Verantwortungsbereiche
├── 03_Resources/       # Referenzmaterial
├── 04_Archive/         # Abgeschlossene/Inaktive Notizen
├── Projects_Index.md   # Auto-generierter MOC
├── Areas_Index.md
├── Resources_Index.md
└── Semantic_Clusters.md
```

### Vault initialisieren

```bash
# PARA-Ordner erstellen
python3 init_vault.py

# Info über bestehende Inhalte anzeigen
python3 init_vault.py --info

# Dry-Run (zeigt nur was passieren würde)
python3 init_vault.py --dry-run

# Oder mit Task
task init-vault
task init-vault-info
```

### Vault aufräumen

```bash
# Analysiere alte Ordner im Root
python3 cleanup_vault.py --analyze

# Zeige was verschoben würde
python3 cleanup_vault.py --dry-run

# Verschiebe Ordner in PARA-Struktur
python3 cleanup_vault.py --move

# Oder mit Task
task cleanup-analyze
task cleanup-dry-run
task cleanup-move
```

### Daily Notes

```bash
# Erstelle Daily Note für heute
python3 create_dailies.py --create --days 1

# Erstelle Daily Notes für letzte Woche
python3 create_dailies.py --create --days 7

# Scanne kürzlich geänderte Dateien
python3 create_dailies.py --scan --days 3

# Verlinke geänderte Dateien in Daily Notes
python3 create_dailies.py --link-recent --days 3

# Oder mit Task
task daily-create
task daily-week
task daily-scan
task daily-link
```

### YouTube Workflow (mit Fabric AI)

```bash
# Zeige verfügbare Patterns
python3 youtube_workflow.py --list-patterns

# Einfaches Transkript extrahieren
python3 youtube_workflow.py "https://youtube.com/watch?v=..."

# Mit Timestamps
python3 youtube_workflow.py "https://youtube.com/watch?v=..." --timestamps

# Mit Fabric Pattern (extract_wisdom, summarize, etc.)
python3 youtube_workflow.py "https://youtube.com/watch?v=..." --pattern extract_wisdom

# Mehrere Videos auf einmal
python3 youtube_workflow.py url1 url2 url3 --pattern summarize

# Oder mit Task
task yt-list-patterns
task yt-extract URL="https://youtube.com/watch?v=..."
task yt-wisdom URL="https://youtube.com/watch?v=..."
```

**Beliebte Patterns für YouTube:**

- `extract_wisdom` - Extrahiert die wichtigsten Erkenntnisse
- `summarize` - Kurze Zusammenfassung
- `analyze_claims` - Analysiert Behauptungen
- `create_keynote` - Erstellt Präsentations-Outline
