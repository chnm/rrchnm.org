# AGENTS.md

> For feature specifications, business rules, and domain models, see [SPEC.md](./SPEC.md).

---

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Project Initialization](#project-initialization)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Development Workflow](#development-workflow)
- [Best Practices & Key Conventions](#best-practices--key-conventions)
- [Notes for AI Agents](#notes-for-ai-agents)

---

## Project Overview

Public website for the Roy Rosenzweig Center for History and New Media (RRCHNM) at George Mason University. A Hugo static site styled with Tailwind CSS. The site showcases the center's projects, publications, blog, people, and graduate education programs.

---

## Tech Stack

### Task Runner

- **[just](https://github.com/casey/just)** for local development commands (see `justfile`)
- **npm** for Node.js dependencies (PostCSS/Tailwind build pipeline)
- Key commands:
  - `just setup` → `npm ci` (install dependencies)
  - `just dev` → `hugo server --buildDrafts --navigateToChanged` (local dev with live reload)
  - `just build` → `hugo --minify` (production build)

### Frontend

- **Hugo 0.154.5 Extended** — static site generator (Extended version required for CSS processing)
- **Tailwind CSS 3.4** — utility-first CSS framework
- **PostCSS** with autoprefixer
- **Alpine.js** — lightweight JS for interactive components (project filtering, staff modals)
- **@tailwindcss/typography** — prose styling plugin
- No build bundler (Vite, Webpack, etc.) — Hugo's asset pipeline handles everything

### Database

None. All content is Markdown files with YAML frontmatter. Data-driven content uses YAML files in `data/`.

---

## Project Initialization

**Prerequisites:**
- Hugo Extended 0.154.5+ ([install guide](https://gohugo.io/installation/))
- Node.js and npm

**Setup:**
```bash
git clone <repo-url>
cd rrchnm.org
just setup
just dev
```

The dev server runs at `http://localhost:1313/` with live reload.

---

## Project Structure

```
rrchnm.org/
├── assets/
│   ├── css/main.css          # Tailwind entry point (@layer base/components/utilities)
│   └── js/                   # JavaScript modules
├── content/
│   ├── blog/                 # Blog posts (Markdown + YAML frontmatter)
│   ├── our-work/             # Project pages (served at /projects/)
│   ├── publications/         # Publication entries
│   ├── spotlight/            # Featured spotlight content
│   └── page/                 # Static pages (about, contact, etc.)
├── data/
│   ├── menus.yaml            # Navigation menus (top_nav, mobile_nav, footer)
│   ├── people.yaml           # Staff directory
│   ├── dissertations.yaml    # Digital dissertations for grad education page
│   └── footer.yaml           # Footer configuration
├── layouts/
│   ├── _default/             # Base templates (baseof, list, single)
│   ├── blog/                 # Blog templates
│   ├── our-work/             # Project templates (list separates active/inactive)
│   ├── publications/         # Publication templates
│   ├── spotlight/            # Spotlight templates
│   ├── page/                 # Custom page templates (our-story, our-people, graduate-student-education, etc.)
│   ├── partials/             # Reusable template fragments
│   ├── shortcodes/           # Custom Hugo shortcodes
│   ├── tags/                 # Tag taxonomy templates
│   └── index.html            # Homepage
├── static/
│   ├── media/                # Shared content images and documents
│   │   ├── reports/          # Annual report PDFs
│   │   └── grad/             # Graduate education images
│   ├── img/                  # Site assets (logos, favicon, default images)
│   └── _redirects            # URL redirect rules
├── scripts/                  # Python utilities (project crawling, frontmatter cleanup)
├── hugo.yaml                 # Hugo site configuration
├── tailwind.config.js        # Tailwind theme (colors, fonts, typography)
├── postcss.config.js         # PostCSS plugins (tailwindcss, autoprefixer)
├── Dockerfile                # Multi-stage: Hugo build → Nginx serving
└── package.json              # Node.js dependencies and scripts
```

---

## Architecture

### System Architecture Diagram

```mermaid
graph TD
    A[Content Authors] -->|Git push| B[Markdown + YAML files]
    B --> C[Hugo Build]
    D[Tailwind CSS + PostCSS] --> C
    C -->|hugo --minify| E[Static HTML/CSS/JS in public/]
    E --> F[Docker: Nginx Alpine]
    F --> G[rrchnm.org]
```

### Build Pipeline

1. Content is authored as Markdown files with YAML frontmatter in `content/`
2. Data files in `data/` provide structured content (menus, people, dissertations)
3. Hugo templates in `layouts/` render content into HTML
4. Tailwind CSS is processed via PostCSS during Hugo's asset pipeline
5. `hugo --minify` produces optimized static files in `public/`
6. Docker packages the output into an Nginx container
7. GitHub Actions CI/CD builds and deploys on push to `main` or `preview`

### Template Hierarchy

Hugo resolves templates by section and type:
- `/blog/post-slug/` → `layouts/blog/single.html`
- `/blog/` → `layouts/blog/list.html`
- `/projects/` → `layouts/our-work/list.html` (section is `our-work`, URL overridden to `/projects/`)
- `/projects/project-slug/` → `layouts/our-work/single.html`
- `/people/` → `layouts/page/our-people.html`
- `/our-story/` → `layouts/page/our-story.html`
- `/graduate-student-education/` → `layouts/page/graduate-student-education.html`
- Homepage → `layouts/index.html`
- Fallback → `layouts/_default/single.html` or `list.html`

### Key Interactive Components

- **Project filtering** (`layouts/our-work/list.html`): Alpine.js-driven category filter buttons that show/hide project cards client-side; projects split into active and "Past Projects" sections
- **Staff modal** (`layouts/page/our-people.html`): HTML `<dialog>` element with Alpine.js for staff profile popups
- **Site search**: Cmd-K / Ctrl-K shortcut opens search modal; uses Hugo's JSON output as a client-side search index

### Image Resolution

The `layouts/partials/featured-image.html` partial handles image paths:
- Paths starting with `/` or `http` → used as-is (static or external)
- Bare filenames → resolved as Hugo page resources (bundle images)
- Falls back to `site.Params.default_image`

Gallery arrays in project frontmatter may mix both patterns; the gallery template in `our-work/single.html` uses the same resolution logic.

---

## Development Workflow

### Version Control

- **Main branch:** `main` (production deployments)
- **Preview branch:** `preview` (staging deployments)
- CI/CD triggers on pushes to `main` and `preview`

### Serving the Application

**Development:**
```bash
just dev             # Hugo server at localhost:1313 with live reload
```

**Production build:**
```bash
just build           # hugo --minify → outputs to public/
```

**Docker build:**
```bash
docker build -t rrchnm-website .
```
The Dockerfile runs a multi-stage build: Hugo Extended on Alpine builds the site, then copies `public/` to Nginx Alpine. A symlink `/img → /assets/img` maintains backward compatibility for old image paths.

### CI/CD

GitHub Actions workflow (`.github/workflows/cicd.yml`):
- Uses reusable workflows from the `chnm/.github` org repository
- Builds Hugo site, creates Docker image, pushes to `ghcr.io`
- Deploys to `hugo.rrchnm.org`
- Release tags use ISO date format (YYYY-MM-DD)

---

## Best Practices & Key Conventions

### Styling
- Use Tailwind utility classes in templates; avoid inline styles
- Custom component styles go in `assets/css/main.css` under `@layer components`
- Brand colors: `red-brand` (#C32A26), `red-dark` (#9E2220)
- Fonts: IBM Plex Serif (headings), IBM Plex Sans (body), IBM Plex Mono (code)
- Max content width: `max-w-site` (1200px)
- All containers (header, main, footer) use `mx-auto max-w-site px-6 lg:px-10` for consistent alignment
- Use the `.label` class for metadata labels (dates, categories, taglines)
- Use `.prose` class (from Typography plugin) for long-form Markdown content

### Templates
- Shared UI goes in `layouts/partials/`
- Custom page layouts go in `layouts/page/` and are matched by `layout` field in frontmatter or by filename to `content/page/` slugs
- Use `[x-cloak]` attribute on Alpine.js elements to prevent flash of unstyled content
- Two-column layouts use `lg:w-2/3` + `lg:w-1/3` flex pattern (see blog single, our-story, graduate education)

### Content
- Blog frontmatter: `title`, `date`, `slug`, `author_name`, `authors`, `categories`, `draft`, `lede` (optional custom summary; falls back to Hugo `.Summary`)
- Blog categories: `Post`, `News` (News category hides author display)
- Project frontmatter: `title`, `categories`, `featured_image`, `project_url`, `funders`, `gallery`, `featured_project`, `status`
- Publication frontmatter: `title`, `pub_date`, `essay_author`, `essay_date`, `essay_publication_info`
- Set `draft: true` to exclude content from production builds
- Prefer page bundle images (co-located with content) over `static/media/` for content-specific images
- Organize `static/media/` by topic (`reports/`, `grad/`), not by date

### Accessibility
- WCAG 2.1 AA target
- Focus-visible indicators use `outline-red-brand` with `outline-offset-2`
- All decorative images use empty `alt=""` and `aria-hidden="true"`
- Interactive elements use `aria-label` where visible text is insufficient

---

## Notes for AI Agents

### Important Context
- Goldmark renderer has `unsafe: true` enabled, so raw HTML in Markdown is intentional and expected
- Homepage has Lorem ipsum placeholder text that will be replaced with final editorial copy
- The `static/_redirects` file handles URL redirects including `/our-work/` → `/projects/`
- Docker build creates a symlink `/img → /assets/img` for backward compatibility with old WordPress image paths
- The content section directory is `content/our-work/` but it is served at `/projects/` via `url:` override in `_index.md`
- Social icons in `layouts/partials/social-icons.html` only render when a URL is configured

### When Making Changes
- Run `just dev` to verify changes render correctly
- Hugo templates use Go template syntax (`{{ }}`) — not Jinja, Handlebars, etc.
- Tailwind classes are purged based on `content` paths in `tailwind.config.js` — if adding templates in new directories, update the content array
- The `data/menus.yaml` file drives all navigation — don't hardcode nav links in templates
- Staff data lives in `data/people.yaml`, not in content files
- Digital dissertations live in `data/dissertations.yaml`
- When adding images for a specific content page, prefer adding to the page bundle over `static/`

### What to Avoid
- Don't add JavaScript frameworks beyond Alpine.js — keep the JS footprint minimal
- Don't use Hugo's built-in menu system — the site uses `data/menus.yaml` instead
- Don't put styles outside of Tailwind utilities or `@layer` directives in `main.css` (exception: JS-generated DOM that Tailwind can't purge, like search results)
- Don't change `hugo.yaml` `baseURL` for local development — Hugo server handles this automatically
- Don't use date-based paths for new static media — use semantic folder names (e.g., `static/media/reports/`)

---
*Last Updated: 2026-03-30*
*This document is maintained for AI agent context and onboarding.*
