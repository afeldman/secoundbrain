# Installation Guide

## Schnellstart mit uv (empfohlen)

```bash
# 1. uv installieren (falls noch nicht vorhanden)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Repository klonen
git clone https://github.com/afeldman/fabric-second-brain.git
cd fabric-second-brain

# 3. Projekt mit uv installieren
uv sync

# 4. Fabric AI installieren
go install github.com/danielmiessler/fabric@latest
fabric --setup

# 5. Umgebungsvariable setzen
export OBSIDIAN_VAULT="$HOME/lynq"

# 6. Fertig! Scripts nutzen
uv run init-vault
uv run youtube "https://youtube.com/..." --ai-summary
```

## Alternative: Mit Task

```bash
# Komplette Installation
task setup

# Scripts nutzen
task init-vault
task yt-summary URL="https://youtube.com/..."
task daily-create
```

## Voraussetzungen

- **uv** - Modernes Python Package Management (https://docs.astral.sh/uv/)
- **Python** ≥ 3.11
- **Go** (für Fabric AI)
- **Obsidian** Vault
- **Task** (optional, für Shortcuts)

## Warum uv?

`uv` ist ein ultraschneller Python Package Manager:

- ⚡ **10-100x schneller** als pip
- 🔒 **Automatisches Lockfile** Management
- 📦 **Eingebautes venv** Management
- 🎯 **Direkte Script-Ausführung** mit `uv run`
- 🚀 **Keine manuellen venv-Aktivierungen** nötig

## Fabric AI Setup

Fabric ist das Herzstück für KI-gestützte Analyse:

```bash
# Installation
go install github.com/danielmiessler/fabric@latest

# Konfiguration (wähle deinen AI Provider)
fabric --setup

# Empfohlen: DeepSeek Chat (schnell + günstig)
# Oder: Lokale Modelle via Ollama
```

Unterstützte Provider:

- OpenAI
- Anthropic (Claude)
- Ollama (lokal)
- LM Studio (lokal)

## Obsidian Vault

Setze den Pfad zu deinem Vault:

```bash
# Temporär
export OBSIDIAN_VAULT="$HOME/Obsidian"

# Permanent (in ~/.zshrc oder ~/.bashrc)
echo 'export OBSIDIAN_VAULT="$HOME/Obsidian"' >> ~/.zshrc
```

## Verwendung mit Task

Optional kannst du [Task](https://taskfile.dev) für komfortablere Befehle nutzen:

```bash
# Installation
brew install go-task

# Verfügbare Tasks
task --list

# Beispiele
task organize           # Vollständige Organisation
task rename            # Nur Dateien umbenennen
task build-moc         # Maps of Content generieren
```
