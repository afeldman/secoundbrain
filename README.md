# Fabric Second Brain

Automatisierte Second Brain Organisation mit Fabric AI + Obsidian + LM Studio/Ollama

## Quick Start

```bash
# Umgebungsvariable für deinen Obsidian Vault setzen
export OBSIDIAN_VAULT="$HOME/Obsidian"

# Dependencies installieren
pip install -r requirements.txt

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

## Manuelle Verwendung

```bash
# Einzelne Aktionen ausführen
python3 organize.py rename --rules rules/rename.yaml
python3 organize.py move --rules rules/categorize.yaml
python3 organize.py tags --rules rules/tags.yaml

# Generatoren
python3 generators/project_extractor.py
python3 generators/people_extractor.py
python3 generators/moc_builder.py
python3 generators/cluster_map.py

# Mit Fabric AI
fabric apply summarize,keywords,tags -r "$OBSIDIAN_VAULT"
fabric apply categorize -r "$OBSIDIAN_VAULT" -o rules/categorize.yaml
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
# Python-Dependencies
pip install -r requirements.txt

# Fabric AI installieren
# siehe: https://github.com/danielmiessler/fabric
go install github.com/danielmiessler/fabric@latest
fabric --setup
```

## Ordnerstruktur

Das Projekt organisiert deinen Vault nach der PARA-Methode:

```
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
