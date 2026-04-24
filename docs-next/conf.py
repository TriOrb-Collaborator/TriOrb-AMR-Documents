"""Sphinx configuration for the TriOrb BASE developer guide (docs-next PoC)."""

from __future__ import annotations

import os

project = "TriOrb BASE Developer Guide"
author = "TriOrb Inc."
copyright = "2025-2026, TriOrb Inc."
release = os.environ.get("DOCS_RELEASE", "v1.2.4")
version = release

extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_togglebutton",
    "sphinxcontrib.mermaid",
    "breathe",
    "sphinx.ext.autodoc",
    "sphinx.ext.ifconfig",
    "sphinx.ext.intersphinx",
]

# Breathe (C++ via Doxygen XML). breathe_projects is populated from
# packages/_manifest.json which is produced by docs-next/docker/run_rosdoc2.sh.
# Each entry names a ROS 2 package whose Doxygen XML was exported to
# packages/<pkg>/_doxygen/xml during the rosdoc2 run.
import json as _json
from pathlib import Path as _Path

_manifest_path = _Path(__file__).parent / "packages" / "_manifest.json"
breathe_projects = {}
if _manifest_path.exists():
    for _pkg_name, _entry in _json.loads(_manifest_path.read_text(encoding="utf-8")).items():
        _proj = _entry.get("breathe_project")
        _xml = _entry.get("doxygen_xml")
        if _proj and _xml:
            breathe_projects[_proj] = _xml
breathe_default_project = next(iter(breathe_projects), "")
breathe_default_members = ("members", "undoc-members")

# Packages that were introspected without their Python deps installed locally.
autodoc_mock_imports = [
    "rclpy",
    "rclcpp",
    "std_msgs",
    "std_srvs",
    "geometry_msgs",
    "sensor_msgs",
    "triorb_cv_interface",
    "triorb_drive_interface",
    "triorb_field_interface",
    "triorb_project_interface",
    "triorb_sensor_interface",
    "triorb_static_interface",
    "triorb_plc_interface",
    "triorb_collaboration_interface",
]

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "linkify",
    "substitution",
    "tasklist",
]

templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "locale",
    "venv",
    ".venv",
    "README.md",
    "CI.md",
    "HANDOFF.md",
    "_rosdoc2_out",
    "_rosdoc2_sources",
    "_handwritten",
    "_drafts",
    "packages/*/_doxygen",
]

# - myst.xref_missing: legacy mike version archive links (../v1.2.x/) resolve only at deploy time.
# - duplicate_declaration.c / ref.label: rosdoc2-via-exhale generates identically-named
#   C macros (NODE_NAME etc.) and labels (dir_include, namespace_rclcpp) per package —
#   these are expected when multiple ROS 2 packages are aggregated in one umbrella build.
suppress_warnings = [
    "myst.xref_missing",
    "duplicate_declaration.c",
    "duplicate_label",
]

# English is the source of truth. Japanese is a translation target under
# locale/ja/LC_MESSAGES/*.po; rosdoc2-generated labels (which are English)
# therefore line up with the source language naturally.
language = "en"
locale_dirs = ["locale/"]
gettext_compact = False

html_theme = "furo"
html_title = f"{project} {release}"
html_static_path = ["_static"]
html_favicon = "_static/favicon.png"
html_logo = "_static/TriOrb_BASE.svg"
# brand.css adds the Lapis-Lazuli overlay (sidebar gradient, H1 accent
# underline, active-nav side border, icon hiding). Served from _static/
# so every page gets a theme-correct relative href at build time — this
# is what keeps the site consistent when deployed under a project page
# prefix like /TriOrb-AMR-Documents/.
html_css_files = ["brand.css"]
html_js_files = ["mqtt-api-modal.js"]

# Lapis Lazuli brand colors, carried over from the legacy mike site
# (triorb-amr-docs/docs/stylesheets/extra.css — primary rgb(34,59,128)).
# Furo converts these into CSS custom properties served from its own theme.
html_theme_options = {
    "source_repository": "https://github.com/TriOrb-Inc/TriOrb-AMR-Documents",
    "source_branch": "docs2-poc",
    "source_directory": "docs-next/",
    # Logo already contains the "TriOrb BASE" wordmark — don't double up.
    "sidebar_hide_name": True,
    "light_css_variables": {
        "color-brand-primary": "rgb(34, 59, 128)",
        "color-brand-content": "rgb(34, 59, 128)",
    },
    "dark_css_variables": {
        # Lightened for contrast against Furo's dark background.
        "color-brand-primary": "rgb(138, 162, 224)",
        "color-brand-content": "rgb(138, 162, 224)",
    },
}

# Language switcher rendered via _templates/sidebar/language-switcher.html
html_sidebars = {
    "**": [
        "sidebar/scroll-start.html",
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/language-switcher.html",
        "sidebar/navigation.html",
        "sidebar/scroll-end.html",
    ]
}

# Source suffix: prefer Markdown (MyST) for hand-written pages.
source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}

# Multi-version config is supplied when sphinx-multiversion is used at release build time.
smv_tag_whitelist = r"^v\d+\.\d+\.\d+$"
smv_branch_whitelist = r"^(master|docs2/.*)$"
smv_remote_whitelist = r"^origin$"
smv_released_pattern = r"^refs/tags/v\d+\.\d+\.\d+$"
