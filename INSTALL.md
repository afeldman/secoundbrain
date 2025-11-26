# Installation Guide

## Core Requirements

```bash
# Install Python 3.11+
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Fabric Second Brain
cd fabric-second-brain
uv pip install -e .
```

## Optional Dependencies

For full document and media support, install these optional tools:

### macOS (Homebrew)

```bash
# Document processing
brew install pandoc        # Universal document converter
brew install poppler       # PDF tools (includes pdftotext)
brew install ghostscript   # PostScript processing

# Media processing
brew install ffmpeg        # Audio/video processing
```

### Ubuntu/Debian

```bash
# Document processing
sudo apt update
sudo apt install -y pandoc poppler-utils ghostscript

# Media processing
sudo apt install -y ffmpeg
```

### Arch Linux

```bash
# Document processing
sudo pacman -S pandoc poppler ghostscript

# Media processing
sudo pacman -S ffmpeg
```

## Verification

Check if tools are installed:

```bash
# Document tools
pandoc --version
pdftotext -v
ps2txt --version

# Media tools
ffmpeg -version
```

## Fabric AI Setup

Install and configure Fabric AI:

```bash
# Install Fabric
# See: https://github.com/danielmiessler/fabric

# Configure Fabric with your AI provider
fabric --setup
```

## LM Studio / Ollama (Optional)

For local AI models:

### LM Studio

1. Download from: https://lmstudio.ai
2. Install and launch
3. Download a model (e.g., smollm3-3b)
4. Start server mode

### Ollama

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama2
```

## Configuration

Initialize your Second Brain:

```bash
second-brain init
second-brain config set-model <your-model>
second-brain config set-vault ~/Obsidian
```

## Doctor Command

Verify your setup:

```bash
second-brain doctor
```

This will check:

- ✅ Fabric installation
- ✅ Vault path exists
- ✅ LM Studio/Ollama server connectivity
- ✅ Optional tools (pandoc, ffmpeg, etc.)
