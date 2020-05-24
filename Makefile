##################
# USER VARIABLES #
##################

# You can set these variables from the command line

VERSION = $(shell git tag --list | tail -n1 | sed s/v//)

PYTHON				= python3
PIP					= $(PYTHON) -m pip
PYTEST				= PYTHONPATH="$$PYTHONPATH:src" $(PYTHON) -m pytest
PYTEST_OPTS			= --disable-pytest-warnings
SITE_PACKAGES		= $(shell $(PYTHON) -c 'import sys; print([p for p in sys.path if "site-packages" in p][0])')
DEV_INSTALL_LINK	= $(SITE_PACKAGES)/taskforge-cli.egg-link
BUILDDIR            = build
DIST_TARBALL        = dist/$(PROJECT)-cli-$(VERSION).tar.gz

DEB_ORIG_TARBALL    = ../$(PROJECT)_$(VERSION).orig.tar.gz
DEB_MAN_PAGES_DIR   = debian/taskforge/usr/share/man/man1

############
# BUILDING #
############

.PHONY: clean pydocstyle flake8 lint lint-docs-validate-links \
	lint-docs-vale help livehtml docs dist lint-and-test

lint-and-test: lint test-all

install-dev: $(DEV_INSTALL_LINK)
$(DEV_INSTALL_LINK):
	$(PIP) install --editable .
	$(PIP) install -r requirements-dev.txt

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
		-I".flake8" \
		-I".travis.yml" \
		-I".vale/*" \
		-I".vale.ini" \
		-I"debian/*" \
		-I".benchmarks/*" \
		-I".github/*" \
		-i'(\.pytest_cache|\.benchmarks|debian|.*taskforge_cli\.egg-info|\.git|\.github|tests|\.vale|dist|docs)/.*|\.gitignore|Dockerfile.*|\.flake8rc|\.travis\.yml|\.vale\.ini|requirements.*\.txt|setup\.cfg|Makefile|pytest\.ini'

###########
# LINTING #
###########

flake8:
	$(PYTHON) -m flake8

pydocstyle:
	$(PYTHON) -m pydocstyle src

lint: fmt flake8 pydocstyle
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
