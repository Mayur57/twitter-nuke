import unittest
import json
import os
from unittest.mock import patch, mock_open
from src.processor import process_tweet_json, parse_json_batched
from src.batch import delete_tweets_batch, delete_tweet_batch
from src.constants import (
    JS_FILE_PATH,
    JSON_FILE_PATH,
    DELETED_TWEETS_PATH,
    SKIPPED_TWEETS_PATH,
    LIKES_THRESHOLD,
    RETWEETS_THRESHOLD,
)

class TestTweetProcessor(unittest.TestCase):
    def setUp(self):
        self.js_data = "window.YTD.tweet.part0 = [/* ... */]"
        self.json_data = [
            {
                "tweet": {
                    "id": "1234567890",
                    "full_text": "This is a test tweet.",
                    "favorite_count": 10,
                    "retweet_count": 5,
                }
            },
            {
                "tweet": {
                    "id": "9876543210",
                    "full_text": "Another test tweet.",
                    "favorite_count": 50,
                    "retweet_count": 20,
                }
            },
        ]

    @patch("builtins.open", new_callable=mock_open, read_data=js_data)
    def test_process_tweet_json(self, mock_open):
        process_tweet_json()
        mock_open.assert_called_with(JS_FILE_PATH, "r")
        mock_open.return_value.write.assert_called_with(json.dumps(self.json_data)[25:])

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps(json_data))
    def test_parse_json_batched(self, mock_open):
        tweets_to_delete = parse_json_batched()
        self.assertEqual(len(tweets_to_delete), 1)
        self.assertEqual(tweets_to_delete[0], "1234567890")

        with open(DELETED_TWEETS_PATH, "r") as f:
            deleted_tweets = f.read()
        self.assertIn("1234567890", deleted_tweets)

        with open(SKIPPED_TWEETS_PATH, "r") as f:
            skipped_tweets = f.read()
        self.assertIn("9876543210", skipped_tweets)

class TestTweetDeletion(unittest.TestCase):
    def setUp(self):
        self.tweet_ids = ["1234567890", "9876543210"]
        self.api_mock = mock_tweepy_api()  # Assuming this function exists

    @patch("tweepy.API", return_value=api_mock)
    def test_delete_tweets_batch(self, mock_api):
        delete_tweets_batch(mock_api, self.tweet_ids)
        self.assertEqual(mock_api.destroy_status.call_count, 2)

    @patch("tweepy.API", return_value=api_mock)
    def test_delete_tweet_batch(self, mock_api):
        deleted_tweets = delete_tweet_batch(mock_api, self.tweet_ids)
        self.assertEqual(len(deleted_tweets), 2)
        self.assertListEqual(deleted_tweets, self.tweet_ids)

if __name__ == "__main__":
    unittest.main()