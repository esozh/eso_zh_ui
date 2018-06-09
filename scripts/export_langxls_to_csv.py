#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : export_langxls_to_csv.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 从 csv 提取原文，从 xls 提取汉化，写入 zh.lang.csv 中
# 


import os
import sys

from utils.lang_def import *
from utils.utils import merge_dict
from utils.langxls_loader import load_from_langxls
from utils.text_replacer import TextReplacer
from utils import log


def load_translation(translation_path):
    """从文件夹中读取所有翻译文件

    Args:
        translation_path (str): 存放翻译 xlsx 文件的路径或文件

    Returns:
        category_to_translated (dict[str: list]): dict<str, list>, 根据 category 归类的翻译
    """
    file_list = []
    if os.path.isfile(translation_path):
        file_list.append((translation_path, translation_path))
    else:
        for dir_path, dir_names, file_names in os.walk(translation_path):
            for file_name in file_names:
                if file_name.lower().endswith('.xlsx') and not file_name.startswith('~'):
                    file_path = os.path.join(dir_path, file_name)
                    file_list.append((file_name, file_path))

    category_to_translated = {}
    for file_name, file_path in file_list:
        # load from one file
        log.info('load from %s' % file_name)
        category, translated_data = load_from_langxls(file_path, "zh", need_check=True)
        log.info('load %d %ss' % (len(translated_data), category))
        if category in category_to_translated:
            log.warning('warning: override category %s' % category)
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


def get_en_line_to_zh_line(lines, translated_data):
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

    # 批量替换文本
    replacer = TextReplacer()

    # {"en_line": "zh_line"}
    en_line_to_zh_line = {}
    for file_id, unknown, index, zh_text in translated_data:
        key = '"%s","%s","%s"' % (file_id, unknown, index)
        if key in en_key_to_line:
            en_line = en_key_to_line[key]
            file_id, unknown, index, offset, en_text = en_line.split(',', 4)
            # 处理汉化过的文本里的特殊标记
            zh_text = replacer.replace(zh_text)
            zh_line = '%s,%s,"%s"\n' % (key, offset, zh_text.replace('"', '""').replace('""""', '""'))
            en_line_to_zh_line[en_line] = zh_line

    return en_line_to_zh_line


def get_translated_lines_converter(file_id_to_lines, category_to_translated):
    """转换格式

    Args:
        file_id_to_lines (dict[int: list[str]]):
                key 为 file_id,
                value 为 list<line>, 每行的格式为 "ID","Unknown","Index","Offset","Text"
        category_to_translated (dict[str: list]): dict,
                key 为 category,
                value 为 list of [file_id, unknown, index, text]

    Returns:
        en_line_to_zh_line (dict[str: str]): key 为原文的行， value 为译文的行
    """

    translated_count_dry = 0    # 不包括重复的

    # translated_dict, {"en_line": "zh_line"}
    en_line_to_zh_line = {}
    # 已经处理过的 file_id
    translated_file_ids = []

    # 遍历从每个 xls 读入的数据
    for category, translated_data in sorted(category_to_translated.items()):
        translated_count_dry += len(translated_data)
        possible_file_ids = []
        # 根据 category 决定处理方法
        if category in file_id_of_list.keys():
            possible_file_ids = file_id_of_list[category]
        elif category in file_id_of_array.keys():
            possible_file_ids = file_id_of_array[category]
        elif category in file_id_of_pair.keys():
            possible_file_ids = file_id_of_pair[category]
        translated_file_ids.extend(possible_file_ids)
        # 需要判断的行
        possible_lines = []
        for file_id in possible_file_ids:
            file_id = int(file_id)
            if file_id in file_id_to_lines:
                possible_lines.extend([line for line in file_id_to_lines[int(file_id)]])
        # load translation
        en_line_to_zh_line_of_category = get_en_line_to_zh_line(possible_lines, translated_data)
        # merge translation
        en_line_to_zh_line = merge_dict(en_line_to_zh_line, en_line_to_zh_line_of_category)

    log.info('%d(%d) lines translated' % (translated_count_dry, len(en_line_to_zh_line)))
    return en_line_to_zh_line


def expand_translated_lines_converter(en_line_to_zh_line, en_lines, jp_lines):
    """处理之前剩下的行
    不同 file_id,unknown,index 对应的文本有可能相同，这种情况下，只要翻译了一个地方，其他地方就可以使用已有的翻译表
    必须英文、日文原文都一致才可以

    Args:
        en_line_to_zh_line (dict[str: str]): key 为原文的行， value 为译文的行
        en_lines (list[str]): 英文原文
        jp_lines (list[str]): 日文原文

    Returns:
        en_line_to_zh_line (dict[str: str]): key 为原文的行， value 为译文的行
    """

    other_translated_count = 0

    en_line_to_jp_text = get_en_line_to_jp_text(en_lines, jp_lines)
    enjp_text_to_zh_text = {}   # 这里不考虑大小写
    for en_line, zh_line in sorted(en_line_to_zh_line.items()):
        _, _, _, _, en_text = en_line.strip().split(',', 4)
        _, _, _, _, zh_text = zh_line.strip().split(',', 4)
        if en_line in en_line_to_jp_text:
            jp_text = en_line_to_jp_text[en_line]
            # 处理其他行时不考虑大小写
            enjp_text_to_zh_text[en_text.lower() + ',' + jp_text.lower()] = zh_text

    # 排除英文原文中已经翻译过的
    en_lines = [line for line in en_lines if line not in en_line_to_zh_line.keys()]
    # 日文原文
    fileid_unknown_index_to_jp_text = get_fileid_unknown_index_to_text(jp_lines)

    for line in en_lines:
        file_id, unknown, index, offset, en_text = line.strip().split(',', 4)
        key = ','.join((file_id, unknown, index))
        # 在日文原文里要存在
        if key in fileid_unknown_index_to_jp_text:
            enjp_text = en_text.lower() + ',' + fileid_unknown_index_to_jp_text[key].lower()
            # 并且这一行英文、日文原文都与已翻译的某一行的原文相等
            if enjp_text in enjp_text_to_zh_text:
                # 那么，直接使用翻译
                zh_line = '%s,%s,%s,%s,%s\n' % (file_id, unknown, index, offset, enjp_text_to_zh_text[enjp_text])
                en_line_to_zh_line[line] = zh_line
                other_translated_count += 1

    log.info('%d more lines translated' % other_translated_count)
    log.info('%d lines left' % (len(en_lines) - other_translated_count))

    return en_line_to_zh_line


def get_fileid_unknown_index_to_text(lines):
    """以 "file_id","unknown","index" 为 key, 以 text 为 value"""
    fileid_unknown_index_to_text = {}
    for line in lines:
        file_id, unknown, index, offset, text = line.strip().split(',', 4)
        fileid_unknown_index_to_text[','.join((file_id, unknown, index))] = text
    return fileid_unknown_index_to_text


def get_en_line_to_jp_text(en_lines, jp_lines):
    """从英文行获取日文文本

    Args:
        en_lines (list[str]): 英文原文
        jp_lines (list[str]): 日文原文

    Returns:
        en_line_to_jp_text: (dict[str: str]): 从英文行获取日文文本
    """
    jp_key_to_text = {}
    # 日文对照表
    for line in jp_lines:
        file_id, unknown, index, offset, text = line.strip().split(',', 4)
        # 日文的 offset 可能与英文不同，所以 key 忽略 offset
        jp_key_to_text[','.join((file_id, unknown, index))] = text

    en_line_to_jp_text = {}
    for line in en_lines:
        file_id, unknown, index, offset, text = line.strip().split(',', 4)
        key = ','.join((file_id, unknown, index))
        if key in jp_key_to_text:
            en_line_to_jp_text[line] = jp_key_to_text[key]
    return en_line_to_jp_text


def get_checked_line(line):
    """屏蔽 EsoExtractData 不支持的格式"""
    if line.endswith(r'\\"' + '\n'):
        return line[:-3] + r'\\ "' + '\n'
    else:
        return line


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
    log.info('read %d lines from en.lang.csv.' % len(lines))

    src_jp_lang_file = os.path.join(src_path, 'jp.lang.csv')
    with open(src_jp_lang_file, 'rt', encoding='utf-8') as fp:
        fp.readline()   # skip
        # lines_jp: 日文原文件中的行
        lines_jp = fp.readlines()
        full_ids_jp = {','.join(line.split(',', 4)[:3]) for line in lines_jp}
    log.info('read %d lines from jp.lang.csv.' % len(lines_jp))

    file_id_to_lines = get_file_id_to_lines(lines)

    # load translation
    category_to_translated = load_translation(translation_path)

    # get result
    en_line_to_zh_line = get_translated_lines_converter(file_id_to_lines, category_to_translated)
    en_line_to_zh_line = expand_translated_lines_converter(en_line_to_zh_line, lines, lines_jp)
    translated_lines = []
    for en_line in lines:
        # 先检查是否已翻译
        if en_line in en_line_to_zh_line.keys():
            translated_lines.append(get_checked_line(en_line_to_zh_line[en_line]))
        else:
            # 不再检查在日文文本里是否有
            translated_lines.append(get_checked_line(en_line))

    # save result
    dest_lang_file = os.path.join(translation_path, 'zh.lang.csv')
    with open(dest_lang_file, 'wt', encoding='utf-8') as fp:
        fp.write(header)
        fp.writelines(translated_lines)
    log.info('write to zh.lang.csv')


if __name__ == '__main__':
    log.debug('main() with args: %s' % str(sys.argv))
    main()
