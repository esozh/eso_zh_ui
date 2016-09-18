#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : test_ui_row.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 
# 


import unittest
from objs.ui_row import UiRow


class TestUiRow(unittest.TestCase):
    def test_ctor(self):
        header = UiRow('名称') \
                .set_id('编号') \
                .set_origin('原文') \
                .set_translation('译文') \
                .set_translator('初翻人员') \
                .set_proofreader('校对') \
                .set_refiner('润色') \
                .set_comments('备注')
        self.assertEqual(['编号', '名称', '原文', '译文', '初翻人员', '校对', '润色', '备注'],
                         header.to_list())
