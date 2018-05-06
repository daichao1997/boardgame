# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import jsonify
import extract
import pymysql


token = ['.','?','!','。','？','！']
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


db = pymysql.connect("localhost","mysql","mysql",\
    "boardgameRecommendation",charset="utf8")
cursor = db.cursor()


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


def error_json(version, reqId):
    return jsonify(version = version,
                   requestId = reqId,
                   response = {
                    "outputSpeech": "对不起，没有找到您想要的。",
                    "reprompt": {
                      "outputSpeech": "对不起，我没听懂您的意思。"
                    },
                    "directives": [],
                    "shouldEndSession": False
                   })


def return_json(res, version, reqId, isEnd=False):
    return jsonify(version = version,
                   requestId = reqId,
                   response = {
                    "outputSpeech": res,
                    "reprompt": {
                      "outputSpeech": "对不起，我没听懂您的意思。"
                    },
                    "directives": [],
                    "shouldEndSession": isEnd
                   })


app = Flask(__name__)

@app.route("/", methods=["POST"])
def handle_post():
    
    json =  request.get_json()
    # print(json)
    
    req = json["request"] # requestId & utterance
    # usr = json["session"]["user"] # userId
    text = req["utterance"]
    # if text[-1] in token:
    #     text = text[:-1]
    print(text)

    rslt = extract.extract(text)
    # print(rslt)
    
    print(rslt["type"])
    # init
    if rslt["type"] == 3: 
        res = "您好，欢迎使用芭乐桌游，请问需要我做些什么？"    
        return return_json(res = res, version = json["version"], reqId = req["requestId"])

    # exit
    elif rslt["type"] == 4:
        res = "谢谢您的使用，再见"
        return return_json(res = res, version = json["version"], reqId = req["requestId"], isEnd = True)
    
    # recommendation
    elif rslt["type"] == 0:
        if "时长" in rslt:
            time = parse_label(rslt, 0)
            print(time)
            if time != -1:
                sql = "SELECT name FROM boardgame WHERE \
                       minTime <= %d AND maxTime >= %d \
                       ORDER BY prevail DESC" % (time, time)
                try:
                    cursor.execute(sql)
                    games = cursor.fetchall()
                    if len(games) == 0:
                        res = "对不起，没有找到满足您要求的桌游。"
                    else:
                        res = "为您推荐"
                        for i in range(0,min(3,len(games))):
                            res += "," + str(i+1) + ":" + games[i][0]                 
                    return return_json(res = res, version = json["version"], reqId = req["requestId"])
                
                except Exception as e:
                    print(e)
                    return error_json(version = json["version"], reqId = req["requestId"])

            else:
                return error_json(version = json["version"], reqId = req["requestId"])
        
        elif "人数" in rslt:
            nop = parse_label(rslt, 1)
            print(nop)
            if nop != -1:
                sql = "SELECT name FROM boardgame WHERE \
                       minNOP <= %d AND maxNOP >= %d \
                       ORDER BY prevail DESC" % (nop, nop)
                try:
                    cursor.execute(sql)
                    games = cursor.fetchall()
                    if len(games) == 0:
                        res = "对不起，没有找到满足您要求的桌游。"
                    else:
                        res = "为您推荐"
                        for i in range(0,min(3,len(games))):
                            res += "," + str(i+1) + ":" + games[i][0]               
                    return return_json(res = res, version = json["version"], reqId = req["requestId"])
                
                except Exception as e:
                    print(e)
                    return error_json(version = json["version"], reqId = req["requestId"])
            
            else:
                return error_json(version = json["version"], reqId = req["requestId"])

        elif "标签" in rslt:
            label = parse_label(rslt, 2)
            print(label)
            if label != "":
                sql = "SELECT name FROM boardgame WHERE \
                       label1 = '%s' OR label2 = '%s' OR label3 = '%s' \
                       OR label4 = '%s' OR label5 = '%s' \
                       ORDER BY prevail DESC" % \
                       (label,label,label,label,label)
                try:
                    cursor.execute(sql)
                    games = cursor.fetchall()
                    if len(games) == 0:
                        res = "对不起，没有找到满足您要求的桌游。"
                    else:
                        res = "为您推荐"
                        for i in range(0,min(3,len(games))):
                            res += "," + str(i+1) + ":" + games[i][0]             
                    return return_json(res = res, version = json["version"], reqId = req["requestId"])
                
                except Exception as e:
                    print(e)
                    return error_json(version = json["version"], reqId = req["requestId"])

            else:
                return error_json(version = json["version"], reqId = req["requestId"])
        
        else:
            return error_json(version = json["version"], reqId = req["requestId"])
        
    # introduction    
    elif rslt["type"] == 1:
        if "桌游名" in rslt:       
            game_name = rslt["桌游名"]
            print(game_name)
            sql = "SELECT intro FROM boardgame WHERE \
                   name = '%s'" % game_name
            try:
                cursor.execute(sql)
                intro = cursor.fetchall()
                if len(intro) == 0:
                    res = "对不起，没有找到满足您要求的桌游。"
                else:
                    res = intro[0][0]
                    res += "希望您喜欢这款游戏！"                
                return return_json(res = res, version = json["version"], reqId = req["requestId"], isEnd = False)
            
            except Exception as e:
                print(e)
                return error_json(version = json["version"], reqId = req["requestId"])
        else:
            return error_json(version = json["version"], reqId = req["requestId"])
   
    # requery
    elif rslt["type"] == 2:
        if "桌游名" in rslt:       
            game_name = rslt["桌游名"]
            print(game_name)
        else:
            return error_json(version = json["version"], reqId = req["requestId"])

        if "时长" in rslt:
            time = parse_label(rslt, 0)
            print(time)
            sql = "SELECT minTime, maxTime FROM boardgame \
                   WHERE name = '%s'" % (game_name)
            
            try:
                cursor.execute(sql)
                query = cursor.fetchall()
                if len(query) == 0:
                    res = "对不起，没有找到相应的答案。"
                else:
                    res = "需要" + str(query[0][0]) + "到" + str(query[0][1]) + "分钟"
                    if time != -1:
                        if query[0][0]<=time and query[0][1]>=time:
                            res = "可以," + res
                        else:
                            res = "不可以," + res
                return return_json(res = res, version = json["version"], reqId = req["requestId"])
            
            except Exception as e:
                print(e)
                return error_json(version = json["version"], reqId = req["requestId"])
        
        elif "人数" in rslt:
            nop = parse_label(rslt, 1)
            print(nop)
            sql = "SELECT minNOP, maxNOP FROM boardgame \
                   WHERE name = '%s'" % (game_name)
            
            try:
                cursor.execute(sql)
                query = cursor.fetchall()
                if len(query) == 0:
                    res = "对不起，没有找到相应的答案。"
                else:
                    res = "需要" + str(query[0][0]) + "到" + str(query[0][1]) + "人"
                    if nop != -1:
                        if query[0][0]<=nop and query[0][1]>=nop:
                            res = "可以," + res
                        else:
                            res = "不可以," + res
                return return_json(res = res, version = json["version"], reqId = req["requestId"])
            
            except Exception as e:
                print(e)
                return error_json(version = json["version"], reqId = req["requestId"])
        
        elif "标签" in rslt:
            label = parse_label(rslt, 2)
            print(label)
            sql = "SELECT label1,label2,label3,label4,label5 \
                   FROM boardgame WHERE name = '%s'" % (game_name)
            
            try:
                cursor.execute(sql)
                query = cursor.fetchall()
                if len(query) == 0:
                    res = "对不起，没有找到相应的答案。"
                
                flag = False
                for tmp in query[0]:
                    if tmp == "null":
                        break
                    if tmp == label:
                        flag = True
                if flag:
                    res = "是的"
                else:
                    res = "不是的"
                return return_json(res = res, version = json["version"], reqId = req["requestId"])
            
            except Exception as e:
                print(e)
                return error_json(version = json["version"], reqId = req["requestId"])
        
        else:
            return error_json(version = json["version"], reqId = req["requestId"])
    
    # failed: -1
    else:       
        return error_json(version = json["version"], reqId = req["requestId"])


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=22101)