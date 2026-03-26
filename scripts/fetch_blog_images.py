#!/usr/bin/env python3
"""Fetch missing featured images from the live WordPress site into blog bundles.

Maps /media/YYYY/MM/file -> https://rrchnm.org/wp-content/uploads/YYYY/MM/file
Downloads into the bundle directory and updates frontmatter to use the local filename.
"""

import os
import re
import urllib.request
import urllib.error
import time

BLOG_DIR = os.path.join(os.path.dirname(__file__), "..", "content", "blog")
BASE_URL = "https://rrchnm.org/wp-content/uploads"


def find_bundles_with_remote_images(blog_dir):
    """Find all bundles whose featured_image still points to /media/..."""
    results = []
    for dirname in sorted(os.listdir(blog_dir)):
        bundle_dir = os.path.join(blog_dir, dirname)
        index_path = os.path.join(bundle_dir, "index.md")
        if not os.path.isdir(bundle_dir) or not os.path.exists(index_path):
            continue

        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()

        match = re.search(r"^featured_image:\s*(/media/.+)$", content, re.MULTILINE)
        if match:
            image_path = match.group(1).strip().strip("'\"")
            results.append((dirname, bundle_dir, index_path, content, image_path))

    return results


def download_image(image_path, dest_path):
    """Download image from live site. Returns True on success."""
    # /media/2017/10/file.jpg -> wp-content/uploads/2017/10/file.jpg
    relative = image_path.lstrip("/").replace("media/", "", 1)
    url = f"{BASE_URL}/{relative}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (rrchnm-migration)"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            with open(dest_path, "wb") as f:
                f.write(resp.read())
        return True
    except (urllib.error.HTTPError, urllib.error.URLError, OSError) as e:
        print(f"    FAILED: {url} ({e})")
        return False


def main():
    blog_dir = os.path.abspath(BLOG_DIR)
    bundles = find_bundles_with_remote_images(blog_dir)
    print(f"Found {len(bundles)} bundles with remote featured images\n")

    downloaded = 0
    failed = 0

    for dirname, bundle_dir, index_path, content, image_path in bundles:
        img_filename = os.path.basename(image_path)
        dest_path = os.path.join(bundle_dir, img_filename)

        # Skip if already downloaded
        if os.path.exists(dest_path):
            print(f"  SKIP (exists): {dirname}/{img_filename}")
            continue

        print(f"  GET: {image_path} -> {dirname}/{img_filename}")
        if download_image(image_path, dest_path):
            # Update frontmatter to use local filename
            content = content.replace(
                f"featured_image: {image_path}",
                f"featured_image: {img_filename}"
            )
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(content)
            downloaded += 1
            # Be polite to the server
            time.sleep(0.2)
        else:
            failed += 1

    print(f"\nDone. Downloaded: {downloaded}, Failed: {failed}")


if __name__ == "__main__":
    main()
