#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : lang_mgr_array.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : .lang.csv 翻译时的管理工具
# 


from objs.lang_mgr import LangMgr


class LangMgrArray(LangMgr):
    """结果按 index-unknown-fileid 排序，假设相同 index 的条目有较强的关联"""
    def __init__(self, translation_path, file_id_list):
        """构造函数

        Args:
            translation_path (str): 翻译文件的路径
            file_id_list (list[str]):
        """
        super().__init__(translation_path=translation_path, file_id_list=file_id_list)

    def to_xls_list(self, deduplicate=True):
        """转换为写入 .xlsx 翻译文件的列表

        按 index-unknown-fileid 排序

        Args:
            deduplicate (bool): 是否去重
        """
        # 生成列表
        xls_list = super().to_xls_list(deduplicate=deduplicate)
        # 按 index-unknown-fileid 排序
        xls_list = sorted(xls_list, key=lambda r: self.get_key_for_row(r))
        # 重新编号
        i = 0
        for row in xls_list:
            row[0] = '%d' % i
            i += 1
        return xls_list

    def get_key_for_row(self, row):
        """获取 index-unknown-fileid 格式的 key

        Args:
            row (list[str]): xls_list 中的一行
        """
        file_id, unknown, index = row[1].split('-')
        return '-'.join((index, unknown, file_id))
