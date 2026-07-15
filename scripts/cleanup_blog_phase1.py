#!/usr/bin/env python3
"""Phase 1 blog cleanup: strip legacy fields, lowercase tags, fix malformed YAML.

Surgical line-based edits — preserves frontmatter ordering and quoting style.

Operations:
  1. Strip top-level keys: lastmod, event_start_date, description.
  2. Lowercase every tag value. Normalize RRCHNM@ / @RRCHNM -> rrchnm.
     Collapse duplicates that emerge after lowercasing.
  3. Fix two known malformed frontmatter delimiters (missing newline after ---).
  4. Add missing author to one post.
  5. Delete __trashed-* directories.

Idempotent: re-running produces no diff.
"""

import os
import re
import shutil
import sys

BLOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'content', 'blog')

DROP_KEYS = {'lastmod', 'event_start_date', 'description'}

MALFORMED_FRONTMATTER_FILES = {
    '2021-03-08-were-hiring-a-full-stack-developer',
    '2023-04-21-welcome-kristen-jacobsen',
}

MISSING_AUTHOR_FILE = '2024-12-13-digital-scholar-makes-year-end-donation-to-rrchnm'

TOP_KEY_RE = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*)\s*:')
LIST_ITEM_RE = re.compile(r"""^(\s*-\s+)(['"]?)(.+?)(['"]?)\s*$""")


def split_frontmatter(text):
    """Return (frontmatter_lines, body_text). If no frontmatter, return (None, text)."""
    if not text.startswith('---'):
        return None, text
    lines = text.split('\n')
    if lines[0].strip() != '---':
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            fm = lines[1:i]
            body = '\n'.join(lines[i + 1:])
            return fm, body
    return None, text


def lowercase_tag(raw_value):
    """Lowercase a tag value, normalizing RRCHNM variants and stripping the @ noise."""
    v = raw_value.strip()
    if v in ('RRCHNM@', '@RRCHNM'):
        return 'rrchnm'
    return v.lower()


def process_frontmatter(fm_lines):
    """Apply Phase 1 edits to a list of frontmatter lines. Returns new list."""
    out = []
    i = 0
    in_tags = False
    seen_tag_values = []

    while i < len(fm_lines):
        line = fm_lines[i]
        m = TOP_KEY_RE.match(line)

        if m:
            key = m.group(1)
            if in_tags:
                in_tags = False
                seen_tag_values = []

            if key in DROP_KEYS:
                # Skip this line and any continuation lines (indented).
                i += 1
                while i < len(fm_lines) and (fm_lines[i].startswith(' ') or fm_lines[i].startswith('\t')):
                    i += 1
                continue

            if key == 'tags':
                in_tags = True
                out.append(line)
                i += 1
                continue

            out.append(line)
            i += 1
            continue

        if in_tags:
            list_m = LIST_ITEM_RE.match(line)
            if list_m:
                prefix, qopen, value, qclose = list_m.groups()
                new_value = lowercase_tag(value)
                if new_value in seen_tag_values:
                    i += 1
                    continue
                seen_tag_values.append(new_value)
                # Preserve original quoting unless the value contains chars
                # that YAML needs quoted (e.g., leading digit, plus sign, special).
                # Use single quotes if value would be ambiguous, else bare.
                needs_quote = (
                    new_value == '' or
                    new_value[0].isdigit() or
                    new_value[0] in "!&*[]{}|>'\"%@`#" or
                    new_value.startswith('- ') or
                    new_value.lower() in ('yes', 'no', 'true', 'false', 'null', 'on', 'off')
                )
                if needs_quote:
                    out.append(f"{prefix}'{new_value}'")
                else:
                    out.append(f"{prefix}{new_value}")
                i += 1
                continue

        out.append(line)
        i += 1

    return out


def fix_malformed_frontmatter(text):
    """Add missing newline after closing --- of frontmatter."""
    # Pattern: ---\n<frontmatter>---<non-newline-content>
    # Replace with: ---\n<frontmatter>---\n\n<content>
    return re.sub(r'(\n---)([^\n])', r'\1\n\n\2', text, count=1)


def ensure_authors(text, dirname):
    if dirname != MISSING_AUTHOR_FILE:
        return text
    fm, body = split_frontmatter(text)
    if fm is None:
        return text
    has_authors = any(TOP_KEY_RE.match(line) and TOP_KEY_RE.match(line).group(1) == 'authors' for line in fm)
    if has_authors:
        return text
    # Insert authors block at the top of the frontmatter, alphabetically the convention
    # places authors first in most posts, so put it at the start.
    new_fm = ['authors:', '- RRCHNM'] + fm
    return '---\n' + '\n'.join(new_fm) + '\n---\n' + body


def process_file(path, dirname):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    original = text

    if dirname in MALFORMED_FRONTMATTER_FILES:
        text = fix_malformed_frontmatter(text)

    fm, body = split_frontmatter(text)
    if fm is None:
        if text != original:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(text)
            return True
        return False

    new_fm = process_frontmatter(fm)
    new_text = '---\n' + '\n'.join(new_fm) + '\n---\n' + body

    new_text = ensure_authors(new_text, dirname)

    if new_text != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_text)
        return True
    return False


def delete_trashed():
    """Delete __trashed-* directories."""
    deleted = []
    for name in sorted(os.listdir(BLOG_DIR)):
        if '__trashed' in name:
            full = os.path.join(BLOG_DIR, name)
            if os.path.isdir(full):
                shutil.rmtree(full)
                deleted.append(name)
    return deleted


def main():
    dry_run = '--apply' not in sys.argv

    changed = []
    for name in sorted(os.listdir(BLOG_DIR)):
        if '__trashed' in name:
            continue
        full = os.path.join(BLOG_DIR, name)
        if not os.path.isdir(full):
            continue
        idx = os.path.join(full, 'index.md')
        if not os.path.exists(idx):
            continue
        if dry_run:
            # Simulate
            with open(idx, 'r', encoding='utf-8') as f:
                text = f.read()
            original = text
            if name in MALFORMED_FRONTMATTER_FILES:
                text = fix_malformed_frontmatter(text)
            fm, body = split_frontmatter(text)
            if fm is not None:
                new_fm = process_frontmatter(fm)
                text = '---\n' + '\n'.join(new_fm) + '\n---\n' + body
                text = ensure_authors(text, name)
            if text != original:
                changed.append(name)
        else:
            if process_file(idx, name):
                changed.append(name)

    if dry_run:
        print(f'[DRY RUN] Would modify {len(changed)} files.')
        print(f'[DRY RUN] Would delete the following __trashed-* directories:')
        for name in sorted(os.listdir(BLOG_DIR)):
            if '__trashed' in name:
                print(f'  - {name}')
        print('\nRun with --apply to make changes.')
    else:
        deleted = delete_trashed()
        print(f'Modified {len(changed)} files.')
        print(f'Deleted {len(deleted)} __trashed-* directories.')


if __name__ == '__main__':
    main()
