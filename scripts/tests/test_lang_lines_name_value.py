#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : test_lang_lines_name_value.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 
# 


import unittest
from objs.lang_lines_name_value import LangLinesNameValue


class TestLangLinesNameValue(unittest.TestCase):
    def setUp(self):
        self.lang_lines = LangLinesNameValue(3)
        self.line_name = '"3427285","0","3","0","Laugh"'
        self.line_value = '"111","1","3","0","laugh..."'
        self.lang_lines.add_name(self.line_name)
        self.lang_lines.add_value(self.line_value)

    def test_add_name_value(self):
        self.assertEqual(self.line_name, self.lang_lines.lines['name'].to_csv_line())
        self.assertEqual(self.line_value, self.lang_lines.lines['value'].to_csv_line())

    def test_to_csv_lines(self):
        lines = [self.line_name, self.line_value]
        self.assertEqual(lines, self.lang_lines.to_csv_lines())

    def test_get_key(self):
        self.assertEqual('Laugh-laugh...', self.lang_lines.get_key())

    def test_add_line(self):
        self.assertRaises(RuntimeError, self.lang_lines.add_line, self.line_name)
