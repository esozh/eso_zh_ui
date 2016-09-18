#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : test_lang_line.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 
# 


import unittest
from objs.lang_line import LangLine


class TestLangLine(unittest.TestCase):
    def test_ctor(self):
        line = '"3427285","0","3","0","Laugh"'
        lang_line = LangLine.from_csv_line(line)
        self.assertEqual(line, lang_line.to_csv_line())

    def test_ctor_file_header(self):
        self.assertIsNone(LangLine.from_csv_line('"ID","Unknown","Index","Offset","Text"'))

    def test_translation(self):
        lang_line = LangLine.from_csv_line('"3427285","0","3","0","Laugh"')
        lang_line.set_translation('笑')
        self.assertEqual('"3427285","0","3","0","笑"', lang_line.to_csv_line())
