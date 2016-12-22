#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : apply_xls_format.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 套用模板格式
# 


import os
import sys

from utils.xlsutils import load_xls, save_xlsx_template


def apply_format(file_path):
    """xlsx 套用格式"""
    data = load_xls(file_path)
    if len(data) < 2:
        return
    header = data[0]
    data = data[1:]
    if len(header) in (9, 12):
        save_xlsx_template(file_path, data, header=header)


def format_file_path(filename, default_path):
    """如果只有名字，就到 default_path 找 filename"""
    if '\\' not in filename and '/' not in filename:
        filename = os.path.join(default_path, filename)
    return filename


def main():
    if len(sys.argv) < 2:
        print('usage: python apply_xls_format.py 1.xlsx 2.xlsx')
        sys.exit(2)

    cd = os.path.dirname(os.path.abspath(__file__))
    translation_path = os.path.join(cd, '../translation/lang')

    for filename in sys.argv[1:]:
        file_path = format_file_path(filename, translation_path)
        apply_format(file_path)


if __name__ == '__main__':
    main()
