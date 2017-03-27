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


def main():
    cd = sys.path[0]
    translate_file = os.path.join(cd, '../translation/lang/en.lang.csv')

    with open(translate_file, 'rt', encoding='utf-8') as fp:
        fp.readline()
        lines = fp.readlines()

    # 寻找累类似 <<1>> 的标记
    tagger = re.compile(r'<<.*?>>')
    tags = set()

    # 搜索 去重
    for line in lines:
        lang_line = LangLine.from_csv_line(line)
        for match in tagger.finditer(lang_line.origin):
            tags.add(match.group(0))

    # 排序输出
    for tag in sorted(tags):
        print(tag)


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
    main()
