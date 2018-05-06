# -*- coding: utf-8 -*-

import pymysql

with open("db.txt") as file:
	games = file.readlines()

for i in range(0,len(games)):
	games[i] = games[i].strip('\n')

db = pymysql.connect("localhost","mysql","mysql",\
	"boardgameRecommendation",charset="utf8")
cursor = db.cursor()


cursor.execute("DROP TABLE IF EXISTS boardgame")

sql = '''CREATE TABLE boardgame(
			name VARCHAR(10),
			alias VARCHAR(10),
			minNOP INT NOT NULL,
			maxNOP INT NOT NULL,
			minTime INT NOT NULL,
			maxTime INT NOT NULL,
			prevail INT NOT NULL,
			content VARCHAR(10),
			setup INT NOT NULL,
			label1 VARCHAR(10),
			label2 VARCHAR(10),
			label3 VARCHAR(10),
			label4 VARCHAR(10),
			label5 VARCHAR(10),
			intro TEXT NOT NULL,
			PRIMARY KEY(name)
			)DEFAULT CHARSET=utf8'''

cursor.execute(sql)

for game in games:

	info = game.split()
	assert len(info) == 15
	# for i in range(0,len(info)):

	# 	if info[i] == "null":
	# 		info[i] = ""

	name = info[0]
	alias = info[1]
	minNOP = int(info[2])
	maxNOP = int(info[3])
	minTime = int(info[4])
	maxTime = int(info[5])
	prevail = int(info[6])
	content = info[7]
	setup = int(info[8])
	label1 = info[9]
	label2 = info[10]
	label3 = info[11]
	label4 = info[12]
	label5 = info[13]
	intro = info[14]

	sql = "INSERT INTO boardgame(name,alias,minNOP,\
			 maxNOP,minTime,maxTime,prevail,content,setup,\
			 label1,label2,label3,label4,label5,intro)\
			 VALUES('%s','%s',%d,%d,%d,%d,%d,'%s',%d,'%s',\
			 '%s','%s','%s','%s','%s')" % (name,alias,\
			 minNOP,maxNOP,minTime,maxTime,prevail,content,setup,\
			 label1,label2,label3,label4,label5,intro)
	
	try:
	    cursor.execute(sql)
	    db.commit()
	except Exception as err:
		db.rollback()
		print(err)

db.close()
