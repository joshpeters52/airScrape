import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import csv
import wget
import subprocess
from PhotoHandler import PhotoHandler
import MySQLdb
import smtplib
from email.mime.text import MIMEText

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

        cnx = {'host': 'air-scrape-db2.ch5gacg1ryrd.us-east-1.rds.amazonaws.com',
                'username': 'sharknado2',
                'password': 'badandboujee2',
                'db': 'sharknado2'}
        self.db = MySQLdb.connect(host=cnx['host'],port=3306,user=cnx['username'],passwd=cnx['password'],db=cnx['db'])


    def handle_data(self, data):
        file = open('output.txt', 'w+')
        tweet = json.loads(data) # load it as Python dict
        print(json.dumps(tweet, indent=4)) # pretty-print#pprint(data["medai_url"])
        name = tweet['user']['name']
        screenName = tweet['user']['screen_name']
        #link = tweet
        try:
            mediaUrl = tweet['extended_entities']['media'][0]['media_url']
            filename = wget.download(mediaUrl, out = 'data/images/'+screenName+'.jpg')
            conf, airports, airline = self.handler.findDataInPicture('data/images/' + screenName + '.jpg')
            if conf is None:
                return
            self.writeToDB(name, screenName, mediaUrl, ','.join(conf), ','.join(airports), airline, 'NONE')
            self.sendEmail()
        except Exception as e:
            print(e)
            mediaUrl = ''

    def writeToDB(self, name, handle, mediaUrl, conf, airports, airlines, linkURL):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO data (name, twitterHandle, imageURL, confirmationCode, airports, airlines, linkURL) VALUES (%s,%s,%s,%s,%s,%s,%s)", (name,handle,mediaUrl,conf,airports,airlines,linkURL))
        self.db.commit()
 
    def sendEmail(self):
        gmail_user = "airscraper.scrappy@gmail.com"
        gmail_pwd = "badandboujee"
        FROM = "airscraper.scrappy@gmail.com"
        TO = "rjdean123@gmail.com"
        message = "hello world"

        msg = MIMEText("I found you another vulnerable flight! Check it out at http://localhost:5000")
        msg['Subject'] = 'AIRSCRAPE | New Flight!'
        me = 'rjdean123@gmail.com'
        you = 'rjdean123@gmail.com'
        msg['From'] = me
        msg['To'] = you
        
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.ehlo() # optional, called by login()
        server_ssl.login(gmail_user, gmail_pwd)  
        # ssl server doesn't support or need tls, so don't call server_ssl.starttls() 
        server_ssl.sendmail(FROM, TO, msg.as_string())
        #server_ssl.quit()
        server_ssl.close()

    def on_data(self, data):
        self.handle_data(data)
        return True
 
    def on_error(self, status):
        print(status)
        return True
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#TJHACKS'])

