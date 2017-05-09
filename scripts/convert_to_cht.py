#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : convert_to_cht.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 转换为繁体
#   字典来源: https://github.com/BYVoid/OpenCC
# 


import os
import sys
import math
import multiprocessing
from multiprocessing import Pool

from utils.text_replacer import TextReplacer


def usage():
    print('usage:')
    print('python convert_to_cht.py input_file output_file')


def prepare_cht_converter():
    """从字典构造简繁替换类

    Returns:
        text_replacer (TextReplacer): 替换工具
    """

    # 字典文件
    cd = os.path.dirname(os.path.abspath(__file__))
    phrases_dict_path = os.path.join(cd, 'utils/data/STPhrases.txt')
    chars_dict_path = os.path.join(cd, 'utils/data/STCharacters.txt')
    other_dict_path = os.path.join(cd, '../translation/STOthers.txt')   # 人工整理的

    lines = []

    if os.path.isfile(other_dict_path):
        with open(other_dict_path, 'rt', encoding='utf-8') as fp:
            lines.extend(fp.readlines())

    with open(phrases_dict_path, 'rt', encoding='utf-8') as fp:
        lines.extend(fp.readlines())
    with open(chars_dict_path, 'rt', encoding='utf-8') as fp:
        lines.extend(fp.readlines())

    if os.path.isfile(other_dict_path):
        with open(other_dict_path, 'rt', encoding='utf-8') as fp:
            lines.extend(fp.readlines())

    # 对应表
    replacement = []
    for line in lines:
        line = line.strip()
        if line != '':
            chs, cht = line.split('\t', 1)
            cht = cht.split(' ')[0]     # 如果有多种可能，随便取一个
            cht = cht.split('\t')[0]
            replacement.append((chs, cht))

    text_replacer = TextReplacer(replacement)
    return text_replacer


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
    print('init...')
    # 输入输出文本文件
    input_file_path, output_file_path = sys.argv[1], sys.argv[2]

    # 替换工具
    text_replacer = prepare_cht_converter()

    with open(input_file_path, 'rt', encoding='utf-8') as fp:
        lines = fp.readlines()

    # 文本预处理
    # 按行数平分文本
    input_text = []
    num_per_part = 1000     # 每份的行数
    part_num = int(math.ceil(len(lines) / num_per_part))    # 分成多少份
    for i in range(0, part_num):
        input_text.append(lines[num_per_part * i:num_per_part * (i + 1)])
    if part_num > 1:
        input_text.append(lines[num_per_part * (part_num - 1):])

    convert_args = [(''.join(partial_text), text_replacer) for partial_text in input_text]

    # 转换
    print('convert...')
    with Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.starmap(convert, convert_args)
    output_text = ''.join(results)

    # 保存
    with open(output_file_path, 'wt', encoding='utf-8') as fp:
        fp.write(output_text)


if __name__ == '__main__':
    main()
