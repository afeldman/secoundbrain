# Taskfile Usage Guide

This project uses [Task](https://taskfile.dev) for task automation. Task is a modern alternative to Make with a simpler syntax.

## Installation

```bash
brew install go-task
```

## Quick Start

```bash
# Show all available tasks
task --list

# Complete setup (install all dependencies)
task setup

# Run code quality checks
task check

# Auto-fix issues
task fix

# Run the application
task run CLI_ARGS="--help"
```

## Common Tasks

### Development

```bash
task install              # Install project dependencies
task install-dev          # Install development tools
task install-optional     # Install optional system dependencies (pandoc, ffmpeg, etc.)
task install-fabric       # Install Fabric AI

task dev                  # Development mode
task doctor               # Run diagnostics
task debug                # Show debug info
```

### Code Quality

```bash
task lint                 # Run linter
task lint-fix             # Run linter with auto-fix
task format               # Format code
task format-check         # Check formatting without changes
task typecheck            # Run type checking

task check                # Run all checks
task fix                  # Auto-fix all issues
```

### Testing

```bash
task test                 # Run tests (when available)
task test-ingest          # Test document ingestion
```

### Application Commands

```bash
task init                 # Initialize Obsidian vault
task config               # Show configuration
task doctor               # Run system diagnostics

# Vault management
task vault-init           # Initialize vault
task vault-organize       # AI-powered organization
task vault-classify       # Auto-classify notes
```

### Git Workflow

```bash
task commit               # Run checks before commit
task pre-commit           # Pre-commit hook
task tag TAG=v0.2.0       # Create and push git tag
```

### Cleanup

```bash
task clean                # Remove caches and generated files
task clean-logs           # Remove log files
task clean-all            # Full cleanup including venv
```

### Build & Release

```bash
task build                # Build distribution packages
task publish-test         # Publish to TestPyPI
task publish              # Publish to PyPI
```

### Utilities

```bash
task version              # Show version
task deps                 # Show dependencies
task deps-outdated        # Check for updates
task deps-update          # Update dependencies
task tree                 # Show project structure

task docs                 # Show README
task docs-install         # Show installation guide
task docs-changelog       # Show changelog
```

## Custom Task Execution

Run the CLI with custom arguments:

```bash
task run CLI_ARGS="ingest document.pdf --title 'My Doc' --tags 'important'"
task run CLI_ARGS="wisdom https://youtube.com/watch?v=example"
task run CLI_ARGS="search 'machine learning'"
```

## Pre-Commit Hook

To automatically run checks before commits:

```bash
# Add to .git/hooks/pre-commit
#!/bin/bash
task pre-commit
```

## Tips

- Use `task --summary <taskname>` to see task description
- Use `task --list-all` to show all tasks including internal ones
- Tasks can be chained: `task clean check build`
- Set variables: `task tag TAG=v1.0.0`

## Troubleshooting

If a task fails:

1. Run `task doctor` to check system dependencies
2. Run `task install` to ensure dependencies are up-to-date
3. Run `task clean` to clear caches
4. Check logs in the `logs/` directory

## Task Dependencies

Some tasks depend on system tools:

- `install-optional`: Requires `brew` (macOS)
- `install-fabric`: Requires `go`
- `watch`: Requires `fswatch` on macOS
- `tree`: Requires `tree` utility

Install missing tools:

```bash
brew install fswatch tree
```
