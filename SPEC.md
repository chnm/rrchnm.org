# SPEC.md

> For technical implementation details, architecture, and developer documentation, see [AGENTS.md](./AGENTS.md).

---

## Table of Contents

- [Overview](#overview)
- [Users & Roles](#users--roles)
- [Business Rules](#business-rules)
- [Features](#features)
- [User Flows](#user-flows)
  - [Flow 1: Browsing Projects](#flow-1-browsing-projects)
  - [Flow 2: Reading a Blog Post](#flow-2-reading-a-blog-post)
- [Out of Scope](#out-of-scope)
- [Open Questions](#open-questions)

---

## Overview

The RRCHNM website (rrchnm.org) is the public-facing site for the Roy Rosenzweig Center for History and New Media at George Mason University. It serves as the primary web presence for the center, showcasing its mission of using digital media and technology to democratize history.

**Core value proposition:** Communicate RRCHNM's work, people, and impact to researchers, funders, students, and the public.

**Primary goals:**
- Showcase active and past digital history projects
- Publish blog posts and news about the center's work
- Present the center's research publications
- Provide information about staff, graduate education, and the center's story
- Drive newsletter signups and donations

**Target audience:** Digital historians, academic researchers, potential funders, graduate students, and the general public interested in digital humanities.

---

## Users & Roles

This is a public, read-only website with no user accounts or authentication. All visitors see the same content.

### Site Visitor
- Can browse all pages, projects, publications, and blog posts
- Can filter projects by category
- Can search site content via Cmd-K / Ctrl-K
- Can navigate via top nav, mobile nav, footer, and breadcrumbs
- Can click through to external project URLs, donation page, and newsletter signup

### Content Editor (out-of-band)
- Adds/edits content by authoring Markdown files with YAML frontmatter
- Updates data files (menus, people directory) in `data/`
- Changes are deployed via Git push to `main` or `preview` branches

---

## Business Rules

### Content Publishing
- Blog posts with `draft: true` are excluded from production builds
- Blog posts require: `title`, `date`, `slug`, and `author_name`
- Projects with `featured_project: true` appear on the homepage (up to 9)
- Projects require: `title`, `categories`; optional: `featured_image`, `project_url`, `funders`, `gallery`
- Publications require: `title`, `pub_date`; optional: `essay_author`, `essay_date`, `essay_publication_info`

### Navigation
- Navigation menus are defined in `data/menus.yaml` (top_nav, mobile_nav, footer)
- Primary sections: People, Projects, Publications, Blog, Graduate Education

### Display Rules
- Pagination: 12 items per page across all list views
- Related posts shown on blog singles, weighted by tags (100), categories (10), date (5)
- Homepage "The Latest" shows the 2 most recent blog posts
- Homepage "Our Work" shows up to 9 featured projects
- Homepage spotlight section is controlled via `content/_index.md` frontmatter (`spotlight_title`, `spotlight_body`, `spotlight_link_url`, `spotlight_link_text`)

### URL Structure
- Blog: `/blog/:slug/`
- Projects: `/projects/:slug/`
- Publications: `/publications/:slug/`
- Pages: `/:slug/` (defined by file path in `content/page/`)

---

## Features

### Feature: Project Showcase

**Description:** Filterable gallery of RRCHNM's digital history projects.

**Functionality:**
- Grid display of project cards with featured images
- Client-side category filtering via Alpine.js on `/our-work/`
- Individual project pages with description, external URL, funders, and image gallery
- Featured projects surfaced on homepage

### Feature: Blog

**Description:** News and updates from the center, dating back to 2002.

**Functionality:**
- Paginated list view with featured images and author names
- Single post view with prose-styled content
- Related posts based on shared tags/categories
- Tag and category taxonomy pages

### Feature: Publications

**Description:** Research publications produced by center staff.

**Functionality:**
- List view sorted by publication date
- Single page with author, publication info, and full text or link

### Feature: Site Search

**Description:** Client-side search accessible via Cmd-K / Ctrl-K keyboard shortcut.

**Functionality:**
- Hugo generates a JSON search index at build time (home page JSON output)
- JavaScript-driven search modal with real-time results
- Results display title, section, and metadata

### Feature: People Directory

**Description:** Staff and affiliate listing on `/people/`.

**Functionality:**
- Staff cards rendered from `data/people.yaml`
- Modal dialog (`#staff-modal`) for viewing individual staff details
- Organized by affiliation/role

### Feature: Newsletter & Donation CTAs

**Description:** Calls to action for newsletter subscription and donations.

**Functionality:**
- Newsletter links to external Airtable form (configured in `hugo.yaml` `params.newsletter_url`)
- Donate links to GMU's secure giving page (configured in `hugo.yaml` `params.donate_url`)
- CTAs appear in homepage hero sidebar and bottom CTA section

---

## User Flows

### Flow 1: Browsing Projects

**Goal:** Visitor discovers and explores RRCHNM's digital history projects.

**Steps:**
1. Visitor lands on homepage, sees up to 9 featured projects in "Our Work" grid
2. Clicks "View all" → navigates to `/our-work/`
3. On project listing, uses category filter buttons (Alpine.js) to narrow results
4. Clicks a project card → navigates to project detail page
5. Reads project description, views image gallery, clicks external project URL to visit the live project

### Flow 2: Reading a Blog Post

**Goal:** Visitor reads center news and discovers related content.

**Steps:**
1. Visitor sees "The Latest" in homepage sidebar with 2 recent posts
2. Clicks a post title → navigates to blog single page
3. Reads post content (prose-styled Markdown)
4. Sees related posts at bottom based on shared tags/categories
5. Optionally browses tag/category taxonomy pages for more posts

---

## Out of Scope

### Not Applicable (Static Site)
- User accounts, authentication, or authorization
- Server-side search or database queries
- Comments or user-generated content
- E-commerce or payment processing (donations link to external GMU page)
- CMS admin interface (content managed via Git)

### Future Considerations
- The site is currently undergoing a Tailwind CSS redesign (`tailwind-redesign` branch)
- Some homepage placeholder text (Lorem ipsum) needs to be replaced with final copy

---

## Open Questions

- **Q:** What should replace the Lorem ipsum placeholder text on the homepage hero?
  - **Context:** Two paragraphs of placeholder text exist in `layouts/index.html`
  - **Owner:** Content/editorial team
  - **Status:** Open

---
*Last Updated: 2026-03-26*
*This document is maintained for AI agent context and onboarding.*
