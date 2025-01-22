from telegram import InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice, PreCheckoutQuery, Update
from django.core.management.base import BaseCommand
from telegram.ext import (
    Application,
    ChatMemberHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackContext,
    PreCheckoutQueryHandler,
    CallbackQueryHandler
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
from celery import shared_task


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = f"https://{os.getenv('DOMAIN_NAME')}/webhook/"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}"
PAYMENT_PROVIDER_TOKEN = os.getenv('PAYMENT_PROVIDER_TOKEN')

user_data = {}

application = Application.builder().token(TOKEN).build()


async def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    logger.info(f"Received /start command from {chat_id}")

    greeting_text = (
        "Привіт! Я бот школи Starlingua для нагадувань та оплати занять.\n"
        "Для реєстрації у боті та подальшого отримання нагадувань про заплановані уроки відправте команду /phone\n"
        "Команда /pay - для оплати уроків\n"
    )

    try:
        await context.bot.send_message(chat_id=chat_id, text=greeting_text)
    except Exception as e:
        logger.error(f"Error sending start message: {e}")


async def register_phone(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    logger.info(f"Received /phone command from {chat_id}")

    user_data[chat_id] = {"waiting_for_phone": True}

    try:
        await context.bot.send_message(chat_id=chat_id,
                                       text="Будь ласка, відправте мені номер телефону, який Ви зареєстрували на сайті.")
    except Exception as e:
        logger.error(f"Error sending phone registration message: {e}")


async def process_phone_number(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    phone_number = update.message.text

    if chat_id in user_data and user_data[chat_id].get("waiting_for_phone", False):
        try:
            student = await sync_to_async(Student.objects.get)(phone_number=phone_number)
            user_data[chat_id] = {"student_id": student.id}

            student.telegram_id = str(chat_id)
            await sync_to_async(student.save)()

            await update.message.reply_text(
                f"Дякуємо, {student.name}! Ваш номер телефону підтверджено. Тепер я буду відправляти вам нагадування."
            )

            user_data[chat_id]["waiting_for_phone"] = False

        except Student.DoesNotExist:
            await update.message.reply_text(
                "Такий номер телефону не зареєстрован. Будь ласка, спробуйте ще раз."
            )
    else:
        await update.message.reply_text("Невідома команда. Використовуйте /start, /pay або /phone.")


async def send_message(application: Application, chat_id, message):
    await application.bot.send_message(chat_id=chat_id, text=message)


async def choose_lesson_type(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    keyboard = [
        [InlineKeyboardButton("Індивідуальні", callback_data="individual")],
        [InlineKeyboardButton("Парні", callback_data="pair")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=chat_id, text="Оберіть тип занять:", reply_markup=reply_markup)


async def choose_language(update: Update, context: CallbackContext, lesson_type):
    chat_id = update.callback_query.message.chat_id

    keyboard = [
        [InlineKeyboardButton("Англійська", callback_data=f"{lesson_type}_english")],
        [InlineKeyboardButton("Німецька", callback_data=f"{lesson_type}_german")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=chat_id, text="Оберіть мову, за яку бажаєте заплатити:", reply_markup=reply_markup)

async def choose_number_of_lessons(update: Update, context: CallbackContext, language, lesson_type):
    chat_id = update.callback_query.message.chat_id

    keyboard = [
        [InlineKeyboardButton("1 урок", callback_data=f"{lesson_type}_{language}_1")],
        [InlineKeyboardButton("3 урока", callback_data=f"{lesson_type}_{language}_3")],
        [InlineKeyboardButton("5 уроків", callback_data=f"{lesson_type}_{language}_5")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=chat_id, text="Оберіть кількість уроків:", reply_markup=reply_markup)

async def send_invoice(update: Update, context: CallbackContext, language, lessons_count, lesson_type):
    chat_id = update.callback_query.message.chat_id
    title = f"Оплата за навчання ({language})"
    description = f"Оплата за {lessons_count} уроків ({language})"
    payload = f"Оплата {language} за {lessons_count} уроків"
    currency = "UAH"

    if lesson_type == "individual":
        price_per_lesson = 400 if language == "english" else 600
    else:
        price_per_lesson = 600 if language == "english" else 800

    total_amount = price_per_lesson * lessons_count

    prices = [LabeledPrice(f"{language} - {lessons_count} урок(ів)", total_amount * 100)]

    try:
        await context.bot.send_invoice(
            chat_id=chat_id,
            title=title,
            description=description,
            payload=payload,
            provider_token=PAYMENT_PROVIDER_TOKEN,
            currency=currency,
            prices=prices,
            start_parameter="payment-for-lessons",
        )
    except Exception as e:
        logger.error(f"Помилка при надсиланні рахунку: {e}")


async def handle_lesson_type_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    lesson_type = query.data
    logger.info(f"Selected lesson type: {lesson_type}")
    await choose_language(update, context, lesson_type)
    await query.answer()


async def handle_language_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    lesson_type, language = query.data.split("_")

    logger.info(f"Selected language: {language}, lesson type: {lesson_type}")
    await choose_number_of_lessons(update, context, lesson_type, language)
    await query.answer()


async def handle_lessons_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    lesson_type, language, lessons_count = query.data.split("_")
    lessons_count = int(lessons_count)
    logger.info(f"Selected {lessons_count} lessons for {language}")
    await send_invoice(update, context, language, lessons_count, lesson_type)
    await query.answer()

async def precheckout_callback(update: Update, context: CallbackContext):
    query = update.pre_checkout_query
    await query.answer(ok=True)

async def successful_payment_callback(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    await context.bot.send_message(chat_id=chat_id, text="Оплата пройшла успішно! Дякуємо за ваш платіж.")


@csrf_exempt
async def telegram_webhook(request):
    logger.info("Received a webhook request.")
    if request.method == "POST":
        try:
            update = Update.de_json(json.loads(request.body), application.bot)
            logger.info(f"Update received: {update}")

            user_id = update.callback_query.from_user.id if update.callback_query else update.message.from_user.id
            context = CallbackContext(application, user_id)

            if update.message and update.message.text:
                logger.info(f"Message received: {update.message.text}")
                if update.message.text.startswith("/start"):
                    await start(update, context)
                elif update.message.text.startswith("/pay"):
                    await choose_lesson_type(update, context)
                elif update.message.text.startswith("/phone"):
                    await register_phone(update, context)
                else:
                    await process_phone_number(update, context)
            elif update.callback_query:
                callback_data = update.callback_query.data

                data_parts = callback_data.split("_")

                if len(data_parts) == 1:
                    await handle_lesson_type_selection(update, context)
                elif len(data_parts) == 2:
                    await handle_language_selection(update, context)
                elif len(data_parts) == 3:
                    await handle_lessons_selection(update, context)
                else:
                    logger.warning(f"Unexpected callback data format: {callback_data}")
            elif update.pre_checkout_query:
                await precheckout_callback(update, context)
            elif update.message.successful_payment:
                await successful_payment_callback(update, context)

            return HttpResponse(status=200)

        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return HttpResponse(status=500)

    else:
        logger.warning("Received non-POST request.")
        return HttpResponse("Invalid request", status=400)


class Command(BaseCommand):
    help = 'Запуск Telegram-бота'

    def handle(self, *args, **kwargs):
        application.bot.set_webhook(WEBHOOK_URL)
        logger.info(f"Webhook set to: {WEBHOOK_URL}")

        application.add_handler(CommandHandler('start', start))
        application.add_handler(CommandHandler('pay', choose_language))
        application.add_handler(CommandHandler('phone', register_phone))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_phone_number))
        application.add_handler(CallbackQueryHandler(handle_lesson_type_selection, pattern='^(individual|pair)$'))
        application.add_handler(CallbackQueryHandler(handle_language_selection, pattern='^(individual|pair)_(english|german)$'))
        application.add_handler(CallbackQueryHandler(handle_lessons_selection, pattern='^(english|german)_(individual|pair)_[1-5]$'))
        application.add_handler(PreCheckoutQueryHandler(precheckout_callback))
