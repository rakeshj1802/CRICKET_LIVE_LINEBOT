import asyncio
import logging
import httpx
from telegram import Bot
from telegram.error import RetryAfter

# Telegram Bot Token and Channel ID
BOT_TOKEN = "7721365750:AAGw66skneGqXXGy_B8xKoLiR8uDthayvrI"
CHANNEL_ID = "-1002481582963"

# Cricket API Details
API_URL = "https://api.cricapi.com/v1/currentMatches"
API_KEY = "733fc7f6-fc1b-46e6-8f67-d45a01d44a6a"

# Initialize Telegram Bot
bot = Bot(token=BOT_TOKEN)

async def get_cricket_updates():
    """Fetch live IPL matches from the API."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}?apikey={API_KEY}", timeout=10)
            response.raise_for_status()
            data = response.json()

            # Log full response for debugging
            logging.info(f"API Response: {data}")

            if not data or "data" not in data:
                logging.error("Invalid API response format.")
                return None

            # Filter IPL matches
            ipl_matches = [
                match for match in data["data"] 
                if "Indian Premier League" in match.get("series", {}).get("name", "")
            ]

            if not ipl_matches:
                logging.info("No ongoing IPL matches found.")
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
        team1 = match.get("teamInfo", [{}])[0].get("name", "Unknown")
        team2 = match.get("teamInfo", [{}])[1].get("name", "Unknown")
        venue = match.get("venue", "Unknown")
        start_time = match.get("dateTimeGMT", "TBA")
        score = f"{match.get('score', 'N/A')} / {match.get('wickets', 'N/A')}"
        match_url = match.get("matchLink", "No link")

        msg = (
            f"🏏 *{team1} vs {team2}*\n"
            f"📍 *Venue:* {venue}\n"
            f"🕒 *Time:* {start_time}\n"
            f"📊 *Score:* {score}\n"
            f"🔗 *More Info:* [Click Here]({match_url})"
        )
        messages.append(msg)
    return messages

async def post_update():
    """Send updates to Telegram while handling rate limits."""
    while True:
        matches = await get_cricket_updates()

        if matches is None:
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

        await asyncio.sleep(300)  # Fetch updates every 5 minutes

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(post_update())
