import logging
import os
import random
import time

import time

from img_match import find_img_position
import logging
from datetime import datetime

from io import BytesIO

from PIL import Image
from ppadb.client import Client as AdbClient

client = AdbClient(host="127.0.0.1", port=5037)

device = client.devices()[0]

baseline = {}

SCREEN_PATH = 'screen.png'

# 日志输出
logging.basicConfig(format='[%(asctime)s][%(name)s:%(levelname)s(%(lineno)d)][%(module)s:%(funcName)s]:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S',
                    level=logging.INFO)

# 屏幕分辨率
device_x, device_y = 1280, 720
base_x, base_y = 1280, 720


def init():
    find_screen_size()


def convert_cord(x, y):
    real_x = int(x / base_x * device_x)
    real_y = int(y / base_y * device_y)
    return real_x, real_y


def tap_screen(x, y):
    """calculate real x, y according to device resolution."""
    real_x, real_y = convert_cord(x, y)
    real_x = random.randint(real_x, real_x + 10)
    real_y = random.randint(real_y, real_y + 10)
    device.shell('input tap {} {}'.format(real_x, real_y))


def stop_game():
    device.shell('am force-stop com.tencent.tmgp.sgame')  # 关闭游戏


def start_game():
    device.shell('monkey -p com.tencent.tmgp.sgame -c android.intent.category.LAUNCHER 1')  # 打开游戏

    time.sleep(60)

    tap_screen(643, 553) #选区界面 开始游戏

    logging.info("等待1分钟")

    time.sleep(60)

    logging.info("关闭广告")
    check_game_state(True)


def restart_game():
    stop_game()

    logging.info("休息10分钟")
    time.sleep(60 * 10)

    logging.info("重启游戏")

    start_game()


def tap_center(top_left, bottom_right):
    tap_screen((top_left[0] + bottom_right[0]) / 2, (top_left[1] + bottom_right[1]) / 2)


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
        if not os.path.exists(SCREEN_PATH):
            time.sleep(1)
        img = Image.open(SCREEN_PATH)
    if resize and img.size != (base_x, base_y):
        return img.resize((base_x, base_y))
    else:
        return img


def tap_sleep(x, y):
    tap_screen(x, y)
    time.sleep(0.5)


def check_game_state(justClosePop=False):
    speed_time = datetime.now()
    current_count = 0
    error_count = 0
    while True:
        try:
            pull_screenshot(method=1, save_file=False)

            res = find_img_position()  # 这里容易出错
            error_count = 0
            if justClosePop:
                while res is not None and "b_close_pop" in res[0]:
                    tap_sleep(res[1], res[2])  # X掉开始的活动广告
                    time.sleep(1)

                    pull_screenshot(method=1, save_file=False)
                    res = find_img_position()
                break  # 关完活动页就关闭了
            if res is not None:  # 正常匹配
                name = res[0]
                if "b_finish" in name:  # 超出上限
                    stop_game()
                    logging.info("超出上限")
                    break
                elif "a_relax" in name:  # 妲己提示休息
                    logging.info("妲己提示休息,休息十分钟")
                    restart_game()
                else:
                    if "crop_restart" in name:
                        current_count = current_count + 1
                        logging.info("已运行{}次,本次时间{}秒".format(current_count, (datetime.now() - speed_time).seconds))
                        speed_time = datetime.now()
                    tap_sleep(res[1], res[2])
                    time.sleep(0.5)
            else:  # 未匹配
                time.sleep(1)
        except Exception as e:
            error_count = error_count + 1
            print(e)
            if error_count > 10:
                stop_game()
                logging.info("错误次数过多")
                break


def tapToStart():
    tap_sleep(1007, 531)  # 万象天工

    tap_sleep(90, 170)  # 快捷入口第一个

    tap_sleep(658, 346)  # 挑战

    tap_sleep(1006, 610)
