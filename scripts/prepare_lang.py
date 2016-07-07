#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : prepare_lang.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 提取成对的<名称、描述>，放到同一个文件中
# 


import sys
from utils import prepare_lang_name_and_desc, save_lang_name_and_desc


def usage(category):
    print('Usage:')
    print('python prepare_lang.py category')
    print('available category:')
    print(category)


def main():
    # category: (name_file_id, desc_file_id)
    file_id_dict = {
        'skill': ('198758357', '132143172'),
        'book': ('51188213', '21337012'),
        'item': ('242841733', '228378404'),
    }

    if len(sys.argv) != 2:
        usage(sorted(file_id_dict.keys()))
        sys.exit(2)

    category = sys.argv[1]
    if category not in file_id_dict.keys():
        usage(sorted(file_id_dict.keys()))
        sys.exit(2)
    name_file_id = file_id_dict[category][0]
    desc_file_id = file_id_dict[category][1]

    # load, match name and desc
    name_desc = prepare_lang_name_and_desc(name_file_id, desc_file_id)
    name_desc_jp = prepare_lang_name_and_desc(name_file_id, desc_file_id, lang='jp')

    # save
    dest_filename = 'en.%ss.lang.csv' % category
    save_lang_name_and_desc(dest_filename, category, '名称', '描述', name_desc, name_desc_jp)
    print('save to %s' % dest_filename)


if __name__ == '__main__':
    main()
