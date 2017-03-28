from flask import Flask, render_template

import MySQLdb

app = Flask(__name__)

@app.route("/")
def index():
	entries = getData()
	for i, entry in enumerate(entries):
		entry['style'] = 'even'
		if i % 2 == 0:
			entry['style'] = 'odd'
		temp = entry['airports']
		temp = temp.split(',')
		entry['FROM'] = "LAX"
		entry['TO'] = "ATL"
		if len(temp) > 0:
			entry['FROM'] = temp[0]
		if len(temp) > 1:
			entry['TO'] = temp[1]
	return render_template('index.html', entries = entries)

def getData():
	cnx = {'host': 'air-scrape-db2.ch5gacg1ryrd.us-east-1.rds.amazonaws.com',
                'username': 'sharknado2',
                'password': 'badandboujee2',
                'db': 'sharknado2'}
	db = MySQLdb.connect(host=cnx['host'],port=3306,user=cnx['username'],passwd=cnx['password'],db=cnx['db'])

	cursor = db.cursor()

	query = ("SELECT * FROM data")

	cursor.execute(query)

	entries = []

	websites = {
		'alaska' : 'https://www.alaskaair.com/',
		'allegiant' : 'https://www.allegiantair.com/online-checkin',
		'american' : 'https://www.aa.com/homePage.do',
		'delta' : 'http://www.delta.com/',
		'frontier' : 'https://www.flyfrontier.com/manage-travel/my-trip/',
		'hawaiian' : 'https://www.hawaiianairlines.com/',
		'jetblue' : 'https://book.jetblue.com/B6.myb/#/landing',
		'southwest' : 'https://www.southwest.com/flight/lookup-air-reservation.html',
		'spirit' : 'https://www.spirit.com/Default.aspx',
		'united' : 'https://www.united.com/ual/en/us/',
		'virgin' : 'https://www.virginamerica.com/manage-itinerary/'
	}

	for (id, name, handle, imageurl, conf, airports, airlines, linkurl) in cursor:
	  temp = {}
	  temp['name'] = name
	  temp['handle'] = handle
	  temp['imageurl'] = imageurl
	  conf = conf.split(',')
	  temp['conf'] = conf[0]
	  temp['airports'] = airports
	  temp['airlines'] = airlines
	  temp['linkurl'] = linkurl
	  temp['airlineurl'] = "http://www.delta.com"
	  if airlines.lower() in websites:
	  	temp['airlineurl'] = websites[airlines.lower()]
	  entries.append(temp)

	cursor.close()

	return entries


if __name__ == "__main__":
	app.run()
