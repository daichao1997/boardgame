# -*- coding: utf-8 -*-

import pymysql

with open("db.txt") as file:
	games = file.readlines()

db = pymysql.connect("localhost","mysql","mysql",\
	"boardgameRecommendation",charset="utf8")
cursor = db.cursor()


cursor.execute("DROP TABLE IF EXISTS boardgame")

sql = '''CREATE TABLE boardgame(
			id VARCHAR(10),
			name VARCHAR(20),
			minNOP TINYINT NOT NULL,
			maxNOP TINYINT NOT NULL,
			minTime TINYINT NOT NULL,
			maxTime TINYINT NOT NULL,
			prevail TINYINT NOT NULL,
			content VARCHAR(10),
			setup TINYINT NOT NULL,
			label VARCHAR(30),
			intro TEXT NOT NULL,
			PRIMARY KEY(id)
			)DEFAULT CHARSET=utf8'''

cursor.execute(sql)

cursor.execute("DROP TABLE IF EXISTS barmanager")

sql = '''CREATE TABLE barmanager(
			-- manager VARCHAR(30),
			-- passwd VARCHAR(100),
			-- speakers VARCHAR(500),
			-- games VARCHAR(500),
			-- PRIMARY KEY(manager)
			userid VARCHAR(100),
			id VARCHAR(10)
			)DEFAULT CHARSET=utf8'''

cursor.execute(sql)	

# boardgame
cnt = -1
for game in games:

	if cnt == -1:
		cnt = 0
		continue

	info = game.strip().split()
	assert len(info) == 15

	name = info[0]
	if not info[1] == 'null':
		name += ','+info[1]
	
	minNOP = int(info[2])
	maxNOP = int(info[3])
	minTime = int(info[4])
	maxTime = int(info[5])
	prevail = int(info[6])
	content = info[7]
	setup = int(info[8])

	label = info[9]
	for i in range(10,14):
		if not info[i] == 'null':
			label += ','+info[i]
		else:
			break

	intro = info[14]

	sql = "INSERT INTO boardgame(id,name,minNOP,maxNOP,\
			 minTime,maxTime,prevail,content,setup,label,\
			 intro) VALUES('%d','%s',%d,%d,%d,%d,%d,'%s',%d,\
			 '%s','%s')" % (cnt,name,minNOP,maxNOP,minTime,\
			 maxTime,prevail,content,setup,label,intro)
	
	try:
	    cursor.execute(sql)
	    db.commit()
	except Exception as err:
		db.rollback()
		print(err)

	cnt += 1

# barmanager
# game = '0'
# for i in range(1,30):
# 	game += ','+str(i)

# sql = '''INSERT INTO barmanager(manager,games) \
# 			VALUES('-1default','%s')''' % game

# try:
#     cursor.execute(sql)
#     db.commit()
# except Exception as err:
# 	db.rollback()
# 	print(err)

db.close()