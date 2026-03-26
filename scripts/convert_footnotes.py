#!/usr/bin/env python3
"""Convert WordPress-style footnotes to Markdown footnotes.

Handles these patterns:
- Inline references: [1](#_ftn1), [1](#_edn1), [2](#_ftn2), etc.
- Footnote definitions: [1](#_ftnref1) Text..., [1](#_ednref1) Text...
- Also handles <a name="_ftn1"> anchor tags

Converts to standard Markdown footnotes:
- Inline: [^1]
- Definition: [^1]: Text...
"""

import os
import re
import sys

CONTENT_DIR = os.path.join(os.path.dirname(__file__), "..", "content")


def convert_footnotes(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Remove anchor tags like <a name="_ftn1"> or <a name="_edn1">
    content = re.sub(r'<a\s+name=["\']_(?:ftn|edn)\d+["\']>\s*</a>', '', content)
    content = re.sub(r'<a\s+name=["\']_(?:ftn|edn)ref\d+["\']>\s*</a>', '', content)

    # Convert inline references: [1](#_ftn1) or [1](#_edn1) → [^1]
    content = re.sub(
        r'\[(\d+)\]\(#_(?:ftn|edn)\d+\)',
        r'[^\1]',
        content
    )

    # Convert footnote definitions: [1](#_ftnref1) or [1](#_ednref1) → [^1]:
    content = re.sub(
        r'^\[(\d+)\]\(#_(?:ftn|edn)ref\d+\)\s*',
        r'[^\1]: ',
        content,
        flags=re.MULTILINE
    )

    # Remove "Footnotes:" or "Author Bio:" headers that precede footnote sections
    # Only remove "Footnotes:" if it's on its own line and followed by footnote definitions
    content = re.sub(r'^Footnotes:\s*\n', '', content, flags=re.MULTILINE)

    # Clean up any leftover empty <a> tags
    content = re.sub(r'<a\s+(?:id|name)=["\']_(?:ftn|edn)(?:ref)?\d+["\'][^>]*>\s*</a>', '', content)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def main():
    content_dir = os.path.abspath(CONTENT_DIR)
    converted = 0
    files_converted = []

    # Walk all content directories
    for root, dirs, files in os.walk(content_dir):
        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue
            filepath = os.path.join(root, fname)
            if convert_footnotes(filepath):
                converted += 1
                relpath = os.path.relpath(filepath, content_dir)
                files_converted.append(relpath)
                print(f"  CONVERTED: {relpath}")

    print(f"\nDone. Converted {converted} files.")


if __name__ == "__main__":
    main()
