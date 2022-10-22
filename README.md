<h1 align="center"><em>Telegram bot.</em></h1>

<p align="center">
<a href="https://github.com/donBarbos/telegram-bot-template/actions/workflows/checks.yml"><img src="https://img.shields.io/github/workflow/status/donBarbos/telegram-bot-template/Checks?label=checks&style=plastic" alt="Checking Status"></a>
<a href="https://github.com/donBarbos/telegram-bot-template/actions/workflows/docker-image.yml"><img src="https://img.shields.io/github/workflow/status/donBarbos/telegram-bot-template/Docker%20Image%20CI?label=docker%20image&style=plastic" alt="Docker Build Status"></a>
<a href="https://www.python.org/downloads"><img src="https://img.shields.io/badge/Python-3.7%2B-blue?style=plastic" alt="Python"></a>
<a href="https://github.com/donBarbos/telegram-bot-template/blob/master/LICENSE"><img src="https://img.shields.io/github/license/donBarbos/telegram-bot-template?style=plastic" alt="License"></a>
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=plastic" alt="Code style"></a>
<p>


## 🚀 Getting Started

### Running on Local Machine

- install dependencies using [Poetry](https://python-poetry.org "python package manager")
    ```
    poetry install
    ```
- configure environment variables in `.env` file

- start bot in virtual environment
    ```
    poetry run python -m bot
    ```

### Launch in Docker

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


## 🌍 Environment variables

| variables         | description |
|:-----------------:| ----------- |
| `BOT_TOKEN`       | Telegram bot API token |
| `PG_HOST`         | hostname or an IP address PostgreSQL database |
| `PG_NAME`         | the name of the PostgreSQL database |
| `PG_PASSWORD`     | password used to authenticate |
| `PG_PORT`         | connection port number (defaults to 5432 if not provided) |
| `PG_USER`         | the username used to authenticate |
| `REDIS_HOST`      | hostname or an IP address Redis database |
| `REDIS_PASSWORD`  | Redis database password, empty by default |
| `REDIS_PORT`      | port from Redis database |

> *I use Redis for Finite State Machine, and PostgreSQL as Database*


## 🔧 Tech Stack

- `aiogram` — asynchronous framework for Telegram Bot API
- `asyncpg` — asynchronous PostgreSQL database client library
- `poetry` — development workflow
- `loguru` — third party library for logging in Python
- `docker` — to automate deployment
- `postgres` — powerful, open source object-relational database system
- `redis` — an in-memory data structure store


## 👷🏾 Contributing

First off, thanks for taking the time to contribute! Contributions are what makes the open-source community such an amazing place to learn, inspire, and create. Any contributions you make will benefit everybody else and are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!

1. `Fork` this repository
2. Create a `branch`
3. `Commit` your changes
4. `Push` your `commits` to the `branch`
5. Submit a `pull request`



## 📝 License

Distributed under the GPL-3.0 license. See `LICENSE` for more information.


## 📢 Contact

[donbarbos](https://github.com/donBarbos): donbarbos@proton.me
