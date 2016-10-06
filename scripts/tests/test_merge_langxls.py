#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : test_merge_langxls.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 
# 


import unittest
from merge_langxls import merge_translation_by_col


class TestMergeLangXls(unittest.TestCase):
    def test_merge_translation_by_col(self):
        dest_data = [
            ['0', 'id_1', 'o1', ''],
            ['1', 'id_2', 'o2', 't2'],
            ['2', 'id_3', 'o3', ''],
            ['3', 'id_4', 'o4', 't4'],
            ['4', 'id_5', 'o5', 't5'],
            ['5', 'id_6', 'o6', 't6'],
            ['6', 'id_7', 'o7', 't7']   # 只在 dest 中
        ]
        src_data = [
            ['0', 'id_1', 'o1', ''],    # 都未翻译
            ['0', 'id_2', 'o2', ''],    # 仅 dest 有译文
            ['0', 'id_3', 'o3', 't3'],  # 仅 src 有译文
            ['4', 'id_4', 'o?', 't4'],  # 原文冲突
            ['4', 'id_5', 'o5', 't?'],  # 译文冲突
            ['4', 'id_6', 'o6', 't6'],  # 相同译文
            ['4', 'id_8', 'o8', 't8']   # 只在 src 中
        ]
        exp_merged = [
            ['0', 'id_1', 'o1', ''],
            ['1', 'id_2', 'o2', 't2'],
            ['2', 'id_3', 'o3', 't3'],
            ['3', 'id_4', 'o4', 't4'],
            ['4', 'id_5', 'o5', 't5'],
            ['5', 'id_6', 'o6', 't6'],
            ['6', 'id_7', 'o7', 't7']
        ]
        exp_conflict = [
            ['3', 'id_4', 'o4', 't4'],
            ['4', 'id_5', 'o5', 't5'],
            ['6', 'id_7', 'o7', 't7']
        ]

        merged_data, conflict_data = merge_translation_by_col(dest_data, src_data, 1, [2, ], [3, ])
        self.assertEqual(exp_merged, merged_data)
        self.assertEqual(exp_conflict, conflict_data)

