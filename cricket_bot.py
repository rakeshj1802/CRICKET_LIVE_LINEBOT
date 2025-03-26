import asyncio
import logging
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.ext import Application
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Telegram Bot Configuration
BOT_TOKEN = "7721365750:AAGw66skneGqXXGy_B8xKoLiR8uDthayvrI"
CHANNEL_ID = "-1002481582963"

class IPLLiveScraper:
    def __init__(self, bot_token, channel_id, match_url):
        self.bot_token = bot_token
        self.channel_id = channel_id
        self.match_url = match_url
        self.last_message = None

    def get_headers(self):
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }

    def parse_live_score_card(self, soup):
        """Parse the live score card details"""
        try:
            # Find live score card
            score_card = soup.find('div', class_='live-score-card')
            
            if not score_card:
                return {
                    'team_score': 'N/A',
                    'run_rate': 'N/A',
                    'match_status': 'N/A'
                }

            # Extract Team Score
            team_score_elem = score_card.find('div', class_='team-score')
            team_score = team_score_elem.find('span').text.strip() if team_score_elem else 'N/A'

            # Extract Current Run Rate
            run_rate_elem = score_card.find('span', class_='data')
            run_rate = run_rate_elem.text.strip() if run_rate_elem else 'N/A'

            # Extract Match Status
            match_status_elem = score_card.find('div', class_='final-result')
            match_status = match_status_elem.text.strip() if match_status_elem else 'N/A'

            return {
                'team_score': team_score,
                'run_rate': run_rate,
                'match_status': match_status
            }

        except Exception as e:
            logging.error(f"Error parsing live score card: {e}")
            return {
                'team_score': 'N/A',
                'run_rate': 'N/A',
                'match_status': 'N/A'
            }

    def extract_current_over_scorecard(self, soup):
        """Extract detailed scorecard for the current over"""
        try:
            # Find the overs timeline section
            overs_timeline = soup.find('div', class_='overs-timeline')
            
            if overs_timeline:
                # Find the current over slide (usually the last slide)
                current_over_slide = overs_timeline.find_all('div', class_='overs-slide')[-1]
                
                # Extract over number
                over_number = current_over_slide.find('span').text.strip()
                
                # Find all ball details
                ball_elements = current_over_slide.find_all('div', class_=re.compile(r'ml-o-b-\d+'))
                
                # Extract ball details
                ball_details = [ball.text.strip() for ball in ball_elements]
                
                # Total runs for the over
                total_runs_element = current_over_slide.find('div', class_='total')
                total_runs = total_runs_element.text.strip() if total_runs_element else "N/A"
                
                # Format scorecard entry
                scorecard_entry = f"SCORE CARD :- {total_runs}\n{' '.join(ball_details)}"
                
                return scorecard_entry
            
            return "No current over details available"

        except Exception as e:
            logging.error(f"Error parsing current over slide: {e}")
            return "Error extracting current over details"

    def scrape_live_score(self):
        try:
            response = requests.get(self.match_url, headers=self.get_headers())
            soup = BeautifulSoup(response.text, 'html.parser')

            # Parse live score card
            live_score_info = self.parse_live_score_card(soup)

            # Detailed Batsmen Information
            batsmen_details = []
            striker = None
            batsmen_elements = soup.find_all('div', class_='batsmen-info-wrapper')
            
            for batsman_elem in batsmen_elements:
                # Check for striker icon
                strike_icon = batsman_elem.find('div', class_='circle-strike-icon')
                
                # Extract batsman name
                name_elem = batsman_elem.find('a')
                name = name_elem.find('p').text.strip() if name_elem else "Unknown"
                
                # Extract score details
                score_elem = batsman_elem.find('div', class_='batsmen-score')
                runs = score_elem.find_all('p')
                
                if len(runs) >= 2:
                    batsman_info = f"{name} {runs[0].text}({runs[1].text})"
                else:
                    batsman_info = name
                
                # Identify striker
                if strike_icon:
                    striker = name
                
                batsmen_details.append(batsman_info)

            # Bowler Detection
            bowler = "No bowler info"
            
            # First, check for bowler in batsmen elements with bowling stats
            bowler_elements = [elem for elem in batsmen_elements if 'bowler' in str(elem).lower()]
            if bowler_elements:
                bowler_name_elem = bowler_elements[0].find('a')
                if bowler_name_elem:
                    bowler = bowler_name_elem.find('p').text.strip()
            
            # If not found, check commentary
            if bowler == "No bowler info":
                commentary_elements = soup.find_all('span', class_='cm-b-comment-c1')
                for elem in commentary_elements:
                    if 'to' in elem.text:
                        potential_bowler = elem.text.split('to')[0].strip()
                        if potential_bowler:
                            bowler = potential_bowler
                            break

            # Match Odds Detection
            match_odds = []
            
            # Look for odds in the odds section
            odds_section = soup.find('div', class_='odds-session-left')
            if odds_section:
                # Find favorite team odds
                fav_odd = odds_section.find('div', class_='fav-odd')
                if fav_odd:
                    team_name = fav_odd.find('span', class_='rate-team-full-name')
                    odds_values = fav_odd.find_all('div', class_='odd')
                    
                    if team_name and odds_values:
                        team = team_name.text.strip()
                        odds = [val.text.strip() for val in odds_values]
                        match_odds.append(f"Fav {team}: {' | '.join(odds)}")
            
            # Fallback to popup odds if not found
            if not match_odds:
                odds_popup = soup.find('div', class_='oddSessionInProgress')
                if odds_popup:
                    team = odds_popup.find_all('div')[0].text.strip()
                    odds = [div.text.strip() for div in odds_popup.find_all('div')[1:]]
                    match_odds.append(f"Fav {team}: {' | '.join(odds)}")

            # Win Probability
            probabilities = []
            probability_popup = soup.find('div', class_='overlayPopup')
            if probability_popup:
                prob_view = probability_popup.find('div', class_='progressBarWrapper')
                if prob_view:
                    team_probs = prob_view.find_all('div', class_='teamName')
                    for team_prob in team_probs:
                        team = team_prob.find_all('div')[0].text.strip()
                        prob = team_prob.find_all('div')[1].text.strip()
                        probabilities.append(f"{team}: {prob}")

            # Extract current over scorecard
            current_over_scorecard = self.extract_current_over_scorecard(soup)

            # Prepare message
            message = f"""
🏏 Live Match Update 🏏

📊 RR: {live_score_info['team_score']}
🏃 Current Run Rate: {live_score_info['run_rate']}

📝 Match Status: {live_score_info['match_status']}

🏏 Batsmen:
{' | '.join(batsmen_details)}

🎯 Current Striker: {striker or 'Not identified'}

🎯 Current Bowler: {bowler}

🏆 Match Odds:
{' | '.join(match_odds) if match_odds else 'No odds available'}

📊 Win Probability:
{' | '.join(probabilities) if probabilities else 'No probability data'}

📈 Current Over Scorecard:
{current_over_scorecard}
            """

            return message

        except Exception as e:
            logging.error(f"Comprehensive Scraping Error: {e}")
            return None

    async def send_telegram_update(self, message):
        try:
            bot = Bot(token=self.bot_token)
            
            if message and message != self.last_message:
                await bot.send_message(
                    chat_id=self.channel_id, 
                    text=message,
                    parse_mode='Markdown'
                )
                self.last_message = message
                logging.info("Telegram message sent successfully")
        except Exception as e:
            logging.error(f"Telegram sending error: {e}")

    async def run(self):
        while True:
            try:
                message = self.scrape_live_score()
                
                if message:
                    await self.send_telegram_update(message)
                
                await asyncio.sleep(0)  # Update every minute
            
            except Exception as e:
                logging.error(f"Main run error: {e}")
                await asyncio.sleep(0)

async def main():
    MATCH_URL = "https://crex.live/scoreboard/T2Z/1PD/6th-Match/J/M/kkr-vs-rr-6th-match-indian-premier-league-2025/live"
    
    scraper = IPLLiveScraper(BOT_TOKEN, CHANNEL_ID, MATCH_URL)
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    await scraper.run()

if __name__ == "__main__":
    asyncio.run(main())
