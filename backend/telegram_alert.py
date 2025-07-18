from telegram import Bot
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN is missing. Check your .env file or deployment environment.")

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def send_forecast_alert(user_id, message):
    bot.send_message(chat_id=user_id, text=message)

