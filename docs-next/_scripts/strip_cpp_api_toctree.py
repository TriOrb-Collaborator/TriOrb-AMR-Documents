"""Post-process packages/*/index.html after we rm -rf the generated/ tree.

Removes toctree entries that point at generated/* so the package index
page doesn't show dead "C++ API" / "Class Hierarchy" / "File Hierarchy"
links.

Idempotent; safe to run repeatedly.
"""
from __future__ import annotations

import sys
from pathlib import Path

from bs4 import BeautifulSoup


def strip(path: Path) -> int:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    removed = 0
    for a in soup.select('a.reference.internal[href*="generated/"]'):
        li = a.find_parent("li")
        if li is None:
            continue
        li.decompose()
        removed += 1
    # Also remove any <section id="cpp-api"> or empty toctrees left over.
    for sec in soup.select('section[id="cpp-api"], section[id*="class-view"], section[id*="file-view"]'):
        sec.decompose()
        removed += 1
    path.write_text(str(soup), encoding="utf-8")
    return removed


if __name__ == "__main__":
    for p in sys.argv[1:]:
        n = strip(Path(p))
        if n:
            print(f"{p}: stripped {n} C++ API entries")
