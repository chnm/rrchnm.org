#!/usr/bin/env python3
"""Set specific 2020+ blog posts to category: Essay."""

import os
import re
import yaml

BLOG_DIR = os.path.join(os.path.dirname(__file__), "..", "content", "blog")

ESSAY_SLUGS = {
    "2025-12-04-lost-in-the-park-roy-rosenzweigs-public-history-legacy",
    "2025-02-10-celebrating-black-history-month",
    "2025-03-06-celebrating-womens-history-month",
    "2021-09-10-remembering-the-creation-of-the-september-11-digital-archive",
    "2025-02-13-teaching-writing-and-research-with-ai",
    "2022-11-08-how-philip-lampi-recovered-the-lost-history-of-early-american-elections",
    "2025-05-13-report-from-the-seventh-conference-on-digital-humanities-and-digital-history",
    "2021-08-06-transcribing-structured-data-with-the-datascribe-module-for-omeka-s",
    "2023-08-15-rrchnm-past-present-and-future",
    "2021-02-18-documenting-sharing-and-learning-from-jewish-life-during-the-pandemic",
    "2022-04-06-rrchnms-custom-api-for-data-driven-projects",
    "2025-08-25-graduate-student-reflections-sustainability-summer",
    "2025-04-11-carrying-on-when-the-grants-go-away",
    "2023-01-25-remembering-paula-petrik",
    "2024-05-08-graduate-student-reflections-brandan-p-buck",
    "2021-09-07-models-of-argument-driven-digital-history",
    "2020-10-21-from-historical-sources-to-datasets-a-preview-of-datascribe",
    "2025-01-27-graduate-student-reflections-how-network-analysis-influenced-my-research",
    "2024-06-20-graduate-student-reflections-teaching-dh",
    "2025-02-07-graduate-student-reflections-aha-presentations",
    "2024-02-20-the-end-of-our-hike",
    "2023-10-18-exploring-true-crime-in-early-modern-europe-in-the-classroom",
    "2023-11-01-talking-to-the-dead-spiritualists-and-seances",
    "2020-10-28-new-publication-model-editor-for-current-research-in-digital-history",
}


def main():
    blog_dir = os.path.abspath(BLOG_DIR)
    updated = 0

    for slug in sorted(ESSAY_SLUGS):
        index_path = os.path.join(blog_dir, slug, "index.md")
        if not os.path.exists(index_path):
            print(f"  NOT FOUND: {slug}")
            continue

        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()

        match = re.match(r'^---\n(.*?\n)---\n(.*)', content, re.DOTALL)
        if not match:
            continue

        fm_str = match.group(1)
        body = match.group(2)

        try:
            fm = yaml.safe_load(fm_str)
        except yaml.YAMLError:
            continue

        if fm.get("categories") == ["Essay"]:
            continue

        fm["categories"] = ["Essay"]
        new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False)
        new_content = f"---\n{new_fm}---\n{body}"

        with open(index_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        title = fm.get("title", slug)
        print(f"  Essay: {title}")
        updated += 1

    print(f"\nDone. Updated {updated} posts to Essay.")


if __name__ == "__main__":
    main()
