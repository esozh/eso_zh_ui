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

sys.path.insert(0, '../../scripts/')
from utils import log


def execute(cmd):
    print('> %s' % cmd)
    ret = os.system(cmd)
    if ret != 0:
        sys.exit(-1)


def update_translation():
    """1. 更新翻译"""
    NEED_CLEAR = True
    os.system('pwd')
    eso_path = ' '.join(sys.argv[2:])
    log.info('ESO PATH: %s' % eso_path)
    mnf_path = os.path.join(eso_path, 'depot/eso.mnf')
    extract_path = '../../temp/extract/'

    datestr = time.strftime('%Y%m%d')
    print('请输入文件后缀并按下回车: (默认为今天日期: %s)' % datestr)
    datestr_new = input().strip()
    if datestr_new != '':
        datestr = datestr
    log.info('filename suffix: %s' % datestr)

    if NEED_CLEAR:
        print('### 正在清理...')
        log.debug('正在清理...')
        # 清理输出目录
        dirs = ('../../输出/更新翻译/1_new/',
                '../../输出/更新翻译/2_diff/',)
        for dir in dirs:
            if os.path.exists(dir):
                log.info('clear %s' % dir)
                shutil.rmtree(dir)
        # 清理 mnf 提取目录
        if os.path.exists(extract_path):
            log.info('clear %s' % extract_path)
            shutil.rmtree(extract_path)
        # 清理翻译中间目录
        log.info('clear csv and xlsx')
        for root, dirs, files in os.walk('../../translation/lang'):
            for f in files:
                if (f.startswith('en.') or f.startswith('jp.')) \
                        and (f.endswith('.lang.csv') or f.endswith('.lang.xlsx')):
                    filename = os.path.join(root, f)
                    log.debug('remove %s' % filename)
                    os.remove(filename)
            break
        log.info('clear ui text')
        files = (
            '../../translation/en_pregame.lua',
            '../../translation/en_client.lua',
            '../../translation/zh_translate.txt',
        )
        for f in files:
            if os.path.exists(f):
                log.debug('remove %s' % f)
                os.remove(f)

    print('### 创建目录...')
    log.debug('创建目录...')
    dirs = (
        '../../输出/更新翻译/1_new/',
        '../../输出/更新翻译/2_diff/',
        '../../输出/更新翻译/4_old/',
    )
    for dir in dirs:
        if not os.path.isdir(dir):
            log.info('create %s' % dir)
            os.makedirs(dir)

    print('### 正在解码...')
    log.debug('正在解码...')
    log.debug('extract eso.mnf -a 0')
    execute('EsoExtractData.exe "%s" -a 0 ../../temp/extract' % mnf_path)
    log.debug('extract eso.mnf -a 2')
    execute('EsoExtractData.exe "%s" -a 2 ../../temp/extract' % mnf_path)
    if not os.path.exists(extract_path):
        log.error('提取失败')
        sys.exit(-1)

    os.chdir('../../')
    os.system('pwd')
    print('### 正在复制...')
    log.debug('正在复制...')
    src_dst = (
        ('temp/extract/gamedata/lang/en.lang.csv', 'translation/lang/en.lang.csv',),
        ('temp/extract/gamedata/lang/jp.lang.csv', 'translation/lang/jp.lang.csv',),
        ('temp/extract/esoui/lang/en_pregame.lua', 'translation/en_pregame.lua',),
        ('temp/extract/esoui/lang/en_client.lua', 'translation/en_client.lua',),
    )
    for src, dst in src_dst:
        log.info('copy %s to %s' % (src, dst))
        shutil.copy(src, dst)

    os.chdir('scripts/')
    os.system('pwd')
    print('### 正在分析...')
    log.debug('正在分析...')
    execute('python split_lang_csv_by_id.py')
    execute('python split_lang_csv_by_id.py -l jp')

    print('### 正在导出新版xls...')
    log.debug('正在导出新版xls...')
    execute('python prepare_lang.py --all')
    execute('python convert_lua_to_txt.py')
    execute('python convert_txt_to_xls.py')

    print('### 正在保存结果...')
    log.debug('正在保存结果...')
    dst = '../输出/更新翻译/1_new/'
    for root, dirs, files in os.walk('../translation/lang'):
        for f in files:
            if f.startswith('en.') and f.endswith('.lang.xlsx'):
                filename = os.path.join(root, f)
                log.info('copy %s to %s' % (filename, dst))
                shutil.copy(filename, dst)
        break
    filename = '../translation/zh_translate.xlsx'
    log.info('copy %s to %s' % (filename, dst))
    shutil.copy(filename, dst)


def merge_translation():
    pass


def main():
    if sys.argv[1] == '1':
        update_translation()
    elif sys.argv[1] == '2':
        merge_translation()
    else:
        log.warning('unknown args')
        sys.exit(-2)


if __name__ == '__main__':
    log.debug('main() with args: %s' % str(sys.argv))
    main()
