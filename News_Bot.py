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

        except Exception as ex:
            logging.error(ex)

        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    listener = PyStreamListener()
    stream = Stream(auth_handler, listener)
    stream.filter(track= ['Trump'], languages=['en'], stall_warnings = True)
