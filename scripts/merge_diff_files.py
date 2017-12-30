#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : merge_diff_files.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 合并 xls 文件，删除未翻译的行，不去重，按 id 排列
# 


import os
import sys


from utils import lang_def
from utils.lang_def import category_names
from utils.langxls_loader import get_filename_and_category, get_category_of_id
from utils.xlsutils import load_xls, save_xlsx
from utils import log


def usage():
    print('usage:')
    print('python merge_diff_files.py suffix output_dir diff_dir')


def merge_diff_files(files, output_path):
    """按要求合并翻译文件，并写入文件"""
    if len(files) <= 0:
        return

    header = None
    all_diff_data = []
    for filename in files:
        log.info('loading %s...' % os.path.basename(filename))
        diff_data = load_xls(filename)
        header, diff_data = diff_data[0], diff_data[1:]
        all_diff_data.extend(diff_data)

    # 去空
    category = get_category_of_id(all_diff_data[0][1])
    if category in lang_def.file_id_of_array or category in lang_def.file_id_of_list:
        all_diff_data = [row for row in all_diff_data if row[4] != '']
    elif category in lang_def.file_id_of_pair:
        all_diff_data = [row for row in all_diff_data if row[4] + row[7] != '']
    else:
        log.error('unknown category %s.' % category)
        raise RuntimeError('unknown category')

    # 去重
    all_diff_data_by_id = {}
    for row in all_diff_data:
        row = tuple(row)
        key = row[0]
        if key not in all_diff_data_by_id:
            all_diff_data_by_id[key] = {row}
        else:
            if row not in all_diff_data_by_id:
                all_diff_data_by_id[key].add(row)

    # 按顺序重排
    all_diff_data = []
    for _, rows_set in sorted(all_diff_data_by_id.items()):
        all_diff_data.extend(rows_set)

    output_name = os.path.basename(output_path)
    if len(all_diff_data) > 0:
        log.info('saving %s...' % output_name)
        save_xlsx(output_path, all_diff_data, header=header)
    else:
        log.info('skip %s' % output_name)


def main():
    if len(sys.argv) != 4:
        usage()
        sys.exit(2)

    # init path
    suffix, output_path, diff_path = sys.argv[1], sys.argv[2], sys.argv[3]

    # check category
    log.info('merge: diff dir')
    diff_filename_to_category = get_filename_and_category(diff_path)

    # merge
    log.info('merge: merge')
    for category, category_name in sorted(category_names.items()):
        diff_files = []
        # 检查是否有此 category
        for diff_filename, diff_category in sorted(diff_filename_to_category.items()):
            if category == diff_category:
                diff_files.append(diff_filename)
        # 合并此 category 的文件
        if len(diff_files) > 0:
            output_filename = 'diff_%s_%s.xlsx' % (category_name, suffix)
            merge_diff_files(diff_files, os.path.join(output_path, output_filename))


if __name__ == '__main__':
    main()
