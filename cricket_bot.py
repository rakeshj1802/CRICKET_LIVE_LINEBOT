import requests
import time
import logging
from telegram import Bot
import asyncio

# Telegram Bot Credentials
BOT_TOKEN = "7721365750:AAGw66skneGqXXGy_B8xKoLiR8uDthayvrI"
CHANNEL_ID = "-1002481582963"  # Your Telegram Channel ID

# CricAPI Endpoint & API Key
CRICKET_API_URL = "https://api.cricapi.com/v1/currentMatches"
API_KEY = "733fc7f6-fc1b-46e6-8f67-d45a01d44a6a"

# Initialize bot
bot = Bot(token=BOT_TOKEN)
logging.basicConfig(level=logging.INFO)

# Store the last known scores to avoid duplicate messages
last_scores = {}

def get_cricket_updates():
    try:
        params = {"apikey": API_KEY}
        response = requests.get(CRICKET_API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return data.get("data", [])  # List of matches
    except Exception as e:
        logging.error(f"Error fetching cricket updates: {e}")
    return None

def format_message(matches):
    global last_scores
    new_messages = []

    for match in matches:
        match_id = match.get("id", "N/A")
        match_name = match.get("name", "N/A")
        status = match.get("status", "N/A")
        score = "N/A"
        
        if 'score' in match:
            score = f"{match['score'][0].get('runs', 'N/A')}/{match['score'][0].get('wickets', 'N/A')} in {match['score'][0].get('overs', 'N/A')} overs"
        
        # Check if score has changed
        if match_id not in last_scores or last_scores[match_id] != score:
            last_scores[match_id] = score
            new_messages.append(f"🏏 *{match_name}* 🏏\n*Status:* {status}\n*Score:* {score}\n")

    return new_messages

async def post_update():
    while True:
        matches = get_cricket_updates()
        new_messages = format_message(matches)

        if new_messages:
            for msg in new_messages:
                await bot.send_message(chat_id=CHANNEL_ID, text=msg, parse_mode="Markdown")
        
        await asyncio.sleep(300)  # Check every 5 minutes

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(post_update())
