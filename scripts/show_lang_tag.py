#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : show_lang_tag.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 列出 lang.csv 里所有的 << >> 标签
# 


import io
import os
import sys
import re

from objs.lang_line import LangLine
from objs.ui_mgr import UiMgr


def main():
    cd = sys.path[0]
    translation_path = os.path.join(cd, '../translation')

    lang_file = os.path.join(translation_path, 'lang/en.lang.csv')
    with open(lang_file, 'rt', encoding='utf-8') as fp:
        fp.readline()
        lines = [LangLine.from_csv_line(line).origin for line in fp.readlines()]

    pregame_file = os.path.join(translation_path, 'en_pregame.lua')
    client_file = os.path.join(translation_path, 'en_client.lua')
    ui_mgr = UiMgr()
    ui_mgr.load_lua_file(pregame_file)
    ui_mgr.load_lua_file(client_file)
    lines.extend([ui_line.origin for ui_line in ui_mgr.ui_lines.values()])

    # 寻找累类似 <<1>> 的标记
    tagger = re.compile(r'<<.*?>>')
    tags = set()

    # 搜索 去重
    for line in lines:
        for match in tagger.finditer(line):
            tags.add(match.group(0))

    # 排序输出
    for tag in sorted(tags):
        print(tag)


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='gb18030')
    main()
