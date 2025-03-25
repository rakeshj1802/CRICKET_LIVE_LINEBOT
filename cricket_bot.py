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
    if not matches:
        return "🏏 No live matches available right now."

    message = "🏏 *Live Cricket Updates* 🏏\n\n"
    for match in matches[:2]:  # Limit to 2 matches to keep messages short
        message += f"*Match:* {match.get('name', 'N/A')}\n"
        message += f"*Status:* {match.get('status', 'N/A')}\n"
        if 'score' in match:
            message += f"*Score:* {match['score'][0].get('runs', 'N/A')}/{match['score'][0].get('wickets', 'N/A')} in {match['score'][0].get('overs', 'N/A')} overs\n"
        message += "\n"
    return message

async def post_update():
    while True:
        matches = get_cricket_updates()
        message = format_message(matches)
        await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="Markdown")
        await asyncio.sleep(1)  # Update every 5 minutes

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(post_update())
