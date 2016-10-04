#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : lang_mgr_pair.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : .lang.csv 翻译时的管理工具
# 


from objs.lang_mgr_array import LangMgrArray


NAME_SUFFIX = 'name_'
DESC_SUFFIX = 'value'   # 为了排在 name 后


class LangMgrPair(LangMgrArray):
    """结果按 fileid-unknown-index 排序"""
    def __init__(self, translation_path, name_file_id, desc_file_id):
        """构造函数

        Args:
            translation_path (str): 翻译文件的路径
        name_file_id (str): “名字”文件的 ID
        desc_file_id (str): “描述”文件的 ID
        """
        super().__init__(translation_path=translation_path, file_id_list=[name_file_id, desc_file_id])

        self.name_lang_groups = self.all_lang_groups[name_file_id]
        self.desc_lang_groups = self.all_lang_groups[desc_file_id]
        self.name_id_pad, self.desc_id_pad = ('%09d' % int(v) for v in (name_file_id, desc_file_id))

    @staticmethod
    def get_header():
        return ['行号', '内部编号', '日文', '英文', '中文', '日文', '英文', '中文', '初翻人员', '校对', '润色', '备注']

    @staticmethod
    def get_named_header(name_title, desc_title):
        return [
            '行号', '内部编号',
            '日文%s' % name_title, '英文%s' % name_title, '中文%s' % name_title,
            '日文%s' % desc_title, '英文%s' % desc_title, '中文%s' % desc_title,
            '初翻人员', '校对', '润色', '备注'
        ]

    def to_xls_list(self, deduplicate=True):
        """转换为写入 .xlsx 翻译文件的列表

        按 index-unknown-fileid 排序

        Args:
            deduplicate (bool): 是否去重
        """
        # 生成列表（已按 index-unknown-name/value 排序，即先按 index-unknown 排序， index-unknown 相同的话 name 在前 ）
        # 注：此列表不能去重，去重操作在后面
        xls_list_single = super().to_xls_list(deduplicate=False)

        # 组织为 pair
        xls_by_index = {}
        for row in xls_list_single:
            index, unknown, file_type = self.get_key_for_row(row).split('-')
            # 构造新的行 (pair)
            if index not in xls_by_index:
                xls_by_index[index] = row[:2] + ['', ] * 6 + row[5:]
            if file_type == NAME_SUFFIX:
                xls_by_index[index][2:5] = row[2:5]
            elif file_type == DESC_SUFFIX:
                xls_by_index[index][5:8] = row[2:5]

        # 去重
        if deduplicate:
            duplicated_text = set()
            for index in sorted(xls_by_index.copy().keys()):
                row = xls_by_index[index]
                origin, origin_jp, origin_v, origin_v_jp = row[2], row[3], row[5], row[6]
                if (origin, origin_jp, origin_v, origin_v_jp) not in duplicated_text:
                    duplicated_text.add((origin, origin_jp, origin_v, origin_v_jp))
                else:
                    del xls_by_index[index]

        # 重新编号
        xls_list = []
        i = 0
        for index in sorted(xls_by_index.keys()):
            row = xls_by_index[index]
            row[0], row[1] = i, index
            xls_list.append(row)
            i += 1
        return xls_list

    def get_key_for_row(self, row):
        """获取 index-unknown-fileid 格式的 key

        Args:
            row (list[str]): xls_list 中的一行
        """
        key = super().get_key_for_row(row)
        return key.replace(self.name_id_pad, NAME_SUFFIX).replace(self.desc_id_pad, DESC_SUFFIX)
