# Taskfile Usage Guide

Dieses Projekt nutzt [Task](https://taskfile.dev) für Automatisierung.

## Installation

```bash
brew install go-task
```

## Schnellstart

```bash
# Alle verfügbaren Tasks anzeigen
task --list

# Setup durchführen
task setup

# Vollständige Vault-Organisation
task organize
```

## Hauptfunktionen

### Vault-Organisation

```bash
task organize           # Vollständige Organisation (bootstrap-secondbrain.sh)
task rename            # Dateien umbenennen
task move              # Dateien in PARA-Struktur verschieben
task tags              # Tags normalisieren
```

### Content-Generierung

```bash
task extract-projects  # Projekt-Tags extrahieren
task extract-people    # Personen extrahieren
task build-moc         # Maps of Content generieren
task build-clusters    # Semantische Cluster-Maps
```

### Fabric AI Integration

```bash
task fabric-analyze     # Inhaltsanalyse (Summaries, Keywords, Tags)
task fabric-categorize  # Auto-Kategorisierung
task fabric-normalize   # YAML Frontmatter normalisieren
```

### Setup & Utilities

```bash
task setup             # Komplettes Setup
task install           # Python-Dependencies installieren
task install-fabric    # Fabric AI installieren
task check-vault       # Vault-Pfad überprüfen
task clean             # Temporäre Dateien löschen
```

### Dokumentation

```bash
task docs              # README anzeigen
task help              # Task-Liste anzeigen
task commit            # Git-Status anzeigen
```

## Umgebungsvariablen

```bash
# Vault-Pfad setzen (Standard: ~/Obsidian)
export OBSIDIAN_VAULT="/pfad/zu/deinem/vault"

# Dann Tasks ausführen
task organize
```

## Workflow-Beispiel

Typischer Workflow für Vault-Organisation:

```bash
# 1. Setup (einmalig)
task setup

# 2. Fabric AI konfigurieren (einmalig)
task install-fabric

# 3. Vault organisieren
task organize

# Oder Schritt für Schritt:
task fabric-normalize    # Frontmatter aufräumen
task fabric-analyze      # Inhalte analysieren
task rename              # Dateien umbenennen
task move                # In Ordner verschieben
task tags                # Tags bereinigen
task build-moc           # Index-Seiten erstellen
```

## Tipps

- `task --summary <taskname>` zeigt Task-Beschreibung
- Tasks können verkettet werden: `task rename move tags`
- Vault-Pfad über `OBSIDIAN_VAULT` konfigurierbar
