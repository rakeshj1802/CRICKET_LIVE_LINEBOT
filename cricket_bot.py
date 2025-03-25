import requests
import time
from telegram import Bot


# 🔹 RapidAPI Credentials
RAPIDAPI_KEY = "7cf2d66dfcmshdb2e3038cee6474p13fa3ajsn8f43f7bc4ddd"
RAPIDAPI_HOST = "cricket-live-line1.p.rapidapi.com"

# 🔹 API URLs
LIVE_MATCHES_URL = "https://cricket-live-line1.p.rapidapi.com/home"
PREVIOUS_MATCHES_URL = "https://cricket-live-line1.p.rapidapi.com/matches"

# 🔹 Headers for API requests
HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST
}

def get_live_ipl_scores():
    """Fetch live IPL match details."""
    response = requests.get(LIVE_MATCHES_URL, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json().get("data", [])

        print("\n🔴 LIVE IPL MATCHES 🔴\n")
        found = False
        for match in data:
            if "IPL" in match.get("series", ""):
                print(f"🏏 Match: {match['team_1']} vs {match['team_2']}")
                print(f"📌 Status: {match.get('match_status', 'N/A')}")
                print(f"📊 Score: {match.get('score', 'N/A')}\n")
                found = True
        
        if not found:
            print("❌ No Live IPL Matches Found.")
    else:
        print(f"❌ API Error: {response.status_code}")

def get_previous_ipl_match():
    """Fetch the most recent completed IPL match details."""
    response = requests.get(PREVIOUS_MATCHES_URL, headers=HEADERS)
    
    if response.status_code == 200:
        matches = response.json().get("data", [])

        print("\n✅ PREVIOUS IPL MATCH ✅\n")
        for match in matches:
            if "IPL" in match.get("series", "") and match.get("match_status") == "completed":
                print(f"🏏 Match: {match['team_1']} vs {match['team_2']}")
                print(f"📅 Date: {match['match_date']}")
                print(f"📌 Match ID: {match['match_id']}")
                print(f"🏆 Winner: {match['match_winner']}")
                print(f"🎯 Final Score: {match.get('score', 'N/A')}\n")
                return match['match_id']

        print("❌ No completed IPL matches found.")
        return None
    else:
        print(f"❌ API Error: {response.status_code}")
        return None

# Run both functions
get_live_ipl_scores()
get_previous_ipl_match()
