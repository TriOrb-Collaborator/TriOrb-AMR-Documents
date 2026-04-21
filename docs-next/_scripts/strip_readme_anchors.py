"""Post-process packages/index.html: remove the rosdoc2 "README" anchor
entries that Sphinx inserts under each package in the category toctree
because `:titlesonly:` does not suppress H2 headings brought in via
`.. include ::`.

Idempotent; safe to run repeatedly.
"""
from __future__ import annotations

import sys
from pathlib import Path

from bs4 import BeautifulSoup


def strip(path: Path) -> int:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    removed = 0
    for a in soup.select('a.reference.internal[href*="#readme"]'):
        # Walk up to the enclosing <li class="toctree-l*">.
        li = a.find_parent("li")
        if li is None:
            continue
        li.decompose()
        removed += 1
    path.write_text(str(soup), encoding="utf-8")
    return removed


if __name__ == "__main__":
    for p in sys.argv[1:]:
        n = strip(Path(p))
        print(f"{p}: stripped {n} README anchor entries")
