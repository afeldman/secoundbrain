"""Utility functions for CLI commands.

This module provides common helper functions used across CLI commands.

Functions:
    check_command_exists: Check if a command is available in PATH
    check_lmstudio_server: Check if LM Studio server is reachable
    get_template_dir: Get the templates directory
    ensure_default_wisdom_template: Create default wisdom template
    load_wisdom_template: Load a wisdom template by name
    generate_slug: Generate URL-safe slug from text
    slugify: Convert text to URL-friendly slug
    derive_slug_from_source: Derive slug from PDF or YouTube URL
    default_title_from_slug: Generate title from slug
"""

import re
import shutil
import socket
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from platformdirs import PlatformDirs

from fabric_second_brain.config import APP_AUTHOR, APP_NAME


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


def generate_slug(text: str) -> str:
    """Generate a URL-safe slug from text.

    Args:
        text: Input text to convert to slug

    Returns:
        URL-safe slug (lowercase, alphanumeric with hyphens)

    Example:
        >>> generate_slug("Hello World!")
        "hello-world"
    """
    # Convert to lowercase
    slug = text.lower()
    # Replace spaces and special chars with hyphens
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_-]+", "-", slug)
    # Remove leading/trailing hyphens
    slug = slug.strip("-")
    return slug


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
