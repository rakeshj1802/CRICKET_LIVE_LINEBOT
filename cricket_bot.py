import requests
import time
import logging
from telegram import Bot

# Telegram Bot Token and Channel ID
TELEGRAM_BOT_TOKEN ="7721365750:AAGw66skneGqXXGy_B8xKoLiR8uDthayvrI"
TELEGRAM_CHANNEL_ID = "-1002481582963"


API_KEY = "733fc7f6-fc1b-46e6-8f67-d45a01d44a6a"
URL = f"https://api.cricapi.com/v1/cricScore?apikey={API_KEY}"

def get_live_ipl_scores():
    response = requests.get(URL)
    data = response.json()

    if "data" in data:
        for match in data["data"]:
            if match["matchType"] == "t20" and "IPL" in match["series"]:
                print(f"Match: {match['t1']} vs {match['t2']}")
                print(f"Score: {match.get('t1s', 'N/A')} - {match.get('t2s', 'N/A')}")
                print(f"Status: {match['status']}\n")
    else:
        print("No live IPL matches found.")

# Run the function
get_live_ipl_scores()
