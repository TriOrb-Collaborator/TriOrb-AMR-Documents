#!/usr/bin/env bash
# Run rosdoc2 on one or more TriOrb-AMR-Package ROS 2 packages and materialize
# the generated RST + Doxygen XML under docs-next/packages/<pkg>/ so the
# umbrella Sphinx build can consume them.
#
# Usage:
#   bash docs-next/docker/run_rosdoc2.sh                           # default set
#   bash docs-next/docker/run_rosdoc2.sh pkgs/.../triorb_sick_plc_wrapper
#   bash docs-next/docker/run_rosdoc2.sh pkgs/.../pkg_a pkgs/.../pkg_b
#
# Outputs (host paths):
#   docs-next/packages/<pkg_name>/                RST + _doxygen/xml (umbrella-ready)
#   docs-next/packages/_manifest.json             breathe project registry
#   docs-next/_rosdoc2_out/<pkg_name>/            full standalone rosdoc2 HTML (debug)
#   docs-next/_rosdoc2_sources/<pkg_name>/        raw wrapped_sphinx_directory (debug)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SUBMODULE="$REPO_ROOT/submodules/TriOrb-AMR-Package"
OUT_HOST="$REPO_ROOT/docs-next/_rosdoc2_out"
SRC_OUT_HOST="$REPO_ROOT/docs-next/_rosdoc2_sources"
PACKAGES_DIR="$REPO_ROOT/docs-next/packages"
MANIFEST="$PACKAGES_DIR/_manifest.json"

# When no args given, auto-discover every package.xml under pkgs/ and filter
# out upstream / template / collab / third-party wrappers (user-facing docs
# should only cover TriOrb-authored packages).
EXCLUDE_PATTERNS=(
    "pkgs-collab/"              # separate site for collab (per decision 2026-04-20)
    "pkgs/template/"            # scaffolding templates, not shipped
    "pkgs/mqtt_client/"         # upstream ros2/mqtt_client fork, document externally
    "pkgs/rosbridge_suite/"     # upstream fork
    "pkgs/stella_vslam_ros"     # shown as a "Visual SLAM" stub instead
    "pkgs/tagslam_ws/src/tagslam"      # upstream TagSLAM
    "pkgs/tagslam_ws/src/flex_sync"    # upstream dep
    "pkgs/tagslam_ws/src/apriltag_msgs"  # upstream dep
)

# Skip hidden packages (basename starts with '.') and any package that colcon
# would ignore via a COLCON_IGNORE marker — either in the package directory
# itself or anywhere between the package and the submodule root.
is_excluded() {
    local path="$1"
    case "$(basename "$path")" in
        .*) return 0 ;;
    esac
    local pat
    for pat in "${EXCLUDE_PATTERNS[@]}"; do
        case "$path" in *"$pat"*) return 0 ;; esac
    done
    # Walk up from <path> to $SUBMODULE, looking for COLCON_IGNORE.
    local cur="$SUBMODULE/$path"
    while [ "$cur" != "$SUBMODULE" ] && [ "$cur" != "/" ]; do
        if [ -e "$cur/COLCON_IGNORE" ]; then
            return 0
        fi
        cur="$(dirname "$cur")"
    done
    return 1
}

# Extract the <name> tag from a package.xml (colcon's truth).
pkg_name_from_xml() {
    grep -oE '<name>[^<]+</name>' "$1" | head -1 | sed -E 's|</?name>||g'
}

if [ $# -gt 0 ]; then
    PKG_RELS=("$@")
else
    PKG_RELS=()
    while IFS= read -r pkgxml; do
        rel="${pkgxml#"$SUBMODULE/"}"
        rel="${rel%/package.xml}"
        is_excluded "$rel" && continue
        PKG_RELS+=("$rel")
    done < <(find "$SUBMODULE/pkgs" -name package.xml 2>/dev/null | sort)
fi

if [ ${#PKG_RELS[@]} -eq 0 ]; then
    echo "ERROR: no packages selected" >&2
    exit 1
fi

mkdir -p "$OUT_HOST" "$SRC_OUT_HOST" "$PACKAGES_DIR"

# Verify all packages exist and resolve each directory to its package.xml <name>
# (colcon/rosdoc2 target names come from the XML, not the directory basename —
# they occasionally differ, e.g. sick_Flexi-Soft_ROS2/src → sick_flexi_soft).
# PKG_NAMES[i] corresponds to PKG_RELS[i].
PKG_NAMES=()
for pkg_rel in "${PKG_RELS[@]}"; do
    xml="$SUBMODULE/$pkg_rel/package.xml"
    if [ ! -f "$xml" ]; then
        echo "ERROR: package.xml not found: $xml" >&2
        exit 1
    fi
    name="$(pkg_name_from_xml "$xml")"
    if [ -z "$name" ]; then
        echo "ERROR: could not parse <name> in $xml" >&2
        exit 1
    fi
    PKG_NAMES+=("$name")
done

echo "=== targets (${#PKG_NAMES[@]}): ${PKG_NAMES[*]} ==="

# Build all targets in a single colcon invocation (shared dep graph → fastest).
COLCON_PKG_LIST="${PKG_NAMES[*]}"

# Docker-side script: colcon build once, then rosdoc2 per package.
docker run --rm -t \
    -v "$SUBMODULE":/ws/src-ro:ro \
    -v "$OUT_HOST":/ws/output \
    -v "$SRC_OUT_HOST":/ws/sources_out \
    -w /ws \
    triorb-rosdoc2 \
    bash -c "
        set -e
        source /opt/ros/humble/setup.bash
        mkdir -p /ws/src
        ln -sfn /ws/src-ro /ws/src/TriOrb-AMR-Package

        echo '=== rosdep install ==='
        rosdep install -i -y -r --from-paths /ws/src/TriOrb-AMR-Package --rosdistro humble \
            --skip-keys='tagslam cuda_efficient_features stella_vslam rosbridge_server rosbridge_library rosbridge_msgs rosapi rosapi_msgs rosbridge_test_msgs' \
            >/dev/null 2>&1 || echo '(rosdep: some deps skipped; continuing)'

        echo '=== colcon build --packages-up-to ${COLCON_PKG_LIST} ==='
        colcon build --base-paths src --packages-up-to ${COLCON_PKG_LIST} --merge-install \
            --cmake-args -DCMAKE_BUILD_TYPE=Release 2>&1 | tail -20
        source install/setup.bash

        # Iterate paired arrays (bash hack: expand rel then name via indexed access).
        rels=(${PKG_RELS[*]})
        names=(${PKG_NAMES[*]})
        for i in \"\${!rels[@]}\"; do
            pkg_rel=\"\${rels[i]}\"
            pkg_name=\"\${names[i]}\"
            echo \"=== rosdoc2 build: \$pkg_name (\$pkg_rel) ===\"
            rosdoc2 build \
                --package-path /ws/src/TriOrb-AMR-Package/\$pkg_rel \
                --output-directory /ws/output \
                --install-directory /ws/install \
                2>&1 | tail -10 || echo \"(rosdoc2 failed for \$pkg_name; continuing)\"

            WRAPPED_SRC=\$(find /ws/docs_build/\$pkg_name -type d -name wrapped_sphinx_directory | head -1)
            if [ -z \"\$WRAPPED_SRC\" ]; then
                echo \"WARN: wrapped_sphinx_directory not found for \$pkg_name; skipping export\"
                continue
            fi
            DEST=/ws/sources_out/\$pkg_name
            rm -rf \"\$DEST\"
            mkdir -p \"\$DEST\"
            cp -r \"\$WRAPPED_SRC/.\" \"\$DEST/\"
            rm -rf \"\$DEST/sphinx_output\"
            chmod -R u+rw \"\$DEST\" || true
        done
        # Relax ownership so host scripts can read/modify.
        chown -R $(id -u):$(id -g) /ws/sources_out /ws/output || true
    "

# Host-side post-processing: for each package, materialize under packages/<name>/
# Args: REPO_ROOT [<pkg_rel>:<pkg_name>] ...
PAIRS=()
for i in "${!PKG_RELS[@]}"; do
    PAIRS+=("${PKG_RELS[i]}:${PKG_NAMES[i]}")
done
python3 - <<'PY' "$REPO_ROOT" "${PAIRS[@]}"
import json
import os
import re
import shutil
import sys
from pathlib import Path

repo_root = Path(sys.argv[1]).resolve()
pairs = [arg.split(":", 1) for arg in sys.argv[2:]]


# Category mapping — derived from the package's path under TriOrb-AMR-Package.
# Order here drives the display order in packages/index.md.
CATEGORY_ORDER = [
    "Drive & Navigation",
    "SLAM",
    "Sensor I/O",
    "Safety Sensors",
    "OS / Infrastructure",
    "Interfaces",
    "Other",
]

# Packages excluded from the public API docs. Mirrors the master-side
# gather_md.py EXCLUDE_KWDS so docs-next and the legacy MkDocs navigation
# stay aligned. Matched against `pkg_rel` (the package path under the
# submodule root); substring match.
EXCLUDE_PREFIXES = (
    "pkgs/triorb_navi_bridge",       # leaf pkg — not public API
    "pkgs/triorb_navigation_pkgs/",  # internal controller / planner modules
    "pkgs/triorb_fleet/",            # fleet management, internal
    "pkgs/triorb_service/",          # infra services, internal
    "pkgs/rosbridge_suite/",
    "pkgs-collab/",                  # collaborative API — separate site, not exposed here
    "pkgs/stella_vslam_ros/",        # visual_slam page is the hand-written replacement
    "pkgs/triorb_drive/path_planning_server",
    # Additional exclusions (2026-04-22) — internal / not public API.
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
    # 3rd-party SICK safetyscanner driver stack — internal-only.
    "pkgs/triorb_sensor/sick/sick_safetyscanners2",
    "pkgs/triorb_sensor/sick/sick_safetyscanners_base",
)


def is_excluded(pkg_rel: str) -> bool:
    return any(pkg_rel.startswith(p) for p in EXCLUDE_PREFIXES)


def categorize(pkg_rel: str) -> str:
    """Classify a ROS 2 package by its source path."""
    if pkg_rel.startswith("pkgs/triorb_drive/"):
        return "Drive & Navigation"
    if pkg_rel.startswith("pkgs/triorb_navigation_pkgs/"):
        return "Drive & Navigation"
    if pkg_rel == "pkgs/triorb_navi_bridge":
        return "Drive & Navigation"
    if pkg_rel.startswith("pkgs/tagslam_ws/"):
        return "SLAM"
    if pkg_rel.startswith("pkgs/triorb_sensor/sick/"):
        return "Safety Sensors"
    if pkg_rel.startswith("pkgs/triorb_sensor/"):
        return "Sensor I/O"
    if pkg_rel.startswith("pkgs/triorb_os/"):
        return "OS / Infrastructure"
    if pkg_rel.startswith("pkgs/triorb_fleet/"):
        return "Fleet"
    if pkg_rel.startswith("pkgs/triorb_service/"):
        return "Service"
    if pkg_rel.startswith("pkgs/TriOrb-ROS2-Types/"):
        return "Interfaces"
    return "Other"


# Handwritten pages map their category via docs-next/_handwritten/packages/_categories.json.
handwritten_categories = {}
hw_cats_path = repo_root / "docs-next" / "_handwritten" / "packages" / "_categories.json"
if hw_cats_path.exists():
    handwritten_categories = json.loads(hw_cats_path.read_text(encoding="utf-8"))

sources_root = repo_root / "docs-next" / "_rosdoc2_sources"
output_root = repo_root / "docs-next" / "_rosdoc2_out"
packages_root = repo_root / "docs-next" / "packages"
manifest_path = packages_root / "_manifest.json"
packages_root.mkdir(parents=True, exist_ok=True)

manifest = {}
if manifest_path.exists():
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        manifest = {}

project_re = re.compile(r":project:\s+(.+?)\s*$", re.MULTILINE)

for pkg_rel, pkg_name in pairs:
    if is_excluded(pkg_rel):
        print(f"SKIP {pkg_name}: excluded by EXCLUDE_PREFIXES rule ({pkg_rel})")
        manifest.pop(pkg_name, None)
        continue
    src = sources_root / pkg_name
    if not src.exists():
        print(f"SKIP {pkg_name}: RST sources missing at {src}", file=sys.stderr)
        continue

    dest = packages_root / pkg_name
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)

    # Copy RST tree (excluding conf.py — umbrella owns Sphinx config, and
    # exhale's generated/ output which leaks license-auth internals such as
    # ct.hpp / sha256.h program listings).
    for item in src.iterdir():
        if item.name == "conf.py":
            continue
        if item.name == "generated":
            continue  # security: see docs-next/_scripts/strip_cpp_api_toctree.py
        target = dest / item.name
        if item.is_dir():
            shutil.copytree(item, target, symlinks=False)
        else:
            shutil.copy2(item, target)

    # Copy Doxygen XML into dest/_doxygen/xml (if any).
    dox_xml = output_root / pkg_name / "generated" / "doxygen" / "xml"
    if dox_xml.is_dir():
        dest_xml = dest / "_doxygen" / "xml"
        dest_xml.parent.mkdir(parents=True, exist_ok=True)
        if dest_xml.exists():
            shutil.rmtree(dest_xml)
        shutil.copytree(dox_xml, dest_xml, symlinks=False)

    # Strip the toctree line that points at the deleted `generated/` tree
    # ("   C++ API <generated/index>"). Leaving it causes Sphinx to emit a
    # broken-toctree warning and a dead link on the package page.
    pkg_index = dest / "index.rst"
    if pkg_index.is_file():
        lines = pkg_index.read_text(encoding="utf-8").splitlines()
        keep = [ln for ln in lines if "generated/index" not in ln]
        if len(keep) != len(lines):
            pkg_index.write_text("\n".join(keep) + "\n", encoding="utf-8")

    # Rewrite literalinclude paths: rosdoc2 emits relative paths anchored at the
    # container build dir. The container mounts the submodule at
    # /ws/src/TriOrb-AMR-Package, so the generated RST goes up 6 levels then
    # into src/TriOrb-AMR-Package/<pkg_rel>/<file>. On the host, the submodule
    # lives at submodules/TriOrb-AMR-Package, reachable from
    # docs-next/packages/<pkg_name>/<subdirs>/<file.rst>. Count up-levels per file.
    up_prefix_re = re.compile(r"(\.\./)+src/TriOrb-AMR-Package/")
    for rst in dest.rglob("*.rst"):
        # rel_depth = number of intermediate directories between packages/ and the file.
        # Example: packages/<pkg>/interfaces/msg/foo.rst → 3 intermediate dirs (<pkg>, interfaces, msg).
        # Up from the rst to repo root: rel_depth + 2 levels (one for `packages/`, one for `docs-next/`).
        rel_depth = len(rst.relative_to(packages_root).parts) - 1
        ups = "../" * (rel_depth + 2)
        target_prefix = f"{ups}submodules/TriOrb-AMR-Package/"
        text = rst.read_text(encoding="utf-8")
        new_text, n = up_prefix_re.subn(target_prefix, text)
        if n:
            rst.write_text(new_text, encoding="utf-8")

    # Discover breathe project name (first occurrence wins).
    breathe_project = None
    for rst in dest.rglob("*.rst"):
        m = project_re.search(rst.read_text(encoding="utf-8"))
        if m:
            breathe_project = m.group(1).strip()
            break
    entry = {
        "path": f"packages/{pkg_name}",
        "category": categorize(pkg_rel),
    }
    if breathe_project and (dest / "_doxygen" / "xml").is_dir():
        entry["breathe_project"] = breathe_project
        entry["doxygen_xml"] = f"packages/{pkg_name}/_doxygen/xml"
    manifest[pkg_name] = entry
    print(f"OK   {pkg_name}: materialized to {dest.relative_to(repo_root)} (category='{entry['category']}', breathe='{breathe_project}')")

manifest_path.write_text(
    json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)
print(f"=== manifest updated: {manifest_path.relative_to(repo_root)} ===")

# Merge hand-written package pages from docs-next/_handwritten/packages/*.md
# These are committed to the repo and represent packages that should appear in
# the Package API nav but whose internals are not suitable for rosdoc2 (external
# wrappers like stella_vslam_ros → "Visual SLAM").
handwritten_root = repo_root / "docs-next" / "_handwritten" / "packages"
handwritten_names = []
if handwritten_root.is_dir():
    for item in sorted(handwritten_root.iterdir()):
        if item.suffix != ".md" or item.name.startswith("_"):
            continue
        name = item.stem
        dest_md = packages_root / f"{name}.md"
        shutil.copy2(item, dest_md)
        handwritten_names.append(name)
        category = handwritten_categories.get(name, "Other")
        manifest[name] = {
            "path": f"packages/{name}",
            "category": category,
            "handwritten": True,
        }
        print(f"HAND {name}: copied {item.relative_to(repo_root)} -> {dest_md.relative_to(repo_root)} (category='{category}')")

# Emit packages/index.md grouped by category. Each category becomes a ## heading
# with its own toctree. Categories appear in CATEGORY_ORDER; packages within a
# category are alphabetized. Hand-written pages (where entry["handwritten"] is
# True) render without the /index suffix.
by_cat = {c: [] for c in CATEGORY_ORDER}  # dict[str, list[(name, entry)]]
for name, entry in manifest.items():
    cat = entry.get("category", "Other")
    by_cat.setdefault(cat, []).append((name, entry))

idx_path = packages_root / "index.md"
lines = [
    "# Package API",
    "",
    "Auto-generated API reference for ROS 2 packages under TriOrb-AMR-Package,",
    "produced by rosdoc2. Packages are grouped by subsystem; within each group",
    "they are sorted alphabetically.",
    "",
]
for cat in CATEGORY_ORDER:
    entries = by_cat.get(cat, [])
    if not entries:
        continue
    lines.extend([f"## {cat}", ""])
    lines.extend(["```{toctree}", ":maxdepth: 1", ":titlesonly:", ""])
    for name, entry in sorted(entries, key=lambda kv: kv[0]):
        suffix = "" if entry.get("handwritten") else "/index"
        lines.append(f"{name}{suffix}")
    lines.extend(["```", ""])

# Any uncategorized leftovers (shouldn't happen but defensive).
extras = [n for n in by_cat if n not in CATEGORY_ORDER and by_cat[n]]
if extras:
    lines.extend(["## Other", ""])
    lines.extend(["```{toctree}", ":maxdepth: 1", ":titlesonly:", ""])
    for cat in extras:
        for name, entry in sorted(by_cat[cat], key=lambda kv: kv[0]):
            suffix = "" if entry.get("handwritten") else "/index"
            lines.append(f"{name}{suffix}")
    lines.extend(["```", ""])

idx_path.write_text("\n".join(lines), encoding="utf-8")
print(f"=== umbrella package index written: {idx_path.relative_to(repo_root)} ===")
PY

echo "done."
