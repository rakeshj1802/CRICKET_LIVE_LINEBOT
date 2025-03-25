import requests
from datetime import datetime
from telegram import Bot
import time

# API details
url = "https://cricket-live-line1.p.rapidapi.com/upcomingMatches"
headers = {
    "x-rapidapi-key": "7cf2d66dfcmshdb2e3038cee6474p13fa3ajsn8f43f7bc4ddd",
    "x-rapidapi-host": "cricket-live-line1.p.rapidapi.com"
}

# Telegram bot details
TELEGRAM_BOT_TOKEN = "7721365750:AAGw66skneGqXXGy_B8xKoLiR8uDthayvrI"
TELEGRAM_CHANNEL_ID = "-1002481582963"

# Fetch upcoming matches
response = requests.get(url, headers=headers)
matches = response.json()

# Check if the response is a list
if isinstance(matches, list):
    # Define the start date
    start_date = datetime.strptime("25/03/2025", "%d/%m/%Y")

    # Filter for IPL matches starting from the specified date
    ipl_matches = []
    for match in matches:
        league = match.get("league", "")
        match_date_str = match.get("date", "")
        
        try:
            match_date = datetime.strptime(match_date_str, "%d/%m/%Y")
        except ValueError:
            continue

        if "IPL" in league and match_date >= start_date:
            ipl_matches.append(match)

    # Extract match IDs
    ipl_match_ids = [match["id"] for match in ipl_matches]

    # Initialize Telegram bot
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    # Send match IDs to Telegram channel
    if ipl_match_ids:
        message = f"IPL Match IDs from 25/03/2025: {ipl_match_ids}"
        bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=message)
    else:
        bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text="No IPL matches found from the specified date.")
else:
    print("Error fetching matches:", matches)
