import requests
from constant import SERVER_SCKEY
def postServerMsg(msg):
    if len(SERVER_SCKEY) == 0:
        return
    url = "https://sc.ftqq.com/" + SERVER_SCKEY + ".send?text=" + msg
    requests.get(url)