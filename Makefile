APP_NAME = jyflow

.PHONY: install build test lint docker-build docker-run clean help

install:
	poetry install

build:
	poetry build

test:
	poetry run pytest

lint:
	poetry run ruff check jyflow/ --fix
	poetry run mypy --check-untyped-defs --ignore-missing-imports jyflow/

docker-build:
	docker build -t $(APP_NAME):latest .

docker-run:
	docker run --rm $(APP_NAME):latest

clean:
	rm -rf dist/ build/ *.egg-info

help:
	@echo "Available targets:"
	@echo "  install        Install dependencies"
	@echo "  build          Build the package"
	@echo "  test           Run tests"
	@echo "  lint           Run code linting"
	@echo "  type-check     Run type checks"
	@echo "  docker-build   Build the Docker image"
	@echo "  docker-run     Run the Docker container"
	@echo "  clean          Clean build artifacts"
