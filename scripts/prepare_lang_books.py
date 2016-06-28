#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : prepare_lang_books.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 提取书名、正文，放到同一个文件中
# 


from utils import prepare_lang_name_and_desc, save_lang_name_and_desc


def main():
    book_name_file_id = '51188213'
    book_content_file_id = '21337012'

    # load, match name and content
    name_content = prepare_lang_name_and_desc(book_name_file_id, book_content_file_id)
    name_content_jp = prepare_lang_name_and_desc(book_name_file_id, book_content_file_id, lang='jp')

    # save
    dest_filename = 'en.books.lang.csv'
    save_lang_name_and_desc(dest_filename, 'book', '书名', '正文', name_content, name_content_jp)


if __name__ == '__main__':
    main()
