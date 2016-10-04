#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : test_prepare_lang.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 
# 


import os
import sys
import unittest
from prepare_lang import load_lang_list
from utils import xlsutils
from tests import test_util


class TestPrepareLang(unittest.TestCase):
    def setUp(self):
        self.data_path = os.path.join(sys.path[0], 'data')

    def test_load_lang_list(self):
        rows = load_lang_list(['12529189', '188155806', '172030117'], translation_path=self.data_path)
        self.assertEqual(28, len(rows))

        with open(os.path.join(self.data_path, 'achievements.list.csv'), 'rt', encoding='utf-8') as fp:
            lines_exp = fp.readlines()
        lines = test_util.xls_list_to_lines(rows)[1:]
        self.assertEqual(lines_exp, lines)

        # xlsutils.save_xls(os.path.join(self.data_path, 'achievements.list.xls.tmp'), rows)
