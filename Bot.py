from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext

TOKEN = '7012033090:AAE-fPMtlyaO2y5dXrrGSDaGK3G3B6YAYG4'
CHANNELS = ['https://t.me/onlinesavdo200k', 'https://t.me/onlineshop200k']  # Majburiy obuna kanallari
WELCOME_MESSAGE = "Assalomu alaykum! Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:"
SUBSCRIPTION_CONFIRMED_MESSAGE = "Obunani tasdiqladingiz! Iltimos, film uchun maxsus raqamni yuboring."
INVALID_SUBSCRIPTION_MESSAGE = "Obuna tasdiqlanmadi. Iltimos, yuqoridagi kanallarga obuna bo'ling."
FILMS = {
    '12345': 'URL_OR_PATH_TO_FILM_1',
    '67890': 'URL_OR_PATH_TO_FILM_2',
    # Yana boshqa filmlar uchun maxsus raqamlarni shu yerga qo'shing
}

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("Obunani tekshirish", callback_data='check_subscription')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(WELCOME_MESSAGE + '\n'.join(CHANNELS), reply_markup=reply_markup)

def check_subscription(update: Update, context: CallbackContext) -> None:
    user_id = update.callback_query.from_user.id
    for channel in CHANNELS:
        chat_member = context.bot.get_chat_member(chat_id=channel, user_id=user_id)
        if chat_member.status not in ['member', 'administrator', 'creator']:
            update.callback_query.message.reply_text(INVALID_SUBSCRIPTION_MESSAGE)
            return
    update.callback_query.message.reply_text(SUBSCRIPTION_CONFIRMED_MESSAGE)

def handle_film_code(update: Update, context: CallbackContext) -> None:
    film_code = update.message.text
    if film_code in FILMS:
        context.bot.send_document(chat_id=update.message.chat_id, document=FILMS[film_code])
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="Noto'g'ri kod kiritildi. Iltimos, yana bir bor tekshirib ko'ring.")

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(check_subscription, pattern='check_subscription'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_film_code))
    
    application.run_polling()

if __name__ == '__main__':
    main()
