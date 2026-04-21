# docs-next HANDOFF (2026-04-21)

Live snapshot for picking up this work in a fresh session. Pair with
`~/.claude/projects/-nvme-home-tobeta-TriOrb-AMR-Documents/memory/`.

## 1. Current state — Phase 4 largely landed

| Area | Status |
| --- | --- |
| Pipeline | Sphinx + rosdoc2 + Furo on `docs-next/`, committed on `docs2/phase2`. |
| Landing page (`/`) | Bilingual version picker at `docs-next/_landing/index.html`. Level B (logo-free, JA+EN description, version cards, last-updated stamp, contact). |
| Deploy layout | `_build/deploy/{index.html, v1.2.4/{en,ja}/, favicon.png, TriOrb_concept.webp, brand.css}`. `deploy-stage-local` hydrates `v1.2.2/`, `v1.2.3/`, and mike shared assets from the local `gh-pages` branch for end-to-end local preview. |
| Release label | `conf.py` default `v1.2.4`; `DOCS_RELEASE` env override. |
| Legacy mike | `.github/workflows/jekyll-gh-pages2.yml` is a `workflow_dispatch` + `if: false` stub. Effectively disabled. |
| gh-pages deploy | CI step **not yet wired**. Phase 4 pre-cutover is local-only. |
| Translation scope | **B plan**: only the 7 hand-written pages are translated (`index.md`, `guides/{overview,history,terms,privacy}.md`, `packages/index.md`, `packages/visual_slam.md`). rosdoc2-generated API pages ship English-only. PO tree under `locale/ja/LC_MESSAGES/packages/**` was deleted; gitignore allows `packages/{index,visual_slam}.po` as exceptions. |
| Branding | Lapis Lazuli `rgb(34, 59, 128)` from the legacy mike site. Applied both in Furo (via `conf.py` theme options) and on the landing page. `brand.css` injected at deploy-stage adds mike-style polish (sidebar brand gradient, H1 accent underline, active-nav side border, admonition border, TOC heading color). |
| Favicon | `image/triorb_connect_icon.png` → `_static/favicon.png` (Sphinx) + `_landing/favicon.png` (landing). |

## 2. Content correctness pass (2026-04-21)

The product overview now describes the **ball-drive omnidirectional motion
mechanism** (3 spheres, 3 motors) per the TriOrb corporate site — the
earlier "three omniwheels" line was wrong. Collaborative navigation is
dropped from the public documentation (API is not designed for control
from external ROS 2 nodes). Terms / Privacy H1s are simplified to
"Terms of Use" / "Privacy Policy" and "利用規約" / "プライバシー
ポリシー" (dropping the "(Draft)" / "（案）" suffix).

`packages/index.md` now excludes everything the master-side
`gather_md.py` marks as non-public (`pkgs/triorb_navi_bridge`,
`pkgs/triorb_navigation_pkgs`, `pkgs/triorb_fleet`, etc.) plus
`path_planning_server`. The whole "Fleet" category is removed as a
result. `deploy-stage` then runs `_scripts/strip_readme_anchors.py` to
scrub the rosdoc2 "README" anchor entries that Sphinx's `:titlesonly:`
fails to suppress when they come from an `.. include ::` directive.

## 3. Build performance (B plan payoff)

On this box, a single-line source edit after `make clean`:

| Before B plan | After B plan |
| --- | --- |
| 1583 docs invalidated per edit | 100–120 docs invalidated (only hand-written pages + their category neighbors) |
| 60–120 min per rebuild | 10–20 min per rebuild |
| `fill_translations.py` used to touch ~1,500 PO files each invocation | filler's save-only-on-hit patch + no packages/** means 0–4 PO files touched |

`conf.py` edits still reset `env.pickle` entirely (Sphinx's
`config_status` is conservative), so avoid conf.py tweaks during
iteration. Brand-color tweaks go in `_static/` / `_landing/brand.css`
or the theme_options light/dark CSS variables already in place.

## 4. Commit history (docs2/phase2 tip)

```
daaf407 docs: rewrite root README around current docs-next pipeline
b46840c docs2: B plan — drop rosdoc2 packages/** from i18n scope
97ef73a docs2: refresh terms/privacy JA PO after H1 simplification
59c419e docs2: simplify Terms/Privacy H1 titles (drop "(Draft)" / "（案）")
287c64d docs2: add brand image assets + landing page chrome
0b63be2 docs2: add Sphinx favicon + Lapis Lazuli brand palette
033a70f docs2: refresh index + history JA PO files after content pass
66e6553 docs2: retire v1.2.5-dev references + point past-versions list at v1.2.3/2
5930dd4 docs2: add Phase 4 landing page + deploy-stage layout targets
e640941 docs2: bump Sphinx release to v1.2.4 + exclude HANDOFF.md from build
8ad6ba8 docs2: track generated packages/**/*.po (D2 filler outputs + hand-edited)  [superseded by b46840c]
1895c96 docs2: fix visual_slam PO path + drop orphan _handwritten PO
4461fa2 docs2: extend D2 label dict + skip no-op PO saves
0d48153 add root CLAUDE.md with pipeline split guidance
2c7180c docs2: add Phase 2 handoff doc + iterate visual-check targets
1d14cc2 docs2: add translation filler + parallel Sphinx builds
43635d6 docs2: strip numeric H2 prefixes from Terms/Privacy (MyST i18n workaround)
e06cc6d docs2: group Package API index by subsystem category (pre-session)
77ca04b docs2: add Sphinx + rosdoc2 + Furo docs pipeline (pre-session)
```

## 5. Resume commands

```bash
# Shell prerequisites
source /nvme/home/tobeta/TriOrb-AMR-Documents/.venv-docs2/bin/activate
cd /nvme/home/tobeta/TriOrb-AMR-Documents/docs-next

# Typical translation + rebuild loop (~10 min on this box)
python3 _scripts/fill_translations.py
sphinx-intl build -l ja
SPHINXOPTS="-j 1" make html-ja        # -j auto has crashed; use -j 1 or -j 4

# Full-site local preview
make deploy-stage-local               # landing + v1.2.4/{en,ja}/ + v1.2.2/3 from gh-pages
cd _build/deploy && python3 -m http.server 18000 &
# Open http://localhost:18000/
```

## 6. Still pending / next decisions

1. **CI gh-pages deploy step**: add to `.github/workflows/docs2.yml` as
   `workflow_dispatch` first, then enable automatic deploy on
   `docs2/phase2` push after a smoke run.
2. **Cutover announcement**: inform stakeholders before flipping
   `/v1.2.4/` on gh-pages (the legacy mike `/v1.2.4/` gets replaced).
3. **Sphinx logo**: we have `image/TriOrb_Logo_White-Blue_with_concept.svg`;
   not yet wired via `html_logo`. Adding it would trigger a full
   rebuild — bundle it with the next content batch.
4. **v1.2.4 release work on `master`**: separate session. Submodule
   bumps (`TriOrb-AMR-Package @ 9cb35f1d`, `triorb-core @ cb94e5c`),
   `gather_md.py` regen, `triorb-amr-docs/docs/TriOrb-AMR-Package/**`
   updates.
5. **v1.2.4 release notes → history.md**: currently the summary pulls
   from `1.2.4.2` release notes; keep in sync as new patch releases
   land.

## 7. Where things live

```
docs-next/
├── HANDOFF.md                               ← this file
├── CI.md                                    ← CI design notes
├── README.md                                ← current docs-next quickstart
├── conf.py                                  ← Sphinx config (v1.2.4, favicon, Lapis brand)
├── Makefile                                 ← html, html-ja, gettext, update-po, rosdoc2, deploy-stage{,-local}, serve{,-deploy}
├── index.md                                 ← site root (MyST)
├── guides/{overview,history,terms,privacy}.md
├── packages/                                ← rosdoc2 output (gitignored except .md/.po below)
│   ├── index.md                             ← category-grouped toctree
│   └── visual_slam.md                       ← external-component hand-written stub
├── _handwritten/packages/visual_slam.md     ← authoring source (copied into packages/)
├── _landing/                                ← deploy-stage landing
│   ├── index.html                           ← bilingual version picker template
│   ├── favicon.png, TriOrb_concept.webp
│   └── brand.css                            ← mike-style overlay (injected into every versioned page at deploy-stage)
├── _static/                                 ← Sphinx static (favicon, concept)
├── _scripts/
│   ├── fill_translations.py                 ← D1 PO filler (7 hand-written pages)
│   └── strip_readme_anchors.py              ← post-process: remove rosdoc2 README anchors from packages/index.html
├── _templates/sidebar/language-switcher.html
├── docker/                                  ← rosdoc2 Docker image + run script
└── locale/ja/LC_MESSAGES/                   ← JA PO/MO (D1 only: guides, index, packages/{index,visual_slam})
.github/workflows/
├── docs2.yml                                ← build + artifact; gh-pages deploy step pending
└── jekyll-gh-pages2.yml                     ← stub, disabled
```

Memory index: `~/.claude/projects/-nvme-home-tobeta-TriOrb-AMR-Documents/memory/MEMORY.md`.
