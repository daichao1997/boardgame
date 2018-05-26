# -*- coding: utf-8 -*-
import re

# 词语表
什么 = "((有|是)?(没有|什么|哪些)(是)?)"
是 = "是"
吗 = "(吗|嘛|么)"
吗问 = "(" + 吗 + "?)"
啊 = "(啊|呀|哪|呢|嘛|嗯|呵|哈|哼|嘿)"
啊问 = "(" + 啊 + "?)"

怎么 = "(怎|怎么|怎样|怎么样|怎么着|咋|咋着|如何)"
桌游 = "((的)?(桌游|游戏))"
能 = "((能|适合|可以|应|该|应该|应当))"
能问 = "(" + 能 + "?)"

数位 = "(零|半|一|二|双|两|俩|三|仨|四|五|六|七|八|九|十|0|1|2|3|4|5|6|7|8|9)"
基本数字 = "(" + 数位 + "*)"
人数 = "(" + r"(?P<人数>" + 基本数字 + ")" + "个人" + ")"

玩 = "玩"
玩完 = "(" + 玩 + "(完)?" + ")"

推荐问 = "(查|找|推荐|有没有|什么|哪|我想|我要|介绍)"
介绍问 = "(讲一下|讲讲|介绍|说明|解释)"

# 示例
桌游名表 = '''(富饶之城|达芬奇密码|德国心脏病|抵抗组织|大富翁|地产大亨|\
            只言片语|谁知我心|狼人杀|三国杀|uno|UNO|Uno|乌诺|乌诺纸牌|\
            角斗士棋|格格不入|俄罗斯方块棋|宿命|星杯|星杯传说|阿瓦隆|\
            冷战热斗|卡坦岛|风声|波多黎各|矮人矿工|矮人矿坑|卡卡颂|\
            卡卡城|历史巨轮|电力公司|发电厂|怒海求生|救生艇|山屋惊魂|\
            小黑屋|冰与火之歌|权力的游戏|马尼拉|僵尸广场)'''
桌游名 = r"(?P<桌游名>" + 桌游名表 + ")"

规则 = "(的?(游戏)?(规则|玩法))"
规则问 = "(" + 规则 + "?)"

时长 = r"(?P<时长>" + 基本数字 + "(个)?(小时|钟头|分钟|分))"
时长内 = "(" + 时长 + "(内)?" + ")"

# 示例
标签表 = "(策略|博弈|刺激|轻松|欢乐|欢快|费脑|烧脑|智商|逻辑|动脑|思考|经营|赚钱|开店|伪装|演技|演戏|敏捷|反应|手速|手牌管理|打牌|扮演|容易上手)"
标签 = r"(" + "(是)?" + "(" + "?P<标签>" + 标签表 + ")" + "(的)?" + ")"

几 = "(几|多少)"
几个人 = "(" + 几 + "(个)?人" + ")"

多长时间内 = "((在)?(多长时间|多久)(内)?)"

启动 = "((打开|启动|进入)(芭乐|八的|八月|八路)(左右|中有|猪油|桌游)(在吗)?)"
退出 = "(退出|再见|滚蛋|滚吧|去死|掰掰|拜拜|休息|闭嘴)"

继续推荐 = "再来|继续|接着|(换|下)一(批|个)|不要|还要|还有(吗|呢)|我觉得不行"

管理桌游 = "管理(桌游|猪油|左右|中有)"

有没有 = "有没有|这家店有|这里有|这儿有"

def extract(sentence):
    player = re.compile(人数).search(sentence)
    duration = re.compile(时长).search(sentence)
    label = re.compile(标签).search(sentence)
    ask_player = re.compile(几个人).search(sentence)
    ask_duration = re.compile(多长时间内).search(sentence)
    
    name = re.compile(桌游名).search(sentence)

    nextround = re.compile(继续推荐).search(sentence)
    
    manage = re.compile(管理桌游).match(sentence)
    
    start = re.compile(启动).match(sentence)
    shutdown = re.compile(退出).match(sentence)
    
    exist = re.compile(有没有).search(sentence)
    
    # 启动
    if not (start is None):
        return {"type" : 3}
    # 退出    
    if not (shutdown is None):
        return {"type" : 4}
    
    if not (nextround is None):
        return {"type" : 5}
    
    if not (manage is None):
        return {"type" : 6}
    
    if not (name is None):
        # 询问：有名字，有特征
        if not (player is None):
            return {"type" : 2, "人数" : player.group("人数"), "桌游名" : name.group("桌游名")}
        if not (ask_player is None):
            return {"type" : 2, "人数" : "问", "桌游名" : name.group("桌游名")}
        if not (duration is None):
            return {"type" : 2, "时长" : duration.group("时长"), "桌游名" : name.group("桌游名")}
        if not (ask_duration is None):
            return {"type" : 2, "时长" : "问", "桌游名" : name.group("桌游名")}
        if not (label is None):
            return {"type" : 2, "标签" : label.group("标签"), "桌游名" : name.group("桌游名")}
        if not (exist is None):
            return {"type" : 7, "桌游名": name.group("桌游名")}
        # 介绍：有名字，无特征
        else:
            return {"type" : 1, "桌游名" : name.group("桌游名")}
    else:
        # 推荐：无名字，有特征
        if not (player is None):
            return {"type" : 0, "人数" : player.group("人数")}
        if not (duration is None):
            return {"type" : 0, "时长" : duration.group("时长")}
        if not (label is None):
            return {"type" : 0, "标签" : label.group("标签")}

    return {"type": -1}

def extract_test(sentence):
    print(sentence)
    print(extract(sentence))

if __name__ == "__main__":
    #介绍
    extract_test("让芭乐桌游帮我查一下三国杀")
    extract_test("狼人杀怎么玩")
    #推荐
    extract_test("有没有就是那种超级无敌紧张刺激的蛇皮桌游？")
    extract_test("有什么桌游需要演技")
    extract_test("查一下五个人玩的桌游")
    extract_test("有什么一个小时内能玩完的桌游")
    #继续推荐
    extract_test("继续嘛")
    extract_test("人家还要")
    extract_test("这都什么垃圾桌游，下一个")
    extract_test("我觉得不行")
    #询问
    extract_test("三国杀多长时间内能玩完啊")
    extract_test("Uno是轻松愉快的桌游吗")
    #有没有
    extract_test("你们这儿有三国杀吗")
    extract_test("有没有大富翁")
    #管理
    extract_test("管理桌游")
    #开关
    extract_test("打开芭乐桌游")
    extract_test("滚吧")
    pass
