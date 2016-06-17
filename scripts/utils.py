#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : utils.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 将 .txt 文件转换为 .str 文件。其中 .txt 文件是翻译过的 .lua 文件。
# 


import xlrd


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


def load_xls(file_path):
    """读取 Excel 文件中的数据。"""
    with xlrd.open_workbook(file_path) as workbook:
        sheet = workbook.sheet_by_index(0)
        nrows = sheet.nrows
        ncols = sheet.ncols
        data = []
        for curr_row in range(0, nrows):
            data.append([str(sheet.cell(curr_row, curr_col).value) for curr_col in range(0, ncols)])
        return data
