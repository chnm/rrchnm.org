# rrchnm.org task runner
# Run `just` to see all available commands.

# Default: list available recipes
default:
    @just --list

# ── Development ──────────────────────────────────────────────

# Start the dev server with live reload
dev:
    hugo server --buildDrafts --buildFuture --navigateToChanged

# Start the dev server (published content only, no drafts)
serve:
    hugo server

# Production build with minification
build:
    hugo --minify

# Install dependencies
setup:
    npm ci

# ── Content Creation ─────────────────────────────────────────

# Create a new blog post: just post "my-post-title"
post slug:
    hugo new blog/$(date +%Y-%m-%d)-{{slug}}/index.md
    @echo "Created: content/blog/$(date +%Y-%m-%d)-{{slug}}/index.md"

# Create a new project page: just project "project-name"
project slug:
    hugo new our-work/{{slug}}/index.md
    @echo "Created: content/our-work/{{slug}}/index.md"

# Create a new publication: just publication "publication-slug"
publication slug:
    hugo new publications/{{slug}}/index.md
    @echo "Created: content/publications/{{slug}}/index.md"

# Create a new spotlight: just spotlight "item-name"
spotlight slug:
    hugo new spotlight/{{slug}}.md
    @echo "Created: content/spotlight/{{slug}}.md"

# ── Content Helpers ──────────────────────────────────────────

# List all draft content
drafts:
    @grep -rl 'draft: true' content/ --include='*.md' | sort

# List all published (non-draft) blog posts from this year
recent:
    @ls -d content/blog/$(date +%Y)-*/ 2>/dev/null | sort -r | head -20

# Show posts missing a featured image
missing-images:
    @for dir in content/blog/202*/; do \
        if [ -f "$dir/index.md" ] && ! grep -q 'featured_image' "$dir/index.md"; then \
            echo "$dir"; \
        fi; \
    done

# List all categories in use, with counts
categories:
    @find content -name '*.md' -exec yq --front-matter=extract '.categories[]' {} \; 2>/dev/null | sort | uniq -c | sort -rn

# List all tags in use, with counts
tags:
    @find content -name '*.md' -exec yq --front-matter=extract '.tags[]' {} \; 2>/dev/null | sort | uniq -c | sort -rn

# ── Quality ──────────────────────────────────────────────────

# Check for broken internal links (requires Hugo build first)
check-links: build
    @echo "Checking for broken internal links..."
    @grep -r 'href="/' public/ --include='*.html' -oh | sort -u | while read link; do \
        path="public$link"; \
        if [ "$link" != "/" ] && [ ! -f "${path}index.html" ] && [ ! -f "$path" ] && [ ! -d "${path%/}" ]; then \
            echo "  broken: $link"; \
        fi; \
    done
    @echo "Done."

# Verify the site builds without errors
verify:
    hugo --minify 2>&1 | tail -10
