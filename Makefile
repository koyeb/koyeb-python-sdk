KOYEB_API ?= $(shell echo $${KOYEB_API:-https://api.prod.koyeb.com})
TEST_OPTS=-v -test.timeout 300s
GIT_USER_ID?=koyeb
GIT_REPO_ID?=koyeb-api-client-python
OPENAPI_GENERATOR_VERSION?=latest
PACKAGE_VERSION?=1.3.3


.PHONY: gen-api-client
gen-api-client:
	docker run --rm -v `pwd`/spec:/spec -v `pwd`:/builder openapitools/openapi-generator-cli:${OPENAPI_GENERATOR_VERSION} generate --git-user-id ${GIT_USER_ID} --git-repo-id ${GIT_REPO_ID} -i /spec/openapi.json -g python -o /builder --package-name koyeb.api --additional-properties packageVersion=${PACKAGE_VERSION} --additional-properties licenseInfo="Apache-2.0" --additional-properties generateSourceCodeOnly=true
	git checkout -- koyeb/__init__.py


.PHONY: gen-docs
gen-docs:
	./scripts/generate_docs.sh

.PHONY: format
format:
	black koyeb

.PHONY: fetch-spec
fetch-spec:
	curl -L -s $(KOYEB_API)/public.swagger.json > spec/openapi.json

test:
	python -m unitest
