#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : update_zh_csv.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 用新的 en.lang.csv 更新原来的 zh.lang.csv 文件
# 


import io
import os
import sys

from utils import log
from utils.utils import is_ascii


def update_lang_csv(translate_csv_path, src_csv_path):
    """更新 csv 文件

    Args:
        translate_csv_path (str): 旧版翻译文件路径
        src_csv_path (str): 新版原始文件路径
    """

    # load
    log.info('loading csv')
    with open(src_csv_path, 'rt', encoding='utf-8') as fp:
        src_lines = fp.readlines()
    with open(translate_csv_path, 'rt', encoding='utf-8') as fp:
        translate_lines = fp.readlines()

    log.info('parsing csv')
    # prepare translate data
    translate_by_key = {}
    for line in translate_lines[1:]:
        line = line.strip()
        if line != '' and not is_ascii(line):
            file_id, unknown, index, offset, text = line.split(',', 4)
            key = ','.join((file_id, unknown, index))
            translate_by_key[key] = text

    log.info('updating %s' % translate_csv_path)
    # generate new translate data
    new_csv = [src_lines[0].strip(), ]
    translated_cnt = 0
    for line in src_lines[1:]:
        line = line.strip()
        if line != '':
            file_id, unknown, index, offset, text = line.split(',', 4)
            key = ','.join((file_id, unknown, index))
            if key in translate_by_key and translate_by_key[key] != text:
                text = translate_by_key[key]
                translated_cnt += 1
            # 屏蔽 EsoExtractData 不支持的格式
            if text.endswith(r'\\"'):
                text = text[:-3] + r'\\ "'
            line = ','.join((key, offset, text))
            new_csv.append(line)

    log.info('%d/%d lines translated' % (translated_cnt, len(new_csv) - 1))
    with open(translate_csv_path, 'wt', encoding='utf-8') as fp:
        fp.write('\n'.join(new_csv))


def main():
    cd = os.path.dirname(os.path.abspath(__file__))
    translation_path = os.path.join(cd, '../translation/lang')
    en_csv = os.path.join(translation_path, 'en.lang.csv')
    zh_csv = os.path.join(translation_path, 'translated/zh.lang.csv')
    update_lang_csv(zh_csv, en_csv)


if __name__ == '__main__':
    log.debug('main() with args: %s' % str(sys.argv))
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='gb18030')
    main()
