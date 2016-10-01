#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : lang_group.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : .lang.csv 翻译时的行，以 index 为 key，管理 LangLine
# 


from objs.lang_line import LangLine


class LangGroup:
    def __init__(self, index):
        """构造函数

        Args:
            index (int):
        """
        self.index = index
        self.lines = {}

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

    def add_jp(self, line, key=None):
        """添加一行日文原文

        index 必须与当前一致

        Args:
            line(str): jp.csv 里的一行
            key(str): 指定 key
        """
        lang_line_jp = LangLine.from_csv_line(line)

        if lang_line_jp is None:
            raise RuntimeError('failed to create lang line')
        if lang_line_jp.index != self.index:
            raise RuntimeError('index does not match')

        if key is None:
            key = lang_line_jp.get_key()
        if key in self.lines:
            self.lines[key].set_origin_jp(lang_line_jp.origin)

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
        """转换为写入 lang.csv 文件的行"""
        csv_lines = []
        for key in sorted(self.lines):
            csv_lines.append(self.lines[key].to_csv_line())
        return csv_lines

    def to_xls_list(self):
        """转换为写入 .xlsx 翻译文件的列表

        Returns:
            xls_list (list[list[str]]): xls_list 中的每一个 list 代表一行
        """
        i = 1
        xls_list = []
        for key in sorted(self.lines):
            lang_line = self.lines[key]
            if lang_line.origin_jp is not None:     # 日文没有的行可以删除
                plain_list = [
                    i, lang_line.get_xls_key(), lang_line.origin_jp, lang_line.origin, lang_line.translation,
                    lang_line.translator, lang_line.proofreader, lang_line.refiner, lang_line.comments
                ]
                xls_list.append([str(value) for value in plain_list])
                i += 1
        return xls_list
