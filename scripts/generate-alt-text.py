#!/usr/bin/env python3
"""Scan Hugo content for images missing alt text and generate suggestions via Claude.

Usage:
    python scripts/generate-alt-text.py                # dry-run: print suggestions
    python scripts/generate-alt-text.py --apply        # patch files in place
    python scripts/generate-alt-text.py --model opus   # use a specific Claude model

Requires: claude CLI (Claude Code) installed and authenticated.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

# Markdown images with empty alt text: ![](path) or ![ ](path)
EMPTY_ALT_RE = re.compile(r'(!\[)\s*(\]\([^)]+\))')

# Hugo figure shortcodes without an alt= attribute
FIGURE_NO_ALT_RE = re.compile(
    r'(\{\{<\s*figure\s+)((?:(?!alt=)[^>])*)(>\s*\}\})'
)

ALT_SUFFIX = " This alt text was written by a generative AI."

PROMPT_TEMPLATE = (
    'Read the image at {image_path} and describe it in one or two concise '
    'sentences for use as alt text on a digital history and humanities website. '
    'Focus on what is visually depicted. Do not start with "This image shows" '
    'or "The image depicts". Just state what you see. '
    'Always finish your sentence — never cut off mid-word or mid-phrase. '
    'Aim for under 200 characters but completeness matters more than brevity. '
    'Output ONLY the alt text, nothing else — no labels, no quotes.'
)


def find_empty_markdown_images(content_dir: Path) -> list[dict]:
    """Find markdown images with empty alt text: ![](path)."""
    results = []
    for md_file in sorted(content_dir.rglob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        for match in EMPTY_ALT_RE.finditer(text):
            full_match = match.group(0)
            img_path = re.search(r'\]\(([^)]+)\)', full_match)
            if img_path:
                results.append({
                    "file": md_file,
                    "match": full_match,
                    "img_ref": img_path.group(1).strip(),
                    "line": text[:match.start()].count("\n") + 1,
                    "type": "markdown",
                })
    return results


def find_figure_shortcodes_missing_alt(content_dir: Path) -> list[dict]:
    """Find Hugo figure shortcodes without alt= attribute."""
    results = []
    for md_file in sorted(content_dir.rglob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        for match in FIGURE_NO_ALT_RE.finditer(text):
            full_match = match.group(0)
            src = re.search(r'src="([^"]+)"', full_match)
            if src:
                results.append({
                    "file": md_file,
                    "match": full_match,
                    "img_ref": src.group(1).strip(),
                    "line": text[:match.start()].count("\n") + 1,
                    "type": "figure",
                })
    return results


def resolve_image_path(md_file: Path, img_ref: str) -> Path | None:
    """Resolve an image reference to an actual file path."""
    if img_ref.startswith("http://") or img_ref.startswith("https://"):
        return None
    # Strip any markdown title syntax e.g. 'image.jpg "title"'
    clean_ref = img_ref.split('"')[0].strip().split("'")[0].strip()
    if clean_ref.startswith("/"):
        candidate = STATIC_DIR / clean_ref.lstrip("/")
    else:
        candidate = md_file.parent / clean_ref
    if candidate.exists():
        return candidate
    return None


def generate_alt_text(image_path: Path, model: str) -> str:
    """Call claude -p to generate alt text for an image."""
    prompt = PROMPT_TEMPLATE.format(image_path=image_path)
    try:
        result = subprocess.run(
            ["claude", "-p", prompt, "--model", model, "--allowedTools", "Read"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            print(f"  ERROR: claude failed for {image_path}: {result.stderr.strip()}", file=sys.stderr)
            return ""
        text = result.stdout.strip()
        # Strip any markdown formatting claude might add
        text = re.sub(r'^\*\*.*?\*\*:?\s*', '', text)
        text = text.strip('"').strip("'").strip()
        # Collapse to single line
        text = " ".join(text.split())
        # Ensure the text ends with a period
        if text and text[-1] not in ".!?":
            text += "."
        return text
    except FileNotFoundError:
        print("ERROR: 'claude' CLI not found. Install Claude Code first.", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print(f"  ERROR: claude timed out for {image_path}", file=sys.stderr)
        return ""


def apply_markdown_alt(md_file: Path, old_match: str, alt_text: str) -> None:
    """Patch a markdown image: ![](path) → ![alt text](path)."""
    text = md_file.read_text(encoding="utf-8")
    new_match = old_match.replace("![", f"![{alt_text}{ALT_SUFFIX}", 1)
    text = text.replace(old_match, new_match, 1)
    md_file.write_text(text, encoding="utf-8")


def apply_figure_alt(md_file: Path, old_match: str, alt_text: str) -> None:
    """Patch a figure shortcode: add alt="..." attribute."""
    text = md_file.read_text(encoding="utf-8")
    escaped = alt_text.replace('"', '\\"')
    full_alt = f'{escaped}{ALT_SUFFIX}'
    # Insert alt= before the closing >}}
    new_match = FIGURE_NO_ALT_RE.sub(
        lambda m: f'{m.group(1)}{m.group(2)}alt="{full_alt}" {m.group(3)}',
        old_match,
    )
    text = text.replace(old_match, new_match, 1)
    md_file.write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Generate alt text for images missing it.")
    parser.add_argument("--apply", action="store_true", help="Patch files in place (default: dry run)")
    parser.add_argument("--model", default="sonnet", help="Claude model to use (default: sonnet)")
    args = parser.parse_args()

    print(f"Scanning {CONTENT_DIR} for images with empty alt text...\n")

    md_entries = find_empty_markdown_images(CONTENT_DIR)
    fig_entries = find_figure_shortcodes_missing_alt(CONTENT_DIR)
    entries = md_entries + fig_entries

    if not entries:
        print("No images with missing alt text found.")
        return

    print(f"Found {len(md_entries)} markdown image(s) and {len(fig_entries)} figure shortcode(s) missing alt text.\n")

    skipped = 0
    processed = 0

    for entry in entries:
        rel_file = entry["file"].relative_to(CONTENT_DIR.parent)
        img_path = resolve_image_path(entry["file"], entry["img_ref"])

        if img_path is None:
            print(f"  SKIP: {rel_file}:{entry['line']} — cannot resolve {entry['img_ref']}")
            skipped += 1
            continue

        print(f"  Processing [{entry['type']}]: {rel_file}:{entry['line']} — {entry['img_ref']}")
        alt_text = generate_alt_text(img_path, args.model)

        if not alt_text:
            skipped += 1
            continue

        print(f"    → {alt_text}{ALT_SUFFIX}")

        if args.apply:
            if entry["type"] == "markdown":
                apply_markdown_alt(entry["file"], entry["match"], alt_text)
            else:
                apply_figure_alt(entry["file"], entry["match"], alt_text)
            print(f"    ✓ Patched")

        processed += 1

    print(f"\nDone. Processed: {processed}, Skipped: {skipped}")
    if not args.apply and processed > 0:
        print("Run with --apply to write changes to files.")


if __name__ == "__main__":
    main()
