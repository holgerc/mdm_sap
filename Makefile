# MDM SAP Makefile
.PHONY: help build up down logs shell migrate seed clean test

# Default target
help:
	@echo "MDM SAP - Available commands:"
	@echo ""
	@echo "  make build     - Build Docker images"
	@echo "  make up        - Start all services"
	@echo "  make down      - Stop all services"
	@echo "  make logs      - View logs"
	@echo "  make shell     - Open shell in backend container"
	@echo "  make seed      - Run database seeding"
	@echo "  make clean     - Remove all containers and volumes"
	@echo "  make test      - Run tests"
	@echo "  make pgadmin   - Start with PgAdmin"
	@echo ""

# Build Docker images
build:
	docker-compose build

# Start services
up:
	docker-compose up -d
	@echo ""
	@echo "Services started!"
	@echo "  - API: http://localhost:8000"
	@echo "  - API Docs: http://localhost:8000/api/v1/docs"
	@echo "  - Health: http://localhost:8000/api/v1/health"
	@echo ""

# Start with PgAdmin
pgadmin:
	docker-compose --profile tools up -d
	@echo ""
	@echo "Services started!"
	@echo "  - API: http://localhost:8000"
	@echo "  - PgAdmin: http://localhost:5050"
	@echo ""

# Stop services
down:
	docker-compose down

# View logs
logs:
	docker-compose logs -f

# Backend logs only
logs-backend:
	docker-compose logs -f backend

# Open shell in backend
shell:
	docker-compose exec backend /bin/bash

# Run database seeding
seed:
	docker-compose exec backend python /app/scripts/seed_data.py

# Run migrations (if using Alembic)
migrate:
	docker-compose exec backend alembic upgrade head

# Clean everything
clean:
	docker-compose down -v --remove-orphans
	docker system prune -f

# Run tests
test:
	docker-compose exec backend pytest -v

# Restart backend
restart:
	docker-compose restart backend

# Check status
status:
	docker-compose ps
