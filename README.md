<h1 align="center"><em>Telegram bot.</em></h1>

<p align="center">
<a href="https://github.com/DONSIMON92/telegram-bot-template/actions/workflows/checks.yml"><img src="https://img.shields.io/github/workflow/status/DONSIMON92/telegram-bot-template/Tests?style=plastic" alt="Testing Status"></a>
<a href="https://www.python.org/downloads"><img src="https://img.shields.io/badge/Python-3.7%2B-blue?style=plastic" alt="Python"></a>
<a href="https://github.com/DONSIMON92/telegram-bot-template/blob/master/LICENSE"><img src="https://img.shields.io/github/license/DONSIMON92/telegram-bot-template?style=plastic" alt="License"></a>
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=plastic" alt="Code style"></a>
<p>

# Installation

## Running on Local Machine

- install dependencies using [Poetry](https://python-poetry.org "python package manager")
    ```
    poetry install
    ```
- configure environment variables in `.env` file

- start bot in virtual environment
    ```
    poetry run python -m bot
    ```

## Launch in Docker

- configure environment variables in `.env` file

- start virtual environment
    ```
    poetry shell
    ```
- building the docker image
    ```
    docker-compose build
    ```
- start service
    ```
    docker-compose up -d
    ```

# Environment variables

- `BOT_TOKEN` — Telegram bot token
- `PG_HOST` — hostname or an IP address PostgreSQL database
- `PG_NAME` — the name of the PostgreSQL database
- `PG_PASSWORD` — password used to authenticate
- `PG_PORT` — connection port number (defaults to 5432 if not provided)
- `PG_USER` — the username used to authenticate
- `REDIS_HOST` — hostname or an IP address Redis database 
- `REDIS_PASSWORD` — Redis database password, empty by default
- `REDIS_PORT` — port from Redis database

> *I use Redis for Finite State Machine, and PostgreSQL as Database*

# Tech Stack

- `aiogram` — asynchronous framework for Telegram Bot API
- `asyncpg` — asynchronous PostgreSQL database client library
- `poetry` — development workflow
- `loguru` — third party library for logging in Python
- `docker` — to automate deployment
- `postgres` — powerful, open source object-relational database system
- `redis` — an in-memory data structure store
