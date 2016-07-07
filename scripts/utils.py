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
    """从 csv 中读取文本，并用 index 当作其索引"""
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


def prepare_lang_name_and_desc(name_file_id, desc_file_id, lang='en'):
    """从两个不同 ID 对应文件中，读取同一 index 对应的内容

    两个文件分别存储“名字”及“描述”，每一对“名字”、“描述”的 index 相同。

    Args:
        name_file_id: “名字”文件的 ID
        desc_file_id: “描述”文件的 ID
        lang: 语言
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
    repeat_check_list = []  # 用于去重的列表
    for index, desc in sorted(desc_dict.items()):
        if index in name_dict.keys():
            name = name_dict[index]
            to_check = '%s%s' % (name, desc)
            if to_check not in repeat_check_list:   # 去重
                name_and_desc.append([index, name, desc])
                repeat_check_list.append(to_check)

    return name_and_desc


def save_lang_name_and_desc(dest_filename, name_in_id, name_title, desc_title, name_desc_en, name_desc_jp=None):
    """保存“名字”“描述”到准备翻译的文件里

    Args:
        dest_filename: 目标文件名
        name_in_id: “名字”的英文
        name_title: 名字标题
        desc_title: 描述标题
        name_desc_en: 英文内容
        name_desc_jp: 日文内容
    """

    cd = sys.path[0]
    dest_path = os.path.join(cd, '../translation/lang')
    dest_filename = os.path.join(dest_path, dest_filename)

    with open(dest_filename, 'wt', encoding='utf-8') as fp:
        line_id = 1     # from 1 to ...
        if name_desc_jp is None:        # 英汉对照
            header = '行号\t内部编号\t英文%s\t中文%s\t英文%s\t中文%s\t初翻人员\t校对\t润色\t备注\n' % \
                     (name_title, name_title, desc_title, desc_title)
            fp.write(header)
            for index, name, desc in name_desc_en:
                line = '%d\t%s-%05d\t%s\t\t%s\t\t\t\t\t\n' % (line_id, name_in_id, index, name, desc)
                line_id += 1
                fp.write(line)
        else:       # 带日文参考
            # convert to dict
            name_desc_dict_jp = {}
            for index, name, desc in name_desc_jp:
                name_desc_dict_jp[index] = (name, desc)
            # mach en and jp, save
            header = '行号\t内部编号\t日文%s\t英文%s\t中文%s\t日文%s\t英文%s\t中文%s\t初翻人员\t校对\t润色\t备注\n' % \
                     (name_title, name_title, name_title, desc_title, desc_title, desc_title)
            fp.write(header)
            for index, name, desc in name_desc_en:
                # match
                if index in name_desc_dict_jp:
                    name_jp, desc_jp = name_desc_dict_jp[index]
                else:
                    name_jp = desc_jp = ''
                # save
                line = '%d\t%s-%05d\t%s\t%s\t\t%s\t%s\t\t\t\t\t\n' % \
                       (line_id, name_in_id, index, name_jp, name, desc_jp, desc)
                line_id += 1
                fp.write(line)


def prepare_lang_list(file_id_list, lang='en'):
    """从多个不同 ID 对应文件中读取文本，并去重。

    Args:
        file_id_list: 各文件的 ID
        lang: 语言

    Returns:
        list of [(int)file_id, (str)unknown-index, (str)text]
    """

    cd = sys.path[0]
    translation_path = os.path.join(cd, '../translation/lang')

    # load
    text_dicts = {}     # 外层 dict 的索引是 file_id, 内层 dict 的索引是文件中的 Index
    for file_id in file_id_list:
        filename = os.path.join(translation_path, '%s.%s.lang.csv' % (lang, file_id))
        text_dict = load_unknown_index_text_from_csv(filename)
        text_dicts[file_id] = text_dict

    # decuplication
    texts = []
    repeat_check_list = []  # 用于去重的列表
    for file_id, text_dict in sorted(text_dicts.items()):
        for index, text in sorted(text_dict.items()):
            if text not in repeat_check_list:   # 去重
                texts.append([int(file_id), index, text])
                repeat_check_list.append(text)

    return texts


def save_lang_list(dest_filename, name_of_category, texts_en, texts_jp=None):
    """保存文本到准备翻译的文件里

    Args:
        dest_filename: 目标文件名
        name_of_category: “名字”的英文
        texts_en: [file_id, unknown-index, text]
        texts_jp: 日文文本
    """

    cd = sys.path[0]
    dest_path = os.path.join(cd, '../translation/lang')
    dest_filename = os.path.join(dest_path, dest_filename)

    with open(dest_filename, 'wt', encoding='utf-8') as fp:
        line_id = 1     # from 1 to ...
        if texts_jp is None:        # 英汉对照
            header = '行号\t内部编号\t英文\t中文\t初翻人员\t校对\t润色\t备注\n'
            fp.write(header)
            for file_id, index, text in texts_en:
                joined_id = '%09d-%s' % (file_id, index)
                line = '%d\t%s-%s\t%s\t\t\t\t\t\n' % (line_id, name_of_category, joined_id, text)
                line_id += 1
                fp.write(line)
        else:       # 带日文参考
            # convert to dict
            text_dict_jp = {}
            for file_id, index, text in texts_jp:
                joined_id = '%09d-%s' % (file_id, index)
                text_dict_jp[joined_id] = text
            # mach en and jp, save
            header = '行号\t内部编号\t日文\t英文\t中文\t初翻人员\t校对\t润色\t备注\n'
            fp.write(header)
            for file_id, index, text in texts_en:
                joined_id = '%09d-%s' % (file_id, index)
                # match
                if joined_id in text_dict_jp:
                    text_jp = text_dict_jp[joined_id]
                else:
                    text_jp = ''
                # save
                line = '%d\t%s-%s\t%s\t%s\t\t\t\t\t\n' % (line_id, name_of_category, joined_id, text_jp, text)
                line_id += 1
                fp.write(line)
