# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hugo static site for the Roy Rosenzweig Center for History and New Media (RRCHNM) at George Mason University. Currently on the `tailwind-redesign` branch migrating to Tailwind CSS.

## Commands

- **Dev server:** `npm run dev` (runs `hugo server`)
- **Production build:** `npm run build` (runs `hugo --minify`)
- **Install dependencies:** `npm ci`

Hugo Extended 0.154.5+ is required (for CSS processing).

## Architecture

### Content Types

Content lives in `content/` with four main sections:

- **blog/** — Blog posts (555+), frontmatter: `author_name`, `categories`, `date`, `slug`, `draft`
- **projects/** — Project pages (57+), frontmatter: `categories`, `featured_image`, `project_url`, `funders`, `gallery`
- **publications/** — Research publications (54+), frontmatter: `essay_author`, `essay_date`, `pub_date`, `essay_publication_info`
- **page/** — Static pages (about, contact, policies, education)

### Layout System

Templates in `layouts/` follow Hugo conventions:
- `layouts/index.html` — Homepage with featured projects and latest posts
- `layouts/{section}/single.html` and `list.html` — Section templates
- `layouts/page/*.html` — Custom page layouts (e.g., `our-work.html` uses Alpine.js for category filtering, `our-people.html` has staff modal)
- `layouts/partials/` — Shared components (header, footer, nav, breadcrumbs)
- `layouts/shortcodes/` — Custom Hugo shortcodes

### Data-Driven Configuration

YAML files in `data/` drive site structure:
- `menus.yaml` — Navigation (top_nav, mobile_nav, footer)
- `people.yaml` — Staff directory
- `footer.yaml` — Footer configuration

### Styling

- `assets/css/main.css` — Tailwind CSS with `@layer` directives (base, components, utilities)
- `tailwind.config.js` — Custom brand colors (`red-brand: #C32A26`), IBM Plex font family (Serif, Sans, Mono), max-width 1200px
- Typography plugin (`@tailwindcss/typography`) with customized prose styles

### JavaScript

- Alpine.js for interactive UI (project filtering, staff modals)
- Client-side search with Cmd-K shortcut (Hugo JSON output generates search index)

### CI/CD

GitHub Actions (`.github/workflows/cicd.yml`) builds on pushes to `main` and `preview`:
1. Hugo build with minification
2. Docker image (Nginx + built static files) pushed to ghcr.io
3. Deployed to rrchnm.org

### Hugo Configuration

Key settings in `hugo.yaml`:
- Unsafe HTML rendering enabled in Goldmark
- Blog permalinks: `/blog/:slug/`
- Pagination: 12 items per page
- Taxonomies: categories and tags
- JSON output on homepage for search index

### URL Redirects

Static redirects configured in `static/_redirects`.
