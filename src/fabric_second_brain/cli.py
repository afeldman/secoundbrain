"""Command-line interface for Fabric Second Brain.

This module provides the main CLI implementation for interacting with
Fabric AI, Obsidian vaults, and LM Studio/Ollama models.
"""

from __future__ import annotations

import argparse
import re
import shutil
import socket
import subprocess
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from platformdirs import PlatformDirs

from .banner import print_banner
from .color import error, info, magenta, success
from .config import APP_AUTHOR, APP_NAME, SBConfig, load_config, save_config
from .document_processor import DocumentProcessor, MediaProcessor

# --- Helper Functions --------------------------------------------------------


def check_command_exists(cmd: str) -> bool:
    """Check if a command exists in PATH.

    Args:
        cmd: Command name to check.

    Returns:
        True if command is available, False otherwise.
    """
    return shutil.which(cmd) is not None


def check_lmstudio_server(host: str, port: int) -> bool:
    """Check if LM Studio server is reachable.

    Args:
        host: Server hostname or IP address.
        port: Server port number.

    Returns:
        True if server is reachable, False otherwise.
    """
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except OSError:
        return False


def get_template_dir() -> Path:
    """Get the directory for Markdown templates.

    Creates the templates directory if it doesn't exist.
    Example: ~/.config/fabric_second_brain/markdown_templates

    Returns:
        Path to the markdown templates directory.
    """
    dirs = PlatformDirs(APP_NAME, APP_AUTHOR)
    config_dir = Path(dirs.user_config_dir)
    templates_dir = config_dir / "markdown_templates"
    templates_dir.mkdir(parents=True, exist_ok=True)
    return templates_dir


def ensure_default_wisdom_template() -> Path:
    """Ensure default wisdom template exists.

    Creates a default wisdom template if it doesn't exist.
    Template placeholders: {title}, {source}, {summary}, {tags}

    Returns:
        Path to the default wisdom template file.
    """
    templates_dir = get_template_dir()
    tpl_path = templates_dir / "wisdom_default.md"
    if tpl_path.exists():
        return tpl_path

    default_content = """# {title}

> Source: {source}
> Tags: {tags}

## Summary

{summary}

## Key Insights

-

## Notable Quotes

>

## Action Items

-

## Topics & Tags

{tags}
"""
    tpl_path.write_text(default_content, encoding="utf-8")
    return tpl_path


def load_wisdom_template(name: str = "wisdom_default.md") -> str:
    """Load a Markdown template from the templates directory.

    Args:
        name: Template filename. Defaults to 'wisdom_default.md'.

    Returns:
        Template content as string.
    """
    templates_dir = get_template_dir()
    path = templates_dir / name
    if not path.exists():
        path = ensure_default_wisdom_template()
    return path.read_text(encoding="utf-8")


def run_fabric(cfg: SBConfig, args: list[str]) -> int:
    """Execute Fabric command with arguments.

    Args:
        cfg: Configuration instance containing fabric_cmd.
        args: List of arguments to pass to Fabric.

    Returns:
        Return code from Fabric command.
    """
    cmd = [cfg.fabric_cmd, *args]
    try:
        return subprocess.call(cmd)
    except FileNotFoundError:
        print(
            error(
                f"❌ '{cfg.fabric_cmd}' not found in PATH – "
                "bitte in der Config (fabric_cmd) anpassen"
            )
        )
        return 1


def run_fabric_capture(cfg: SBConfig, args: list[str]) -> tuple[int, str, str]:
    """Execute Fabric command and capture output.

    Args:
        cfg: Configuration instance containing fabric_cmd.
        args: List of arguments to pass to Fabric.

    Returns:
        Tuple of (return_code, stdout, stderr).
    """
    cmd = [cfg.fabric_cmd, *args]
    try:
        proc = subprocess.run(
            cmd,
            text=True,
            capture_output=True,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except FileNotFoundError:
        msg = f"❌ '{cfg.fabric_cmd}' not found in PATH – bitte in der Config (fabric_cmd) anpassen"
        print(error(msg))
        return 1, "", msg


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug.

    Converts to lowercase, replaces non-alphanumeric characters with hyphens,
    and trims leading/trailing hyphens.

    Args:
        text: Text to slugify.

    Returns:
        Slugified string, defaults to 'wisdom' if empty.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "wisdom"


def derive_slug_from_source(pdf: str | None, youtube: str | None) -> str:
    """Derive a slug from PDF filename or YouTube URL.

    Args:
        pdf: Path to PDF file, if applicable.
        youtube: YouTube URL, if applicable.

    Returns:
        Slug string prefixed with 'wisdom-'.
    """
    if pdf:
        base = Path(pdf).stem
    else:
        url = youtube or ""
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        base = qs["v"][0] if qs.get("v") else Path(parsed.path).stem or parsed.netloc or "wisdom"
    return f"wisdom-{slugify(base)}"


def default_title_from_slug(slug: str) -> str:
    """Generate human-readable title from slug.

    Converts slug like 'wisdom-the-power-of-focus' to 'The Power Of Focus'.

    Args:
        slug: Slug string to convert.

    Returns:
        Title-cased string, defaults to 'Wisdom' if empty.
    """
    core = slug[len("wisdom-") :] if slug.startswith("wisdom-") else slug
    return core.replace("-", " ").title() or "Wisdom"


# --- Commands: Core ----------------------------------------------------------


def cmd_classify(cfg: SBConfig, path: str | None) -> int:
    """Auto-classify notes in the vault using Fabric AI.

    Args:
        cfg: Configuration instance.
        path: Optional override for vault path.

    Returns:
        Return code from Fabric classify command.
    """
    vault = Path(path) if path else cfg.vault_path
    print(info(f"📂 Auto-classifying notes in {vault} (model={cfg.model})"))
    return run_fabric(cfg, ["classify", "--path", str(vault)])


def cmd_search(cfg: SBConfig, query: str) -> int:
    """Perform semantic search in the vault.

    Args:
        cfg: Configuration instance.
        query: Search query string.

    Returns:
        Return code from Fabric search command.
    """
    print(
        info("🔍 Semantic search: ")
        + magenta(query)
        + info(f" (model={cfg.model}, vendor={cfg.vendor})")
    )
    return run_fabric(cfg, ["search", query])


def cmd_organize(cfg: SBConfig, path: str | None) -> int:
    """Organize vault folders using AI.

    Args:
        cfg: Configuration instance.
        path: Optional override for vault path.

    Returns:
        Return code from Fabric organize command.
    """
    vault = Path(path) if path else cfg.vault_path
    print(info(f"🗂️  Organizing vault {vault} (model={cfg.model}, vendor={cfg.vendor})"))
    return run_fabric(cfg, ["organize", str(vault)])


def cmd_vision(cfg: SBConfig, image: str) -> int:
    """Perform vision analysis on an image.

    Args:
        cfg: Configuration instance.
        image: Path to image file.

    Returns:
        Return code from Fabric vision command.
    """
    print(info(f"🖼️  Vision analysis for {image} (model={cfg.model}, vendor={cfg.vendor})"))
    return run_fabric(cfg, ["vision", "analyze", image])


def cmd_summary(cfg: SBConfig, file: str) -> int:
    """Summarize a file using AI.

    Args:
        cfg: Configuration instance.
        file: Path to file to summarize.

    Returns:
        Return code from Fabric summarize command.
    """
    print(info(f"📝 Summarizing {file} (model={cfg.model}, vendor={cfg.vendor})"))
    return run_fabric(cfg, ["summarize", file])


# --- Commands: Config --------------------------------------------------------


def cmd_config_show(cfg: SBConfig) -> int:
    """Display current configuration.

    Args:
        cfg: Configuration instance to display.

    Returns:
        Always returns 0 (success).
    """
    print(success("Current Second Brain configuration:\n"))
    print(f"{info('model:       ')} {cfg.model}")
    print(f"{info('vault_path:  ')} {cfg.vault_path}")
    print(f"{info('vendor:      ')} {cfg.vendor}")
    print(f"{info('fabric_cmd:  ')} {cfg.fabric_cmd}")
    return 0


def cmd_config_set_model(cfg: SBConfig, model: str) -> int:
    """Set the default AI model in configuration.

    Args:
        cfg: Configuration instance to update.
        model: Model name to set.

    Returns:
        Always returns 0 (success).
    """
    cfg.model = model
    save_config(cfg)
    print(success(f"✅ model set to: {model}"))
    return 0


def cmd_config_set_vault(cfg: SBConfig, vault: str) -> int:
    """Set the Obsidian vault path in configuration.

    Args:
        cfg: Configuration instance to update.
        vault: Path to Obsidian vault.

    Returns:
        Always returns 0 (success).
    """
    cfg.vault_path = Path(vault).expanduser()
    save_config(cfg)
    print(success(f"✅ vault_path set to: {cfg.vault_path}"))
    return 0


def cmd_config_set_fabric(cfg: SBConfig, fabric_cmd: str) -> int:
    """Set the Fabric command in configuration.

    Args:
        cfg: Configuration instance to update.
        fabric_cmd: Fabric command name or path.

    Returns:
        Always returns 0 (success).
    """
    cfg.fabric_cmd = fabric_cmd
    save_config(cfg)
    print(success(f"✅ fabric_cmd set to: {fabric_cmd}"))
    return 0


# --- Wisdom Extractor --------------------------------------------------------


def cmd_wisdom(
    cfg: SBConfig,
    pdf: str | None,
    youtube: str | None,
    into_vault: bool,
    output_file: str | None,
    title: str | None,
    tags_raw: str | None,
) -> int:
    """Extract wisdom from a PDF or YouTube URL.

    Uses Fabric summarize to process the source and generates a
    formatted markdown wisdom note using a template.

    Args:
        cfg: Configuration instance.
        pdf: Path to PDF file, if applicable.
        youtube: YouTube URL, if applicable.
        into_vault: If True, save to vault's Wisdom/ directory.
        output_file: Explicit output file path.
        title: Override for auto-generated title.
        tags_raw: Comma-separated list of tags.

    Returns:
        0 on success, non-zero on error.
    """
    if pdf and youtube:
        print(error("❌ Bitte entweder --pdf ODER --youtube angeben, nicht beides."))
        return 1

    if not pdf and not youtube:
        print(error("❌ Bitte --pdf <file.pdf> oder --youtube <url> angeben."))
        return 1

    source = pdf or youtube or ""

    if pdf:
        path = Path(pdf)
        if not path.exists():
            print(error(f"❌ PDF not found: {path}"))
            return 1

    print(
        info("✨ Wisdom Extractor für: ")
        + magenta(source)
        + info(f" (model={cfg.model}, vendor={cfg.vendor})")
    )

    rc, stdout, stderr = run_fabric_capture(cfg, ["summarize", source])

    if rc != 0:
        print(error("❌ Fabric summarize returned an error."))
        if stderr:
            print(error(stderr))
        return rc

    summary = stdout.strip()
    if not summary:
        print(error("❌ Fabric summarize returned empty output."))
        return 1

    slug = derive_slug_from_source(pdf, youtube)
    final_title = title or default_title_from_slug(slug)
    tags = [t.strip() for t in (tags_raw or "").split(",") if t.strip()]
    tags_str = ", ".join(tags) if tags else ""

    template = load_wisdom_template()
    md_content = template.format(
        title=final_title,
        source=source,
        summary=summary,
        tags=tags_str,
    )

    output_path: Path | None = None

    if output_file:
        output_path = Path(output_file).expanduser()
    elif into_vault:
        vault = cfg.vault_path
        wisdom_dir = vault / "Wisdom"
        wisdom_dir.mkdir(parents=True, exist_ok=True)
        output_path = wisdom_dir / f"{slug}.md"

    if output_path is None:
        print(info("\n--- Wisdom Markdown (stdout) ---\n"))
        print(md_content)
        print(info("\n--- End ---"))
        return 0

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(md_content, encoding="utf-8")
    print(success(f"✅ Wisdom file written to: {output_path}"))
    return 0


# --- Debug & Doctor ----------------------------------------------------------


def cmd_debug(cfg: SBConfig, lm_host: str, lm_port: int) -> int:
    """Display debug information about system setup.

    Args:
        cfg: Configuration instance.
        lm_host: LM Studio server host.
        lm_port: LM Studio server port.

    Returns:
        Always returns 0 (success).
    """
    print(info("🔧 Second-Brain Debug Information"))
    print("-----------------------------------")
    print(f"Fabric command:     {cfg.fabric_cmd}")
    print(f"Fabric installed:   {'✅' if check_command_exists(cfg.fabric_cmd) else '❌'}")
    print(f"Vendor:             {cfg.vendor}")
    print(f"Model:              {cfg.model}")
    print(f"Vault path:         {cfg.vault_path}")
    print(f"LM Studio host:     {lm_host}")
    print(f"LM Studio port:     {lm_port}")

    if cfg.vendor == "lmstudio":
        print(
            f"LM Studio server:   "
            f"{'✅ reachable' if check_lmstudio_server(lm_host, lm_port) else '❌ not reachable'}"
        )

    if cfg.vendor == "ollama":
        print("Ollama:             (no active HTTP check implemented, vendor=ollama)")

    return 0


def cmd_doctor(cfg: SBConfig, lm_host: str, lm_port: int) -> int:
    """Run system diagnostics and check component availability.

    Verifies Fabric installation, vault path, and server connectivity.

    Args:
        cfg: Configuration instance.
        lm_host: LM Studio server host.
        lm_port: LM Studio server port.

    Returns:
        Number of problems found (0 if all OK).
    """
    print(info("🩺 Running Second-Brain Doctor"))
    print("-----------------------------------")

    problems = 0

    if not check_command_exists(cfg.fabric_cmd):
        print(error(f"❌ {cfg.fabric_cmd} not installed or not in PATH"))
        problems += 1
    else:
        print(success(f"✅ {cfg.fabric_cmd} found in PATH"))

    if not cfg.vault_path.exists():
        print(error(f"❌ vault path does not exist: {cfg.vault_path}"))
        problems += 1
    else:
        print(success(f"✅ vault path exists: {cfg.vault_path}"))

    if cfg.vendor == "lmstudio":
        if check_lmstudio_server(lm_host, lm_port):
            print(success(f"✅ LM Studio server reachable at {lm_host}:{lm_port}"))
        else:
            print(
                error(
                    f"❌ LM Studio server not reachable at {lm_host}:{lm_port} – "
                    "please start server mode"
                )
            )
            problems += 1

    if cfg.vendor == "ollama":
        if check_command_exists("ollama"):
            print(success("✅ ollama CLI found"))
        else:
            print(error("❌ ollama CLI not found in PATH"))
            problems += 1

    if problems == 0:
        print(success("🎉 System OK – everything looks good!"))
    else:
        print(error(f"⚠ Found {problems} problem(s)."))

    return problems


def cmd_wisdom_summary(
    cfg: SBConfig,
    pdf: str | None,
    youtube: str | None,
    into_vault: bool,
    output_file: str | None,
    title: str | None,
    tags_raw: str | None,
) -> int:
    """Create wisdom note and a second-level summary.

    Like cmd_wisdom, but additionally creates a summary of the
    wisdom note itself and saves it as <slug>-summary.md.

    Args:
        cfg: Configuration instance.
        pdf: Path to PDF file, if applicable.
        youtube: YouTube URL, if applicable.
        into_vault: If True, save to vault's Wisdom/ directory.
        output_file: Explicit output file path.
        title: Override for auto-generated title.
        tags_raw: Comma-separated list of tags.

    Returns:
        0 on success, non-zero on error.
    """
    if pdf and youtube:
        print(error("❌ Bitte entweder --pdf ODER --youtube angeben, nicht beides."))
        return 1

    if not pdf and not youtube:
        print(error("❌ Bitte --pdf <file.pdf> oder --youtube <url> angeben."))
        return 1

    source = pdf or youtube or ""

    if pdf:
        path = Path(pdf)
        if not path.exists():
            print(error(f"❌ PDF not found: {path}"))
            return 1

    print(
        info("✨ Wisdom+Summary für: ")
        + magenta(source)
        + info(f" (model={cfg.model}, vendor={cfg.vendor})")
    )

    # 1) Erste Zusammenfassung direkt von der Quelle
    rc, stdout, stderr = run_fabric_capture(cfg, ["summarize", source])

    if rc != 0:
        print(error("❌ Fabric summarize (Quelle) returned an error."))
        if stderr:
            print(error(stderr))
        return rc

    base_summary = stdout.strip()
    if not base_summary:
        print(error("❌ Fabric summarize (Quelle) returned empty output."))
        return 1

    # 2) Wisdom-Note aus Summary bauen
    slug = derive_slug_from_source(pdf, youtube)
    final_title = title or default_title_from_slug(slug)
    tags = [t.strip() for t in (tags_raw or "").split(",") if t.strip()]
    tags_str = ", ".join(tags) if tags else ""

    template = load_wisdom_template()
    wisdom_md = template.format(
        title=final_title,
        source=source,
        summary=base_summary,
        tags=tags_str,
    )

    # 3) Speicherort für Wisdom bestimmen
    wisdom_path: Path | None = None

    if output_file:
        wisdom_path = Path(output_file).expanduser()
    elif into_vault:
        vault = cfg.vault_path.expanduser()
        wisdom_dir = vault / "Wisdom"
        wisdom_dir.mkdir(parents=True, exist_ok=True)
        wisdom_path = wisdom_dir / f"{slug}.md"
    else:
        print(error("❌ wisdom-summary benötigt entweder --into-vault oder --output-file"))
        return 1

    wisdom_path.parent.mkdir(parents=True, exist_ok=True)
    wisdom_path.write_text(wisdom_md, encoding="utf-8")
    print(success(f"✅ Wisdom note written to: {wisdom_path}"))

    # 4) Zweite Zusammenfassung (Summary der Wisdom-Note)
    rc2, stdout2, stderr2 = run_fabric_capture(cfg, ["summarize", str(wisdom_path)])

    if rc2 != 0:
        print(error("❌ Fabric summarize (Wisdom-Note) returned an error."))
        if stderr2:
            print(error(stderr2))
        return rc2

    summary2 = stdout2.strip()
    if not summary2:
        print(error("❌ Fabric summarize (Wisdom-Note) returned empty output."))
        return 1

    summary_title = f"{final_title} – Summary"
    summary_path = wisdom_path.with_name(f"{wisdom_path.stem}-summary{wisdom_path.suffix}")

    summary_md = f"# {summary_title}\n\n> Source wisdom note: {wisdom_path.name}\n\n{summary2}\n"

    summary_path.write_text(summary_md, encoding="utf-8")
    print(success(f"✅ Summary note written to: {summary_path}"))
    return 0


# --- Ingest Command ----------------------------------------------------------


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
        import tempfile

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


# --- ArgumentParser ----------------------------------------------------------
# --- ArgumentParser ----------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the CLI.

    Returns:
        Configured ArgumentParser instance with all subcommands.
    """
    parser = argparse.ArgumentParser(
        prog="second-brain",
        description="Second Brain CLI for Fabric AI + Obsidian + LM Studio/Ollama",
    )

    parser.add_argument(
        "--vendor",
        choices=["lmstudio", "ollama"],
        help="Override vendor from config for this run",
    )
    parser.add_argument(
        "--model",
        help="Override model from config for this run",
    )
    parser.add_argument(
        "--lmstudio-host",
        default="127.0.0.1",
        help="LM Studio server host (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--lmstudio-port",
        type=int,
        default=1234,
        help="LM Studio server port (default: 1234)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_classify = sub.add_parser("classify", help="Auto-classify notes in the vault")
    p_classify.add_argument("--path", help="Override vault path")

    p_search = sub.add_parser("search", help="Semantic search in your vault")
    p_search.add_argument("query", nargs=argparse.REMAINDER, help="Search query")

    p_organize = sub.add_parser("organize", help="Organize vault folders using AI")
    p_organize.add_argument("--path", help="Override vault path")

    p_vision = sub.add_parser("vision", help="Vision analysis on an image")
    p_vision.add_argument("image", help="Path to image file")

    p_summary = sub.add_parser("summary", help="Summarize a file")
    p_summary.add_argument("file", help="Path to file")

    sub.add_parser("init", help="Initialize a Second-Brain Obsidian vault structure")

    # === Ingest Command ===
    p_ingest = sub.add_parser(
        "ingest",
        help="Ingest documents and media files into Second Brain vault",
    )
    p_ingest.add_argument("file", help="Path to document or media file")
    p_ingest.add_argument(
        "--into-vault",
        action="store_true",
        help="Save note into Obsidian vault",
    )
    p_ingest.add_argument(
        "--output-file",
        help="Explicit output markdown file path",
    )
    p_ingest.add_argument(
        "--title",
        help="Override auto-generated title for the note",
    )
    p_ingest.add_argument(
        "--tags",
        help="Comma-separated list of tags",
    )
    p_ingest.add_argument(
        "--category",
        help="Vault category (e.g., 'Literature', 'Media', 'Inbox'). Default: auto-detect",
    )

    # === Wisdom+Summary (Pipeline) ===
    p_wisum = sub.add_parser(
        "wisdom-summary",
        help="Create a wisdom note from a source and a second-level summary note",
    )
    group2 = p_wisum.add_mutually_exclusive_group(required=True)
    group2.add_argument("--pdf", help="Path to a PDF file")
    group2.add_argument("--youtube", help="YouTube URL")
    p_wisum.add_argument(
        "--into-vault",
        action="store_true",
        help="Write wisdom + summary markdown into Obsidian vault under 'Wisdom/'",
    )
    p_wisum.add_argument(
        "--output-file",
        help="Explicit wisdom markdown file path; summary will be stored next to it",
    )
    p_wisum.add_argument(
        "--title",
        help="Override auto-generated title for the wisdom note",
    )
    p_wisum.add_argument(
        "--tags",
        help="Comma-separated list of tags to include in the wisdom note",
    )

    p_wisdom = sub.add_parser(
        "wisdom",
        help="Extract wisdom from a PDF or YouTube URL using Fabric summarize",
    )
    group = p_wisdom.add_mutually_exclusive_group(required=True)
    group.add_argument("--pdf", help="Path to a PDF file")
    group.add_argument("--youtube", help="YouTube URL")
    p_wisdom.add_argument(
        "--into-vault",
        action="store_true",
        help="Write wisdom markdown into Obsidian vault under 'Wisdom/'",
    )
    p_wisdom.add_argument(
        "--output-file",
        help="Explicit output markdown file path",
    )
    p_wisdom.add_argument(
        "--title",
        help="Override auto-generated title for the wisdom note",
    )
    p_wisdom.add_argument(
        "--tags",
        help="Comma-separated list of tags to include in the wisdom note",
    )

    p_config = sub.add_parser("config", help="Show or modify configuration")
    cfg_sub = p_config.add_subparsers(dest="config_command", required=True)

    cfg_sub.add_parser("show", help="Show current configuration")

    cfg_set_model = cfg_sub.add_parser("set-model", help="Set default model")
    cfg_set_model.add_argument("model")

    cfg_set_vault = cfg_sub.add_parser("set-vault", help="Set Obsidian vault path")
    cfg_set_vault.add_argument("vault")

    cfg_set_fabric = cfg_sub.add_parser("set-fabric-cmd", help="Set fabric command")
    cfg_set_fabric.add_argument("fabric_cmd")

    sub.add_parser("debug", help="Show debug information")
    sub.add_parser("doctor", help="Run system diagnostics")

    return parser


# --- Init Command ------------------------------------------------------------


def cmd_init(cfg: SBConfig) -> int:
    """Initialize Second Brain vault structure.

    Prompts for vault path, creates necessary directories, copies templates,
    and creates a README file.

    Args:
        cfg: Configuration instance to update.

    Returns:
        Always returns 0 (success).
    """
    print(info("🧠 Second-Brain Init"))
    print("-----------------------------------")
    print(info(f"Aktueller Vault-Pfad in der Config: {magenta(str(cfg.vault_path))}"))
    new_path = input("Neuer Vault-Pfad (leer lassen für aktuellen Wert): ").strip()

    if new_path:
        vault = Path(new_path).expanduser()
        cfg.vault_path = vault
        save_config(cfg)
        print(success(f"✅ vault_path in der Config aktualisiert: {vault}"))
    else:
        vault = cfg.vault_path.expanduser()
        print(info(f"➡️  Verwende bestehenden Vault-Pfad: {vault}"))

    print(info(f"🚀 Initializing Second Brain at: {vault}"))

    # 1. Vault erstellen
    vault.mkdir(parents=True, exist_ok=True)

    # 2. Standardverzeichnisse
    folders = [
        "Wisdom",
        "Daily",
        "Inbox",
        "Literature",
        "Media",
        "Templates",
    ]

    for f in folders:
        (vault / f).mkdir(parents=True, exist_ok=True)

    # 3. Templates kopieren
    from .config import get_template_dir

    template_src = get_template_dir()
    template_dst = vault / "Templates"

    copied = 0
    for tpl in template_src.iterdir():
        if tpl.is_file() and tpl.suffix == ".md":
            target = template_dst / tpl.name
            if not target.exists():
                target.write_text(tpl.read_text(encoding="utf-8"), encoding="utf-8")
                copied += 1

    # 4. README
    readme = vault / "README.md"
    if not readme.exists():
        readme.write_text(
            (
                "# Second Brain Vault\n\n"
                "Dies ist dein persönliches Second Brain, bereit für "
                "## Struktur\n"
                "- Wisdom/ — extrahiertes Wissen aus Quellen (PDF, YouTube, Webseiten)\n"
                "- Literature/ — Buchnotizen, Paper, Dokumente\n"
                "- Media/ — Audio- und Videodateien, Musik\n"
                "- Inbox/ — Rohnotizen, unfertig\n"
                "- Daily/ — tägliche Logbücher, Journals\n"
                "- Templates/ — Markdown-Templates für Auto-Generierung\n\n"
                "- Templates/ — Markdown-Templates für Auto-Generierung\n\n"
                "Erstellt von **fabric-second-brain**.\n"
            ),
            encoding="utf-8",
        )

    print(success("🎉 Second-Brain Vault initialized!"))
    print(success(f"📁 Path: {vault}"))
    print(success(f"📄 Copied templates: {copied}"))
    return 0


# --- Main --------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the CLI.

    Args:
        argv: Command-line arguments. Uses sys.argv[1:] if None.

    Returns:
        Exit code (0 for success, non-zero for errors).
    """
    print_banner()

    argv = argv or sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)

    cfg = load_config()

    if args.vendor is not None:
        cfg.vendor = args.vendor
    if args.model is not None:
        cfg.model = args.model

    lm_host = args.lmstudio_host
    lm_port = args.lmstudio_port

    if args.command == "classify":
        return cmd_classify(cfg, args.path)

    if args.command == "search":
        if not args.query:
            print(error("Usage: second-brain search <query>"))
            return 1
        return cmd_search(cfg, " ".join(args.query))

    if args.command == "organize":
        return cmd_organize(cfg, args.path)

    if args.command == "vision":
        return cmd_vision(cfg, args.image)

    if args.command == "summary":
        return cmd_summary(cfg, args.file)

    if args.command == "ingest":
        return cmd_ingest(
            cfg,
            file_path=args.file,
            into_vault=getattr(args, "into_vault", False),
            output_file=getattr(args, "output_file", None),
            title=getattr(args, "title", None),
            tags_raw=getattr(args, "tags", None),
            category=getattr(args, "category", None),
        )

    if args.command == "wisdom":
        return cmd_wisdom(
            cfg,
            pdf=getattr(args, "pdf", None),
            youtube=getattr(args, "youtube", None),
            into_vault=getattr(args, "into_vault", False),
            output_file=getattr(args, "output_file", None),
            title=getattr(args, "title", None),
            tags_raw=getattr(args, "tags", None),
        )

    if args.command == "wisdom-summary":
        return cmd_wisdom_summary(
            cfg,
            pdf=getattr(args, "pdf", None),
            youtube=getattr(args, "youtube", None),
            into_vault=getattr(args, "into_vault", False),
            output_file=getattr(args, "output_file", None),
            title=getattr(args, "title", None),
            tags_raw=getattr(args, "tags", None),
        )

    if args.command == "config":
        if args.config_command == "show":
            return cmd_config_show(cfg)
        if args.config_command == "set-model":
            return cmd_config_set_model(cfg, args.model)
        if args.config_command == "set-vault":
            return cmd_config_set_vault(cfg, args.vault)
        if args.config_command == "set-fabric-cmd":
            return cmd_config_set_fabric(cfg, args.fabric_cmd)

    if args.command == "debug":
        return cmd_debug(cfg, lm_host, lm_port)

    if args.command == "doctor":
        return cmd_doctor(cfg, lm_host, lm_port)

    if args.command == "init":
        return cmd_init(cfg)

    print(error("Unknown command"))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
