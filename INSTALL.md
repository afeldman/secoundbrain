# Installation Guide

## Schnellstart

```bash
# Repository klonen
git clone https://github.com/afeldman/fabric-second-brain.git
cd fabric-second-brain

# Python-Dependencies installieren
pip install -r requirements.txt

# Fabric AI installieren
go install github.com/danielmiessler/fabric@latest
fabric --setup

# Umgebungsvariable setzen
export OBSIDIAN_VAULT="$HOME/Obsidian"

# Organisation ausführen
./bootstrap-secondbrain.sh
```

## Voraussetzungen

- **Python** ≥ 3.11
- **Go** (für Fabric AI)
- **Obsidian** Vault

## Fabric AI Setup

Fabric ist das Herzstück für KI-gestützte Analyse:

```bash
# Installation
go install github.com/danielmiessler/fabric@latest

# Konfiguration (wähle deinen AI Provider)
fabric --setup
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
