#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : setup_merge_xls_dir_main.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 合并文件的 cx_Freeze 脚本
# 


import sys, os
import merge_xls_dir
import apply_xls_format


if __name__ == '__main__':
    dest_xls_path, src_xls_path, conflict_xls_path = None, None, None

    # init path
    if len(sys.argv) in (3, 4):
        dest_xls_path, src_xls_path = sys.argv[1], sys.argv[2]
        conflict_xls_path = None
        if len(sys.argv) == 4:
            conflict_xls_path = sys.argv[3]
    else:
        for dir_path, dir_names, file_names in os.walk('.'):
            for dir_name in dir_names:
                if dir_name.startswith('1_'):
                    dest_xls_path = dir_name
                elif dir_name.startswith('2_'):
                    conflict_xls_path = dir_name
                elif dir_name.startswith('4_'):
                    src_xls_path = dir_name

    if dest_xls_path is None or src_xls_path is None or conflict_xls_path is None:
        print('参数错误')
        sys.exit(-2)

    merge_xls_dir.merge(dest_xls_path, src_xls_path, conflict_xls_path)

    for path in (dest_xls_path, src_xls_path, conflict_xls_path):
        paths = apply_xls_format.format_file_path(path, None)
        apply_xls_format.apply_format(paths)

    print('ok')
