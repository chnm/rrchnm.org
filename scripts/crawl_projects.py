#!/usr/bin/env python3
"""
Crawl RRCHNM WordPress project pages to extract:
- Project website URL
- Funder information
- Additional project images
Then update Hugo content files with the extracted data.
"""

import re
import os
import sys
import json
import urllib.request
from html.parser import HTMLParser

CONTENT_DIR = os.path.join(os.path.dirname(__file__), '..', 'content', 'projects')
BASE_URL = 'https://rrchnm.org/portfolio-item/'

class ProjectPageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_content = False
        self.in_funder = False
        self.funders = []
        self.project_url = None
        self.images = []
        self.current_tag = None
        self.current_attrs = {}
        self.depth = 0
        self.content_depth = 0
        self.text_buffer = ''
        self.all_links = []
        self.all_text = []
        self.in_main = False
        self.main_depth = 0

    def handle_starttag(self, tag, attrs):
        self.depth += 1
        self.current_tag = tag
        self.current_attrs = dict(attrs)

        attr_dict = dict(attrs)

        # Track when we're in main content area
        classes = attr_dict.get('class', '')
        if 'entry-content' in classes or 'elementor-widget-container' in classes or 'portfolio-content' in classes:
            self.in_main = True
            self.main_depth = self.depth

        if tag == 'img' and self.in_main:
            src = attr_dict.get('src', '')
            if src and 'uploads' in src and 'thumbnail' not in src and 'logo' not in src and 'icon' not in src and 'Untitled-design' not in src:
                # Skip small thumbnails in related sections
                if 'scaled' in src or any(f'-{i}.' in src or f'-{i}-' in src for i in range(10)):
                    self.images.append(src)

        if tag == 'a':
            href = attr_dict.get('href', '')
            if href:
                self.all_links.append(href)

    def handle_endtag(self, tag):
        if self.in_main and self.depth <= self.main_depth:
            self.in_main = False
        self.depth -= 1

    def handle_data(self, data):
        text = data.strip()
        if text:
            self.all_text.append(text)


def fetch_page(slug):
    url = BASE_URL + slug + '/'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f'  FAIL fetch: {e}', file=sys.stderr)
        return None


def extract_data(html, slug):
    """Extract project URL, funders, and images from HTML."""
    result = {
        'project_url': None,
        'funders': [],
        'images': []
    }

    # Find project images - look for scaled images or numbered project screenshots
    # Pattern: /uploads/YYYY/MM/ProjectName-N-scaled.jpg or similar
    img_pattern = re.compile(r'https?://rrchnm\.org/wp-content/uploads/\d{4}/\d{2}/[^"\']+(?:-scaled|-\d)\.[^"\']+', re.IGNORECASE)
    found_images = set()
    for match in img_pattern.finditer(html):
        img_url = match.group(0)
        # Filter out thumbnails and unrelated images
        if 'thumbnail' not in img_url.lower() and 'untitled' not in img_url.lower():
            found_images.add(img_url)
    result['images'] = sorted(found_images)

    # Find funders - they appear in a specific section, usually after "Funders" or "Funded by"
    # Look for list items or text near funder-related keywords
    funder_section = re.search(r'(?:Funder|Funded by|Funding|Sponsor)[^<]*</(?:h[2-6]|p|div|strong)>(.*?)(?=<h[2-6]|<div class="(?:elementor-element|related)|$)', html, re.DOTALL | re.IGNORECASE)
    if funder_section:
        funder_html = funder_section.group(1)
        # Extract from list items
        funder_items = re.findall(r'<li[^>]*>([^<]+)</li>', funder_html)
        if funder_items:
            result['funders'] = [f.strip() for f in funder_items if f.strip()]
        else:
            # Try paragraphs or plain text
            funder_texts = re.findall(r'>([^<]+)<', funder_html)
            result['funders'] = [f.strip() for f in funder_texts if f.strip() and len(f.strip()) > 3]

    # Also try a simpler pattern - funders often in a widget or specific div
    if not result['funders']:
        funder_list = re.findall(r'<li[^>]*class="[^"]*funder[^"]*"[^>]*>([^<]+)</li>', html, re.IGNORECASE)
        if funder_list:
            result['funders'] = [f.strip() for f in funder_list]

    # Try yet another pattern - elementor text widgets after "Funders" heading
    if not result['funders']:
        sections = re.split(r'<(?:h[2-6]|strong|b)[^>]*>', html)
        for i, section in enumerate(sections):
            if re.match(r'\s*Funder', section, re.IGNORECASE):
                # Get the next section's list items or text
                if i + 1 < len(sections):
                    next_section = sections[i + 1]
                    items = re.findall(r'<li[^>]*>\s*(?:<[^>]+>)*\s*([^<]+)', next_section)
                    if items:
                        result['funders'] = [f.strip() for f in items if f.strip() and len(f.strip()) > 3]
                        break
                    # Try line-by-line text
                    lines = re.findall(r'>([^<]{4,})<', next_section[:2000])
                    potential = [l.strip() for l in lines if l.strip() and not l.strip().startswith('http') and len(l.strip()) > 3]
                    if potential and len(potential) < 15:
                        result['funders'] = potential
                        break

    # Find project URL - look for prominent external links
    # Usually in a "Visit" button or the first external link in content
    visit_pattern = re.search(r'(?:Visit|Website|Project Site|View Project)[^<]*</(?:a|button|span)>|<a[^>]+href="([^"]+)"[^>]*>[^<]*(?:Visit|Website|View)', html, re.IGNORECASE)
    if visit_pattern:
        url = visit_pattern.group(1) if visit_pattern.group(1) else None
        if url and 'rrchnm.org' not in url:
            result['project_url'] = url

    # Also try finding project URL from elementor button widgets
    if not result['project_url']:
        button_links = re.findall(r'<a[^>]+class="[^"]*(?:elementor-button|btn)[^"]*"[^>]+href="([^"]+)"', html)
        for link in button_links:
            if 'rrchnm.org' not in link and link.startswith('http'):
                result['project_url'] = link
                break

    # Try any prominent external link in the content area
    if not result['project_url']:
        content_match = re.search(r'class="entry-content"(.*?)(?:class="related|class="sidebar|$)', html, re.DOTALL)
        if content_match:
            content = content_match.group(1)
            external_links = re.findall(r'href="(https?://(?!rrchnm\.org)[^"]+)"', content)
            if external_links:
                result['project_url'] = external_links[0]

    return result


def update_frontmatter(filepath, data):
    """Update Hugo frontmatter with extracted data."""
    with open(filepath, 'r') as f:
        content = f.read()

    # Parse frontmatter
    if not content.startswith('---'):
        return False

    end = content.index('---', 3)
    frontmatter = content[3:end]
    body = content[end+3:]

    changed = False

    # Add project_url if not present and we found one
    if data['project_url'] and 'project_url:' not in frontmatter:
        frontmatter += f'project_url: "{data["project_url"]}"\n'
        changed = True

    # Add funders if not present and we found some
    if data['funders'] and 'funders:' not in frontmatter:
        frontmatter += 'funders:\n'
        for funder in data['funders']:
            funder = funder.replace('"', '\\"')
            frontmatter += f'- "{funder}"\n'
        changed = True

    # Add extra images if we found any beyond the featured image
    if data['images'] and 'gallery:' not in frontmatter:
        # Convert WP URLs to local paths
        local_images = []
        for img_url in data['images']:
            # /wp-content/uploads/YYYY/MM/file.jpg -> /media/YYYY/MM/file.jpg
            match = re.search(r'/uploads/(\d{4}/\d{2}/[^?]+)', img_url)
            if match:
                local_path = '/media/' + match.group(1)
                local_images.append(local_path)

        if local_images:
            frontmatter += 'gallery:\n'
            for img in local_images:
                frontmatter += f'- "{img}"\n'
            changed = True

    if changed:
        with open(filepath, 'w') as f:
            f.write('---\n' + frontmatter + '---' + body)

    return changed


def main():
    slugs = []
    for fname in sorted(os.listdir(CONTENT_DIR)):
        if fname.endswith('.md') and fname != '_index.md':
            filepath = os.path.join(CONTENT_DIR, fname)
            with open(filepath) as f:
                content = f.read()
            match = re.search(r'^slug:\s*(.+)$', content, re.MULTILINE)
            if match:
                slugs.append((match.group(1).strip(), filepath))

    print(f'Found {len(slugs)} projects to crawl')

    results = {}
    for i, (slug, filepath) in enumerate(slugs):
        print(f'[{i+1}/{len(slugs)}] {slug}...', end=' ', flush=True)
        html = fetch_page(slug)
        if html:
            data = extract_data(html, slug)
            updated = update_frontmatter(filepath, data)
            status = []
            if data['project_url']: status.append(f"url={data['project_url'][:40]}")
            if data['funders']: status.append(f"{len(data['funders'])} funders")
            if data['images']: status.append(f"{len(data['images'])} images")
            print(f"{'UPDATED' if updated else 'no change'} ({', '.join(status) if status else 'nothing found'})")
            results[slug] = data
        else:
            print('SKIP (fetch failed)')

    # Summary
    with_url = sum(1 for d in results.values() if d['project_url'])
    with_funders = sum(1 for d in results.values() if d['funders'])
    with_images = sum(1 for d in results.values() if d['images'])
    print(f'\nSummary: {with_url} with URLs, {with_funders} with funders, {with_images} with images')


if __name__ == '__main__':
    main()
