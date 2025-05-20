.PHONY: dev up down build rebuild logs clean test stage prod help

dev:
	@bash -c 'source scripts/load_env.sh dev && docker compose up'

up:
	@bash -c 'source scripts/load_env.sh dev && docker compose up -d'

down:
	@bash -c 'source scripts/load_env.sh dev && docker compose down'

build:
	@bash -c 'source scripts/load_env.sh dev && docker compose build'

rebuild:
	@bash -c 'source scripts/load_env.sh dev && docker compose build --no-cache'

logs:
	@bash -c 'source scripts/load_env.sh dev && docker compose logs -f'

clean:
	@bash -c 'source scripts/load_env.sh dev && docker compose down -v'
	@docker system prune -f

test:
	@bash -c 'source scripts/load_env.sh dev && docker compose run --rm core pytest core/ flow_engine/'

stage:
	@bash -c 'source scripts/load_env.sh stage && docker compose up -d'

prod:
	@bash -c 'source scripts/load_env.sh prod && docker compose up -d'

env_test:
	@bash -c 'source scripts/load_env.sh dev'

help:
	@echo "Available commands:"
	@echo "  make dev      - Start development environment"
	@echo "  make up       - Start services"
	@echo "  make down     - Stop services"
	@echo "  make build    - Build services"
	@echo "  make rebuild  - Rebuild services from scratch"
	@echo "  make logs     - View logs"
	@echo "  make clean    - Clean up containers and volumes"
	@echo "  make test     - Run tests (core and flow_engine)"
	@echo "  make lint     - Run linter (core, shared, and flow_engine)"
	@echo "  make stage    - Start stage environment"
	@echo "  make prod     - Start production environment"
	@echo "  make env-test - Load environment variables for testing"
