#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : ui_mgr.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : UI 翻译管理工具
#


from objs.ui_line import UiLine
from objs.ui_row import UiRow
from utils.utils import read_translate_txt


class UiMgr:
    """
    Attributes:
        lines (dict[str: UiLine]):
    """
    def __init__(self):
        self.lines = {}

    def load_lua_file(self, lua_file_path):
        """从 lua 文件加载

        Args:
            lua_file_path (str): .lua 文件的路径
        """
        with open(lua_file_path, 'rt', encoding='utf-8') as fp:
            for line in fp.readlines():
                line = UiLine.from_lua_line(line)
                if line is not None:
                    self.lines[line.name] = line

    def apply_translate_txt(self, txt_file_path):
        """从 _translate.txt 加载

        不检查更新

        Args:
            txt_file_path (str): 翻译的 _translate.txt 路径
        """
        lines_with_translation = read_translate_txt(txt_file_path)
        for name, line in lines_with_translation.items():
            if name in self.lines.keys() and line.origin == self.lines[name].origin:
                self.lines[name].set_translation(line.translation)

    def get_rows(self):
        """转换成写入 .xls 的 UiRow 列表

        Returns:
            return (dict[str: UiRow]): 名字 - UiRow
        """
        rows = {}
        count = 0
        for name, line in sorted(self.lines.items()):
            count += 1
            row = UiRow(name) \
                .set_origin(line.origin) \
                .set_translation(line.translation) \
                .set_id(count)
            rows[name] = row
        return rows

    def get_txt_lines(self):
        """转换成写入 .txt 的行

        Returns:
            return (list[str]): 要写入的行的列表
        """
        lines = []
        for name, line in sorted(self.lines.items()):
            lines.append(line.to_lua_line() + '\n')
            if line.translation != '':
                lines.append(line.translation + '\n')
        return lines

    def get_str_lines(self, mode='both'):
        """转换成写入 .str 的行

        Args:
            mode (str): 翻译模式， origin, translation, both

        Returns:
            return (list[str]): 要写入的行的列表
        """
        lines = []
        for name, line in sorted(self.lines.items()):
            value = line.origin
            if line.translation != '':
                if mode == 'translation':
                    value = line.translation
                elif mode == 'both':
                    value += ' ' + line.translation
            lines.append('[%s] = "%s"\n' % (name, value))
        return lines
