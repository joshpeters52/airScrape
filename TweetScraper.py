
# coding: utf-8

# In[7]:

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


# In[8]:

class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print (status)


# In[ ]:

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['#flightbooked'])


# In[ ]:



