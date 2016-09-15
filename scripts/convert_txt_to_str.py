#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : convert_txt_to_str.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 将 .txt 文件转换为 .str 文件。其中 .txt 文件是翻译过的 .lua 文件。
# 


import getopt
import os
import sys
from utils import read_lua, read_translate_txt


def main():
    lang = 'zh'
    mode = 'both'   # origin, translation, both

    # getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'l:m:')
    except getopt.GetoptError as e:
        print(e)
        sys.exit(2)
    for o, a in opts:
        if o == '-l':
            lang = a
        elif o == '-m':
            mode = a.lower()

    cd = sys.path[0]
    translation_path = os.path.join(cd, '../translation')
    dest_path = os.path.join(cd, '../AddOns/esoui/lang')

    # load translation
    translate_file = os.path.join(translation_path, '%s_translate.txt' % lang)
    name_translation = read_translate_txt(translate_file)

    # load header
    header_file = os.path.join(translation_path, 'str_header.txt')
    with open(header_file, 'rt', encoding='utf-8') as fp:
        header = fp.readlines()

    # load lua
    pregame_src = os.path.join(translation_path, '%s_pregame.lua' % lang)
    pregame_dest = os.path.join(dest_path, '%s_pregame.str' % lang)
    convert(pregame_src, pregame_dest, name_translation, header, mode)

    client_src = os.path.join(translation_path, '%s_client.lua' % lang)
    client_dest = os.path.join(dest_path, '%s_client.str' % lang)
    convert(client_src, client_dest, name_translation, header, mode)


def convert(src_file, dest_file, name_translation, header, mode):
    """转换文件

    Args:
        src_file (str): .lua 文件的路径
        dest_file (str): 输出的 .csv 文件的路径
        name_translation (dict[str: str]): 原文: 译文
        header (list[str]): .str 文件的公共头
        mode (str): 翻译模式， origin, translation, both
    """

    # merge translation & save str file
    name_values = {}
    read_lua(src_file, name_values)

    count_total = 0
    count_translated = 0
    with open(dest_file, 'wt', encoding='utf-8') as fp:
        fp.writelines(header)
        for name, (value, version) in sorted(name_values.items()):
            count_total += 1
            if name in name_translation:
                count_translated += 1
                # apply translation
                if mode == 'origin':
                    pass    # keep origin
                elif mode == 'translation':
                    value = name_translation[name]
                else:
                    value = '%s %s' % (name_translation[name], value)   # both translation and origin
            fp.write('[%s] = "%s"\n' % (name, value))
        print('%d/%d translated in %s.' % (count_translated, count_total, dest_file))


if __name__ == '__main__':
    main()
