#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : export_uixls_to_txt.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 从 lua 提取原文，从 xls 提取汉化，写入 txt 中
# 


import os
import sys

from objs.ui_mgr import UiMgr
from utils.xlsutils import load_xls
from utils import log


def usage():
    print('usage:')
    print('python export_uixls_to_txt.py xls_file_name')


def main():
    lang = 'zh'

    if len(sys.argv) != 2:
        usage()
        sys.exit(2)

    xls_path = sys.argv[1]

    cd = sys.path[0]
    translation_path = os.path.join(cd, '../translation')
    translate_file = os.path.join(translation_path, '%s_translate.txt' % lang)

    ui_mgr = UiMgr()

    # load lua
    pregame_src = os.path.join(translation_path, 'en_pregame.lua')
    ui_mgr.load_lua_file(pregame_src)

    client_src = os.path.join(translation_path, 'en_client.lua')
    ui_mgr.load_lua_file(client_src)

    # load translation
    data_from_xls = load_xls(xls_path)
    ui_mgr.apply_translate_from_xls(data_from_xls)
    ui_mgr.apply_translate_from_xls(data_from_xls)

    # save result
    txt_lines = ui_mgr.get_txt_lines(replace=True)
    with open(translate_file, 'wt', encoding='utf-8') as fp:
        fp.writelines(txt_lines)
        log.info('save translate file succeed.')


if __name__ == '__main__':
    main()
