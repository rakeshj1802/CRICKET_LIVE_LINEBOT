import feedparser
from telegram import Bot

# Telegram bot details
TELEGRAM_BOT_TOKEN = "7721365750:AAGw66skneGqXXGy_B8xKoLiR8uDthayvrI"
TELEGRAM_CHANNEL_ID = "-1002481582963"

# Default live feed URL
_live_scores_xml = 'http://static.espncricinfo.com/rss/livescores.xml'

class CricInfo:
    def __init__(self, live_scores_xml=_live_scores_xml):
        self.live_scores_xml = live_scores_xml
        self.matches = []

    def update_live_scores(self):
        # Parse the RSS feed
        feed = feedparser.parse(self.live_scores_xml)
        for entry in feed.entries:
            match = {
                'title': entry.title,
                'description': entry.description,
                'link': entry.link,
                'guid': entry.id
            }
            self.matches.append(match)

    def __iter__(self):
        return iter(self.matches)

def send_to_telegram(matches):
    # Initialize Telegram bot
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    
    # Send match details to Telegram channel
    for match in matches:
        message = (
            f"Title: {match['title']}\n"
            f"Description: {match['description']}\n"
            f"Link: {match['link']}\n"
            f"GUID: {match['guid']}\n"
        )
        bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=message)

if __name__ == '__main__':
    # Instantiate and update live scores
    matches = CricInfo()
    matches.update_live_scores()
    
    # Send live match updates to Telegram
    send_to_telegram(matches)
