import requests
import time
import logging
from telegram import Bot

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Telegram Bot Credentials
TELEGRAM_BOT_TOKEN = "7721365750:AAGw66skneGqXXGy_B8xKoLiR8uDthayvrI"
TELEGRAM_CHANNEL_ID = "-1002481582963"

# Cricket API Credentials
API_URL = "https://cricket-live-line1.p.rapidapi.com/home"
HEADERS = {
    "x-rapidapi-key": "7cf2d66dfcmshdb2e3038cee6474p13fa3ajsn8f43f7bc4ddd",
    "x-rapidapi-host": "cricket-live-line1.p.rapidapi.com"
}

# Initialize Telegram bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

def get_live_matches():
    """Fetch live match data from the API."""
    try:
        response = requests.get(API_URL, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            logging.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None

def send_telegram_message(message):
    """Send a message to the Telegram channel."""
    try:
        bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=message)
        logging.info("Message sent successfully!")
    except Exception as e:
        logging.error(f"Failed to send message: {e}")

def process_live_matches():
    """Fetch and send live cricket match updates to Telegram."""
    matches = get_live_matches()
    
    if not matches:
        send_telegram_message("⚠ No live matches found or API error occurred.")
        return
    
    match_list = matches.get("data", [])
    if not match_list:
        send_telegram_message("⚠ No live matches available at the moment.")
        return

    for match in match_list:
        match_message = (
            f"🏏 *Live Match Update*\n"
            f"📢 {match.get('matchTitle', 'Unknown Match')}\n"
            f"📅 Date: {match.get('date', 'N/A')}\n"
            f"🏟 Venue: {match.get('venue', 'N/A')}\n"
            f"🔴 Status: {match.get('matchStatus', 'N/A')}\n"
            f"🏆 Series: {match.get('series', 'N/A')}\n"
        )
        send_telegram_message(match_message)

if __name__ == "__main__":
    logging.info("Cricket bot started...")
    while True:
        process_live_matches()
        time.sleep(60)  # Fetch updates every 60 seconds
