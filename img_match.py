import logging
import os

import aircv as ac
import cv2
import numpy as np
from PIL import Image

from constant import PC_PROJECT_ROOT, SCREEN_PATH, PC_RECONGNIZE_TEST, getRecognizeTarget,getTargetImgs

from logger import logger as logging





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

    for template in getTargetImgs():
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
            logging.debug('match result =  {}'.format(res['confidence']))
            logging.debug('match position =  ({},{})'.format(x, y))

            if debugEveryOne is True:
                logging.debug('match Img :{}'.format(template))

                # show the rect of find subImage
                rect = res['rectangle']
                crop_file = template.replace(getRecognizeTarget(), PC_RECONGNIZE_TEST)
                if os.path.exists(crop_file):
                    os.remove(crop_file)
                Image.open('{}{}'.format(PC_PROJECT_ROOT,SCREEN_PATH)).crop((rect[0][0],
                                                                    rect[0][1],
                                                                     rect[3][0],
                                                                     rect[3][1],)).save(crop_file)
            else:
                return template,x, y
        elif debugEveryOne is True:
                logging.debug('not match Img :{}'.format(template))
    return None
