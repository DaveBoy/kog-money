import os
import time
from datetime import datetime
from multiprocessing import Process

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from util import pull_screenshot,pull_screenshot, SCREEN_METHOD


def add(name):
    count = 0
    while True:
        count = count + 1
        pull_screenshot(SCREEN_METHOD, True)
        print("add:{0}:{1}".format(name,count))
        time.sleep(3)
        if count>50:
            time.sleep(20)



class MyHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        if "screen.png" in event.src_path:
            global lastChangeTime
            lastChangeTime = datetime.now()
        if event.is_directory:
            print("directory moved from {0} to {1}".format(event.src_path, event.dest_path))
        else:
            print("file moved from {0} to {1}".format(event.src_path, event.dest_path))

    def on_created(self, event):
        if "screen.png" in event.src_path:
            global lastChangeTime
            lastChangeTime = datetime.now()

        if event.is_directory:
            print("directory created:{0}".format(event.src_path))
        else:
            print("file created:{0}".format(event.src_path))

    def on_deleted(self, event):
        if "screen.png" in event.src_path:
            global lastChangeTime
            lastChangeTime = datetime.now()

        if event.is_directory:
            print("directory deleted:{0}".format(event.src_path))
        else:
            print("file deleted:{0}".format(event.src_path))

    def on_modified(self, event):
        if "screen.png" in event.src_path:
            global lastChangeTime
            lastChangeTime = datetime.now()

        if event.is_directory:
            print("directory modified:{0}".format(event.src_path))
        else:
            print("file modified:{0}".format(event.src_path))

lastChangeTime = datetime.now()

if __name__ == "__main__":
    print('Parent process %s.' % os.getpid())
    p = Process(target=add, args=('test',))
    print('Process will start.')
    p.start()

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    print(f'启动成功')
    try:
        while True:
            if (datetime.now() - lastChangeTime).seconds > 20:
                p.terminate()
                p= Process(target=add, args=('test',))
                print('Process will start.')
                p.start()
                lastChangeTime = datetime.now()
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()


    observer.join()

    print('Process end.')
