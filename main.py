"""
TODO: Put everything into a single project
TODO: Handler for messages without data
TODO: Handler without command
TODO: Command /calendar_add to add a new event
TODO: Command /calendar_delete to show next events 
TODO: Fix /start with all avaiable commands.
"""

import os
import logging
from dotenv import load_dotenv

from src import calendar_service 
from src import genai
from src import telegram_bot 

# Setup
load_dotenv()

def main():
    print("🚀 Avvio sistema...")

if __name__ == "__main__":
    main()