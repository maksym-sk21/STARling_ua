web: daphne -b 0.0.0.0 -p $PORT starlingua.asgi:application
bot: python manage.py telegram_bot
celery: celery -A starlingua worker --loglevel=info --concurrency=1
celery_beat: celery -A starlingua beat --loglevel=info
