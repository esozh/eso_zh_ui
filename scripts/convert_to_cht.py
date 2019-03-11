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
from utils import log


def usage():
    print('usage:')
    print('python convert_to_cht.py input_file output_file')


def get_text_replacer(lines):
    """从一个字典文件构造简繁替换类

    Args:
        lines (list[str]): 替换表中的行

    Returns:
        text_replacer (TextReplacer): 替换工具
    """
    # 对应表
    replacement = []
    for line in lines:
        line = line.strip()
        if line != '':
            parts = line.split('\t')
            if len(parts) >= 2:
                chs, cht = parts[0], parts[1]
                cht = cht.split(' ')[0]     # 如果有多种可能，随便取一个
                cht = cht.split('\t')[0]
                replacement.append((chs, cht))
    # 替换工具
    text_replacer = TextReplacer(replacement)
    return text_replacer


def split_lines_by_first_word_len(lines):
    """根据行中第一个词的长度来对行分组
    本方法没有通用性
    """
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    for line in lines:
        key_len = len(line.strip().split('\t')[0])
        if key_len <= 0:
            continue
        elif key_len <= 2:
            l1.append(line)
        elif key_len <= 3:
            l2.append(line)
        elif key_len <= 4:
            l3.append(line)
        else:
            l4.append(line)

    assert len(l1) != 0
    assert len(l2) != 0
    assert len(l3) != 0
    assert len(l4) != 0
    return [l4, l3, l2, l1]


def prepare_converter(phrases_dict_path, general_dict_paths, other_dict_path=None):
    """获取所有需要的简繁替换类，使用时按顺序调用

    Args:
        phrases_dict_path (str): 简繁转换的通用对照表
        general_dict_paths (list[str]): 目标语言的词组映射表，把直接转换后的词语映射为更加符合当地习惯的词语
        other_dict_path (str|None): 人工指定的对照表

    Returns:
        replacer_list (list[TextReplacer]): 替换工具
    """

    # 字典文件
    with open(phrases_dict_path, 'rt', encoding='utf-8') as fp:
        phrases_dict_lines = fp.readlines()

    dict_lines_list = []
    for dict_path in general_dict_paths:
        with open(dict_path, 'rt', encoding='utf-8') as fp:
            dict_lines_list.append(fp.readlines())

    other_dict_lines = []
    if other_dict_path is not None:
        with open(other_dict_path, 'rt', encoding='utf-8') as fp:
            other_dict_lines = fp.readlines()
    phrases_dict_lines_group = split_lines_by_first_word_len(phrases_dict_lines)

    # 替换顺序
    # 先是自己指定的，然后按字典单词从长到短的顺序来替换，最后再按当地习惯进行一次替换，结束时再用自己指定的来复查一遍
    replacer_list = [
    ]
    if other_dict_lines:
        replacer_list.append(get_text_replacer(other_dict_lines))
    for i in range(4):
        get_text_replacer(phrases_dict_lines_group[i])
    for dict_lines in dict_lines_list:
        replacer_list.append(get_text_replacer(dict_lines))
    if other_dict_lines:
        replacer_list.append(get_text_replacer(other_dict_lines))

    return replacer_list


def prepare_cht_converter():
    """获取所有需要的简繁替换类，使用时按顺序调用

    Returns:
        replacer_list (list[TextReplacer]): 替换工具
    """
    cd = os.path.dirname(os.path.abspath(__file__))
    phrases_dict_path = os.path.join(cd, 'utils/data/STPhrases.txt')
    general_dict_names = (
        'STCharacters', 'TWVariants', 'TWPhrasesName', 'TWPhrasesOther', 'TWPhrasesIT',
    )
    general_dict_paths = [os.path.join(cd,'utils/data', name + '.txt') for name in general_dict_names]
    other_dict_path = os.path.join(cd, '../translation/STOthers.txt')   # 人工整理的
    return prepare_converter(phrases_dict_path, general_dict_paths, other_dict_path)


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
    log.info('initializing cht converter')
    # 输入输出文本文件
    input_file_path, output_file_path = sys.argv[1], sys.argv[2]

    # 替换工具
    replacer_list = prepare_cht_converter()

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
    log.info('converting to cht')
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
