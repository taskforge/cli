##################
# USER VARIABLES #
##################

# You can set these variables from the command line

VERSION = $(shell git tag --list | tail -n1 | sed s/v//)
PROJECT = taskforge

PYTHON				= python3
PIP					= $(PYTHON) -m pip
PYTEST				= PYTHONPATH="$$PYTHONPATH:src" $(PYTHON) -m pytest
PYTEST_OPTS			= --disable-pytest-warnings
DOCKER				= docker
SITE_PACKAGES		= $(shell $(PYTHON) -c 'import sys; print([p for p in sys.path if "site-packages" in p][0])')
DEV_INSTALL_LINK	= $(SITE_PACKAGES)/taskforge-cli.egg-link
DOCS				= $(shell find docs -name '*.rst' -or -name '*.html' | grep -v 'cli/task_.*\.rst')
VALE				= $(DOCKER) run		\
	--rm -v $(PWD)/.vale/styles:/styles \
	--rm -v $(PWD):/docs				\
	-w /docs							\
	jdkato/vale


SPHINXOPTS			= 
SPHINXBUILD			= sphinx-build
BUILDDIR            = build
DIST_TARBALL        = dist/$(PROJECT)-cli-$(VERSION).tar.gz     

DEB_ORIG_TARBALL    = ../$(PROJECT)_$(VERSION).orig.tar.gz
DEB_MAN_PAGES_DIR   = debian/taskforge/usr/share/man/man1

WEBSITE_DEPLOY_DIR  = /var/www/html
WEBSITE_DEPLOY_PORT = 22
WEBSITE_DEPLOY_USER = deploy
WEBSITE_HOSTNAME    = taskforge.io
DOC_SOURCEDIR		= docs
DOC_BUILDDIR		= $(BUILDDIR)/docs

MAN_PAGES = $(DOC_BUILDDIR)/man/task.1 \
			$(DOC_BUILDDIR)/man/task-add.1 \
			$(DOC_BUILDDIR)/man/task-complete.1 \
			$(DOC_BUILDDIR)/man/task-edit.1 \
			$(DOC_BUILDDIR)/man/taskforged.1 \
			$(DOC_BUILDDIR)/man/task-next.1 \
			$(DOC_BUILDDIR)/man/task-query.1 \
			$(DOC_BUILDDIR)/man/task-todo.1 \
			$(DOC_BUILDDIR)/man/task-workon.1
MAN_PAGES_GZ = $(addsuffix .gz,$(MAN_PAGES))

WEBSITEDIR          = $(BUILDDIR)/website/public


############
# BUILDING #
############

.PHONY: clean pydocstyle pylint lint lint-docs-validate-links \
	lint-docs-vale help livehtml docs dist lint-and-test

lint-and-test: lint test-all

install-dev: $(DEV_INSTALL_LINK)
$(DEV_INSTALL_LINK):
	$(PIP) install --editable .
	$(PIP) install -r requirements/dev.txt

install:
	$(PYTHON) setup.py install

clean:
# Clean up python dist and test directories
	rm -rf $(BUILDDIR) dist $(WEBSITEDIR)
	rm -rf {} **/*.egg-info
	rm -f **/*.pyc
	rm -f ../$(PROJECT)_$(VERSION).tar.gz
	rm -rf .pytest_cache
	rm -f $(DEV_INSTALL_LINK)

# Cleanup debian packaging output
	rm -rf debian/.debhelper debian/debhelper-build-stamp .pybuild debian/taskforge
	rm -f $(DEBIAN_ORIG_TARBALL) \
		../taskforge_$(VERSION).dsc \
		../taskforge_$(VERSION)_source* \
		../taskforge_$(VERSION).tar.xz \
		../taskforge_$(VERSION).debian.tar.xz \
		../taskforge_$(VERSION).orig.tar.gz \
		../taskforge_$(VERSION)*.deb

#############
# PACKAGING #
#############

$(DIST_TARBALL):
	VERSION=$(VERSION) python setup.py sdist bdist_wheel
pkg-pypi: $(DIST_TARBALL)

pkg-pypi-upload: docs pkg-pypi 
	twine upload dist/*

$(DEB_ORIG_TARBALL): $(DIST_TARBALL)
	cp $(DIST_TARBALL) $(DEB_ORIG_TARBALL)
$(DEB_MAN_PAGES): $(MAN_PAGES_GZ)
pkg-deb: $(MAN_PAGES_GZ) $(DEB_ORIG_TARBALL)
	mkdir -p $(DEB_MAN_PAGES_DIR)
	cp $(MAN_PAGES_GZ) $(DEB_MAN_PAGES_DIR)
	debuild \
		-I \
		-I"tests/*" \
		-I"docs/*" \
		-I"build/*" \
		-I"dist/*" \
		-I".pytest_cache/*" \
		-I"requirements/dev.txt" \
		-I"requirements.txt" \
		-I"Makefile" \
		-I"pytest.ini" \
		-I".gitignore" \
		-I"Dockerfile.website" \
		-I".pylintrc" \
		-I".travis.yml" \
		-I".vale/*" \
		-I".vale.ini" \
		-I"debian/*" \
		-I".benchmarks/*" \
		-I".github/*" \
		-i'(\.pytest_cache|\.benchmarks|debian|.*taskforge_cli\.egg-info|\.git|\.github|tests|\.vale|dist|docs)/.*|\.gitignore|Dockerfile.*|\.pylintrc|\.travis\.yml|\.vale\.ini|requirements.*\.txt|setup\.cfg|Makefile|pytest\.ini'	

########
# DOCS #
########

docs: docs-html docs-man

# Build the website directory
website: install-dev clean docs-html
	mkdir -p $(WEBSITEDIR)/docs
	cp -R $(DOC_BUILDDIR)/html/* $(WEBSITEDIR)/docs
	cp $(DOC_SOURCEDIR)/index.html $(WEBSITEDIR)/index.html

# Build the web site container
docker-website: website
	docker build --no-cache \
		--tag "chasinglogic/taskforge.io:latest" \
		--file Dockerfile.website .

publish-website: website
	rsync -e "ssh -p $(WEBSITE_DEPLOY_PORT)" -avz build/website/public/* $(WEBSITE_DEPLOY_USER)@$(WEBSITE_HOSTNAME):$(WEBSITE_DEPLOY_DIR)/$(WEBSITE_HOSTNAME)/

docs-live-%:
	sphinx-autobuild --watch ./src -b $* $(SPHINXOPTS) "$(DOC_SOURCEDIR)" $(DOC_BUILDDIR)/html

$(DOC_BUILDDIR):
	mkdir -p $(DOC_BUILDDIR)

$(MAN_PAGES): docs-man
$(MAN_PAGES_GZ): $(MAN_PAGES)
%.1.gz:
	gzip --force --keep $*.1
docs-%: $(DOC_BUILDIR)
	$(SPHINXBUILD) -M $* "$(DOC_SOURCEDIR)" "$(DOC_BUILDDIR)" $(SPHINXOPTS) $(O)

###########
# LINTING #
###########

lint-docs-vale:
	$(VALE) --glob='!docs/cli/task_*.rst' $(DOCS)

lint-docs-validate-links:
	$(DOCKER) run --name taskforge_link_validation -p 8080:80 -d chasinglogic/taskforge.io:latest
	pylinkvalidate.py -P http://localhost:8080
	$(DOCKER) stop taskforge_link_validation

lint-docs: lint-docs-vale lint-docs-validate-links

mypy:
	$(PYTHON) -m mypy src

pylint:
	$(PYTHON) -m pylint --rcfile=setup.cfg src
	$(PYTHON) -m pylint --rcfile=tests/.pylintrc tests

pydocstyle:
	$(PYTHON) -m pydocstyle src

lint: fmt pylint pydocstyle mypy
	@echo "Ready to commit!"

black-check:
	$(PYTHON) -m black --check src tests

isort-check:
	$(PYTHON) -m isort --check-only --recursive src tests

fmt:
	$(PYTHON) -m isort --recursive src tests
	$(PYTHON) -m black src tests

###########
# TESTING #
###########

test: test-not-slow

test-all:
	$(PYTEST) $(PYTEST_OPTS)

test-coverage:
	$(PYTEST) $(PYTEST_OPTS) -m 'not benchmark' \
		--cov-report term-missing --cov=task_forge

test-not-%:
	$(PYTEST) $(PYTEST_OPTS) -m "not $*"

test-%:
	$(PYTEST) $(PYTEST_OPTS) -m "$*"
