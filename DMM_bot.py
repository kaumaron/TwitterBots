from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, API
from tweepy import Stream
from time import sleep
from random import randint
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

sources = [ 'BBCNews',
 'nypost',
 'BBCWorld',
 'Forbes',
 'CBSNews',
 'CNNBRK',
 'thehill',
 'FoxNews',
 'washingtonpost',
 'WSJ',
 'ABC',
 'NBCNews',
 'WashTimes',
 'BBCBreaking',
 'BreitbartNews',
 'TheEconomist',
 'business',
 'nytimes',
 'AP',
 'CNN',
 'guardian']

 
class PyStreamListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        try:
            publish = False
            if tweet['user']['screen_name'] in sources:
               if not tweet['retweeted']:
                    publish = True
               print('Tweeted: ' + tweet['user']['screen_name'])

            if publish:
                twitter_client.retweet(tweet['id'])
                logging.debug("RT: {}".format(tweet['text']))
                sleep(randint(90,300))

        except Exception as ex:
            logging.error(ex)

        return True

    def on_error(self, status):
        print(status)

def start_stream():
    while True:
        try:
            stream = Stream(auth_handler, listener)
            stream.filter(track= ['FBI','Trump'], languages=['en'], stall_warnings = True)
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
