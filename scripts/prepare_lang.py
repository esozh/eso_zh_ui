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
from utils.lang_def import *
from utils.utils import load_index_and_text_from_csv
from utils.xlsutils import save_xls


def usage():
    print('Usage:')
    print('python prepare_lang.py category')
    print('available category:')
    available_category = sorted(list(file_id_of_pair.keys()) + list(file_id_of_list.keys()))
    print(available_category)


def load_lang_name_and_desc(name_file_id, desc_file_id, lang='en'):
    """从两个不同 ID 对应文件中，读取同一 index 对应的内容

    两个文件分别存储“名字”及“描述”，每一对“名字”、“描述”的 index 相同。

    Args:
        name_file_id (str): “名字”文件的 ID
        desc_file_id (str): “描述”文件的 ID
        lang (str): 语言

    Returns:
        name_and_desc (list[LangLinesNameValue]): LangLines 列表
        duplicated_index (dict[str: list[LangLinesNameValue]]): 重复列表，应用翻译时使用。 {key: [lang_lines1, lang_lines2, ...]}
    """

    cd = sys.path[0]
    translation_path = os.path.join(cd, '../translation/lang')

    # load
    name_filename = os.path.join(translation_path, '%s.%s.lang.csv' % (lang, name_file_id))
    name_dict = load_index_and_text_from_csv(name_filename)
    desc_filename = os.path.join(translation_path, '%s.%s.lang.csv' % (lang, desc_file_id))
    desc_dict = load_index_and_text_from_csv(desc_filename)

    # match name and desc
    name_and_desc = []
    duplicated_index = {}
    repeat_check_list = set()  # 用于去重的列表
    for index, desc in sorted(desc_dict.items()):
        if index in name_dict.keys():
            name = name_dict[index]
            to_check = '%s%s' % (name, desc)
            if to_check not in repeat_check_list:   # 去重
                name_and_desc.append([index, name, desc])
                repeat_check_list.add(to_check)
                duplicated_index[to_check] = [index, ]
            else:
                duplicated_index[to_check].append(index)

    return name_and_desc, duplicated_index


def save_lang_name_and_desc(dest_filename, name_in_id, name_title, desc_title, name_desc_en,
                            name_desc_jp, duplicated_index=None):
    """保存“名字”“描述”到准备翻译的文件里

    Args:
        dest_filename (str): 目标文件名
        name_in_id (str): “名字”的英文
        name_title (str): 名字标题
        desc_title (str): 描述标题
        name_desc_en (list[list]): 英文内容
        name_desc_jp (list[list]): 日文内容
        duplicated_index (dict[str: list[int]]): 英文重复表
    """

    cd = sys.path[0]
    dest_path = os.path.join(cd, '../translation/lang')
    dest_filename = os.path.join(dest_path, dest_filename)

    lines = []
    line_id = 1     # from 1 to ...

    # convert to dict
    name_desc_dict_jp = {}
    for index, name, desc in name_desc_jp:
        name_desc_dict_jp[index] = (name, desc)
    # mach en and jp, save
    header = '行号\t内部编号\t日文%s\t英文%s\t中文%s\t日文%s\t英文%s\t中文%s\t初翻人员\t校对\t润色\t备注\n' % \
             (name_title, name_title, name_title, desc_title, desc_title, desc_title)
    lines.append(header)
    for index, name, desc in name_desc_en:
        # match
        name_jp = desc_jp = ''
        # 若有重复表，那么相同内容对应的 id 所对应的日文都有可能有内容
        # 注：暂不考虑英文内容相同，但对应的日文不相同的情况
        if duplicated_index is not None:
            possible_index_list_jp = duplicated_index['%s%s' % (name, desc)]
            for possible_index in possible_index_list_jp:
                if possible_index in name_desc_dict_jp:
                    name_jp, desc_jp = name_desc_dict_jp[possible_index]
                    break
        # 没有重复表，就直接找 index
        elif index in name_desc_dict_jp:
            name_jp, desc_jp = name_desc_dict_jp[index]
        # 没有日文的，说明已废弃
        if (name_jp == '') and (desc_jp == ''):
            continue
        # save
        line = '%d\t%s-%05d\t%s\t%s\t\t%s\t%s\t\t\t\t\t\n' % \
               (line_id, name_in_id, index, name_jp, name, desc_jp, desc)
        line_id += 1
        lines.append(line)

    # save file
    with open(dest_filename, 'wt', encoding='utf-8') as fp:
        fp.writelines(lines)


def load_lang_list(file_id_list, translation_path):
    """从多个不同 ID 对应文件中读取文本，并去重。

    按 fileid-unknown-index 排序

    Args:
        file_id_list (list[str]): 各文件的 ID
        translation_path (str): 翻译文件的路径

    Returns:
        rows (list[list[str]]): 准备写入 .xls 的列表
    """

    lang_mgr = LangMgr(translation_path, file_id_list)
    rows = [lang_mgr.get_header(), ]
    rows.extend(lang_mgr.to_xls_list())

    return rows


def prepare_pair_lang(category, pair_file_id):
    """提取成对的 <名称、描述>，放到同一个文件中

    Args:
        category (str): 分类名字
        pair_file_id (list[str]): 对应的 file_id
    """
    name_file_id = pair_file_id[0]
    desc_file_id = pair_file_id[1]

    # load, match name and desc
    name_desc, duplicated_index = load_lang_name_and_desc(name_file_id, desc_file_id)
    name_desc_jp, duplicated_index_jp = load_lang_name_and_desc(name_file_id, desc_file_id, lang='jp')

    # save
    dest_filename = 'en.%ss.lang.csv' % category
    save_lang_name_and_desc(dest_filename, category, '名称', '描述', name_desc,
                            name_desc_jp=name_desc_jp, duplicated_index=duplicated_index)
    print('save to %s' % dest_filename)


def prepare_list_lang(category, list_file_id, translation_path):
    """提取一系列的文本，放到同一个文件中

    Args:
        category (str): 分类名字
        list_file_id (list[str]): 对应的 file_id
        translation_path (str): 翻译文件的路径
    """

    # load
    rows = load_lang_list(list_file_id, translation_path)
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
        prepare_pair_lang(category, file_id_of_pair[category])
    elif category in file_id_of_list.keys():
        prepare_list_lang(category, file_id_of_list[category], translation_path)
    else:
        usage()
        sys.exit(2)


if __name__ == '__main__':
    main()
