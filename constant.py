import glob
import os.path
import logging
import configparser

SCREEN_FILE_NAME = "screen"
SCREEN_FILE_TYPE = ".png"
SCREEN_PATH = '{}{}'.format(SCREEN_FILE_NAME, SCREEN_FILE_TYPE)
PC_PROJECT_ROOT = "{}\\".format(os.getcwd())
PC_CROP_PARENT_NAME = "screen_crop"
PC_CROP_PARENT_PATH = "{}\\".format(PC_CROP_PARENT_NAME)
PC_RECONGNIZE_TEST = "maoxian_crop"

SCREEN_METHOD = 1
# 0：python自带的方式，实际原理类似3
# 1：推荐方式
#
# 3：普通模式，0出问题的时候(看根目录下生成的screen.png是否正常)用，比如腾讯手游助手就需要设置为3
#
# 2：对方法3时生成带时间戳的文件名（如：screen_1616773251284.png）的解决方式，目前就遇到小米会这样

LOG_FILE_SWITCH = True
LOG_FILE_LEVEL = logging.DEBUG
LOG_CONSOLE_LEVEL = logging.DEBUG
LOG_SERVER_LEVEL = logging.WARNING

PAUSE_COUNT = -1  # 多少次暂停一次  不暂停设为-1，防止检测用的，不知道有没有用

config = configparser.ConfigParser()
config.read("config.ini")
SERVER_SCKEY = config.get("Key", "SERVER_SCKEY") # http://sc.ftqq.com/?c=code

SERVER_TIMES = 10
MAX_TIME = 240  # 一局需要的最长时间 检测卡主的时间  如果一次完成之后这么久还没完成下一次，就算做卡主了，结束游戏，不然一直卡主挂机浪费在线时间
MIN_TIME = 60  # 一局需要的最短时间 检测卡主
WAIT_SHOW_GOD = True  # 是否要在再次挑战之前等几秒钟，因为某些低端机比较卡，可能显示不出

device_x = 1280
device_y = 720
PC_RECOGNIZE_TARGET = "maoxian_{}".format(device_x)
target_imgs = glob.glob('{}/*'.format(PC_RECOGNIZE_TARGET))


def setDeviceSize(x, y):
    global PC_RECOGNIZE_TARGET
    global target_imgs
    global device_x
    global device_y
    device_x = x
    device_y = y

    PC_RECOGNIZE_TARGET = "maoxian_{}".format(device_x)
    target_imgs = glob.glob('{}/*'.format(PC_RECOGNIZE_TARGET))


def getDeviceSize():
    return device_x, device_y


def getRecognizeTarget():
    return PC_RECOGNIZE_TARGET


def getTargetImgs():
    return target_imgs
