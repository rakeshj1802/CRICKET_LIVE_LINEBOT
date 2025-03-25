
import requests
import time
import logging
from telegram import Bot

# Telegram Bot Credentials
BOT_TOKEN = "7721365750:AAGw66skneGqXXGy_B8xKoLiR8uDthayvrI"
CHANNEL_ID = "-1002481582963"  # Replace with your channel ID

# Cricket API (Replace with a valid source)
CRICKET_API_URL = "https://www.cricketlineguru.com/"  # Placeholder
BOOKIE_API_URL = "https://www.southbook.in/"  # Placeholder

# Initialize bot
bot = Bot(token=BOT_TOKEN)
logging.basicConfig(level=logging.INFO)

def get_cricket_updates():
    try:
        response = requests.get(CRICKET_API_URL)
        if response.status_code == 200:
            return response.json()  # Adjust parsing as per actual API
    except Exception as e:
        logging.error(f"Error fetching cricket updates: {e}")
    return None

def get_bookie_ratings():
    try:
        response = requests.get(BOOKIE_API_URL)
        if response.status_code == 200:
            return response.json()  # Adjust parsing as per actual API
    except Exception as e:
        logging.error(f"Error fetching bookie ratings: {e}")
    return None

def format_message(cricket_data, bookie_data):
    message = "🏏 *Live Cricket Update* 🏏\n\n"
    if cricket_data:
        message += f"*Score:* {cricket_data.get('score', 'N/A')}\n"
        message += f"*Over:* {cricket_data.get('over', 'N/A')}\n"
        message += f"*Batsman:* {cricket_data.get('batsman', 'N/A')}\n"
        message += f"*Bowler:* {cricket_data.get('bowler', 'N/A')}\n"
    if bookie_data:
        message += f"\n🎰 *Bookie Ratings* 🎰\n"
        message += f"Odds: {bookie_data.get('odds', 'N/A')}\n"
    return message

def post_update():
    while True:
        cricket_data = get_cricket_updates()
        bookie_data = get_bookie_ratings()
        message = format_message(cricket_data, bookie_data)
        if message:
            bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="Markdown")
        time.sleep(5)  # Fetch every 5 seconds

if __name__ == "__main__":
    post_update()
