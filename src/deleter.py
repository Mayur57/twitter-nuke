"""
This script, Twitter Nuke, will delete all of the tweets in the specified account.

You will need developer level access to get Twitter API tokens to use this
script. You can do so by registering a Twitter application at https://developer.twitter.com/

@requirements: Python 3.10+, Tweepy (https://docs.tweepy.org/en/stable/)
@author: Mayur Bhoi
"""

import tweepy

from src.constants import (
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET,
)
from src.logging import setup_logging
from src.batch import delete_tweets_batch
from src.processor import process_tweet_json, parse_json_batched

setup_logging()

def main() -> None:
    """Main function to run the Twitter Nuke script."""
    process_tweet_json()
    tweets_to_delete = parse_json_batched()

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    logging.info("""
    Deletion of tweets takes a long time due to the sluggish Twitter API.
    The script uses multithreading to delete tweets faster. However, it might
    still take a few minutes to delete your entire history of tweets if it
    exceeds a couple of thousand tweets.
    """)

    delete_tweets_batch(api, tweets_to_delete)

if __name__ == "__main__":
    main()