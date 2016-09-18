#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : lang_line.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : .lang.csv 翻译时的一行
# 


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

    @staticmethod
    def from_csv_line(line):
        """从 csv 文件的一行里构造

        Args:
            line(str): csv 里的一行

        Returns:
            return (LangLine | None): 从这一行里构造出的 LangLine 对象
        """
        data = line.strip().split(',', 4)
        try:
            file_id, unknown, index, offset = [int(v[1:-1]) for v in data[0:4]]
            text = data[4][1:-1]
            return LangLine(file_id, unknown, index, offset, text)
        except ValueError:
            # 文件头等，类型转换失败
            return None

    def set_origin_jp(self, origin_jp):
        self.origin_jp = origin_jp

    def set_translation(self, translation):
        self.translation = translation

    def to_csv_line(self):
        text = self.translation if self.translation != '' else self.origin
        return '"%d","%d","%d","%d","%s"' % (self.file_id, self.unknown, self.index, self.offset, text)
