import requests
import time
from telegram import Bot

# 🔹 Telegram Bot Credentials
TELEGRAM_BOT_TOKEN = "7721365750:AAGw66skneGqXXGy_B8xKoLiR8uDthayvrI"
TELEGRAM_CHANNEL_ID = "-1002481582963"

# 🔹 RapidAPI Headers
headers = {
    "x-rapidapi-key": "7cf2d66dfcmshdb2e3038cee6474p13fa3ajsn8f43f7bc4ddd",
    "x-rapidapi-host": "betfair-sports-casino-live-tv-result-odds.p.rapidapi.com"
}

# 🚀 Send Telegram Message
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHANNEL_ID, "text": message}
    requests.post(url, json=payload)

# 🏏 Get IPL Event ID
def get_ipl_event_id():
    url = "https://betfair-sports-casino-live-tv-result-odds.p.rapidapi.com/api/result/event-list"
    querystring = {"sid": "4"}  # "4" for Cricket
    response = requests.get(url, headers=headers, params=querystring)
    
    events = response.json().get("data", [])
    for event in events:
        if "IPL" in event.get("event_name", ""):
            return event["event_id"]
    
    return None

# 🎯 Get Toss Result
def get_toss_result(event_id):
    url = f"https://betfair-sports-casino-live-tv-result-odds.p.rapidapi.com/api/result/{event_id}"
    response = requests.get(url, headers=headers)
    
    data = response.json()
    toss_winner = data.get("toss_winner", "Unknown")
    toss_decision = data.get("toss_decision", "Unknown")
    
    return f"🏏 **Toss Result**: {toss_winner} won the toss and chose to {toss_decision}."

# 💰 Get Market Odds
def get_market_odds(event_id):
    url = "https://betfair-sports-casino-live-tv-result-odds.p.rapidapi.com/api/GetMarketOdds"
    querystring = {"market_id": event_id}
    response = requests.get(url, headers=headers, params=querystring)
    
    return response.json()

# 🔥 Get Live Score & Player Stats
def get_live_score(event_id):
    url = "https://betfair-sports-casino-live-tv-result-odds.p.rapidapi.com/api/live-score"
    querystring = {"eventid": event_id}
    response = requests.get(url, headers=headers, params=querystring)
    
    data = response.json()

    # Extract Score Details
    team1 = data.get("team_1", "Team A")
    team2 = data.get("team_2", "Team B")
    score = data.get("score", "N/A")
    overs = data.get("overs", "N/A")
    wickets = data.get("wickets", "N/A")
    run_rate = data.get("run_rate", "N/A")
    required_run_rate = data.get("required_run_rate", "N/A")  # If chasing

    # Extract Batsman Details
    batsman_1 = data.get("batsman_1", "Unknown")
    batsman_1_runs = data.get("batsman_1_runs", "0")
    batsman_1_balls = data.get("batsman_1_balls", "0")
    batsman_1_sr = round((int(batsman_1_runs) / int(batsman_1_balls)) * 100, 2) if int(batsman_1_balls) > 0 else 0

    batsman_2 = data.get("batsman_2", "Unknown")
    batsman_2_runs = data.get("batsman_2_runs", "0")
    batsman_2_balls = data.get("batsman_2_balls", "0")
    batsman_2_sr = round((int(batsman_2_runs) / int(batsman_2_balls)) * 100, 2) if int(batsman_2_balls) > 0 else 0

    striker = data.get("striker", batsman_1)  # Who is on strike?

    # Extract Bowler Details
    bowler = data.get("bowler", "Unknown")
    bowler_wickets = data.get("bowler_wickets", "0")
    bowler_runs = data.get("bowler_runs", "0")
    bowler_overs = data.get("bowler_overs", "0")
    bowler_economy = round(int(bowler_runs) / float(bowler_overs), 2) if float(bowler_overs) > 0 else 0

    # Extract Shot Details
    last_ball = data.get("last_ball", "No Update")
    shot_details = data.get("shot_details", "Unknown Shot")  # API must support shot details

    # Extract Wicket Info
    wicket = data.get("wicket", None)  # Only show if it's not None

    message = f"""
🏏 **Live IPL Match**: {team1} vs {team2}
📊 **Score**: {score} | **Overs**: {overs} | **Wickets**: {wickets}  
🔥 **Run Rate**: {run_rate} | **Req. Run Rate**: {required_run_rate}  

🏏 **Batsmen Stats:**  
🔹 **{batsman_1}** - {batsman_1_runs}({batsman_1_balls}) | SR: {batsman_1_sr}  
🔹 **{batsman_2}** - {batsman_2_runs}({batsman_2_balls}) | SR: {batsman_2_sr}  
🎯 **On Strike:** {striker}  

🎯 **Bowler:** {bowler}  
🔥 **Wickets:** {bowler_wickets} | 🎯 **Economy:** {bowler_economy}  

⚡ **Last Ball:** {last_ball}  
🏏 **Shot**: {shot_details}  
"""

    if wicket:  # Only include wicket details if there's a wicket
        message += f"❌ **Wicket**: {wicket}"

    return message

# 📌 Main Execution (Every Ball Update)
def main():
    print("\nFetching IPL Event ID...")
    event_id = get_ipl_event_id()

    if not event_id:
        print("❌ No IPL matches found!")
        send_telegram_message("❌ No IPL matches found!")
        return

    print(f"✅ IPL Event ID Found: {event_id}")
    send_telegram_message(f"🏏 **Live IPL Match Started!** \n🎯 **Event ID**: {event_id}")

    # Step 1: Get Toss Result
    toss_result = get_toss_result(event_id)
    send_telegram_message(toss_result)

    # Step 2: Start Loop for Every Ball Update
    while True:
        print("\nFetching Live Score & Market Odds...")
        
        # Fetch Live Score (Ball by Ball)
        live_score = get_live_score(event_id)
        send_telegram_message(live_score)

        # Fetch Market Odds
        market_odds = get_market_odds(event_id)
        send_telegram_message(f"💰 **Market Odds**: {market_odds}")

        time.sleep(10)  # Wait 10 seconds before checking again

# 🚀 Run the script
if __name__ == "__main__":
    main()
