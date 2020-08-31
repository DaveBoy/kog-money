import logging
import os
import time
from io import BytesIO

import numpy as np
from PIL import Image
from ppadb.client import Client as AdbClient
import random
client = AdbClient(host="127.0.0.1", port=5037)

device = client.devices()[0]

baseline = {}

SCREEN_PATH = 'screen.png'




# 屏幕分辨率
device_x, device_y = 1280, 720
base_x, base_y = 1280, 720


def init():
    find_screen_size()


def convert_cord(x,y):
    real_x = int(x / base_x * device_x)
    real_y = int(y / base_y * device_y)
    return real_x, real_y


def tap_screen(x, y):
    """calculate real x, y according to device resolution."""
    real_x, real_y = convert_cord(x, y)
    real_x=random.randint(real_x,real_x+10)
    real_y = random.randint(real_y, real_y + 10)
    device.shell('input tap {} {}'.format(real_x, real_y))


def stop_game():
    device.shell('am force-stop com.tencent.tmgp.sgame')  # 关闭游戏


def start_game():
    device.shell('monkey -p com.tencent.tmgp.sgame -c android.intent.category.LAUNCHER 1')  # 打开游戏

    time.sleep(60)

    tap_screen(643, 553)

    logging.info("等待1分钟")

    time.sleep(60)

    logging.info("关闭广告")
    for i in range(5):  # 关闭广告
        tap_screen(1174, 77)


def restart_game():
    stop_game()

    logging.info("休息10分钟")
    time.sleep(60 * 10)

    logging.info("重启游戏")

    start_game()


def tap_center(top_left, bottom_right):
    tap_screen((top_left[0] + bottom_right[0])/2, (top_left[1] + bottom_right[1])/2)



def swipe(x, y, x1, y1, duration):
    device.shell('input swipe {} {} {} {} {}'.format(x, y, x1, y1, duration))


def find_screen_size():
    global device_x
    global device_y
    img = pull_screenshot(False)
    device_x, device_y = img.size
    logging.info('device size x, y = ({}, {})'.format(device_x, device_y))




def pull_screenshot(resize=False, method=0, save_file=False):
    if save_file and os.path.exists(SCREEN_PATH):
        os.remove(SCREEN_PATH)

    if method == 0:
        result = device.screencap()
        img = Image.open(BytesIO(result))

        if save_file:
            with open(SCREEN_PATH, "wb") as fp:
                fp.write(result)
    else:
        os.system('adb shell screencap -p /sdcard/screen.png')
        os.system('adb pull /sdcard/screen.png {}'.format(SCREEN_PATH))
        img = Image.open(SCREEN_PATH)

    if resize and img.size != (base_x, base_y):
        return img.resize((base_x, base_y))
    else:
        return img
