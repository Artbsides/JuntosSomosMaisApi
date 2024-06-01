.ONESHELL:

SHELL  = /bin/bash
PYTHON = /usr/bin/python3

PYTHON_VERSION = 3.12.3


-include .env
export


define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
    match = re.match(r'^([a-zA-Z_-]+):.*?## (.*?)(?: - (.*))?$$', line)
    if match:
        target, params, help = match.groups()
        target = target.ljust(19)
        params = params.ljust(59)
        print("  %s %s %s" % (target, params, help or ""))
endef
export PRINT_HELP_PYSCRIPT


MAKEFLAGS += --silent


help:
	@echo "Usage: make <option>"
	@echo "Options:"

	@$(PYTHON) -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


version:  ## Read or update api version - Parameters: update-to=[0-9].[0-9].[0-9]
	@poetry version $(if $(update-to), $(update-to), -s)

build: stop  ## Build dockerized images, run tests and code convention
	@docker-compose build

	@echo
	@docker-compose -f compose.yml -f compose.development.yml build

	@echo
	@$(MAKE) tests dockerized=true
	@$(MAKE) code-convention dockerized=true

dependencies:  ## Resolve dependencies for local development
	@poetry --version &> /dev/null || (pip3 install poetry && false) && \
		poetry config virtualenvs.in-project true

	@poetry install

tests: -B  ## Run dockerized tests - Parameters: dockerized=true, verbose=true
	DOCKER_COMPOSE=""

	@if [ "$(dockerized)" = "true" ]; then
		DOCKER_COMPOSE="docker-compose -f compose.yml -f compose.development.yml run --rm runner"
	fi

	$$DOCKER_COMPOSE poetry run pytest $(if $(filter "$(verbose)", "true"),-sxvv,)

code-convention:  ## Run dockerized code convention - Parameters: dockerized=true, fix-imports=true, github=true
	DOCKER_COMPOSE=""

	@if [ "$(dockerized)" = "true" ]; then
		DOCKER_COMPOSE="docker-compose -f compose.yml -f compose.development.yml run --rm runner"
	fi

	$$DOCKER_COMPOSE poetry run ruff check . $(if $(filter "$(github)", "true"),--output-format github,) && \
		$$DOCKER_COMPOSE poetry run isort $(if $(filter "$(fix-imports)", "true"),,--check) . -q

coverage:  ## Run dockerized tests and write reports - Parameters: dockerized=true
	DOCKER_COMPOSE=""

	@if [ "$(dockerized)" = "true" ]; then
		DOCKER_COMPOSE="docker-compose -f compose.yml -f compose.development.yml run --rm runner"
	fi

	$$DOCKER_COMPOSE poetry run pytest --cov-report=html:tests/reports

run:  ## Run dockerized api
	@APP_DEBUG="false" APP_ENVIRONMENT=production docker-compose up api --wait

run-terminal:  ## Run dockerized api terminal
	@docker-compose run --rm runner

run-debug:  ## Run dockerized api in the development environment
	@COMPOSE_DEVELOPMENT_COMMAND="python -m debugpy --listen ${APP_HOST}:5678 -m uvicorn api.main:app --host ${APP_HOST} --port ${APP_HOST_PORT} --reload" \
		docker-compose -f compose.yml -f compose.development.yml up api --wait

run-terminal-debug:  ## Run dockerized api terminal in the development environment
	@docker-compose -f compose.yml -f compose.development.yml run --rm runner

monitoring:  ## Run dockerized monitoring
	@docker-compose up -d prometheus grafana --wait

stop:  ## Stop dockerized api, terminal and monitoring
	@docker-compose down --volumes

github-tag:  ## Manage github tags - Parameters: action=create|delete, tag=[0-9].[0-9].[0-9]-staging|[0-9].[0-9].[0-9]
	@if [ "$(action)" = "create" ]; then
		git tag $(tag) && git push origin $(tag)
	elif [ "$(action)" = "uninstall" ]; then
		git tag -d $(tag) && git push origin :refs/tags/$(tag)
	else
		echo "==== Action not found"
	fi


%:
	@:
