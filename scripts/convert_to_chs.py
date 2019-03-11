#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : convert_to_cht.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 转换为简体
#   字典来源: https://github.com/BYVoid/OpenCC
# 


import os
import sys
import math
import multiprocessing
from multiprocessing import Pool

import convert_to_cht
from utils.text_replacer import TextReplacer
from utils import log


def usage():
    print('usage:')
    print('python convert_to_chs.py input_file output_file')


def prepare_chs_converter():
    """获取所有需要的简繁替换类，使用时按顺序调用

    Returns:
        replacer_list (list[TextReplacer]): 替换工具
    """
    cd = os.path.dirname(os.path.abspath(__file__))
    phrases_dict_path = os.path.join(cd, 'utils/data/TSPhrases.txt')
    general_dict_names = (
        'TSCharacters',
    )
    general_dict_paths = [os.path.join(cd,'utils/data', name + '.txt') for name in general_dict_names]
    return convert_to_cht.prepare_converter(phrases_dict_path, general_dict_paths)


def convert(input_text, text_replacer):
    """从字典构造简繁替换类

    Args:
        input_text (str): 待替换文本
        text_replacer (TextReplacer): 替换工具
    """
    return text_replacer.replace(input_text)


def main():
    if len(sys.argv) != 3:
        usage()
        sys.exit(2)

    # init file path
    log.info('initializing chs converter')
    # 输入输出文本文件
    input_file_path, output_file_path = sys.argv[1], sys.argv[2]

    # 替换工具
    replacer_list = prepare_chs_converter()

    with open(input_file_path, 'rt', encoding='utf-8') as fp:
        lines = fp.readlines()

    # 文本预处理
    # 按行数平分文本
    input_text = []
    num_per_part = 1000     # 每份的行数
    part_num = int(math.ceil(len(lines) / num_per_part))    # 分成多少份
    for i in range(0, part_num - 1):
        input_text.append(lines[num_per_part * i:num_per_part * (i + 1)])
    input_text.append(lines[num_per_part * (part_num - 1):])

    # 转换
    log.info('converting to chs')
    text_list = [''.join(partial_text) for partial_text in input_text]
    for text_replacer in replacer_list:
        # 每个 replacer 转一遍
        log.debug('convert with one converter')
        convert_args = [(partial_text, text_replacer) for partial_text in text_list]
        with Pool(processes=multiprocessing.cpu_count()) as pool:
            text_list = pool.starmap(convert, convert_args)

    # 结果
    output_text = ''.join(text_list)

    # 保存
    log.debug('writing convert result')
    with open(output_file_path, 'wt', encoding='utf-8') as fp:
        fp.write(output_text)


if __name__ == '__main__':
    log.debug('main() with args: %s' % str(sys.argv))
    main()
