import os
import re
import frontmatter
from pathlib import Path

VAULT = os.path.expanduser("~/Obsidian")

name_pattern = re.compile(r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b")

def main():
    for f in Path(VAULT).rglob("*.md"):
        text = open(f).read()
        names = name_pattern.findall(text)
        meta = frontmatter.load(f)
        if names:
            meta["tags"] = list(set(meta.get("tags", []) + ["person"]))
            with open(f, "w") as out:
                out.write(frontmatter.dumps(meta))

if __name__ == "__main__":
    main()
