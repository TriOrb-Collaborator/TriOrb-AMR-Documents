# docs2 Phase 2 Handoff (2026-04-20)

Live snapshot for picking up this work in a fresh session (Claude Code CLI or
similar). Pair with the memory files under
`~/.claude/projects/-nvme-home-tobeta-TriOrb-AMR-Documents/memory/`.

## 1. Current git state

- Branch: **`docs2/phase2`** (cut from master @ `62f080c`).
- Committed on this branch:
  1. `77ca04b docs2: add Sphinx + rosdoc2 + Furo docs pipeline (Phase 1 + Phase 2 PoC)`
  2. `e06cc6d docs2: group Package API index by subsystem category`
- Submodules currently checked out (matches uncommitted v1.2.4 work on master side):
  - `submodules/TriOrb-AMR-Package` → `9cb35f1d` (release/std1.2.4 tip)
  - `submodules/triorb-core` → `cb94e5c` (master tip)

## 2. Working-tree status (two independent changesets mingled)

Run `git status -s` — you will see changes from **two** unrelated work streams.
Do **not** commit them together.

### 2a. v1.2.4 release work → belongs on `master`
- `gather_md.py`
- `submodules/TriOrb-AMR-Package`, `submodules/triorb-core`
- `triorb-amr-docs/docs/TriOrb-AMR-Package/**` (History.md, pkgs/…, pkgs-collab/…, auto-gen)
- `triorb-amr-docs/docs/TriOrb-AMR-Package/document/` deletions (internal materials)
- New API pages under `Reference_API/` for 1.2.4 additions
- New root-level files: `triorb-amr-docs/docs/TriOrb-AMR-Package/pkgs/Reference_API/triorb-{drive/triorb-snr-mux-driver,os/triorb-battery-info,sensor/triorb-can}.md`

### 2b. docs2 phase 2 follow-up → belongs on `docs2/phase2`
- `docs-next/Makefile` (added `-j auto` parallel build; `update-po` now also runs `sphinx-intl build`; added `deploy-stage` target earlier — already committed, only the new changes are unstaged)
- `docs-next/_shot.py` (iterated visual-check targets)
- `docs-next/guides/terms.md`, `docs-next/guides/privacy.md` (numeric heading prefixes stripped, see section 3)
- `docs-next/locale/ja/LC_MESSAGES/guides/terms.po`, `…/privacy.po` (re-filled via `fill_translations.py`)
- `triorb-amr-docs/docs/Terms.md`, `…/Terms.en.md`, `…/PrivacyPolicy.md`, `…/PrivacyPolicy.en.md` (same numeric-prefix strip — legacy site stays in sync)

Suggested path forward for splitting:
```bash
# Save docs2 follow-ups
git stash push -m "docs2-phase2-post-rosdoc2-run" \
    docs-next/Makefile docs-next/_shot.py \
    docs-next/guides/terms.md docs-next/guides/privacy.md \
    docs-next/locale/ja/LC_MESSAGES/guides/terms.po \
    docs-next/locale/ja/LC_MESSAGES/guides/privacy.po \
    triorb-amr-docs/docs/Terms.md triorb-amr-docs/docs/Terms.en.md \
    triorb-amr-docs/docs/PrivacyPolicy.md triorb-amr-docs/docs/PrivacyPolicy.en.md
# Handle v1.2.4 on master in its own session
git checkout master
# → commit the remaining working tree there
# Come back
git checkout docs2/phase2
git stash pop
# → commit these docs2 follow-ups
```

## 3. Open issue worked around during this session

**MyST-parser + Sphinx i18n drops translations for `## 1. Title` numbered H2**.
- Confirmed: `.mo` contains `"1. Scope" → "1. 適用範囲"`, `gettext.translation(...).gettext("1. Scope")` returns the JP correctly, yet Sphinx renders EN.
- Non-numbered headings (`## Scope`) translate correctly.
- Rosdoc2 labels ("Class Documentation" etc.) translate correctly.
- **Workaround applied**: stripped the numeric `N. ` prefix from Terms / Privacy H2 headings in both docs-next EN source and legacy JP/EN site.
- **Follow-up for root-cause fix**: reproduce minimally and file upstream issue (MyST-parser or sphinx-intl). Not urgent.

After the strip + `make update-po`, `sphinx-intl update` inherited the old
numbered translations as `fuzzy` attached to the new non-numbered msgids. The
filler script at `docs-next/_scripts/fill_translations.py` was updated to
**override fuzzy entries** and clear the flag.

## 4. Translation dictionary layout

- **D1 (hand-written pages)** — dicts in `docs-next/_scripts/fill_translations.py`
  (INDEX_MD_DICT, OVERVIEW_MD_DICT, HISTORY_MD_DICT, PKG_INDEX_DICT,
  VISUAL_SLAM_DICT) plus paragraph-aligned pairs from
  `triorb-amr-docs/docs/{Terms,PrivacyPolicy}.md`.
- **D2 (rosdoc2 common labels)** — ROSDOC2_LABEL_DICT in the same file; applied
  to all `docs-next/locale/ja/LC_MESSAGES/packages/**/*.po`.

## 5. Resume commands

```bash
# Shell prerequisites
source /nvme/home/tobeta/TriOrb-AMR-Documents/.venv-docs2/bin/activate
cd /nvme/home/tobeta/TriOrb-AMR-Documents/docs-next

# (Optional) rerun rosdoc2 full set — ~30 min on this box:
make rosdoc2             # → packages/_manifest.json, packages/<pkg>/…

# Extract + fill + compile JA translations:
make update-po           # runs gettext + sphinx-intl update + sphinx-intl build
python3 _scripts/fill_translations.py
sphinx-intl build -l ja  # recompile .mo after fill

# Builds (parallel):
make clean && make html     # EN, ~10 min
make html-ja                # JA, ~8 min

# Deploy-ready tree (strips .doctrees / _sources):
make deploy-stage           # → _build/deploy/{en,ja}/

# Preview:
cd _build/html/en && python3 -m http.server 18100 &
cd ../../html/ja && python3 -m http.server 18101 &

# Visual check:
python3 _shot.py            # → _shots/*.png
```

## 6. Known state of the last run (before handoff)

- `make html` (EN): last succeeded with **451 warnings** (cosmetic cross-package
  exhale label / C declaration collisions; suppressed where possible).
- `make html-ja` (JA): last succeeded with **568 warnings** (same pattern plus
  a few fuzzy-translation notices cleared after the fill fix).
- Deploy tree size: **EN 651 MB + JA 652 MB ≈ 1.3 GB total** after stripping.
- Package materialized count: **58 rosdoc2 + 1 hand-written (Visual SLAM) = 59**.

## 7. Next tasks (prioritized)

1. **Screenshot-verify the latest JA build**. Last shots in `_shots/` reflect
   the pre-strip state — regenerate before committing. (Preview servers were
   started on 18101 and killed mid-check.)
2. **Commit docs2 follow-ups** to `docs2/phase2`:
   - Makefile parallelism + `sphinx-intl build` hook
   - `_scripts/fill_translations.py` (new file + fuzzy-override fix)
   - Terms / Privacy (+ legacy .md) heading strip
   - Updated PO files for terms / privacy
3. **Handle v1.2.4 work on master** (separate session).
4. **CI smoke run**: push `docs2/phase2` to remote and confirm
   `.github/workflows/docs2.yml` fires.
5. **Phase 3 decision points** (memory: `project_docs2_migration.md`):
   - rosdoc2 package README translation policy (D3 scope)
   - Cross-package exhale label collision prefixing
   - Package-README per-page navigation size (still ~420 KB/page)

## 8. Where things live

```
docs-next/
├── HANDOFF.md                               ← this file
├── CI.md                                    ← CI design notes
├── README.md                                ← developer setup
├── conf.py                                  ← Sphinx + Furo + breathe + i18n
├── Makefile                                 ← html / html-ja / gettext / update-po / rosdoc2 / rosdoc2-image / deploy-stage
├── index.md                                 ← site root (EN source)
├── guides/{overview,history,terms,privacy}.md
├── _handwritten/packages/
│   ├── _categories.json                     ← handwritten → category mapping
│   └── visual_slam.md                       ← external-component stub
├── _templates/sidebar/language-switcher.html
├── _scripts/fill_translations.py            ← D1+D2 PO filler
├── docker/
│   ├── Dockerfile.rosdoc2                   ← ROS 2 Humble + rosdoc2
│   └── run_rosdoc2.sh                       ← auto-discover + colcon + rosdoc2 + host post-process
├── locale/ja/LC_MESSAGES/**.po              ← JA translations
├── packages/                                ← gitignored; rebuilt by `make rosdoc2`
│   ├── _manifest.json
│   ├── index.md                             ← category-grouped toctree
│   └── <pkg_name>/…
├── _rosdoc2_out/  _rosdoc2_sources/         ← gitignored intermediates
└── _build/  _shots/  .venv-docs2/           ← gitignored
.github/workflows/docs2.yml                  ← CI: build + artefact (no gh-pages yet)
```

Memory index: `~/.claude/projects/-nvme-home-tobeta-TriOrb-AMR-Documents/memory/MEMORY.md`.
