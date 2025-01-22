#!/bin/bash
python manage.py migrate

python manage.py collectstatic --noinput

daphne -b 0.0.0.0 -p 8080 starlingua.asgi:application &

celery -A starlingua worker -l info &

celery -A starlingua beat -l info

wait
