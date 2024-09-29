from telegram import Update
from django.core.management.base import BaseCommand
from telegram.ext import (
    Application,
    ChatMemberHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackContext,
)
from students.models import Student
from schedule.models import Lesson
from datetime import datetime, timedelta
import logging
from asgiref.sync import sync_to_async
import os
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import asyncio


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = f"https://{os.getenv('DOMAIN_NAME')}/webhook/"

user_data = {}


async def start(update: Update, context: CallbackContext):
    logger.info(f"Received /start command from {update.effective_user.id}")
    chat_id = update.message.chat_id
    await update.message.reply_text("Привет! Отправь мне, пожалуйста, свой номер телефона, зарегистрированный в системе.")
    user_data[chat_id] = {"waiting_for_phone": True}


async def process_phone_number(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    phone_number = update.message.text

    if chat_id in user_data and user_data[chat_id].get("waiting_for_phone"):
        try:
            # Проверка, существует ли пользователь с таким email
            student = await sync_to_async(Student.objects.get)(phone_number=phone_number)
            user_data[chat_id] = {"student_id": student.id}  # Сохраняем ID студента для дальнейших напоминаний

            await update.message.reply_text(
                f"Спасибо, {student.name}! Ваш номер телефона подтвержден. Теперь я буду отправлять вам напоминания."
            )
        except Student.DoesNotExist:
            await update.message.reply_text(
                "Такой номер телефона не зарегистрирован. Пожалуйста, попробуйте ещё раз."
            )
    else:
        await update.message.reply_text("Сначала отправьте команду /start.")


async def remind_payment(application: Application):
    students = Student.objects.all()
    for student in students:
        remaining_hours = sum([turnover.remaining_hours for turnover in student.turnovers.all()])
        if remaining_hours <= 1:
            student_telegram_id = student.telegram_id
            if student_telegram_id:
                message = f"Привет, {student.name}! У тебя осталось {remaining_hours} оплаченных часов. Пожалуйста, пополни баланс."
                await send_message(application, student_telegram_id, message)


async def remind_lessons(application: Application):
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    lessons = Lesson.objects.filter(date=tomorrow)
    for lesson in lessons:
        student_telegram_id = lesson.student.telegram_id
        if student_telegram_id:
            message = f"Напоминание: У тебя завтра урок с {lesson.teacher.name} в {lesson.start_time}. Не забудь подготовиться!"
            await send_message(application, student_telegram_id, message)


async def send_message(application: Application, chat_id, message):
    await application.bot.send_message(chat_id=chat_id, text=message)


@csrf_exempt
def telegram_webhook(request):
    application = Application.builder().token(TOKEN).build()
    if request.method == "POST":
        update = Update.de_json(json.loads(request.body), application.bot)
        application.update_queue.put(update)
        return HttpResponse(status=200)
    else:
        return HttpResponse("Invalid request", status=400)


async def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_phone_number))

    webhook_url = WEBHOOK_URL
    await application.bot.set_webhook(webhook_url)

    await application.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv('PORT', '8443')),
        url_path="/webhook/",
        webhook_url=webhook_url
    )


class Command(BaseCommand):
    help = 'Запуск Telegram-бота'

    def handle(self, *args, **kwargs):
        asyncio.run(main())
