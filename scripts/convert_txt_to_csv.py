#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : convert_txt_to_csv.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 将 .txt 文件转换为TAB分隔的文本，准备导入Excel
# 


import getopt
import os
import sys
from utils import read_lua, read_translate_txt


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

    # load translation
    translate_file = os.path.join(translation_path, '%s_translate.txt' % lang)
    name_translation = read_translate_txt(translate_file)

    # convert
    csv_xls_file = os.path.join(dest_path, '%s_translate.csv' % lang)
    convert(translate_file, csv_xls_file, name_translation)


def convert(src_file, dest_file, name_translation):
    """转换文件

    Args:
        src_file (str): .lua 文件的路径
        dest_file (str): 输出的 .csv 文件的路径
        name_translation (dict[str: str]): 原文: 译文
    """

    # merge translation & save str file
    name_values = {}
    read_lua(src_file, name_values)

    count_total = 0
    count_translated = 0
    header = '编号\t名称\t原文\t译文\t初翻人员\t校对\t润色\t备注\n'
    with open(dest_file, 'wt', encoding='utf-8') as fp:
        fp.writelines(header)
        for name, (origin_text, version) in sorted(name_values.items()):
            count_total += 1
            # 原文、翻译文本
            if name in name_translation:
                count_translated += 1
                # apply translation
                trans_text = name_translation[name]
            else:
                trans_text = ''
            # 初翻、校对、润色
            translator = ''
            proofreader = ''
            refiner = ''
            comments = ''
            fp.write('\t'.join(('UI-%d' % count_total, name, origin_text, trans_text,
                                translator, proofreader, refiner, comments)) + '\n')
        print('%d/%d translated in %s.' % (count_translated, count_total, dest_file))


if __name__ == '__main__':
    main()
