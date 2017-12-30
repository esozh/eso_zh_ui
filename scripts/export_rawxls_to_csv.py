#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : export_rawxls_to_csv.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 从导出的 xlsx 文件提取，合并得到去重后的 csv
# 


import os
import sys

from utils.xlsutils import load_xls
from utils.lang_def import *
from utils import log


def get_csv_from_xls(translation_path):
    """从文件夹中读取所有翻译文件

    Args:
        translation_path (str): 存放翻译 xlsx 文件的路径

    Returns:
        csv_list (dict[str: list]): dict<str, list>, 根据 category 归类的翻译
    """
    category_to_translated = {}
    for dir_path, dir_names, file_names in os.walk(translation_path):
        for file_name in file_names:
            if file_name.lower().endswith('.xlsx') and file_name.startswith('en.') \
                    and not file_name.startswith('~'):
                file_abs_path = os.path.join(dir_path, file_name)
                # load from one file
                log.info('load from %s' % file_name)
                category, translated_data = load_from_rawxls(file_abs_path)
                log.info('load %d %ss' % (len(translated_data), category))
                if category in category_to_translated:
                    log.warning('warning: override category %s' % category)
                category_to_translated[category] = translated_data
    list_list = [line for _, translated_data in sorted(category_to_translated.items())
                 for line in translated_data]
    return ['"%s","%s","%s","0","%s"\n' % (line[0], line[1], line[2], line[3])
            for line in list_list]


def load_from_list_category(data):
    """恢复从 list<text> 模式的 xlsx 中读取的数据

    Args:
        data: 从 xlsx 读出的数据，data[i][j] 表示第 i 行第 j 列的数据

    Returns:
        category (str): category from lang_def
        csv_data (list[str]): list of [file_id, unknown, index, text]
    """

    # 删除多余数据，只保留 内部编号, 英文
    data = [(row[1], row[3]) for row in data]
    category = data[0][0].rsplit('-', 3)[0]

    # 恢复编号
    csv_data = []
    for intern_id, text in data:
        if intern_id != '' and text != '':
            # 各 id 为 str 形式，不带前导0
            file_id, unknown, index = [str(int(x)) for x in intern_id.rsplit('-', 3)[1:]]
            csv_data.append([file_id, unknown, index, text])

    return category, csv_data


def load_from_pair_category(data):
    """恢复从 <name, desc> 模式的 xlsx 中读取的数据

    Args:
        data: 从 xlsx 读出的数据，data[i][j] 表示第 i 行第 j 列的数据

    Returns:
        category (str): category from lang_def
        csv_data (list[str]): list of [file_id, unknown, index, text]
    """

    # 删除多余数据，只保留 内部编号, 英文名称, 英文描述
    data = [(row[1], row[3], row[6]) for row in data]

    category = data[0][0].rsplit('-', 1)[0]
    name_file_id, desc_file_id = file_id_of_pair[category]

    # 恢复编号
    csv_data = []
    for intern_id, name, desc in data:
        if intern_id == '':
            continue        # 空行
        index = intern_id.rsplit('-', 1)[-1]
        index = str(int(index))     # 消除前导0
        # 这里直接令 unknown 为 0，对此类数据，暂时没有发现例外
        unknown = '0'
        if name != '':
            csv_data.append([name_file_id, unknown, index, name])
        if desc != '':
            csv_data.append([desc_file_id, unknown, index, desc])

    return category, csv_data


def load_from_rawxls(file_path):
    """从 xlsx 文件恢复数据到 lang.csv 的格式

    xlsx 文件可能是 <name, desc> 模式，也可能是 list<text> 模式。

    Args:
        file_path (str): xlsx 文件路径

    Returns:
        category (str): category from lang_def
        csv_data (list[str]): list of [file_id, unknown, index, text]，不带前导0
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


def get_dict_from_csv(csv):
    """从 csv 的行转换到 "fileid","unknown","index" 为 key, "offset","text" 为 value 的 dict

    Args:
        csv (list[str]): 从 csv 中读到的行

    Returns:
        csv_dict (dict[str:str]):
    """
    csv_dict = {}
    for line in csv:
        if line.strip() != '':
            file_id, unknown, index, offset_text = line.split(',', 3)
            csv_dict[','.join((file_id, unknown, index))] = offset_text
    return csv_dict


def main():
    cd = sys.path[0]
    src_path = os.path.join(cd, '../translation/lang')
    translation_path = os.path.join(cd, '../translation/lang/translated')

    # load from xlsx
    csv_list = get_csv_from_xls(src_path)

    # convert
    csv_dict = get_dict_from_csv(csv_list)
    csv_list_reduced = []
    for k, v in sorted(csv_dict.items()):
        csv_list_reduced.append('%s,%s' % (k, v))

    # save result
    dest_csv_file = os.path.join(translation_path, 'en.lang.reduce.csv')
    with open(dest_csv_file, 'wt', encoding='utf-8') as fp:
        fp.writelines(csv_list_reduced)
    log.info('write to en.lang.reduce.csv')

    # load zh
    zh_src_path = os.path.join(cd, '../translation/lang/translated/zh.lang.csv')
    if not os.path.isfile(zh_src_path):
        return
    with open(zh_src_path, 'rt', encoding='utf-8') as fp:
        zh_csv_list = fp.readlines()

    # convert
    zh_csv_dict = get_dict_from_csv(zh_csv_list)

    zh_csv_list_reduced = []
    for k in sorted(csv_dict):
        if k in zh_csv_dict:
            zh_csv_list_reduced.append('%s,%s' % (k, zh_csv_dict[k]))

    # save zh
    zh_dest_csv_file = os.path.join(translation_path, 'zh.lang.reduce.csv')
    with open(zh_dest_csv_file, 'wt', encoding='utf-8') as fp:
        fp.writelines(zh_csv_list_reduced)
    log.info('write to zh.lang.reduce.csv')


if __name__ == '__main__':
    log.debug('main() with args: %s' % str(sys.argv))
    main()
