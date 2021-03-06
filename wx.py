import requests
from img import compress_image
import json
import time
import os

import configparser
import logging

# 读取配置文件
config = configparser.ConfigParser()
config.read("config.ini")
corpid = config.get("Key", "corpid")
agentid = int(config.get("Key", "agentid"))
corpsecret = config.get("Key", "corpsecret")
token = config.get("Key", "token")



httpDedbug=False

def sendWxMsg(msg):
    if httpDedbug:
        # 启用调试于 http.client 级别 (requests->urllib3->http.client)
        # 你将能看到 REQUEST，包括 HEADERS 和 DATA，以及包含 HEADERS 但不包含 DATA 的 RESPONSE。
        # 唯一缺少的是 response.body，它不会被 log 记录。
        try:
            from http.client import HTTPConnection
        except ImportError:
            from httplib import HTTPConnection
        HTTPConnection.debuglevel = 1

        logging.basicConfig()  # 初始化 logging，否则不会看到任何 requests 的输出。
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    try:
        jsonData = uploadFile()
        code = jsonData["errcode"]
        if code == 0:
            code = sendMsg(jsonData["media_id"], msg)
            if code == 42001:
                getToken()
                sendMsg(jsonData["media_id"], msg)
        elif code == 42001:
            getToken()
            jsonData = uploadFile()
            code = jsonData["errcode"]
            if code == 0:
                sendMsg(jsonData["media_id"], msg)
    except Exception as e:
        print(e)
        print("发送失败")


def sendMsg(media_id, msg):
    payload = {
        "touser": "@all",
        "msgtype": "mpnews",
        "agentid": agentid,
        "mpnews": {
            "articles": [
                {
                    "title": "王者金币脚本",
                    "thumb_media_id": media_id,
                    "digest": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n" + msg,
                    "content": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                }
            ]
        }
    }

    msgUrl = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token
    r = requests.post(url=msgUrl, data=json.dumps(payload))
    print(r.text)
    jsonData = json.loads(r.text)
    return jsonData["errcode"]


def getToken():
    r = requests.get(
        url="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + corpid + "&corpsecret=" + corpsecret)
    print(r.text)
    jsonData = json.loads(r.text)
    if jsonData["errcode"] == 0:
        global token
        token = jsonData["access_token"]
        config.set("Key", "token", token)
        config.write(open("config.ini", "w"))
    return jsonData["errcode"]


def uploadFile():
    uploadUrl = "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token=" + token + "&type=image"
    if not os.path.exists('pic'):
        os.makedirs('pic')
    files = {'file': open(compress_image('screen.png', 'pic/screen.png'), 'rb')}  # 图片文件foo.png需和脚本在同一个目录

    r = requests.post(uploadUrl, files=files)

    print(r.text)
    jsonData = json.loads(r.text)
    return jsonData


if __name__ == '__main__':
    sendWxMsg("已运行90次")
