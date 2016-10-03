#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : test_lang_mgr.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 
# 


import sys
import os
import unittest
from objs.lang_mgr import LangMgr
from tests import test_util


class TestLangMgr(unittest.TestCase):
    def setUp(self):
        self.data_path = os.path.join(sys.path[0], 'data')

    def test_no_jp(self):
        lang_mgr = LangMgr(self.data_path, ['3427285', ])
        self.assertEqual([], lang_mgr.to_xls_list())

    def test_deduplicate(self):
        lang_mgr = LangMgr(self.data_path, ['12529189', '12529189'])
        xls_list = lang_mgr.to_xls_list()
        self.assertEqual(13, len(xls_list))

    def test_to_xls_list(self):
        lang_mgr = LangMgr(self.data_path, ['12529189', '188155806', '172030117'])
        xls_list = lang_mgr.to_xls_list()
        self.assertEqual(26, len(xls_list))

        with open(os.path.join(self.data_path, 'achievements.list.csv'), 'rt', encoding='utf-8') as fp:
            lines_exp = fp.readlines()
        lines = test_util.xls_list_to_lines(xls_list)
        # with open(os.path.join(self.data_path, 'achievements.list.tmp'), 'wt', encoding='utf-8') as fp:
        #     fp.writelines(lines)
        self.assertEqual(lines_exp, lines)

    def test_to_xls_pair(self):
        pass

    def test_get_header(self):
        lang_mgr = LangMgr(self.data_path, ['12529189', '188155806', '172030117'])
        rows = [lang_mgr.get_header(), ]
        rows.extend(lang_mgr.to_xls_list())
        self.assertEqual(27, len(rows))
        self.assertEqual(len(rows[0]), len(rows[1]))
