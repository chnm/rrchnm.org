#!/usr/bin/env python3
"""Convert flat .md content files to Hugo page bundles.

For each .md file (excluding _index.md):
1. Create a directory with the same slug name
2. Move the .md file to index.md inside that directory
3. Copy any referenced images from /static/media/ into the bundle
4. Update frontmatter image paths to relative (bundle-local) filenames

Handles:
- featured_image in frontmatter
- thumbnail in frontmatter
- gallery list in frontmatter
- Image references in body content pointing to /media/
"""

import os
import re
import shutil
import yaml

STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")


def find_media_refs(content, frontmatter_str):
    """Find all /media/ references in frontmatter and body."""
    refs = set()
    # Match /media/... paths in the full file content
    for m in re.finditer(r'(/media/[^\s"\')\]]+)', content):
        refs.add(m.group(1))
    return refs


def copy_image(media_path, bundle_dir):
    """Copy an image from static/media/ to the bundle dir. Returns the new filename."""
    # media_path looks like /media/2022/04/thumbnail-ARE.jpg
    src = os.path.join(STATIC_DIR, media_path.lstrip("/"))
    if not os.path.exists(src):
        print(f"    WARNING: image not found: {src}")
        return None
    filename = os.path.basename(media_path)
    dst = os.path.join(bundle_dir, filename)
    if not os.path.exists(dst):
        shutil.copy2(src, dst)
    return filename


def update_content(content, path_map):
    """Replace absolute /media/ paths with relative filenames."""
    for old_path, new_name in sorted(path_map.items(), key=lambda x: -len(x[0])):
        content = content.replace(old_path, new_name)
    return content


def convert_section(section_dir):
    """Convert all flat .md files in a section to page bundles."""
    section_dir = os.path.abspath(section_dir)
    converted = 0

    for fname in sorted(os.listdir(section_dir)):
        if not fname.endswith(".md") or fname == "_index.md":
            continue

        filepath = os.path.join(section_dir, fname)
        if not os.path.isfile(filepath):
            continue

        slug = fname.replace(".md", "")
        bundle_dir = os.path.join(section_dir, slug)

        # Read file content
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Find all /media/ references
        media_refs = find_media_refs(content, "")

        # Create bundle directory
        os.makedirs(bundle_dir, exist_ok=True)

        # Copy images and build path map
        path_map = {}
        for ref in media_refs:
            new_name = copy_image(ref, bundle_dir)
            if new_name:
                path_map[ref] = new_name

        # Update content with relative paths
        new_content = update_content(content, path_map)

        # Write index.md
        index_path = os.path.join(bundle_dir, "index.md")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        # Remove old flat file
        os.remove(filepath)

        converted += 1
        img_count = len(path_map)
        print(f"  BUNDLED: {slug}/ ({img_count} image{'s' if img_count != 1 else ''})")

    return converted


def main():
    base = os.path.join(os.path.dirname(__file__), "..", "content")

    sections = ["our-work", "publications"]

    for section in sections:
        section_dir = os.path.join(base, section)
        if not os.path.isdir(section_dir):
            print(f"Skipping {section} (not found)")
            continue

        print(f"\n=== Converting {section} ===")
        count = convert_section(section_dir)
        print(f"  Done. Converted {count} files to page bundles.")


if __name__ == "__main__":
    main()
