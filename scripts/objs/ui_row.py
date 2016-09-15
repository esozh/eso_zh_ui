#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : ui_row.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : UI 翻译时 .xls 的一行
#


class UiRow:
    def __init__(self, name):
        """构造函数

        Args:
            name(str): SI_ 开头的名字
        """
        self.name = name        # 名字
        self.id = ''            # 编号
        self.origin = ''        # 原文
        self.translation = ''   # 译文
        self.translator = ''    # 初翻
        self.proofreader = ''   # 校对
        self.refiner = ''       # 润色
        self.comments = ''      # 备注

    def set_id(self, _id):
        self.id = _id
        return self

    def set_origin(self, origin):
        self.origin = origin
        return self

    def set_translation(self, translation):
        self.translation = translation
        return self

    def set_translator(self, translator):
        self.translator = translator
        return self

    def set_proofreader(self, proofreader):
        self.proofreader = proofreader
        return self

    def set_refiner(self, refiner):
        self.refiner = refiner
        return self

    def set_comments(self, comments):
        self.comments = comments
        return self

    def to_list(self):
        plain_list = [
            self.id, self.name, self.origin, self.translation,
            self.translator, self.proofreader, self.refiner, self.comments
        ]
        return [str(value) for value in plain_list]
