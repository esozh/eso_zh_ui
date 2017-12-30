#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : xls2csv.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 将 xlsx 文件转换为 csv 格式
# 


import sys


from utils.xlsutils import load_xls
from utils import log


def usage():
    print('usage:')
    print('python xls2csv.py input.xlsx [output.csv]')


def main():
    if len(sys.argv) not in (2, 3):
        usage()
        sys.exit(2)

    # init path
    input_path = sys.argv[1]
    if len(sys.argv) == 3:
        output_path = sys.argv[2]
    else:
        if input_path.lower().endswith('.xlsx'):
            output_path = input_path[:-5] + '.csv'
        else:
            output_path = input_path + '.csv'

    # convert
    log.info('input path: %s' % input_path)
    log.info('out path: %s' % output_path)
    csv_data = load_xls(input_path)
    lines = []
    for row in csv_data:
        lines.append('\t'.join(row) + '\n')
    with open(output_path, 'wt', encoding='utf-8') as fp:
        fp.writelines(lines)


if __name__ == '__main__':
    main()
