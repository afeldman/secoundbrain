#!/usr/bin/env python3
import os
from pathlib import Path
from collections import defaultdict
import frontmatter

VAULT = Path(os.environ.get("OBSIDIAN_VAULT", "~/Obsidian")).expanduser()

def main():
    clusters = defaultdict(list)

    for f in VAULT.rglob("*.md"):
        post = frontmatter.load(f)
        topics = post.get("topics") or []
        tags = post.get("tags") or []

        # Topics priorisieren, ansonsten Tags nutzen
        labels = topics if topics else tags

        for label in labels:
            label_str = str(label)
            clusters[label_str].append(f)

    output = VAULT / "Semantic_Clusters.md"

    with open(output, "w", encoding="utf-8") as out:
        out.write("# Semantic Cluster Map\n\n")
        if not clusters:
            out.write("_Keine Topics/Tags gefunden._\n")
            return

        for label, files in sorted(clusters.items(), key=lambda x: x[0].lower()):
            out.write(f"## {label}\n")
            for f in files:
                out.write(f"- [[{f.stem}]]\n")
            out.write("\n")

if __name__ == "__main__":
    main()
