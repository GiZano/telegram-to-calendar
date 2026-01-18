import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from .genai import get_calendar_json
from .calendar_service import add_event

### REPLY MESSAGES ###

menu = """
Sono il tuo Segretario, pronto ad accogliere ogni tua richiesta 🧐

Comandi disponibili:

- /start - Mostra questo menù

- /calendar_add (titolo - categoria - da inizio a fine) - Aggiungi nuovo evento al calendario
- /calendar_show X - Mostra i prossimi X eventi dai calendari disponibili

- (no comando) - Ripetere messaggio inviato (Troubleshooting)
"""

unknown_reply = """
Non conosco il comando specificato!
Digita /start per verificare i comandi disponibili
"""

# logging for troubleshooting
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

### BASIC HANDLERS ### 

# start handler function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # send menù message to user
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=menu
    )

# unknown command handler function
async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # tell the user the bot doesn't know the specified command
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=unknown_reply
    )

# no command handler function
async def no_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # reply with the same message sent by the user
    chat = update.effective_chat
    if chat:
        await context.bot.send_message(
            chat_id=chat.id,
            text=update.message.text
        )

### ADVANCED HANDLERS ###

async def calendar_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # add a new event to the calendar
    event_json = get_calendar_json(
        user_message=update.message.text
    )

    link = add_event(
        event_data=event_json
    )

    if link:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Evento aggiunto con successo al link: {link}"
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Errore, evento non aggiunto!"
        )

# create bot function
def start_bot():
    # create app
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # create and add /start handler to app
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # create and add /calendar_add handler to app
    calendar_add_handler = CommandHandler('calendar_add', calendar_add)
    application.add_handler(calendar_add_handler)

    # create and add unknown command handler to app
    unknown_command_handler = MessageHandler(filters.COMMAND, unknown_command)
    application.add_handler(unknown_command_handler)

    # create and add no commnad handler to app
    no_command_handler = MessageHandler(filters.TEXT, no_command)
    application.add_handler(no_command_handler)

    # start the application
    application.run_polling()