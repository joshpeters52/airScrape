import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import csv
import wget
import subprocess
from PhotoHandler import PhotoHandler

consumer_key = '0AxoVLfJH79Npvq2IvFZk4JpZ'
consumer_secret = 'YoofWwa2331AxJ143QAFP2FKBEil3470bdALHwecMEZgBBm0xu'
access_token = '254795019-7n0fD8nmriLyzyekwdP1ECVZaOloxa2TXjy4u2Ce'
access_secret = 'IC5cbdTUk34ZIfyfSjnuO66ljYMafcgjRO5Nyt3OlRr5j'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)
 
class MyListener(StreamListener):

    def __init__(self):
        self.handler = PhotoHandler()
        delete_cmd = "rm -rf data/images/"
        process = process = subprocess.Popen(delete_cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        create_cmd = "mkdir data/images/"
        process = process = subprocess.Popen(create_cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    def handle_data(self, data):
        file = open('output.txt', 'w+')
        tweet = json.loads(data) # load it as Python dict
        #print(json.dumps(tweet, indent=4)) # pretty-print#pprint(data["medai_url"])
        name = tweet['user']['name']
        screenName = tweet['user']['screen_name']
        try:
            mediaUrl = tweet['extended_entities']['media'][0]['media_url']
            filename = wget.download(mediaUrl, out = 'data/images/'+screenName+'.jpg')
            conf, airports, airline = self.handler.findDataInPicture('data/images/' + screenName + '.jpg')
            if conf is None:
                return
            file.write(name + ',' + screenName + ',' + mediaUrl + ',')
            for c in conf:
                file.write(c + '-')
            file.write(',')
            for a in airports:
                file.write(a+'-')
            file.write(',' + airline)
            file.write('\n')
        except Exception as e:
            print(e)
            mediaUrl = ''
 
    def on_data(self, data):
        self.handle_data(data)
        return True
 
    def on_error(self, status):
        print(status)
        return True
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#TJHACKS'])

