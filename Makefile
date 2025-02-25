DOCKER_COMPOSE=docker-compose
DOCKER_COMPOSE_FILE=docker-compose.yml

all: build start

build:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) build

start:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up

start-detach:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d

down:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down

rm:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down -v --rmi all --remove-orphans

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  all			Build and start the application"
	@echo "  build			Build the application"
	@echo "  start			Start the application in dev mode"
	@echo "  start-detach	Start the application in detach mode"
	@echo "  down			Stop the application"
	@echo "  rm			Stop the application and remove volumes and images"

.PHONY: build start start-detach down rm help
