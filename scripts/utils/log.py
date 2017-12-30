#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : log.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   :
# 


import os
import logging
from logging import handlers, LogRecord, getLevelName

G_LOG = None


def init_log():
    """初始化log"""
    global G_LOG
    if G_LOG is not None:
        return

    logger = logging.getLogger("eso_zh_ui")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

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
    ch.setFormatter(formatter)
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
        G_LOG.log(logging.DEBUG, "init log")

    G_LOG.log(lvl, msg, *args, **kwargs)
