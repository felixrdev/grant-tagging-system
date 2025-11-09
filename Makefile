.PHONY: help dev build down test fmt lint typecheck clean install seed hooks

help:
	@echo "Available targets:"
	@echo "  make dev        - Start all services with Docker Compose"
	@echo "  make build      - Build Docker images"
	@echo "  make down       - Stop and remove containers"
	@echo "  make test       - Run all tests (backend + frontend)"
	@echo "  make fmt        - Format code (black/ruff + prettier)"
	@echo "  make lint       - Lint code (ruff + eslint)"
	@echo "  make typecheck  - Run TypeScript type checking"
	@echo "  make seed       - Seed database with sample data"
	@echo "  make clean      - Clean build artifacts and caches"
	@echo "  make install    - Install dependencies locally"
	@echo "  make hooks      - Install pre-commit hooks"

dev:
	docker compose up --build

build:
	docker compose build

down:
	docker compose down

test:
	@echo "Running backend tests..."
	cd backend && python -m pytest -v
	@echo "Running frontend build (no tests yet)..."
	cd frontend && pnpm build

fmt:
	@echo "Formatting backend code..."
	cd backend && black . && ruff check --fix .
	@echo "Formatting frontend code..."
	cd frontend && pnpm exec prettier --write "src/**/*.{ts,tsx,js,jsx,json,css,md}"

lint:
	@echo "Linting backend code..."
	cd backend && ruff check .
	@echo "Linting frontend code..."
	cd frontend && pnpm lint

typecheck:
	@echo "Running TypeScript type check..."
	cd frontend && pnpm exec tsc --noEmit

seed:
	@echo "Seeding database with sample grants..."
	cd backend && python scripts/seed.py

clean:
	@echo "Cleaning build artifacts..."
	cd backend && rm -rf __pycache__ .pytest_cache .ruff_cache *.egg-info || true
	cd backend && find . -type d -name "__pycache__" -exec rm -rf {} + || true
	cd frontend && rm -rf dist node_modules/.cache || true
	@echo "Clean complete!"

install:
	@echo "Installing frontend dependencies..."
	cd frontend && pnpm install
	@echo "Installing backend dependencies..."
	cd backend && pip install -e ".[dev]"

hooks:
	@echo "Installing pre-commit hooks..."
	pip install pre-commit
	pre-commit install
	@echo "Pre-commit hooks installed!"
