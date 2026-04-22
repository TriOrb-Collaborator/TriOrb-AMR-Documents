"""Convert submodule `API.md` files into README drafts for each package.

For every leaf package under `submodules/TriOrb-AMR-Package/pkgs/` that (a) is
not excluded by the `EXCLUDE_PREFIXES` rule mirrored here and (b) ships an
`API.md`, emit a draft at:

    docs-next/_drafts/readme_templates/<pkg>/README.md

Layout:

    # <package name>
    <package.xml description as prose>
    > version / maintainer / license

    <<< API.md content, re-leveled so its H1 becomes H2 >>>

    ## Overview (TODO)
    ## Related Packages (TODO)

The draft is meant to be hand-polished and copied into the submodule's
actual `README.md`. Idempotent: re-running overwrites.
"""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SUBMODULE = REPO / "submodules" / "TriOrb-AMR-Package"
DRAFTS = REPO / "docs-next" / "_drafts" / "readme_templates"
PKG_INDEX = REPO / "docs-next" / "packages" / "index.md"


def published_packages() -> set[str]:
    """Leaf package names referenced from docs-next/packages/index.md."""
    if not PKG_INDEX.exists():
        return set()
    text = PKG_INDEX.read_text(encoding="utf-8")
    names: set[str] = set()
    for m in re.finditer(r"^([A-Za-z][A-Za-z0-9_\-]+)/index\s*$", text, re.MULTILINE):
        names.add(m.group(1))
    return names

# Keep in sync with docker/run_rosdoc2.sh EXCLUDE_PREFIXES.
EXCLUDE_PREFIXES = (
    "pkgs/triorb_navi_bridge",
    "pkgs/triorb_navigation_pkgs/",
    "pkgs/triorb_fleet/",
    "pkgs/triorb_service/",
    "pkgs/rosbridge_suite/",
    "pkgs-collab/",
    "pkgs/stella_vslam_ros/",
    "pkgs/triorb_drive/path_planning_server",
    "pkgs/triorb_drive/triorb_path_search_server",
    "pkgs/triorb_drive/triorb_region_map",
    "pkgs/triorb_sensor/triorb_calibration",
    "pkgs/triorb_sensor/triorb_camera_calibration",
    "pkgs/triorb_sensor/triorb_can",
    "pkgs/triorb_sensor/triorb_sls_drive_manager",
    "pkgs/TriOrb-ROS2-Types/triorb_collaboration_interface",
    "pkgs/TriOrb-ROS2-Types/triorb_cv_interface",
    "pkgs/TriOrb-ROS2-Types/triorb_field_interface",
    "pkgs/TriOrb-ROS2-Types/triorb_project_interface",
)


def is_excluded(pkg_rel: str) -> bool:
    return any(pkg_rel.startswith(p) for p in EXCLUDE_PREFIXES)


def package_meta(pkg_dir: Path) -> dict:
    """Return {name, version, description, maintainer, license} from package.xml."""
    px = pkg_dir / "package.xml"
    if not px.exists():
        return {"name": pkg_dir.name}
    try:
        root = ET.parse(px).getroot()
    except ET.ParseError:
        return {"name": pkg_dir.name}
    def _text(tag):
        el = root.find(tag)
        return (el.text or "").strip() if el is not None else ""
    maintainer_el = root.find("maintainer")
    maintainer = ""
    if maintainer_el is not None:
        name = (maintainer_el.text or "").strip()
        email = maintainer_el.attrib.get("email", "")
        maintainer = f"{name} <{email}>" if email else name
    return {
        "name": _text("name") or pkg_dir.name,
        "version": _text("version"),
        "description": _text("description"),
        "maintainer": maintainer,
        "license": _text("license"),
    }


def shift_headings(md_text: str, shift: int = 1) -> str:
    """Demote headings by `shift` levels (H1 -> H2 etc.). Capped at H6."""
    def _sub(m):
        hashes = m.group(1)
        new_level = min(6, len(hashes) + shift)
        return "#" * new_level + m.group(2)
    return re.sub(r"^(#{1,6})(\s)", _sub, md_text, flags=re.MULTILINE)


def convert(api_md: Path, pkg_dir: Path, out_path: Path) -> None:
    meta = package_meta(pkg_dir)
    api_src = api_md.read_text(encoding="utf-8").strip()
    # Drop the first-line top-level title if it repeats the package name —
    # we already render a package-name H1 at the top of the README.
    first_h1 = re.match(r"^#\s+(.+?)\s*$", api_src.split("\n", 1)[0] or "")
    if first_h1 and first_h1.group(1).strip() == meta["name"]:
        api_src = api_src.split("\n", 1)[1].lstrip() if "\n" in api_src else ""
    api_demoted = shift_headings(api_src, shift=1)

    parts = [
        f"# {meta['name']}",
        "",
    ]
    if meta.get("description"):
        parts += [meta["description"].strip(), ""]
    meta_line = []
    if meta.get("version"):
        meta_line.append(f"version: `{meta['version']}`")
    if meta.get("maintainer"):
        meta_line.append(f"maintainer: {meta['maintainer']}")
    if meta.get("license"):
        meta_line.append(f"license: {meta['license']}")
    if meta_line:
        parts += ["> " + " / ".join(meta_line), ""]

    parts += [
        "## Overview",
        "",
        "TODO: このパッケージが提供する機能、起動タイミング、関連ノードとの連携を 2–4 文で。",
        "",
        "## API Reference",
        "",
        "> Source: migrated from the hand-written `API.md` in the submodule.",
        "",
        api_demoted,
        "",
        "## Related Packages",
        "",
        "TODO: 上流・下流の関連パッケージを列挙。",
        "",
    ]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    published = published_packages()
    if not published:
        print("warning: no packages discovered in docs-next/packages/index.md", file=sys.stderr)
    written = 0
    skipped_excluded = 0
    skipped_unpublished = 0
    missing: list[str] = []

    for api_md in sorted((SUBMODULE / "pkgs").rglob("API.md")):
        pkg_dir = api_md.parent
        if not (pkg_dir / "package.xml").exists():
            continue  # not a leaf ROS 2 package
        pkg_rel = pkg_dir.relative_to(SUBMODULE).as_posix()
        if is_excluded(pkg_rel):
            skipped_excluded += 1
            continue
        if pkg_dir.name not in published:
            skipped_unpublished += 1
            continue
        out_path = DRAFTS / pkg_dir.name / "README.md"
        convert(api_md, pkg_dir, out_path)
        print(f"wrote {out_path.relative_to(REPO)}")
        written += 1

    # Highlight published packages WITHOUT API.md so the author knows
    # where to write the next hand-written API doc.
    api_covered = {p.parent.name for p in (SUBMODULE / "pkgs").rglob("API.md")}
    for name in sorted(published):
        if name not in api_covered:
            missing.append(name)

    print(f"\nTotals: {written} drafts written, "
          f"{skipped_excluded} excluded, "
          f"{skipped_unpublished} unpublished.")
    if missing:
        print(f"\nPublished packages without submodule API.md ({len(missing)}):")
        for name in missing:
            print(f"  - {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
