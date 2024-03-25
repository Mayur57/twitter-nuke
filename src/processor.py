import json
import os
from typing import List, Tuple
from multiprocessing import Pool

from src.constants import (
    JS_FILE_PATH,
    JSON_FILE_PATH,
    DELETED_TWEETS_PATH,
    SKIPPED_TWEETS_PATH,
    LIKES_THRESHOLD,
    RETWEETS_THRESHOLD,
    BATCH_SIZE,
)

def process_tweet_json() -> None:
    """Convert the tweet.js file to a JSON file."""
    logging.info("Processing tweet.js file and converting it to JSON.")

    with open(JS_FILE_PATH, "r") as f:
        js_data = f.read()

    json_data = js_data[25:]
    with open(JSON_FILE_PATH, "w") as f:
        f.write(json_data)

    logging.info("Conversion to JSON completed.")

def parse_json_batched() -> List[str]:
    """
    Parse the JSON file and return a list of tweet IDs to delete.

    Returns:
        List[str]: List of tweet IDs to delete.
    """
    tweets_to_delete = []
    skipped_tweets = []

    with open(JSON_FILE_PATH) as jfd:
        data = json.load(jfd)

    pool = Pool()
    batched_data = [data[i:i+BATCH_SIZE] for i in range(0, len(data), BATCH_SIZE)]
    results = pool.map(process_json_batch, batched_data)
    pool.close()
    pool.join()

    for batch_tweets, batch_skipped in results:
        tweets_to_delete.extend(batch_tweets)
        skipped_tweets.extend(batch_skipped)

    with open(DELETED_TWEETS_PATH, "w") as f:
        for tweet_id, tweet_text, likes, retweets in tweets_to_delete:
            f.write(
                f"Tweet deleted:\n\n"
                f"ID: {tweet_id}\n"
                f"Tweet: {tweet_text}\n"
                f"Likes: {likes}\n"
                f"Retweets: {retweets}\n\n"
            )

    with open(SKIPPED_TWEETS_PATH, "w") as f:
        for tweet_id, tweet_text, likes, retweets in skipped_tweets:
            f.write(
                f"Tweet skipped:\n\n"
                f"ID: {tweet_id}\n"
                f"Tweet: {tweet_text}\n"
                f"Likes: {likes}\n"
                f"Retweets: {retweets}\n\n"
            )

    logging.info(f"Selected {len(tweets_to_delete)} tweets to be deleted.")
    logging.info(f"Selected {len(skipped_tweets)} tweets to be skipped.")
    logging.info(f"Filters: Likes more than {LIKES_THRESHOLD} and retweets more than {RETWEETS_THRESHOLD}.")

    return [tweet_id for tweet_id, _, _, _ in tweets_to_delete]

def process_json_batch(batch_data: List[dict]) -> Tuple[List[Tuple], List[Tuple]]:
    """
    Process a batch of JSON data and filter tweets based on specified criteria.

    Args:
        batch_data (List[dict]): A batch of JSON data representing tweets.

    Returns:
        Tuple[List[Tuple], List[Tuple]]: Two lists containing tuples of (tweet_id, tweet_text, likes, retweets)
        for deleted and skipped tweets, respectively.
    """
    deleted_tweets = []
    skipped_tweets = []

    for tweet in batch_data:
        favorite_count = int(tweet["tweet"]["favorite_count"])
        retweet_count = int(tweet["tweet"]["retweet_count"])
        tweet_id = tweet["tweet"]["id"]
        full_text = tweet["tweet"]["full_text"]

        if favorite_count > LIKES_THRESHOLD and retweet_count > RETWEETS_THRESHOLD:
            skipped_tweets.append((tweet_id, full_text, favorite_count, retweet_count))
        else:
            deleted_tweets.append((tweet_id, full_text, favorite_count, retweet_count))

    return deleted_tweets, skipped_tweets