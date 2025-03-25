import requests
import time
from telegram import Bot
from datetime import datetime

# API details
url = "https://cricket-live-line1.p.rapidapi.com/upcomingMatches"
headers = {
    "x-rapidapi-key": "YOUR_RAPIDAPI_KEY",  # Replace with your actual API key
    "x-rapidapi-host": "cricket-live-line1.p.rapidapi.com"
}

# Fetch upcoming matches
response = requests.get(url, headers=headers)
matches = response.json()

# Define the start date
start_date = datetime.strptime("25/03/2025", "%d/%m/%Y")

# Filter for IPL matches starting from the specified date
ipl_matches = [
    match for match in matches
    if "IPL" in match.get("league", "") and datetime.strptime(match.get("date"), "%d/%m/%Y") >= start_date
]

# Extract match IDs
ipl_match_ids = [match["id"] for match in ipl_matches]

print("IPL Match IDs from 25/03/2025:", ipl_match_ids)

# Use the first IPL match ID to get live scores (if needed)
if ipl_match_ids:
    match_id = ipl_match_ids[0]
    live_url = f"https://cricket-live-line1.p.rapidapi.com/match/{match_id}/liveLine"
    live_response = requests.get(live_url, headers=headers)
    print(live_response.json())
else:
    print("No IPL matches found from the specified date.")
