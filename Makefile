.PHONY: install run lint format test migrate docker-up docker-down

install:
	poetry install
	poetry run pre-commit install

run:
	poetry run uvicorn backend.app.main:app --reload

lint:
	poetry run ruff check .
	poetry run mypy .

format:
	poetry run black .
	poetry run ruff check --fix .

test:
	poetry run pytest

migrate:
	poetry run alembic upgrade head

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down
