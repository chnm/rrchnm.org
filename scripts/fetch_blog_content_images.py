#!/usr/bin/env python3
"""Fetch all /media/ images referenced in blog post content from the live WordPress site.

For each blog bundle:
  1. Find all /media/... references in the markdown content
  2. Download each from https://rrchnm.org/wp-content/uploads/...
  3. Save into the bundle directory
  4. Rewrite the markdown to use bundle-relative paths
"""

import os
import re
import urllib.request
import urllib.error
import time

BLOG_DIR = os.path.join(os.path.dirname(__file__), "..", "content", "blog")
BASE_URL = "https://rrchnm.org/wp-content/uploads"

# Match /media/... paths in markdown content (images, links, etc.)
MEDIA_RE = re.compile(r'/media/([^)"\'<>\s]+)')


def main():
    blog_dir = os.path.abspath(BLOG_DIR)
    total_downloaded = 0
    total_failed = 0
    total_skipped = 0

    dirs = sorted(d for d in os.listdir(blog_dir)
                  if os.path.isdir(os.path.join(blog_dir, d)))

    for dirname in dirs:
        bundle_dir = os.path.join(blog_dir, dirname)
        index_path = os.path.join(bundle_dir, "index.md")
        if not os.path.exists(index_path):
            continue

        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Find all /media/ references
        matches = MEDIA_RE.findall(content)
        if not matches:
            continue

        # Deduplicate while preserving order
        seen = set()
        unique_paths = []
        for m in matches:
            if m not in seen:
                seen.add(m)
                unique_paths.append(m)

        modified = False
        for rel_path in unique_paths:
            filename = os.path.basename(rel_path)
            media_path = f"/media/{rel_path}"
            dest_path = os.path.join(bundle_dir, filename)

            # Handle filename collisions (different /media/ paths, same basename)
            if os.path.exists(dest_path):
                # Check if this exact media_path was already replaced
                if media_path not in content:
                    total_skipped += 1
                    continue
                # File exists from a previous run or featured_image download
                # Just rewrite the path
                content = content.replace(media_path, filename)
                modified = True
                total_skipped += 1
                continue

            url = f"{BASE_URL}/{rel_path}"
            try:
                req = urllib.request.Request(url, headers={
                    "User-Agent": "Mozilla/5.0 (rrchnm-migration)"
                })
                with urllib.request.urlopen(req, timeout=15) as resp:
                    with open(dest_path, "wb") as f:
                        f.write(resp.read())

                content = content.replace(media_path, filename)
                modified = True
                total_downloaded += 1
                print(f"  OK: {dirname}/{filename}")
                time.sleep(0.15)

            except (urllib.error.HTTPError, urllib.error.URLError, OSError) as e:
                total_failed += 1
                print(f"  FAIL: {media_path} ({e})")

        if modified:
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(content)

    print(f"\nDone. Downloaded: {total_downloaded}, Failed: {total_failed}, Skipped/existing: {total_skipped}")


if __name__ == "__main__":
    main()
