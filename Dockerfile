FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PROJECT_PATH /django_wallet

RUN apt-get update && apt-get install -y \
    netcat-traditional \
    pkg-config \
    default-libmysqlclient-dev  \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install poetry==1.8.4 && \
    poetry config virtualenvs.create false --local

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root

COPY ./django_wallet ./${PROJECT_PATH}
COPY ./scripts/* ./${PROJECT_PATH}

WORKDIR ${PROJECT_PATH}

EXPOSE ${API_PORT}
RUN chmod +x ./run.sh
