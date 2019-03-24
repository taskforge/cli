##################
# USER VARIABLES #
##################

# You can set these variables from the command line

SPHINXOPTS			= 
SPHINXBUILD			= sphinx-build
DOC_SOURCEDIR		= docs
DOC_BUILDDIR		= build/docs
PYTHON				= python3
PIP					= $(PYTHON) -m pip
PYTEST				= PYTHONPATH="$$PYTHONPATH:src" $(PYTHON) -m pytest
PYTEST_OPTS			= --disable-pytest-warnings
DOCKER				= docker
SITE_PACKAGES		= $(shell python -c 'import sys; print([p for p in sys.path if "site-packages" in p][0])')
DEV_INSTALL_LINK	= $(SITE_PACKAGES)/taskforge-cli.egg-link
DOCS				= $(shell find src/docs -name '*.rst' -or -name '*.html' | grep -v 'cli/task_.*\.rst')
VALE				= $(DOCKER) run		\
	--rm -v $(PWD)/.vale/styles:/styles \
	--rm -v $(PWD):/docs				\
	-w /docs							\
	jdkato/vale


############
# BUILDING #
############

.PHONY: clean pydocstyle pylint lint lint-docs-validate-links \
	lint-docs-vale help livehtml docs

install-dev: $(DEV_INSTALL_LINK)
$(DEV_INSTALL_LINK):
	$(PIP) install --editable .
	$(PIP) install --editable ".[mongo]"
	$(PIP) install -r requirements.dev.txt

install:
	$(PYTHON) setup.py install

clean:
	rm -rf build dist
	rm -rf {} **/*.egg-info
	rm -f **/*.pyc

publish: docs wheel
	python setup.py sdist bdist_wheel
	twine upload dist/*


########
# DOCS #
########

docs: docs-html
	rm -rf docs/*
	mv build/docs/html/* docs/

# Build the website directory
website: install-dev clean html
	mkdir -p public
	cp -R docs/html/* public/
	cp src/docs/index.html public/index.html

# Build the web site container
docker-website: website
	docker build --no-cache \
		--tag "chasinglogic/taskforge.io:latest" \
		--file Dockerfile.website .

publish-website: website
	docker push "chasinglogic/taskforge.io:latest"

livehtml:
	sphinx-autobuild --watch ./src -b html $(SPHINXOPTS) "$(DOC_SOURCEDIR)" $(DOC_BUILDDIR)/html

docs-%:
	mkdir -p $(DOC_BUILDDIR)
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

pylint:
	$(PYTHON) -m pylint src tests

pydocstyle:
	$(PYTHON) -m pydocstyle src

lint: fmt pylint pydocstyle
	@echo "Ready to commit!"

fmt:
	$(PYTHON) -m isort --recursive src tests
	$(PYTHON) -m yapf --recursive -i src tests

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
