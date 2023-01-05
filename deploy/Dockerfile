FROM python:3.10.7-slim-buster

RUN apt-get update && apt-get -y install libpq-dev gcc
RUN pip install poetry==1.2.2

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

RUN poetry install

COPY . /app/src/
RUN poetry install

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
