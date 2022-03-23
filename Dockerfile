FROM python:3.9 as requirements-stage

EXPOSE 40052

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.9

WORKDIR /code
RUN mkdir -p /code/data

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY o365_token.txt /code
COPY ./src /code/src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "40052"]














# FROM python:3.9
# # FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# EXPOSE 40052

# WORKDIR /tmp

# RUN pip install poetry

# COPY ./pyproject.toml ./poetry.lock* /tmp/

# RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# FROM python:3.9

# WORKDIR /code

# COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# COPY ./app /code/app

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]














# FROM python:3.9
# # FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# EXPOSE 40052

# WORKDIR /code

# ENV PYTHONFAULTHANDLER=1 \
#     PYTHONUNBUFFERED=1 \
#     PYTHONHASHSEED=random \
#     PYTHONDONTWRITEBYTECODE=1 \
#     # pip:
#     PIP_NO_CACHE_DIR=off \
#     PIP_DISABLE_PIP_VERSION_CHECK=on \
#     PIP_DEFAULT_TIMEOUT=100 \
#     # poetry:
#     POETRY_VERSION=1.1.13 \
#     POETRY_NO_INTERACTION=1 \
#     POETRY_CACHE_DIR='/var/cache/pypoetry' \
#     PATH="$PATH:/root/.local/bin"

# # install poetry
# # RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
# RUN pip install pipx
# RUN pipx install "poetry==$POETRY_VERSION"
# RUN pipx ensurepath

# # install dependencies
# COPY ./pyproject.toml /code
# # COPY ./pyproject.toml poetry.lock /code
# # RUN poetry install --no-dev --no-root --no-interaction --no-ansi
# RUN poetry install --no-dev --no-interaction --no-ansi

# # copy and run program
# COPY . /code
# CMD [ "poetry", "run", "dev" ]