import time

from img_match import find_img_position
from util import tap_screen, pull_screenshot, stop_game, restart_game
import logging
from datetime import datetime

# 日志输出
logging.basicConfig(format='[%(asctime)s][%(name)s:%(levelname)s(%(lineno)d)][%(module)s:%(funcName)s]:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S',
                    level=logging.INFO)

def tap_sleep(x, y):
    tap_screen(x, y)
    time.sleep(0.5)


def check_game_state():
    speed_time = datetime.now()
    current_count = 0
    while True:
        pull_screenshot(method=1, save_file=True)
        res = find_img_position()

        if res is not None:  # 正常匹配
            name = res[0]
            if "a_finish" in name:  # 超出上限
                stop_game()
            elif "a_relax" in name:  # 妲己提示休息
                restart_game()
            else:
                if "crop_restart" in name:
                    current_count = current_count + 1
                    logging.info("已运行{}次,本次时间{}秒".format(current_count, (datetime.now() - speed_time).seconds))
                    speed_time = datetime.now()
                tap_sleep(res[1], res[2])
                time.sleep(0.5)
        else:  # 未匹配
            time.sleep(2.5)


if __name__ == '__main__':
    tap_sleep(1007, 531)  # 万象天工

    tap_sleep(90, 170)  # 快捷入口第一个

    tap_sleep(658, 346)  # 挑战

    # swipe(313, 582, 318, 250, 500)

    # tap_sleep(681, 377)

    tap_sleep(1006, 610)

    check_game_state()

    # main()
