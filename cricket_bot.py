import requests
import time
from telegram import Bot

# 🔹 RapidAPI Credentials
RAPIDAPI_KEY = "7cf2d66dfcmshdb2e3038cee6474p13fa3ajsn8f43f7bc4ddd"
RAPIDAPI_HOST = "cricket-live-line1.p.rapidapi.com"

# 🔹 Telegram Bot Credentials
TELEGRAM_BOT_TOKEN = "7721365750:AAGw66skneGqXXGy_B8xKoLiR8uDthayvrI"
TELEGRAM_CHANNEL_ID = "-1002481582963"

# 🔹 API URLs
LIVE_MATCHES_URL = "https://cricket-live-line1.p.rapidapi.com/matches"
BALL_BY_BALL_URL = "https://cricket-live-line1.p.rapidapi.com/matchBallByBall"

# 🔹 Headers for API requests
HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST
}

def get_live_match_id():
    """Fetch all live matches and extract the match ID for an IPL match."""
    response = requests.get(LIVE_MATCHES_URL, headers=HEADERS)
    
    if response.status_code == 200:
        matches = response.json().get("data", [])
        
        for match in matches:
            if "IPL" in match.get("series", ""):  # Filter only IPL matches
                print(f"🏏 Match Found: {match['team_1']} vs {match['team_2']}")
                print(f"📌 Match ID: {match['match_id']}")
                return match['match_id']
        
        print("❌ No IPL match found")
        return None
    else:
        print(f"❌ API Error: {response.status_code}")
        return None

def get_ball_by_ball_updates(match_id):
    """Fetch ball-by-ball commentary for the given match ID."""
    params = {"match_id": match_id}
    response = requests.get(BALL_BY_BALL_URL, headers=HEADERS, params=params)

    if response.status_code == 200:
        balls = response.json().get("data", [])
        
        if balls:
            latest_ball = balls[0]  # Get the latest delivery
            message = f"🏏 {latest_ball['over']} Over | {latest_ball['ball']} Ball\n" \
                      f"⚡ {latest_ball['commentary']}\n" \
                      f"🎯 Runs: {latest_ball['run']}, Wicket: {latest_ball['wicket']}"
            return message
        else:
            return "No recent ball updates available."
    else:
        print(f"❌ API Error: {response.status_code}")
        return None

def send_telegram_message(message):
    """Send message to the Telegram channel."""
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=message)

def main():
    """Main function to fetch live IPL match updates."""
    match_id = get_live_match_id()
    
    if match_id:
        print(f"✅ Fetching live updates for match ID {match_id}...")
        while True:
            update = get_ball_by_ball_updates(match_id)
            if update:
                print(update)
                send_telegram_message(update)
            time.sleep(30)  # Fetch every 30 seconds
    else:
        print("❌ No live IPL matches available.")

if __name__ == "__main__":
    main()
