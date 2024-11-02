# Makefile commands to fast run

start: up logs

run: build migrate up

rerun: down run

check: linter test

install:
	pip install poetry==1.8.4
	poetry install


dev_install:
	pip install poetry==1.8.4
	poetry install --with dev


build:
	@docker compose build

up:
	@docker compose -f docker-compose.yml --env-file .env up

down:
	@docker compose down

stop:
	@docker compose stop

logs:
	@docker compose logs -f

linter: dev_install
	@pre-commit run --all-files

local-run:
	@source .venv/bin/activate && cd django_wallet/ && poetry run manage.py runserver

migrate:
	@source .venv/bin/activate && cd django_wallet/ && poetry run manage.py makemigrations && python manage.py migrate

test: dev_install
	@source .venv/bin/activate && source .env.test && cd django_wallet/ && pytest api/tests.py
