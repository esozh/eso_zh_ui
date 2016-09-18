#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : ui_mgr.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : UI 翻译管理工具
# 


from objs.ui_line import UiLine
from objs.ui_row import UiRow


class UiMgr:
    """
    Attributes:
        ui_lines (dict[str: UiLine]):
    """
    def __init__(self):
        self.ui_lines = {}

    def load_lua_file(self, lua_file_path):
        """从 lua 文件加载

        Args:
            lua_file_path (str): .lua 文件的路径
        """
        with open(lua_file_path, 'rt', encoding='utf-8') as fp:
            self.load_lua_lines(fp.readlines())

    def apply_translate_from_txt_file(self, txt_file_path):
        """从 _translate.txt 读到的行中加载的翻译

        Args:
            txt_file_path (str): .txt 文件的路径
        """
        with open(txt_file_path, 'rt', encoding='utf-8') as fp:
            self.apply_translate_from_txt_lines(fp.readlines())

    def load_lua_lines(self, lines):
        """从 lua 文件加载

        Args:
            lines (list[str]): .lua 文件中的行
        """
        for line in lines:
            ui_line = UiLine.from_lua_line(line)
            if ui_line is not None:
                self.ui_lines[ui_line.name] = ui_line

    def apply_translate_from_txt_lines(self, lines_from_txt):
        """从 _translate.txt 读到的行中加载的翻译

        只加载已有的 UiLine 的翻译，并且 txt 和 lua 中的原文要一致

        Args:
            lines_from_txt (list[str]): .txt 文件中的行
        """
        # 每一行 SafeAddString 的下一行可能是翻译
        ui_line = None
        for line in lines_from_txt:
            line = line.strip('\n')
            if line.startswith('SafeAddString'):
                # 原文行
                ui_line = UiLine.from_lua_line(line)
            elif (ui_line is not None) and (line != ''):
                # 译文行，检查并应用翻译
                self.apply_one_translate(ui_line.name, ui_line.origin, line)
                ui_line = None

    def apply_translate_from_xls(self, data_from_xls):
        """应用从 xls 文件加载的翻译

        不检查更新

        Args:
            data_from_xls (list[list[str]]): xls 工作表中的数据
        """
        name_column_id, origin_column_id, translation_column_id = 1, 2, 3
        for row_data in data_from_xls:
            name, origin, translation = \
                    row_data[name_column_id], row_data[origin_column_id], row_data[translation_column_id]
            self.apply_one_translate(name, origin, translation)

    def apply_one_translate(self, name, origin, translation):
        """应用一条翻译

        先检查原文是否一致。不检查更新。

        Args:
            name (str): 名字， SI_ 开头
            origin (str): 原文
            translation (str): 译文
        """
        if name in self.ui_lines.keys() and origin == self.ui_lines[name].origin:
            self.ui_lines[name].set_translation(translation)

    def get_rows(self):
        """转换成写入 .xls 的 UiRow 列表

        Returns:
            return (dict[str: UiRow]): 名字 - UiRow
        """
        rows = {}
        count = 0
        for name, ui_line in sorted(self.ui_lines.items()):
            count += 1
            row = UiRow(name) \
                    .set_origin(ui_line.origin) \
                    .set_translation(ui_line.translation) \
                    .set_id(count)
            rows[name] = row
        return rows

    def get_txt_lines(self):
        """转换成写入 .txt 的行

        Returns:
            return (list[str]): 要写入的行的列表
        """
        lines = []
        for name, ui_line in sorted(self.ui_lines.items()):
            lines.append(ui_line.to_lua_line() + '\n')
            if ui_line.translation != '':
                lines.append(ui_line.translation + '\n')
        return lines

    def get_str_lines(self, mode='both'):
        """转换成写入 .str 的行

        Args:
            mode (str): 翻译模式， origin, translation, both

        Returns:
            return (list[str]): 要写入的行的列表
        """
        lines = []
        for name, ui_line in sorted(self.ui_lines.items()):
            value = ui_line.origin
            if ui_line.translation != '':
                if mode == 'translation':
                    value = ui_line.translation
                elif mode == 'both':
                    value += ' ' + ui_line.translation
            lines.append('[%s] = "%s"\n' % (name, value))
        return lines
