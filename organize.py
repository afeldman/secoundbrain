#!/usr/bin/env python3
import os
import re
import shutil
import yaml
import frontmatter
from pathlib import Path

# Vault-Pfad aus Umgebungsvariable, Default: ~/Obsidian
VAULT = Path(os.environ.get("OBSIDIAN_VAULT", "~/Obsidian")).expanduser()

def load_rules(path):
    with open(path) as f:
        return yaml.safe_load(f)

def rename_file(file, rules):
    meta = frontmatter.load(file)
    title = meta.get("title") or file.stem
    for pattern, repl in rules["patterns"].items():
        title = re.sub(pattern, repl, title)
    new_name = f"{title}.md"
    return file.parent / new_name

def categorize_file(file, rules):
    meta = frontmatter.load(file)
    tags = meta.get("tags", [])
    for cat, rule in rules["categories"].items():
        if any(t in tags for t in rule["tags"]):
            return rule["folder"]
    return "03_Resources"

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=["rename", "move", "tags"])
    p.add_argument("--rules", required=True)
    args = p.parse_args()

    rules = load_rules(args.rules)

    for file in VAULT.rglob("*.md"):
        if args.action == "rename":
            newfile = rename_file(file, rules)
            if file != newfile:
                file.rename(newfile)

        elif args.action == "move":
            folder = categorize_file(file, rules)
            target = VAULT / folder
            target.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file), target / file.name)

        elif args.action == "tags":
            meta = frontmatter.load(file)
            tags = meta.get("tags", [])
            normalized = sorted(set([str(t).lower() for t in tags]))
            meta["tags"] = normalized
            with open(file, "w") as f:
                f.write(frontmatter.dumps(meta))

if __name__ == "__main__":
    main()
