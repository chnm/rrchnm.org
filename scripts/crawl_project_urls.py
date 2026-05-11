#!/usr/bin/env python3
"""Second pass: extract project website URLs from WordPress pages."""

import re
import os
import sys
import urllib.request

CONTENT_DIR = os.path.join(os.path.dirname(__file__), '..', 'content', 'projects')
BASE_URL = 'https://rrchnm.org/portfolio-item/'


def fetch_page(slug):
    url = BASE_URL + slug + '/'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        return None


def extract_project_url(html):
    """Try multiple patterns to find the project website URL."""

    # Pattern 1: "Website:" followed by a link
    m = re.search(r'Website:\s*</?\w[^>]*>\s*<a[^>]+href="([^"]+)"', html, re.IGNORECASE)
    if m:
        return m.group(1)

    # Pattern 2: "Website:" in text then a link nearby
    m = re.search(r'Website:.*?<a[^>]+href="([^"]+)"', html[:html.find('</article>') if '</article>' in html else len(html)], re.DOTALL | re.IGNORECASE)
    if m and 'rrchnm.org' not in m.group(1):
        return m.group(1)

    # Pattern 3: elementor button with "Visit" text
    m = re.search(r'<a[^>]+href="([^"]+)"[^>]*>(?:[^<]*<[^>]+>)*[^<]*Visit[^<]*</a>', html, re.IGNORECASE)
    if m and 'rrchnm.org' not in m.group(1):
        return m.group(1)

    # Pattern 4: Link text that looks like a domain
    m = re.search(r'<a[^>]+href="(https?://(?!rrchnm\.org)[^"]+)"[^>]*>\s*\w+\.\w+\s*</a>', html)
    if m:
        return m.group(1)

    return None


def update_frontmatter(filepath, project_url):
    with open(filepath, 'r') as f:
        content = f.read()

    if 'project_url:' in content:
        return False

    if not content.startswith('---'):
        return False

    end = content.index('---', 3)
    frontmatter = content[3:end]
    body = content[end+3:]

    frontmatter += f'project_url: "{project_url}"\n'

    with open(filepath, 'w') as f:
        f.write('---\n' + frontmatter + '---' + body)

    return True


def main():
    slugs = []
    for fname in sorted(os.listdir(CONTENT_DIR)):
        if fname.endswith('.md') and fname != '_index.md':
            filepath = os.path.join(CONTENT_DIR, fname)
            with open(filepath) as f:
                content = f.read()
            # Skip if already has project_url
            if 'project_url:' in content:
                continue
            match = re.search(r'^slug:\s*(.+)$', content, re.MULTILINE)
            if match:
                slugs.append((match.group(1).strip(), filepath))

    print(f'Found {len(slugs)} projects without URLs to crawl')

    found = 0
    for i, (slug, filepath) in enumerate(slugs):
        print(f'[{i+1}/{len(slugs)}] {slug}...', end=' ', flush=True)
        html = fetch_page(slug)
        if html:
            url = extract_project_url(html)
            if url:
                update_frontmatter(filepath, url)
                print(f'FOUND: {url[:60]}')
                found += 1
            else:
                print('no URL found')
        else:
            print('fetch failed')

    print(f'\nFound URLs for {found}/{len(slugs)} projects')


if __name__ == '__main__':
    main()
