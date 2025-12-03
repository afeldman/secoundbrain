import os
from pathlib import Path
import frontmatter

VAULT = Path(os.environ.get("OBSIDIAN_VAULT", "~/Obsidian")).expanduser()

def build_moc(category, path):
    output = Path(VAULT) / f"{category}_Index.md"
    entries = []

    for f in Path(VAULT, path).rglob("*.md"):
        meta = frontmatter.load(f)
        title = meta.get("title", f.stem)
        entries.append(f"- [[{f.stem}|{title}]]")

    with open(output, "w") as outf:
        outf.write(f"# {category} Index\n\n")
        outf.write("\n".join(entries))

def main():
    build_moc("Projects", "01_Projects")
    build_moc("Areas", "02_Areas")
    build_moc("Resources", "03_Resources")
    build_moc("Archive", "04_Archive")

if __name__ == "__main__":
    main()
