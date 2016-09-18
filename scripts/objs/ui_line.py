#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : ui_line.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : UI 翻译时 .lua 的一行
# 


class UiLine:
    def __init__(self, name):
        """构造函数

        Args:
            name(str): SI_ 开头的名字
        """
        self.name = name        # 名字
        self.origin = ''        # 原文
        self.translation = ''   # 译文
        self.version = ''       # 版本（未用）

    @staticmethod
    def from_lua_line(line):
        """从 lua 文件的一行里构造

        Args:
            line(str): lua 里的一行

        Returns:
            return (UiLine | None): 从这一行里构造出的 UiLine 对象
        """
        line = line.strip()
        if line.startswith('SafeAddString'):
            name = line.split('(', 1)[1].split(',', 1)[0].strip()
            text = line.split(',', 1)[1].rsplit(',', 1)[0].strip()
            text = text[1:-1]     # remove quotes
            version = line.rsplit(',', 1)[1].strip(')').strip()
            return UiLine(name).set_origin(text).set_version(version)
        else:
            return None

    def set_origin(self, origin):
        self.origin = origin
        return self

    def set_translation(self, translation):
        self.translation = translation
        return self

    def set_version(self, version):
        self.version = version
        return self

    def to_lua_line(self):
        return 'SafeAddString(%s, "%s", %s)' % (self.name, self.origin, self.version)
