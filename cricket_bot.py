import requests
import time
import logging
from telegram import Bot

# Enable logging
logging.basicConfig(level=logging.INFO)

# Telegram Bot Token and Channel ID
TELEGRAM_BOT_TOKEN = "7721365750:AAGw66skneGqXXGy_B8xKoLiR8uDthayvrI"
TELEGRAM_CHANNEL_ID = "-1002481582963"

# CricAPI Key & URL
API_KEY = "733fc7f6-fc1b-46e6-8f67-d45a01d44a6a"
URL = f"https://api.cricapi.com/v1/cricScore?apikey={API_KEY}"

# Initialize Telegram Bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Function to fetch live IPL scores
def get_live_ipl_scores():
    try:
        response = requests.get(URL)
        
        # Handle request errors
        if response.status_code != 200:
            logging.error(f"HTTP Error: {response.status_code}")
            return None

        data = response.json()
        
        # Check if data is present
        if "data" not in data:
            logging.error("Invalid API Response")
            return None

        messages = []  # Store messages to send to Telegram
        for match in data["data"]:
            if match.get("matchType") == "t20" and "IPL" in match.get("series", ""):
                match_info = (
                    f"🏏 *{match['t1']} vs {match['t2']}*\n"
                    f"📊 Score: {match.get('t1s', 'N/A')} - {match.get('t2s', 'N/A')}\n"
                    f"⏳ Status: {match['status']}"
                )
                messages.append(match_info)

        return messages if messages else ["No live IPL matches found."]

    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None

# Function to send message to Telegram
def send_to_telegram(messages):
    for message in messages:
        try:
            bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=message, parse_mode="Markdown")
            logging.info("Message sent successfully.")
        except Exception as e:
            logging.error(f"Failed to send message: {e}")

# Main Loop: Fetch and Send Live Scores Every 5 Minutes
if __name__ == "__main__":
    while True:
        scores = get_live_ipl_scores()
        if scores:
            send_to_telegram(scores)
        time.sleep(300)  # Wait 5 minutes before checking again
