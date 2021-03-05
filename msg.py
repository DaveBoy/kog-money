import requests
from constant import SERVER_SCKEY
from wx import sendWxMsg


def postServerMsg(msg, title="王者荣耀脚本通知"):
    sendWxMsg(msg)
    if len(SERVER_SCKEY) == 0:
        return
    url = "https://sc.ftqq.com/" + SERVER_SCKEY + ".send?text=" + title + "&desp=" + msg
    requests.get(url)


def postWxMsg(msg):
    sendWxMsg(msg)
