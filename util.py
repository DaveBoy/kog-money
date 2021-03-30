import logging
import os
import random
import shutil
import time
from datetime import datetime
from io import BytesIO

from PIL import Image, ImageFile
from ppadb.client import Client as AdbClient

from constant import SCREEN_PATH, getDeviceSize, setDeviceSize, PAUSE_COUNT, SERVER_TIMES, \
    MAX_TIME, MIN_TIME, PC_CROP_PARENT_NAME, PC_PROJECT_ROOT, SCREEN_METHOD
from img_match import find_img_position

# 日志输出
from logger import logger as logging

ImageFile.LOAD_TRUNCATED_IMAGES = True

base_x, base_y = 1280, 720

current_count = 0


def initDevice():
    os.system('taskkill /f /im %s' % 'cmd.exe')
    os.system('taskkill /f /im %s' % 'adb.exe')

    os.system("adb kill-server")
    os.system("adb start-server")
    global client
    client = AdbClient(host="127.0.0.1", port=5037)
    global device
    device = client.devices()[0]


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
    time.sleep(1)
    pull_screenshot(method=SCREEN_METHOD, save_file=True)
    res = find_img_position()
    if res is None:
        time.sleep(20)
    init()


def restart_game(needSleep=600):
    stop_game()

    if needSleep > 0:
        logging.info("休息10分钟")
        time.sleep(needSleep)

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


# 小米手机可能失败  因为adb shell screencap -p /sdcard/screen.png会生成screen_1616773251284.png类似文件名
def pull_screenshot(method=0, save_file=False):
    img = None
    if save_file and os.path.exists(SCREEN_PATH):
        os.remove(SCREEN_PATH)
    if method == 0:
        result = device.screencap()
        img = Image.open(BytesIO(result))

        if save_file:
            with open(SCREEN_PATH, "wb") as fp:
                fp.write(result)
    elif method == 1:
        pull_screenshot_new()
    elif method == 2:
        pull_screenshot_fix()
    else:
        os.system('adb shell screencap -p /sdcard/{}'.format(SCREEN_PATH))  # adb shell screencap -p /sdcard/screen.png
        os.system('adb pull /sdcard/{} {}'.format(SCREEN_PATH, SCREEN_PATH))  # adb pull /sdcard/screen.png screen.png
    if img is None and not save_file:
        img = Image.open(SCREEN_PATH)
    return img


def pull_screenshot_new():
    os.system('adb exec-out screencap -p > {}'.format(SCREEN_PATH))  # adb exec-out screencap -p > screen.png
    # https://stackoverflow.com/questions/13984017/how-to-capture-the-screen-as-fast-as-possible-through-adb
    # https://stackoverflow.com/questions/13578416/read-binary-stdout-data-from-adb-shell


def pull_screenshot_fix():
    if os.path.exists(PC_CROP_PARENT_NAME):
        shutil.rmtree(PC_CROP_PARENT_NAME)

    os.system('adb shell rm -r /sdcard/{}'.format(PC_CROP_PARENT_NAME))
    os.system('adb shell mkdir /sdcard/{}'.format(PC_CROP_PARENT_NAME))
    os.system('adb shell screencap -p /sdcard/{}/{}'.format(PC_CROP_PARENT_NAME, SCREEN_PATH))  # 此处文件名不一定匹配
    os.system('adb pull /sdcard/{} {}'.format(PC_CROP_PARENT_NAME, PC_PROJECT_ROOT))

    file_name = os.listdir(PC_CROP_PARENT_NAME)
    shutil.copy('{0}/{1}'.format(PC_CROP_PARENT_NAME, file_name[0]), SCREEN_PATH)


def startToHome():
    noDialogCount = 0
    while noDialogCount < 3:  # 连续三次检测不到弹窗、选区
        try:
            pull_screenshot(method=SCREEN_METHOD, save_file=True)
            res = find_img_position()
            if res is None:
                noDialogCount += 1
                time.sleep(5)
            elif res[0].startswith("z_choose_region"):
                noDialogCount = 0
                tap_screen(res[1], res[2])
                time.sleep(5)
            elif res[0].startswith("b_close_pop"):
                noDialogCount = 0
                tap_screen(res[1], res[2])  # X掉开始的活动广告
                time.sleep(1)
            else:
                noDialogCount += 1
                time.sleep(3)
        except Exception as e:
            print(e)

    logging.debug("关闭弹窗结束")


def check_game_state(waitTime=None):
    startToHome()
    speed_time = datetime.now()
    global current_count
    error_count = 0
    fast_count = 0

    while True:
        try:
            if (datetime.now() - speed_time).seconds > MAX_TIME:
                logging.warning("异常卡住，结束游戏")
                speed_time = datetime.now()
                restart_game(needSleep=0)
                continue
            pull_screenshot(method=SCREEN_METHOD, save_file=True)

            res = find_img_position()  # 这里容易出错
            error_count = 0
            if res is not None:  # 正常匹配
                name = res[0]
                if name.startswith("b_finish"):  # 超出上限
                    stop_game()
                    logging.warning("超出上限")
                    if waitTime is not None:
                        waitTime.value = -1
                    break
                elif name.startswith("a_relax"):  # 妲己提示休息
                    logging.warning("妲己提示休息,休息十分钟")
                    if waitTime is not None:
                        waitTime.value = 1
                    restart_game()
                    if waitTime is not None:
                        waitTime.value = 0
                elif name.startswith("crop_restart"):
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
                            if waitTime is not None:
                                waitTime.value = 1
                            restart_game()
                            if waitTime is not None:
                                waitTime.value = 0
                    else:
                        fast_count = fast_count + 1
                        if fast_count > 10:
                            logging.warning("错误次数过多(过快)")
                            restart_game(needSleep=0)
                            continue

                tap_screen(res[1], res[2])
                if name.startswith("crop_continue"):
                    time.sleep(3)
                else:
                    time.sleep(2)
            else:  # 未匹配
                time.sleep(2)
        except Exception as e:
            error_count = error_count + 1
            logging.error(e, exc_info=True, stack_info=True)
            if error_count > 10:
                logging.warning("错误次数过多")
                restart_game(needSleep=0)


def tapToStart():
    print("已用图片识别替代")
    # tap_screen_convert(1007, 531)  # 万象天工
    #
    # tap_screen_convert(90, 170)  # 快捷入口第一个
    #
    # tap_screen_convert(658, 346)  # 挑战
    #
    # tap_screen_convert(957, 640)  # 下一步
