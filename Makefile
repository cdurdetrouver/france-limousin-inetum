DOCKER_COMPOSE=docker compose
DOCKER_COMPOSE_FILE=docker-compose.yml

all: build start

build:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) build

start: build
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up

start-detach: build
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d

down:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down

rm:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down -v --rmi all --remove-orphans

clear-db: build
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec db sh -c "rm -rf /var/lib/postgresql/data/*"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down

backup:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d
	docker exec db sh -c 'exec mysqldump --databases wordpress -uwordpressuser -pwordpresspassword' > db_backup.sql
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down

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
	@echo "  clear-db			Clear the data from the db"

.PHONY: build start start-detach down rm help
