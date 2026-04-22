"""Strip stale sidebar entries from rendered HTML pages.

Sphinx's incremental builder does not always re-render every page when the
global TOC changes (the source didn't change, so the page is skipped even
though its sidebar is stale). Rather than force a full rebuild, we post-
process every HTML under the deploy tree to remove:

  1. README anchor entries — `<a href="…index.html#readme">README</a>`
     produced by the `__readme_include.rst` title.
  2. Python API entries — `<a href="…/modules.html">Python API</a>`.
  3. Standard Documents entries — `<a href="…/standards.html">Standard
     Documents</a>`.

Only the wrapping `<li class="toctree-l*">` is removed, which drops the
label and its children in one pass.

Idempotent; safe to re-run. BeautifulSoup parser.
"""
from __future__ import annotations

import sys
from pathlib import Path

from bs4 import BeautifulSoup


def strip_html(path: Path) -> int:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    removed = 0
    renamed = 0

    # Normalize stale visual_slam sidebar labels that linger after incremental
    # rebuilds — the canonical labels are set by the page H1s:
    #   packages/visual_slam/index.html  → "triorb_visual_slam"
    #   packages/visual_slam/API.html    → "API"
    for a in soup.select("a.reference.internal[href]"):
        if a.parent is None:
            continue
        href = a.get("href", "") or ""
        if href.endswith("visual_slam/index.html") or href.endswith("visual_slam/"):
            if a.get_text(strip=True) != "triorb_visual_slam":
                a.string = "triorb_visual_slam"
                renamed += 1
        elif href.endswith("visual_slam/API.html"):
            if a.get_text(strip=True) != "API":
                a.string = "API"
                renamed += 1

    # 1. README anchors: href contains `#readme` and text equals "README".
    for a in soup.select('a.reference.internal[href*="#readme"]'):
        if a.get_text(strip=True) != "README":
            continue
        li = a.find_parent("li")
        if li is None:
            continue
        li.decompose()
        removed += 1

    # 2 + 3. Python API / Standard Documents links.
    targets = {
        "modules.html": "Python API",
        "standards.html": "Standard Documents",
    }
    for a in list(soup.select("a.reference.internal[href]")):
        if a.parent is None:
            continue  # already removed upstream
        href = a.get("href", "") or ""
        for suffix, label in targets.items():
            if href.endswith(suffix) and a.get_text(strip=True) == label:
                li = a.find_parent("li")
                if li is not None:
                    li.decompose()
                    removed += 1
                break

    if removed or renamed:
        path.write_text(str(soup), encoding="utf-8")
    return removed + renamed


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: strip_sidebar_noise.py <html_root> [...]", file=sys.stderr)
        return 2
    grand_total = 0
    file_count = 0
    for root in argv:
        for html in Path(root).rglob("*.html"):
            n = strip_html(html)
            if n:
                grand_total += n
                file_count += 1
    print(f"strip_sidebar_noise: touched {file_count} HTML files, removed {grand_total} <li> nodes")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
