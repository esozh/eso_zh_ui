#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : merge_uixls.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 更新或合并从 lang.csv 生成的 xls 汉化文件
#   合并时，以 dest 文件为准，逐行从 src 文件加载译文。
#   1. 如果 dest 没有译文，并且 dest 和 src 的原文一致，就把 src 的译文写入 dest；
#   2. 否则，dest 的这一行保持不变。
# 


import os
import sys

from merge_langxls import format_file_path, merge_translation_by_col
from utils.xlsutils import load_xls, save_xlsx


def usage():
    print('usage:')
    print('python merge_uixls.py dest src')
    print('by default keep dest if conflict')


def merge_translation_file(dest_xls_path, src_xls_path, conflict_xls_file):
    """合并两个文件中的数据，写回 dest 文件

    Args:
        dest_xls_path (str): 合并目标文件路径，当发生冲突时以此文件为准
        src_xls_path (str): 合并源文件路径
        conflict_xls_file (str | None): 冲突数据存放文件
    """

    # load
    print('load %s' % dest_xls_path)
    dest_data = load_xls(dest_xls_path)
    header, dest_data = dest_data[0], dest_data[1:]
    print('load %s' % src_xls_path)
    src_data = load_xls(src_xls_path)[1:]

    # check
    if not (dest_data[0][1].startswith('SI_') and src_data[0][1].startswith('SI_')):
        raise RuntimeError('invalid ui xls file')

    # merge
    merged_data, conflict_data = merge_translation_by_col(dest_data, src_data, id_col=1,
                                                          origin_col_ids=[2, ], translation_col_ids=[3, 4, 5, 6, 7])

    # save
    print('%d conflicts.' % len(conflict_data))
    print('save %s' % dest_xls_path)
    save_xlsx(dest_xls_path, merged_data, header=header)
    if conflict_xls_file is not None and len(conflict_data) > 0:
        print('save %s' % conflict_xls_file)
        save_xlsx(conflict_xls_file, conflict_data, header=header)


def main():
    cd = sys.path[0]
    translation_path = os.path.join(cd, '../translation/lang/translated')

    if len(sys.argv) not in (3, 4):
        usage()
        sys.exit(2)

    # init path
    dest_xls_file, src_xls_file = (format_file_path(name, translation_path) for name in (sys.argv[1], sys.argv[2]))
    conflict_xls_file = None
    if len(sys.argv) == 4:
        conflict_xls_file = format_file_path(sys.argv[3], translation_path)

    # merge translation & save
    merge_translation_file(dest_xls_file, src_xls_file, conflict_xls_file)


if __name__ == '__main__':
    main()
