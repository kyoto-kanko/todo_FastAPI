FROM python:3.9-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /src

RUN pip install poetry

# https://python-poetry.org/
COPY pyproject.toml* poetry.lock* ./

# poetryでライブラリをインストール (pyproject.tomlが既にある場合)
RUN poetry config virtualenvs.in-project true
RUN if [ -f pyproject.toml ]; then poetry install; fi

ENTRYPOINT ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--reload"]

# 新しいパッケージをインスールした場合は以下のコマンドでパッケージを更新
# docker-compose build --no-cache
