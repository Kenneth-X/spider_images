# -*- encoding: utf-8 -*-
# Filename         :baidu_photo_spider.py
# Description      :
# Time             :2021/09/09 11:06:28
# Author           :王睿彪
# Email            :robin.wang@nio.com
# Version          :1.0

"""
log 配置

参考：


loguru 请参考： https://loguru.readthedocs.io/en/stable/api/logger.html#file

logging 请参考：https://docs.python.org/zh-cn/3/howto/logging-cookbook.html


Authos: wangshuai06(shuai.wang6@nio.com)
Date: 2021-07-19 14:01:01
"""

import os
import sys

from loguru import logger as loguru_logger

ENVS_CLASS = os.environ


def logger_init(log_path, rotation="10 GB", format_fmt=None, level="INFO"):
    """
    Args:
        rotation，达到指定大小或制定时间，切分日志，
            Examples: "100 MB", "0.5 GB", "1 month 2 weeks", "4 days", "10h", "monthly",
                "18:00", "sunday", "w0", "monday at 12:00", …
        retention，定期清理。
        compression，压缩节省空间。
        level, 举例子说明，如果设置为INFO，那么只会输出INFO,WARNING,ERROR,CRITICAL
             LevelName	SeverityValue	LoggerMethod
             DEBUG	10	logger.debug()
             INFO	20	logger.info()
             WARNING	30	logger.warning()
             ERROR	40	logger.error()
             CRITICAL	50	logger.critical()

    """

    dir = os.path.dirname(log_path)

    if dir != "" and not os.path.isdir(dir):
        os.makedirs(dir)
    #loguru_logger.remove()
    fmt = '{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {file}[{line}] {function} | {message}'

    if format_fmt is not None:
        fmt = format_fmt
    return loguru_logger.add(log_path, enqueue=True, format=fmt, \
                             encoding='utf-8', rotation=rotation, backtrace=True, diagnose=True, level=level)


def setup_console_logger(sink=sys.stderr):
    config = {
        "handlers": [
            {"sink": sink, "format": "{time:HH:mm:ss} - {file}({line}) <level>{message}</level>", "colorize": True},
        ],
    }
    loguru_logger.configure(**config)


log_file = ENVS_CLASS.get("LOGFILE", "baidu_photo_spider.log")
if log_file != "" and log_file is not None:
    if log_file in ('stdout', 'stderr'):
        if log_file == 'stdout':
            sink = sys.stdout
        if log_file == 'stderr':
            sink = sys.stderr
        setup_console_logger(sink)
    else:
        logger_init(log_file, rotation="10 GB", format_fmt=None, level="INFO")
else:
    setup_console_logger(sys.stderr)
logger = loguru_logger
