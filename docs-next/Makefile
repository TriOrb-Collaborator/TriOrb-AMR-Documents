# Minimal Makefile for docs-next (Sphinx).
#
# English is the source language; Japanese is produced from PO translations
# in locale/ja/LC_MESSAGES/.
#
# Usage:
#   make html          # build English (default)
#   make html-ja       # build Japanese translation
#   make gettext       # extract translatable strings to _build/gettext/*.pot
#   make update-po     # refresh locale/ja PO files from latest POT
#   make serve         # local preview (English) on http://localhost:8000
#   make clean
#   make rosdoc2-image # build ROS 2 Humble + rosdoc2 docker image (one-time)
#   make rosdoc2       # regenerate packages/ via rosdoc2

SPHINXBUILD ?= sphinx-build
SOURCEDIR   := .
BUILDDIR    := _build
# Parallel read/write passes. Umbrella does NOT run exhale itself (rosdoc2
# produced the RST inside its container), so -j auto is safe.
# Override with SPHINXOPTS= on the make command line.
SPHINXOPTS  ?= -j auto

.PHONY: html html-ja gettext update-po serve clean rosdoc2 rosdoc2-image deploy-stage deploy-stage-local serve-deploy

# Phase 4 deploy layout. The release label also drives /v1.2.X/ path.
DOCS_RELEASE ?= v1.2.4

html:
	rm -rf "$(BUILDDIR)/html/en"
	$(SPHINXBUILD) $(SPHINXOPTS) -b html -D language=en "$(SOURCEDIR)" "$(BUILDDIR)/html/en"
	@# Strip rosdoc2's exhale `generated/` dirs right after build — they
	@# leak license-auth internals (ct.hpp, sha256.h). See deploy-stage.
	@find "$(BUILDDIR)/html/en/packages" -type d -name generated -prune -exec rm -rf {} + 2>/dev/null || true

html-ja:
	rm -rf "$(BUILDDIR)/html/ja"
	$(SPHINXBUILD) $(SPHINXOPTS) -b html -D language=ja "$(SOURCEDIR)" "$(BUILDDIR)/html/ja"
	@find "$(BUILDDIR)/html/ja/packages" -type d -name generated -prune -exec rm -rf {} + 2>/dev/null || true

gettext:
	$(SPHINXBUILD) $(SPHINXOPTS) -b gettext "$(SOURCEDIR)" "$(BUILDDIR)/gettext"
	@# B plan (Phase 4): rosdoc2-generated packages/** ship in English only.
	@# Drop the extracted POTs under packages/ so sphinx-intl update can't
	@# regenerate the corresponding PO tree.
	@rm -rf "$(BUILDDIR)/gettext/packages"

update-po: gettext
	sphinx-intl update -p "$(BUILDDIR)/gettext" -l ja
	sphinx-intl build -l ja
	@# Prune stale .mo / .po under packages/ in case they linger locally.
	@rm -rf locale/ja/LC_MESSAGES/packages

serve: html
	@echo "Open http://localhost:8000/"
	cd "$(BUILDDIR)/html/en" && python3 -m http.server 8000

clean:
	rm -rf "$(BUILDDIR)"

rosdoc2-image:
	docker build -t triorb-rosdoc2 -f docker/Dockerfile.rosdoc2 docker

rosdoc2:
	bash docker/run_rosdoc2.sh $(PKGS)

# Produce a deploy-ready tree under $(BUILDDIR)/deploy/ matching the Phase 4
# gh-pages layout:
#   _build/deploy/index.html          (version & language landing)
#   _build/deploy/$(DOCS_RELEASE)/en/ (Sphinx EN, stripped)
#   _build/deploy/$(DOCS_RELEASE)/ja/ (Sphinx JA, stripped)
# Past versions (v1.2.2, v1.2.3) are preserved in gh-pages by the deploy
# workflow (they are NOT staged here). Use deploy-stage-local to pull them
# from the local gh-pages branch for end-to-end preview.
#
# Stripped from each lang tree:
#   - .doctrees/   (Sphinx pickled AST cache, ~2 GB, only needed for incremental builds)
#   - _sources/    (copies of the input .rst files; users can get the real source from git)
#
# Assumes `make html` (and optionally `make html-ja`) have already run.
deploy-stage:
	rm -rf "$(BUILDDIR)/deploy"
	mkdir -p "$(BUILDDIR)/deploy/$(DOCS_RELEASE)"
	@for lang in en ja; do \
		if [ -d "$(BUILDDIR)/html/$$lang" ]; then \
			echo "staging $(DOCS_RELEASE)/$$lang..."; \
			rsync -a --delete \
				--exclude='.doctrees/' \
				--exclude='_sources/' \
				"$(BUILDDIR)/html/$$lang/" "$(BUILDDIR)/deploy/$(DOCS_RELEASE)/$$lang/"; \
		fi; \
	done
	@LAST_UPDATED_ISO=$$(date -u +"%Y-%m-%dT%H:%M:%SZ"); \
	LAST_UPDATED=$$(date -u +"%Y-%m-%d"); \
	sed -e "s|{{LAST_UPDATED_ISO}}|$$LAST_UPDATED_ISO|g" \
	    -e "s|{{LAST_UPDATED}}|$$LAST_UPDATED|g" \
	    _landing/index.html > "$(BUILDDIR)/deploy/index.html"
	@# Landing sibling assets (favicon, hero image, brand.css).
	@# Any non-index.html file under _landing/ is copied verbatim.
	@find _landing -maxdepth 1 -type f ! -name index.html \
	    -exec cp {} "$(BUILDDIR)/deploy/" \;
	@# brand.css is now bundled into Sphinx's build via `html_css_files`
	@# in conf.py. Every HTML already references it with a correct
	@# relative path (e.g., `../../_static/brand.css`) so it works under
	@# any URL prefix — no post-build injection needed.
	@# Strip the "README" anchor-only entries that rosdoc2 surfaces under
	@# each package in packages/index.html (Sphinx's `:titlesonly:` does
	@# not suppress them for H2 headings brought in via .. include ::).
	@PY=$$(command -v python3 || echo python3); \
	if [ -x ../.venv-docs2/bin/python3 ]; then PY=../.venv-docs2/bin/python3; fi; \
	for lang in en ja; do \
	    f="$(BUILDDIR)/deploy/$(DOCS_RELEASE)/$$lang/packages/index.html"; \
	    [ -f "$$f" ] && "$$PY" _scripts/strip_readme_anchors.py "$$f"; \
	done
	@# Scrub every HTML's left-sidebar so no stale README / Python API /
	@# Standard Documents entries survive an incremental rebuild. Safer
	@# than forcing a full rebuild, idempotent, runs in a few seconds.
	@PY=$$(command -v python3 || echo python3); \
	if [ -x ../.venv-docs2/bin/python3 ]; then PY=../.venv-docs2/bin/python3; fi; \
	"$$PY" _scripts/strip_sidebar_noise.py "$(BUILDDIR)/deploy/$(DOCS_RELEASE)"
	@# SECURITY + NOISE: rosdoc2's exhale-generated `generated/` directories
	@# expose private license-auth internals (ct.hpp, sha256.h) as source
	@# listings. They also dominate the sidebar with C++ file/class hierarchy
	@# noise. Strip them from every package tree under the deployed release.
	@# Also scrub references from package index.html so there are no broken
	@# links in the sidebar or content toctree.
	@find "$(BUILDDIR)/deploy/$(DOCS_RELEASE)" -type d -name generated -prune -exec rm -rf {} + 2>/dev/null || true
	@PY=$$(command -v python3 || echo python3); \
	if [ -x ../.venv-docs2/bin/python3 ]; then PY=../.venv-docs2/bin/python3; fi; \
	find "$(BUILDDIR)/deploy/$(DOCS_RELEASE)" -path '*/packages/*/index.html' -print0 \
	    | xargs -0 "$$PY" _scripts/strip_cpp_api_toctree.py 2>/dev/null || true
	@echo "deploy-ready tree: $(BUILDDIR)/deploy/"
	@du -sh "$(BUILDDIR)/deploy"/* 2>/dev/null | sort -h

# Local-preview-only: populate _build/deploy/ with v1.2.2, v1.2.3, and the
# shared mike assets (index.html is NOT overwritten — we keep our landing)
# using `git archive` on the gh-pages branch. Safe to run repeatedly.
deploy-stage-local: deploy-stage
	@REPO_ROOT=$$(git rev-parse --show-toplevel); \
	DEPLOY_ABS=$$(cd "$(BUILDDIR)/deploy" && pwd); \
	for v in v1.2.2 v1.2.3; do \
		echo "pulling $$v from gh-pages..."; \
		rm -rf "$$DEPLOY_ABS/$$v"; \
		git -C "$$REPO_ROOT" archive gh-pages "$$v" | tar -x -C "$$DEPLOY_ABS/"; \
	done; \
	echo "pulling shared mike assets from gh-pages..."; \
	for d in assets javascripts stylesheets search TriOrb-AMR-Package triorb-core; do \
		rm -rf "$$DEPLOY_ABS/$$d"; \
		git -C "$$REPO_ROOT" archive gh-pages "$$d" 2>/dev/null | tar -x -C "$$DEPLOY_ABS/" 2>/dev/null || true; \
	done
	@echo "local deploy preview ready: $(BUILDDIR)/deploy/"

# Serve the staged deploy tree (landing + all versions) on one origin so the
# language switcher's /ja/ <-> /en/ URL rewrite actually works.
serve-deploy:
	@test -d "$(BUILDDIR)/deploy" || { echo "run make deploy-stage (or deploy-stage-local) first"; exit 1; }
	@echo "Open http://localhost:18000/"
	cd "$(BUILDDIR)/deploy" && python3 -m http.server 18000
