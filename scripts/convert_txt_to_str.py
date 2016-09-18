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

from objs.ui_mgr import UiMgr


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
    dest_path = os.path.join(cd, '../AddOns/EsoUI/lang')

    # load header
    header_file = os.path.join(translation_path, 'str_header.txt')
    with open(header_file, 'rt', encoding='utf-8') as fp:
        header = fp.readlines()

    ui_mgr_pregame = UiMgr()
    ui_mgr_client = UiMgr()

    # load lua
    pregame_src = os.path.join(translation_path, '%s_pregame.lua' % lang)
    ui_mgr_pregame.load_lua_file(pregame_src)

    client_src = os.path.join(translation_path, '%s_client.lua' % lang)
    ui_mgr_client.load_lua_file(client_src)

    # load translation
    translate_file = os.path.join(translation_path, '%s_translate.txt' % lang)
    with open(translate_file, 'rt', encoding='utf-8') as fp:
        lines = fp.readlines()
        ui_mgr_pregame.apply_translate_from_txt_lines(lines)
        ui_mgr_client.apply_translate_from_txt_lines(lines)

    # save lua
    pregame_dest = os.path.join(dest_path, '%s_pregame.str' % lang)
    pregame_lines = ui_mgr_pregame.get_str_lines(mode)
    with open(pregame_dest, 'wt', encoding='utf-8') as fp:
        fp.writelines(header)
        fp.writelines(pregame_lines)

    client_dest = os.path.join(dest_path, '%s_client.str' % lang)
    client_lines = ui_mgr_pregame.get_str_lines(mode)
    with open(client_dest, 'wt', encoding='utf-8') as fp:
        fp.writelines(header)
        fp.writelines(client_lines)


if __name__ == '__main__':
    main()
