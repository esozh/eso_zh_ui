#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : utils.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   :
# 


import os
from utils import log


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


def parse_csv_line(line):
    """从 csv 文件的一行里读取需要的参数

    Args:
        line(str): csv 里的一行

    Returns:
        return (list | None): 从这一行里解析出的参数, [file_id, unknown, index, offset, origin]
    """
    data = line.strip().split(',', 4)
    try:
        file_id, unknown, index, offset = [int(v[1:-1]) for v in data[0:4]]
        text = data[4][1:-1]
        return [file_id, unknown, index, offset, text]
    except ValueError:
        return None


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
            log.error('duplicate index: %s' % (str((_id, unknown, index, offset, text))))
            raise RuntimeError('duplicate index')
        data_dict_by_index[index] = text
    return data_dict_by_index


def load_unknown_index_text_from_csv(file_path):
    """从 csv 中读取文本，并用 unknown-index 当作其索引

    Args:
        file_path (str): csv 文件的路径

    Returns:
        data_dict_by_index (dict[int: str]): {unknown-index: text}
    """
    data = load_lang_csv(file_path, skip_header=False)
    data_dict_by_index = {}
    for _id, unknown, index, offset, text in data:
        unknown = int(unknown)
        index = int(index)
        joined_index = '%02d-%05d' % (unknown, index)
        if joined_index in data_dict_by_index:     # 如果 unknown-index 没有重复，将来就可以只用 unknown-index 来反查
            log.error('duplicate index: %s' % (str((unknown, index))))
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


def almost_equals(str1, str2):
    """两个字符串的英文字符和数字都相等

    Args:
        str1 (str): 待比较字符串1
        str2 (str): 待比较字符串2

    Returns:
        eq (bool): 是否相等
    """
    charset = set('abcdefghijklmnopqrstuvwxyz0123456789')
    str1_filtered = filter_string(str1.lower(), charset)
    str2_filtered = filter_string(str2.lower(), charset)
    return str1_filtered == str2_filtered


def filter_string(src, charset):
    """过滤字符串，仅保留所需字符

    Args:
        src (str): 待过滤字符串
        charset (set): 允许出现的字符

    Returns:
        left_str (str): 过滤后的字符串
    """
    if src is None:
        return src
    return ''.join((ch for ch in src if ch in charset))


def walk_xlsx_files(dir):
    """遍历目录下的所有 xlsx 文件，返回其绝对路径

    Args:
        dir (str): 要遍历的路径

    Returns:
        files (list[str]): 所有 xlsx 文件的绝对路径
    """
    files = []
    for dir_path, dir_names, file_names in os.walk(dir):
        for file_name in file_names:
            if file_name.lower().endswith('.xlsx') and not file_name.startswith('~'):
                file_abs_path = os.path.join(dir_path, file_name)
                files.append(file_abs_path)
    return files


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def merge_dict(dict1, dict2):
    """合并两个 dict, 生成新 dict"""
    dictx = dict1.copy()
    dictx.update(dict2)
    return dictx

