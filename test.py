import logging

from img_match import find_img_position



# 日志输出
from logger import logger as logging



if __name__ == '__main__':
    #init()
    #pull_screenshot(False,1,True)
    res=find_img_position(True)
    if res is None:
        logging.debug("not match")
    else:
        logging.debug("{} found on:({},{})".format(res[0],res[1],res[2]))