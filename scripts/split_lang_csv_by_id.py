#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : split_lang_csv_by_id.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 根据 ID 拆分 en.lang.csv
# 


import getopt
import os
import sys

from utils.lang_def import file_id_of_pair, file_id_of_list, file_id_of_array, ignored_file_id


def main():
    lang = 'en'

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
    translation_path = os.path.join(cd, '../translation/lang')
    dest_path = translation_path

    # load translation
    lines_grouped_by_id = {}    # ID 作为 key， 每个 key 对应一个 list，每个 list 中的成员是原文件中的一行
    translate_file = os.path.join(translation_path, '%s.lang.csv' % lang)

    with open(translate_file, 'rt', encoding='utf-8') as fp:
        fp.readline()
        lines = fp.readlines()

    # split
    for line in lines:
        _id = line.split(',', 1)[0]
        _id = _id[1:-1]     # remove "
        if _id not in lines_grouped_by_id.keys():
            lines_grouped_by_id[_id] = []
        lines_grouped_by_id[_id].append(line)

    for _id, lines_with_same_id in sorted(lines_grouped_by_id.items()):
        target_file = os.path.join(dest_path, '%s.%s.lang.csv' % (lang, _id))
        with open(target_file, 'wt', encoding='utf-8') as fp:
            fp.writelines(lines_with_same_id)

    # known id
    known_id = set()
    for values in (file_id_of_pair.values(), file_id_of_list.values(), file_id_of_array.values()):
        for id_tuple in values:
            for _id in id_tuple:
                known_id.add(_id)
    known_id = known_id | ignored_file_id

    # file list
    target_file = os.path.join(dest_path, '%s.lang.split.txt' % lang)
    with open(target_file, 'wt', encoding='utf-8') as fp:
        id_list = sorted([int(_id) for _id in lines_grouped_by_id.keys()])
        for _id in id_list:
            fp.write('%d\n' % _id)
            if str(_id) not in known_id:
                print('warning: unknown id %d.' % _id)


if __name__ == '__main__':
    main()
