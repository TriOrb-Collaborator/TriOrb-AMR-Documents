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

.PHONY: html html-ja gettext update-po serve clean rosdoc2 rosdoc2-image deploy-stage

html:
	$(SPHINXBUILD) -b html -D language=en "$(SOURCEDIR)" "$(BUILDDIR)/html/en"

html-ja:
	$(SPHINXBUILD) -b html -D language=ja "$(SOURCEDIR)" "$(BUILDDIR)/html/ja"

gettext:
	$(SPHINXBUILD) -b gettext "$(SOURCEDIR)" "$(BUILDDIR)/gettext"

update-po: gettext
	sphinx-intl update -p "$(BUILDDIR)/gettext" -l ja

serve: html
	@echo "Open http://localhost:8000/"
	cd "$(BUILDDIR)/html/en" && python3 -m http.server 8000

clean:
	rm -rf "$(BUILDDIR)"

rosdoc2-image:
	docker build -t triorb-rosdoc2 -f docker/Dockerfile.rosdoc2 docker

rosdoc2:
	bash docker/run_rosdoc2.sh $(PKGS)

# Produce a deploy-ready tree under $(BUILDDIR)/deploy/ that strips
# build-only artefacts:
#   - .doctrees/   (Sphinx pickled AST cache, ~2 GB, only needed for incremental builds)
#   - _sources/    (copies of the input .rst files; users can get the real source from git)
# Assumes `make html` (and optionally `make html-ja`) have already run.
deploy-stage:
	rm -rf "$(BUILDDIR)/deploy"
	mkdir -p "$(BUILDDIR)/deploy"
	@for lang in en ja; do \
		if [ -d "$(BUILDDIR)/html/$$lang" ]; then \
			echo "staging $$lang..."; \
			rsync -a --delete \
				--exclude='.doctrees/' \
				--exclude='_sources/' \
				"$(BUILDDIR)/html/$$lang/" "$(BUILDDIR)/deploy/$$lang/"; \
		fi; \
	done
	@echo "deploy-ready tree: $(BUILDDIR)/deploy/"
	@du -sh "$(BUILDDIR)/deploy"/* 2>/dev/null | sort -h
