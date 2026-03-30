#!/usr/bin/env python3
"""Generate lede summaries for blog posts that don't have one.

Extracts the first 1-2 meaningful sentences from the post body content
and adds them as a `lede` field in the YAML frontmatter.
"""

import re
import glob
import sys


def extract_frontmatter_and_body(content):
    """Split content into frontmatter and body."""
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        return None, content
    return match.group(1), match.group(2)


def has_lede(frontmatter):
    """Check if frontmatter already has a lede field."""
    return bool(re.search(r'^lede:', frontmatter, re.MULTILINE))


def clean_markdown(text):
    """Strip markdown formatting to get plain text."""
    # Remove images
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove links but keep text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove headings
    text = re.sub(r'^#{1,6}\s+.*$', '', text, flags=re.MULTILINE)
    # Remove bold/italic markers
    text = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', text)
    text = re.sub(r'_{1,3}([^_]+)_{1,3}', r'\1', text)
    # Remove blockquotes
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)
    # Remove shortcodes
    text = re.sub(r'\{\{[<>].*?[<>]\}\}', '', text)
    # Remove list markers
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
    # Remove numbered lists
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
    # Collapse whitespace
    text = re.sub(r'\n\s*\n', '\n', text)
    text = re.sub(r'  +', ' ', text)
    return text.strip()


def extract_sentences(text, max_sentences=2, max_chars=300):
    """Extract the first N meaningful sentences."""
    # Split into sentences (rough but good enough)
    sentences = re.split(r'(?<=[.!?])\s+', text)

    result = []
    char_count = 0
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        # Skip very short fragments
        if len(s) < 15:
            continue
        # Skip sentences that are just URLs
        if s.startswith('http'):
            continue
        result.append(s)
        char_count += len(s)
        if len(result) >= max_sentences or char_count > max_chars:
            break

    return ' '.join(result)


def escape_yaml_string(s):
    """Escape a string for use in YAML double quotes."""
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace('\n', ' ')
    # Remove any remaining problematic chars
    s = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', s)
    return s


def process_file(filepath):
    """Process a single blog post file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    frontmatter, body = extract_frontmatter_and_body(content)
    if frontmatter is None:
        return False, "no frontmatter"

    if has_lede(frontmatter):
        return False, "already has lede"

    # Clean and extract
    clean = clean_markdown(body)
    if not clean:
        return False, "no body content"

    lede = extract_sentences(clean)
    if not lede or len(lede) < 20:
        return False, "lede too short"

    # Truncate if too long
    if len(lede) > 300:
        # Cut at last sentence boundary before 300 chars
        truncated = lede[:300]
        last_period = truncated.rfind('.')
        if last_period > 100:
            lede = truncated[:last_period + 1]
        else:
            lede = truncated.rstrip() + '...'

    escaped = escape_yaml_string(lede)

    # Insert lede after title line
    new_frontmatter = re.sub(
        r'(^title:.*$)',
        r'\1\nlede: "' + escaped + '"',
        frontmatter,
        count=1,
        flags=re.MULTILINE
    )

    new_content = f'---\n{new_frontmatter}\n---\n{body}'

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True, lede[:80]


def main():
    files = glob.glob('/Users/jheppler/work/chnm/rrchnm.org/content/blog/*/index.md')
    files.sort()

    updated = 0
    skipped = 0
    errors = 0

    for filepath in files:
        try:
            success, msg = process_file(filepath)
            if success:
                updated += 1
            else:
                skipped += 1
        except Exception as e:
            errors += 1
            print(f"ERROR: {filepath}: {e}", file=sys.stderr)

    print(f"Done. Updated: {updated}, Skipped: {skipped}, Errors: {errors}")


if __name__ == '__main__':
    main()
