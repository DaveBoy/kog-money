import glob
import os.path
import logging

SCREEN_FILE_NAME = "screen"
SCREEN_FILE_TYPE = ".png"
SCREEN_PATH = '{}{}'.format(SCREEN_FILE_NAME, SCREEN_FILE_TYPE)
PC_PROJECT_ROOT = "{}\\".format(os.getcwd())
PC_CROP_PARENT_NAME = "screen_crop"
PC_CROP_PARENT_PATH = "{}\\".format(PC_CROP_PARENT_NAME)
PC_RECONGNIZE_TEST = "maoxian_crop"

SCREEN_METHOD = 0  # 0一般手机都行  1是0截图出问题的时候用，比如腾讯手游助手就需要设置为1

LOG_FILE_SWITCH = True
LOG_FILE_LEVEL = logging.INFO
LOG_CONSOLE_LEVEL = logging.DEBUG

PAUSE_COUNT = 30  # 多少次暂停一次  不暂停设为-1，防止检测用的，不知道有没有用

device_x = 1280
device_y = 720
PC_RECONGNIZE_TARGET = "maoxian_{}".format(device_x)
target_imgs = glob.glob('{}/*'.format(PC_RECONGNIZE_TARGET))


def setDeviceSize(x, y):
    global PC_RECONGNIZE_TARGET
    global target_imgs
    global device_x
    global device_y
    device_x = x
    device_y = y

    PC_RECONGNIZE_TARGET = "maoxian_{}".format(device_x)
    target_imgs = glob.glob('{}/*'.format(PC_RECONGNIZE_TARGET))


def getDeviceSize():
    return device_x, device_y


def getRecongnizeTarget():
    return PC_RECONGNIZE_TARGET


def getTargetImgs():
    return target_imgs


