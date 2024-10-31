# Makefile commands to fast run

start: up logs

run: linter build up

rerun: down run

install:
	pip install poetry==1.8.4
	poetry install

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

linter: # correct path to virtual environment directory if needs
	@source .venv/bin/activate &&  pre-commit run --all-files

local-run:
	@source .venv/bin/activate && cd django_wallet/ && poetry run manage.py runserver

migrate:
	@source .venv/bin/activate && cd django_wallet/ && poetry run manage.py makemigrations && python manage.py migrate

test:
	@source .venv/bin/activate && cd django_wallet/ && poetry run manage.py test
