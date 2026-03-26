#!/usr/bin/env python3
"""Convert markdown images in 2020+ blog posts to Hugo figure shortcodes.

Handles these patterns:
1. [caption ...][![alt](thumb)](full) Caption[/caption]  (WordPress caption)
2. [caption ...]![alt](img) Caption[/caption]             (WordPress caption, no link)
3. [![alt](thumb)](full)                                   (linked image)
4. ![alt](img)                                             (plain image)
5. <figure>...<img src=...>...<figcaption>...</figcaption>...</figure> (HTML figure)

Converts to: {{< figure src="img" alt="alt" caption="caption" >}}
"""

import os
import re

BLOG_DIR = os.path.join(os.path.dirname(__file__), "..", "content", "blog")


def convert_post(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Pattern 1: WordPress [caption] with linked image
    # [caption id="..." align="..." width="..."][![alt](thumb)](full) Caption text[/caption]
    content = re.sub(
        r'\[caption[^\]]*\]\s*\[!\[([^\]]*)\]\([^)]*\)\]\(([^)]+)\)\s*(.*?)\[/caption\]',
        lambda m: _figure(m.group(2), m.group(1), m.group(3).strip()),
        content,
        flags=re.DOTALL
    )

    # Pattern 2: WordPress [caption] with plain image
    # [caption id="..." align="..." width="..."]![alt](img) Caption text[/caption]
    content = re.sub(
        r'\[caption[^\]]*\]\s*!\[([^\]]*)\]\(([^)]+)\)\s*(.*?)\[/caption\]',
        lambda m: _figure(m.group(2), m.group(1), m.group(3).strip()),
        content,
        flags=re.DOTALL
    )

    # Pattern 3: HTML <figure> blocks
    content = re.sub(
        r'<figure[^>]*>\s*<img\s+src=(["\'])([^"\']+)\1[^>]*alt=(["\'])([^"\']*)\3[^>]*/?\s*>\s*(?:<figcaption[^>]*>(.*?)</figcaption>)?\s*</figure>',
        lambda m: _figure(m.group(2), m.group(4), m.group(5).strip() if m.group(5) else ""),
        content,
        flags=re.DOTALL
    )

    # Pattern 4: Linked image [![alt](thumb)](full) — use full-size image
    content = re.sub(
        r'\[!\[([^\]]*)\]\([^)]*\)\]\(([^)]+)\)',
        lambda m: _figure(m.group(2), m.group(1), ""),
        content
    )

    # Pattern 5: Plain image ![alt](img) — standalone on its own line
    content = re.sub(
        r'^!\[([^\]]*)\]\(([^)]+)\)\s*$',
        lambda m: _figure(m.group(2), m.group(1), ""),
        content,
        flags=re.MULTILINE
    )

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def _figure(src, alt, caption):
    """Build a Hugo figure shortcode string."""
    parts = ['{{< figure']
    parts.append(f' src="{src.strip()}"')
    if alt:
        # Escape quotes in alt text
        alt = alt.strip().replace('"', '\\"')
        parts.append(f' alt="{alt}"')
    if caption:
        # Clean up caption: strip HTML tags, escape quotes
        caption = re.sub(r'<[^>]+>', '', caption).strip()
        caption = caption.replace('"', '\\"')
        if caption:
            parts.append(f' caption="{caption}"')
    parts.append(' >}}')
    return ''.join(parts)


def main():
    blog_dir = os.path.abspath(BLOG_DIR)
    converted = 0

    for dirname in sorted(os.listdir(blog_dir)):
        if not dirname.startswith("202"):
            continue
        bundle_dir = os.path.join(blog_dir, dirname)
        index_path = os.path.join(bundle_dir, "index.md")
        if not os.path.isdir(bundle_dir) or not os.path.exists(index_path):
            continue

        if convert_post(index_path):
            converted += 1
            print(f"  CONVERTED: {dirname}")

    print(f"\nDone. Converted {converted} posts.")


if __name__ == "__main__":
    main()
