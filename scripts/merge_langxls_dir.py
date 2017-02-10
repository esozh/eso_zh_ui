#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : merge_langxls_dir.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 以目录1为基准，把目录2的文件导入目录1里
# 


import os
import sys

from utils import lang_def
from utils.langxls_loader import get_category
from utils.xlsutils import load_xls, save_xlsx
from utils.utils import almost_equals
from merge_langxls import merge_translation_file


def usage():
    print('usage:')
    print('python merge_langxls_dir.py dest_dir src_dir diff_dir')
    print('by default keep dest if conflict')


def get_filename_and_category(target_path):
    """获取目录中每个文件名及其对应的种类

    Args:
        target_path (str): 要遍历的路径

    Returns:
        filename_to_category (dict[str: str]): 文件名: category
    """
    filename_to_category = {}
    for dir_path, dir_names, file_names in os.walk(target_path):
        for file_name in file_names:
            if file_name.lower().endswith('.xlsx') and not file_name.startswith('~'):
                file_abs_path = os.path.join(dir_path, file_name)
                # check category
                category = get_category(file_abs_path)
                if category is not None:
                    filename_to_category[file_abs_path] = category
                    print('%s: %s' % (file_name, category))
                else:
                    print('failed to get category of %s' % file_abs_path)
    return filename_to_category


def main():
    if len(sys.argv) not in (3, 4):
        usage()
        sys.exit(2)

    # init path
    dest_xls_path, src_xls_path = sys.argv[1], sys.argv[2]
    conflict_xls_path = None
    if len(sys.argv) == 4:
        conflict_xls_path = sys.argv[3]

    # check category
    print('-- dest dir')
    dest_filename_to_category = get_filename_and_category(dest_xls_path)
    print('-- src dir')
    src_filename_to_category = get_filename_and_category(src_xls_path)

    # match & merge
    print('-- match')
    conflict_filename = None
    for dest_filename, dest_category in sorted(dest_filename_to_category.items()):
        for src_filename, src_category in sorted(src_filename_to_category.items()):
            if dest_category == src_category:
                if conflict_xls_path is not None:
                    conflict_filename = 'diff_%s===%s.xlsx' % (os.path.splitext(os.path.basename(dest_filename))[0],
                                                        os.path.splitext(os.path.basename(src_filename))[0])
                    conflict_filename = os.path.join(conflict_xls_path, conflict_filename)
                print('%s X %s' % (dest_filename, src_filename))
                merge_translation_file(dest_filename, src_filename, conflict_filename)


if __name__ == '__main__':
    main()
