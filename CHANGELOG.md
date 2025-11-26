# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-26

### Added

- Initial release of Fabric Second Brain CLI
- Core command-line interface with subcommands:
  - `init` - Initialize Obsidian vault structure
  - `config` - Manage configuration (show, set-model, set-vault, set-fabric-cmd)
  - `classify` - Auto-classify notes in vault
  - `search` - Semantic search in vault
  - `organize` - AI-powered vault organization
  - `vision` - Vision analysis for images
  - `summary` - Summarize files
  - `wisdom` - Extract wisdom from PDFs and YouTube
  - `wisdom-summary` - Create wisdom note + second-level summary
  - `ingest` - Process documents and media files
  - `debug` - Show debug information
  - `doctor` - Run system diagnostics

### Document Processing

- Support for multiple document formats:
  - PDF (via pdftotext or pandoc)
  - Microsoft Office: DOC, DOCX, XLS, XLSX, PPT, PPTX
  - OpenOffice: ODT, ODS, ODP
  - Text: TXT, MD, CSV
  - PostScript: PS, EPS
  - E-books: EPUB, MOBI
- Automatic text extraction with fallback strategies
- Integration with pandoc for universal document conversion
- CSV parsing with table formatting

### Media Processing

- Media file support:
  - Video: MP4, AVI, MOV, MKV, WebM, FLV
  - Audio: MP3, WAV, M4A, FLAC, OGG, AAC
- Audio extraction from video files
- Duration detection for media files
- FFmpeg integration for processing

### AI Integration

- Fabric AI integration for summarization
- Support for LM Studio and Ollama
- Configurable AI models and vendors
- Automatic content summarization
- YouTube video processing

### Vault Management

- Auto-generated Obsidian vault structure:
  - Wisdom/ - Extracted knowledge
  - Literature/ - Documents and papers
  - Media/ - Audio and video
  - Inbox/ - Raw notes
  - Daily/ - Journals
  - Templates/ - Markdown templates
- Template-based note generation
- Automatic categorization
- Tag support
- Slug generation for filenames

### Code Quality

- Full type hints (mypy compliant)
- Ruff linting and formatting
- Google-style documentation
- Comprehensive error handling
- Logging with loguru

### Configuration

- Platform-aware config storage via platformdirs
- TOML-based configuration
- Per-run vendor/model overrides
- Template customization support

### Documentation

- Comprehensive README with examples
- Installation guide for all platforms
- Supported formats documentation
- Development setup instructions

[0.1.0]: https://github.com/yourusername/fabric-second-brain/releases/tag/v0.1.0
