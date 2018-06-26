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

AVOID = ['COD', 'CallofDuty']  #["monty", "leather", "skin", "bag", "blood", "bite", "dailym.ai", "@MailOnline"]
flagged_users = [
'andrewg69968905',
'CMG_eSports',
'SadeMarq',
'6TedyBear5',
'andrzejbor61',
'invisible_jp',
'namethej_com'
]

terms =[
 'from:highcastletv',
 '#highcastle',
 '#maninthehighcastle',
 '#alternatehistory',
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
 'from:HistoryofWWII',
 '-#MarchForOurLives',
 '#tweetfromalternatehistory',
] 

class PyStreamListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        try:
            publish = True
            if tweet['user']['screen_name'] in flagged_users:
                publish = False

            for word in AVOID:
                if word.lower() in tweet['text'].lower():
                    logging.info("SKIPPED FOR {}".format(word))
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

def start_stream():
    while True:
        try:
            stream = Stream(auth_handler, listener)
            stream.filter(track= terms, languages=['en'], stall_warnings = True)
        except KeyboardInterrupt:
            logging.debug("Manual interrupt! Don't worry. Be Happy!\nBippity Boppity Boo.")
            print("Manual interrupt! Don't worry. James, that means you!\nDown for maintenence or malicious intent.")
            break
        except Exception as e:
            print("Stream failed due to error: {}".format(e))
            logging.debug("Stream failed due to error: {}".format(e))
            continue

if __name__ == '__main__':
    listener = PyStreamListener()
    start_stream()
