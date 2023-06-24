.PHONY: test
test:
	pytest -s
	npm run test

.PHONY: build_webcomp
build_webcomp:
	cd webcomp && yarn clean && yarn build
	cp webcomp/dist/*.js src/webcomp.ts
	echo "// @ts-nocheck" > src/webcomp.tmp
	cat src/webcomp.ts >> src/webcomp.tmp
	mv src/webcomp.tmp src/webcomp.ts

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
	rm -rf dist
	rm -rf *.egg-info
	rm -rf webcomp/.parcel
	rm -rf webcomp/.parcel-cache

.PHONY: try-publish
try-publish:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: lint-fix
lint-fix:
	black ipylivebash