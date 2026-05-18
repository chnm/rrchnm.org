#!/usr/bin/env python3
"""Phase 3 blog cleanup: collapse categories to exactly two values.

Every post ends up with either `news` or `post` (lowercase, single value).

Rule:
  - Currently `Post`/`Posts`/`post` (any case)  -> `post`
  - Title matches essay/narrative patterns      -> `post`
  - Everything else                             -> `news`

Idempotent.
"""

import os
import re
import sys
from pathlib import Path

BLOG_DIR = Path(__file__).resolve().parent.parent / 'content' / 'blog'

ESSAY_TITLE_RE = re.compile(
    r'\b(graduate student reflections|'
    r'remembering [A-Z]|'
    r'in memory of|'
    r'reflections? (on|from)|'
    r'^how [A-Z]|'
    r'^why [A-Z]|'
    r'^when [A-Z]|'
    r'^what (we|i) learned|'
    r'models of|'
    r'thoughts on|'
    r'lessons from)\b',
    re.IGNORECASE)

POST_VALUES_LOWER = {'post', 'posts'}

CATEGORIES_BLOCK_RE = re.compile(
    r'^categories:\s*\n((?:[ \t]*-\s+.+\n)+)',
    re.MULTILINE)

INLINE_CATEGORIES_RE = re.compile(
    r'^categories:[ \t]+(.+)\n', re.MULTILINE)

TITLE_RE = re.compile(r'^title:[ \t]+(.+?)\s*$', re.MULTILINE)


def split_frontmatter(text):
    if not text.startswith('---\n'):
        return None, text
    end = text.find('\n---\n', 4)
    if end < 0:
        return None, text
    return text[4:end], text[end + 5:]


def current_categories(fm_text):
    m = CATEGORIES_BLOCK_RE.search(fm_text)
    if m:
        vals = re.findall(r'-\s+["\']?([^"\'\n]+)["\']?', m.group(1))
        return [v.strip() for v in vals]
    m = INLINE_CATEGORIES_RE.search(fm_text)
    if m:
        return [m.group(1).strip().strip("'\"")]
    return []


def get_title(fm_text):
    m = TITLE_RE.search(fm_text)
    if not m:
        return ''
    return m.group(1).strip().strip("'\"")


def decide(fm_text):
    cats_lower = [c.lower() for c in current_categories(fm_text)]
    if any(c in POST_VALUES_LOWER for c in cats_lower):
        return 'post'
    title = get_title(fm_text)
    if ESSAY_TITLE_RE.search(title):
        return 'post'
    return 'news'


def set_categories(text, new_value):
    """Replace the categories block (or inline) with `categories:\\n- <value>`."""
    fm, body = split_frontmatter(text)
    if fm is None:
        return text
    new_block = f'categories:\n- {new_value}\n'

    if CATEGORIES_BLOCK_RE.search(fm + '\n'):
        new_fm = CATEGORIES_BLOCK_RE.sub(new_block, fm + '\n').rstrip('\n')
    elif INLINE_CATEGORIES_RE.search(fm + '\n'):
        new_fm = INLINE_CATEGORIES_RE.sub(new_block, fm + '\n').rstrip('\n')
    else:
        # No categories field at all -- insert after the first line of frontmatter.
        new_fm = fm.rstrip('\n') + '\n' + new_block.rstrip('\n')

    return '---\n' + new_fm + '\n---\n' + body


def process_file(path):
    text = path.read_text(encoding='utf-8')
    fm, _ = split_frontmatter(text)
    if fm is None:
        return False
    new_cat = decide(fm)
    new_text = set_categories(text, new_cat)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        return True
    return False


def main():
    dry_run = '--apply' not in sys.argv
    changed = []
    cat_counts = {'news': 0, 'post': 0}
    for d in sorted(os.listdir(BLOG_DIR)):
        full = BLOG_DIR / d
        if not full.is_dir():
            continue
        idx = full / 'index.md'
        if not idx.exists():
            continue

        text = idx.read_text(encoding='utf-8')
        fm, _ = split_frontmatter(text)
        if fm is None:
            continue
        new_cat = decide(fm)
        cat_counts[new_cat] += 1
        new_text = set_categories(text, new_cat)
        if new_text != text:
            changed.append(d)
            if not dry_run:
                idx.write_text(new_text, encoding='utf-8')

    print(f'Final category counts: {cat_counts}')
    print(f'{"Would modify" if dry_run else "Modified"} {len(changed)} files.')
    if dry_run:
        print('Run with --apply to write changes.')


if __name__ == '__main__':
    main()
