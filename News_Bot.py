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

auth_handler = OAuthHandler(consumer_key_news, consumer_secret_news)
auth_handler.set_access_token(access_token_news, access_token_secret_news)
twitter_client = API(auth_handler, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

logging.getLogger("main").setLevel(logging.INFO)

AVOID = ["monty", "leather", "skin", "bag", "blood", "bite", "dailym.ai", "@MailOnline", "opinion"]
terms =[ 'from:BBCNews',
 'from:nypost',
 'from:BBCWorld',
 'from:Forbes',
 'from:CBSNews',
 'from:CNNBRK',
 'from:thehill',
 'from:FoxNews',
 'from:washingtonpost',
 'from:WSJ',
 'from:ABC',
 'from:NBCNews',
 'from:WashTimes',
 'from:BBCBreaking',
 'from:BreitbartNews',
 'from:TheEconomist',
 'from:business',
 'from:nytimes',
 'from:AP',
 'from:NewsandGuts',
 'from:DanRather',
 'from:Methodenstreit',
 'from:BillGates',
 'from:TheNewsUnspun',
 'from:kold830',
 'from:adamkornfield',
 'from:CNN',
 'from:guardian']

 
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
