import MySQLdb


def writeToDB(name, handle, mediaUrl, conf, airports, airlines, linkURL, db):
    cursor = db.cursor()
    cursor.execute("INSERT INTO data (name, twitterHandle, imageURL, confirmationCode, airports, airlines, linkURL) VALUES (%s,%s,%s,%s,%s,%s,%s)", (name,handle,mediaUrl,conf,airports,airlines,linkURL))
    db.commit()


cnx = {'host': 'air-scrape-db2.ch5gacg1ryrd.us-east-1.rds.amazonaws.com',
                'username': 'sharknado2',
                'password': 'badandboujee2',
                'db': 'sharknado2'}
db = MySQLdb.connect(host=cnx['host'],port=3306,user=cnx['username'],passwd=cnx['password'],db=cnx['db'])

text_file = open("data/prefillrows.txt", "r")
text = text_file.read()

lines = text.split("\n")

for line in lines:
    line = line.split(',')
    name = line[0]
    handle = line[1]
    mediaUrl = line[2]
    conf = line[3]
    airports = line[4]
    airports = airports.split('-')
    airports = ','.join(airports)
    airlines = line[5]
    linkURL = line[6]
    writeToDB(name, handle, mediaUrl, conf, airports, airlines, linkURL, db)