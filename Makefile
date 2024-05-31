.ONESHELL:

SHELL  = /bin/bash
PYTHON = /usr/bin/python3

PYTHON_VERSION = 3.12.3


-include .env
export


define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("	%-18s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT


MAKEFLAGS += --silent


help:
	@echo "Usage  : make <command>"
	@echo "Options:"

	@$(PYTHON) -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


install: build tests code-convention  ## Build dockerized images, run tests and code convention


dependencies:  ## Install api dependencies for local development
	@poetry --version &> /dev/null || (pip3 install poetry && false) && \
		poetry config virtualenvs.in-project true

	@poetry install

build: stop  ## Build dockerized images
	@docker-compose build

	@echo
	@docker-compose -f compose.yml -f compose.development.yml build

tests: -B  ## Run dockerized tests. verbose=true|false
	@docker-compose -f compose.yml -f compose.development.yml run --rm runner \
		poetry run pytest $(if $(filter "$(verbose)", "true"),-sxvv,)

code-convention:  ## Run dockerized code convention. fix-imports=true
	@docker-compose -f compose.yml -f compose.development.yml run --rm runner \
		poetry run ruff check -q api tests; \
		poetry run isort $(if $(filter "$(fix-imports)", "true"),,--check) . -q

	echo ==== No errors found.

coverage:  ## Run dockerized tests and write reports
	@docker-compose -f compose.yml -f compose.development.yml run --rm runner \
		poetry run pytest --cov-report=html:tests/reports

version:  ## Set the package version. update-to=[0-9].[0-9].[0-9]
	@poetry version $(if $(update-to), $(update-to), -s)

run:  ## Run dockerized api or terminal. target=api|terminal
	@if [ "$(target)" = "api" ]; then
		APP_DEBUG="false" APP_ENVIRONMENT=production docker-compose up api --wait
	elif [ "$(target)" = "terminal" ]; then
		docker-compose run --rm runner
	else
		echo ==== Target not found.
	fi

run-debug:  ## Run dockerized api or terminal in the development environment. target=api|terminal
	@if [ "$(target)" = "api" ]; then
		COMPOSE_DEVELOPMENT_COMMAND="python -m debugpy --listen ${APP_HOST}:${APP_DEBUG_PORT} -m uvicorn api.main:app --host ${APP_HOST} --port ${APP_HOST_PORT} --reload" \
			docker-compose -f compose.yml -f compose.development.yml up api --wait
	elif [ "$(target)" = "terminal" ]; then
		docker-compose -f compose.yml -f compose.development.yml run --rm runner
	else
		echo ==== Target not found.
	fi

monitoring:  ## Run dockerized monitoring
	@docker-compose up -d prometheus grafana --wait

stop:  ## Stop dockerized api, terminal and monitoring
	@docker-compose down --volumes

github-tag:  ## Manage github tags. action=create|delete tag=[0-9].[0-9].[0-9]-staging | [0-9].[0-9].[0-9]
	@if [ "$(action)" = "create" ]; then
		git tag $(tag) && git push origin $(tag)
	elif [ "$(action)" = "uninstall" ]; then
		git tag -d $(tag) && git push origin :refs/tags/$(tag)
	else
		echo "==== Action not found"
	fi


%:
	@:
