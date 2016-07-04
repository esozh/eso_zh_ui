#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : export_uixls_to_txt.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 从 lua 提取原文，从 xls 提取汉化，写入 txt 中
# 


import os
import sys
from xlsutils import load_xls
from utils import read_lua


def usage():
    print('usage:')
    print('python export_uixls_to_txt.py xls_file_name name_column_id text_column_id')


def main():
    lang = 'zh'
    if len(sys.argv) != 4:
        usage()
        sys.exit(2)

    xls_path = sys.argv[1]
    name_column_id = int(sys.argv[2])    # 名称
    text_column_id = None if len(sys.argv) == 3 else int(sys.argv[3])     # 译文

    cd = sys.path[0]
    translation_path = os.path.join(cd, '../translation')
    translate_file = os.path.join(translation_path, '%s_translate.txt' % lang)

    # load lua
    name_values = {}
    pregame_file = os.path.join(translation_path, '%s_pregame.lua' % lang)
    client_file = os.path.join(translation_path, '%s_client.lua' % lang)
    read_lua(pregame_file, name_values)
    read_lua(client_file, name_values)
    print('read %d lines from lua.' % len(name_values))

    # load translation
    name_translation = {line[name_column_id]: line[text_column_id] for line in load_xls(xls_path)}
    print('read %d lines from xls.' % len(name_translation))

    # save result
    with open(translate_file, 'wt', encoding='utf-8') as fp:
        for name, (value, version) in sorted(name_values.items()):
            fp.write('SafeAddString(%s, "%s", %s)\n' % (name, value, version))
            if name in name_translation:
                translation = name_translation[name].strip()
                if translation != '':
                    fp.write(name_translation[name] + '\n')
        print('save translate file succeed.')


if __name__ == '__main__':
    if os.name == 'nt':
        sys.stdout = open(1, 'w', encoding='utf-8', closefd=False)  # windows
    main()
