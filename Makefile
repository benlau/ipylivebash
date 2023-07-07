.PHONY: test
test:
	pytest -s

.PHONY: build_webcomp
build_webcomp:
	cd webcomp && yarn clean && yarn build

.PHONY: build_js
build_js: build_webcomp
	yarn run build

.PHONY: build_package
build_package: build_webcomp
	yarn run build:prod
	python setup.py sdist bdist_wheel

.PHONY: clean
clean:
	rm -rf build
	rm -rf lib
	rm -rf dist
	rm -rf *.egg-info
	rm -rf webcomp/dist
	rm -rf webcomp/.parcel
	rm -rf webcomp/.parcel-cache

.PHONY: try-publish
try-publish:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: lint-fix
lint-fix:
	black ipylivebash
	cd webcomp && yarn run lint:fix