#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : utils.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   :
#


import os
import sys


def read_lua(file_path, name_values):
    """从 lua 文件读取 name 和文本，将结果存入 name_values

    Args:
        file_path (str): lua 文件路径
        name_values (dict[str: str]): name 与 文本
    """
    with open(file_path, 'rt', encoding='utf-8') as fp:
        for line in fp.readlines():
            line = line.strip()
            if line.startswith('SafeAddString'):
                name = line.split('(', 1)[1].split(',', 1)[0].strip()
                value = line.split(',', 1)[1].rsplit(',', 1)[0].strip()
                value = value[1:-1]     # remove quotes
                version = line.rsplit(',', 1)[1].strip(')').strip()
                name_values[name] = (value, version)


def read_translate_txt(file_path):
    """从 .translate.txt 文件读取 name 和文本

    Args:
        file_path (str): 文件路径

    Returns:
        name_translation (dict[str: str]): name 与 文本
    """
    name_translation = {}
    with open(file_path, 'rt', encoding='utf-8') as fp:
        # 每一行 SafeAddString 的下一行可能是翻译
        is_origin = False
        last_name = ''
        for line in fp.readlines():
            line = line.strip()
            if line.startswith('SafeAddString'):
                name = line.split('(', 1)[1].split(',', 1)[0].strip()
                is_origin = True
                last_name = name
            elif is_origin and line != '':
                name_translation[last_name] = line
                is_origin = False
    return name_translation


def load_lang_csv(file_path, skip_header=True):
    """读取 lang.csv 文件

    Args:
        file_path (str): 文件路径
        skip_header (bool): 跳过第一行
    """
    data = []
    with open(file_path, 'rt', encoding='utf-8') as fp:
        if skip_header:     # 跳过第一行
            header = fp.readline()
        for line in fp.readlines():
            values = line.strip().split(',', 4)
            data.append([value.strip()[1:-1] for value in values])  # append values without "
    return data


def load_index_and_text_from_csv(file_path):
    """从 csv 中读取文本，并用 index 当作其索引

    Args:
        file_path (str): lang.csv 的路径

    Returns:
        data_dict_by_index (dict[int: str]): {index: text}
    """
    data = load_lang_csv(file_path, skip_header=False)
    data_dict_by_index = {}
    for _id, unknown, index, offset, text in data:
        index = int(index)
        if index in data_dict_by_index:     # 如果 index 没有重复，将来就可以只用 index 来反查
            print(_id, unknown, index, offset, text)
            raise RuntimeError('duplicate index')
        data_dict_by_index[index] = text
    return data_dict_by_index


def load_unknown_index_text_from_csv(file_path):
    """从 csv 中读取文本，并用 unknown-index 当作其索引

    Args:
        file_path (str): csv 文件的路径
    """
    data = load_lang_csv(file_path, skip_header=False)
    data_dict_by_index = {}
    for _id, unknown, index, offset, text in data:
        unknown = int(unknown)
        index = int(index)
        joined_index = '%02d-%05d' % (unknown, index)
        if joined_index in data_dict_by_index:     # 如果 unknown-index 没有重复，将来就可以只用 unknown-index 来反查
            raise RuntimeError('duplicate index')
        data_dict_by_index[joined_index] = text
    return data_dict_by_index


def sort_texts_by_fileid_index_unknown(texts):
    """根据 file_id, index, unknown 排序

    Args:
        texts (list[list]): list of [(int)file_id, (str)unknown-index, (str)text]

    Returns:
        sorted_texts (list[list])
    """
    sorted_texts = sorted(texts, key=lambda x: '%d-%s' % (x[0], '-'.join(reversed(x[1].split('-')))))
    return sorted_texts


def merge_dict(dict1, dict2):
    dictx = dict1.copy()
    dictx.update(dict2)
    return dictx

