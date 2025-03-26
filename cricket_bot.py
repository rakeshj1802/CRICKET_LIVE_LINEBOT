import requests
import time
from telegram import Bot

# 🔹 Telegram Bot Credentials
TELEGRAM_BOT_TOKEN = "7721365750:AAGw66skneGqXXGy_B8xKoLiR8uDthayvrI"
TELEGRAM_CHANNEL_ID = "-1002481582963"

# 🔹 RapidAPI Credentials
RAPIDAPI_KEY = "7cf2d66dfcmshdb2e3038cee6474p13fa3ajsn8f43f7bc4ddd"
RAPIDAPI_HOST = "betfair-sports-casino-live-tv-result-odds.p.rapidapi.com"

# Initialize Telegram Bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Step 1: Get Previous IPL Match Event ID
event_list_url = "https://betfair-sports-casino-live-tv-result-odds.p.rapidapi.com/api/result/event-list"
query_params = {"sid": "4"}  # 4 is the sport ID for Cricket

headers = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST
}

response = requests.get(event_list_url, headers=headers, params=query_params)
event_data = response.json()

# Extract the latest IPL match ID
ipl_matches = [event for event in event_data["data"] if "IPL" in event["name"]]
if ipl_matches:
    previous_match = ipl_matches[0]  # Last completed IPL match
    match_id = previous_match["event_id"]
    market_id = previous_match["market_id"]  # Market ID for betting odds
    print(f"✅ Found Previous IPL Match ID: {match_id}, Market ID: {market_id}")
else:
    print("❌ No IPL matches found")
    exit()

# Step 2: Fetch Ball-by-Ball Data for the First Innings
ball_by_ball_url = "https://betfair-sports-casino-live-tv-result-odds.p.rapidapi.com/api/ball-by-ball"
query_params = {"eventid": match_id}

response = requests.get(ball_by_ball_url, headers=headers, params=query_params)
ball_data = response.json()

first_innings_balls = ball_data["innings"][0]["balls"]  # Get first innings data

# Step 3: Fetch Market Odds
market_odds_url = "https://betfair-sports-casino-live-tv-result-odds.p.rapidapi.com/api/GetMarketOdds"
query_params = {"market_id": market_id}

response = requests.get(market_odds_url, headers=headers, params=query_params)
odds_data = response.json()

# Extract Match Odds
team1 = odds_data["data"][0]["team1"]
team2 = odds_data["data"][0]["team2"]
team1_odds = odds_data["data"][0]["team1_odds"]
team2_odds = odds_data["data"][0]["team2_odds"]

# Step 4: Send Ball-by-Ball Updates with Market Odds to Telegram
for ball in first_innings_balls:
    over = ball["over"]
    ball_number = ball["ball_number"]
    batsman = ball["batsman"]
    bowler = ball["bowler"]
    runs = ball["runs"]
    shot_type = ball["shot_type"]
    wicket = ball.get("wicket", None)
    
    # Format the output
    message = f"🏏 *First Innings - Ball {over}.{ball_number}*\n"
    message += f"🔹 Batsman: {batsman}\n"
    message += f"🎯 Bowler: {bowler}\n"
    message += f"⚡ Runs: {runs} Runs\n"
    message += f"🏏 Shot: {shot_type}\n"
    
    if wicket:
        message += f"❌ WICKET! {wicket['batsman_out']} is Out ({wicket['dismissal_type']})\n"

    # Add Market Odds
    message += f"\n🎲 *Match Odds*:\n"
    message += f"🔹 {team1}: {team1_odds}\n"
    message += f"🔹 {team2}: {team2_odds}\n"

    print(message)  # Print message in console
    bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=message, parse_mode="Markdown")

    time.sleep(1)  # Small delay to avoid spamming Telegram
