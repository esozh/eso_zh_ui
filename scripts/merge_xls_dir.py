#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : merge_xls_dir.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 以目录1为基准，把目录2的文件导入目录1里
# 


import os
import sys

from utils.langxls_loader import get_filename_and_category
from merge_langxls import merge_translation_file as merge_lang_xls_file
from merge_uixls import merge_translation_file as merge_ui_xls_file
from utils import log


def usage():
    print('usage:')
    print('python merge_xls_dir.py dest_dir src_dir diff_dir')
    print('by default keep dest if conflict')


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
    log.info('merge: check dest dir')
    dest_filename_to_category = get_filename_and_category(dest_xls_path)
    log.info('merge: check src dir')
    src_filename_to_category = get_filename_and_category(src_xls_path)

    # match & merge
    log.info('merge: match')
    conflict_filename = None
    for dest_filename, dest_category in sorted(dest_filename_to_category.items()):
        for src_filename, src_category in sorted(src_filename_to_category.items()):
            if dest_category == src_category:
                if conflict_xls_path is not None:
                    conflict_filename = 'diff_%s===%s.xlsx' % (os.path.splitext(os.path.basename(dest_filename))[0],
                                                        os.path.splitext(os.path.basename(src_filename))[0])
                    conflict_filename = os.path.join(conflict_xls_path, conflict_filename)
                log.info('%s X %s' % (dest_filename, src_filename))
                if src_category == 'UI':
                    merge_ui_xls_file(dest_filename, src_filename, conflict_filename)
                else:
                    merge_lang_xls_file(dest_filename, src_filename, conflict_filename, check_category=False)


if __name__ == '__main__':
    main()
