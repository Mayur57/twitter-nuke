import os

# Archive paths
ARCHIVE_PATH = ""
JS_FILE_PATH = os.path.join(ARCHIVE_PATH, "data", "tweets.js")
JSON_FILE_PATH = os.path.join(ARCHIVE_PATH, "data", "deleter.json")
DELETED_TWEETS_PATH = os.path.join(ARCHIVE_PATH, "data", "deleted_tweets.txt")
SKIPPED_TWEETS_PATH = os.path.join(ARCHIVE_PATH, "data", "skipped_tweets.txt")

# Filters
RETWEETS_THRESHOLD = 0
LIKES_THRESHOLD = 40

# Twitter API keys
CONSUMER_KEY = 'xxxxxxxx'
CONSUMER_SECRET = 'xxxxxxxx'
ACCESS_TOKEN = 'xx-xxxxxx'
ACCESS_TOKEN_SECRET = 'xxxxxxxx'

# Batch size for processing JSON data and API calls
BATCH_SIZE = 1000