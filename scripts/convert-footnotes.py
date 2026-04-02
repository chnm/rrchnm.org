#!/usr/bin/env python3
"""
Convert legacy HTML/markdown footnotes in publication content to Hugo/Goldmark
footnote syntax ([^1] references and [^1]: definitions).

Handles multiple legacy formats:
  - [1](#N_1_), [1](#f1), [1](#ref1), [1](#FOOT1), [1](#1)
  - [1.](#ref1), [1](#t1), [1](#REF1), [1](#ftn1), [2.](#2-a)

Also strips leftover HTML footnote anchors from frontmatter.
"""

import re
import sys
from pathlib import Path


def convert_file(filepath: Path, dry_run: bool = False) -> dict:
    """Convert a single file's footnotes. Returns stats."""
    text = filepath.read_text()
    original = text
    stats = {"refs": 0, "defs": 0, "frontmatter_cleaned": 0}

    # --- Clean frontmatter footnote anchors ---
    # e.g. <a href="#N_1_"name="ref1"id="ref1"><sup>1</sup></a>
    frontmatter_fn = re.compile(
        r'<a\s+href="#[^"]*"[^>]*>\s*<sup>\d+</sup>\s*</a>'
    )
    text, n = frontmatter_fn.subn("", text)
    stats["frontmatter_cleaned"] = n

    # --- Convert footnote definitions FIRST (start of line) ---
    # These appear at the end of the document as:
    #   [1.](#ref1) Footnote text...   or   [1](#t1) Footnote text...
    # They start at the beginning of a line
    def replace_def(m):
        num = m.group(1)
        stats["defs"] += 1
        return f"[^{num}]: "

    text = re.sub(
        r'^\[(\d+)\.?\]\(#[^)]+\)\s*',
        replace_def,
        text,
        flags=re.MULTILINE,
    )

    # --- Convert inline references (not at start of line) ---
    # Match patterns like [1](#N_1_), [1](#f1), [1](#ref1), [1](#1), [1](#FOOT1)
    def replace_ref(m):
        num = m.group(1)
        stats["refs"] += 1
        return f"[^{num}]"

    text = re.sub(
        r'\[(\d+)\]\(#[^)]+\)',
        replace_ref,
        text,
    )

    if text != original:
        if not dry_run:
            filepath.write_text(text)
        return stats
    return stats


def main():
    dry_run = "--dry-run" in sys.argv
    pub_dir = Path(__file__).parent.parent / "content" / "publications"

    if not pub_dir.exists():
        print(f"Error: {pub_dir} not found", file=sys.stderr)
        sys.exit(1)

    total = {"files": 0, "refs": 0, "defs": 0, "frontmatter": 0}

    for md_file in sorted(pub_dir.glob("*/index.md")):
        stats = convert_file(md_file, dry_run=dry_run)
        if stats["refs"] or stats["defs"] or stats["frontmatter_cleaned"]:
            total["files"] += 1
            total["refs"] += stats["refs"]
            total["defs"] += stats["defs"]
            total["frontmatter"] += stats["frontmatter_cleaned"]
            slug = md_file.parent.name
            fm = f", {stats['frontmatter_cleaned']} frontmatter" if stats["frontmatter_cleaned"] else ""
            prefix = "[dry-run] " if dry_run else ""
            print(f"  {prefix}Converted {slug}: {stats['refs']} refs, {stats['defs']} defs{fm}")

    action = "Would convert" if dry_run else "Converted"
    print(f"\n{action} {total['files']} files: "
          f"{total['refs']} references, {total['defs']} definitions, "
          f"{total['frontmatter']} frontmatter anchors")


if __name__ == "__main__":
    main()
