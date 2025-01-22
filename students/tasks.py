from celery import shared_task
from turnover.models import Client
from schedule.models import Lesson
from datetime import datetime, timedelta
import os
import requests
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

@shared_task
def remind_payment():
    logger.info("Начало выполнения задачи отправки напоминаний.")
    clients = Client.objects.all()
    for client in clients:
        remaining_hours = client.remaining_hours
        cache_key = f'payment_reminder_sent_{client.id}'
        reminder_sent = cache.get(cache_key)
        if remaining_hours <= 1 and not reminder_sent:
            student_telegram_id = client.turnover.student.telegram_id
            if student_telegram_id:
                message = f"Нагадування: У тебе залишилось {remaining_hours} оплачених годин. Будь ласка, оплатіть подальше навчання."
                send_message(student_telegram_id, message)
                cache.set(cache_key, True, timeout=7 * 24 * 60 * 60)
                logger.info("Задача отправки напоминаний завершена.")

@shared_task
def remind_lessons():
    logger.info("Начало выполнения задачи отправки напоминаний.")
    today = datetime.now().date()
    lessons = Lesson.objects.filter(date=today)
    for lesson in lessons:
        student_telegram_id = lesson.student.telegram_id
        if student_telegram_id:
            message = f"Нагадування: У тебе сьогодні урок з {lesson.teacher.name} о {lesson.start_time}. Не забудь підготуватись!"
            send_message(student_telegram_id, message)
            logger.info("Задача отправки напоминаний завершена.")


@shared_task
def update_payment(client_id):
    client = Client.objects.get(id=client_id)
    cache_key = f'payment_reminder_sent_{client.id}'
    cache.delete(cache_key)
    logger.info(f"Статус напоминания об оплате для клиента {client.turnover.student.name} сброшен.")


def send_message(chat_id, message):
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise Exception(f"Error sending message: {response.text}")
