import logging
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from obr1 import process_texts

TEXT_INPUT, CHOICE = range(2)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
texts = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global texts
    texts = []
    await update.message.reply_text(
        "Привет! Пожалуйста, введите ваш текст одним сообщением. Когда закончите, напишите /done."
    )
    return TEXT_INPUT

async def text_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global texts
    texts.append(update.message.text)
    return TEXT_INPUT

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global texts
    await update.message.reply_text("Пожалуйста, подождите, идет обработка вашего запроса...")
    loop = asyncio.get_running_loop()
    words_count_list, words_importance_list, wc_counts_path, wc_importance_path = await loop.run_in_executor(
        None, process_texts, texts
    )
    context.user_data['words_count_list'] = words_count_list
    context.user_data['words_importance_list'] = words_importance_list
    context.user_data['wc_counts_path'] = wc_counts_path
    context.user_data['wc_importance_path'] = wc_importance_path
    reply_keyboard = [['По количеству', 'По важности']]
    await update.message.reply_text(
        "Выберите один из вариантов:",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return CHOICE

async def choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    if choice == 'По количеству':
        words_count_list = context.user_data['words_count_list']
        text = "Список слов по количеству:\n"
        for phrase, count in words_count_list:
            text += f"{phrase}: {count}\n"
        await update.message.reply_text(text)
        await update.message.reply_photo(open(context.user_data['wc_counts_path'], 'rb'))
    elif choice == 'По важности':
        words_importance_list = context.user_data['words_importance_list']
        text = "Список слов по важности:\n"
        for phrase, score in words_importance_list:
            text += f"{phrase}: {score}\n"
        await update.message.reply_text(text)
        await update.message.reply_photo(open(context.user_data['wc_importance_path'], 'rb'))
    else:
        await update.message.reply_text("Пожалуйста, выберите 'По количеству' или 'По важности'")
        return CHOICE
    await update.message.reply_text(
        "Если хотите обработать ещё текст, то пришлите его полностью одним сообщением. Когда закончите, напишите /done."
    )
    global texts
    texts = []
    return TEXT_INPUT

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Разговор завершён. Чтобы начать заново, введите /start')
    return ConversationHandler.END

def main():
    application = ApplicationBuilder().token('7864209032:AAEvcpTnsVBDDtz30NrmCxS7sisPDcf4J-U').build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            TEXT_INPUT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, text_input),
                CommandHandler('done', done)
            ],
            CHOICE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, choice)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()
