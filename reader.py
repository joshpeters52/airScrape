import json
import csv
import wget


file = open('output.txt', 'w+')
count = 0;


with open('tweets.json', 'r') as f:

	for line in f:
		tweet = json.loads(line) # load it as Python dict
		#print(json.dumps(tweet, indent=4)) # pretty-print#pprint(data["medai_url"])
		name = tweet['user']['name']
		screenName = tweet['user']['screen_name']
		try:
			mediaUrl = tweet['extended_entities']['media'][0]['media_url']
			file.write(name + ',' + screenName + ',' + mediaUrl + '\n')
			filename = wget.download(mediaUrl)
		except:
			print('error on ' + str(count))
			mediaUrl = ''
			pass

