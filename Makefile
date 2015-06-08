APP=risno
VERSION=0.1.0

NO_COLOR=\033[0m
OK_COLOR=\033[32;01m
ERROR_COLOR=\033[31;01m
WARN_COLOR=\033[33;01m

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

all: help

help:
	@echo -e "$(OK_COLOR)==== $(APP) [$(VERSION)] ====$(NO_COLOR)"
	@echo -e "$(WARN_COLOR)- init               : Download dependencies used by Risno"
	@echo -e "$(WARN_COLOR)- build image=xxx    : Make the Docker image"
	@echo -e "$(WARN_COLOR)- publish image=xxx  : Publish the image to the Docker Hub"
	@echo -e "$(WARN_COLOR)- clean              : Cleanup environment"

machine-linux:
	@echo -e "$(OK_COLOR)[$(APP)] Installation Docker machine Linux $(NO_COLOR)"
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
init: machine-$(OS) compose-$(OS)

.PHONY: clean
clean:
	@rm ./docker-compose ./docker-machine

.PHONY: build
build:
	@echo -e "$(OK_COLOR)[$(APP)] Build $(NAMESPACE)/$(image):$(IMAGE_VERSION)$(NO_COLOR)"
	@$(DOCKER) build -t $(NAMESPACE)/$(image):$(IMAGE_VERSION) $(image)

.PHONY: publish
publish:
	@echo -e "$(OK_COLOR)[$(APP)] Publish $(NAMESPACE)/$(image):$(IMAGE_VERSION)$(NO_COLOR)"
	@$(DOCKER) push $(NAMESPACE)/$(image):$(IMAGE_VERSION)
