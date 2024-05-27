.ONESHELL:

SHELL  = /bin/bash
PYTHON = /usr/bin/python3

PYTHON_VERSION = 3.12.3

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


system-dependencies:
	@if [ "$(action)" = "install" ]; then
		sudo apt update &&
			sudo apt install build-essential curl file git

		/bin/bash -c "$$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)" &&
			echo -e '\neval $$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)' >> ~/.profile

		source ~/.profile &&
			brew install pyenv &&
			pyenv install $(PYTHON_VERSION) &&
			pyenv local $(PYTHON_VERSION) &&
			brew install poetry

	elif [ "$(action)" = "uninstall" ]; then
		pyenv local system

		brew uninstall poetry
		brew uninstall pyenv

		/bin/bash -c "$$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/uninstall.sh)" &&
			sed -i '/eval.*linuxbrew/d' ~/.profile

		sudo rm -rf /home/user/.pyenv
		sudo rm -rf /home/linuxbrew

		source /etc/environment

	else
		echo "==== Action not found"
	fi

project-dependencies:
	@if [ "$(action)" = "install" ]; then
		poetry install
	elif [ "$(action)" = "uninstall" ]; then
		sudo rm -rf .venv
	else
		echo "==== Action not found"
	fi

dependencies:  ## Install/Uninstall system and project dependencies. action=install|uninstall target=system|project
	@if [ "$(target)" = "system" -o "$(target)" = "project" ]; then
		$(MAKE) $(target)-dependencies
	else
		echo "==== Target not found";
	fi

tests: -B  ## Run tests. verbose=true
	@poetry run pytest $(if $(filter "$(verbose)", "true"),-sxvv,)

coverage:  ## Run tests and write coverage html
	@poetry run pytest --cov-report=html:tests/reports

code-convention:  ## Run code convention. fix-imports=true
	@poetry run ruff check -q api tests; \
		poetry run isort $(if $(filter "$(fix-imports)", "true"),,--check) . -q

build:  ## Generate build
	echo "..."

version:  ## Set package version. update-to=[0-9].[0-9].[0-9]
	@poetry version $(if $(update-to), $(update-to), -s)

github-tag:  ## Create or delete github tags. action=create|delete tag=[0-9].[0-9].[0-9]-development | [0-9].[0-9].[0-9]
	@if [ "$(action)" = "create" ]; then
		git tag $(tag) && git push origin $(tag)
	elif [ "$(action)" = "uninstall" ]; then
		git tag -d $(tag) && git push origin :refs/tags/$(tag)
	else
		echo "==== Action not found"
	fi


%:
	@:
