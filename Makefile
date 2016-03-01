APP=risno
VERSION=0.1.0


SHELL = /bin/bash

NO_COLOR=\033[0m
OK_COLOR=\033[32;01m
ERROR_COLOR=\033[31;01m
WARN_COLOR=\033[33;01m

MAKE_COLOR=\033[33;01m%-20s\033[0m

DOCKER_MACHINE_URI=https://github.com/docker/machine/releases/download
DOCKER_MACHINE_VERSION=v0.2.0

DOCKER_COMPOSE_URI=https://github.com/docker/compose/releases/download
DOCKER_COMPOSE_VERSION=1.2.0

DOCKER = docker
COMPOSE = ./compose
MACHINE = ./machine

NAMESPACE="risno"

UNAME := $(shell uname)
ifeq ($(UNAME),$(filter $(UNAME),Linux Darwin))
ifeq ($(UNAME),$(filter $(UNAME),Darwin))
OS=darwin
else
OS=linux
endif
else
OS=windows
endif

.DEFAULT_GOAL := help

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(MAKE_COLOR) : %s\n", $$1, $$2}'

machine-linux:
	@echo "$(OK_COLOR)[$(APP)] Installation Docker machine Linux $(NO_COLOR)"
	@wget $(DOCKER_MACHINE_URI)/$(DOCKER_MACHINE_VERSION)/docker-machine_linux-amd64 -O docker-machine
	@chmod +x ./docker-machine

machine-darwin:
	@echo -e "$(OK_COLOR)[$(APP)] Installation Docker machine OSX $(NO_COLOR)"
	@wget $(DOCKER_MACHINE_URI)/$(DOCKER_MACHINE_VERSION)/docker-machine_darwin-amd64 -O docker-machine
	@chmod +x ./docker-machine

machine-windows:
	@echo -e "$(OK_COLOR)[$(APP)] Installation Docker machine Windows $(NO_COLOR)"
	@wget $(DOCKER_MACHINE_URI)/$(DOCKER_MACHINE_VERSION)/docker-machine_windows-amd64.exe -O docker-machine
	@chmod +x ./docker-machine

compose-linux:
	@echo -e "$(OK_COLOR)[$(APP)] Installation Docker compose Linux $(NO_COLOR)"
	@wget $(DOCKER_COMPOSE_URI)/$(DOCKER_COMPOSE_VERSION)/docker-compose-Linux-x86_64 -O docker-compose
	@chmod +x ./docker-compose

compose-darwin:
	@echo -e "$(OK_COLOR)[$(APP)] Installation Docker compose $(NO_COLOR)"
	@wget $(DOCKER_COMPOSE_URI)/$(DOCKER_COMPOSE_VERSION)/docker-compose-Darwin_x86-64 -O docker-compose
	@chmod +x ./docker-compose

.PHONY: init
init: machine-$(OS) compose-$(OS) ## Install Docker tools

.PHONY: clean
clean: ## Cleanup repository
	@rm ./docker-compose ./docker-machine
