import logging
import aircv as ac
import os
import numpy as np
import cv2
import time

import glob
from PIL import Image

from constant import PC_PROJECT_ROOT,PC_CROP_PARENT_NAME,PC_CROP_PARENT_PATH,SCREEN_FILE_NAME,SCREEN_FILE_TYPE,SCREEN_PATH,PC_RECONGNIZE_TEST,PC_RECONGNIZE_TARGET

from skimage.feature import match_template
from matplotlib import pyplot as plt

# 日志输出

logging.basicConfig(format='[%(asctime)s][%(name)s:%(levelname)s(%(lineno)d)][%(module)s:%(funcName)s]:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S',
                    level=logging.INFO)

target_imgs=glob.glob('{}/*'.format(PC_RECONGNIZE_TARGET))



def matchImg(src_path, obj_path, confidencevalue=0.8):  # imgsrc=原始图像，imgobj=待查找的图片
    imsrc = cv2.imdecode(np.fromfile(src_path,dtype=np.uint8),-1)
    imobj = cv2.imdecode(np.fromfile(obj_path,dtype=np.uint8),-1)
    match_result = ac.find_template(imsrc, imobj, confidencevalue)
    if match_result is not None:
        match_result['shape'] = (imsrc.shape[1], imsrc.shape[0])  # 0为高，1为宽
    return match_result



def find_img_position(debugEveryOne=False):
    if debugEveryOne and not os.path.exists(PC_RECONGNIZE_TEST):
        os.makedirs(PC_RECONGNIZE_TEST)

    for template in target_imgs:
        if not os.path.exists(SCREEN_PATH):
            time.sleep(1)
        res = matchImg('{}{}'.format(PC_PROJECT_ROOT,SCREEN_PATH),template,confidencevalue=0.9)
        # {'confidence': 0.5435812473297119, 'rectangle': ((394, 384), (394, 416), (450, 384), (450, 416)), 'result': (422.0, 400.0)
        # confidence：匹配相似率
        #
        # rectangle：匹配图片在原始图像上四边形的坐标
        #
        # result：匹配图片在原始图片上的中心坐标点，也就是我们要找的点击点
        # 如果结果匹配到的confidence小于入参传递的相似度confidence，则会返回None，不返回字典
        if res is not None:
            x, y = res['result']
            logging.info('match result =  {}'.format(res['confidence']))
            logging.info('match position =  ({},{})'.format(x, y))

            if debugEveryOne is True:
                logging.info('match Img :{}'.format(template))
                # show the rect of find subImage
                rect = res['rectangle']
                crop_file = template.replace(PC_RECONGNIZE_TARGET,PC_RECONGNIZE_TEST)
                if os.path.exists(crop_file):
                    os.remove(crop_file)
                Image.open('{}{}'.format(PC_PROJECT_ROOT,SCREEN_PATH)).crop((rect[0][0],
                                                                    rect[0][1],
                                                                     rect[3][0],
                                                                     rect[3][1],)).save(crop_file)
            else:
                return template,x, y
    return None


def matchAllImg(imgsrc, imgobj, confidencevalue=0.8):  # imgsrc=原始图像，imgobj=待查找的图片
    #imsrc = cv2.imdecode(np.fromfile(imgsrc,dtype=np.uint8),-1)
    #imobj = cv2.imdecode(np.fromfile(imgobj,dtype=np.uint8),-1)
    imsrc = ac.imread(imgsrc)
    imobj = ac.imread(imgobj)
    match_result = ac.find_all_template(imsrc, imobj, confidencevalue)
    print(match_result)