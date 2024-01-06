import logging

from django.conf import settings
from telegram.ext import (ApplicationBuilder, ContextTypes, CommandHandler,
                          MessageHandler, filters)

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

PHONE_BUTTON_TEXT = 'Подтвердить номер телефона'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton(PHONE_BUTTON_TEXT, request_contact=True)]],
        resize_keyboard=True
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Здравствуйте! Пожалуйста нажмите на эту кнопку для '
             'подтверждения номера телефона',
        reply_markup=keyboard
    )


async def handle_phone_number(update: Update,
                              context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    contact_info = update.message.contact

    if contact_info:
        phone_number = contact_info.phone_number
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Успешно подтвердили номер телефона!\n'
                 f'Спасибо, {user.first_name}!'
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Вы не подтвердили номер телефона.\n'
                 'Пожалуйста, подтвердите его для взаимодействия с сервисом'
        )


if __name__ == '__main__':
    application = ApplicationBuilder().token(settings.TG_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    phone_number_handler = MessageHandler(filters.CONTACT, handle_phone_number)
    application.add_handler(phone_number_handler)

    application.run_polling()
