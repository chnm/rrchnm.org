#!/usr/bin/env python3
"""Convert flat blog markdown files into Hugo page bundles.

For each content/blog/<filename>.md (except _index.md):
  1. Extract the slug from frontmatter (or derive from filename)
  2. Create content/blog/<slug>/index.md
  3. Move the original file's content into the new index.md
  4. Remove the original flat file
"""

import os
import re
import shutil

BLOG_DIR = os.path.join(os.path.dirname(__file__), "..", "content", "blog")


def extract_slug(filepath, content):
    """Extract slug from YAML frontmatter, fall back to filename."""
    match = re.search(r"^slug:\s*(.+)$", content, re.MULTILINE)
    if match:
        return match.group(1).strip().strip("'\"")
    # Derive from filename: strip date prefix and .md extension
    basename = os.path.basename(filepath).replace(".md", "")
    # Remove leading date pattern like 2025-12-08-
    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", basename)
    return slug


def main():
    blog_dir = os.path.abspath(BLOG_DIR)
    files = sorted(f for f in os.listdir(blog_dir)
                   if f.endswith(".md") and f != "_index.md")

    print(f"Found {len(files)} blog posts to convert")

    for filename in files:
        filepath = os.path.join(blog_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        slug = extract_slug(filepath, content)
        bundle_dir = os.path.join(blog_dir, slug)
        bundle_index = os.path.join(bundle_dir, "index.md")

        # Handle collision: if bundle dir already exists
        if os.path.exists(bundle_dir):
            print(f"  SKIP (dir exists): {filename} -> {slug}/")
            continue

        os.makedirs(bundle_dir)
        with open(bundle_index, "w", encoding="utf-8") as f:
            f.write(content)

        os.remove(filepath)
        print(f"  OK: {filename} -> {slug}/index.md")

    print("Done.")


if __name__ == "__main__":
    main()
