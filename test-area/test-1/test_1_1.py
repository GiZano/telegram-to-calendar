from dotenv import load_dotenv
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# load environment variables from .env file
load_dotenv()

# start handler function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Send welcome message to user
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="I'm your personal assistant, ready to help with your requests 🧐"
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

    # start the application
    application.run_polling()