#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : test_util.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 
# 


def xls_list_to_lines(xls_list):
    lines = []
    for row in xls_list:
        row_quoted = ['"%s"' % v for v in row]
        line = ','.join(row_quoted) + '\n'
        lines.append(line)
    return lines
