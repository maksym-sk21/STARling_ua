FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev

RUN pip install poetry==1.8.3

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY . .

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

EXPOSE 8080
EXPOSE 8443

CMD ["daphne", "-b", "0.0.0.0", "-p", "8080", "starlingua.asgi:application"]
