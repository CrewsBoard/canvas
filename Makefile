.PHONY: dev up down build rebuild logs clean test stage prod help

dev:
	@source scripts/load_env.sh dev && docker compose up

up:
	@source scripts/load_env.sh dev && docker compose up -d

down:
	@source scripts/load_env.sh dev && docker compose down

build:
	@source scripts/load_env.sh dev && docker compose build

rebuild:
	@source scripts/load_env.sh dev && docker compose build --no-cache

logs:
	@source scripts/load_env.sh dev && docker compose logs -f

clean:
	@source scripts/load_env.sh dev && docker compose down -v
	@docker system prune -f

test:
	@source scripts/load_env.sh dev && docker compose run --rm core pytest core/ flow_engine/

stage:
	@source scripts/load_env.sh stage && docker compose up -d

prod:
	@source scripts/load_env.sh prod && docker compose up -d

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