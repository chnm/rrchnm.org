# rrchnm.org

Public website for the [Roy Rosenzweig Center for History and New Media](https://rrchnm.org) (RRCHNM) at George Mason University.

## Quick Start

**Prerequisites:** [Hugo Extended](https://gohugo.io/installation/) 0.154.5+, Node.js, and [just](https://github.com/casey/just).

```bash
just setup       # install dependencies
just dev         # start dev server
```

The dev server runs at `http://localhost:1313/` with live reload.

## Production Build

```bash
just build       # outputs to public/
```

## Tech Stack

- **[Hugo](https://gohugo.io/)** — static site generator
- **[Tailwind CSS](https://tailwindcss.com/)** — utility-first CSS framework
- **[Alpine.js](https://alpinejs.dev/)** — lightweight interactivity (filtering, modals, search)

## Project Structure

```
content/          Markdown content organized by section (blog, our-work, publications, page)
data/             YAML data files (menus, people, dissertations)
layouts/          Hugo templates
assets/css/       Tailwind CSS entry point
static/           Images, PDFs, and other static assets
scripts/          Utility scripts
```

## Content Authoring

Content is authored as Markdown files with YAML frontmatter, organized in [Hugo page bundles](https://gohugo.io/content-management/page-bundles/). Each content item is a directory with an `index.md` and any associated images.

### Adding a Blog Post

Create a new directory in `content/blog/` following the naming convention `YYYY-MM-DD-slug/index.md`:

```yaml
---
title: Your Post Title
date: '2026-01-15T10:00:00Z'
slug: your-post-slug
author_name: Author Name
authors:
  - Author Name
categories:
  - Post
draft: false
---

Your content here.
```

### Adding a Project

Create a new directory in `content/our-work/` with an `index.md` and any images:

```yaml
---
title: Project Name
categories:
  - Public History
featured_image: thumbnail.jpg
project_url: https://example.org
featured_project: true
---

Project description here.
```

To mark a project as inactive, add a `status` field:

```yaml
status:
  - active: false
```

### Updating Navigation

Edit the `menus:` section in `hugo.yaml` to change navigation links. Do not hardcode nav links in templates.

### Updating Staff

Edit `data/people.yaml` to add, remove, or update staff listings.

## Deployment

Pushes to `main` or `preview` branches trigger GitHub Actions CI/CD, which builds a Docker image and deploys to production.

## Documentation

- **[CLAUDE.md](./CLAUDE.md)** — AI assistant context for Claude Code
- **[AGENTS.md](./AGENTS.md)** — Detailed technical architecture and conventions
- **[SPEC.md](./SPEC.md)** — Feature specifications and business rules

## License

Content is copyright Roy Rosenzweig Center for History and New Media, George Mason University.
