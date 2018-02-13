#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : main.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 
# 


import os
import sys
import shutil
import time
import zipfile

sys.path.insert(0, '../../scripts/')
from utils import log


def main():
    log.info(os.getcwd())
    print('### 正在清理...')
    log.debug('正在清理...')
    # 清理输出目录
    dir = '../../输出/搜索工具/'
    if os.path.exists(dir):
        log.info('clear %s' % dir)
        shutil.rmtree(dir)
    log.info('create %s' % dir)
    os.makedirs(dir)

    os.chdir('../../')
    log.info(os.getcwd())
    print('### 正在复制...')
    log.debug('正在复制...')
    dst = '输出/搜索工具/'
    files = (
        '工具/搜索工具/lang_finder.exe',
        'translation/lang/en.lang.csv',
        'translation/lang/translated/zh.lang.csv',
    )
    for f in files:
        log.info('copy %s to %s' % (f, dst))
        shutil.copy(f, dst)

    os.chdir('输出/搜索工具/')
    log.info(os.getcwd())
    print('### 正在打包...')
    log.debug('正在打包...')
    datestr = time.strftime('%Y%m%d')
    zip_name = 'ESO文本搜索_%s.zip' % datestr
    zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f != zip_name:
                zipf.write(os.path.join(root, f))
    zipf.close()


if __name__ == '__main__':
    log.debug('main() with args: %s' % str(sys.argv))
    main()
