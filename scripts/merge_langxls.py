#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : merge_langxls.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 更新或合并从 lang.csv 生成的 xls 汉化文件
#   合并时，以 dest 文件为准，逐行从 src 文件加载译文。
#   1. 如果 dest 没有译文，并且 dest 和 src 的原文一致，就把 src 的译文写入 dest；
#   2. 否则，dest 的这一行保持不变。
# 


import os
import sys

from utils import lang_def
from utils.langxls_loader import load_from_langxls
from utils.xlsutils import load_xls, save_xlsx


def usage():
    print('usage:')
    print('python merge_langxls.py dest src')
    print('by default keep dest if conflict')


def merge_translation_file(dest_xls_path, src_xls_path, conflict_xls_file):
    """合并两个文件中的数据，写回 dest 文件

    Args:
        dest_xls_path (str): 合并目标文件路径，当发生冲突时以此文件为准
        src_xls_path (str): 合并源文件路径
        conflict_xls_file (str | None): 冲突数据存放文件
    """

    # check category
    category, _ = load_from_langxls(dest_xls_path)
    category_src, _ = load_from_langxls(src_xls_path)
    if category != category_src:
        raise RuntimeError('category not equal.')

    # load
    dest_data = load_xls(dest_xls_path)
    header, dest_data = dest_data[0], dest_data[1:]
    src_data = load_xls(src_xls_path)[1:]

    # merge
    merged_data, conflict_data = merge_translation_data(category, dest_data, src_data)

    # save
    save_xlsx(dest_xls_path, merged_data, header=header)
    print('%d conflicts.' % len(conflict_data))
    print('save %s' % dest_xls_path)
    if conflict_xls_file is not None and len(conflict_data) > 0:
        save_xlsx(conflict_xls_file, conflict_data, header=header)
        print('save %s' % conflict_xls_file)


def merge_translation_data(category, dest_data, src_data):
    """根据类型合并数据

    Args:
        category (str): category from lang_def，用于类型判断
        dest_data (list[list[str]]): 目标文件中的数据
        src_data (list[list[str]]): 源文件中的数据

    Returns:
        merged_data (list[list[str]]): 合并后的数据
        conflict_data (list[list[str]]): 合并时冲突的行（原文不一致，或都有译文）
    """

    if category in lang_def.file_id_of_array or category in lang_def.file_id_of_list:
        return merge_translation_by_col(dest_data, src_data, id_col=1,
                                        origin_col_ids=[2, 3], translation_col_ids=[4, 5, 6, 7, 8])
    elif category in lang_def.file_id_of_pair:
        return merge_translation_by_col(dest_data, src_data, id_col=1,
                                        origin_col_ids=[2, 3, 5, 6], translation_col_ids=[4, 7, 8, 9, 10, 11])
    else:
        raise RuntimeError('unknown category.')


def merge_translation_by_col(dest_data, src_data, id_col, origin_col_ids, translation_col_ids):
    """合并数据

    合并时，以 dest 文件为准，逐行从 src 文件加载译文。
    1. 如果 dest 没有译文，并且 dest 和 src 的原文一致，就把 src 的译文写入 dest；
    2. 否则，dest 的这一行保持不变。

    判断冲突行的目的是，在 dest 中寻找与 src 不一致的地方，以便人工修改。
    冲突判断条件：
    1. dest 与 src 中原文不一致
    2. dest 与 src 中都有译文且不一致
    3. dest 中有，但 src 中无此 id

    Args:
        dest_data (list[list[str]]): 目标文件中的数据
        src_data (list[list[str]]): 源文件中的数据
        id_col (int): id 所在的列
        origin_col_ids (list[int]): 原文的列
        translation_col_ids (list[int]): 译文的列

    Returns:
        merged_data (list[list[str]]): 合并后的数据，按 id 排序
        conflict_data (list[list[str]]): 合并时冲突的行（原文不一致，或都有译文）
    """
    dest_by_id = {row[id_col]: row for row in dest_data}
    src_by_id = {row[id_col]: row for row in src_data}

    merged_count = 0

    merged_data = []
    conflict_data = []
    for _id in sorted(dest_by_id.keys()):
        dest_row = dest_by_id[_id]
        if _id in src_by_id:
            # 按 id 逐行检查
            src_row = src_by_id[_id]

            dest_row_origin = tuple(dest_row[i] for i in origin_col_ids)
            src_row_origin = tuple(src_row[i] for i in origin_col_ids)
            dest_row_translation = tuple(dest_row[i] for i in translation_col_ids)
            src_row_translation = tuple(src_row[i] for i in translation_col_ids)
            empty_row_translation = tuple('' for i in translation_col_ids)

            # 检查原文是否相等
            if dest_row_origin != src_row_origin:
                conflict_data.append(dest_row)
            # 如果原文相等，并且 src 的译文非空
            elif src_row_translation != empty_row_translation:
                # 检查 dest 的译文是否为空
                if dest_row_translation != empty_row_translation:
                    # 译文都非空且不等，判定为冲突
                    if dest_row_translation != src_row_translation:
                        conflict_data.append(dest_row)
                else:
                    # 空，则拷贝译文
                    merged_count += 1
                    for i in translation_col_ids:
                        dest_row[i] = src_row[i]
        else:
            # src 没有此 id，判为冲突（新增）
            conflict_data.append(dest_row)
        merged_data.append(dest_row)

    print('copy %d rows to dest' % merged_count)
    return merged_data, conflict_data


def format_file_path(filename, default_path):
    """如果只有名字，就到 default_path 找 filename"""
    if '\\' not in filename and '/' not in filename:
        filename = os.path.join(default_path, filename)
    return filename


def main():
    cd = sys.path[0]
    translation_path = os.path.join(cd, '../translation/lang/translated')

    if len(sys.argv) not in (3, 4):
        usage()
        sys.exit(2)

    # init path
    dest_xls_file, src_xls_file = (format_file_path(name, translation_path) for name in (sys.argv[1], sys.argv[2]))
    conflict_xls_file = None
    if len(sys.argv) == 4:
        conflict_xls_file = format_file_path(sys.argv[3], translation_path)

    # merge translation & save
    merge_translation_file(dest_xls_file, src_xls_file, conflict_xls_file)


if __name__ == '__main__':
    main()
