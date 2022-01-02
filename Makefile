.PHONY: test
test:
	poetry run pytest

.PHONY: build_package
build_package:
	yarn run build:prod
	python setup.py sdist bdist_wheel

.PHONY: clean
clean:
	rm -rf dist

.PHONY: try-publish
try-publish:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*