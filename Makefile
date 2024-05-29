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


install: dependencies build tests code-convention  ## Install local api


dependencies:  ## Install dependencies
	@poetry --version &> /dev/null || (pip3 install poetry && false) && \
		poetry config virtualenvs.in-project true

	@poetry install

build: stop  ## Build docker images
	@docker-compose build

	@echo
	@docker-compose -f compose.yml -f compose.development.yml build

tests: -B  ## Run tests. verbose=true|false
	@poetry run pytest $(if $(filter "$(verbose)", "true"),-sxvv,)

code-convention:  ## Run code convention. fix-imports=true
	@poetry run ruff check -q api tests; \
		poetry run isort $(if $(filter "$(fix-imports)", "true"),,--check) . -q

coverage:  ## Run tests and write coverage html
	@poetry run pytest --cov-report=html:tests/reports

version:  ## Set package version. update-to=[0-9].[0-9].[0-9]
	@poetry version $(if $(update-to), $(update-to), -s)

run:  ## Run dockerized api or terminal. target=api|terminal
	@if [ "$(target)" = "api" ]; then
		APP_DEBUG="false" APP_ENVIRONMENT=production docker-compose up api --wait
	elif [ "$(target)" = "terminal" ]; then
		docker-compose run --rm runner
	else
		echo ==== Target not found.
	fi

run-debug:  ## Run dockerized development api or terminal. target=api|terminal
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

stop:  ## Stop api
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
