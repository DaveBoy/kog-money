import logging
import aircv as ac

import glob
# 日志输出
logging.basicConfig(format='[%(asctime)s][%(name)s:%(levelname)s(%(lineno)d)][%(module)s:%(funcName)s]:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S',
                    level=logging.INFO)

target_imgs=glob.glob('maoxian/*')

def matchImg(imgsrc, imgobj, confidencevalue=0.8):  # imgsrc=原始图像，imgobj=待查找的图片
    imsrc = ac.imread(imgsrc)
    imobj = ac.imread(imgobj)
    match_result = ac.find_template(imsrc, imobj, confidencevalue)
    if match_result is not None:
        match_result['shape'] = (imsrc.shape[1], imsrc.shape[0])  # 0为高，1为宽
    return match_result


def find_img_position(debugEveryOne=False):
    for template in target_imgs:
        res = matchImg('screen.png',template)
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
            else:
                return template,x, y
    return None


