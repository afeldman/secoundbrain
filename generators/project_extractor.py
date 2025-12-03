import os
import frontmatter
from pathlib import Path

VAULT = Path(os.environ.get("OBSIDIAN_VAULT", "~/Obsidian")).expanduser()

def main():
    for f in Path(VAULT).rglob("*.md"):
        meta = frontmatter.load(f)
        summary = meta.get("summary", "")
        if any(x in summary.lower() for x in ["deadline", "deliverable", "milestone"]):
            meta["tags"] = list(set(meta.get("tags", []) + ["project"]))
            with open(f, "w") as out:
                out.write(frontmatter.dumps(meta))

if __name__ == "__main__":
    main()
