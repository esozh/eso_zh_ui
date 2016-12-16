#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : test_util.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 
# 


import unittest
from utils.utils import *


class TestUtil(unittest.TestCase):
    def test_almost_equals(self):
        str1 = 'ab, cDe(0)'
        str2 = 'abcd-e0'
        str3 = 'abcd-e'
        self.assertTrue(almost_equals(str1, str2))
        self.assertFalse(almost_equals(str1, str3))


def xls_list_to_lines(xls_list):
    lines = []
    for row in xls_list:
        row_quoted = ['"%s"' % v for v in row]
        line = ','.join(row_quoted) + '\n'
        lines.append(line)
    return lines
