#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : lang_mgr.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : .lang.csv 翻译时的管理工具
# 


import os
from objs.lang_group import LangGroup
from utils.utils import load_lang_csv, parse_csv_line


class LangMgr:
    def __init__(self, translation_path, file_id_list):
        """构造函数

        Args:
            translation_path (str): 翻译文件的路径
            file_id_list (list[int]):
        """
        self.lang_groups = {}       # 根据文件 id 组织的 LangGroup 集合，每个小集合按 index 组织
        for file_id in file_id_list:
            lang_groups = {}
            # 英文
            file_path = os.path.join(translation_path, 'en.%s.lang.csv' % file_id)
            for line in load_lang_csv(file_path, skip_header=False):
                _, _, index, _, _ = parse_csv_line(line)
                if index not in lang_groups.keys():
                    # 如果是新出现的 index，则新建
                    lang_groups[index] = LangGroup(index)
                lang_groups[index].add_line(line)
            # 日文
            file_path_jp = os.path.join(translation_path, 'en.%s.lang.csv' % file_id)
            for line in load_lang_csv(file_path_jp, skip_header=False):
                _, _, index, _, origin_jp = parse_csv_line(line)
                if index not in lang_groups.keys():
                    # 如果是新出现的 index，则舍弃
                    print('new index from jp: %s' % line)
                    continue
                lang_groups[index].add_jp(line)

            self.lang_groups[file_id] = lang_groups

    @staticmethod
    def get_header():
        return ['行号', '内部编号', '日文', '英文', '中文', '初翻人员', '校对', '润色', '备注']

    def to_xls_list(self):
        """转换为写入 .xlsx 翻译文件的列表"""
        xls_list = []
        for key1 in sorted(self.lang_groups):
            lang_groups = self.lang_groups[key1]
            for key2 in sorted(lang_groups):
                lang_group = lang_groups[key2]
                xls_list.extend(lang_group.to_xls_list())
        # 重新编号
        i = 0
        for row in xls_list:
            row[0] = '%02d' % i
            i += 1
        return xls_list
