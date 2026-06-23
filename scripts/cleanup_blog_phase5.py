#!/usr/bin/env python3
"""Phase 5 blog cleanup: rename igorj2.sg-host slugs.

Operations on each directory whose slug contains 'igorj2.sg-host':
  1. Replace 'igorj2.sg-host' with 'rrchnm' (preserves possessive 's' if present).
  2. Strip internal date prefixes that duplicate the outer YYYY-MM-DD wrapper
     (formats: MM-DD-YYYY, MM-DD-YY, MMDDYYYY, MDDYYYY).
  3. Collapse any double-dashes that result.
  4. Update the `slug:` field in index.md to match the new directory name's
     slug portion (everything after the YYYY-MM-DD wrapper).
  5. `git mv` the directory.

Per user decision: no `aliases:` entries are added. Old URLs will 404.

Dry-run by default; --apply performs the renames.
"""

import argparse
import os
import re
import subprocess
from pathlib import Path

BLOG_DIR = Path(__file__).resolve().parent.parent / 'content' / 'blog'

OUTER_DATE_RE = re.compile(r'^(\d{4}-\d{2}-\d{2})-(.+)$')
# Internal date prefixes that appear right after the outer date.
# Match either MM-DD-YYYY / MM-DD-YY style or MMDDYYYY style.
INTERNAL_DATE_RE = re.compile(
    r'^('
    r'\d{2}-\d{2}-\d{4}|'          # 03-15-2018
    r'\d{2}-\d{2}-\d{2}|'          # 06-22-18
    r'\d{6,8}'                      # 02082017 or 1042017 or 11152017
    r')-(.+)$')

SLUG_FIELD_RE = re.compile(r'^slug:[ \t]+.+$', re.MULTILINE)


MONTHS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
          'jul', 'aug', 'sep', 'oct', 'nov', 'dec']


def internal_date_to_suffix(raw_date):
    """Convert MMDDYYYY/MM-DD-YYYY/MM-DD-YY/MDDYYYY to '<mon>-YYYY'.
    Returns None if it can't be parsed."""
    parts = raw_date.split('-')
    if len(parts) == 3:
        mm, _dd, yy = parts
    elif len(parts) == 1:
        s = parts[0]
        if len(s) == 8:        # MMDDYYYY
            mm, _dd, yy = s[0:2], s[2:4], s[4:8]
        elif len(s) == 7:      # MDDYYYY
            mm, _dd, yy = s[0:1], s[1:3], s[3:7]
        elif len(s) == 6:      # MMDDYY
            mm, _dd, yy = s[0:2], s[2:4], s[4:6]
        else:
            return None
    else:
        return None
    try:
        m_int = int(mm)
        year = int(yy)
    except ValueError:
        return None
    if not 1 <= m_int <= 12:
        return None
    if year < 100:
        year += 2000
    return f'{MONTHS[m_int - 1]}-{year}'


def rename_slug(dirname, taken=None):
    """Compute the new directory name from an old one. Returns None if no change.
    If `taken` is provided (set of names), append an internal-date suffix when
    the base rename would collide."""
    m = OUTER_DATE_RE.match(dirname)
    if not m:
        return None
    outer_date, rest = m.group(1), m.group(2)

    internal_suffix = None
    m2 = INTERNAL_DATE_RE.match(rest)
    if m2:
        internal_suffix = internal_date_to_suffix(m2.group(1))
        rest = m2.group(2)

    rest = re.sub(r'igorj2\.sg-host', 'rrchnm', rest)
    rest = re.sub(r'-+', '-', rest).strip('-')

    new_dirname = f'{outer_date}-{rest}'
    if taken is not None and new_dirname in taken and internal_suffix:
        new_dirname = f'{outer_date}-{rest}-{internal_suffix}'

    if new_dirname == dirname:
        return None
    return new_dirname


def update_slug_field(idx_path, new_slug):
    text = idx_path.read_text(encoding='utf-8')
    new_text = SLUG_FIELD_RE.sub(f'slug: {new_slug}', text, count=1)
    if new_text != text:
        idx_path.write_text(new_text, encoding='utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    all_dirs = set(os.listdir(BLOG_DIR))
    renames = []  # (old_path, new_path, new_slug)
    proposed = set()
    for d in sorted(os.listdir(BLOG_DIR)):
        full = BLOG_DIR / d
        if not full.is_dir():
            continue
        if 'igorj2.sg-host' not in d:
            continue
        # Pass `taken` so collisions get the date suffix.
        new_d = rename_slug(d, taken=all_dirs | proposed)
        if new_d is None:
            continue
        proposed.add(new_d)
        m = OUTER_DATE_RE.match(new_d)
        new_slug = m.group(2)
        renames.append((full, BLOG_DIR / new_d, new_slug))

    if not args.apply:
        print(f'Would rename {len(renames)} directories:')
        for old, new, slug in renames:
            print(f'  {old.name}\n  -> {new.name}')
        return

    for old, new, slug in renames:
        if new.exists():
            print(f'  SKIP (target exists): {new.name}')
            continue
        # Use git mv so the rename is tracked.
        subprocess.run(['git', 'mv', str(old), str(new)], check=True)
        idx = new / 'index.md'
        if idx.exists():
            update_slug_field(idx, slug)
    print(f'Renamed {len(renames)} directories.')


if __name__ == '__main__':
    main()
