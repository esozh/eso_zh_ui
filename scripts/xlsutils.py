#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : xlsutils.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   :
#


import xlrd


def load_xls(file_path):
    """读取 Excel 文件中的数据。

    Args:
        file_path (str): xlsx 文件的路径
    """
    with xlrd.open_workbook(file_path) as workbook:
        sheet = workbook.sheet_by_index(0)
        nrows = sheet.nrows
        ncols = sheet.ncols
        data = []
        for curr_row in range(0, nrows):
            data.append([str(sheet.cell(curr_row, curr_col).value) for curr_col in range(0, ncols)])
        return data
