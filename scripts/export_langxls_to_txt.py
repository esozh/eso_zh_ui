#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : export_langxls_to_txt.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 从 lua 提取原文，从 xls 提取汉化，写入 zh.lang.csv 中
# 


import os
import sys
from lang_def import *
from xlsutils import load_xls
from check_xls import check_string_with_origin


def load_from_type_list(data):
    """解析从 list<text> 模式的 xlsx 中读取的翻译"""

    # check
    for row in data:
        if row[4] != '' and not check_string_with_origin(row[3], row[4]):
            print(row[1], row[3])

    # 删除多余数据，只保留 内部编号, 中文
    data = [(row[1], row[4]) for row in data]
    text_type = data[0][0].rsplit('-', 3)[0]

    # 恢复编号
    translated_data = []
    for intern_id, text in data:
        if text != '':
            file_id, unknown, index = [int(x) for x in intern_id.rsplit('-', 3)[1:]]
            translated_data.append([file_id, unknown, index, text])

    print('load %d %ss' % (len(translated_data), text_type))
    return translated_data


def load_from_type_pair(data):
    """解析从 <name, desc> 模式的 xlsx 中读取的翻译"""

    # check
    for row in data:
        if (row[4] != '' and not check_string_with_origin(row[3], row[4])) \
                or (row[7] != '' and not check_string_with_origin(row[6], row[7])):
            print(row[1], row[3])

    # 删除多余数据，只保留 内部编号, 中文名称, 中文描述
    data = [(row[1], row[4], row[7]) for row in data]

    text_type = data[0][0].rsplit('-', 1)[0]
    name_file_id, desc_file_id = pair_file_id_dict[text_type]
    name_file_id, desc_file_id = int(name_file_id), int(desc_file_id)

    # 恢复编号
    translated_data = []
    for intern_id, name, desc in data:
        index = int(intern_id.rsplit('-', 1)[-1])
        # TODO: 这里直接令 unknown 为 0，需验证
        unknown = 0
        if name != '':
            translated_data.append([name_file_id, unknown, index, name])
        if desc != '':
            translated_data.append([desc_file_id, unknown, index, desc])

    print('load %d %ss' % (len(translated_data), text_type))
    return translated_data


def load_from_xls(file_path):
    """从 xlsx 文件中读取翻译

    xlsx 文件可能是 <name, desc> 模式，也可能是 list<text> 模式。
    """
    data = load_xls(file_path)[1:]
    # 判断文件模式
    id_split = data[0][1].split('-')
    if len(id_split) > 3 and id_split[-1].isdigit() and id_split[-2].isdigit() and id_split[-3].isdigit():
        # list of text
        return load_from_type_list(data)
    elif len(id_split) > 1 and id_split[-1].isdigit():
        # name_desc
        return load_from_type_pair(data)
    else:
        print('load failed.')
        return []


def get_translated_lines(lines, translated_data):
    """转换格式

    Args:
        lines: 英文原文件中的行, 每行的格式为 "ID","Unknown","Index","Offset","Text"
        translated_data: list, 其成员格式为 [file_id, unknown, index, text]

    Returns:
        可以写入 lang.csv 的行
    """
    # en_dict, {id: (offset, text)}
    en_dict = {}
    for line in lines:
        file_id, unknown, index, offset, text = line.split(',', 4)
        key = ','.join((file_id, unknown, index))
        en_dict[key] = (offset, text)

    # translated_dict, {"en_text": "zh_text"}
    translated_dict = {en_dict['"%d","%d","%d"' % (file_id, unknown, index)][1]: '"%s"\n' % text
                       for file_id, unknown, index, text in translated_data}

    # convert
    translated_lines = []
    translated_count = 0    # 包括重复的
    for line in lines:
        file_id, unknown, index, offset, text = line.split(',', 4)
        if text in translated_dict.keys():
            translated_line = '%s,%s,%s,%s,%s' % (file_id, unknown, index, offset, translated_dict[text])
            translated_lines.append(translated_line)
            translated_count += 1
        else:
            translated_lines.append(line)

    print('%d(%d) / %d translated' % (translated_count, len(translated_data), len(translated_lines)))
    return translated_lines


def main():
    cd = sys.path[0]
    src_path = os.path.join(cd, '../translation/lang')
    translation_path = os.path.join(cd, '../translation/lang/translated')

    # load en.lang.csv
    src_lang_file = os.path.join(src_path, 'en.lang.csv')
    with open(src_lang_file, 'rt', encoding='utf-8') as fp:
        header = fp.readline()
        lines = fp.readlines()
    print('read %d lines from en.lang.csv.' % len(lines))

    # load translation
    translated_data = []
    for dir_path, dir_names, file_names in os.walk(translation_path):
        for file_name in file_names:
            if file_name.lower().endswith('.xlsx') and not file_name.startswith('~'):
                file_abs_path = os.path.join(dir_path, file_name)
                # load from one file
                print('load from %s' % file_name)
                translated_data.extend(load_from_xls(file_abs_path))

    # save result
    translated_lines = get_translated_lines(lines, translated_data)
    dest_lang_file = os.path.join(translation_path, 'zh.lang.csv')
    with open(dest_lang_file, 'wt', encoding='utf-8') as fp:
        fp.write(header)
        fp.writelines(translated_lines)
    print('write to zh.lang.csv')


if __name__ == '__main__':
    main()
