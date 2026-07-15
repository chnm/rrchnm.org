---
title: "Scheduled Post Test: Automatic Publishing and Image Attachment"
authors:
- "RRCHNM Web Team"
date: 2026-07-14
publishDate: 2026-07-16T09:00:00Z
draft: false
slug: scheduled-post-test
categories:
- post
tags:
- test
lede: "A throwaway test post demonstrating scheduled publishing and image attachment. Safe to delete."
featured_image: placeholder.png
_build:
  render: always
  list: never
---

> **This is a test post.** It exists only to demonstrate scheduled publishing
> and image attachment on rrchnm.org, and is safe to delete at any time.

This post was written on **July 14, 2026** but set to publish on **July 16,
2026** through the `publishDate` field in its front matter. Until the site's
weekday build runs on or after that date (scheduled for 11:08 UTC, though
GitHub often runs it later in the morning, U.S. Eastern), Hugo keeps it hidden.
So if you are reading this on the live site, the scheduling mechanism worked.

## How this post is scheduled

The front matter sets three fields that work together:

- `draft: false` — it is not a draft, so it is eligible to publish.
- `date: 2026-07-14` — the authored date readers see on the post.
- `publishDate: 2026-07-16T09:00:00Z` — the moment it becomes visible.

The 9:00 UTC publish time is deliberately before the weekday build at 11:08
UTC, so the very next scheduled run picks it up. See the publishing guide,
section 9, for the full explanation.

This post is also **unlisted**: a `_build` block in the front matter
(`render: always`, `list: never`) keeps it out of the blog index, homepage,
RSS feed, sitemap, and search. It is only reachable at its direct URL
(`/blog/scheduled-post-test/`), so the scheduling mechanism can be verified
on the live site without broadcasting a test post to readers.

## Image attachment demo

The image below lives in this post's own bundle folder
(`content/blog/2026-07-14-scheduled-post-test/placeholder.png`) and is
referenced by bare filename through the `figure` shortcode. The same file is
set as this post's `featured_image`, so it also appears as the banner at the
top of the page.

{{< figure src="placeholder.png" alt="A gray placeholder image with a border and a diagonal cross" caption="A placeholder image attached from this post's own bundle folder." >}}

When you no longer need this demo, delete the whole
`2026-07-14-scheduled-post-test/` folder.
