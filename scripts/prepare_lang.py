#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : prepare_lang.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 从 lang.csv 提取待翻译文本，放到另一个 csv 文件中
# 


import os
import sys
from utils import load_index_and_text_from_csv, load_unknown_index_text_from_csv


# category: (name_file_id, desc_file_id)
pair_file_id_dict = {
    'skill': ('198758357', '132143172'),
    'book': ('51188213', '21337012'),
    'item': ('242841733', '228378404'),
    'questitem': ('267697733', '139139780'),
    'achievement': ('12529189', '188155806'),   # 172030117
    'mount': ('18173141', '211640654'),     # 坐骑宠物服装DLC等等
}
# category: (file1_id, file2_id, ...)
list_file_id_dict = {
    'interact': ('3427285', '6658117', '8158238', '12320021', '12912341', '34717246', '45275092', '45608037',
                 '70307621', '74865733', '84555781', '108533454', '139475237', '219689294', '263004526')
}


def usage():
    print('Usage:')
    print('python prepare_lang.py category')
    print('available category:')
    available_category = sorted(list(pair_file_id_dict.keys()) + list(list_file_id_dict.keys()))
    print(available_category)


def load_lang_name_and_desc(name_file_id, desc_file_id, lang='en'):
    """从两个不同 ID 对应文件中，读取同一 index 对应的内容

    两个文件分别存储“名字”及“描述”，每一对“名字”、“描述”的 index 相同。

    Args:
        name_file_id: “名字”文件的 ID
        desc_file_id: “描述”文件的 ID
        lang: 语言

    Returns:
        name_and_desc: [index, name, desc]
        duplicated_index: {namedesc: [index1, index2, ...]}
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
    repeat_check_list = []  # 用于去重的列表
    for index, desc in sorted(desc_dict.items()):
        if index in name_dict.keys():
            name = name_dict[index]
            to_check = '%s%s' % (name, desc)
            if to_check not in repeat_check_list:   # 去重
                name_and_desc.append([index, name, desc])
                repeat_check_list.append(to_check)
                duplicated_index[to_check] = [index, ]
            else:
                duplicated_index[to_check].append(index)

    return name_and_desc, duplicated_index


def save_lang_name_and_desc(dest_filename, name_in_id, name_title, desc_title, name_desc_en,
                            name_desc_jp, duplicated_index=None):
    """保存“名字”“描述”到准备翻译的文件里

    Args:
        dest_filename: 目标文件名
        name_in_id: “名字”的英文
        name_title: 名字标题
        desc_title: 描述标题
        name_desc_en: 英文内容
        name_desc_jp: 日文内容
        duplicated_index: 英文重复表
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
        # 没有重复表，就直接找 index
        elif index in name_desc_dict_jp:
            name_jp, desc_jp = name_desc_dict_jp[index]
        # save
        line = '%d\t%s-%05d\t%s\t%s\t\t%s\t%s\t\t\t\t\t\n' % \
               (line_id, name_in_id, index, name_jp, name, desc_jp, desc)
        line_id += 1
        lines.append(line)

    # save file
    with open(dest_filename, 'wt', encoding='utf-8') as fp:
        fp.writelines(lines)


def load_lang_list(file_id_list, lang='en'):
    """从多个不同 ID 对应文件中读取文本，并去重。

    Args:
        file_id_list: 各文件的 ID
        lang: 语言

    Returns:
        texts: list of [(int)file_id, (str)unknown-index, (str)text]
        duplicated_index: {text: [unknown-index1, unknown-index2, ...]}
    """

    cd = sys.path[0]
    translation_path = os.path.join(cd, '../translation/lang')

    # load
    text_dicts = {}     # 外层 dict 的索引是 file_id, 内层 dict 的索引是文件中的 Index
    for file_id in file_id_list:
        filename = os.path.join(translation_path, '%s.%s.lang.csv' % (lang, file_id))
        try:
            text_dict = load_unknown_index_text_from_csv(filename)
            text_dicts[file_id] = text_dict
        except FileNotFoundError:
            print('Warning: cannot find file %s' % filename)

    # deduplicate
    texts = []
    duplicated_index = {}
    repeat_check_list = []  # 用于去重的列表
    for file_id, text_dict in sorted(text_dicts.items()):
        for index, text in sorted(text_dict.items()):
            if text not in repeat_check_list:   # 去重
                texts.append([int(file_id), index, text])
                repeat_check_list.append(text)
                duplicated_index[text] = [[int(file_id), index], ]
            else:
                duplicated_index[text].append([int(file_id), index])

    return texts, duplicated_index


def save_lang_list(dest_filename, name_of_category, texts_en, texts_jp, duplicated_index=None):
    """保存文本到准备翻译的文件里

    Args:
        dest_filename: 目标文件名
        name_of_category: “名字”的英文
        texts_en: [file_id, unknown-index, text]
        texts_jp: 日文文本
        duplicated_index: 英文重复表
    """

    cd = sys.path[0]
    dest_path = os.path.join(cd, '../translation/lang')
    dest_filename = os.path.join(dest_path, dest_filename)

    lines = []
    line_id = 1     # from 1 to ...

    # convert to dict
    text_dict_jp = {}
    for file_id, index, text in texts_jp:
        joined_id = '%09d-%s' % (file_id, index)
        text_dict_jp[joined_id] = text
    # mach en and jp, save
    header = '行号\t内部编号\t日文\t英文\t中文\t初翻人员\t校对\t润色\t备注\n'
    lines.append(header)
    for file_id, index, text in texts_en:
        # 使用的 joined_id 格式为 fileid-unknown-index
        joined_id = '%09d-%s' % (file_id, index)
        # match
        text_jp = ''
        # 说明见 save_lang_name_and_desc
        if duplicated_index is not None:
            possible_index_list_jp = duplicated_index[text]
            for possible_file_id, possible_index in possible_index_list_jp:
                possible_joined_id = '%09d-%s' % (possible_file_id, possible_index)
                if possible_joined_id in text_dict_jp:
                    text_jp = text_dict_jp[possible_joined_id]
                    break
        if joined_id in text_dict_jp:
            text_jp = text_dict_jp[joined_id]
        # save
        line = '%d\t%s-%s\t%s\t%s\t\t\t\t\t\n' % (line_id, name_of_category, joined_id, text_jp, text)
        line_id += 1
        lines.append(line)

    with open(dest_filename, 'wt', encoding='utf-8') as fp:
        fp.writelines(lines)


def prepare_pair_lang(category, pair_file_id):
    """提取成对的 <名称、描述>，放到同一个文件中"""
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


def prepare_list_lang(category, list_file_id):
    """提取一系列的文本，放到同一个文件中"""
    # load
    texts, duplicated_index = load_lang_list(list_file_id)
    texts_jp, duplicated_index_jp = load_lang_list(list_file_id, lang='jp')
    # save
    dest_filename = 'en.%ss.lang.csv' % category
    save_lang_list(dest_filename, category, texts, texts_jp, duplicated_index=duplicated_index)
    print('save to %s' % dest_filename)


def main():
    if len(sys.argv) != 2:
        usage()
        sys.exit(2)

    # 调用 prepare_xxx_lang, prepare_xxx_lang 中再调用 load_lang_xxx, save_lang_xxx

    category = sys.argv[1]
    if category in pair_file_id_dict.keys():
        prepare_pair_lang(category, pair_file_id_dict[category])
    elif category in list_file_id_dict.keys():
        prepare_list_lang(category, list_file_id_dict[category])
    else:
        usage()
        sys.exit(2)


if __name__ == '__main__':
    main()
