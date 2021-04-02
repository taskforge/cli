# system python interpreter. used only to create virtual environment
PY = python3
VENV = env
BIN=$(VENV)/bin

# make it work on windows too
ifeq ($(OS), Windows_NT)
    BIN=$(VENV)/Scripts
    PY=python
endif


all: lint test

$(VENV): requirements.txt requirements-dev.txt setup.py
	$(PY) -m venv $(VENV)
	$(BIN)/pip install --upgrade -r requirements.txt
	$(BIN)/pip install --upgrade -r requirements-dev.txt
	$(BIN)/pip install -e .
	touch $(VENV)

.PHONY: test
test: $(VENV)
	$(BIN)/pytest

.PHONY: lint
lint: $(VENV) format
	$(BIN)/flake8 src tests

.PHONY: format
format: $(VENV)
	$(BIN)/black src tests
	$(BIN)/isort src tests

.PHONY: release
release: $(VENV)
	$(BIN)/python setup.py sdist bdist_wheel
	twine upload dist/*

clean:
	rm -rf $(VENV)
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete
