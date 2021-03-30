from img_match import find_img_position
from util import init, pull_screenshot,pull_screenshot_fix, check_game_state, SCREEN_METHOD, setDeviceSize

# 日志输出
from logger import logger as logging
from multiprocessing import Value
from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool

import os

if __name__ == '__main__':
     os.system('taskkill /f /im %s' % 'cmd.exe')

     # init()
    # pull_screenshot(SCREEN_METHOD,True)
    # res = find_img_position(True)
    # if res is None:
    #     logging.debug("not match")
    # else:
    #     logging.debug("{} found on:({},{})".format(res[0], res[1], res[2]))
