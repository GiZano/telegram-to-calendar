from dotenv import load_dotenv
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

menu = """
Sono il tuo Segretario, pronto ad accogliere ogni tua richiesta 🧐

Comandi disponibili:

/start - Avvia bot e mostra questo menù

"""

# load environment variables from .env file
load_dotenv()

# start handler function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # send message to user
    await context.bot.send_message(chat_id=update.effective_chat.id, text=menu)

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat:
        await context.bot.send_message(
            chat_id = chat.id,
            text = "Comando non riconosciuto. Per favore, usa /start per iniziare."
        )

async def any_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat:
        await context.bot.send_message(
            chat_id = chat.id,
            text = update.message.text
        )

# load telegram bot token from .env file
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

# logging for troubleshooting
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


if __name__ == '__main__':
    # create application
    application = ApplicationBuilder().token(bot_token).build()

    # create handler with (command, function) mapping
    start_handler = CommandHandler('start', start)
    # add handler to application
    application.add_handler(start_handler)

    # create and add handler for unknown commands
    unknown_command_handler = MessageHandler(filters.COMMAND, unknown_command)
    application.add_handler(unknown_command_handler)

    # create and add handlers for any text
    any_text_handler = MessageHandler(filters.TEXT, any_text)
    application.add_handler(any_text_handler)

    # start the application
    application.run_polling()