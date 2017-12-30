#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : join_langxls.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 把多个 xls 合成两个文件，一个是 pair 格式，一个是 list 格式
# 


import os
import sys
import io

from utils import lang_def
from utils.langxls_loader import get_category_of_id
from utils.xlsutils import load_xls, save_xlsx
from utils.utils import walk_xlsx_files
from utils import log


def usage():
    print('usage:')
    print('python join_langxls.py xls_dir output_dir')


def join_all_xls(file_path):
    """合并文件夹里的所有 xls 文件，合并成两类

    Args:
        file_path (str): 要遍历的路径

    Returns:
        data_pair (list): pair 格式的数据
        data_list (list): list 格式的数据
    """
    data_pair = []
    data_list = []

    for filename in walk_xlsx_files(file_path):
        # 读取数据
        data = load_xls(filename)
        category = get_category_of_id(data[1][1])
        # 判断是哪一类
        if category in lang_def.file_id_of_pair:
            if len(data_pair) > 0:  # header 只留一次
                data = data[1:]
            data_pair.extend(data)
        else:
            if len(data_list) > 0:
                data = data[1:]
            data_list.extend(data)
    return data_pair, data_list


def main():
    if len(sys.argv) != 3:
        usage()
        sys.exit(2)

    xls_dir, output_dir = sys.argv[1:]
    data_pair, data_list = join_all_xls(xls_dir)

    save_xlsx(os.path.join(output_dir, 'pair.xlsx'), data_pair)
    save_xlsx(os.path.join(output_dir, 'list.xlsx'), data_list)


if __name__ == '__main__':
    log.debug('main() with args: %s' % str(sys.argv))
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
    main()
