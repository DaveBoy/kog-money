import logging
import aircv as ac

import glob
from PIL import Image
from img_match import find_img_position
from util import pull_screenshot
method = 'cv2.TM_SQDIFF'

# 日志输出
logging.basicConfig(format='[%(asctime)s][%(name)s:%(levelname)s(%(lineno)d)][%(module)s:%(funcName)s]:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S',
                    level=logging.INFO)



if __name__ == '__main__':
    pull_screenshot(False,1,True)
    res=find_img_position(True)
    if res is None:
        logging.info("not match")
    else:
        logging.info("{} found on:({},{})".format(res[0],res[1],res[2]))