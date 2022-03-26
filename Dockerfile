FROM python:3.9 as requirements-stage

WORKDIR /tmp

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.9

WORKDIR /code
RUN mkdir -p /code/data

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir --upgrade -r /code/requirements.txt

#COPY o365_token.txt /code
COPY ./src /code/src

EXPOSE 40052

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "40052"]