FROM python:3.10.5-slim

EXPOSE 8081/tcp

WORKDIR /usr/src/app
COPY . .

RUN apt update && \
    apt install --no-install-recommends -y build-essential curl && \
    /usr/local/bin/python -m pip install --upgrade pip && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    export PATH="/root/.local/bin:$PATH" && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev && \
    poetry cache clear --no-interaction --all pypi && \
    curl -sSL https://install.python-poetry.org | python3 - --uninstall && \
    apt-get -y remove build-essential curl && apt-get -y autoremove --purge && apt-get -y clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /var/cache/apt

ENTRYPOINT ["python", "-m", "bot"]
