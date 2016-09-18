#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : test_ui_line.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 
# 


import unittest
from objs.ui_line import UiLine


class TestUiLine(unittest.TestCase):
    def test_ctor(self):
        line = 'SafeAddString(SI_DIALOG_NO, "No", 2)'
        ui_line = UiLine.from_lua_line(line)
        self.assertEqual(line, ui_line.to_lua_line())

    def test_ctor_file_header(self):
        self.assertIsNone(UiLine.from_lua_line('-- NOTE:'))

    def test_translation(self):
        ui_line = UiLine.from_lua_line('SafeAddString(SI_DIALOG_NO, "No", 2)')
        ui_line.set_translation('否')
        self.assertEqual('否', ui_line.translation)
