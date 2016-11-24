#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : lang_mgr.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : .lang.csv 翻译时的管理工具
# 


import os
from objs.lang_group import LangGroup
from utils.utils import load_lang_csv


class LangMgr:
    """结果按 fileid-unknown-index 排序"""
    def __init__(self, translation_path, file_id_list):
        """构造函数

        Args:
            translation_path (str): 翻译文件的路径
            file_id_list (list[str]):
        """
        self.all_lang_groups = {}       # 根据文件 id 组织的 LangGroup 集合，每个小集合按 index 组织
        # 读取文件
        for file_id in file_id_list:
            self.add_file_by_id(translation_path, file_id)

    def add_file_by_id(self, translation_path, file_id_str):
        """添加一个文件

        Args:
            translation_path (str): 翻译文件的路径
            file_id_str (str): 文件 id
        """
        lang_groups = {}
        # 英文
        file_path = os.path.join(translation_path, 'en.%s.lang.csv' % file_id_str)
        if os.path.isfile(file_path):
            for line in load_lang_csv(file_path, skip_header=False):
                file_id, unknown, index, offset = [int(v) for v in line[0:4]]
                origin = line[4]
                if index not in lang_groups.keys():
                    # 如果是新出现的 index，则新建
                    lang_groups[index] = LangGroup(index)
                lang_groups[index].add(file_id, unknown, index, offset, origin)
        # 日文
        file_path_jp = os.path.join(translation_path, 'jp.%s.lang.csv' % file_id_str)
        if os.path.isfile(file_path_jp):
            for line in load_lang_csv(file_path_jp, skip_header=False):
                file_id, unknown, index, offset = [int(v) for v in line[0:4]]
                origin_jp = line[4]
                if index not in lang_groups.keys():
                    # 如果是新出现的 index，则舍弃
                    print('> new index from jp: %s' % line)
                    continue
                lang_groups[index].add_jp(file_id, unknown, index, offset, origin_jp)
        # 添加
        self.all_lang_groups[file_id_str] = lang_groups

    @staticmethod
    def get_header():
        return ['行号', '内部编号', '日文', '英文', '中文', '初翻人员', '校对', '润色', '备注']

    def to_xls_list(self, deduplicate=True):
        """转换为写入 .xlsx 翻译文件的列表

        按 fileid-unknown-index 排序

        Args:
            deduplicate (bool): 是否去重
        """
        xls_list = []
        # 生成列表
        for key1 in sorted(self.all_lang_groups, key=lambda x: int(x)):
            lang_groups = self.all_lang_groups[key1]
            for key2 in sorted(lang_groups):
                lang_group = lang_groups[key2]
                xls_list.extend(lang_group.to_xls_list())
        # 去重
        if deduplicate:
            deduplicate_xls_list = []
            duplicated_text = set()
            for row in xls_list:
                origin, origin_jp = row[2], row[3]
                if (origin, origin_jp) not in duplicated_text:
                    deduplicate_xls_list.append(row)
                    duplicated_text.add((origin, origin_jp))
            xls_list = deduplicate_xls_list
        # 重新编号
        i = 0
        for row in xls_list:
            row[0] = '%d' % i
            i += 1
        return xls_list
