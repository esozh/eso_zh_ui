#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : prepare_lang.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 从 lang.csv 提取待翻译文本，放到另一个 csv 文件中
# 


import sys
from utils import prepare_lang_name_and_desc, save_lang_name_and_desc, prepare_lang_list, save_lang_list


# category: (name_file_id, desc_file_id)
pair_file_id_dict = {
    'skill': ('198758357', '132143172'),
    'book': ('51188213', '21337012'),
    'item': ('242841733', '228378404'),
}
# category: (file1_id, file2_id, ...)
list_file_id_dict = {
    'interact': ('70307621', '8158238', '12912341', '74865733', '108533454', '139475237', '219689294', '263004526')
}


def usage():
    print('Usage:')
    print('python prepare_lang.py category')
    print('available category:')
    available_category = sorted(list(pair_file_id_dict.keys()) + list(list_file_id_dict.keys()))
    print(available_category)


def prepare_pair_lang(category, pair_file_id):
    """提取成对的 <名称、描述>，放到同一个文件中"""
    name_file_id = pair_file_id[0]
    desc_file_id = pair_file_id[1]

    # load, match name and desc
    name_desc = prepare_lang_name_and_desc(name_file_id, desc_file_id)
    name_desc_jp = prepare_lang_name_and_desc(name_file_id, desc_file_id, lang='jp')

    # save
    dest_filename = 'en.%ss.lang.csv' % category
    save_lang_name_and_desc(dest_filename, category, '名称', '描述', name_desc, name_desc_jp)
    print('save to %s' % dest_filename)


def prepare_list_lang(category, list_file_id):
    """提取一系列的文本，放到同一个文件中"""
    # load
    texts = prepare_lang_list(list_file_id)
    texts_jp = prepare_lang_list(list_file_id, lang='jp')
    # save
    dest_filename = 'en.%ss.lang.csv' % category
    save_lang_list(dest_filename, category, texts, texts_jp)
    print('save to %s' % dest_filename)


def main():
    if len(sys.argv) != 2:
        usage()
        sys.exit(2)

    category = sys.argv[1]
    if category in pair_file_id_dict.keys():
        prepare_pair_lang(category, pair_file_id_dict[category])
    elif category in list_file_id_dict.keys():
        prepare_list_lang(category, list_file_id_dict[category])
    else:
        usage()
        sys.exit(2)


if __name__ == '__main__':
    main()
