import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

consumer_key = '0AxoVLfJH79Npvq2IvFZk4JpZ'
consumer_secret = 'YoofWwa2331AxJ143QAFP2FKBEil3470bdALHwecMEZgBBm0xu'
access_token = '254795019-7n0fD8nmriLyzyekwdP1ECVZaOloxa2TXjy4u2Ce'
access_secret = 'IC5cbdTUk34ZIfyfSjnuO66ljYMafcgjRO5Nyt3OlRr5j'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)
 
class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('tweets.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            #print(&quot;Error on_data: %s&quot; % str(e))
            print(e)
        return True
 
    def on_error(self, status):
        print(status)
        return True
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#TJHACKS'])

