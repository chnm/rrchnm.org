#!/usr/bin/env python3
"""Phase 4 blog cleanup: prune low-value posts among the currently-published set.

Apply the same deletion patterns used in Phase 2, but to ALL posts (since
Phase 2 only touched drafts). Produces a CSV of proposed deletes for review,
and only acts with --apply.

Spare rules (identical to Phase 2):
  - Director-change posts
  - DH2024 posts
  - Institutional milestones (in memory, remembering, anniversaries, etc.)
  - Posts mentioning still-listed projects from data/projects.yaml
  - Posts by Roy Rosenzweig, Mills Kelly, Sharon Leon
"""

import argparse
import csv
import os
import re
import shutil
from pathlib import Path

# Reuse Phase 2 classification.
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cleanup_blog_phase2 import (
    BLOG_DIR, DELETION_PATTERNS, MAJOR_AUTHORS, PROJECT_TITLES,
    SPARE_DH2024, SPARE_DIRECTOR, SPARE_INSTITUTIONAL,
    parse_frontmatter,
)

CSV_PATH = Path(__file__).resolve().parent.parent / 'blog-phase4-disposition.csv'

# Title-only patterns that mark a post as personnel regardless of body length.
# Order: director-change spare and institutional milestone spare run first;
# this catches what's left.
STRICT_PERSONNEL_TITLE_RE = re.compile(
    r'\b('
    r'(rrchnm|chnm)\s+welcomes\b|'
    r'welcomes?\b.*\bto\s+(the\s+)?(staff|center|team|rrchnm|chnm)\b|'
    r'^welcome,?\s+[A-Z]|'
    r'congratulations\b|'
    r'(rrchnm|chnm|we)\s+joins?\b|'
    r'joins?\s+(the\s+)?(staff|center|team|rrchnm|chnm|r2 studios|.* network)\b|'
    r'hiring (a|an)\b|'
    r'(is|are)\s+hiring\b|'
    r'come work with us\b|'
    r'farewell\b'
    r')',
    re.IGNORECASE | re.MULTILINE)


def classify(directory, meta, body):
    body_len = len(body.strip())
    title = meta.get('title', '')
    authors = meta.get('authors', [])
    haystack = f'{title}\n{body}'

    if SPARE_DH2024.search(haystack):
        return 'keep', 'dh2024 spare'
    if SPARE_DIRECTOR.search(title):
        return 'keep', 'director-change spare'
    if SPARE_INSTITUTIONAL.search(title):
        return 'keep', 'institutional milestone spare'

    if STRICT_PERSONNEL_TITLE_RE.search(title):
        return 'delete', f'personnel post: "{title}"'

    haystack_lower = haystack.lower()
    project_match = next((p for p in PROJECT_TITLES if p in haystack_lower), None)

    hits = []
    for name, regex in DELETION_PATTERNS.items():
        if regex.search(haystack):
            hits.append(name)

    has_major_author = bool(set(authors) & MAJOR_AUTHORS)
    if has_major_author and body_len >= 1000:
        return 'keep', f'major author ({",".join(set(authors) & MAJOR_AUTHORS)})'

    is_igorj_stub = 'igorj2.sg-host' in directory

    if body_len < 300 and not project_match:
        return 'delete', 'short (<300ch) stub'

    if is_igorj_stub and body_len < 800 and not project_match:
        return 'delete', 'igorj2.sg-host stub (<800ch)'

    if body_len < 1200 and hits and not project_match:
        return 'delete', f'<1200ch + {",".join(hits)}'

    if project_match:
        return 'keep', f'project mention: {project_match}'

    return 'keep', f'no delete signal (len={body_len})'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    rows = []
    counts = {'keep': 0, 'delete': 0}
    for d in sorted(os.listdir(BLOG_DIR)):
        full = BLOG_DIR / d
        if not full.is_dir():
            continue
        idx = full / 'index.md'
        if not idx.exists():
            continue
        text = idx.read_text(encoding='utf-8')
        meta, body = parse_frontmatter(text)
        if meta is None:
            continue
        action, reason = classify(d, meta, body)
        counts[action] += 1
        rows.append([d, meta.get('title', ''), meta.get('date', ''),
                     len(body.strip()), action, reason])
        if args.apply and action == 'delete':
            shutil.rmtree(full)

    with CSV_PATH.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['directory', 'title', 'date', 'body_len', 'action', 'reason'])
        for r in rows:
            w.writerow(r)
    print(f'Wrote {CSV_PATH} ({len(rows)} rows)')
    print(f'Counts: {counts}')
    if not args.apply:
        print('Dry run. Re-run with --apply to delete.')


if __name__ == '__main__':
    main()
