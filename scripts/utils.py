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
    with open(file_path, 'rt', encoding='utf-8') as fp:
        for line in fp.readlines():
            line = line.strip()
            if line.startswith('SafeAddString'):
                name = line.split('(', 1)[1].split(',', 1)[0].strip()
                value = line.split(',', 1)[1].rsplit(',', 1)[0].strip()
                value = value[1:-1]     # remove quotes
                version = line.rsplit(',', 1)[1].strip(')').strip()
                name_values[name] = (value, version)


def read_translate_txt(file_path, name_translation):
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


def load_lang_csv(file_path, skip_header=True):
    """读取 lang.csv 文件"""
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
        file_path: lang.csv 的路径

    Returns:
        data_dict_by_index: {index: text}
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
    """从 csv 中读取文本，并用 unknown-index 当作其索引"""
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


def read_translate_lang_csv(file_path, mode):
    """读取一行原文、一行译文的 lang.csv 文件"""
    count_translated = 0
    lang_translate = []
    with open(file_path, 'rt', encoding='utf-8') as fp:
        header = fp.readline()
        is_origin = False   # 读到了原文（否则读到了翻译）
        for line in fp.readlines():
            if is_origin and (not line.startswith('"')):
                is_origin = False
                count_translated += 1
                # TODO: 引号的处理
                text_zh = line.strip().replace('"', '').replace("'", '')
                # apply translation
                if mode == 'origin':
                    pass    # keep origin
                elif mode == 'translation':
                    lang_translate[-1][1] = text_zh
                else:
                    # both translation and origin
                    if text_zh != lang_translate[-1][1]:
                        lang_translate[-1][1] = r'%s\n%s' % (text_zh, lang_translate[-1][1])
            else:
                a, b, c, d, text_en = line.strip().split(',', 4)
                info = (a, b, c, d)
                text_en = text_en.strip()[1:-1]     # remove quotes
                lang_translate.append([info, text_en])
                is_origin = True
    return header, lang_translate, count_translated


def merge_dict(dict1, dict2):
    dictx = dict1.copy()
    dictx.update(dict2)
    return dictx

