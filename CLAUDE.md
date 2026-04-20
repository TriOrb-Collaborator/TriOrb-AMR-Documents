# CLAUDE.md

Guidance for AI agents (Claude Code / similar) working in this repository.

## Two active doc pipelines — do not mix

This repo currently runs **two independent doc toolchains in parallel**.
Changesets must not cross between them.

| Pipeline | Source dirs | Branch for ongoing work | Output target |
| --- | --- | --- | --- |
| **v1.2.x (legacy, shipping)** | `triorb-amr-docs/`, `gather_md.py`, `submodules/*` | `master` | `gh-pages` via `mike` |
| **docs2 (Sphinx + rosdoc2)** | `docs-next/` | `docs2/phase2` | `gh-pages /v1.2.5/{en,ja}/` (Phase 4) |

Before editing anything, check `git branch --show-current` and confirm the
changeset belongs there. See `docs-next/HANDOFF.md` for the exact file split
when both streams have unstaged work at once.

## First read on resume

1. `docs-next/HANDOFF.md` — live state, open issues, resume commands.
2. `~/.claude/projects/-nvme-home-tobeta-TriOrb-AMR-Documents/memory/MEMORY.md`
   — project/decision memory across sessions.
3. `docs-next/README.md` / `docs-next/CI.md` — developer setup and CI design.

## Active gotchas

- **MyST + Sphinx i18n drops `## N. Title` numbered H2 translations.** Workaround
  in effect: strip numeric `N. ` prefix in source (EN) for Terms / Privacy. Do
  not re-introduce numbered H2 until upstream fix is confirmed.
- **`sphinx-intl update` marks renamed msgids as `fuzzy`.** The filler
  `docs-next/_scripts/fill_translations.py` overrides fuzzy entries and clears
  the flag — do not revert that behavior without reason.
- **Submodules (`submodules/TriOrb-AMR-Package`, `submodules/triorb-core`)
  belong to the v1.2.x pipeline.** Never bump them in a docs2 commit.

## Multi-agent orchestration

The user prefers delegation via sub-agents for anything that spans multiple
files or requires broad exploration. Use `Agent` (Explore / Plan / general)
for: code archaeology, cross-package sweeps, and long-running build verification.
Keep the main thread focused on synthesis and user-facing decisions.
