#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : prepare_lang.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 从 lang.csv 提取待翻译文本，放到另一个 csv 文件中
# 


import os
import sys

from objs.lang_mgr import LangMgr
from objs.lang_mgr_array import LangMgrArray
from objs.lang_mgr_pair import LangMgrPair
from utils.lang_def import *
from utils.xlsutils import save_xls


def usage():
    print('Usage:')
    print('python prepare_lang.py category')
    print('available category:')
    available_category = list(file_id_of_pair.keys()) + list(file_id_of_list.keys()) + list(file_id_of_array.keys())
    print(sorted(available_category))


def load_lang_array(category, file_id_list, translation_path):
    """从多个不同 ID 对应文件中读取文本，并去重。相同 index 表示相关联。

    按 index-unknown-fileid 排序

    Args:
        category (str): 分类名字
        file_id_list (list[str]): 各文件的 ID
        translation_path (str): 翻译文件的路径

    Returns:
        rows (list[list[str]]): 准备写入 .xls 的列表
    """

    lang_mgr = LangMgrArray(translation_path, file_id_list)
    rows = [lang_mgr.get_header(), ]
    rows.extend(lang_mgr.to_xls_list())

    # index prefix
    for row in rows[1:]:
        row[1] = '%s-%s' % (category, row[1])

    return rows


def load_lang_name_and_desc(category, name_file_id, desc_file_id, translation_path):
    """从两个不同 ID 对应文件中，读取同一 index 对应的内容

    两个文件分别存储“名字”及“描述”，每一对“名字”、“描述”的 index 相同。

    Args:
        category (str): 分类名字
        name_file_id (str): “名字”文件的 ID
        desc_file_id (str): “描述”文件的 ID
        translation_path (str): 翻译文件的路径

    Returns:
        rows (list[list[str]]): 准备写入 .xls 的列表
    """

    # load
    lang_mgr = LangMgrPair(translation_path, name_file_id, desc_file_id)
    rows = [lang_mgr.get_named_header('名称', '描述'), ]
    rows.extend(lang_mgr.to_xls_list())

    # index prefix
    for row in rows[1:]:
        row[1] = '%s-%s' % (category, row[1])

    return rows


def load_lang_list(category, file_id_list, translation_path):
    """从多个不同 ID 对应文件中读取文本，并去重。

    按 fileid-unknown-index 排序

    Args:
        category (str): 分类名字
        file_id_list (list[str]): 各文件的 ID
        translation_path (str): 翻译文件的路径

    Returns:
        rows (list[list[str]]): 准备写入 .xls 的列表
    """

    lang_mgr = LangMgr(translation_path, file_id_list)
    rows = [lang_mgr.get_header(), ]
    rows.extend(lang_mgr.to_xls_list())

    # index prefix
    for row in rows[1:]:
        row[1] = '%s-%s' % (category, row[1])

    return rows


def prepare_array_lang(category, list_file_id, translation_path):
    """提取一系列的文本，放到同一个文件中。相同 index 表示相关联。

    Args:
        category (str): 分类名字
        list_file_id (list[str]): 对应的 file_id
        translation_path (str): 翻译文件的路径
    """

    # load
    rows = load_lang_array(category, list_file_id, translation_path)
    # save
    dest_filename = 'en.%ss.lang.xls' % category
    save_xls(os.path.join(translation_path, dest_filename), rows)
    print('save to %s' % dest_filename)


def prepare_pair_lang(category, pair_file_id, translation_path):
    """提取成对的 <名称、描述>，放到同一个文件中

    Args:
        category (str): 分类名字
        pair_file_id (list[str]): 对应的 file_id
    """
    if len(pair_file_id) != 2:
        raise RuntimeError('len(pair_file_id) in prepare_pair_lang must equals 2.')
    name_file_id = pair_file_id[0]
    desc_file_id = pair_file_id[1]

    # load, match name and desc
    rows = load_lang_name_and_desc(category, name_file_id, desc_file_id, translation_path)

    # save
    dest_filename = 'en.%ss.lang.xls' % category
    save_xls(os.path.join(translation_path, dest_filename), rows)
    print('save to %s' % dest_filename)


def prepare_list_lang(category, list_file_id, translation_path):
    """提取一系列的文本，放到同一个文件中

    Args:
        category (str): 分类名字
        list_file_id (list[str]): 对应的 file_id
        translation_path (str): 翻译文件的路径
    """

    # load
    rows = load_lang_list(category, list_file_id, translation_path)
    # save
    dest_filename = 'en.%ss.lang.xls' % category
    save_xls(os.path.join(translation_path, dest_filename), rows)
    print('save to %s' % dest_filename)


def main():
    if len(sys.argv) != 2:
        usage()
        sys.exit(2)

    cd = sys.path[0]
    translation_path = os.path.join(cd, '../translation/lang')

    # 调用 prepare_xxx_lang, prepare_xxx_lang 中再调用 load_lang_xxx, save_lang_xxx

    category = sys.argv[1]
    if category in file_id_of_pair.keys():
        prepare_pair_lang(category, file_id_of_pair[category], translation_path)
    elif category in file_id_of_list.keys():
        prepare_list_lang(category, file_id_of_list[category], translation_path)
    elif category in file_id_of_array.keys():
        prepare_array_lang(category, file_id_of_array[category], translation_path)
    else:
        usage()
        sys.exit(2)


if __name__ == '__main__':
    main()
