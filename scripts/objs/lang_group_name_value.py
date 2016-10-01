#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : lang_group_name_value.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : .lang.csv 翻译时的一组数据，一个名字行与若干内容行，有共同的 index，
#                 例如 成就名 与 (成就描述，成就子目标)
# 


from objs.lang_group import LangGroup


class LangGroupNameValue(LangGroup):
    """继承自 LangLines, alias 保存 name, value 两个 key"""
    def __init__(self, index):
        """构造函数

        Args:
            index (int):
        """
        super().__init__(index)

    @staticmethod
    def get_header():
        return '行号\t内部编号\t日文\t英文\t中文\t日文\t英文\t中文\t初翻人员\t校对\t润色\t备注\n'

    @staticmethod
    def get_named_header(name_title, desc_title):
        return '行号\t内部编号\t日文%s\t英文%s\t中文%s\t日文%s\t英文%s\t中文%s\t初翻人员\t校对\t润色\t备注\n' % \
               (name_title, name_title, name_title, desc_title, desc_title, desc_title)

    def add_line(self, line, key=None):
        raise RuntimeError('not supported. please use "add_name" or "add_value".')

    def add(self, file_id, unknown, index, offset, origin):
        raise RuntimeError('not supported. please use "add_name" or "add_value".')

    def add_name(self, line):
        """add_line 改版，索引为 name"""
        super(LangGroupNameValue, self).add_line(line, key='name')

    def add_value(self, line):
        """add_line 改版，索引为 value"""
        super(LangGroupNameValue, self).add_line(line, key='value')

    def get_key(self):
        """用于去重，减少翻译工作的 key"""
        name = ''
        value = ''
        if 'name' in self.lines.keys():
            name = self.lines['name'].origin
        if 'value' in self.lines.keys():
            value = self.lines['value'].origin
        if name == '' or value == '':
            raise RuntimeError('empty LangLines')
        return '%s-%s' % (name, value)
