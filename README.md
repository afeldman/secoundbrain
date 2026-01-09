## Project Context

This repository implements secondbrain, a long-term knowledge, memory, and context system for humans.

secondbrain is not an analysis engine, not a decision system, and not a source of system truth.

It consumes human-readable content, indexes it, links it, and makes it retrievable over time.

🎯 **Purpose of secondbrain**

secondbrain answers questions like:

- “Have we seen something like this before?”
- “Where is related knowledge documented?”
- “What did we learn last time?”
- “How are topics, incidents, and ideas connected over time?”

secondbrain does not answer:

- why something objectively happened
- what the root cause is
- how severe something is
- what action must be taken


🧭 **Role in the Ecosystem**

secondbrain is a pure consumer.

Canonical flow:

Systems / Adapters
	↓
errorbrain (Verdicts, English, canonical)
	↓
Markdown / Obsidian notes
	↓
secondbrain (indexing, linking, retrieval)

- Data flow is one-way
- All inputs are read-only
- secondbrain never influences upstream systems


🧱 **Hard Architecture Rules (non-negotiable)**

- secondbrain produces no system truth
- secondbrain performs no analysis or evaluation
- secondbrain assigns no confidence, severity, or scores
- secondbrain does not modify verdicts
- secondbrain has no write-back channels
- Removing secondbrain must not affect any other system
- If something looks like analysis, decision, or judgement → it does not belong here.

📥 **Inputs (Allowed)**

- Markdown files (e.g. Obsidian vaults)
- Human-written notes
- Metadata: tags, dates, references, links
- References to external systems (IDs, URLs)

❌ **Not Allowed**

- API writes to other systems
- Event emission
- Verdict generation
- Automated feedback loops

🧠 **Internal Data Model Guidelines**

Allowed concepts:
- notes
- tags
- links
- relationships
- timelines
- clusters (descriptive only)

Forbidden concepts:
- root_cause
- confidence_score
- severity_decision
- recommended_action (as a system decision)

All stored content is contextual and interpretive, not authoritative.

🌍 **Translation & Localization**

secondbrain may translate human-readable content before storing or indexing it.

Rules:
- errorbrain output is always English and canonical
- Translation happens only in secondbrain
- Translation is a presentation step, not reasoning
- Markdown structure must be preserved
- Code blocks and identifiers must not be changed
- No summarization or interpretation is allowed
- English remains the source of truth. Translations are localized views for humans.

Example configuration:

    SECONDBRAIN_LANGUAGE=de
    SECONDBRAIN_TRANSLATOR=google|deepl|llm|none

🧠 **LLM Usage (if used)**

LLMs in secondbrain may:
- summarize text
- cluster related documents
- detect similarity
- support navigation and retrieval

LLMs must not:
- determine causes
- assign scores or confidence
- override human-written content
- produce system decisions

LLMs here act as librarians, not judges.

🧹 **Refactoring & Maintenance Guidelines**

When modifying secondbrain:
- Prefer simpler structures over clever logic
- Rename anything that sounds like analysis to overview or inspection
- Keep all processing read-only
- Separate clearly: external facts, human interpretation
- Treat all inputs as context, never as truth

🚦 **Acceptance Criteria**

secondbrain is correctly implemented if:
- It can be deleted without breaking other systems
- All inputs are read-only
- No decisions are made anywhere in the code
- Translations can be removed without data loss
- All outputs remain clearly human-authored

🧠 **Mental Model**

errorbrain judges.
Humans reflect.
secondbrain remembers and connects.

🚀 **Next Steps**

- Finalize repository structure
- Enforce read-only ingest paths
- Add translator module (pure function)
- Index and retrieve knowledge safely
- Integrate downstream only after cleanup

**Final Reminder**

secondbrain exists to support human memory and understanding, not to automate judgement.

If it ever feels “smart” in a decision-making sense, it is doing too much.
## Using secondbrain with errorbrain

secondbrain is designed to work seamlessly with **errorbrain** as a
**long-term knowledge and context layer**, not as an analysis or decision system.

The two projects have **strictly separated responsibilities**.

### Roles and Responsibilities

- **errorbrain**
  - Ingests facts (events, logs, status, metrics)
  - Correlates evidence
  - Performs reasoning (rules, optional LLM support)
  - Produces structured **Verdicts** (machine truth)

	- **secondbrain**
	- Consumes **human-readable knowledge**
	- Indexes, links, and retrieves context over time
	- Supports reflection, learning, and navigation
	- Never produces system truth or decisions

> secondbrain does not analyze incidents.  
> It remembers and connects what humans wrote about them.

---

### Data Flow (One-Way)

Adapters (e.g. fluxbrain)
↓
errorbrain
↓
Verdict (structured, machine-readable)
↓
Markdown / Obsidian notes (human-readable)
↓
secondbrain

- The flow is **read-only**
- There is **no feedback loop**
- secondbrain never influences errorbrain

---

### Typical Workflow

1. **An incident occurs**
	- Collected by adapters (e.g. FluxCD, CI, runtime signals)

2. **errorbrain produces a Verdict**
	- What likely happened
	- Supporting evidence
	- Recommended actions
	- Confidence level

3. **Verdict is rendered as Markdown**
	- Often via an Obsidian vault
	- Includes human notes, reflections, follow-ups

4. **secondbrain indexes the knowledge**
	- Tags, links, timelines
	- Similar incidents
	- Recurring patterns
	- Long-term context

5. **Humans query secondbrain**
	- “Have we seen this before?”
	- “What usually causes this?”
	- “What did we learn last time?”

---

### What secondbrain Explicitly Does NOT Do

When used with errorbrain, secondbrain must not:

- Determine root causes
- Assign confidence or severity
- Override or modify verdicts
- Feed decisions back into operational systems
- Act as an automated advisor

All system-level truth remains in **errorbrain**.

---

### Why This Separation Matters

This design ensures:

- Clear ownership of decisions
- Reproducible, auditable verdicts
- Human knowledge stays human
- No architectural feedback loops
- Safe long-term learning without operational risk

> **errorbrain judges.  
> Humans reflect.  
> secondbrain remembers.**

---

### Integration Readiness

secondbrain is considered correctly integrated with errorbrain if:

- All inputs are read-only (Markdown / exported data)
- No errorbrain APIs are written to
- Removing secondbrain does not affect errorbrain
- All interpretations remain clearly human-authored
## Obsidian → secondbrain Integration

secondbrain konsumiert ausschließlich human-readable Markdown-Notizen (z. B. aus Obsidian-Vaults), die aus System-Verdicts abgeleitet wurden.
Es indexiert, verlinkt und stellt Kontext bereit – beeinflusst oder verändert aber niemals die Ursprungssysteme.

# Fabric Second Brain

Automatisierte Second Brain Organisation mit Fabric AI + Obsidian

## LLM Usage & Guardrails

**Jede Nutzung von LLMs in secoundbrain ist strikt limitiert auf:**

- Zusammenfassung (Summarization)
- Clustering
- Ähnlichkeitssuche (Similarity Detection)
- Navigation/Verlinkung

**LLMs dürfen NICHT:**

- Analysieren, bewerten, scoren oder Entscheidungen treffen
- Systemwahrheiten erzeugen
- Ursachen bewerten oder Empfehlungen aussprechen

LLMs in secondbrain sind Bibliothekare, keine Richter. Sie unterstützen nur bei Kontext, Übersicht und Navigation.

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
