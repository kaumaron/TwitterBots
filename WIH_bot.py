from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, API
from tweepy import Stream
from time import sleep
import json
import logging
import warnings
from pprint import pprint
from secrets import *

warnings.filterwarnings('ignore')

auth_handler = OAuthHandler(consumer_key_WIH, consumer_secret_WIH)
auth_handler.set_access_token(access_token_WIH, access_token_secret_WIH)
twitter_client = API(auth_handler, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

logging.getLogger("main").setLevel(logging.INFO)

AVOID = []  #["monty", "leather", "skin", "bag", "blood", "bite", "dailym.ai", "@MailOnline"]
terms =['from:highcastletv',
 '#highcastle',
 '#maninthehighcastle',
 '#alternatehistory',
 '#whatif',
 '#whatifhistory',
 'from:alt_historian',
 'from:ahwupdate',
 'from:Yesterday_Today',
 '#militaryhistory',
 'from:MilHistNow',
 '#WW2',
 'from:WW2Nation',
 'from:HNTurtledove',
 '#WorldWar2',
 'from:HistoryofWWII'] 

class PyStreamListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        try:
            publish = True
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

        except Exception as ex:
            logging.error(ex)

        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    listener = PyStreamListener()
    stream = Stream(auth_handler, listener)
    stream.filter(track=terms, stall_warnings = True)