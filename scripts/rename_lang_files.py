#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : rename_lang_files.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 根据 lang_def 的定义重命名文件
# 


import os
import sys


from utils.lang_def import category_names
from utils.langxls_loader import get_category


def usage():
    print('usage:')
    print('python rename_lang_files.py suffix file_dir')


def rename_file(filename, suffix):
    """按规则重命名文件"""
    category = get_category(filename)
    path_name = os.path.dirname(filename)
    new_name = os.path.join(path_name, 'ESO_%s_%s.xlsx' % (category_names[category], suffix))
    print('%s -> %s' % (filename, new_name))
    os.system('mv %s %s' % (filename, new_name))


def format_file_path(filename_or_path):
    """如果只有名字，就到 default_path 找 filename
    如果是路径，就遍历，
    返回文件名 list
    """
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
    if len(sys.argv) < 3:
        usage()
        sys.exit(2)

    # init path
    suffix = sys.argv[1]

    file_paths = []
    for filename in sys.argv[2:]:
        file_paths.extend(format_file_path(filename))
    for filename in file_paths:
        rename_file(filename, suffix)


if __name__ == '__main__':
    main()
