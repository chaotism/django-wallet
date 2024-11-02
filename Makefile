# Makefile commands to fast run

start: up logs

run: build migrate up

rerun: down run

check: linter test

install:
	pip install poetry==1.8.4
	poetry install --without dev


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
	@poetry run pre-commit run --all-files

local-run:
	@poetry run manage.py runserver

migrate:
	@poetry run manage.py makemigrations && poetry run manage.py migrate

test: dev_install
	@poetry run pytest django_wallet/api/tests.py


