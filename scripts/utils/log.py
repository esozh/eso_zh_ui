#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : log.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   :
# 


import ctypes
import os
import sys
import logging
from logging import handlers, LogRecord, getLevelName

# logging 对象
G_LOG = None

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
COLORS = {
    'DEBUG': GREEN,
    'INFO': GREEN,
    'WARNING': YELLOW,
    'ERROR': RED,
    'CRITICAL': RED
}


class ColoredLogRecord(LogRecord):
    """增加 colorlevelname 一项"""
    def __init__(self, name, level, pathname, lineno,
                 msg, args, exc_info, func=None, sinfo=None, **kwargs):
        super().__init__(name, level, pathname, lineno,
                         msg, args, exc_info, func, sinfo, **kwargs)
        self.colorlevelname = get_color_level_name(level)


def get_color_level_name(level):
    level_name = getLevelName(level)
    if level_name in COLORS:
        return '\033[1;%dm%s\033[0m' % (30 + COLORS[level_name], level_name)
    else:
        return level_name


def init_log():
    """初始化log"""
    global G_LOG
    if G_LOG is not None:
        return

    logging.setLogRecordFactory(ColoredLogRecord)
    logger = logging.getLogger(sys.argv[0])
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    if hasattr(ctypes, 'windll') and hasattr(ctypes.windll, 'kernel32'):
        ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), 7)
    color_formatter = logging.Formatter('%(asctime)s - %(name)s - %(colorlevelname)s - %(message)s')

    # to file
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../logs')
    log_path = str(os.path.join(log_dir, 'esozh.log'))
    fh = logging.handlers.RotatingFileHandler(log_path, maxBytes=10 * 1024 * 1024, backupCount=10)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # to screen
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(color_formatter)
    logger.addHandler(ch)

    G_LOG = logger


def debug(msg, *args, **kwargs):
    log(logging.DEBUG, msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    log(logging.INFO, msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    log(logging.WARNING, msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    log(logging.ERROR, msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    log(logging.CRITICAL, msg, *args, **kwargs)


def log(lvl, msg, *args, **kwargs):
    global G_LOG
    if G_LOG is None:
        init_log()
        G_LOG.log(logging.DEBUG, 'init log, %s', str(sys.argv))

    try:
        G_LOG.log(lvl, msg, *args, **kwargs)
    except Exception as e:
        G_LOG.log(logging.ERROR, "failed to write log:\n%s", repr(e))
