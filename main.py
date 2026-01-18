import os
import logging
from dotenv import load_dotenv

# Setup
load_dotenv()

from src import telegram_bot as tgb

def main():
    print("Avvio sistema...")

    tgb.start_bot()

if __name__ == "__main__":
    main()