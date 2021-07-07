"""
This script will delete all of the tweets in the specified account.


You will need developer level access to get a Twitter API tokens to use this
script, you can do so by registering a twitter application at https://developer.twitter.com/

@requirements: Python 3.10+, Tweepy (https://docs.tweepy.org/en/stable/)
@Original_author: Mayur Bhoi
@Co-author (forked by): <your-name-here>
"""

import json
import tweepy
import threading
import time

# Extract your archive and name the folder something you can remember

# Paste your folder's absolute path below
# For example it can be–
# ARCHIVE_PATH = "/Users/mayur57/Desktop/archive"
ARCHIVE_PATH = ""
JS_FILE = ARCHIVE_PATH + "/data/tweet.js"
JSON_FILE = ARCHIVE_PATH + "/data/deleter.json"
DELETED_TWEETS = ARCHIVE_PATH + "/data/deleted_tweets.txt"
SKIPPED_TWEETS = ARCHIVE_PATH + "/data/skipped_tweets.txt"

# These are optional filters for the tweets you want to delete.
# DO NOT edit these if you want to delete all of your tweets without
# any filters. Otherwise, for example, if you want to skip tweets
# having likes more 30 and retweets more than 5, you change the below
# values as:
# -> LIKES=30, RETWEETS=5
RETWEETS=0
LIKES=40

# Generate your own Twitter API keys and edit them here
consumer_key = 'xxxxxxxx'
consumer_secret = 'xxxxxxxx'
access_token = 'xx-xxxxxx'
access_token_secret = 'xxxxxxxx'

skipped_tweets = []
tweets_to_delete = []

# Number of tweets to be deleted by each thread.
# Smaller batch size means faster deletion but may strain the CPU.
# Recommended value is <500> tweets per thread.
batch_size = 500

def process_tweet_json(JS_FILE):
    print("\n\n>> Processing your tweet.js file and converting it to a JSON.")

    print("\n>> Processing tweet.js file")
    js_file = open(JS_FILE, "r")
    js_data = js_file.read()
    js_file.close()

    print("\n>> Converting to processable JSON")
    json_data = js_data[25:]
    json_file = open(JSON_FILE, "w")
    json_file.write(json_data)
    json_file.close()

def parse_json(JSON_FILE, LIKES, RETWEETS=0):
    with open(JSON_FILE) as jfd:
        data = json.load(jfd)
    
    for tweet in data:
        if(int(tweet["tweet"]["favorite_count"]) > LIKES and int(tweet["tweet"]["retweet_count"]) > RETWEETS):
            f = open(SKIPPED_TWEETS, "w")
            f.write("Tweets skipped:\n\n"
                    + "ID: "+tweet["tweet"]["id"] + "\n"
                    + "Tweet: "+tweet["tweet"]["full_text"]+"\n"
                    + "Likes: "+tweet["tweet"]["favorite_count"]+"\n"
                    + "Retweets: "+tweet["tweet"]["retweet_count"]+"\n\n")
            f.close()
            skipped_tweets.append(str(tweet["tweet"]["id"]))

        else:
            f = open(DELETED_TWEETS, "w")
            f.write("Tweets deleted:\n\n"
                    + "ID: "+tweet["tweet"]["id"] + "\n"
                    + "Tweet: "+tweet["tweet"]["full_text"]+"\n"
                    + "Likes: "+tweet["tweet"]["favorite_count"]+"\n"
                    + "Retweets: "+tweet["tweet"]["retweet_count"]+"\n\n")
            f.close()
            tweets_to_delete.append(str(tweet["tweet"]["id"]))
    
    print("\n>> You have selected " + str(len(tweets_to_delete)) + " tweets to be deleted.")
    print(">> You have selected " + str(len(skipped_tweets))  + " tweets to be deleted.")
    print("\n>> Your choices for filters were: ")
    print(f">> Likes more than {LIKES} and retweets more than {RETWEETS}.\n")

def delete_tweets(batch_start, api):
    for i in range(batch_start, batch_start+batch_size):
        try:
            api.destroy_status(int(tweets_to_delete[i]))
            print("T - Deleted: " + tweets_to_delete[i])
        except tweepy.TweepError as e:
            error_code = str(e.reason[10:13])
            if error_code == "327":
                print("  D ---Skipping: " + tweets_to_delete[i])
            elif error_code == "139":
                print("  D ---Already liked: " + tweets_to_delete[i])
            elif error_code == "185":
                print("ERROR: Rate limit reached. Exiting.")
                break
            else:
                print("ERROR: ---" + e.reason + tweets_to_delete[i])


def make_threads():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    print('''
    
    >> Deletion of tweets takes a long time due to the sluggish Twitter API. The script uses multithreading to delete threads faster. However, it might still take a few minutes to delete your entire history of tweets if it exceeds a couple of thousand tweets.''')
    i = 0
    thread_count = 0
    while(i < int(len(tweets_to_delete))):
        thread_count = thread_count + 1
        t1 = threading.Thread(target=delete_tweets, args=(i, api))
        t1.start()
        print(f"Thread started for deletion. Thread #{thread_count}")
        i = i + batch_size

start_time = time.time()
process_tweet_json(JS_FILE)
parse_json(JSON_FILE, LIKES, RETWEETS)
make_threads()
print(f"--> Successfully deleted {len(tweets_to_delete)} tweets.")
print(f"--> Successfully skipped {len(skipped_tweets)} tweets from deletion.")
print(f"--> Number of threads used: {len(tweets_to_delete) % batch_size} of batch size {batch_size} each.")
print("\n\n--> Process finished in %s seconds." % (time.time() - start_time))
