#!/usr/bin/env python3
"""Recategorize 2020+ blog posts: keep only News or Essay as category,
move everything else to tags.

Rules:
- "Essay" and "Essays" -> category: Essay
- "News", "Uncategorized", or anything else -> category: News (default)
- All other former categories become tags
- Merge with any existing tags (no duplicates)
"""

import os
import re
import yaml

BLOG_DIR = os.path.join(os.path.dirname(__file__), "..", "content", "blog")

# Categories that map to "Essay"
ESSAY_CATS = {"Essay", "Essays"}
# Categories that are just noise (don't become tags either)
SKIP_CATS = {"Uncategorized", "News", "wip"}


def process_post(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Split frontmatter from body
    match = re.match(r'^---\n(.*?\n)---\n(.*)', content, re.DOTALL)
    if not match:
        return False

    fm_str = match.group(1)
    body = match.group(2)

    try:
        fm = yaml.safe_load(fm_str)
    except yaml.YAMLError:
        return False

    if not fm or "categories" not in fm:
        return False

    old_cats = fm.get("categories", []) or []
    old_tags = fm.get("tags", []) or []

    # Determine new category
    is_essay = any(c in ESSAY_CATS for c in old_cats)
    new_cat = "Essay" if is_essay else "News"

    # Everything else becomes a tag
    new_tags_from_cats = [
        c for c in old_cats
        if c not in ESSAY_CATS and c not in SKIP_CATS and c != "News"
    ]

    # Merge with existing tags, preserving order, no duplicates
    seen = set()
    merged_tags = []
    for t in old_tags + new_tags_from_cats:
        if t not in seen:
            seen.add(t)
            merged_tags.append(t)

    # Check if anything changed
    if old_cats == [new_cat] and sorted(old_tags) == sorted(merged_tags):
        return False

    # Rebuild frontmatter
    fm["categories"] = [new_cat]
    if merged_tags:
        fm["tags"] = merged_tags
    elif "tags" in fm:
        del fm["tags"]

    # Reconstruct the file preserving style
    # Use yaml.dump for the frontmatter
    new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False)
    new_content = f"---\n{new_fm}---\n{body}"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True


def main():
    blog_dir = os.path.abspath(BLOG_DIR)
    updated = 0

    for dirname in sorted(os.listdir(blog_dir)):
        if not dirname.startswith("202"):
            continue
        index_path = os.path.join(blog_dir, dirname, "index.md")
        if not os.path.exists(index_path):
            continue

        if process_post(index_path):
            # Read back to report
            with open(index_path, "r") as f:
                content = f.read()
            cats = re.findall(r"^categories:\n((?:- .+\n)*)", content, re.MULTILINE)
            tags = re.findall(r"^tags:\n((?:- .+\n)*)", content, re.MULTILINE)
            cat_str = cats[0].strip() if cats else ""
            tag_str = tags[0].strip() if tags else "(none)"
            print(f"  {dirname}")
            print(f"    cat: {cat_str}  tags: {tag_str}")
            updated += 1

    print(f"\nDone. Updated {updated} posts.")


if __name__ == "__main__":
    main()
