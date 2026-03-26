#!/usr/bin/env python3
"""Update blog bundles: prepend date to directory name and pull featured images into bundles.

For each content/blog/<slug>/index.md:
  1. Extract date from frontmatter
  2. Rename directory to <YYYY-MM-DD>-<slug>/
  3. If featured_image points to static/media/..., copy the image into the bundle
     and update frontmatter to reference it as a page resource
"""

import os
import re
import shutil

BLOG_DIR = os.path.join(os.path.dirname(__file__), "..", "content", "blog")
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")


def extract_date(content):
    """Extract date string (YYYY-MM-DD) from frontmatter."""
    match = re.search(r"^date:\s*['\"]?(\d{4}-\d{2}-\d{2})", content, re.MULTILINE)
    if match:
        return match.group(1)
    return None


def extract_featured_image(content):
    """Extract featured_image path from frontmatter."""
    match = re.search(r"^featured_image:\s*(.+)$", content, re.MULTILINE)
    if match:
        return match.group(1).strip().strip("'\"")
    return None


def main():
    blog_dir = os.path.abspath(BLOG_DIR)
    static_dir = os.path.abspath(STATIC_DIR)

    dirs = sorted(d for d in os.listdir(blog_dir)
                  if os.path.isdir(os.path.join(blog_dir, d)) and d != "_index.md")

    print(f"Found {len(dirs)} blog bundles to update")

    renamed = 0
    images_copied = 0
    skipped = 0

    for dirname in dirs:
        bundle_dir = os.path.join(blog_dir, dirname)
        index_path = os.path.join(bundle_dir, "index.md")

        if not os.path.exists(index_path):
            continue

        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()

        date_str = extract_date(content)
        if not date_str:
            print(f"  SKIP (no date): {dirname}")
            skipped += 1
            continue

        # --- Copy featured image into bundle ---
        featured_image = extract_featured_image(content)
        if featured_image:
            # featured_image is like /media/2016/07/eagleeye.png
            # The actual file is at static/media/2016/07/eagleeye.png
            src_path = os.path.join(static_dir, featured_image.lstrip("/"))
            if os.path.exists(src_path):
                img_filename = os.path.basename(src_path)
                dest_path = os.path.join(bundle_dir, img_filename)
                if not os.path.exists(dest_path):
                    shutil.copy2(src_path, dest_path)
                    # Update frontmatter to use bundle-relative path
                    content = content.replace(
                        f"featured_image: {featured_image}",
                        f"featured_image: {img_filename}"
                    )
                    with open(index_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    images_copied += 1
                    print(f"  IMG: {dirname} <- {featured_image}")
            else:
                print(f"  IMG NOT FOUND: {dirname} -> {featured_image}")

        # --- Rename directory with date prefix ---
        # Check if already has date prefix
        if re.match(r"\d{4}-\d{2}-\d{2}-", dirname):
            continue

        new_dirname = f"{date_str}-{dirname}"
        new_bundle_dir = os.path.join(blog_dir, new_dirname)

        if os.path.exists(new_bundle_dir):
            print(f"  SKIP (exists): {dirname} -> {new_dirname}")
            skipped += 1
            continue

        os.rename(bundle_dir, new_bundle_dir)
        renamed += 1

    print(f"\nDone. Renamed: {renamed}, Images copied: {images_copied}, Skipped: {skipped}")


if __name__ == "__main__":
    main()
