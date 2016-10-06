#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : convert_txt_to_xls.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 将 .txt 文件转换为TAB分隔的文本，准备导入Excel
# 


import getopt
import os
import sys

from objs.ui_row import UiRow
from objs.ui_mgr import UiMgr
from utils.xlsutils import save_xlsx


def main():
    lang = 'zh'

    # getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'l:')
    except getopt.GetoptError as e:
        print(e)
        sys.exit(2)
    for o, a in opts:
        if o == '-l':
            lang = a

    cd = sys.path[0]
    translation_path = os.path.join(cd, '../translation')
    dest_path = translation_path

    ui_mgr = UiMgr()

    # load translation
    translate_file = os.path.join(translation_path, '%s_translate.txt' % lang)
    ui_mgr.load_lua_file(translate_file)
    ui_mgr.apply_translate_from_txt_file(translate_file)      # _translate.txt 中同时存了原文和译文

    rows = ui_mgr.get_rows()
    rows = [row for name, row in sorted(rows.items())]

    header = UiRow('名称') \
            .set_id('编号') \
            .set_origin('原文') \
            .set_translation('译文') \
            .set_translator('初翻人员') \
            .set_proofreader('校对') \
            .set_refiner('润色') \
            .set_comments('备注')
    rows[0:0] = [header, ]

    # save
    xls_file = os.path.join(dest_path, '%s_translate.xlsx' % lang)
    plain_rows = [row.to_list() for row in rows]    # list of [id, name, origin, translation, ...]
    save_xlsx(xls_file, plain_rows)


if __name__ == '__main__':
    main()
