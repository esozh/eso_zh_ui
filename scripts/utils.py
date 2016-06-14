#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : utils.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 将 .txt 文件转换为 .str 文件。其中 .txt 文件是翻译过的 .lua 文件。
# 


def read_lua(file_path, name_values):
    with open(file_path, 'rt', encoding='utf-8') as fp:
        for line in fp.readlines():
            line = line.strip()
            if line.startswith('SafeAddString'):
                name = line.split('(', 1)[1].split(',', 1)[0].strip()
                value = line.split(',', 1)[1].rsplit(',', 1)[0].strip().strip('"')
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
