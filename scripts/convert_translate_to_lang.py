#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : convert_translate_to_lang.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 将带翻译的 zh.lang.translate.csv 转换为 zh.lang.csv
# 


import getopt
import os
import sys


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
    count_total = 0
    count_translated = 0
    lang_translate = []
    with open(translate_file, 'rt', encoding='utf-8') as fp:
        header = fp.readline()
        is_origin = False   # 读到了原文（否则读到了翻译）
        for line in fp.readlines():
            if is_origin and (not line.startswith('"')):
                is_origin = False
                count_translated += 1
                text_zh = line.strip()
                # apply translation
                if mode == 'origin':
                    pass    # keep origin
                elif mode == 'translation':
                    lang_translate[-1][1] = text_zh
                else:
                    # both translation and origin
                    lang_translate[-1][1] = r'%s\n%s' % (text_zh, lang_translate[-1][1])
            else:
                count_total += 1
                a, b, c, d, text_en = line.strip().split(',', 4)
                lang_translate.append([','.join((a, b, c, d)), text_en.strip().strip('"')])
                is_origin = True

    # save translation
    with open(dest_file, 'wt', encoding='utf-8') as fp:
        fp.write(header)
        for info, text in lang_translate:
            fp.write('%s,"%s"\n' % (info, text))


if __name__ == '__main__':
    main()
