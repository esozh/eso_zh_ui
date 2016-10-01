#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : lang_line.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : .lang.csv 翻译时的一行
# 


from utils.utils import parse_csv_line


class LangLine:
    def __init__(self, file_id, unknown, index, offset, origin):
        """构造函数

        Args:
            file_id (int): ID
            unknown (int):
            index (int):
            offset (int):
            origin (str): 原文
        """
        self.file_id = file_id
        self.unknown = unknown
        self.index = index
        self.offset = offset
        self.origin = origin
        self.origin_jp = None
        self.translation = ''
        self.translator = ''    # 初翻
        self.proofreader = ''   # 校对
        self.refiner = ''       # 润色
        self.comments = ''      # 备注

    @staticmethod
    def from_csv_line(line):
        """从 csv 文件的一行里构造

        Args:
            line(str): csv 里的一行

        Returns:
            return (LangLine | None): 从这一行里构造出的 LangLine 对象
        """
        data = parse_csv_line(line)
        if data is None:
            return None
        else:
            file_id, unknown, index, offset, origin = data
            return LangLine(file_id, unknown, index, offset, origin)

    def set_origin_jp(self, origin_jp):
        self.origin_jp = origin_jp

    def set_translation(self, translation):
        self.translation = translation

    def get_key(self):
        return '%d-%d-%d' % (self.file_id, self.unknown, self.index)

    def get_xls_key(self):
        return '%09d-%02d-%05d' % (self.file_id, self.unknown, self.index)

    def to_csv_line(self):
        """转换为写入 lang.csv 文件的行"""
        text = self.translation if self.translation != '' else self.origin
        return '"%d","%d","%d","%d","%s"' % (self.file_id, self.unknown, self.index, self.offset, text)
