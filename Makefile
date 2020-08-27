.PHONY: dist
PIPVERSION=$(shell cat stackable/VERSION | sed 's/-//')

test:
	python -m unittest

dist:
	: "run setup.py sdist bdist_wheel"
	rm -rf ./dist/*
	rm -rf ./build/*
	python setup.py sdist bdist_wheel
	twine check dist/stackable-${PIPVERSION}-py3-none-any.whl


release-test: dist
	: "twine upload to pypi test"
	# see https://packaging.python.org/tutorials/packaging-projects/
	# config is in $HOME/.pypirc
	twine upload --repository testpypi dist/*
	pip install -U --index-url https://test.pypi.org/simple/ stackable
	pip install -e .

release-prod: test dist
	: "twine upload to pypi prod"
	# see https://packaging.python.org/tutorials/packaging-projects/
	# config is in $HOME/.pypirc
	twine upload --repository pypi dist/*
	pip install --force-reinstall -U stackable==${PIPVERSION}
	pip install -e .
