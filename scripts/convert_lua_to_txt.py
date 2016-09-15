#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : convert_lua_to_txt.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 将从 mnf 中解出的， esoui 文件夹下的 en_client.lua 等转换为 .txt 文件
# 


import os
import sys
from utils import read_lua, read_translate_txt


def main():
    lang = 'zh'
    if len(sys.argv) == 2:
        lang = sys.argv[1]

    cd = sys.path[0]
    translation_path = os.path.join(cd, '../translation')

    # load lua
    name_values = {}
    pregame_file = os.path.join(translation_path, '%s_pregame.lua' % lang)
    client_file = os.path.join(translation_path, '%s_client.lua' % lang)
    read_lua(pregame_file, name_values)
    read_lua(client_file, name_values)
    print('read %d lines.' % len(name_values))

    # save merged lines
    name_translation = {}
    translate_file = os.path.join(translation_path, '%s_translate.txt' % lang)
    if os.path.exists(translate_file):
        choose = input('%s_translate.txt file exists, merge? [y/N]' % lang)
        choose = choose.lower().strip()
        if choose != '' and choose[0] == 'y':
            print('merging to translate file.')
            name_translation = read_translate_txt(translate_file)
        else:
            print('skipped.')
            return

    with open(translate_file, 'wt', encoding='utf-8') as fp:
        for name, (value, version) in sorted(name_values.items()):
            fp.write('SafeAddString(%s, "%s", %s)\n' % (name, value, version))
            if name in name_translation:
                fp.write(name_translation[name] + '\n')
        print('save translate file succeed.')


if __name__ == '__main__':
    main()
