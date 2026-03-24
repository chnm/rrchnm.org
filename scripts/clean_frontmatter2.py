#!/usr/bin/env python3
"""Second pass cleanup of funder entries."""

import re
import os

CONTENT_DIR = os.path.join(os.path.dirname(__file__), '..', 'content', 'projects')

# Known good funders
GOOD_FUNDERS = {
    'national endowment for the humanities',
    'andrew w. mellon foundation',
    'alfred p. sloan foundation',
    'institute of museum and library services',
    'american council of learned societies',
    'virginia foundation for the humanities',
    'united states diplomacy center',
    'una chapman cox foundation',
    'national science foundation',
    'national park service',
    'national historical publications and records commission',
    'monash university',
    'library of congress',
    'hewlett foundation',
    'florence gould foundation',
    'corporation for digital scholarship',
    'carnegie corporation',
    'samuel h kress foundation',
    'samuel h. kress foundation',
    'getty foundation',
    'u.s. department of education',
    'u.s. department of veterans',
    'spencer foundation',
    'davis foundation',
    'george mason university',
}

def is_good_funder(text):
    t = text.lower().strip()
    # Check against known good list
    if t in GOOD_FUNDERS:
        return True
    # Looks like a funder if it contains Foundation, Institute, NEH, etc.
    funder_words = ['foundation', 'institute', 'endowment', 'council', 'commission',
                    'university', 'library', 'museum', 'corporation', 'department', 'center']
    if any(w in t for w in funder_words):
        return True
    return False


def clean_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    if not content.startswith('---'):
        return False

    end = content.index('---', 3)
    frontmatter = content[3:end]
    body = content[end:]

    new_lines = []
    in_funders = False
    funder_items = []
    changed = False

    for line in frontmatter.split('\n'):
        if line.strip() == 'funders:':
            in_funders = True
            continue  # We'll re-add it with clean items
        if in_funders:
            if line.strip().startswith('- '):
                val = line.strip().lstrip('- ').strip('"')
                if is_good_funder(val):
                    funder_items.append(val)
                else:
                    changed = True
            else:
                in_funders = False
                # Write funders section
                if funder_items:
                    new_lines.append('funders:')
                    for f in funder_items:
                        new_lines.append(f'- "{f}"')
                else:
                    changed = True
                funder_items = []
                new_lines.append(line)
        else:
            new_lines.append(line)

    # Handle case where funders is last in frontmatter
    if in_funders and funder_items:
        new_lines.append('funders:')
        for f in funder_items:
            new_lines.append(f'- "{f}"')

    if changed:
        frontmatter = '\n'.join(new_lines)
        with open(filepath, 'w') as f:
            f.write('---\n' + frontmatter + body)

    return changed


def main():
    count = 0
    for fname in sorted(os.listdir(CONTENT_DIR)):
        if not fname.endswith('.md') or fname == '_index.md':
            continue
        filepath = os.path.join(CONTENT_DIR, fname)
        if clean_file(filepath):
            print(f'Cleaned: {fname}')
            count += 1
    print(f'\nCleaned {count} files')


if __name__ == '__main__':
    main()
