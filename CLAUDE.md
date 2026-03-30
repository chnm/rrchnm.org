# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hugo static site for the Roy Rosenzweig Center for History and New Media (RRCHNM) at George Mason University. Uses Tailwind CSS for styling.

## Commands

- **Dev server:** `just dev` (runs `hugo server --buildDrafts --navigateToChanged`)
- **Production build:** `just build` (runs `hugo --minify`)
- **Install dependencies:** `just setup` (runs `npm ci`)

Hugo Extended 0.154.5+ is required (for CSS processing).

## Architecture

### Content Types

Content lives in `content/` with four main sections:

- **blog/** — Blog posts (555+), frontmatter: `author_name`, `authors`, `categories`, `date`, `slug`, `draft`, `lede`
- **our-work/** — Project pages (57+), served at `/projects/`, frontmatter: `categories`, `featured_image`, `project_url`, `funders`, `gallery`, `featured_project`, `status`
- **publications/** — Research publications (54+), frontmatter: `essay_author`, `essay_date`, `pub_date`, `essay_publication_info`
- **page/** — Static pages (about, contact, policies, education)
- **spotlight/** — Featured spotlight content for homepage callout

### Layout System

Templates in `layouts/` follow Hugo conventions:
- `layouts/index.html` — Homepage with spotlight, featured projects, latest posts, and CRDH callout
- `layouts/{section}/single.html` and `list.html` — Section templates
- `layouts/page/*.html` — Custom page layouts matched by filename to `content/page/` slugs
- `layouts/our-work/list.html` — Project listing with Alpine.js category filtering, active/inactive separation
- `layouts/partials/` — Shared components (header, footer, nav, breadcrumbs, featured-image, social-icons)
- `layouts/shortcodes/` — Custom Hugo shortcodes

### Data-Driven Configuration

YAML files in `data/` drive site structure:
- `menus.yaml` — Navigation (top_nav, mobile_nav, footer)
- `people.yaml` — Staff directory (rendered via `layouts/page/our-people.html`)
- `dissertations.yaml` — Digital dissertations list (rendered on graduate education page)
- `footer.yaml` — Footer configuration

### Image Handling

Images use a dual approach handled by `layouts/partials/featured-image.html`:
- **Page bundle resources** — Images co-located with content in the same directory (e.g., `content/our-work/project-name/image.jpg`), referenced by bare filename in frontmatter
- **Static assets** — Shared images in `static/img/` (site assets) and `static/media/` (content images), referenced by absolute path (e.g., `/media/reports/file.pdf`)

The `featured-image.html` partial auto-detects which type: paths starting with `/` or `http` are used as-is; otherwise resolved as page resources. Gallery templates use the same logic.

Prefer page bundle resources for project/content-specific images. Use `static/` for shared assets (logos, default images, PDFs). Organize `static/media/` by topic (e.g., `reports/`, `grad/`), not by date.

### Styling

- `assets/css/main.css` — Tailwind CSS with `@layer` directives (base, components, utilities)
- `tailwind.config.js` — Custom brand colors (`red-brand: #C32A26`), IBM Plex font family (Serif, Sans, Mono), max-width `max-w-site` (1200px)
- Typography plugin (`@tailwindcss/typography`) with customized prose styles
- All containers use consistent `mx-auto max-w-site px-6 lg:px-10` for alignment

### JavaScript

- Alpine.js for interactive UI (project filtering, staff modals)
- Client-side search with Cmd-K shortcut (Hugo JSON output generates search index)

### SEO & Social

- Open Graph and Twitter Card meta tags via Hugo's internal templates
- RSS autodiscovery in `<head>`
- Canonical URLs on all pages
- `params.images` in `hugo.yaml` provides default social sharing image

### CI/CD

GitHub Actions (`.github/workflows/cicd.yml`) builds on pushes to `main` and `preview`:
1. Hugo build with minification
2. Docker image (Nginx + built static files) pushed to ghcr.io
3. Deployed to rrchnm.org

### Hugo Configuration

Key settings in `hugo.yaml`:
- Unsafe HTML rendering enabled in Goldmark
- Blog permalinks: `/blog/:slug/`
- Projects section served at `/projects/` (via `url:` in `_index.md`)
- Pagination: 12 items per page
- Taxonomies: categories and tags
- JSON output on homepage for search index
- Social media links in `params.social` (conditionally rendered — URL must be present)

### URL Redirects

Static redirects configured in `static/_redirects`, including `/our-work/` → `/projects/`.

### Project Status

Projects use a `status` field in frontmatter to indicate active/inactive state:
```yaml
status:
- active: false
```
Inactive projects appear in a separate "Past Projects" section on the projects page.
