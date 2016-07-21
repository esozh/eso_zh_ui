#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : export_langxls_to_csv.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 从 lua 提取原文，从 xls 提取汉化，写入 zh.lang.csv 中
# 


import os
import sys
from lang_def import *
from utils import merge_dict
from xlsutils import load_xls
from check_xls import check_string_with_origin


def load_from_list_category(data):
    """解析从 list<text> 模式的 xlsx 中读取的翻译

    Args:
        data: 从 xlsx 读出的数据，data[i][j] 表示第 i 行第 j 列的数据

    Returns:
        category: category from lang_def
        translated_data: list of [file_id, unknown, index, text]
    """

    # check
    for row in data:
        if row[4] != '' and not check_string_with_origin(row[3], row[4]):
            print(row[1], row[3])

    # 删除多余数据，只保留 内部编号, 中文
    data = [(row[1], row[4]) for row in data]
    category = data[0][0].rsplit('-', 3)[0]

    # 恢复编号
    translated_data = []
    for intern_id, text in data:
        if text != '':
            file_id, unknown, index = [int(x) for x in intern_id.rsplit('-', 3)[1:]]
            translated_data.append([file_id, unknown, index, text])

    print('load %d %ss' % (len(translated_data), category))
    return category, translated_data


def load_from_pair_category(data):
    """解析从 <name, desc> 模式的 xlsx 中读取的翻译

    Args:
        data: 从 xlsx 读出的数据，data[i][j] 表示第 i 行第 j 列的数据

    Returns:
        category: category from lang_def
        translated_data: list of [file_id, unknown, index, text]
    """

    # check
    for row in data:
        if (row[4] != '' and not check_string_with_origin(row[3], row[4])) \
                or (row[7] != '' and not check_string_with_origin(row[6], row[7])):
            print(row[1], row[3])

    # 删除多余数据，只保留 内部编号, 中文名称, 中文描述
    data = [(row[1], row[4], row[7]) for row in data]

    category = data[0][0].rsplit('-', 1)[0]
    name_file_id, desc_file_id = file_id_of_pair[category]
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

    print('load %d %ss' % (len(translated_data), category))
    return category, translated_data


def load_from_xls(file_path):
    """从 xlsx 文件中读取翻译

    xlsx 文件可能是 <name, desc> 模式，也可能是 list<text> 模式。

    Args:
        file_path: xlsx 文件路径

    Returns:
        category: category from lang_def
        translated_data: list of [file_id, unknown, index, text]
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
        print('load failed.')
        return '', []


def load_translation(translation_path):
    """从文件夹中读取所有翻译文件

    Args:
        translation_path: 存放翻译 xlsx 文件的路径

    Returns:
        category_to_translated: dict<str, list>, 根据 category 归类的翻译
    """
    category_to_translated = {}
    for dir_path, dir_names, file_names in os.walk(translation_path):
        for file_name in file_names:
            if file_name.lower().endswith('.xlsx') and not file_name.startswith('~'):
                file_abs_path = os.path.join(dir_path, file_name)
                # load from one file
                print('load from %s' % file_name)
                category, translated_data = load_from_xls(file_abs_path)
                category_to_translated[category] = translated_data
    return category_to_translated


def get_file_id_to_lines(lines):
    """根据 file id 分组 lines.

    Args:
        lines: 英文原文件中的行, 每行的格式为 "ID","Unknown","Index","Offset","Text"

    Returns:
        file_id_to_lines:
            <int> file id 作为 key,
            <list> lines 作为 value.
    """
    str_file_id_to_lines = {}
    for line in lines:
        file_id, unknown, index, offset, text = line.strip().split(',', 4)
        # file_id 格式为 "0", 类型为 str
        if file_id not in str_file_id_to_lines.keys():
            str_file_id_to_lines[file_id] = []
        str_file_id_to_lines[file_id].append(line)
    # 把 key 转换为 int 类型
    file_id_to_lines = {int(file_id[1:-1]): lines
                        for file_id, lines in str_file_id_to_lines.items()}
    return file_id_to_lines


def get_en_line_to_zh_line_for_list_category(lines, translated_data):
    """获取从英文行到中文行的对照，翻译类型为 text

    已知译文的 id-unknown-index，可以用它得到译文对应的原文，这样就有了原文到译文的映射。（重复相同的原文可以对应同一条译文）

    Args:
        lines: 英文原文件中的行, 每行的格式为 "ID","Unknown","Index","Offset","Text"
        translated_data: list of [file_id, unknown, index, text]

    Returns:
        en_line_to_zh_line: key 为原文行, value 为译文行
    """
    en_key_to_line = {}
    for line in lines:
        file_id, unknown, index, offset, text = line.split(',', 4)
        key = ','.join((file_id, unknown, index))   # 格式为 "file_id","unknown","index"
        en_key_to_line[key] = line

    # {"en_line": "zh_line"}
    en_line_to_zh_line = {}
    for file_id, unknown, index, zh_text in translated_data:
        key = '"%d","%d","%d"' % (file_id, unknown, index)
        if key in en_key_to_line:
            en_line = en_key_to_line[key]
            file_id, unknown, index, offset, en_text = en_line.split(',', 4)
            zh_line = '%s,%s,"%s"\n' % (key, offset, zh_text)
            en_line_to_zh_line[en_line] = zh_line

    return en_line_to_zh_line


def get_en_line_to_zh_line_for_pair_category(lines_of_name, lines_of_desc, translated_data):
    """获取从英文行到中文行的对照，翻译类型为 <name, desc>

    已知译文的 index，可以用它得到 name, desc 分别对应的 id-unknown-index，
    再根据译文的id-unknown-index，得到原文(line)到译文(line)的映射。

    Args:
        lines_of_name: 英文名字原文件中的行, 每行的格式为 "ID","Unknown","Index","Offset","Text"
        lines_of_desc: 英文描述原文件中的行, 每行的格式为 "ID","Unknown","Index","Offset","Text"
        translated_data: list of [file_id, unknown, index, text]

    Returns:
        en_line_to_zh_line: key 为原文行, value 为译文行
    """

    # 首先利用 name-desc 的关系进行处理
    # 得到 {index: ("id","unknown","index", line)}

    index_to_en_key_and_line_of_name = {}
    for line in lines_of_name:
        file_id, unknown, index, offset, name = line.split(',', 4)
        key = '%s,%s,%s' % (file_id, unknown, index)
        index_to_en_key_and_line_of_name[index] = (key, line)

    index_to_en_key_and_line_of_desc = {}
    for line in lines_of_desc:
        file_id, unknown, index, offset, desc = line.split(',', 4)
        key = '%s,%s,%s' % (file_id, unknown, index)
        index_to_en_key_and_line_of_desc[index] = (key, line)

    # 把能对应上的 name, desc 整理出来
    en_key_to_line = {}
    for index, key_and_line_of_name in index_to_en_key_and_line_of_name.items():
        if index in index_to_en_key_and_line_of_desc.keys():
            key_of_name, line_of_name = key_and_line_of_name
            key_of_desc, line_of_desc = index_to_en_key_and_line_of_desc[index]
            # add to dict
            en_key_to_line[key_of_name] = line_of_name
            en_key_to_line[key_of_desc] = line_of_desc

    # 之后就和 get_en_line_to_zh_line_for_list_category() 类似了
    # {"en_line": "zh_line"}
    en_line_to_zh_line = {}
    for file_id, unknown, index, zh_text in translated_data:
        key = '"%d","%d","%d"' % (file_id, unknown, index)
        if key in en_key_to_line:
            en_line = en_key_to_line[key]
            file_id, unknown, index, offset, en_text = en_line.split(',', 4)
            zh_line = '%s,%s,"%s"\n' % (key, offset, zh_text)
            en_line_to_zh_line[en_line] = zh_line

    return en_line_to_zh_line


def get_translated_lines_converter(file_id_to_lines, category_to_translated):
    """转换格式

    Args:
        file_id_to_lines: key 为 file_id, value 为 list<line>, 每行的格式为 "ID","Unknown","Index","Offset","Text"
        category_to_translated: dict, key 为 category, value 为 list of [file_id, unknown, index, text]

    Returns:
        en_line_to_zh_line: key 为原文的行， value 为译文的行
    """

    translated_count_dry = 0    # 不包括重复的

    # translated_dict, {"en_line": "zh_line"}
    en_line_to_zh_line = {}

    # 根据 category 决定处理方法
    for category, translated_data in sorted(category_to_translated.items()):
        translated_count_dry += len(translated_data)
        if category in file_id_of_list.keys():
            possible_file_ids = file_id_of_list[category]
            possible_lines = [line for file_id in possible_file_ids for line in file_id_to_lines[int(file_id)]]
            # load translation
            en_line_to_zh_line_of_category = get_en_line_to_zh_line_for_list_category(possible_lines, translated_data)
            # merge translation
            en_line_to_zh_line = merge_dict(en_line_to_zh_line, en_line_to_zh_line_of_category)
        elif category in file_id_of_pair.keys():
            name_file_id, desc_file_id = file_id_of_pair[category]
            lines_of_name = file_id_to_lines[int(name_file_id)]
            lines_of_desc = file_id_to_lines[int(desc_file_id)]
            # load translation
            en_line_to_zh_line_of_category = get_en_line_to_zh_line_for_pair_category(
                lines_of_name, lines_of_desc, translated_data)
            # merge translation
            en_line_to_zh_line = merge_dict(en_line_to_zh_line, en_line_to_zh_line_of_category)

    print('%d(%d) lines translate' % (translated_count_dry, len(en_line_to_zh_line)))
    return en_line_to_zh_line


def main():
    cd = sys.path[0]
    src_path = os.path.join(cd, '../translation/lang')
    translation_path = os.path.join(cd, '../translation/lang/translated')

    # load en.lang.csv
    src_lang_file = os.path.join(src_path, 'en.lang.csv')
    with open(src_lang_file, 'rt', encoding='utf-8') as fp:
        header = fp.readline()
        # lines: 英文原文件中的行, 每行的格式为 "ID","Unknown","Index","Offset","Text"
        lines = fp.readlines()
    print('read %d lines from en.lang.csv.' % len(lines))
    file_id_to_lines = get_file_id_to_lines(lines)

    # load translation
    category_to_translated = load_translation(translation_path)

    # get result
    en_line_to_zh_line = get_translated_lines_converter(file_id_to_lines, category_to_translated)
    translated_lines = []
    for en_line in lines:
        if en_line in en_line_to_zh_line.keys():
            translated_lines.append(en_line_to_zh_line[en_line])
        else:
            translated_lines.append(en_line)

    # save result
    dest_lang_file = os.path.join(translation_path, 'zh.lang.csv')
    with open(dest_lang_file, 'wt', encoding='utf-8') as fp:
        fp.write(header)
        fp.writelines(translated_lines)
    print('write to zh.lang.csv')


if __name__ == '__main__':
    main()
