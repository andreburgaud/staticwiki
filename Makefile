.DEFAULT_GOAL := help
MODULE := staticwiki
VERSION := $(shell echo `grep __version__ ${MODULE}/__init__.py | cut -d '"' -f 2`)

# twine installed globally
check:
	twine check dist/*

clean:
	find . -name '*.pyc' -delete || true
	find . -name '__pycache__' -type d | xargs rm -rf || true
	find . -name '.pytest_cache' -type d | xargs rm -rf || true
	rm *.bak || true
	rm -rf .cache build dist staticwiki.egg-info || true

# twine installed globally
deploy:
	twine upload dist/*

difflib: SHELL:=/bin/bash
difflib:
	diff -w <(pip-chill | grep -v ${MODULE}) <(cat requirements.txt)


dist: freeze version test clean wheel check

# black installed globally
fmt:
	black ${MODULE}

freeze:
	pip freeze | grep -v staticwiki > requirements.txt

help:
	@echo 'Makefile for StaticWiki ${VERSION} (Python static site generator)'
	@echo
	@echo 'Usage:'
	@echo '    make check         Check the wheel'
	@echo '    make clean         Delete temp files (*.pyc), caches (__pycache__)'
	@echo '    make deploy        Deploy package to the Cheese Shop (PyPI)'
	@echo '    make difflib       Identify differences between libraries installed and requirement.txt file'
	@echo '    make dist          Clean, generate the distribution and check'
	@echo '    make fmt           Format Python files using Black (installed globally)'
	@echo '    make freeze        Update the requirements.txt excluding local package (staticwiki)'
	@echo '    make help          Display this help message'
	@echo '    make lint          Lint Python file using Pylint (installed globally)'
	@echo '    make test          Execute tests'
	@echo '    make type          Type checking using Mypy (installed globally)'
	@echo '    make version       Display current package version'
	@echo '    make wheel         Build the wheel'

# pylint installed globally
lint:
	pylint ${MODULE}

tag:
	git push
	git tag -a ${VERSION} -m 'Version ${TAG}'
	git push --tags

test:
	pytest tests -vv

# mypy installed globally
type:
	mypy ${MODULE}

version:
	@echo '${MODULE} version: ${VERSION}'
	@perl -pi.bak -e 's/version="(\d+\.\d+\.\d+.*)"/version="${VERSION}"/' setup.py

wheel:
	python setup.py sdist bdist_wheel
