#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : setup_merge_xls_dir.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 合并文件的 cx_Freeze 脚本
# 


import sys
from cx_Freeze import setup, Executable


base = None
if sys.platform == 'win32':
    base = 'Console'

options = {
    'build_exe': {
        "packages": [
            "os",
        ],
        'includes': [
            'xlrd',
            'openpyxl',
        ]
    }
}

executables = [
    Executable('setup_merge_xls_dir_main.py', base=base, targetName='MergeXls.exe')
]

setup(name='合并翻译',
      version='0.5.14',
      description='bssthu, all rights reserved',
      options=options,
      executables=executables
      )
