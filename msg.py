import requests
from constant import SERVER_SCKEY
def postServerMsg(msg,title="王者荣耀脚本通知"):
    if len(SERVER_SCKEY) == 0:
        return
    url = "https://sc.ftqq.com/" + SERVER_SCKEY + ".send?text=" + title+"&desp="+msg
    requests.get(url)