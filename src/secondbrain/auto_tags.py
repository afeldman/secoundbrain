#!/usr/bin/env python3
import os
from pathlib import Path
import yaml
import frontmatter

VAULT = Path(os.environ.get("OBSIDIAN_VAULT", "~/Obsidian")).expanduser()
RULES_PATH = Path("rules/auto_tags.yaml")

def load_rules():
    if not RULES_PATH.exists():
        print(f"⚠️ Keine auto_tags-Regeln gefunden unter {RULES_PATH}, überspringe.")
        return []
    with open(RULES_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    # Erwartet: list von {tag: "project", keywords: ["deadline", ...]}
    return data.get("rules", [])

def main():
    rules = load_rules()
    if not rules:
        return

    print(f"🏷  Wende Auto-Tag-Regeln an auf Vault: {VAULT}")

    for f in VAULT.rglob("*.md"):
        with open(f, "r", encoding="utf-8") as fh:
            text = fh.read()

        post = frontmatter.loads(text)
        body = post.content
        tags = set(str(t).lower() for t in post.get("tags", []))

        body_lower = body.lower()

        for rule in rules:
            tag = rule.get("tag")
            kws = rule.get("keywords", [])
            if not tag or not kws:
                continue
            if any(kw.lower() in body_lower for kw in kws):
                tags.add(tag.lower())

        post["tags"] = sorted(tags)
        with open(f, "w", encoding="utf-8") as out:
            out.write(frontmatter.dumps(post))

        # Optional: kleine Statusanzeige
        # print(f"🏷  Updated tags for {f}")

if __name__ == "__main__":
    main()
