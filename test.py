
from img_match import find_img_position
from util import init,pull_screenshot,check_game_state,SCREEN_METHOD



# 日志输出
from logger import logger as logging



if __name__ == '__main__':
    init()
    pull_screenshot(SCREEN_METHOD,True)
    res=find_img_position(True)
    if res is None:
        logging.debug("not match")
    else:
        logging.debug("{} found on:({},{})".format(res[0],res[1],res[2]))
