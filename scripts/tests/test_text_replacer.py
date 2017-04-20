#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : test_text_replacer.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 
# 


import unittest
from utils.text_replacer import *


class TestUtil(unittest.TestCase):
    def test_replace(self):
        text_replacer = TextReplacer()
        self.assertEqual(text_replacer.replace('abc<<A:1>>d-e0'), 'abc<<1>>d-e0')

    def custom_dict(self):
        my_dict = [('汉字', '漢字')]
        text_replacer = TextReplacer(my_dict)
        self.assertEqual(text_replacer.replace('汉字测试'), '漢字测试')
