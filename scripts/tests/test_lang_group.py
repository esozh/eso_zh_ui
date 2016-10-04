#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : test_lang_group.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 
# 


import unittest
from objs.lang_group import LangGroup


class TestLangGroup(unittest.TestCase):
    def setUp(self):
        self.lang_lines = LangGroup(3)
        self.line1 = '"3427285","0","3","0","Laugh"'
        self.line2 = '"111","1","3","0","laugh..."'
        self.lang_lines.add(3427285, 0, 3, 0, "Laugh")
        self.lang_lines.add(111, 1, 3, 0, "laugh...")

    def test_add_name_value(self):
        self.assertEqual(self.line1, self.lang_lines.lines['3427285-0-3'].to_csv_line())
        self.assertEqual(self.line2, self.lang_lines.lines['111-1-3'].to_csv_line())

    def test_to_csv_lines(self):
        lines = [self.line2, self.line1]
        self.assertEqual(lines, self.lang_lines.to_csv_lines())

    def test_to_xls_list(self):
        self.assertEqual([], self.lang_lines.to_xls_list())

        self.lang_lines.add_jp(3427285, 0, 3, 0, "aaa")
        self.lang_lines.add_jp(111, 1, 3, 0, "bbb")
        xls_list = [
            ['1', '000000111-01-00003', 'bbb', 'laugh...', '', '', '', '', ''],
            ['2', '003427285-00-00003', 'aaa', 'Laugh', '', '', '', '', '']
        ]
        self.assertEqual(xls_list, self.lang_lines.to_xls_list())
