#!/usr/bin/env python3
import os
from pathlib import Path
import frontmatter

VAULT = Path(os.environ.get("OBSIDIAN_VAULT", "~/Obsidian")).expanduser()

def has_frontmatter(text: str) -> bool:
    return text.lstrip().startswith("---")

def extract_title(body: str, filename: str) -> str:
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
        return stripped
    return Path(filename).stem

def main():
    print(f"🔎 Scanning vault for missing YAML: {VAULT}")
    for f in VAULT.rglob("*.md"):
        with open(f, "r", encoding="utf-8") as fh:
            content = fh.read()

        if has_frontmatter(content):
            continue

        body = content
        title = extract_title(body, f.name)

        meta = {
            "title": title,
            "tags": [],
        }

        post = frontmatter.Post(body, **meta)
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(frontmatter.dumps(post))

        print(f"📝 Added YAML to: {f}")

if __name__ == "__main__":
    main()
