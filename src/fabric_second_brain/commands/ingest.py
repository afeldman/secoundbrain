"""Ingest documents and media files into Second Brain.

This module provides the ingest command to process various document
and media formats, extract content, summarize with AI, and store
in the Obsidian vault.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from fabric_second_brain.color import error, info, magenta, success
from fabric_second_brain.config import SBConfig
from fabric_second_brain.fabric import run_fabric_capture
from fabric_second_brain.processors import DocumentProcessor, MediaProcessor
from fabric_second_brain.utils import load_wisdom_template, slugify


def cmd_ingest(
    cfg: SBConfig,
    file_path: str,
    into_vault: bool,
    output_file: str | None,
    title: str | None,
    tags_raw: str | None,
    category: str | None,
) -> int:
    """Ingest documents and media files into Second Brain.

    Supports various document formats (PDF, DOCX, XLSX, CSV, etc.) and
    media files (audio, video). Extracts content, summarizes with AI,
    and stores in Obsidian vault.

    Args:
        cfg: Configuration instance.
        file_path: Path to file to ingest.
        into_vault: If True, save to vault's Inbox/ directory.
        output_file: Explicit output file path.
        title: Override for auto-generated title.
        tags_raw: Comma-separated list of tags.
        category: Category for vault organization (e.g., 'Literature', 'Media').

    Returns:
        0 on success, non-zero on error.
    """
    path = Path(file_path).expanduser()

    if not path.exists():
        print(error(f"❌ File not found: {path}"))
        return 1

    print(
        info("📥 Ingesting file: ")
        + magenta(str(path.name))
        + info(f" (model={cfg.model}, vendor={cfg.vendor})")
    )

    # Initialize processors
    doc_processor = DocumentProcessor()
    media_processor = MediaProcessor()

    content = ""
    file_type = "document"

    # Try to extract content
    try:
        if doc_processor.is_supported(path):
            print(info("📄 Extracting text from document..."))
            content = doc_processor.extract_text(path)
            file_type = "document"
        elif media_processor.is_supported(path):
            print(info("🎬 Processing media file..."))
            print(
                info(
                    "Note: Media transcription requires external services. "
                    "Using file metadata for now."
                )
            )
            duration = media_processor.get_duration(path)
            content = (
                f"Media file: {path.name}\n"
                f"Type: {path.suffix}\n"
                f"Duration: {duration:.1f} seconds\n\n"
                "For full transcription, use: second-brain wisdom --youtube <url>"
            )
            file_type = "media"
        else:
            print(
                error(
                    f"❌ Unsupported file format: {path.suffix}\n"
                    f"Supported documents: {', '.join(sorted(doc_processor.SUPPORTED_EXTENSIONS))}\n"
                    f"Supported media: {', '.join(sorted(media_processor.SUPPORTED_EXTENSIONS))}"
                )
            )
            return 1
    except Exception as e:
        print(error(f"❌ Content extraction failed: {e}"))
        return 1

    # Summarize with Fabric
    if content and file_type == "document":
        print(info("🤖 Generating AI summary..."))

        # Write content to temporary file for Fabric
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        try:
            rc, stdout, stderr = run_fabric_capture(cfg, ["summarize", tmp_path])

            if rc != 0:
                print(error("❌ Fabric summarize returned an error."))
                if stderr:
                    print(error(stderr))
                # Use extracted content as fallback
                summary = content[:1000] + "..." if len(content) > 1000 else content
            else:
                summary = stdout.strip() or content
        finally:
            Path(tmp_path).unlink(missing_ok=True)
    else:
        summary = content

    # Generate title and slug
    if not title:
        title = path.stem.replace("_", " ").replace("-", " ").title()

    slug = slugify(path.stem)
    tags = [t.strip() for t in (tags_raw or "").split(",") if t.strip()]
    tags_str = ", ".join(tags) if tags else ""

    # Determine vault category
    if not category:
        category = "Media" if file_type == "media" else "Inbox"

    # Create markdown note
    template = load_wisdom_template()
    md_content = template.format(
        title=title,
        source=str(path),
        summary=summary,
        tags=tags_str,
    )

    # Determine output path
    output_path: Path | None = None

    if output_file:
        output_path = Path(output_file).expanduser()
    elif into_vault:
        vault = cfg.vault_path
        category_dir = vault / category
        category_dir.mkdir(parents=True, exist_ok=True)
        output_path = category_dir / f"{slug}.md"

    if output_path is None:
        print(info("\n--- Document Summary (stdout) ---\n"))
        print(md_content)
        print(info("\n--- End ---"))
        return 0

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(md_content, encoding="utf-8")
    print(success(f"✅ Note written to: {output_path}"))

    return 0
