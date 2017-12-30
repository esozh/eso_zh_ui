#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : apply_xls_format.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 套用模板格式
# 


import os
import sys
import multiprocessing
from multiprocessing import Pool

from utils.xlsutils import load_xls, save_xlsx_template
from utils import log


def apply_format(file_path):
    """xlsx 套用格式"""
    data = load_xls(file_path)
    if len(data) < 2:
        return
    header = data[0]
    data = data[1:]
    if len(header) in (8, 9, 12):
        save_xlsx_template(file_path, data, header=header)
        log.info('save %s' % file_path)
    else:
        log.error('unknown xls %s.' % file_path)


def format_file_path(filename_or_path, default_path):
    """如果只有名字，就到 default_path 找 filename
    如果是路径，就遍历，
    返回文件名 list
    """
    if '\\' not in filename_or_path and '/' not in filename_or_path:
        filename_or_path = os.path.join(default_path, filename_or_path)

    if os.path.isdir(filename_or_path):
        # 遍历路径中的 xlsx 文件
        formatted_filename = []
        for dir_path, dir_names, file_names in os.walk(filename_or_path):
            for file_name in file_names:
                if file_name.lower().endswith('.xlsx') and not file_name.startswith('~'):
                    file_abs_path = os.path.join(dir_path, file_name)
                    formatted_filename.append(file_abs_path)
        return formatted_filename
    else:
        # 是文件，则直接返回
        return [filename_or_path, ]


def main():
    if len(sys.argv) < 2:
        print('usage: python apply_xls_format.py 1.xlsx 2.xlsx')
        sys.exit(2)

    cd = os.path.dirname(os.path.abspath(__file__))
    translation_path = os.path.join(cd, '../translation/lang')

    file_paths = []
    for filename in sys.argv[1:]:
        file_paths.extend(format_file_path(filename, translation_path))
    with Pool(processes=multiprocessing.cpu_count()) as pool:
        pool.map(apply_format, file_paths)


if __name__ == '__main__':
    main()
