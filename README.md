# Fabric Second Brain

Second Brain CLI around Fabric AI + Obsidian + LM Studio/Ollama

## Quick Start

```bash
# Install Task runner (if not installed)
brew install go-task

# Complete setup
task setup

# Or install manually
uv pip install -e .

# Show all available tasks
task --list
```

## Task Runner

This project uses [Task](https://taskfile.dev) for automation. See [TASKS.md](TASKS.md) for detailed usage.

Common commands:
```bash
task install              # Install dependencies
task check                # Run all code quality checks
task fix                  # Auto-fix issues
task doctor               # Run diagnostics
task test-ingest          # Test document ingestion
```

## Usage

```bash
# Initialize your Second Brain vault
second-brain init

# Configure
second-brain config show
second-brain config set-model <model-name>
second-brain config set-vault <path-to-obsidian-vault>

# Ingest documents and media files
second-brain ingest document.pdf --into-vault
second-brain ingest spreadsheet.xlsx --into-vault --category Literature
second-brain ingest presentation.pptx --into-vault --tags "work,presentation"
second-brain ingest video.mp4 --into-vault --category Media

# Extract wisdom from sources
second-brain wisdom --pdf document.pdf --into-vault
second-brain wisdom --youtube https://www.youtube.com/watch?v=... --into-vault

# Search your vault
second-brain search "your query"

# Classify notes
second-brain classify

# Organize vault
second-brain organize

# System diagnostics
second-brain doctor
```

## Features

- 🧠 Extract wisdom from PDFs and YouTube videos
- 📄 Ingest documents (PDF, DOCX, XLSX, CSV, ODT, RTF, etc.)
- 🎬 Process media files (MP4, MP3, WAV, etc.)
- 🔍 Semantic search in your Obsidian vault
- 📝 Auto-classify and organize notes
- 🖼️ Vision analysis for images
- ⚙️ Support for LM Studio and Ollama
- 📁 Template-based note generation

## Supported Formats

### Documents

- PDF, DOC/DOCX, ODT, RTF
- XLS/XLSX, ODS, CSV
- PPT/PPTX, ODP
- PostScript (PS/EPS)
- E-books (EPUB, MOBI)
- Plain text (TXT, MD)

### Media

- Video: MP4, AVI, MOV, MKV, WebM
- Audio: MP3, WAV, M4A, FLAC, OGG
- YouTube (via URL)

## Requirements

- Python ≥3.11
- Fabric AI CLI
- LM Studio or Ollama (optional)

### Optional Tools (for better document support)

```bash
# macOS
brew install pandoc poppler ghostscript ffmpeg

# Ubuntu/Debian
sudo apt install pandoc poppler-utils ghostscript ffmpeg
```

## Development

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run linters
uv run ruff check src/
uv run mypy src/

# Format code
uv run ruff format src/
```
