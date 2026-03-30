# Contributing to rrchnm.org

This guide covers how to create and edit content on the RRCHNM website. The site is built with [Hugo](https://gohugo.io/), a static site generator. Content is written in Markdown with YAML frontmatter.

## Getting Started

### Prerequisites

- [Hugo Extended](https://gohugo.io/installation/) v0.154.5+
- [Node.js](https://nodejs.org/) (for Tailwind CSS processing)
- [just](https://github.com/casey/just) (task runner)

### Local Development

```bash
just setup        # Install dependencies
just dev          # Start the dev server (http://localhost:1313)
just build        # Production build
```

## Content Sections

The site has several content sections, each with its own directory under `content/`:

| Section | Path | Description |
|---------|------|-------------|
| Blog | `content/blog/` | News, essays, reflections |
| Our Work | `content/our-work/` | Project pages |
| Publications | `content/publications/` | Research publications & essays |
| Spotlight | `content/spotlight/` | Featured highlights for the homepage |
| Video | `content/video/` | Video content |
| Pages | `content/page/` | Static pages (about, contact, policies) |

All content sections except Pages use **page bundles**: each piece of content is a directory containing an `index.md` file and any associated images.

---

## Creating Content

### Blog Posts

Blog posts live in `content/blog/` as page bundles with date-prefixed directory names.

**Create a new post:**

```bash
hugo new blog/my-post-title/index.md
```

This generates a file from the archetype at `archetypes/blog.md`. Edit the frontmatter:

```yaml
---
title: "My Post Title"
date: 2025-06-15T10:00:00Z
draft: true           # Set to false when ready to publish
slug: my-post-title
author_name: "Your Name"
authors:
  - "Your Name"
categories:
  - News              # Options: News, Essay, Research + Tools,
                      # Teaching + Learning, Events
---
```

**Optional frontmatter fields:**

| Field | Description |
|-------|-------------|
| `featured_image` | Filename of a hero image in the same directory (e.g., `hero.jpg`) |
| `lede` | A one-sentence summary displayed in the hero area |
| `tags` | Additional tags for the post |
| `crossposted` | List of sites where this post also appears (see below) |

**Adding images:** Drop image files directly into the post's directory alongside `index.md`. Reference them in the post body with the figure shortcode:

```markdown
{{</* figure src="my-image.jpg" alt="Description" caption="Caption text" */>}}
```

**Crossposting:** If a post also appears on another site, add:

```yaml
crossposted:
  - url: "https://other-site.org/the-post"
    name: "Other Site"
```

This displays a notice above the post content linking to the other version.

### Projects (Our Work)

Project pages live in `content/our-work/` as page bundles.

**Create a new project:**

```bash
hugo new our-work/project-name/index.md
```

**Required frontmatter:**

```yaml
---
title: "Project Name"
date: 2025-06-15T10:00:00Z
draft: true
slug: project-name
categories:
  - "Education"       # Options: Education, Data Driven History,
                      # Public History, Podcasts, Research + Tools,
                      # Teaching + Learning
featured_image: "thumbnail.jpg"
---
```

**Optional frontmatter fields:**

| Field | Description |
|-------|-------------|
| `featured_project` | Set to `true` to display on the homepage |
| `project_url` | External link to the live project |
| `funders` | List of funding organizations |
| `gallery` | List of screenshot filenames for the gallery |
| `short_description` | Brief text for project cards on the listing page |
| `intro_text` | Longer introductory text shown on the project page |
| `affiliates` | List of people with `name` and `role` fields |
| `status` | Set `active: false` and `years_active` for archived projects |

**Images:** Place the featured image and any gallery images in the project directory. Use just the filename in frontmatter:

```yaml
featured_image: "thumbnail.jpg"
gallery:
  - "screenshot-1.jpg"
  - "screenshot-2.jpg"
```

### Publications

Publication pages live in `content/publications/` as page bundles.

**Create a new publication:**

```bash
hugo new publications/publication-slug/index.md
```

**Required frontmatter:**

```yaml
---
title: "Publication Title"
date: 2025-06-15T10:00:00Z
draft: true
slug: publication-slug
essay_author: "Author Name"
authors:
  - "Author Name"
pub_date: "2025"
---
```

**Optional frontmatter fields:**

| Field | Description |
|-------|-------------|
| `essay_date` | Formatted publication date (e.g., "January 2025") |
| `essay_publication_info` | Venue/journal info (supports HTML like `<em>`) |
| `publisher` | Publisher name |
| `isbn` | ISBN number |
| `doi` | DOI identifier |
| `thumbnail` | Cover image filename |
| `external_url` | Link to the publication elsewhere (skips the full-text layout) |
| `abstract` | Brief description |

For publications hosted elsewhere, set `external_url` and optionally `abstract`. For full-text publications hosted on our site, write the content in the body of the Markdown file.

### Spotlight

Spotlights are featured items that appear on the homepage.

```bash
hugo new spotlight/item-name.md
```

```yaml
---
title: "Spotlight Title"
date: 2025-06-15
featured: true
author: "Author Name"
lede: "Short description for the homepage."
link_text: "Learn more"
---
```

### Video

```bash
hugo new video/video-name.md
```

```yaml
---
title: "Video Title"
date: 2025-06-15
draft: true
video_url: "https://youtu.be/VIDEO_ID"
lede: "Short description."
---
```

---

## Shortcodes

Hugo shortcodes let you embed rich content in Markdown. Use them with the `{{</* shortcode */>}}` syntax.

### figure

Embed an image with optional alt text and caption:

```markdown
{{</* figure src="photo.jpg" alt="Description" caption="Caption text" */>}}
```

### button

Render a styled call-to-action button:

```markdown
{{</* button href="https://example.com" text="Click Here" */>}}
```

For internal links (no external icon, no new tab):

```markdown
{{</* button href="/our-work/" text="See Our Work" external="false" */>}}
```

### youtube

Embed a YouTube video:

```markdown
{{</* youtube VIDEO_ID */>}}
```

---

## Images

### Where to put images

Always place images in the same directory as the content's `index.md` file. This is Hugo's "page bundle" pattern and keeps content self-contained.

```
content/blog/2025-06-15-my-post/
├── index.md
├── hero.jpg
└── chart.png
```

Reference images by filename only in both frontmatter and body content.

### Image guidelines

- Use descriptive filenames (e.g., `team-photo-2025.jpg` not `IMG_4521.jpg`)
- Optimize images before adding them — aim for under 500KB per image
- Provide meaningful alt text for accessibility
- Preferred formats: `.jpg` for photos, `.png` for screenshots/graphics, `.webp` where possible

---

## Staff Directory

Staff information is managed in `data/people.yaml`, not in content files. Each person entry looks like:

```yaml
- name: "First Last"
  title: "Job Title"
  headshot: "/media/headshots/first-last.jpg"
  group: "staff"         # staff, student, affiliate
  active: true
```

---

## Navigation

Site navigation is configured in `data/menus.yaml`. Changes to navigation structure should be coordinated with the development team.

---

## Publishing Workflow

1. Create content with `draft: true`
2. Preview locally with `just dev`
3. When ready, set `draft: false`
4. Commit and push to the appropriate branch
5. The CI/CD pipeline builds and deploys automatically on pushes to `main`

For the `preview` branch, the site deploys to a staging environment for review before merging to `main`.
