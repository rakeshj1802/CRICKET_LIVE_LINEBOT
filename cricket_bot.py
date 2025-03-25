import requests
import asyncio
import logging
from telegram import Bot

# Telegram Bot Credentials
BOT_TOKEN = "7721365750:AAGw66skneGqXXGy_B8xKoLiR8uDthayvrI"
CHANNEL_ID = "-1002481582963"  # Replace with your channel ID

# Cricket & Bookie API (Replace with valid sources)
CRICKET_API_URL = "https://www.cricketlineguru.com/"  # Placeholder
BOOKIE_API_URL = "https://www.southbook.in/"  # Placeholder

# Initialize bot
bot = Bot(token=BOT_TOKEN)
logging.basicConfig(level=logging.INFO)

async def get_data(api_url):
    """Fetch JSON data from an API with debugging."""
    try:
        response = requests.get(api_url, timeout=10)
        logging.info(f"Fetching data from: {api_url}")
        logging.info(f"Response Status Code: {response.status_code}")
        logging.info(f"Response Content: {response.text}")  # Debugging line
        
        response.raise_for_status()  # Raise HTTP error if exists
        
        # Try to parse JSON
        try:
            data = response.json()
            if not data:
                raise ValueError("Empty API response")
            return data
        except ValueError:
            logging.error(f"Invalid JSON response from {api_url}")
            return None
        
    except requests.exceptions.RequestException as e:
        logging.error(f"API Error ({api_url}): {e}")
    return None

async def format_message():
    """Format the Telegram message."""
    cricket_data = await get_data(CRICKET_API_URL)
    bookie_data = await get_data(BOOKIE_API_URL)

    if not cricket_data and not bookie_data:
        return None  # No data to send

    message = "🏏 *Live Cricket Update* 🏏\n\n"
    
    if cricket_data:
        message += f"🏆 *Match:* {cricket_data.get('match', 'N/A')}\n"
        message += f"🏏 *Score:* {cricket_data.get('score', 'N/A')}\n"
        message += f"⚾ *Over:* {cricket_data.get('over', 'N/A')}\n"
        message += f"🦸 *Batsman:* {cricket_data.get('batsman', 'N/A')}\n"
        message += f"🎯 *Bowler:* {cricket_data.get('bowler', 'N/A')}\n"

    if bookie_data:
        message += "\n🎰 *Bookie Ratings* 🎰\n"
        message += f"📊 *Odds:* {bookie_data.get('odds', 'N/A')}\n"

    return message

async def send_updates():
    """Continuously send updates to the Telegram channel."""
    while True:
        message = await format_message()
        if message:
            try:
                await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="Markdown")
                logging.info("✅ Message sent successfully")
            except Exception as e:
                logging.error(f"Telegram API Error: {e}")
        await asyncio.sleep(2)  # Fetch data every 30 seconds

if __name__ == "__main__":
    asyncio.run(send_updates())
