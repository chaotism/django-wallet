# django-wallet

## Task

```text
Task:
Develop REST API server using django-rest-framework with pagination, sorting and filtering for two models:

Transaction (id, wallet_id (fk), txid, amount);

Wallet (id, label, balance);

Where txid is required unique string field, amount is a number with 18-digits precision, label is a string field, balance is a summary of all transactions’s amounts. Transaction amount may be negative. Wallet balance should NEVER be negative

Tech Stack:

Python – 3.11+
Database – mysql
API specification – JSON:API — A specification for building APIs in JSON (you are free to use plugin https://django-rest-framework-json-api.readthedocs.io/en/stable/)

Will be your advantage:

Test coverage
SQLAlchemy migrations is an option
Any linter usage
Quick start app guide if you create your own docker-compose or Dockerfiles
Comments in non-standart places in code
Use database indexes if you think it's advisable
Leave github link to repo. Please delete the repo after HR feedback

[execution time limit] 4 seconds (sh)

[memory limit] 1 GB
```

## Task

```text
Improvement: By adding a transaction status, we can achieve a transaction outbox pattern and avoid the need to calculate the balance immediately. (alternative is using https://github.com/juntossomosmais/django-outbox-pattern)
Improvement: It will be possible to migrate to Saga pattern in the future
Improvement: Mark the object as deleted when deleting it instead of actually deleting it
Improvement: Use Library for SQLAlchemy integration like https://django-sorcery.readthedocs.io/en/latest/ or https://github.com/aldjemy/aldjemy
Improvement: Migrate to an onion structure project like my previous one https://github.com/chaotism/sbersupermarket-product-scraper
Improvement: use Multi-stage builds
Improvement: use pytests fixtures for wallet and transactions
Improvement: add mypy and sonar-qube checks, migrate to ruff
Improvement: migrate to async
```

## Prerequisites
Before running this project you should have installed linux environment with the following software:

- Git
- Docker
- Docker-compose
- GNU Make
- python 3.13

## Installation

Install django-wallet with pip

```bash
pip install django-wallet
```
