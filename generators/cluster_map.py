import os
from pathlib import Path
import frontmatter
from collections import defaultdict

VAULT = os.path.expanduser("~/Obsidian")

def main():
    clusters = defaultdict(list)

    for f in Path(VAULT).rglob("*.md"):
        meta = frontmatter.load(f)
        topics = meta.get("topics", [])
        for t in topics:
            clusters[t].append(f)

    output = Path(VAULT) / "Semantic_Clusters.md"

    with open(output, "w") as out:
        out.write("# Semantic Cluster Map\n\n")
        for topic, files in clusters.items():
            out.write(f"## {topic}\n")
            for f in files:
                out.write(f"- [[{f.stem}]]\n")
            out.write("\n")

if __name__ == "__main__":
    main()
