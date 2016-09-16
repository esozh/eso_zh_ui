#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : xlsutils.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   :
#


import xlrd
import xlwt


def load_xls(file_path):
    """读取 Excel 文件中的数据。

    Args:
        file_path (str): xlsx 文件的路径

    Returns:
        data (list[list[str]]): 工作表中的内容
    """
    data = []
    with xlrd.open_workbook(file_path) as workbook:
        sheet = workbook.sheet_by_index(0)
        nrows = sheet.nrows
        ncols = sheet.ncols
        for curr_row in range(0, nrows):
            data.append([str(sheet.cell(curr_row, curr_col).value) for curr_col in range(0, ncols)])
    return data


def save_xls(file_path, data, header=None, col_id=None):
    """将输入保存到 Excel 文件中。

    全部保存为文本。

    Args:
        file_path (str): xlsx 文件的路径
        data (list[list]): 要保存的数据，二维
        header (list): 第一行
        col_id (list[int]): data 中列号到 xlsx 中列号的映射
    """
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('sheet 1')

    row_id = 0
    # 保存第一行
    if header is not None:
        for j in range(0, len(header)):
            sheet.write(row_id, j, str(header[j]))
        row_id += 1

    num_col = len(data[0])
    if col_id is None:
        col_id = list(range(0, num_col))
    # 保存其他行
    for row in data:
        for j in range(0, num_col):
            sheet.write(row_id, col_id[j], str(row[j]))
        row_id += 1

    workbook.save(file_path)
