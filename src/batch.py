import logging
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed

import tweepy

def delete_tweets_batch(api, tweets_to_delete: List[str], batch_size: int = 100) -> None:
    """
    Delete tweets using the Twitter API in batches.

    Args:
        api (tweepy.API): Authenticated Twitter API object.
        tweets_to_delete (List[str]): List of tweet IDs to delete.
        batch_size (int): Number of tweets to delete in each batch.
    """
    with ThreadPoolExecutor() as executor:
        batched_tweets = [tweets_to_delete[i:i+batch_size] for i in range(0, len(tweets_to_delete), batch_size)]
        futures = [executor.submit(delete_tweet_batch, api, batch) for batch in batched_tweets]

        for future in as_completed(futures):
            try:
                result = future.result()
                if result:
                    logging.info(f"Successfully deleted {len(result)} tweets.")
            except Exception as e:
                logging.error(f"Error deleting batch of tweets: {e}")

def delete_tweet_batch(api, tweets_to_delete: List[str]) -> List[str]:
    """
    Delete a batch of tweets using the Twitter API.

    Args:
        api (tweepy.API): Authenticated Twitter API object.
        tweets_to_delete (List[str]): List of tweet IDs to delete.

    Returns:
        List[str]: List of successfully deleted tweet IDs.
    """
    deleted_tweets = []

    for tweet_id in tweets_to_delete:
        try:
            api.destroy_status(int(tweet_id))
            deleted_tweets.append(tweet_id)
        except tweepy.TweepError as e:
            error_code = str(e.reason[10:13])
            if error_code == "327":
                logging.warning(f"Skipping: {tweet_id}")
            elif error_code == "139":
                logging.warning(f"Already liked: {tweet_id}")
            elif error_code == "185":
                logging.error("Rate limit reached. Exiting.")
                break
            else:
                logging.error(f"Error: {e.reason} {tweet_id}")

    return deleted_tweets