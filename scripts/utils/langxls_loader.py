#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : langxls_loader.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   :
# 


import os
from utils.xlsutils import load_xls, load_xls_cell
from utils.check_xls import check_string_with_origin
from utils.lang_def import *
from utils import log


def load_from_list_category(data):
    """解析从 list<text> 模式的 xlsx 中读取的翻译

    Args:
        data: 从 xlsx 读出的数据，data[i][j] 表示第 i 行第 j 列的数据

    Returns:
        category (str): category from lang_def
        translated_data (list[str]): list of [file_id, unknown, index, text]
    """

    # check
    for row in data:
        if row[4] != '' and not check_string_with_origin(row[3], row[4]):
            log.warning('check string failed: %s', str(row[1]))

    # 删除多余数据，只保留 内部编号, 中文
    data = [(row[1], row[4]) for row in data]
    category = data[0][0].rsplit('-', 3)[0]

    # 恢复编号
    translated_data = []
    for intern_id, text in data:
        if intern_id != '' and text != '':
            file_id, unknown, index = [str(int(x)) for x in intern_id.rsplit('-', 3)[1:]]   # str 形式，不带前导0
            translated_data.append([file_id, unknown, index, text])

    return category, translated_data


def load_from_pair_category(data):
    """解析从 <name, desc> 模式的 xlsx 中读取的翻译

    Args:
        data: 从 xlsx 读出的数据，data[i][j] 表示第 i 行第 j 列的数据

    Returns:
        category (str): category from lang_def
        translated_data (list[str]): list of [file_id, unknown, index, text]
    """

    # check
    for row in data:
        if (row[4] != '' and not check_string_with_origin(row[3], row[4])) \
                or (row[7] != '' and not check_string_with_origin(row[6], row[7])):
            log.warning('check string failed: %s', str(row[1]))

    # 删除多余数据，只保留 内部编号, 中文名称, 中文描述
    data = [(row[1], row[4], row[7]) for row in data]

    category = data[0][0].rsplit('-', 1)[0]
    name_file_id, desc_file_id = file_id_of_pair[category]

    # 恢复编号
    translated_data = []
    for intern_id, name, desc in data:
        if intern_id == '':
            continue        # 空行
        index = intern_id.rsplit('-', 1)[-1]
        index = str(int(index))     # 消除前导0
        # 这里直接令 unknown 为 0，对此类数据，暂时没有发现例外
        unknown = '0'
        if name != '':
            translated_data.append([name_file_id, unknown, index, name])
        if desc != '':
            translated_data.append([desc_file_id, unknown, index, desc])

    return category, translated_data


def load_from_langxls(file_path):
    """从 xlsx 文件中读取 lang.csv 的翻译

    xlsx 文件可能是 <name, desc> 模式，也可能是 list<text> 模式。

    Args:
        file_path (str): xlsx 文件路径

    Returns:
        category (str): category from lang_def
        translated_data (list[str]): list of [file_id, unknown, index, text]，不带前导0
    """

    data = load_xls(file_path)[1:]
    # 判断文件模式
    id_split = data[0][1].split('-')
    if len(id_split) > 3 and id_split[-1].isdigit() and id_split[-2].isdigit() and id_split[-3].isdigit():
        # list of text
        return load_from_list_category(data)
    elif len(id_split) > 1 and id_split[-1].isdigit():
        # name_desc
        return load_from_pair_category(data)
    else:
        log.error('load %s failed.' % file_path)
        return '', []


def get_category(file_path):
    """判断 xlsx 文件是哪种"""
    first_id = load_xls_cell(file_path, 1, 1)
    return get_category_of_id(first_id)


def get_category_of_id(_id):
    """返回 id 中的 category 部分"""
    if _id.startswith('SI_'):
        # UI 汉化文件
        return 'UI'
    # 否则就是 item-111 或者 tip-1111-1-11 的格式
    id_split = _id.split('-')
    if len(id_split) > 3 and id_split[-1].isdigit() and id_split[-2].isdigit() and id_split[-3].isdigit():
        # list of text
        return '-'.join(id_split[:-3])
    elif len(id_split) > 1 and id_split[-1].isdigit():
        # name_desc
        return '-'.join(id_split[:-1])
    return None


def get_filename_and_category(target_path):
    """获取目录中每个文件名及其对应的种类

    Args:
        target_path (str): 要遍历的路径

    Returns:
        filename_to_category (dict[str: str]): 文件名: category
    """
    filename_to_category = {}
    for dir_path, dir_names, file_names in os.walk(target_path):
        for file_name in file_names:
            if file_name.lower().endswith('.xlsx') and not file_name.startswith('~'):
                file_abs_path = os.path.join(dir_path, file_name)
                # check category
                category = get_category(file_abs_path)
                if category is not None:
                    filename_to_category[file_abs_path] = category
                    log.info('%s: %s' % (file_name, category))
                else:
                    log.error('failed to get category of %s' % file_abs_path)
    return filename_to_category
