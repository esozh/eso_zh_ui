#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : test_lang_lines.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 
# 


import unittest
from objs.lang_lines import LangLines


class TestLangLins(unittest.TestCase):
    def setUp(self):
        self.lang_lines = LangLines(3)
        self.line1 = '"3427285","0","3","0","Laugh"'
        self.line2 = '"111","1","3","0","laugh..."'
        self.lang_lines.add_line(self.line1)
        self.lang_lines.add_line(self.line2)

    def test_add_name_value(self):
        self.assertEqual(self.line1, self.lang_lines.lines['3427285-0-3'].to_csv_line())
        self.assertEqual(self.line2, self.lang_lines.lines['111-1-3'].to_csv_line())

    def test_to_csv_lines(self):
        lines = [self.line2, self.line1]
        self.assertEqual(lines, self.lang_lines.to_csv_lines())
