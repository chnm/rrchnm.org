#!/usr/bin/env python3
"""Clean up scraped frontmatter: remove srcset noise from gallery, bad funder entries."""

import re
import os

CONTENT_DIR = os.path.join(os.path.dirname(__file__), '..', 'content', 'projects')

# Funder entries that are clearly not funders
BAD_FUNDERS = {
    'date:', 'website:', 'visit', 'http', 'www.', '.org', '.com', '.edu',
    'related', 'project', 'read more', 'category', 'categories',
    'data driven', 'public history', 'education', 'the center',
}

def clean_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    if not content.startswith('---'):
        return False

    end = content.index('---', 3)
    frontmatter = content[3:end]
    body = content[end:]

    changed = False

    # Clean gallery entries - remove lines with srcset data (contain "w," or multiple URLs)
    new_lines = []
    for line in frontmatter.split('\n'):
        if 'gallery:' in line or not line.strip().startswith('- "'):
            new_lines.append(line)
            continue
        # Check if this is a gallery entry
        val = line.strip().lstrip('- ').strip('"')
        if val.startswith('/media/'):
            # Keep only clean paths (no srcset noise)
            if ' ' not in val and 'http' not in val:
                new_lines.append(line)
                changed = True if line not in new_lines else changed
            else:
                changed = True  # Dropped a bad line
        else:
            new_lines.append(line)

    frontmatter = '\n'.join(new_lines)

    # Clean funder entries
    new_lines = []
    in_funders = False
    for line in frontmatter.split('\n'):
        if line.strip() == 'funders:':
            in_funders = True
            new_lines.append(line)
            continue
        if in_funders:
            if line.strip().startswith('- '):
                val = line.strip().lstrip('- ').strip('"').lower()
                # Skip bad entries
                if any(bad in val for bad in BAD_FUNDERS):
                    changed = True
                    continue
                if len(val) < 4:
                    changed = True
                    continue
                new_lines.append(line)
            else:
                in_funders = False
                new_lines.append(line)
        else:
            new_lines.append(line)

    frontmatter = '\n'.join(new_lines)

    # Remove empty gallery/funders sections
    frontmatter = re.sub(r'gallery:\n(?=\w)', '', frontmatter)
    frontmatter = re.sub(r'funders:\n(?=\w)', '', frontmatter)

    if changed:
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
