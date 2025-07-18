import requests
import os

def send_telegram(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    return requests.post(url, json={"chat_id": chat_id, "text": message})

def send_whatsapp(message):
    # Replace with Twilio or Gupshup API
    return {"status": "not_implemented"}