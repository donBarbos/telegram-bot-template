.DEFAULT_GOAL:=help

.PHONY: default deps up down stop kill build ps exec logs mm migrate downgrade check format clean backup mount-docker-backup restore extract update compile babel

LOCALES = bot/locales

help:
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

deps:
	@poetry install --no-root

up:
	docker compose up -d

down:
	docker compose down

stop:
	docker compose stop

kill:
	docker compose kill

build:
	docker compose build

ps:
	docker compose ps

exec:
	docker compose exec app $(args)

logs:
	docker compose logs $(args) -f

# MIGRATIONS
mm:
	docker compose exec bot alembic revision --autogenerate -m "$(args)"

migrate:
	docker compose exec bot alembic upgrade head

downgrade:
	docker compose exec bot alembic downgrade $(args)

# STYLE
check:
	@poetry run ruff check .
	@poetry run ruff format --check .

format:
	@poetry run ruff check --fix .
	@poetry run ruff format .

clean:
	@rm -rf .pytest_cache .ruff_cache .hypothesis build/ -rf dist/ .eggs/ .coverage coverage.xml coverage.json htmlcov/ .mypy_cache
	@find . -name '*.egg-info' -exec rm -rf {} +
	@find . -name '*.egg' -exec rm -f {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -rf {} +
	@find . -name '.pytest_cache' -exec rm -rf {} +
	@find . -name '.ipynb_checkpoints' -exec rm -rf {} +

# BACKUPS
backup:
	docker compose exec bot scripts/postgres/backup

mount-docker-backup:
	docker cp app_db:/backups/$(args) ./$(args)

restore:
	docker compose exec app_db scripts/postgres/restore $(args)

# I18N
extract:
	@poetry run pybabel extract --input-dirs=. -o $(LOCALES)/messages.pot

update:
	@poetry run pybabel update -d $(LOCALES) -i $(LOCALES)/messages.pot

compile:
	@poetry run pybabel compile -d $(LOCALES)

babel: extract update
