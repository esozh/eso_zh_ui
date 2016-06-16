#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : convert_translate_to_lang_po.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 将带翻译的 zh.lang.translate.csv 转换为 PO(Pootle) 文件 zh.lang.csv
# 


import getopt
import os
import sys
from utils import read_translate_lang_csv


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
    translation_path = os.path.join(cd, '../translation/lang')
    dest_path = translation_path

    # load translation
    translate_file = os.path.join(translation_path, '%s.lang.translate.csv' % lang)
    dest_file = os.path.join(dest_path, '%s.lang.csv' % lang)

    header, lang_translate, count_translated = read_translate_lang_csv(translate_file, mode)
    count_total = len(lang_translate)

    # save translation
    with open(dest_file, 'wt', encoding='utf-8', newline='\n') as fp:
        fp.write('"Location","Source","Target"\n')
        for info, text in lang_translate:
            fp.write('"%s","%s",""\n' % ('-'.join([x.strip().strip('"') for x in info[:-1]]), text))

    print('%d/%d translated in %s.' % (count_translated, count_total, dest_file))


if __name__ == '__main__':
    main()
