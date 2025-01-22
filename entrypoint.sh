#!/bin/bash
python manage.py migrate

# Запуск collectstatic
python manage.py collectstatic --noinput

# Запуск Daphne в фоновом режиме
daphne -b 0.0.0.0 -p 8080 starlingua.asgi:application &

# Запуск Celery worker
celery -A starlingua worker -l info &

# Запуск Celery Beat
celery -A starlingua beat -l info

# Поддерживаем скрипт в работающем состоянии
wait