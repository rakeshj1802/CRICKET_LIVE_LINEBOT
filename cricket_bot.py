import requests
import time
from telegram import Bot

# Telegram Bot Details
TELEGRAM_BOT_TOKEN = "7721365750:AAGw66skneGqXXGy_B8xKoLiR8uDthayvrI"
TELEGRAM_CHANNEL_ID = "-1002481582963"

# API Headers
headers = {
    "x-rapidapi-key": "7cf2d66dfcmshdb2e3038cee6474p13fa3ajsn8f43f7bc4ddd",
    "x-rapidapi-host": "betfair-sports-casino-live-tv-result-odds.p.rapidapi.com"
}

# Function to Send Message to Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": message
    }
    response = requests.post(url, json=payload)
    return response.json()

# Function to Get IPL Event IDs
def get_ipl_event_ids():
    url = "https://betfair-sports-casino-live-tv-result-odds.p.rapidapi.com/api/result/event-list"
    querystring = {"sid": "4"}  # "4" for Cricket
    response = requests.get(url, headers=headers, params=querystring)
    
    all_events = response.json().get("data", [])
    
    # Filter IPL Matches
    ipl_events = [event for event in all_events if "IPL" in event.get("event_name", "")]
    
    return ipl_events

# Function to Get Market ID for an Event
def get_market_id(event_id):
    url = "https://betfair-sports-casino-live-tv-result-odds.p.rapidapi.com/api/GetMarketOdds"
    querystring = {"market_id": event_id}
    response = requests.get(url, headers=headers, params=querystring)
    
    return response.json()

# Function to Get Live Score for a Match
def get_live_score(event_id):
    url = "https://betfair-sports-casino-live-tv-result-odds.p.rapidapi.com/api/live-score"
    querystring = {"eventid": event_id}
    response = requests.get(url, headers=headers, params=querystring)
    
    return response.json()

# Main Execution
def main():
    # Step 1: Get IPL Event IDs
    print("\nFetching IPL Events...")
    ipl_events = get_ipl_event_ids()

    if not ipl_events:
        print("❌ No IPL matches found!")
        send_telegram_message("❌ No IPL matches found!")
        return

    for event in ipl_events:
        event_name = event["event_name"]
        event_id = event["event_id"]
        print(f"✅ Match: {event_name} | Event ID: {event_id}")
        send_telegram_message(f"🏏 **Live IPL Match**: {event_name} \n🎯 **Event ID**: {event_id}")

        # Step 2: Get Market Odds
        print("\nFetching Market Odds...")
        market_odds = get_market_id(event_id)
        send_telegram_message(f"💰 **Market Odds**: {market_odds}")

        # Step 3: Get Live Score
        print("\nFetching Live Score...")
        live_score = get_live_score(event_id)
        send_telegram_message(f"🔥 **Live Score Update**:\n{live_score}")

        print("\n" + "="*50 + "\n")

# Run the script
if __name__ == "__main__":
    main()
