"""Extract wisdom from various sources.

This module provides wisdom commands to extract insights from PDFs,
YouTube videos, and other sources using AI summarization.
"""

from __future__ import annotations

from pathlib import Path

from fabric_second_brain.color import error, info, magenta, success
from fabric_second_brain.config import SBConfig
from fabric_second_brain.fabric import run_fabric_capture
from fabric_second_brain.utils import (
    default_title_from_slug,
    derive_slug_from_source,
    load_wisdom_template,
)


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
