from flask import Flask, render_template

import MySQLdb

app = Flask(__name__)

@app.route("/")
def index():
	entries = getData()
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

	for (id, name, handle, imageurl, conf, airports, airlines, linkurl) in cursor:
	  temp = {}
	  temp['name'] = name
	  temp['handle'] = handle
	  temp['imageurl'] = imageurl
	  temp['conf'] = conf
	  temp['airports'] = airports
	  temp['airlines'] = airlines
	  entries.append(temp)

	cursor.close()

	return entries


if __name__ == "__main__":
	app.run()
