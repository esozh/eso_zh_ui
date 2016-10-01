#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : lang_lines.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : .lang.csv 翻译时的行，以 index 为 key，管理 LangLine
# 


from objs.lang_line import LangLine


class LangLines:
    def __init__(self, index):
        """构造函数

        Args:
            index (int):
        """
        self.index = index
        self.lines = {}

    @staticmethod
    def get_header():
        return '行号\t内部编号\t日文\t英文\t中文\t初翻人员\t校对\t润色\t备注\n'

    def add_line(self, line, key=None):
        """添加一行其他内容

        index 必须与当前一致

        Args:
            line(str): csv 里的一行
            key(str): 指定 key
        """
        lang_line = LangLine.from_csv_line(line)

        if lang_line is None:
            raise RuntimeError('failed to create lang line')
        if lang_line.index != self.index:
            raise RuntimeError('index does not match')

        if key is None:
            key = lang_line.get_key()
        self.lines[key] = lang_line

    def add(self, file_id, unknown, index, offset, origin):
        """添加一行其他内容

        index 必须与当前一致

        Args:
            file_id (int): ID
            unknown (int):
            index (int):
            offset (int):
            origin (str): 原文
        """
        if index != self.index:
            raise RuntimeError('index does not match')

        lang_line = LangLine(file_id, unknown, index, offset, origin)
        self.lines[lang_line.get_key()] = lang_line

    def to_csv_lines(self):
        csv_lines = []
        for key in sorted(self.lines):
            print(key)
            csv_lines.append(self.lines[key].to_csv_line())
        return csv_lines
