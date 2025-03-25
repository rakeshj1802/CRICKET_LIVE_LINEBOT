import asyncio
import logging
import httpx
from telegram import Bot
from telegram.error import RetryAfter

# Telegram Bot Token and Channel ID
BOT_TOKEN = "7721365750:AAGw66skneGqXXGy_B8xKoLiR8uDthayvrI"
CHANNEL_ID = "-1002481582963"

# Cricket API Endpoint (Change if needed)
API_URL = "https://api.cricapi.com/v1/currentiplMatches"
API_KEY="733fc7f6-fc1b-46e6-8f67-d45a01d44a6a"
# Initialize the Telegram Bot
bot = Bot(token=BOT_TOKEN)

async def get_cricket_updates():
    """Fetch live IPL matches from the API."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(API_URL, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data or "matches" not in data:
                logging.error("Invalid API response.")
                return None

            # Filter only IPL matches
            ipl_matches = [match for match in data["matches"] if "IPL" in match.get("series", "")]

            if not ipl_matches:
                logging.info("No IPL matches found.")
                return None

            return ipl_matches

    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP Error: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        logging.error(f"Request Error: {e}")
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")

    return None

def format_message(matches):
    """Format IPL match updates into readable messages."""
    messages = []
    for match in matches:
        msg = (
            f"🏏 *{match['team1']} vs {match['team2']}*\n"
            f"📍 *Venue:* {match.get('venue', 'Unknown')}\n"
            f"🕒 *Time:* {match.get('start_time', 'TBA')}\n"
            f"📊 *Score:* {match.get('score', 'N/A')}\n"
            f"🔗 *More Info:* {match.get('match_url', 'No link')}"
        )
        messages.append(msg)
    return messages

async def post_update():
    """Send updates to Telegram while handling rate limits."""
    while True:
        matches = await get_cricket_updates()

        if matches is None:  # Prevents crashes
            logging.warning("No IPL match data. Retrying in 30 seconds...")
            await asyncio.sleep(30)
            continue

        new_messages = format_message(matches)

        if new_messages:
            for msg in new_messages:
                try:
                    await bot.send_message(chat_id=CHANNEL_ID, text=msg, parse_mode="Markdown")
                    await asyncio.sleep(5)  # Prevent flood limit
                except RetryAfter as e:
                    logging.warning(f"Flood control hit. Retrying in {e.retry_after} sec...")
                    await asyncio.sleep(e.retry_after + 2)  # Wait before retrying

        await asyncio.sleep(5)  # Fetch updates every 5 minutes

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(post_update())
