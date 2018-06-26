from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, API
from tweepy import Stream
from random import randint
from time import sleep
import json
import logging
import warnings
from pprint import pprint
from secrets import *

warnings.filterwarnings('ignore')

auth_handler = OAuthHandler(consumer_key, consumer_secret)
auth_handler.set_access_token(access_token, access_token_secret)
twitter_client = API(auth_handler,
                    wait_on_rate_limit=True,
                    wait_on_rate_limit_notify=True)

logging.getLogger("main").setLevel(logging.INFO)

AVOID = [
        "dailym.ai",
        "@MailOnline",
        ]
terms = [
        'data science',
        'datascience',
        'artificial intelligence',
        'Deep Learning',
        '@TDataScience',
        ]

class PyStreamListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        try:
            publish = True
            if tweet['user']['screen_name'] in AVOID:
                publish = False

            for word in AVOID:
                if word.lower() in tweet['text'].lower():
                    logging.info("SKIPPED FOR {}".format(word))
                    publish = False

            if tweet.get('lang') and tweet.get('lang') != 'en':
                publish = False

            if len(tweet['text']) < 15:
                publish = False

            if publish:
                twitter_client.retweet(tweet['id'])
                logging.debug("RT: {}".format(tweet['text']))
                sleep(randint(180,480))

        except Exception as ex:
            logging.error(ex)

        return True

    def on_error(self, status):
        print(status)

def start_stream():
    while True:
            try:
                stream = Stream(auth_handler, listener)
                stream.filter(track= ['FBI','Trump'], languages=['en'],
                    stall_warnings = True)
            except KeyboardInterrupt:
                logging.debug("Manual interrupt! Don't worry. Be Happy!"+\
                    "Bippity Boppity Boo.")
                print("Manual interrupt! Don't worry. James, that means you!"+\
                        "Down for maintenence or malicious intent.")
                break
            except Exception as e:
                print("Stream failed due to error: {}".format(e))
                logging.debug("Stream failed due to error: {}".format(e))
                continue

if __name__ == '__main__':
    listener = PyStreamListener()
    start_stream()
