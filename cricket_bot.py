import requests
import time
import logging
from telegram import Bot

# Telegram Bot Token and Channel ID
TELEGRAM_BOT_TOKEN ="7721365750:AAGw66skneGqXXGy_B8xKoLiR8uDthayvrI"
TELEGRAM_CHANNEL_ID = "-1002481582963"


# Cricket API Key (Replace with your valid API key)
CRICAPI_KEY = "733fc7f6-fc1b-46e6-8f67-d45a01d44a6a"
MATCH_URL = f"https://api.cricapi.com/v1/currentMatches?apikey={CRICAPI_KEY}"



# Function to fetch live IPL match details
def get_live_ipl_match():
    url = f"https://api.cricapi.com/v1/cricScore?apikey={CRICAPI_KEY}"
    response = requests.get(url).json()

    for match in response["data"]:
        if "IPL" in match["series"] and match["matchStarted"]:
            return match["id"]  # Return IPL match ID

    return None  # No live IPL match

# Function to fetch match score
def get_match_score(match_id):
    url = f"https://api.cricapi.com/v1/cricScore?apikey={CRICAPI_KEY}&id={match_id}"
    response = requests.get(url).json()
    
    if "score" in response["data"]:
        return response["data"]["score"]  # Return match score
    return "Score not available"

# Function to fetch today's completed IPL matches
def get_completed_matches():
    url = f"https://api.cricapi.com/v1/matchCalendar?apikey={CRICAPI_KEY}"
    response = requests.get(url).json()

    completed_matches = []
    for match in response["data"]:
        if "IPL" in match["series"] and match["date"] == time.strftime("%Y-%m-%d"):
            completed_matches.append(f"🏏 {match['series']} ✅ {match['date']}")

    return completed_matches

# Function to send message to Telegram Channel
def send_to_telegram(message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHANNEL_ID, "text": message}
    requests.post(telegram_url, data=data)

# Main Function
def main():
    live_match_id = get_live_ipl_match()
    if live_match_id:
        match_score = get_match_score(live_match_id)
        send_to_telegram(f"📢 LIVE IPL MATCH UPDATE:\n{match_score}")
    else:
        send_to_telegram("❌ No live IPL matches right now.")

    completed_matches = get_completed_matches()
    if completed_matches:
        send_to_telegram("✅ TODAY'S COMPLETED IPL MATCHES:\n" + "\n".join(completed_matches))
    else:
        send_to_telegram("❌ No completed IPL matches today.")

# Run the script every 5 minutes
while True:
    main()
    time.sleep(300)  # Wait 5 minutes before fetching again
