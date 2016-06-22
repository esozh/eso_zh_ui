#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : prepare_lang_books.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 提取书名、正文，放到同一个文件中
# 


import os
import sys
from utils import load_index_and_text_from_csv


def main():
    book_name_file_id = '51188213'
    book_content_file_id = '21337012'

    cd = sys.path[0]
    translation_path = os.path.join(cd, '../translation/lang')
    dest_path = translation_path

    # load
    book_name_file = os.path.join(translation_path, 'en.%s.lang.csv' % book_name_file_id)
    book_name_dict = load_index_and_text_from_csv(book_name_file)
    book_content_file = os.path.join(translation_path, 'en.%s.lang.csv' % book_content_file_id)
    book_content_dict = load_index_and_text_from_csv(book_content_file)

    # match name and content
    name_content = []
    repeat_check_list = []  # 用于去重
    for index, content in sorted(book_content_dict.items()):
        if index in book_name_dict.keys():
            name = book_name_dict[index]
            to_check = '%s%s' % (name, content)
            if to_check not in repeat_check_list:
                name_content.append([index, name, content])
                repeat_check_list.append(to_check)

    # save
    dest_file_name = os.path.join(dest_path, 'en.books.lang.csv')
    with open(dest_file_name, 'wt', encoding='utf-8') as fp:
        header = '编号\t英文书名\t中文书名\t英文正文\t中文正文\t初翻人员\t校对\t润色\t备注\n'
        fp.write(header)
        for index, name, content in name_content:
            line = 'book-%05d\t%s\t\t%s\t\t\t\t\t\n' % (index, name, content)
            fp.write(line)


if __name__ == '__main__':
    main()
