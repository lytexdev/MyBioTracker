.PHONY: help install build dev prod stop clean logs test

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt

build: ## Build the application
	@echo "Building MyBioTracker..."
	./build.sh

dev: ## Start development environment
	@echo "Starting development environment..."
	docker-compose -f docker-compose.dev.yml up --build

prod: ## Start production environment
	@echo "Starting production environment..."
	docker-compose up -d --build

stop: ## Stop all containers
	@echo "Stopping containers..."
	docker-compose down
	docker-compose -f docker-compose.dev.yml down

clean: ## Clean up containers, images, and volumes
	@echo "Cleaning up..."
	docker-compose down -v --remove-orphans
	docker-compose -f docker-compose.dev.yml down -v --remove-orphans
	docker system prune -f

logs: ## Show logs
	docker-compose logs -f

logs-dev: ## Show development logs
	docker-compose -f docker-compose.dev.yml logs -f

test: ## Run tests
	@echo "Running backend tests..."
	cd backend && python -m pytest
	@echo "Running frontend tests..."
	cd frontend && npm test

migrate: ## Run database migrations
	@echo "Running database migrations..."
	cd backend && alembic upgrade head

migration: ## Create new migration
	@echo "Creating new migration..."
	@read -p "Migration name: " name; \
	cd backend && alembic revision --autogenerate -m "$$name"

backup: ## Create backup
	@echo "Creating backup..."
	mkdir -p backups
	docker-compose exec app tar -czf - data/ > backups/mybiotracker-$(shell date +%Y%m%d-%H%M%S).tar.gz
	@echo "Backup created in backups/ directory"

restore: ## Restore from backup
	@echo "Available backups:"
	@ls -la backups/
	@read -p "Backup file: " file; \
	docker-compose exec -T app tar -xzf - < backups/$$file

setup: ## Initial setup
	@echo "Setting up MyBioTracker..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env file from .env.example"; \
		echo "Please edit .env with your configuration"; \
	fi
	@mkdir -p nginx/ssl
	@chmod +x build.sh
	@echo "Setup complete! Edit .env file and run 'make build' to build the application."

health: ## Check application health
	@echo "Checking application health..."
	@curl -f http://localhost/health || echo "Application is not responding"
