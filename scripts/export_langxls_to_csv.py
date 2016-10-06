#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : export_langxls_to_csv.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 从 lua 提取原文，从 xls 提取汉化，写入 zh.lang.csv 中
# 


import os
import sys

from utils.lang_def import *
from utils.utils import merge_dict
from utils.langxls_loader import load_from_langxls


def load_translation(translation_path):
    """从文件夹中读取所有翻译文件

    Args:
        translation_path (str): 存放翻译 xlsx 文件的路径

    Returns:
        category_to_translated (dict[str: list]): dict<str, list>, 根据 category 归类的翻译
    """
    category_to_translated = {}
    for dir_path, dir_names, file_names in os.walk(translation_path):
        for file_name in file_names:
            if file_name.lower().endswith('.xlsx') and not file_name.startswith('~'):
                file_abs_path = os.path.join(dir_path, file_name)
                # load from one file
                print('load from %s' % file_name)
                category, translated_data = load_from_langxls(file_abs_path)
                print('load %d %ss' % (len(translated_data), category))
                if category in category_to_translated:
                    print('> warning: override category %s' % category)
                category_to_translated[category] = translated_data
    return category_to_translated


def get_file_id_to_lines(lines):
    """根据 file id 分组 lines.

    Args:
        lines: 英文原文件中的行, 每行的格式为 "ID","Unknown","Index","Offset","Text"

    Returns:
        file_id_to_lines (dict[int: list]):
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
        lines (list[str]): 英文原文件中的行, 每行的格式为 "ID","Unknown","Index","Offset","Text"
        translated_data (list[str]): list of [file_id, unknown, index, text]

    Returns:
        en_line_to_zh_line (dict[str: str]): key 为原文行, value 为译文行
    """
    en_key_to_line = {}
    for line in lines:
        file_id, unknown, index, offset, text = line.split(',', 4)
        key = ','.join((file_id, unknown, index))   # 格式为 "file_id","unknown","index"
        en_key_to_line[key] = line

    # {"en_line": "zh_line"}
    en_line_to_zh_line = {}
    for file_id, unknown, index, zh_text in translated_data:
        key = '"%s","%s","%s"' % (file_id, unknown, index)
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
        lines_of_name (list[str]): 英文名字原文件中的行, 每行的格式为 "ID","Unknown","Index","Offset","Text"
        lines_of_desc (list[str]): 英文描述原文件中的行, 每行的格式为 "ID","Unknown","Index","Offset","Text"
        translated_data (list[str]): list of [file_id, unknown, index, text]

    Returns:
        en_line_to_zh_line (dict[str: str]): key 为原文行, value 为译文行
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
        key = '"%s","%s","%s"' % (file_id, unknown, index)
        if key in en_key_to_line:
            en_line = en_key_to_line[key]
            file_id, unknown, index, offset, en_text = en_line.split(',', 4)
            zh_line = '%s,%s,"%s"\n' % (key, offset, zh_text)
            en_line_to_zh_line[en_line] = zh_line

    return en_line_to_zh_line


def get_translated_lines_converter(file_id_to_lines, category_to_translated, full_ids_jp):
    """转换格式

    Args:
        file_id_to_lines (dict[int: list[str]]):
                key 为 file_id,
                value 为 list<line>, 每行的格式为 "ID","Unknown","Index","Offset","Text"
        category_to_translated (dict[str: list]): dict, key 为 category, value 为 list of [file_id, unknown, index, text]
        full_ids_jp (set[str]): 日文原文里出现过的 '"file_id","unknown","index"', 在处理其他 file_id 中的翻译的时候用

    Returns:
        en_line_to_zh_line (dict[str: str]): key 为原文的行， value 为译文的行
    """

    translated_count_dry = 0    # 不包括重复的

    # translated_dict, {"en_line": "zh_line"}
    en_line_to_zh_line = {}
    # 已经处理过的 file_id
    translated_file_ids = []

    # 根据 category 决定处理方法
    for category, translated_data in sorted(category_to_translated.items()):
        translated_count_dry += len(translated_data)
        if category in file_id_of_list.keys():
            possible_file_ids = file_id_of_list[category]
            translated_file_ids.extend(possible_file_ids)
            # 需要判断的行
            possible_lines = []
            for file_id in possible_file_ids:
                file_id = int(file_id)
                if file_id in file_id_to_lines:
                    possible_lines.extend([line for line in file_id_to_lines[int(file_id)]])
            # load translation
            en_line_to_zh_line_of_category = get_en_line_to_zh_line_for_list_category(possible_lines, translated_data)
            # merge translation
            en_line_to_zh_line = merge_dict(en_line_to_zh_line, en_line_to_zh_line_of_category)
        elif category in file_id_of_pair.keys():
            name_file_id, desc_file_id = file_id_of_pair[category]
            translated_file_ids.extend(file_id_of_pair[category])
            lines_of_name = file_id_to_lines[int(name_file_id)]
            lines_of_desc = file_id_to_lines[int(desc_file_id)]
            # load translation
            en_line_to_zh_line_of_category = get_en_line_to_zh_line_for_pair_category(
                lines_of_name, lines_of_desc, translated_data)
            # merge translation
            en_line_to_zh_line = merge_dict(en_line_to_zh_line, en_line_to_zh_line_of_category)
    print('%d(%d) lines translated' % (translated_count_dry, len(en_line_to_zh_line)))

    # 处理剩下的行
    # 不同 file_id,unknown,index 对应的文本有可能相同，这种情况下，只要翻译了一个地方，其他地方就可以使用已有的翻译表
    other_translated_count = 0
    en_text_to_zh_text = {key.split(',', 4)[4]: value.split(',', 4)[4]
                          for key, value in sorted(en_line_to_zh_line.items())}

    # 所有的原文行，每行的格式为 "ID","Unknown","Index","Offset","Text"
    en_lines = [line for lines_of_file_id in sorted(file_id_to_lines.values()) for line in lines_of_file_id]
    # 排除已经翻译过的
    en_lines = [line for line in en_lines if line not in en_line_to_zh_line.keys()]
    # 排除 jp.lang.csv 中没有的
    en_lines = [line for line in en_lines if ','.join(line.split(',', 4)[:3]) in full_ids_jp]

    for line in en_lines:
        file_id, unknown, index, offset, en_text = line.split(',', 4)
        if en_text in en_text_to_zh_text:
            zh_line = '%s,%s,%s,%s,%s' % (file_id, unknown, index, offset, en_text_to_zh_text[en_text])
            en_line_to_zh_line[line] = zh_line
            other_translated_count += 1

    print('%d more lines translated' % other_translated_count)
    print('%d lines left' % (len(en_lines) - other_translated_count))

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

    src_jp_lang_file = os.path.join(src_path, 'jp.lang.csv')
    with open(src_jp_lang_file, 'rt', encoding='utf-8') as fp:
        fp.readline()   # skip
        # lines_jp: 日文原文件中的行
        lines_jp = fp.readlines()
        full_ids_jp = {','.join(line.split(',', 4)[:3]) for line in lines_jp}
    print('read %d lines from jp.lang.csv.' % len(lines_jp))

    file_id_to_lines = get_file_id_to_lines(lines)

    # load translation
    category_to_translated = load_translation(translation_path)

    # get result
    en_line_to_zh_line = get_translated_lines_converter(file_id_to_lines, category_to_translated, full_ids_jp)
    translated_lines = []
    for en_line in lines:
        # 先检查是否已翻译
        if en_line in en_line_to_zh_line.keys():
            translated_lines.append(en_line_to_zh_line[en_line])
        else:
            # 如果未翻译，检查在日文文本里是否有这行。检查 file_id,unknown,index
            file_id, unknown, index = en_line.split(',', 4)[:3]
            full_id = ','.join((file_id, unknown, index))
            if (full_id in full_ids_jp) or (file_id in file_id_of_pair['crown']):   # 皇冠商店不同区域可能不一样
                translated_lines.append(en_line)

    # save result
    dest_lang_file = os.path.join(translation_path, 'zh.lang.csv')
    with open(dest_lang_file, 'wt', encoding='utf-8') as fp:
        fp.write(header)
        fp.writelines(translated_lines)
    print('write to zh.lang.csv')


if __name__ == '__main__':
    main()
