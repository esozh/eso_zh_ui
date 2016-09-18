#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : test_ui_mgr.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 
# 


import unittest
from objs.ui_mgr import UiMgr


class TestUiMgr(unittest.TestCase):
    def setUp(self):
        self.lua = [
            'SafeAddString(SI_ABILITYUPGRADELEVEL0, "None", 0)',
            '无',
            'SafeAddString(SI_ABILITYUPGRADELEVEL1, "Bronze", 0)\n',
            '青铜',
            'SafeAddString(SI_ABILITYUPGRADELEVEL2, "Silver", 0)\n',
            'SafeAddString(SI_ABILITYUPGRADELEVEL3, "Gold", 0)\n',
            '黄金\n',
        ]
        self.mgr = UiMgr()
        self.mgr.load_lua_lines(self.lua)

    def test_load_lua(self):
        self.assertEqual(4, len(self.mgr.ui_lines))
        self.assertEqual('None', self.mgr.ui_lines['SI_ABILITYUPGRADELEVEL0'].origin)
        self.assertEqual('', self.mgr.ui_lines['SI_ABILITYUPGRADELEVEL0'].translation)

    def test_apply_translation_txt(self):
        """测试从 .txt 文本文件中读入的翻译"""
        self.mgr.apply_translate_from_txt_lines(self.lua)

        self.assertEqual(4, len(self.mgr.ui_lines))
        self.assertEqual('None', self.mgr.ui_lines['SI_ABILITYUPGRADELEVEL0'].origin)
        self.assertEqual('无', self.mgr.ui_lines['SI_ABILITYUPGRADELEVEL0'].translation)
        self.assertEqual('', self.mgr.ui_lines['SI_ABILITYUPGRADELEVEL2'].translation)
        self.assertEqual('黄金', self.mgr.ui_lines['SI_ABILITYUPGRADELEVEL3'].translation)

    def test_apply_unknown_txt(self):
        """测试翻译 .txt 时的异常处理"""
        lua = [
            'SafeAddString(SI_ABILITYUPGRADELEVEL0, "Fake None", 0)',
            '无',
            'SafeAddString(SI_ABILITY_ACTION_CLEAR_SLOT, "Remove", 1)',
            '移除',
        ]
        self.mgr.load_lua_lines(self.lua)
        self.mgr.apply_translate_from_txt_lines(lua)

        self.assertEqual('', self.mgr.ui_lines['SI_ABILITYUPGRADELEVEL0'].translation)
        self.assertFalse('SI_ABILITY_ACTION_CLEAR_SLOT' in self.mgr.ui_lines.keys())

    def test_apply_translation_xls(self):
        """测试应用从 xls 读入的数据"""
        data = [
            ['1', 'SI_ABILITYUPGRADELEVEL0', 'None', '无', '', '', '', ''],
            ['2', 'SI_ABILITYUPGRADELEVEL1', 'None', '无', '', '', '', ''],
            ['3', 'SI_ABILITYUPGRADELE__FAKE', 'None', '无', '', '', '', ''],
        ]
        self.mgr.apply_translate_from_xls(data)

        self.assertEqual('None', self.mgr.ui_lines['SI_ABILITYUPGRADELEVEL0'].origin)
        self.assertEqual('无', self.mgr.ui_lines['SI_ABILITYUPGRADELEVEL0'].translation)
        self.assertEqual('', self.mgr.ui_lines['SI_ABILITYUPGRADELEVEL1'].translation)
        self.assertFalse('SI_ABILITYUPGRADELE__FAKE' in self.mgr.ui_lines.keys())

    def test_get_rows(self):
        """测试生成 xls 数据的能力"""
        rows = self.mgr.get_rows()
        rows_list = [ui_row.to_list() for name, ui_row in sorted(rows.items())]
        expected_rows_list = [
            ['1', 'SI_ABILITYUPGRADELEVEL0', 'None', '', '', '', '', ''],
            ['2', 'SI_ABILITYUPGRADELEVEL1', 'Bronze', '', '', '', '', ''],
            ['3', 'SI_ABILITYUPGRADELEVEL2', 'Silver', '', '', '', '', ''],
            ['4', 'SI_ABILITYUPGRADELEVEL3', 'Gold', '', '', '', '', ''],
        ]
        self.assertEqual(expected_rows_list, rows_list)

        self.mgr.apply_one_translate('SI_ABILITYUPGRADELEVEL0', 'None', '无')
        expected_rows_list[0][3] = '无'
        rows = self.mgr.get_rows()
        rows_list = [ui_row.to_list() for name, ui_row in sorted(rows.items())]
        self.assertEqual(expected_rows_list, rows_list)

    def test_get_txt_lines(self):
        """测试生成 .txt 的能力"""
        lines = self.mgr.get_txt_lines()
        expected_lines = [
            'SafeAddString(SI_ABILITYUPGRADELEVEL0, "None", 0)\n',
            'SafeAddString(SI_ABILITYUPGRADELEVEL1, "Bronze", 0)\n',
            'SafeAddString(SI_ABILITYUPGRADELEVEL2, "Silver", 0)\n',
            'SafeAddString(SI_ABILITYUPGRADELEVEL3, "Gold", 0)\n',
        ]
        self.assertEqual(expected_lines, lines)

        self.mgr.apply_one_translate('SI_ABILITYUPGRADELEVEL0', 'None', '无')
        lines = self.mgr.get_txt_lines()
        expected_lines[1:1] = ['无\n', ]
        self.assertEqual(expected_lines, lines)

    def test_get_str_lines(self):
        """测试生成 .str 的能力"""
        lines = self.mgr.get_str_lines()
        expected_lines = [
            '[SI_ABILITYUPGRADELEVEL0] = "None"\n',
            '[SI_ABILITYUPGRADELEVEL1] = "Bronze"\n',
            '[SI_ABILITYUPGRADELEVEL2] = "Silver"\n',
            '[SI_ABILITYUPGRADELEVEL3] = "Gold"\n',
        ]
        self.assertEqual(expected_lines, lines)

        self.mgr.apply_one_translate('SI_ABILITYUPGRADELEVEL2', 'Silver', '白银')

        lines = self.mgr.get_str_lines(mode='origin')
        self.assertEqual(expected_lines, lines)
        lines = self.mgr.get_str_lines(mode='translation')
        expected_lines[2] = '[SI_ABILITYUPGRADELEVEL2] = "白银"\n'
        self.assertEqual(expected_lines, lines)
        lines = self.mgr.get_str_lines()
        expected_lines[2] = '[SI_ABILITYUPGRADELEVEL2] = "Silver 白银"\n'
        self.assertEqual(expected_lines, lines)
