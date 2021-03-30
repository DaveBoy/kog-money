import os
import time
from datetime import datetime
from multiprocessing import Process, Value

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from constant import MAX_TIME
# 日志输出
from logger import logger as logging
from util import check_game_state, start_game, initDevice

waitTime = Value('i', 0)


def startGame(waitTime1):
    initDevice()
    global waitTime
    waitTime = waitTime1
    start_game()
    check_game_state(waitTime)


def updateTime(event):
    if "screen.png" in event.src_path:
        global lastChangeTime
        lastChangeTime = datetime.now()
        logging.debug('{0}:{1}'.format(event.event_type, event.src_path))


class MyHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_created(self, event):
        updateTime(event)


lastChangeTime = datetime.now()

if __name__ == '__main__':
    print("父进程：{0}".format(os.getpid()))

    p = Process(target=startGame, args=(waitTime,))

    p.start()
    print("子进程：启动成功")
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    restartCount = 0
    try:
        while True:
            if waitTime.value < 0:
                p.terminate()
                observer.stop()
                break
            elif waitTime.value == 0 and (datetime.now() - lastChangeTime).seconds > MAX_TIME:
                p.terminate()
                p = Process(target=startGame, args=(waitTime,))
                logging.warning('进程重启.')
                restartCount += 1
                if restartCount == 5:
                    p.terminate()
                    observer.stop()
                    break
                p.start()
                lastChangeTime = datetime.now()
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

    logging.error('Process end.')
    # windows系统关机
    os.system("shutdown -s -t 0")
