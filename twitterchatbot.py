import tweepy
import logging
from time import sleep
from datetime import datetime
from random import choice

# Twitter API credentials
API_KEY = "your_api_key"
API_SECRET_KEY = "your_api_secret_key"
ACCESS_TOKEN = "your_access_token"
ACCESS_TOKEN_SECRET = "your_access_token_secret"

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Responses
GREETINGS = [
    "Hello! How can I assist you today?",
    "Hi there! How can I help you?",
    "Hey! What can I do for you today?",
]

HELP_MESSAGES = [
    "Sure! I can help you with various topics such as account issues, product information, and troubleshooting.",
    "I'm here to assist you with any questions or concerns you may have. Feel free to ask!",
    "Need assistance? Just let me know what you need help with!",
]

# Function to respond to mentions
def respond_to_mentions():
    since_id = 1
    while True:
        try:
            logger.info("Retrieving mentions...")
            mentions = api.mentions_timeline(since_id=since_id, tweet_mode="extended")

            for mention in reversed(mentions):
                since_id = mention.id
                logger.info(f"Responding to mention {mention.id} from {mention.user.screen_name}")

                # Extract the user's screen name
                user_screen_name = mention.user.screen_name

                # Respond with a greeting
                greeting = choice(GREETINGS)
                api.update_status(f"@{user_screen_name} {greeting}", in_reply_to_status_id=mention.id)

                # Provide help message
                help_message = choice(HELP_MESSAGES)
                api.update_status(f"@{user_screen_name} {help_message}", in_reply_to_status_id=mention.id)

        except tweepy.TweepError as e:
            logger.error(f"Error: {e.reason}")

        sleep(30)  # Check for mentions every 30 seconds

if __name__ == "__main__":
    logger.info("Bot started at " + str(datetime.now()))
    respond_to_mentions()
