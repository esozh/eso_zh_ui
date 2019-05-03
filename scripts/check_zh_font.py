#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : check_zh_font.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 检查汉化文件中是否所有字都能用游戏字体正确显示
# 


import io
import os
import sys
from fontTools.ttLib import TTFont

from utils import log
from utils.utils import is_ascii


def check_csv(csv_path, font_path, deduplicate=True):
    """检查 csv 文件

    Args:
        csv_path (str): 翻译文件路径
        font_path (str): 字体文件路径
        deduplicate (bool): 是否去重
    """

    # load
    print('check font %s' % font_path)
    with open(csv_path, 'rt', encoding='utf-8') as fp:
        lines = fp.readlines()
    font = TTFont(font_path)

    valid_chars = set()
    for cmap in font['cmap'].tables:
        if cmap.isUnicode():
            for k in cmap.cmap.keys():
                valid_chars.add(k)

    whitelist = {'\t'}

    # check
    invalid_chars = set()
    for line in lines:
        line = line.strip()
        if line != "":
            file_id, unknown, index, offset, text = line.split(',', 4)
            invalid = []
            for char in text:
                if char not in whitelist:
                    if ord(char) not in valid_chars \
                            or ord(char) > 0xffff:
                        if not deduplicate or char not in invalid_chars:
                            invalid.append(char + ' ' + '0x%x' % ord(char))
                        invalid_chars.add(char)
            if invalid:
                key = ','.join((file_id, unknown, index))
                print('invalid char from %s: %s' % (key, ' '.join(invalid)))


def main():
    cd = os.path.dirname(os.path.abspath(__file__))
    translation_path = os.path.join(cd, '../translation/lang')
    font_path = os.path.join(cd, '../AddOns/EsoZH/fonts')
    zh_csv = os.path.join(translation_path, 'translated/zh.lang.csv')
    font_list = (
        "ftn47.otf",
        "ftn57.otf",
        "ftn87.otf",
        "FuturaStd-Condensed.otf",
        "FuturaStd-CondensedBold.otf",
        "FuturaStd-CondensedLight.otf",
        "handwritten_bold.otf",
        "proseantiquepsmt.otf",
        "trajanpro-regular.otf",
        "univers55.otf",
        "univers57.otf",
        "univers67.otf",
    )
    for font_name in font_list:
        check_csv(zh_csv, os.path.join(font_path, font_name))


if __name__ == '__main__':
    log.debug('main() with args: %s' % str(sys.argv))
    main()
