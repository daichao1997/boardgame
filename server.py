# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import jsonify
from Crypto.Cipher import AES
import base64
import urllib
import extract
import pymysql, os
import random, string
import time as time_pkg

# token = ['.','?','!','。','？','！']
trans_num = {
    "半": 0.5,
    "一": 1,
    "单": 1,
    "二": 2,
    "双": 2,
    "两": 2,
    "俩": 2,
    "三": 3,
    "仨": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10
}

label_index = ["策略","费脑","经营","伪装","手牌管理","欢乐","敏捷"]
trans_1abel=[
    ["策略","博弈","谋略","算计","战略","计谋"],
    ["费脑","烧脑","高智商","动脑","思考","逻辑"],
    ["经营","赚钱","开店","商业","做生意","像大富翁"],
    ["伪装","演技","演戏","戏精","说谎","假话","谎言"],
    ["手牌管理","打牌","像三国杀"],
    ["欢乐","欢快","活跃","活泼"],
    ["敏捷","反应","手速","反射弧"]
]

defaultRes = "对不起，我没有找到您想要的";
defaultDB = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29'


def dbConnet():

    conn = pymysql.connect(host="localhost",user="mysql",passwd="mysql",\
        db="boardgameRecommendation",charset="utf8",autocommit=True)
    cursor = conn.cursor()
    return cursor


def parse_label(labelDic, typeIndex):
    # time
    if typeIndex == 0:
        time = labelDic["时长"]
        term = 1
        if time[-1] == "时" or time[-1] == "头":
            term = 60
            time = time[:-2]
        elif time[-1] == "钟":
            time = time[:-2]
        elif time[-1] == "分":
            time = time[:-1]
        
        if time[-1] == "个":
            time = time[:-1]

        if time.isdigit():
            return term*float(time)
        elif time in trans_num:
            return term*trans_num[time]
        else:
            return -1

    # num of players
    elif typeIndex == 1:
        num = labelDic["人数"]
        if num.isdigit():
            return float(num)
        elif num in trans_num:
            return trans_num[num]
        else:
            return -1

    # label
    elif typeIndex == 2:
        label = labelDic["标签"]
        for i in range(0,len(label_index)):
            if label in trans_1abel[i]:
                label = label_index[i]
                break
        return label


def return_json(version, reqId, res=defaultRes, isEnd=False):
    return jsonify(version = version,
                   requestId = reqId,
                   response = {
                    "outputSpeech": res,
                    "reprompt": {
                      "outputSpeech": "对不起，我没听清，可以再试试吗"
                    },
                    "directives": [],
                    "shouldEndSession": isEnd
                   })


def trans_sql(reqType, sqlType, attrList):
    '''
    reqType:
        0 recommendation
        1 introduction
        2 query
    sqlType:
        0 time
        1 num of players
        2 label
    '''
    # recom: usrdb
    if reqType == 0:        
        if sqlType == 0:            
            sql = "SELECT name FROM boardgame WHERE \
                   minTime <= %d AND maxTime >= %d AND \
                   FIND_IN_SET(id,'%s') ORDER BY prevail DESC"\
                    % (attrList[0], attrList[0], attrList[1])
        
        elif sqlType == 1:            
            sql = "SELECT name FROM boardgame WHERE \
                   minNOP <= %d AND maxNOP >= %d AND \
                   FIND_IN_SET(id,'%s') ORDER BY prevail DESC"\
                    % (attrList[0], attrList[0], attrList[1])

        elif sqlType == 2:            
            sql = "SELECT name FROM boardgame WHERE \
                   FIND_IN_SET('%s',label) AND \
                   FIND_IN_SET(id,'%s') \
                   ORDER BY prevail DESC" % \
                   (attrList[0], attrList[1])

        elif sqlType == 3:
            sql = "SELECT name FROM boardgame WHERE \
                   FIND_IN_SET(id,'%s') \
                   ORDER BY prevail DESC" % \
                   (attrList[0])

    elif reqType == 1:       
        sql = "SELECT intro FROM boardgame WHERE \
                   FIND_IN_SET('%s',name)" % attrList[0]
    
    elif reqType == 2:        
        if sqlType == 0:            
            sql = "SELECT minTime, maxTime FROM boardgame \
                   WHERE FIND_IN_SET('%s',name)" % attrList[0]

        elif sqlType == 1:            
            sql = "SELECT minNOP, maxNOP FROM boardgame \
                   WHERE FIND_IN_SET('%s',name)" % attrList[0]
    
    return sql


def logReq(strs):

    with open("log.txt", "a") as fp:
        for line in strs:
            fp.write(line+"\n")
        fp.write("\n")


app = Flask(__name__)

@app.route("/", methods=["POST"])
def handle_post():
    
    json =  request.get_json()
    # print(json)
    
    req = json["request"] # requestId & utterance
    usr = json["session"]["user"]["userId"]
    text = req["utterance"]
    log = []
    log.append(time_pkg.strftime("%Y-%m-%d %H:%M:%S", time_pkg.localtime()))
    log.append("usr:"+usr)
    print(usr)
    log.append("req:"+text)
    print(text)

    rslt = extract.extract(text)
    
    log.append("type:"+str(rslt["type"]))
    print(rslt["type"])

    # init
    if rslt["type"] == 3: 
        res = "您好，欢迎使用芭乐桌游，请问需要我做些什么"
        log.append(res)
        logReq(log)  
        return return_json(res = res, version = json["version"], reqId = req["requestId"])

    # exit
    elif rslt["type"] == 4:
        res = "谢谢您的使用，再见"
        log.append(res)
        logReq(log)
        return return_json(res = res, version = json["version"], reqId = req["requestId"], isEnd = True)

    # recommendation again
    elif rslt["type"] == 5:
        filename = "gameCache/"+usr+".txt"
        if os.path.exists(filename):
            with open(filename,"r") as recomFile:
                games = recomFile.read().split()
            with open(filename,"w") as recomFile:
                n = int(games[0])
                if n <= 0:
                    res = "对不起，没有其他满足您要求的桌游了"
                    recomFile.write("0")
                else:
                    recomFile.write(str(n-3))
                    res = "为您推荐"
                    for i in range(1,n+1):
                        if i<4:
                            res += "," + str(i) + ":" + games[i]
                        else:
                            recomFile.write(" "+games[i])
            log.append(res)
            logReq(log)
            return return_json(res = res, version = json["version"], reqId = req["requestId"]) 
        else:
            res = "您之前还没让我给您推荐过桌游哟"
            log.append(res)
            logReq(log)
            return return_json(res = res, version = json["version"], reqId = req["requestId"])
    
    # manager
    elif rslt["type"] == 6:
        # BLOCK_SIZE = 32
        # PADDING = '{'

        # pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
        # EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
        # DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

        # secret = "HELLO_I_AM_A_KEY"
        # iv = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
        # #iv = "HELLO_I_AM_A_KEY"
        # cipher=AES.new(key=secret,mode=AES.MODE_CBC,IV=iv)
        # encoded = EncodeAES(cipher, usr)

        # id_url = urllib.parse.quote_plus(encoded)
        # url = "http://v.internetapi.cn/boardgame/boardgame.php?userid="+id_url+"&iv="+iv
        code1 = random.choice(string.digits)
        code2 = random.choice(string.digits)
        code3 = random.choice(string.digits)
        code4 = random.choice(string.digits)
        code = code1 + code2 + code3 + code4
        timestamp = int(time_pkg.time())
        try:
            cursor = dbConnet()
            cursor.execute("DELETE FROM code WHERE userid='%s'" % usr)
            print("INSERT INTO code VALUES ('%s', '%s', '%d')" % (usr, code, timestamp))
            cursor.execute("INSERT INTO code VALUES ('%s', '%s', '%d')" % (usr, code, timestamp))
        except Exception as e:
            print(e)
            res = "插入数据库失败"
            return return_json(res=res, version = json["version"], reqId = req["requestId"])

        # log.append(res)
        logReq(log)
        return jsonify(version = json["version"],
                       requestId = req["requestId"],
                       response = {
                        "outputSpeech": "请打开管理链接，输入验证码。您的验证码是，"+code1+"，"+code2+"，"+code3+"，"+code4,
                        "reprompt": {
                          "outputSpeech": "请重新获取验证码"
                        },
                        "directives": [],
                        "shouldEndSession": True
                       })
    
    # has game
    elif rslt["type"] == 7:

        game_name = rslt["桌游名"]
        try:
            cursor = dbConnet()
            cursor.execute("SELECT id FROM boardgame WHERE FIND_IN_SET('%s',name)" % game_name)
            ids = cursor.fetchall()
            cursor.execute("SELECT id FROM barmanager WHERE userid='%s' AND id='%s'" % (usr,ids[0][0]))
            ifhas = cursor.fetchall()
            if len(ifhas) == 0:
                res = "这个没有诶"
            else:
                res = "这个有的"
            log.append(res)
            logReq(log)
            return return_json(res=res, version = json["version"], reqId = req["requestId"])

        except Exception as e:
            print(e)
            res = "数据库错误"
            return return_json(res=res, version = json["version"], reqId = req["requestId"])

    # recommendation
    elif rslt["type"] == 0:

        try:
            cursor = dbConnet()
            cursor.execute("SELECT id FROM barmanager WHERE userid='%s'" % usr)
            db = cursor.fetchall()
            if len(db) == 0:
                usrdb = defaultDB
            else:
                usrdb = ""
                for k in range(len(db)):
                    usrdb += db[k][0]+","
                usrdb = usrdb[:-1]

        except Exception as e:
            print(e)
            res = "数据库错误"
            return return_json(res=res, version = json["version"], reqId = req["requestId"])

        if "时长" in rslt:
            time = parse_label(rslt, 0)
            print("key:"+str(time))
            if time != -1:
                sql = trans_sql(0, 0, [time,usrdb])
            else:
                return return_json(version = json["version"], reqId = req["requestId"])
        
        elif "人数" in rslt:
            nop = parse_label(rslt, 1)
            print("key:"+str(nop))
            if nop != -1:
                sql = trans_sql(0, 1, [nop,usrdb])
            else:
                return return_json(version = json["version"], reqId = req["requestId"])

        elif "标签" in rslt:
            label = parse_label(rslt, 2)
            print("key:"+label)
            if label != "":
                sql = trans_sql(0, 2, [label,usrdb])
            else:
                return return_json(version = json["version"], reqId = req["requestId"])
        
        #elif "流行" in rslt:
         #   sql = trans_sql(0, 3, [usrdb])

        else:
           # return return_json(version = json["version"], reqId = req["requestId"])
            sql = trans_sql(0,3,[usrdb])

        try:
            cursor.execute(sql)
            games = cursor.fetchall()
            if len(games) == 0:
                res = "对不起，没有找到满足您要求的桌游"
            else:
                with open("gameCache/"+usr+".txt", "w") as recomFile:
                    recomFile.write(str(len(games)-3))
                    res = "为您推荐"
                    for i in range(len(games)):
                        game = games[i][0].split(',')          
                        if i<3:
                            res += "," + str(i+1) + ":" + game[0]
                        else:
                            recomFile.write(" "+game[0])
            log.append(res)
            logReq(log)
            return return_json(res = res, version = json["version"], reqId = req["requestId"])
        
        except Exception as e:
            print(e)
            res = "数据库错误"
            return return_json(res=res, version = json["version"], reqId = req["requestId"])
        
    # introduction    
    elif rslt["type"] == 1:
        if "桌游名" in rslt:       
            game_name = rslt["桌游名"]
            print("key:"+game_name)
            sql = trans_sql(1, -1, [game_name])
            try:
                cursor = dbConnet()
                cursor.execute(sql)
                intro = cursor.fetchall()
                if len(intro) == 0:
                    res = "对不起，没有找到满足您要求的桌游"
                else:
                    res = intro[0][0]
                    res += "希望您喜欢这款游戏" 
                log.append(res)
                logReq(log)               
                return return_json(res = res, version = json["version"], reqId = req["requestId"])
            
            except Exception as e:
                print(e)
                res = "数据库错误"
                return return_json(res=res, version = json["version"], reqId = req["requestId"])
        else:
            return return_json(version = json["version"], reqId = req["requestId"])
   
    # requery
    elif rslt["type"] == 2:
        if "桌游名" in rslt:       
            game_name = rslt["桌游名"]
            print("key:"+game_name)
        else:
            return return_json(version = json["version"], reqId = req["requestId"])
        
        noKey = False
        sqlType = 2
        if "时长" in rslt:
            time = parse_label(rslt, 0)
            if time == -1:
                noKey = True
            print("key:"+str(time))
            sqlType = 0
            sql = trans_sql(2, 0, [game_name])
                   
        elif "人数" in rslt:
            nop = parse_label(rslt, 1)
            if nop == -1:
                noKey = True
            print("key:"+str(nop))
            sqlType = 1
            sql = trans_sql(2, 1, [game_name])
        
        else:
            return return_json(version = json["version"], reqId = req["requestId"])

        try:
            cursor = dbConnet()
            cursor.execute(sql)
            query = cursor.fetchall()
            if len(query) == 0:
                res = "对不起，没有找到相应的答案"

            if noKey:
                res = "需要%d到%d" % (query[0][0],query[0][1])
                if sqlType == 0:
                    res += "分钟"
                elif sqlType == 1:
                    res += "人"
            else:
                flag = False      
                if sqlType == 0:
                    if time >= query[0][0] and time <= query[0][1]:
                        flag = True
                    res = "需要%d到%d分钟" % (query[0][0],query[0][1])
                elif sqlType == 1:
                    if nop >= query[0][0] and nop <= query[0][1]:
                        flag = True
                    res = "需要%d到%d人" % (query[0][0],query[0][1])
                
                if flag:
                    res = "可以，" + res
                else:
                    res = "不可以，" + res

            log.append(res)
            logReq(log)
            return return_json(res = res, version = json["version"], reqId = req["requestId"])
        
        except Exception as e:
            print(e)
            res = "数据库错误"
            return return_json(res=res, version = json["version"], reqId = req["requestId"])
    
    # failed: -1
    else:       
        return return_json(version = json["version"], reqId = req["requestId"])


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=22102)
