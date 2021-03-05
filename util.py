import logging
import os
import random
import time
from datetime import datetime
from io import BytesIO

from PIL import Image
from ppadb.client import Client as AdbClient

from constant import SCREEN_PATH, SCREEN_METHOD, getDeviceSize, setDeviceSize, PAUSE_COUNT, SERVER_TIMES, \
    MAX_TIME,MIN_TIME
from img_match import find_img_position

client = AdbClient(host="127.0.0.1", port=5037)

device = client.devices()[0]

baseline = {}

# 日志输出
from logger import logger as logging

base_x, base_y = 1280, 720

current_count = 0


def init():
    global current_count
    current_count = 0
    find_screen_size()


def convert_cord(x, y):
    device_x = getDeviceSize()[0]
    device_y = getDeviceSize()[1]
    real_x = int(x / base_x * device_x)
    real_y = int(y / base_y * device_y)
    logging.debug("坐标转换：{},{}-->{},{}".format(x, y, real_x, real_y))
    return real_x, real_y


# 传固定坐标  以1280参考系位定点  会进行转换
def tap_screen_convert(x, y):
    tap_screen(x, y, True)


# needConvert 控制是否需要进行分辨率转换
def tap_screen(x, y, needConvert=False):
    """calculate real x, y according to device resolution."""
    real_x, real_y = int(x), int(y)
    if needConvert:
        real_x, real_y = convert_cord(x, y)
    real_x = random.randint(real_x, real_x + 10)
    real_y = random.randint(real_y, real_y + 10)
    device.shell('input tap {} {}'.format(real_x, real_y))
    time.sleep(random.random())  # 随机休眠  无实际用处  用于防止检测？不知道有没有用


def stop_game():
    device.shell('am force-stop com.tencent.tmgp.sgame')  # 关闭游戏


def start_game():
    device.shell('monkey -p com.tencent.tmgp.sgame -c android.intent.category.LAUNCHER 1')  # 打开游戏
    logging.info("启动游戏，等待30s")
    time.sleep(30)
    init()
    tap_screen_convert(643, 553)  # 选区界面 开始游戏

    logging.info("选区结束，等待30s")

    time.sleep(30)

    logging.info("关闭广告")
    check_game_state(True)


def restart_game():
    stop_game()

    logging.info("休息10分钟")
    time.sleep(60 * 10)

    logging.info("重启游戏")

    start_game()
    tapToStart()


def swipe(x, y, x1, y1, duration):
    device.shell('input swipe {} {} {} {} {}'.format(x, y, x1, y1, duration))


def find_screen_size():
    img = pull_screenshot(method=SCREEN_METHOD, save_file=False)
    x, y = img.size
    setDeviceSize(x, y)
    logging.info('device size x, y = ({}, {})'.format(x, y))


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
        os.system('adb shell screencap -p /sdcard/{}'.format(SCREEN_PATH))
        os.system('adb pull /sdcard/{} {}'.format(SCREEN_PATH, SCREEN_PATH))
        if not save_file:
            img = Image.open(SCREEN_PATH)
    if resize and img.size != (base_x, base_y):
        return img.resize((base_x, base_y))
    else:
        return img


def check_game_state(justClosePop=False):
    speed_time = datetime.now()
    global current_count
    error_count = 0
    fast_count = 0

    while True:
        try:
            if (datetime.now() - speed_time).seconds > MAX_TIME:
                stop_game()
                logging.warning("异常卡住，结束游戏")
                break
            pull_screenshot(method=SCREEN_METHOD, save_file=True)

            res = find_img_position()  # 这里容易出错
            error_count = 0
            if justClosePop:  # 启动关闭广告
                while res is not None and "b_close_pop" in res[0]:
                    tap_screen(res[1], res[2])  # X掉开始的活动广告
                    time.sleep(2)

                    pull_screenshot(method=SCREEN_METHOD, save_file=True)
                    res = find_img_position()

                time.sleep(5)  # 有个弹窗的直播  特别慢  所以再试一次
                pull_screenshot(method=SCREEN_METHOD, save_file=True)
                res = find_img_position()
                if res is not None and "b_close_pop" in res[0]:
                    tap_screen(res[1], res[2])  # X掉开始的活动广告

                break  # 关完活动页就关闭了 回去继续执行之前的循环
            if res is not None:  # 正常匹配
                name = res[0]
                if "b_finish" in name:  # 超出上限
                    stop_game()
                    logging.warning("超出上限")
                    break
                elif "a_relax" in name:  # 妲己提示休息
                    logging.warning("妲己提示休息,休息十分钟")
                    restart_game()
                else:
                    if "crop_restart" in name:
                        seconds = (datetime.now() - speed_time).seconds
                        speed_time = datetime.now()
                        if seconds >= MIN_TIME:  # 防止卡在结算界面，重复计算成功次数
                            fast_count = 0
                            current_count = current_count + 1
                            logging.info("已运行{}次,本次时间{}秒".format(current_count, seconds))
                            if current_count % SERVER_TIMES == 0:
                                logging.warning("已运行{}次".format(current_count))

                            if 0 < PAUSE_COUNT < current_count:
                                logging.warning("间隔休息十分钟")
                                restart_game()
                        else:
                            fast_count = fast_count + 1
                            if fast_count > 10:
                                stop_game()
                                logging.warning("错误次数过多(过快)")
                                break
                    elif "crop_continue" in name:
                        time.sleep(3)
                    tap_screen(res[1], res[2])
            else:  # 未匹配
                time.sleep(1)
        except Exception as e:
            error_count = error_count + 1
            print(e)
            if error_count > 10:
                stop_game()
                logging.warning("错误次数过多")
                break





def tapToStart():
    tap_screen_convert(1007, 531)  # 万象天工

    tap_screen_convert(90, 170)  # 快捷入口第一个

    tap_screen_convert(658, 346)  # 挑战

    tap_screen_convert(957, 640)  # 下一步
