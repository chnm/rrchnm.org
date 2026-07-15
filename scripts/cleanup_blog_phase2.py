#!/usr/bin/env python3
"""Phase 2 blog cleanup: resolve drafts (publish, delete, or flag for review).

Classification heuristics:
  - < 500 chars + any pattern hit            -> delete
  - < 1500 chars + deletion pattern          -> delete
  - >= 1500 chars + no pattern hits          -> publish
  - >= 1000 chars + major-author             -> publish (skip pattern check)
  - everything else                          -> review (manual CSV)

Always-spare rules (override delete):
  - Director-change posts
  - DH2024 posts
  - Substantive tributes (>2000 chars with personnel pattern)

Modes:
  --dry-run (default)   write CSV, make no file changes
  --apply               apply auto actions, write review CSV
  --apply-csv <path>    apply user-edited CSV decisions

The CSV has columns: directory, title, date, author, body_len, action, reason.
"""

import argparse
import csv
import os
import re
import shutil
import sys
from pathlib import Path

BLOG_DIR = Path(__file__).resolve().parent.parent / 'content' / 'blog'
CSV_PATH = Path(__file__).resolve().parent.parent / 'blog-drafts-disposition.csv'

DELETION_PATTERNS = {
    'staff_personnel': re.compile(
        r'\b(welcomes?|farewells?|congratulations|joins (the|us|our|the staff)|'
        r'hiring|hires|departs?|leaves us|leaves rrchnm|leaves chnm|retires?|'
        r'promoted|appointed|in memory of|obituary|new staff|new hire|'
        r'fellowship awarded to|defended (her|his|their) dissertation|'
        r'we are pleased to welcome|we are hiring|join(ing|s) chnm|'
        r'join(ing|s) rrchnm|farewell to|come work with us)\b',
        re.IGNORECASE),
    'press_blurb': re.compile(
        r'\b(presented at|featured (in|on)|mentioned in|interviewed by|'
        r'discusses .* (on|in)|to speak at|will present|reviewed in|'
        r'recognized by|named (in|as|to)|profiled in|quoted in|'
        r'cited in|appears in|appears on)\b',
        re.IGNORECASE),
    'event_reminder': re.compile(
        r'\b(register now|upcoming workshop|reminder:|countdown|'
        r"one month until|don't forget|join us (for|on)|"
        r'workshop on \d|conference next|conference this|'
        r'this thursday|this friday|this week|'
        r'tomorrow|in two weeks)\b',
        re.IGNORECASE),
    'conference_attendance': re.compile(
        r'\b(connect with .* at|rrchnm at .*\d{2}|chnm at .*\d{2}|'
        r'at aha\s?\d|at mla\s?\d|at oah\s?\d|at digital humanities\s?\d|'
        r'at the .* conference|at the .* annual meeting|'
        r'see (us|you) (at|in))\b',
        re.IGNORECASE),
    'minor_award': re.compile(
        # Individual faculty/staff honors and routine recognitions.
        # Deliberately excludes grant news (NEH/IMLS/Mellon/Sloan/foundation
        # awards), which are project-relevant.
        r'\b('
        r'outstanding (faculty|teaching|service) award|'
        r'distinguished (faculty|teaching) award|'
        r'wins .* (prize|medal|fellowship to)|'
        r'receives .* fellowship to|'
        r'named to the .* (society|academy)|'
        r'recognized by .* (society|association|academy)|'
        r'(honorary degree|honorary doctorate|named fellow of)'
        r')\b',
        re.IGNORECASE),
}

SPARE_DIRECTOR = re.compile(
    r'\b(executive director|director of (rrchnm|chnm|the center)|'
    r'appointed director|new director|incoming director|outgoing director|'
    r'interim director|succeed.* as director|new associate director|'
    r'as director of)\b',
    re.IGNORECASE)

SPARE_DH2024 = re.compile(
    r'(dh\s?2024|digital humanities\s?2024|dh-2024)',
    re.IGNORECASE)

SPARE_INSTITUTIONAL = re.compile(
    r'\b(newly named|center.* named|naming of the center|'
    r'roy rosenzweig forum|rosenzweig forum|'
    r'roy rosenzweig prize|rosenzweig prize|'
    r'10th anniversary|20th anniversary|25th anniversary|30th anniversary|'
    r'in memory of|remembering [a-z])\b',
    re.IGNORECASE)

MAJOR_AUTHORS = {
    'Roy Rosenzweig', 'Mills Kelly', 'Sharon Leon',
}

PROJECT_KEYWORDS_PATH = Path(__file__).resolve().parent.parent / 'data' / 'projects.yaml'


def load_project_keywords():
    """Extract project title tokens from projects.yaml for the spare rule."""
    import yaml
    with PROJECT_KEYWORDS_PATH.open() as f:
        projects = yaml.safe_load(f)
    titles = []
    for p in projects:
        t = (p.get('title') or '').strip().lower()
        if t and len(t) > 6:
            titles.append(t)
    return titles


PROJECT_TITLES = load_project_keywords()


def parse_frontmatter(text):
    """Crude YAML-ish parse of frontmatter. Returns (dict, body) or (None, text)."""
    if not text.startswith('---\n'):
        return None, text
    end = text.find('\n---\n', 4)
    if end < 0:
        return None, text
    fm_text = text[4:end]
    body = text[end + 5:]

    meta = {}
    current_list_key = None
    for line in fm_text.split('\n'):
        if not line.strip():
            continue
        if line.startswith(('- ', '  - ', '\t- ')) and current_list_key:
            val = line.lstrip(' \t-').strip().strip("'\"")
            meta.setdefault(current_list_key, []).append(val)
            continue
        m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$', line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val == '':
                current_list_key = key
                meta.setdefault(key, [])
            else:
                current_list_key = None
                meta[key] = val.strip("'\"")
    return meta, body


def set_draft_false(text):
    """Replace `draft: true` with `draft: false` in frontmatter."""
    return re.sub(r'^draft:\s*true\s*$', 'draft: false',
                  text, count=1, flags=re.MULTILINE)


def classify(directory, meta, body):
    body_len = len(body.strip())
    title = meta.get('title', '')
    authors = meta.get('authors', [])
    haystack = f'{title}\n{body}'

    if SPARE_DH2024.search(haystack):
        return 'publish', 'dh2024 spare'
    if SPARE_DIRECTOR.search(title):
        return 'publish', 'director-change spare'
    if SPARE_INSTITUTIONAL.search(title):
        return 'publish', 'institutional milestone spare'

    haystack_lower = haystack.lower()
    project_match = next(
        (p for p in PROJECT_TITLES if p in haystack_lower),
        None)

    hits = []
    for name, regex in DELETION_PATTERNS.items():
        if regex.search(haystack):
            hits.append(name)

    has_major_author = bool(set(authors) & MAJOR_AUTHORS)

    is_igorj_stub = 'igorj2.sg-host' in directory

    if body_len < 300 and not project_match:
        return 'delete', 'short (<300ch) stub'

    if is_igorj_stub and body_len < 800 and not project_match:
        return 'delete', f'igorj2.sg-host stub (<800ch)'

    if body_len < 1200 and hits and not project_match:
        return 'delete', f'<1200ch + {",".join(hits)}'

    if has_major_author and body_len >= 1000:
        return 'publish', f'major author ({",".join(set(authors) & MAJOR_AUTHORS)})'

    if project_match and body_len >= 400:
        return 'publish', f'mentions project: {project_match}'

    if body_len >= 1500 and not hits:
        return 'publish', 'substantive, no deletion patterns'

    if body_len >= 2000 and hits:
        return 'publish', f'long ({body_len}ch), pattern-matched but kept: {",".join(hits)}'

    return 'publish', f'default-publish (len={body_len}, hits={",".join(hits) or "none"})'


def load_drafts():
    drafts = []
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
        if meta.get('draft') != 'true':
            continue
        drafts.append((d, meta, body, text, idx))
    return drafts


def apply_action(idx_path, dirpath, action, text):
    if action == 'publish':
        idx_path.write_text(set_draft_false(text), encoding='utf-8')
    elif action == 'delete':
        shutil.rmtree(dirpath)


def write_csv(rows):
    with CSV_PATH.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['directory', 'title', 'date', 'author', 'body_len', 'action', 'reason'])
        for r in rows:
            w.writerow(r)
    print(f'Wrote {CSV_PATH} ({len(rows)} rows)')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--apply-csv', dest='apply_csv', type=Path)
    args = ap.parse_args()

    if args.apply_csv:
        # Read CSV and apply user's decisions for each row.
        applied = {'publish': 0, 'delete': 0, 'skip': 0}
        with args.apply_csv.open(encoding='utf-8') as f:
            for row in csv.DictReader(f):
                d = row['directory']
                action = row['action'].strip().lower()
                full = BLOG_DIR / d
                if not full.is_dir():
                    print(f'  skip missing: {d}')
                    continue
                idx = full / 'index.md'
                text = idx.read_text(encoding='utf-8')
                if action == 'publish':
                    idx.write_text(set_draft_false(text), encoding='utf-8')
                    applied['publish'] += 1
                elif action == 'delete':
                    shutil.rmtree(full)
                    applied['delete'] += 1
                else:
                    applied['skip'] += 1
        print(f'Applied from CSV: {applied}')
        return

    drafts = load_drafts()
    rows = []
    counts = {'publish': 0, 'delete': 0, 'review': 0}
    for d, meta, body, text, idx in drafts:
        action, reason = classify(d, meta, body)
        counts[action] += 1
        authors = meta.get('authors', [])
        author_str = '|'.join(authors) if isinstance(authors, list) else str(authors)
        rows.append([d, meta.get('title', ''), meta.get('date', ''),
                     author_str, len(body.strip()), action, reason])
        if args.apply and action in ('publish', 'delete'):
            apply_action(idx, BLOG_DIR / d, action, text)

    write_csv(rows)
    print(f'Counts: {counts}  (total drafts processed: {len(drafts)})')
    if not args.apply:
        print('Dry run — no files changed. Run with --apply to act on publish/delete.')


if __name__ == '__main__':
    main()
