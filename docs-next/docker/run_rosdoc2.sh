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

# Public package pages are intentionally allow-listed. This is more robust than
# relying on accumulated exclude rules alone: partial rosdoc2 refreshes should
# never resurrect internal packages from a stale manifest or old package dirs.
PUBLIC_PACKAGE_NAMES = {
    "triorb_drive_pico",
    "triorb_drive_vector",
    "triorb_navigation",
    "triorb_navigation_manager",
    "triorb_safe_run_cpp",
    "triorb_snr_mux_driver",
    "triorb_tagslam_manager",
    "triorb_camera_argus",
    "triorb_camera_capture",
    "triorb_gamepad",
    "triorb_sick_plc_wrapper",
    "triorb_sls_wrapper",
    "triorb_battery_info",
    "triorb_gpio",
    "triorb_host_info",
    "triorb_os_setting",
}

# Packages excluded from the public API docs. Mirrors the master-side
# gather_md.py EXCLUDE_KWDS so docs-next and the legacy MkDocs navigation
# stay aligned. Matched against `pkg_rel` (the package path under the
# submodule root); substring match.
EXCLUDE_PREFIXES = (
    "pkgs/triorb_drive/path_planning_server",
    "pkgs/triorb_drive/triorb_automove_task",
    "pkgs/triorb_drive/triorb_dead_reckoning",
    "pkgs/triorb_drive/triorb_follow_path_planner",
    "pkgs/triorb_drive/triorb_linear_path_planner",
    "pkgs/triorb_navi_bridge",       # leaf pkg — not public API
    "pkgs/triorb_navigation_pkgs/",  # internal controller / planner modules
    "pkgs/triorb_drive/triorb_navigation_utils",
    "pkgs/triorb_drive/triorb_navigation_vslam_tf",
    "pkgs/triorb_drive/triorb_path_controller_interface",
    "pkgs/triorb_drive/triorb_path_follow_controller",
    "pkgs/triorb_fleet/",            # fleet management, internal
    "pkgs/triorb_service/",          # infra services, internal
    "pkgs/rosbridge_suite/",
    "pkgs-collab/",                  # collaborative API — separate site, not exposed here
    "pkgs/stella_vslam_ros/",        # visual_slam page is the hand-written replacement
    # Additional exclusions (2026-04-22) — internal / not public API.
    "pkgs/triorb_drive/triorb_path_search_server",
    "pkgs/triorb_drive/triorb_pid_pos_controller",
    "pkgs/triorb_drive/triorb_pid_vel_controller",
    "pkgs/triorb_drive/triorb_region_map",
    "pkgs/triorb_drive/triorb_towing_path_planner",
    "pkgs/triorb_drive/triorb_vslam_tf",
    "pkgs/triorb_drive/triorb_vslam_tf_bridge",
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
    # Additional internal-only packages.
    "pkgs/triorb_sensor/triorb_streaming_images",
    "pkgs/triorb_sensor/sick/sick_Flexi-Soft_ROS2",
    "pkgs/triorb_os/triorb_socket",
)


def is_excluded(pkg_rel: str) -> bool:
    return any(pkg_rel.startswith(p) for p in EXCLUDE_PREFIXES)


def is_public_package(pkg_name: str, category: str) -> bool:
    if category == INTERFACE_CATEGORY:
        return True
    return pkg_name in PUBLIC_PACKAGE_NAMES


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
interfaces_root = repo_root / "docs-next" / "interfaces"
manifest_path = packages_root / "_manifest.json"
packages_root.mkdir(parents=True, exist_ok=True)
interfaces_root.mkdir(parents=True, exist_ok=True)

# Category whose packages are materialized under interfaces/ (not packages/).
INTERFACE_CATEGORY = "Interfaces"


def root_for_category(cat: str) -> Path:
    return interfaces_root if cat == INTERFACE_CATEGORY else packages_root


def path_prefix_for_category(cat: str) -> str:
    return "interfaces" if cat == INTERFACE_CATEGORY else "packages"


def strip_leading_markdown_h1(text: str) -> str:
    lines = text.splitlines()
    if not lines:
        return text
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and lines[i].startswith("# "):
        i += 1
        while i < len(lines) and not lines[i].strip():
            i += 1
        return "\n".join(lines[i:]) + ("\n" if i < len(lines) else "")
    return text

manifest = {}
if manifest_path.exists():
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        manifest = {}

project_re = re.compile(r":project:\s+(.+?)\s*$", re.MULTILINE)

for pkg_rel, pkg_name in pairs:
    category = categorize(pkg_rel)
    if is_excluded(pkg_rel) or not is_public_package(pkg_name, category):
        reason = "EXCLUDE_PREFIXES" if is_excluded(pkg_rel) else "PUBLIC_PACKAGE_NAMES allowlist"
        print(f"SKIP {pkg_name}: excluded by {reason} ({pkg_rel})")
        manifest.pop(pkg_name, None)
        stale_pkg = packages_root / pkg_name
        if stale_pkg.exists():
            shutil.rmtree(stale_pkg)
        continue
    src = sources_root / pkg_name
    if not src.exists():
        print(f"SKIP {pkg_name}: RST sources missing at {src}", file=sys.stderr)
        continue

    dest_root = root_for_category(category)
    dest = dest_root / pkg_name
    # Also remove any stale copy under the OTHER root from a previous run
    # (e.g., Interfaces package used to live under packages/).
    other_root = packages_root if dest_root is interfaces_root else interfaces_root
    stale = other_root / pkg_name
    if stale.exists():
        shutil.rmtree(stale)
        manifest.pop(pkg_name, None)
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

    # Copy hand-written language variants for package overview/API pages.
    # The package source remains the authoring source of truth; the umbrella
    # Sphinx build then switches between JA and EN at render time.
    submodule_pkg_dir = repo_root / "submodules" / "TriOrb-AMR-Package" / pkg_rel
    submodule_api = submodule_pkg_dir / "API.md"
    submodule_api_en = submodule_pkg_dir / "API(EN).md"
    has_api = submodule_api.is_file()
    has_api_en = submodule_api_en.is_file()
    if has_api:
        (dest / "API(JA).md").write_text(
            strip_leading_markdown_h1(submodule_api.read_text(encoding="utf-8")),
            encoding="utf-8",
        )
        if has_api_en:
            (dest / "API(EN).md").write_text(
                strip_leading_markdown_h1(submodule_api_en.read_text(encoding="utf-8")),
                encoding="utf-8",
            )
        api_wrapper_lines = [
            "API",
            "===",
            "",
            ".. ifconfig:: language == 'en'",
            "",
        ]
        if has_api_en:
            api_wrapper_lines += [
                "   .. include:: API(EN).md",
                "      :parser: myst_parser.sphinx_",
            ]
        else:
            api_wrapper_lines += [
                "   .. include:: API(JA).md",
                "      :parser: myst_parser.sphinx_",
            ]
        api_wrapper_lines += [
            "",
            ".. ifconfig:: language != 'en'",
            "",
            "   .. include:: API(JA).md",
            "      :parser: myst_parser.sphinx_",
            "",
        ]
        (dest / "API.rst").write_text("\n".join(api_wrapper_lines), encoding="utf-8")
        stale_api_md = dest / "API.md"
        if stale_api_md.exists():
            stale_api_md.unlink()

    # Patch index.rst:
    #   - drop the stale "   C++ API <generated/index>" toctree line
    #     (the generated/ tree is purged for security; see the skip above).
    #   - drop "   Python API <modules>" and "   Standard Documents <standards>"
    #     from the toctree so the sidebar only shows the hand-written API
    #     page we promote on the next line. The underlying pages still exist
    #     (reachable by direct URL) but they no longer clutter navigation.
    #   - when API.md is present, inject "   API <API>" as the FIRST entry
    #     of the main (non-hidden) toctree so it shows up on the package
    #     landing page without needing to touch the hand-written source.
    pkg_index = dest / "index.rst"
    if pkg_index.is_file():
        text = pkg_index.read_text(encoding="utf-8")
        drop_tokens = ("generated/index", "Python API <modules>", "Standard Documents <standards>")
        text = "\n".join(
            ln for ln in text.splitlines()
            if not any(tok in ln for tok in drop_tokens)
        )
        if has_api and "   API <API>" not in text:
            # Inject right after the first `.. toctree::` directive + its
            # option lines. Option lines look like "   :maxdepth: 2".
            m = re.search(r"(\.\. toctree::\n(?:   :\S+:[^\n]*\n)*)", text)
            if m:
                text = text.replace(m.group(1), m.group(1) + "\n   API <API>\n", 1)
        pkg_index.write_text(text + ("\n" if not text.endswith("\n") else ""), encoding="utf-8")

    # Public package landing pages should not be forced to reuse the package's
    # root README. If DOCS.md / DOCS(EN).md exist, treat them as the web-site
    # source of truth; otherwise fall back to README.md / README(EN).md.
    docs_ja_src = submodule_pkg_dir / "DOCS.md"
    docs_en_src = submodule_pkg_dir / "DOCS(EN).md"
    readme_ja_src = submodule_pkg_dir / "README.md"
    readme_en_src = submodule_pkg_dir / "README(EN).md"
    web_ja_src = docs_ja_src if docs_ja_src.is_file() else readme_ja_src
    if docs_en_src.is_file():
        web_en_src = docs_en_src
    elif readme_en_src.is_file():
        web_en_src = readme_en_src
    else:
        web_en_src = web_ja_src

    overview_ja_dst = dest / "overview.md"
    overview_en_dst = dest / "overview(EN).md"
    if web_ja_src.is_file():
        overview_ja_dst.write_text(
            strip_leading_markdown_h1(web_ja_src.read_text(encoding="utf-8")),
            encoding="utf-8",
        )
    if web_en_src.is_file():
        overview_en_dst.write_text(
            strip_leading_markdown_h1(web_en_src.read_text(encoding="utf-8")),
            encoding="utf-8",
        )

    readme_inc = dest / "__readme_include.rst"
    if readme_inc.is_file():
        readme_inc_lines = []
        if overview_en_dst.is_file():
            readme_inc_lines += [
                ".. ifconfig:: language == 'en'",
                "",
                "   .. include:: overview(EN).md",
                "      :parser: myst_parser.sphinx_",
                "",
                ".. ifconfig:: language != 'en'",
                "",
                "   .. include:: overview.md",
                "      :parser: myst_parser.sphinx_",
                "",
            ]
        else:
            readme_inc_lines += [
                ".. include:: overview.md",
                "   :parser: myst_parser.sphinx_",
                "",
            ]
        readme_inc.write_text("\n".join(readme_inc_lines), encoding="utf-8")

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
    path_prefix = path_prefix_for_category(category)
    entry = {
        "path": f"{path_prefix}/{pkg_name}",
        "category": category,
    }
    if breathe_project and (dest / "_doxygen" / "xml").is_dir():
        entry["breathe_project"] = breathe_project
        entry["doxygen_xml"] = f"{path_prefix}/{pkg_name}/_doxygen/xml"
    manifest[pkg_name] = entry
    print(f"OK   {pkg_name}: materialized to {dest.relative_to(repo_root)} (category='{entry['category']}', breathe='{breathe_project}')")

# Merge hand-written package pages from docs-next/_handwritten/packages/*.md
# These are committed to the repo and represent packages that should appear in
# the Package API nav but whose internals are not suitable for rosdoc2 (external
# wrappers like stella_vslam_ros → "Visual SLAM").
handwritten_root = repo_root / "docs-next" / "_handwritten" / "packages"
handwritten_names = []
if handwritten_root.is_dir():
    for item in sorted(handwritten_root.iterdir()):
        if item.name.startswith("_"):
            continue
        # Support two shapes:
        #   _handwritten/packages/<name>.md       → single-page package
        #   _handwritten/packages/<name>/*        → directory package (index.md
        #                                            + optional API.md, etc.)
        is_dir = item.is_dir()
        is_md  = item.is_file() and item.suffix == ".md"
        if not (is_dir or is_md):
            continue
        name = item.stem if is_md else item.name
        category = handwritten_categories.get(name, "Other")
        if is_md:
            dest_md = packages_root / f"{name}.md"
            shutil.copy2(item, dest_md)
            path_val = f"packages/{name}"
            toctree_entry_suffix = ""
            print(f"HAND {name}: copied {item.relative_to(repo_root)} -> {dest_md.relative_to(repo_root)}")
        else:
            dest_dir = packages_root / name
            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            shutil.copytree(item, dest_dir, symlinks=False)
            path_val = f"packages/{name}"
            toctree_entry_suffix = "/index"
            print(f"HAND {name}: copied {item.relative_to(repo_root)}/ -> {dest_dir.relative_to(repo_root)}/ (dir)")
        handwritten_names.append(name)
        manifest[name] = {
            "path": path_val,
            "category": category,
            "handwritten": True,
            "handwritten_dir": is_dir,
        }

# Prune stale package dirs and manifest entries. This keeps partial rosdoc2
# refreshes from reviving internal packages that used to exist in packages/_manifest.json
# or docs-next/packages/<name>/ from older runs.
allowed_package_dirs = set(PUBLIC_PACKAGE_NAMES) | set(handwritten_names)
for child in packages_root.iterdir():
    if not child.is_dir():
        continue
    if child.name.startswith("_"):
        continue
    if child.name not in allowed_package_dirs:
        shutil.rmtree(child)
        manifest.pop(child.name, None)

for name, entry in list(manifest.items()):
    if entry.get("category") == INTERFACE_CATEGORY:
        continue
    if name not in allowed_package_dirs:
        manifest.pop(name, None)

manifest_path.write_text(
    json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)
print(f"=== manifest updated: {manifest_path.relative_to(repo_root)} ===")

# Emit packages/index.md grouped by category. Each category becomes a ## heading
# with its own toctree. Categories appear in CATEGORY_ORDER; packages within a
# category are alphabetized. Hand-written pages (where entry["handwritten"] is
# True) render without the /index suffix.
by_cat = {c: [] for c in CATEGORY_ORDER}  # dict[str, list[(name, entry)]]
for name, entry in manifest.items():
    cat = entry.get("category", "Other")
    by_cat.setdefault(cat, []).append((name, entry))

# Emit packages/index.md for non-Interface categories only.
pkg_idx_path = packages_root / "index.md"
lines = [
    "# Package API",
    "",
    "Auto-generated API reference for ROS 2 packages under TriOrb-AMR-Package,",
    "produced by rosdoc2. Packages are grouped by subsystem; within each group",
    "they are sorted alphabetically.",
    "",
]
for cat in CATEGORY_ORDER:
    if cat == INTERFACE_CATEGORY:
        continue
    entries = by_cat.get(cat, [])
    if not entries:
        continue
    lines.extend([f"## {cat}", ""])
    lines.extend(["```{toctree}", ":maxdepth: 1", ":titlesonly:", ""])
    for name, entry in sorted(entries, key=lambda kv: kv[0]):
        if entry.get("handwritten"):
            suffix = "/index" if entry.get("handwritten_dir") else ""
        else:
            suffix = "/index"
        lines.append(f"{name}{suffix}")
    lines.extend(["```", ""])
pkg_idx_path.write_text("\n".join(lines), encoding="utf-8")
print(f"=== umbrella package index written: {pkg_idx_path.relative_to(repo_root)} ===")

# Emit interfaces/index.md for TriOrb-ROS2-Types packages.
iface_idx_path = interfaces_root / "index.md"
iface_entries = sorted(by_cat.get(INTERFACE_CATEGORY, []), key=lambda kv: kv[0])
if iface_entries:
    iface_lines = [
        "# Interfaces",
        "",
        "TriOrb が公開している ROS 2 メッセージ / サービス / アクション定義の一覧です。",
        "各 Interface パッケージは `submodules/TriOrb-AMR-Package/pkgs/TriOrb-ROS2-Types/` 配下で",
        "配布されており、他のノード実装がインポートして利用します。",
        "",
        "```{toctree}",
        ":maxdepth: 1",
        ":titlesonly:",
        "",
    ]
    for name, entry in iface_entries:
        if entry.get("handwritten"):
            suffix = "/index" if entry.get("handwritten_dir") else ""
        else:
            suffix = "/index"
        iface_lines.append(f"{name}{suffix}")
    iface_lines.extend(["```", ""])
    iface_idx_path.write_text("\n".join(iface_lines), encoding="utf-8")
    print(f"=== interfaces index written: {iface_idx_path.relative_to(repo_root)} ===")
PY

echo "done."
