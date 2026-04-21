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
	$(SPHINXBUILD) $(SPHINXOPTS) -b html -D language=en "$(SOURCEDIR)" "$(BUILDDIR)/html/en"

html-ja:
	$(SPHINXBUILD) $(SPHINXOPTS) -b html -D language=ja "$(SOURCEDIR)" "$(BUILDDIR)/html/ja"

gettext:
	$(SPHINXBUILD) $(SPHINXOPTS) -b gettext "$(SOURCEDIR)" "$(BUILDDIR)/gettext"

update-po: gettext
	sphinx-intl update -p "$(BUILDDIR)/gettext" -l ja
	sphinx-intl build -l ja

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
	@# Landing sibling assets (favicon, hero image). Any non-index.html file
	@# under _landing/ is copied verbatim.
	@find _landing -maxdepth 1 -type f ! -name index.html \
	    -exec cp {} "$(BUILDDIR)/deploy/" \;
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
