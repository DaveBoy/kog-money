from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os.path
import time
from constant import LOG_FILE_SWITCH, LOG_CONSOLE_LEVEL, LOG_FILE_LEVEL,LOG_SERVER_LEVEL
from msg import postServerMsg


class MsgServerHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        postServerMsg(record)


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

time_line = time.strftime('%Y%m%d_%H%M', time.localtime(time.time()))

log_path = os.getcwd() + '\log\\'
logfile = log_path + time_line + '.log'
handler = logging.FileHandler(logfile, mode='w')
handler.setLevel(LOG_FILE_LEVEL)

formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(LOG_CONSOLE_LEVEL)

server = MsgServerHandler()
server.setLevel(LOG_SERVER_LEVEL)

if LOG_FILE_SWITCH:
    logger.addHandler(handler)
logger.addHandler(console)
logger.addHandler(server)

if __name__ == '__main__':
    logger.debug('This is a debug message.')
    logger.info('This is an info message.')
    logger.warning('This is a warning message.')
    logger.error('This is an error message.')
    logger.critical('This is a critical message.')
